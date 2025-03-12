import os
import tempfile
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file

from tools.error.error_tool import ErrorTool
from tools.json_validate.json_validate_tool import JsonValidatorTool
from tools.word_count.word_count_tool import WordCountTool
from tools.dec_to_bin.dec_to_bin_tool import DecToBinTool
from tools.base64_encode.base64_encode_tool import Base64EncodeTool
from tools.base64_decode.base64_decode_tool import Base64DecodeTool
from tools.file_size_calculator.file_size_calculator_tool import FileSizeCalculatorTool
from tools.qr_code_generator.qr_code_generator_tool import QrCodeGeneratorTool
from tools.number_converter.number_converter_tool import NumberConverterTool
from tools.image_converter.image_converter_tool import ImageConverterTool
from tools.word_counter.word_counter_tool import WordCounterTool
from tools.password_generator.password_generator_tool import PasswordGeneratorTool

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Hier müssen wir nur unsere Tools registrieren
tools = {
    "WordCountTool": WordCountTool(),
    "JsonValidatorTool": JsonValidatorTool(),
    "DecToBinTool": DecToBinTool(),
    "ErrorTool": ErrorTool(),
    "Base64EncodeTool": Base64EncodeTool(),
    "Base64DecodeTool": Base64DecodeTool(),
    "FileSizeCalculatorTool": FileSizeCalculatorTool(),
    "QrCodeGeneratorTool": QrCodeGeneratorTool(),
    "NumberConverterTool": NumberConverterTool(),
    "ImageConverterTool": ImageConverterTool(),
    "WordCounterTool": WordCounterTool(),
    "PasswordGeneratorTool": PasswordGeneratorTool()
}

# Hauptseite


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
    return render_template('variable_input_mask.jinja', toolName=tool.name, input_params=tool.input_params, identifier=tool.identifier)

# Output


@app.route("/handle_tool", methods=["POST"])
def handle_tool():
    tool_name = request.form.get('tool_name')
    tool = tools.get(tool_name)

    if not tool:
        return "Tool not found", 404

    input_params = {}

    # Handle file uploads
    if request.files:
        temp_dir = tempfile.gettempdir()  # Get system's temp directory

        for key, file in request.files.items():
            if file.filename != '':
                # Save the file to the system's temp directory
                file_path = os.path.join(temp_dir, file.filename)
                file.save(file_path)
                # Store both the file object and path
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


if __name__ == "__main__":
    app.run(debug=True)
