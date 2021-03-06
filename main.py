#!/usr/bin/env python

from collections import namedtuple
import requests

from flask import Flask, request, redirect, render_template


app = Flask(__name__)


def get_stop_list():
    bus_stop = namedtuple(
        'bus_stop',
        ['mpk_id', 'rozklady_lodz_id', 'stop_name', 'latitude', 'longitude'])

    indexes = [2, 0, 1, 5, 4]

    url = 'http://rozklady.lodz.pl/Home/GetMapBusStopList'
    resp = requests.post(url).json()

    stop_list = {}
    for entry in resp:
        record = bus_stop(*[entry[i] for i in indexes])
        stop_list[record.mpk_id] = record
    return stop_list


STOP_LIST = get_stop_list()


@app.route('/')
def main_view():
    return '''
    <form action="/redirect"><input name="mpk_id">
    '''


@app.route('/redirect')
def redirect_view():
    mpk_id = str(int(request.args['mpk_id']))
    rozklady_lodz_id = str(STOP_LIST[mpk_id].rozklady_lodz_id)
    url = 'http://rozklady.lodz.pl/Home/TimeTableReal?busStopId=' + rozklady_lodz_id
    return redirect(location=url)


@app.route('/frames/<comma_separated_mpk_ids>')
def frames_view(comma_separated_mpk_ids):
    mpk_ids = comma_separated_mpk_ids.split(',')
    return render_template('frames.html', mpk_ids=mpk_ids, percentage=int(100/len(mpk_ids)))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
