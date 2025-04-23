import os
import tempfile
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file, session
from flask_babel import Babel, gettext as _
from markupsafe import Markup

from tools.base64_encode.base64_encode_tool import Base64EncodeTool
from tools.base64_decode.base64_decode_tool import Base64DecodeTool
from tools.file_size_calculator.file_size_calculator_tool import FileSizeCalculatorTool
from tools.qr_code_generator.qr_code_generator_tool import QrCodeGeneratorTool
from tools.number_converter.number_converter_tool import NumberConverterTool
from tools.image_converter.image_converter_tool import ImageConverterTool
from tools.word_counter.word_counter_tool import WordCounterTool
from tools.password_generator.password_generator_tool import PasswordGeneratorTool
from tools.calendar_week.calendar_week_tool import CalendarWeekTool
from tools.image_cropper.image_cropper_tool import ImageCropperTool
from tools.random_number_generator.random_number_generator_tool import RandomNumberGeneratorTool
from tools.audio_converter.audio_converter_tool import AudioConverterTool
from tools.text_to_speech.text_to_speech_tool import TextToSpeechTool
from tools.unix_timestamp.unix_timestamp_tool import UnixTimestampTool
from tools.texte_vergleichen.texte_vergleichen_tool import TexteVergleichenTool
from tools.json_validieren.json_validieren_tool import JSONValidierungTool
from tools.json_formatieren.json_formatieren_tool import JSONFormatierungTool
from tools.unit_converter.unit_converter_tool import UnitConverterTool
from tools.date_calculator.date_calculator_tool import DateCalculatorTool
from tools.placeholder_text.placeholder_text_tool import PlaceholderTextTool
from tools.color_converter.color_converter_tool import ColorConverterTool
from tools.gif_video_converter.gif_video_converter_tool import GifVideoConverterTool
from tools.whisper_subtitle.whisper_subtitle_tool import WhisperSubtitleTool
from tools.pdf_split.pdf_split_tool import PdfSplitTool
from tools.text_summary.text_summary_tool import TextSummaryTool
from tools.pdf_merge.pdf_merge_tool import PdfMergeTool


# Erstellen einer Flask-Anwendung
app = Flask(__name__)

# Festlegen eines geheimen Schlüssels für die Anwendung.
# Dieser Schlüssel wird für die Sitzungsverwaltung und andere sicherheitsrelevante Funktionen verwendet.
app.secret_key = 'supersecretkey'


# Sprachauswahl-Funktion
def get_locale():
    # Versuche Sprache aus der Session zu holen (wenn Benutzer manuell gewählt hat)
    if 'language' in request.args:
        session['language'] = request.args.get('language')
    if 'language' in session:
        return session['language']
    # Ansonsten Browser-Einstellungen verwenden
    return request.accept_languages.best_match(['de', 'en'])

# Babel konfigurieren mit neuerer API
babel = Babel(app)
app.config['BABEL_DEFAULT_LOCALE'] = 'de'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'
babel.init_app(app, locale_selector=get_locale)


# Hier müssen wir nur unsere Tools registrieren
tools = {
    "Base64EncodeTool": Base64EncodeTool(),
    "Base64DecodeTool": Base64DecodeTool(),
    "FileSizeCalculatorTool": FileSizeCalculatorTool(),
    "QrCodeGeneratorTool": QrCodeGeneratorTool(),
    "NumberConverterTool": NumberConverterTool(),
    "ImageConverterTool": ImageConverterTool(),
    "WordCounterTool": WordCounterTool(),
    "CalendarWeekTool": CalendarWeekTool(),
    "RandomNumberGeneratorTool": RandomNumberGeneratorTool(),
    "PasswordGeneratorTool": PasswordGeneratorTool(),
    "ImageCropperTool": ImageCropperTool(),
    "AudioConverterTool": AudioConverterTool(),
    "TextToSpeechTool": TextToSpeechTool(),
    "UnixTimestampTool": UnixTimestampTool(),
    "TexteVergleichenTool": TexteVergleichenTool(),
    "JSONValidierungTool": JSONValidierungTool(),
    "JSONFormatierungTool": JSONFormatierungTool(),
    "UnitConverterTool": UnitConverterTool(),
    "DateCalculatorTool": DateCalculatorTool(),
    "PlaceholderTextTool": PlaceholderTextTool(),
    "ColorConverterTool": ColorConverterTool(),
    "WhisperSubtitleTool": WhisperSubtitleTool(),
    "PdfSplitTool": PdfSplitTool(),
    "GifVideoConverterTool": GifVideoConverterTool(),
    "TextSummaryTool": TextSummaryTool(),
    "PdfMergeTool": PdfMergeTool()
}


