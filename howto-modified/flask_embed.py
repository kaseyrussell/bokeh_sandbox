# From the official bokeh howto
# https://github.com/bokeh/bokeh/blob/master/examples/howto/server_embed/flask_embed.py
# run with python flask_embed.py and open http://127.0.0.1:8000/ in a web browser.
# (or maybe open http://localhost:8000/ in a browser...)

from threading import Thread

from flask import Flask, render_template
from tornado.ioloop import IOLoop

from bokeh.embed import server_document
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure
from bokeh.server.server import Server
from bokeh.themes import Theme
import numpy as np

app = Flask(__name__)

def get_data(num_scans=10):
    """
    Make some fake data
    :return:
    """
    data_dict = dict(sample_names=[])
    for i in range(num_scans):
        temp = np.linspace(20, 200, 8)
        seebeck = 100e-6 + 20e-6 * np.random.random(len(temp))
        sample_name = "{:03d}".format(np.random.randint(999))
        data_dict['sample_names'].append(sample_name)
        data_dict[f'{sample_name}_temp'] = temp
        data_dict[f'{sample_name}_seebeck'] = seebeck

    return ColumnDataSource(data_dict)


def bkapp(doc):
    source = get_data()
    plot = figure(x_axis_label='Temperature (Celsius)', y_range=(0, 200e-6), y_axis_label='Seebeck Coefficient (V/K)',
                  title="Seebeck Coefficient vs Temperature")
    for sample_name in source.data['sample_names']:
        plot.line(f'{sample_name}_temp', f'{sample_name}_seebeck', legend=sample_name, source=source)

    def callback(attr, old, new):
        source.data = get_data(new)

    slider = Slider(start=1, end=10, value=10, step=1, title="Number of curves to plot")
    slider.on_change('value', callback)

    doc.add_root(column(slider, plot))

    doc.theme = Theme(filename="theme.yml")


@app.route('/', methods=['GET'])
def bkapp_page():
    script = server_document('http://localhost:5006/bkapp')
    return render_template("embed.html", script=script, template="Flask")


def bk_worker():
    # Can't pass num_procs > 1 in this configuration. If you need to run multiple
    # processes, see e.g. flask_gunicorn_embed.py
    server = Server({'/bkapp': bkapp}, io_loop=IOLoop(), allow_websocket_origin=["localhost:8000"])
    server.start()
    server.io_loop.start()

Thread(target=bk_worker).start()

if __name__ == '__main__':
    print('Opening single process Flask app with embedded Bokeh application on http://localhost:8000/')
    print()
    print('Multiple connections may block the Bokeh app in this configuration!')
    print('See "flask_gunicorn_embed.py" for one way to run multi-process')
    app.run(port=8000)
