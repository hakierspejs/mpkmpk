from collections import namedtuple
import requests

from flask import Flask, request, redirect

app = Flask(__name__)


def get_stop_list():
    bus_stop = namedtuple(
        'bus_stop',
        ['stop_id', 'time_table_id', 'stop_name', 'latitude', 'longitude'])

    indexes = [2, 0, 1, 5, 4]

    url = 'http://rozklady.lodz.pl/Home/GetMapBusStopList'
    resp = requests.post(url).json()

    ret = {}
    for entry in resp:
        record = bus_stop(*[entry[i] for i in indexes])
        ret[record.stop_id] = record
    return ret


STOP_LIST = get_stop_list()


@app.route('/')
def main_view():
    return '''
    <form action="/redirect"><input name="stop_id">
    '''


@app.route('/redirect')
def redirect_view():
    stop_id = str(int(request.args['stop_id']))
    new_id = str(STOP_LIST[stop_id].time_table_id)
    url = 'http://rozklady.lodz.pl/Home/TimeTableReal?busStopId=' + new_id
    return redirect(location=url)

if __name__ == '__main__':
    app.run()
