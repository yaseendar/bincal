__author__ = 'yaseen'

import calendar
import re


from flask import Flask, render_template

app = Flask(__name__)

from flask import request


@app.route('/')
def show_form():
    return render_template('bintable.html')


@app.route('/getmycal',  methods=['POST'])
def hello_world():
    year = request.form['year']
    month = request.form['month']
    if not month:
        html_cal = calendar.HTMLCalendar(calendar.MONDAY).formatyear(int(year), width=3)
    else:
        html_cal = calendar.HTMLCalendar(calendar.MONDAY).formatmonth(int(year), int(month))

    return make_binary(html_cal)


def make_binary(html_cal):
    new_html = """<style>
            td,th{
                padding: 4px!important;
            }
            table{
                margin: 20px!important;
            }
            .sun, .sat{
            color:red!important;
            }
        </style>"""
    myre = re.compile('([0-9]+)(<)')
    find_calendar = re.finditer(myre, html_cal)
    prev_end = 0
    for val in find_calendar:
        rang = val.span()
        start = rang[0]
        end = rang[1]
        if prev_end == 0:
            new_html += html_cal[prev_end:start]
            new_html += bin(int(html_cal[start:end - 1]))[2:]
        else:
            new_html += html_cal[prev_end:start]
            new_html += bin(int(html_cal[start:end - 1]))[2:]
        prev_end = end - 1
    daylist = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    monlist = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
               "October", "November", "December"]
    day_mon = ['1', '10', '11', '100', '101', '110', '111', '1000', '1001', '1010', '1011', '1100']
    for indx, day in enumerate(daylist):
        new_html = new_html.replace(day, day_mon[indx])
    for indx, day in enumerate(monlist):
        new_html = new_html.replace(day, day_mon[indx])

    return new_html


if __name__ == '__main__':
    app.run()
