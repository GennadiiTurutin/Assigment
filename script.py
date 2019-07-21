import pandas as pd
from datetime import datetime
from bokeh.plotting import figure, show, output_file, Figure
from bokeh.embed import components
from bokeh.layouts import column
from bokeh.models import CustomJS, ColumnDataSource, Slider, LinearAxis, Range1d
from bokeh.layouts import gridplot
from bokeh.models import HoverTool


data = pd.read_excel("data.xlsx", index_col=0)
df = pd.DataFrame(data=data)
df = df.fillna(df.mean())

options = {
    'GEN':   df,
    'GEN_Y': df.resample('Y').mean(),
    'GEN_M': df.resample('M').mean(),
    'GEN_W': df.resample('W').mean(),
    'GEN_D': df.resample('D').mean(),
    'GEN_H': df.resample('H').mean(),

    'O_TEMP':   df["out_door_temp"],
    'O_TEMP_Y': df["out_door_temp"].resample("Y").mean(),
    'O_TEMP_M': df["out_door_temp"].resample("M").mean(),
    'O_TEMP_W': df["out_door_temp"].resample("W").mean(),
    'O_TEMP_D': df["out_door_temp"].resample("D").mean(),
    'O_TEMP_H': df["out_door_temp"].resample("H").mean(),

    'EL_U':   df["electricity_usage"],
    'EL_U_Y': df["electricity_usage"].resample("Y").mean(),
    'EL_U_M': df["electricity_usage"].resample("M").mean(),
    'EL_U_W': df["electricity_usage"].resample("W").mean(),
    'EL_U_D': df["electricity_usage"].resample("D").mean(),
    'EL_U_H': df["electricity_usage"].resample("H").mean(),

    'C_EL_U/O_TEMP':   df,
    'C_EL_U/O_TEMP_Y': df.resample('Y').mean(), 
    'C_EL_U/O_TEMP_M': df.resample('M').mean(),
    'C_EL_U/O_TEMP_W': df.resample('W').mean(),
    'C_EL_U/O_TEMP_D': df.resample('D').mean(),
    'C_EL_U/O_TEMP_H': df.resample('H').mean()
}

TOOLS = "pan,save,box_zoom,box_select,lasso_select,help,tap,wheel_zoom,xwheel_zoom,ywheel_zoom,reset,crosshair"

CALLBACK_1 = """
                const x = source.data['x']
                const y = source.data['y']
                const coef = slider.value
                for (var i = 0; i < x.length; i++) {
                        y[i] = Math.pow(y_base[i], coef)
                }
                source.change.emit()
             """

CALLBACK_2 = """
                const x = source.data['x']
                const y1 = source.data['y1']
                const y2 = source.data['y2']
                const coef = slider.value
                for (var i = 0; i < x.length; i++) {
                        y1[i] = Math.pow(y1_base[i], coef)
                        y2[i] = Math.pow(y2_base[i], coef)
                }
                source.change.emit()
             """

