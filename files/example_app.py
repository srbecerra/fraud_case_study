from flask import Flask, render_template
import json
import requests
import time
from datetime import datetime
import socket
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, CollectionInvalid
import cPickle as pickle
from data_prep import get_data

app = Flask(__name__)
PORT = 5353
REGISTER_URL = "http://10.3.0.79:5000/register"
DATA = []
TIMESTAMP = []
COLUMNS = [#u'body_length',
 # u'name_length',
#  u'event_end',
#  u'venue_latitude',
#  u'event_published',
#  u'user_type',
#  u'channels',
 u'name',
 # u'currency',
# # # u'org_desc',
#  u'event_created',
#  u'approx_payout_date',
#  u'has_logo',
#  u'email_domain',
#  u'user_created',
#  u'payee_name',
#  u'payout_type',
#  u'venue_name',
#  u'sale_duration2',
#  u'venue_address',
#  u'event_start',
#  u'org_twitter',
#  u'gts',
#  u'listed',
#  u'ticket_types',
#  u'org_facebook',
#  u'num_order',
#  u'user_age',
#  u'org_name',
#  ## u'description',
 u'object_id',
 # u'venue_longitude',
 # u'fb_published',
 # u'previous_payouts',
 # u'sale_duration',
 # u'num_payouts',
 u'country',
#  u'delivery_method',
#  u'has_analytics',
#  u'venue_country',
#  u'venue_state',
#  u'has_header',
#  u'_id',
 # u'show_map',
 'prediction']

def get_datapoint():
    r = requests.get('http://galvanize-case-study-on-fraud.herokuapp.com/data_point')
    data = r.json()
    TIMESTAMP.append(time.time())

    if not live_data.find({'object_id':data['object_id']}).count():
        data['prediction'] = model.predict(get_data(data))[0]
        live_data.insert_one(data)
        # live_data.update_one({'object_id' : data[]},{'$set' : {'result' : 0}})
        print 'inserted datapoint'
    # print type(data)
    # X = get_data(data)
    # print model.predict(X)

def get_database_data():
    pings = [item for item in live_data.find()]
    items_list = [[x[y] for y in COLUMNS] for x in pings]
    html = '''<table><tr>'''
    # html = '''<tr>'''
    for col in COLUMNS:
        html += '<th>{}</th>'.format(col)
    html += '</tr>'
    for items in items_list:
        html += '<tr id={}>'.format(items[1])
        for c in items:
            if type(c)==unicode:
                html += '<td>{}</td>'.format(c.encode('utf-8','ignore'))
            else:
                html += '<td>{}</td>'.format(c)
        html += '</tr>'
    html += '</table>'
    return(html)
#   <tr>
#     <th>Company</th>
#     <th>Contact</th>
#     <th>Country</th>
#   </tr>
#   <tr>
#     <td>Alfreds Futterkiste</td>
#     <td>Maria Anders</td>
#     <td>Germany</td>
#   </tr>
# </table>


def print_table():
    pass

@app.route('/')
def check():
    # line1 = "Number of data points: {0}".format(len(DATA))
    # if DATA and TIMESTAMP:
    #     dt = datetime.fromtimestamp(TIMESTAMP[-1])
    #     data_time = dt.strftime('%Y-%m-%d %H:%M:%S')
    #     line2 = "Latest datapoint received at: {0}".format(data_time)
    #     line3 = data
    #     output = "{0}\n\n{1}\n\n{2}".format(line1, line2, line3)
    # else:
    #     output = line1
    # return output, 200, {'Content-Type': 'text/css; charset=utf-8'}
    html = render_template('starter_template.html', title='Hello!')
    html += '''<script type=text/javascript>

    $(function() {$('#tables')[0].innerHTML =` '''
    # {}}".format(get_database_data())
    # html += "'hi'"
    temp = get_database_data()
    html  = str(html)+temp
    # html = str.join(str(html), temp)
    # html = html + get_database_data()#.encode('utf-8','ignore')
    html += '''`});
    $(function() {
    var tmp = $('tr');
    var x;
    for (i=1;i<tmp.length;i++){
        console.log(tmp[i].children)
        if (tmp[i].children[3].innerHTML == '1.0'){
            tmp[i].style.backgroundColor = 'red';
        }
    }
    });
    </script>'''

    # get_database_data()
    return html
    # return get_database_data()

def register_for_ping(ip, port):
    registration_data = {'ip': ip, 'port': port}
    requests.post(REGISTER_URL, data=registration_data)

if __name__ == '__main__':
    with open('static/model.pkl') as f:
        model = pickle.load(f)

    # Connect to database
    db_cilent = MongoClient()
    fraud = db_cilent.get_database('fraud_case_study')
    live_data = fraud.get_collection('live_data')

    app.run(host='0.0.0.0', port=PORT, debug=True)

    while True:
        print 'running'
        time.sleep(10)
        get_datapoint()
