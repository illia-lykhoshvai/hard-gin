from flask import Blueprint, render_template, abort
import os.path, os
from plotter import getPlotComponents

browser = Blueprint('browser', __name__)

class file:
    name = str()
    parameters = list(str())

    def __init__(self, init_name : str, init_param : list(str()) ) -> None:
        self.name = init_name
        self.parameters = init_param

@browser.route('/', defaults={'req_path': ''})
@browser.route('/<path:req_path>')
def list_dir(req_path):
    BASE_DIR = os.path.join(os.getcwd(),'..\logs')
    
    # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR, req_path)
    
    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        script, div = getPlotComponents(abs_path)
        return render_template('viewer.html', script = script, div = div)

    # Show directory contents
    table = list()
    filelist = [file_name for file_name in os.listdir(abs_path) if ".csv" in file_name]
    for file_name in filelist:
        f_data = file(init_name= file_name, init_param= getParameters(abs_path + file_name))
        table.append(f_data)
    return render_template('browser.html', files_table=table)

def getParameters (file_path: str) -> list:
    parsed_parameters = list(str())
    if ".csv" in file_path:
        f = open(file_path, 'r')
        for line in f:
            if "sep=" in line:
                continue # skip first line
            # second line is needed
            if not '\"' in line:
                return [""] 
            line = line.replace('\"', '')
            line = line.split(",")
            i = 0
            for data in line:
                i += 1
                line[i-1] = str(i) + ". " + data
            parsed_parameters = line
            break
    return parsed_parameters