from flask import Flask, render_template, request

from tools.json_validate.json_validate_tool import JsonValidatorTool
from tools.word_count.word_count_tool import WordCountTool

app = Flask(__name__)

tools = {
    "WordCountTool": WordCountTool(),
    "JsonValidatorTool": JsonValidatorTool()
}


@app.route('/')
def index():
    tools_classes = []
    for name,tool in tools.items():
        tools_classes.append(tool)
    return render_template('index.jinja', toolsToRender=tools_classes)


@app.route("/tool/<tool_name>")
def tool_form(tool_name):
    tool = tools.get(tool_name)
    if not tool:
        return "Tool not found", 404
    return render_template('variable_input_mask.jinja', toolName=tool.name, input_params=tool.input_params)


@app.route("/handle_tool", methods=["POST"])
def handle_tool():
    print(request.form)
    tool_name = request.form.get('tool_name')
    tool = tools.get(tool_name)
    
    if not tool:
        return "Tool not found", 404
    
    input_params = request.form.to_dict()
    
    # Remove the tool_name from input_params
    input_params.pop('tool_name', None)
    
    # Convert boolean values from 'on' to True because Forms
    for key, value in input_params.items():
        if value == 'on':
            input_params[key] = True
    
    tool.execute_tool(input_params)
    
    return render_template('output.html', output_text=tool.output)