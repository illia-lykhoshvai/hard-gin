from bokeh.plotting import figure
from bokeh.models import Spinner
from bokeh.layouts import column,row
from bokeh.palettes import Category20_20
from bokeh.embed import components

used_tools = 'hover,wheel_zoom,box_zoom,reset,pan'
TOOLTIPS = [ 
    ("argument is", "@x"),
    ("data is", "@y")
]

def getPlotComponents(file: str):
    return components(getPlot(file))

def getPlot(filePass: str):
    with open(filePass, 'r') as f:
        dataLines = f.readlines()
    names = list()
    indexes = list()
    lines_data = list()

    for line in dataLines:
        if "sep=" in line: # .csv needed line
            separator = line.strip("sep=").rstrip('\n')
            continue
        try:
            data = line.split(separator)
            if '\"' in data[0]:
                continue # browser-related info
            try:
                int(data[0])
            except ValueError: # not an int -->> it is header string
                for name in data:
                    names.append(name)
                lines_data = [list() for _ in range(len(names)-1)]
                continue # jump to next line
            # index is int() compatible
            indexes.append(int(data[0]))
            for i in range(1, len(data)):
                lines_data[i-1].append(float(data[i]))
        except:
            pass

    fig = figure(name = "bokeh_jinja_figure", title=f"Air-correction charts of {filePass}", 
                 x_axis_label="argument", y_axis_label="data",
                 sizing_mode="stretch_both",
                 tools=used_tools, tooltips= TOOLTIPS, toolbar_location="below")
    
    controls = {
        "y_range/start": Spinner(title="Y_start", step=1, value=-10),
        "y_range/end": Spinner(title="Y_end", step=1, value=10),
        "x_range/start": Spinner(title="X_start", low=0, step=1, value=0),
        "x_range/end": Spinner(title="X_end", low=1, step=1)
    }
    
    for name in controls.keys():
        name_list = name.split('/')
        controls[name].js_link('value', getattr(fig, name_list[0]), name_list[1])
        
    controls_array = controls.values()

    palette = Category20_20.__iter__()
    for i in range(len(names)-1):
        fig.line(indexes, lines_data[i], legend_label =f"{names[i+1]}", color=next(palette))

    fig.add_layout(fig.legend[0],'right')
    fig.legend.click_policy="hide"

    controls = row(*controls_array)
    plt = column([fig, controls])
    plt.sizing_mode = "stretch_both"
    
    return plt
