from flask import Flask, render_template
import json
import requests
import time
from datetime import datetime
import socket
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, CollectionInvalid
import cPickle as pickle
from data_prep import get_data, parse_tickets

app = Flask(__name__)
PORT = 5353
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
 # u'ticket_types',
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
 'potential_cost',
 'prediction']

def get_datapoint():
    '''
        Retrieves datapoint from external server and inserts datapoint into MongoDB
    '''
    r = requests.get('http://galvanize-case-study-on-fraud.herokuapp.com/data_point')
    data = r.json()

    if not live_data.find({'object_id':data['object_id']}).count():
        data['prediction'] = model.predict(get_data(data))[0]
        data['potential_cost'] = parse_tickets(data['ticket_types'])[-1]
        live_data.insert_one(data)
        print 'inserted datapoint'

def get_database_data():
    '''
        Retreieves database information and extracts only columns in COLUMNS.
        Returns html of datbase table.
    '''
    pings = [item for item in live_data.find()]
    pings = pings[::-1]
    items_list = [[x[y] for y in COLUMNS] for x in pings]

    html = '''<thead><tr>'''
    for col in COLUMNS:
        html += '<th>{}</th>'.format(col)
    html += '</tr></thead>'
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

@app.route('/')
def check():
    '''
    Returns: html of template plus script
    '''

    html = render_template('starter_template.html', title='Hello!')
    html += '''<script type=text/javascript>

    $(function() {$('#tables')[0].innerHTML =` '''
    temp = get_database_data()
    html  = str(html)+temp
    html += '''`});

    $(function() {
        var tmp = $('tr');
        var x;
        for (i=1;i<tmp.length;i++){
            if (tmp[i].children[4].innerHTML == '1.0'){
                tmp[i].style.backgroundColor = 'red';
            }
        }
    });

    </script>'''
    return html

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
        get_datapoint()
        time.sleep(10)
