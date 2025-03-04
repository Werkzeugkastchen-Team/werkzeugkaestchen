from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

from tools.error.error_tool import ErrorTool
from tools.json_validate.json_validate_tool import JsonValidatorTool
from tools.word_count.word_count_tool import WordCountTool
from tools.dec_to_bin.dec_to_bin_tool import DecToBinTool

app = Flask(__name__)
app.secret_key = 'supersecretkey' 

# Hier müssen wir nur unsere Tools registrieren
tools = {
    "WordCountTool": WordCountTool(),
    "JsonValidatorTool": JsonValidatorTool(),
    "DecToBinTool": DecToBinTool(),
    "ErrorTool": ErrorTool()
}

# Hauptseite
@app.route('/')
def index():
    tools_classes = []
    for name,tool in tools.items():
        tools_classes.append(tool)
    return render_template('index.jinja', toolsToRender=tools_classes)

@app.route("/search_tools", methods=["GET"])
def search_tools():
    query = request.args.get("q", "").lower()
    filtered_tools = [tool for tool in tools if query in tool["name"].lower() or query in tool["description"].lower()]
    return jsonify(filtered_tools)

if __name__ == "__main__":
    app.run(debug=True)


# /contact
@app.route('/contact')
def contact():
    return render_template('contact.jinja') 

#/about
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
    
    input_params = request.form.to_dict()
    
    # remove non-tool input params
    input_params.pop('tool_name', None)
    
    # from 'on' to True because Forms
    for key, value in input_params.items():
        if value == 'on':
            input_params[key] = True
    
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