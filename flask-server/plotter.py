from bokeh.plotting import figure
from bokeh.palettes import Category20_20
from bokeh.embed import components

used_tools = 'hover,wheel_zoom,reset,pan'
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
            continue
        try:
            data = line.split(",")
            if '\"' in data[0]:
                continue
            try:
                int(data[0])
            except ValueError: # not an int -->> it is header string
                for name in data:
                    names.append(name)
                lines_data = [list() for _ in range(len(names))]
                continue # jump to next line
            # index is int() compatible
            indexes.append(int(data[0]))
            for i in range(1, len(data)):
                lines_data[i].append(float(data[i]))
        except:
            pass

    plt = figure(name = "bokeh_jinja_figure",title=f"Air-correction charts of {filePass}", x_axis_label="argument", y_axis_label="data",
                 width=1500, height=800, tools=used_tools,tooltips= TOOLTIPS, toolbar_location="below")

    pallete = Category20_20.__iter__()
    for i in range(1,len(names)):
        plt.line(indexes, lines_data[i], legend_label =f"{names[i]}", color=next(pallete))

    plt.add_layout(plt.legend[0],'right')
    plt.legend.click_policy="hide"

    return plt