class Graph:

    def __init__(self, type ):

        self.type = type

    def get_data(self):

        return options[self.type]

    def get_graph(self):

        data = self.get_data()

        slider = Slider(start=0.8, end=1.2, value=1, step=.001, title="Power", bar_color='red')

        if self.type[:3] == 'GEN':
            x = [datetime.date(data.index[k]) for k in range(data.shape[0])]
            y1 = data.iloc[:, 0]
            y2 = data.iloc[:, 1]
            source = ColumnDataSource(data=dict(x=x, y1=y1, y2=y2))
            graph = figure(tools=TOOLS, 
                           title=self.type, 
                           x_axis_type='datetime', 
                           x_axis_label='date', 
                           y_axis_label="el. usage ", 
                           plot_height=200, 
                           y_range=(0, 4000,))
            graph.line('x', 'y1',  
                       source=source, 
                       legend="Outdoor temperature", 
                       color='orange',
                       alpha=0.5, 
                       y_range_name="temperature",
                       line_width=1)
            graph.line('x', 'y2',  
                       source=source, 
                       legend="Electricity usage",
                       hover_line_color="red", 
                       alpha=0.5, 
                       line_width=1).hover_glyph.line_width=2

            graph.extra_y_ranges = {"temperature": Range1d(start=0, end=100)}
            graph.add_layout(LinearAxis(y_range_name="temperature", axis_label='temperature'), 'right')

            graph.add_tools(HoverTool(
                tooltips=[
                    ("y", "$y{0}"),
                    ("date", '@x{%F}'),
                ],
                formatters={'x': 'datetime'}
            ))
            callback = CustomJS(
                                args=dict(
                                    source=source, 
                                    y1_base=y1, 
                                    y2_base=y2,
                                    slider=slider), 
                                code=CALLBACK_2
            )

        if self.type[:13] == 'C_EL_U/O_TEMP':
            x = data.iloc[:, 0]
            y = data.iloc[:, 1]
            source = ColumnDataSource(data=dict(x=x, y=y))
            graph = Figure(tools=TOOLS, 
                           title=self.type, 
                           y_axis_label='Electricity usage', 
                           x_axis_label="Outside temperature", 
                           plot_height=200, 
                           y_range=(0, 4000))
            
            graph.add_tools(HoverTool(
                tooltips=[
                    ("El. usage", "$y{0}"),
                    ("Out. temp.", "$x"),
                ]
            ))
            graph.scatter('x', 'y', 
                          source=source, 
                          legend="Graph electricity usage vs. outdoor temperature", 
                          alpha=0.5, 
                          size=10)
            callback = CustomJS(
                                args=dict(
                                    source=source, 
                                    y_base=y, 
                                    slider=slider), 
                                code=CALLBACK_1
                                )

        if self.type[:6] == 'O_TEMP':
            x = [datetime.date(data.index[k]) for k in range(data.shape[0])]
            y = data
            source = ColumnDataSource(data=dict(x=x, y=y))
            graph = Figure(tools=TOOLS, 
                           title=self.type, 
                           x_axis_type='datetime', 
                           x_axis_label='date', 
                           y_axis_label="Outside temperature", 
                           plot_height=200,  
                           y_range=(0, 100))
            graph.line('x', 'y', 
                        source=source, 
                        legend="Graph of outdoor temperature vs. time", 
                        line_width=1,
                        alpha=0.5, 
                        hover_line_color="red"
                        ).hover_glyph.line_width=2
            
            graph.add_tools(HoverTool(
                tooltips=[
                    ("Out. temp", "$y{0}"),
                    ("date", '@x{%F}'),
                ],
                formatters={'x': 'datetime'}
            ))
            callback = CustomJS(
                               args=dict(
                                source=source, 
                                y_base=y, 
                                slider=slider
                                ), 
                               code=CALLBACK_1
                                )

        if self.type[:4] == 'EL_U':
            x = [datetime.date(data.index[k]) for k in range(data.shape[0])]
            y = data
            source = ColumnDataSource(data=dict(x=x, y=y))
            graph = Figure(tools=TOOLS, 
                           title=self.type, 
                           x_axis_type='datetime', 
                           x_axis_label='date', 
                           y_axis_label="Electricity usage", 
                           plot_height=200, 
                           y_range=(0, 4000)
                           )
            graph.line('x', 'y', 
                       source=source, 
                       legend="Graph electricity usage vs. time", 
                       line_width=1,
                       hover_line_color="red",
                       alpha=0.5, 
                       ).hover_glyph.line_width=2
            graph.add_tools(HoverTool(
                tooltips=[
                    ("El. usage", "$y{0}"),
                    ("date", '@x{%F}'),
                ],
                formatters={'x': 'datetime'}
            ))
            callback = CustomJS(
                                args=dict(
                                    source=source, 
                                    y_base=y, 
                                    slider=slider), 
                                code=CALLBACK_1
                                )
        else: 
            pass

        slider.js_on_change('value', callback)
        layout = column(slider, graph, sizing_mode = "scale_width" )
        script, div = components(layout)

        return script, div
