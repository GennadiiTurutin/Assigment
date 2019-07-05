import pandas as pd
from datetime import datetime
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components

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

class Graph:
    def __init__(self, type ):
        self.type = type

    def get_data(self):

        return options[self.type]

    def get_graph(self):

        data = self.get_data()

        if self.type[:3] == 'GEN':
            x = [datetime.date(data.index[k]) for k in range(data.shape[0])]
            y1 = data.iloc[:, 0]
            y2 = data.iloc[:, 1]

            graph = figure(title=self.type, x_axis_type='datetime', x_axis_label='all data', y_axis_label="temp or el. usage ", plot_height=200)
            graph.line(x, y1, legend="Outdoor temperature", line_width=2)
            graph.line(x, y2, legend="Electricity usage",line_color="orange", line_width=2)
            graph.sizing_mode = "scale_width"
            script, div = components(graph)
            

        if self.type[:13] == 'C_EL_U/O_TEMP':

            x = data.iloc[:, 0]
            y = data.iloc[:, 1]

            graph = figure(title=self.type, x_axis_label='Electricity usage', y_axis_label="Outside temperature", plot_height=200)
            graph.scatter(x, y, legend="Graph electricity usage vs. outdoor temperature", size=50, alpha=0.5)
            graph.sizing_mode = "scale_width"
            script, div = components(graph)

        if self.type[:6] == 'O_TEMP':
            x = [datetime.date(data.index[k]) for k in range(data.shape[0])]
            y = data

            graph = figure(title=self.type, x_axis_type='datetime', x_axis_label='time', y_axis_label="Outside temperature", plot_height=200)
            graph.line(x, y, legend="Graph of outdoor temperature vs. time", line_width=2)
            graph.sizing_mode = "scale_width"
            script, div = components(graph)

        if self.type[:4] == 'EL_U':
            x = [datetime.date(data.index[k]) for k in range(data.shape[0])]
            y = data

            graph = figure(title=self.type, x_axis_type='datetime', x_axis_label='time', y_axis_label="Electricity usage", plot_height=200)
            graph.line(x, y, legend="Graph electricity usage vs. time", line_width=2)
            graph.sizing_mode = "scale_width"
            script, div = components(graph)

        return script, div
