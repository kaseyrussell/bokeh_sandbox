import pandas as pd
from bokeh.io import curdoc
from bokeh.models.widgets import (
    CheckboxGroup,
)
from bokeh.layouts import column, row, WidgetBox
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import TableColumn, DataTable
from bokeh.palettes import Dark2_5 as palette
import itertools
from scripts.database_interface import get_netzsch_items_with_excel_files, get_upload
from io import BytesIO

p = figure(plot_width=500, plot_height=400)
color_iterator = itertools.cycle(palette)

available_samples = get_netzsch_items_with_excel_files()
available_file_names = []
for sample in available_samples:
    available_file_names += sample['excel_names']

colors = dict()
# for sample in available_samples:
#     colors[sample['id']] = next(color_iterator)
for file_name in available_file_names:
    colors[file_name] = next(color_iterator)

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

    # not optimized!!
    for sample in available_samples:
        for file_name, upload_id in zip(sample['excel_names'], sample['excel_ids']):
            if file_name in selected_file_names:
                obj = get_upload(upload_id)
                df = pd.read_excel(BytesIO(obj.content))
                temperature_arrays.append(df['Temperature (K)'])
                seebeck_arrays.append(df['Seebeck (V/K)'])
                color_array.append(colors[file_name])
                label_array.append(f"{file_name}")

    #
    # for f in selected_file_names:
    #     df = pd.read_excel(Path(f))
    #     temperature_arrays.append(df['Temperature (K)'])
    #     seebeck_arrays.append(df['Seebeck (V/K)'])
    #     color_array.append(colors[f])
    #     label_array.append(f"{f}")

    return ColumnDataSource(dict(temperature=temperature_arrays, seebeck=seebeck_arrays, color=color_array,
                                   label=label_array))


def update(attr, old, new):
    selected_samples = [sample_selection.labels[i] for i in sample_selection.active]
    new_source = get_data(selected_samples)
    source.data.update(new_source.data)
    print("Updated!")


sample_selection = CheckboxGroup(labels=available_file_names, active = [0])
sample_selection.on_change('active', update)

selected_samples = [sample_selection.labels[i] for i in sample_selection.active]
source = get_data(selected_samples)

p.multi_line('temperature', 'seebeck', line_width=2, source=source, color='color', legend='label')
p.xaxis.axis_label = 'Temperature (degC)'
p.yaxis.axis_label = 'Seebeck coefficient (V/K)'
p.legend.location = 'bottom_right'

columns = ['label', '']

curdoc().add_root(row(sample_selection, p))