@app.route('/')
def index():
    tools_classes = []
    for name, tool in tools.items():
        tools_classes.append(tool)
    return render_template('index.jinja', toolsToRender=tools_classes)


@app.route("/search_tools", methods=["GET"])
def search_tools():
    query = request.args.get("q", "").lower()
    filtered_tools = []

    for tool_id, tool in tools.items():
        if query in tool.name.lower() or query in tool.description.lower():
            filtered_tools.append({
                "name": tool.name,
                "description": tool.description,
                "identifier": tool.identifier
            })

    return jsonify(filtered_tools)

# /contact


@app.route('/contact')
def contact():
    return render_template('contact.jinja')

# /about


@app.route('/about')
def about():
    return render_template('about.jinja')

# Input


@app.route("/tool/<tool_name>")
def tool_form(tool_name):
    tool = tools.get(tool_name)
    if not tool:
        return "Tool not found", 404

    # Spezielle Behandlung für bestimmte Tools
    if tool_name == "ColorConverterTool":
        return render_template('color_converter.html')
    elif tool_name == "GifVideoConverterTool":
        return render_template('gif_video_converter.jinja')
    elif tool_name == "ImageCropperTool":
        return render_template('image_cropper.jinja')  # Spezielles Template für den Image Cropper

    # Regulärer Ablauf für andere Tools
    return render_template('variable_input_mask.jinja',
                          tool=tool,
                          toolName=tool.name,
                          input_params=tool.input_params,
                          identifier=tool.identifier)


@app.route("/handle_tool", methods=["POST"])
def handle_tool():
    tool_name = request.form.get('tool_name')
    tool = tools.get(tool_name)

    if not tool:
        return "Tool not found", 404

    input_params = {}

    # Handle file uploads
    temp_dir = tempfile.gettempdir()

    if request.form.get("tool_name") == "PdfMergeTool":
        uploaded_files = request.files.getlist("pdf_files")
        files_info = []

        for file in uploaded_files:
            if file and file.filename.lower().endswith(".pdf"):
                file_path = os.path.join(temp_dir, file.filename)
                file.save(file_path)
                files_info.append({
                    "file_obj": file,
                    "file_path": file_path,
                    "filename": file.filename
                })

        input_params["pdf_files"] = files_info
        input_params["pdf_order"] = request.form.get("pdf_order", "")

    else:
        for key, file in request.files.items():
            if file and file.filename != '':
                file_path = os.path.join(temp_dir, file.filename)
                file.save(file_path)
                input_params[key] = {
                    "file_obj": file,
                    "file_path": file_path,
                    "filename": file.filename
                }


    # Handle form inputs
    for key, value in request.form.items():
        if key != 'tool_name':
            if value == 'on':
                input_params[key] = True
            else:
                input_params[key] = value

    success = tool.execute_tool(input_params)

    if not success:
        return render_template('output.html',
                               toolName=tool.name,
                               output_text=tool.error_message,
                               has_error=True)

    return render_template('output.html',
                           toolName=tool.name,
                           output_text=tool.output)


@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    message = request.form.get('message')
    privacy_policy = request.form.get('privacy_policy')

    if not name or not email or not message or privacy_policy is None:
        flash("Bitte füllen Sie alle Pflichtfelder aus und stimmen Sie der Datenschutzerklärung zu.", "error")
        return redirect(url_for('contact'))

    print(f"Neue Kontaktanfrage von {name} ({email}, {phone}): {message}")

    flash("Vielen Dank für Ihre Nachricht! Wir werden uns so schnell wie möglich bei Ihnen melden.", "success")
    return redirect(url_for('contact_success'))


@app.route('/contact_success')
def contact_success():
    return render_template('contact_success.jinja')


@app.route('/download/<token>')
def download_converted_image(token):
    image_tool = tools.get("ImageConverterTool")
    if not image_tool:
        return "Tool nicht gefunden", 404

    temp_path = image_tool.convert_and_save(token)
    if not temp_path:
        return "Konvertierung fehlgeschlagen oder Token ungültig", 404

    # Get the original filename from pending_conversions
    filename = image_tool.pending_conversions[token]['filename']

    # Send the file with the original filename
    response = send_file(temp_path, as_attachment=True, download_name=filename)

    # Schedule cleanup after response is sent
    @response.call_on_close
    def cleanup():
        # Mark as downloaded and cleanup
        image_tool.pending_conversions[token]['downloaded'] = True
        image_tool.cleanup_old_files()

    return response


