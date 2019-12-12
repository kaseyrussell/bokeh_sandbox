import pandas as pd
from bokeh.io import curdoc
from bokeh.models.widgets import (
    CheckboxGroup,
)
from bokeh.layouts import column, row, WidgetBox
from pathlib import Path
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.palettes import Dark2_5 as palette
import itertools

p = figure(plot_width=500, plot_height=400)
color_iterator = itertools.cycle(palette)

available_samples = [f"{f}" for f in Path('data/').glob('*.xlsx')]
available_samples.sort()

colors = dict()
for sample in available_samples:
    colors[sample] = next(color_iterator)

def get_data(selected_file_names):
    """
    Compile data into a ColumnDataSource for plotting
    :param selected_file_names:
    :return:
    """
    temperature_arrays = []
    seebeck_arrays = []
    color_array = []
    label_array = []

    for f in selected_file_names:
        df = pd.read_excel(Path(f))
        temperature_arrays.append(df['Temperature (K)'])
        seebeck_arrays.append(df['Seebeck (V/K)'])
        color_array.append(colors[f])
        label_array.append(f"{f}")

    return ColumnDataSource(dict(temperature=temperature_arrays, seebeck=seebeck_arrays, color=color_array,
                                   label=label_array))


def update(attr, old, new):
    selected_samples = [sample_selection.labels[i] for i in sample_selection.active]
    new_source = get_data(selected_samples)
    source.data.update(new_source.data)
    print("Updated!")


sample_selection = CheckboxGroup(labels=available_samples, active = [])
sample_selection.on_change('active', update)

selected_samples = [sample_selection.labels[i] for i in sample_selection.active]
source = get_data(selected_samples)

p.multi_line('temperature', 'seebeck', line_width=2, source=source, color='color', legend='label')
p.xaxis.axis_label = 'Temperature (degC)'
p.yaxis.axis_label = 'Seebeck coefficient (V/K)'
p.legend.location = 'bottom_right'
p.legend.click_policy = 'hide'

curdoc().add_root(row(sample_selection, p))

