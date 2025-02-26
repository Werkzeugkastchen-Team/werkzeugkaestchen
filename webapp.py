from flask import Flask, render_template, request

from tools.error.error_tool import ErrorTool
from tools.json_validate.json_validate_tool import JsonValidatorTool
from tools.word_count.word_count_tool import WordCountTool
from tools.dec_to_bin.dec_to_bin_tool import DecToBinTool
app = Flask(__name__)

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
    
        