@app.route('/download_crop/<token>')
def download_cropped_image(token):
    image_tool = tools.get("ImageCropperTool")
    if not image_tool:
        return "Tool nicht gefunden", 404

    temp_path = image_tool.crop_and_save(token)
    if not temp_path:
        return "Zuschneiden fehlgeschlagen oder Token ungültig", 404

    # Get the original filename from pending_crops
    filename = image_tool.pending_crops[token]['filename']

    # Send the file with the original filename
    response = send_file(temp_path, as_attachment=True,
                         download_name=f"cropped_{filename}")

    # Schedule cleanup after response is sent
    @response.call_on_close
    def cleanup():
        # Mark as downloaded and cleanup
        image_tool.pending_crops[token]['downloaded'] = True
        image_tool.cleanup_old_files()

    return response


@app.route('/download_audio/<token>')
def download_converted_audio(token):
    audio_tool = tools.get("AudioConverterTool")
    if not audio_tool:
        print("Error: AudioConverterTool not found")
        return "Tool nicht gefunden", 404

    # Check if the conversion exists
    if token not in audio_tool.pending_conversions:
        print(f"Error: Invalid or expired download token: {token}")
        return "Ungültiger oder abgelaufener Download-Token", 404

    try:
        # Convert the audio file
        temp_path = audio_tool.convert_and_save(token)
        if not temp_path:
            print(f"Error: Failed to convert audio file for token: {token}")
            return "Konvertierung fehlgeschlagen", 500

        if not os.path.exists(temp_path):
            print(f"Error: Converted file not found at: {temp_path}")
            return "Konvertierte Datei nicht gefunden", 404

        # Get file info
        conversion = audio_tool.pending_conversions[token]
        filename = conversion['filename']
        target_format = conversion['target_format']

        # Set the correct content type based on the target format
        content_types = {
            'mp3': 'audio/mpeg',
            'wav': 'audio/wav',
            'aac': 'audio/mp4',  # Changed from audio/aac to audio/mp4 for .m4a files
            'flac': 'audio/flac'
        }
        content_type = content_types.get(
            target_format, 'application/octet-stream')

        # Verify file size
        file_size = os.path.getsize(temp_path)
        if file_size == 0:
            print(f"Error: Converted file is empty: {temp_path}")
            return "Konvertierte Datei ist leer", 500

        print(f"Sending file: {filename} ({content_type}, {file_size} bytes)")

        # Send the file with the correct content type and filename
        response = send_file(
            temp_path,
            as_attachment=True,
            download_name=filename,
            mimetype=content_type
        )

        # Schedule cleanup after response is sent
        @response.call_on_close
        def cleanup():
            try:
                # Mark as downloaded and cleanup
                audio_tool.pending_conversions[token]['downloaded'] = True
                audio_tool.cleanup_old_files()
            except Exception as e:
                print(f"Error during cleanup: {str(e)}")

        return response

    except Exception as e:
        print(f"Error in download_converted_audio: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return "Fehler beim Senden der Datei", 500


@app.route('/download_converted_media/<token>', methods=['GET', 'POST'])
def download_converted_media(token):
    converter_tool = tools.get("GifVideoConverterTool")
    if not converter_tool:
        return "Tool nicht gefunden", 404

    temp_path = converter_tool.convert_and_save(token)
    if not temp_path:
        return "Konvertierung fehlgeschlagen oder Token ungültig", 404

    # Original-Dateiname aus pending_conversions abrufen
    conversion = converter_tool.pending_conversions[token]
    is_gif = conversion["is_gif"]

    # Ausgabenamen bestimmen
    if is_gif:
        # GIF zu Video
        format = conversion.get("format", "mp4")
        filename = os.path.splitext(conversion["filename"])[0] + f".{format}"
    else:
        # Video zu GIF
        filename = os.path.splitext(conversion["filename"])[0] + ".gif"

    # Datei mit dem Original-Dateinamen senden
    response = send_file(temp_path, as_attachment=True, download_name=filename)

    # Cleanup nach dem Senden der Antwort planen
    @response.call_on_close
    def cleanup():
        # Als heruntergeladen markieren und aufräumen
        converter_tool.pending_conversions[token]['downloaded'] = True
        converter_tool.cleanup_old_files()

    return response




if __name__ == "__main__":
    app.run(debug=True)
