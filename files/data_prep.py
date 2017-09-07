import pandas as pd
import numpy as np
import json

def get_data(json_object):
    '''
    Unpacking the fraud ticket information and dropping irrelevant data. 'Live' data will not have labels

    json_object -- the json output from the 'live' data
    '''

    model_data = pd.DataFrame.from_dict(json_object,orient='index').T
    model_data['num_ticket_type'] = model_data['ticket_types'].map(lambda x: parse_tickets(x)[0])
    model_data['avg_ticket_cost'] = model_data['ticket_types'].map(lambda x: parse_tickets(x)[1])
    model_data['avg_ticket_tot_cnt'] = model_data['ticket_types'].map(lambda x: parse_tickets(x)[2])
    model_data['avg_ticket_sold_cnt'] = model_data['ticket_types'].map(lambda x: parse_tickets(x)[3])
    model_data['event_age_at_start(days)'] = (model_data['event_start'] - model_data['event_created'])/86400.0
    model_data = model_data[['num_ticket_type', 'avg_ticket_cost', 'avg_ticket_tot_cnt', 'avg_ticket_sold_cnt', 'event_age_at_start(days)']]
    model_data = model_data.dropna()
    X = model_data.as_matrix()
    return X

def parse_tickets(ticket_types):
    '''
    Collapse differet ticket types into four attributes: number of types, average cost, average total number of each type, and average sold

    ticket_types -- the ticket_types column from the fraud json data
    '''
    num_ticket_type = len(ticket_types)
    costs = []
    totals = []
    sold = []
    for ticket in ticket_types:
        costs.append(ticket['cost'])
        totals.append(ticket['quantity_total'])
        sold.append(ticket['quantity_sold'])
    return [num_ticket_type, np.mean(costs), np.mean(totals), np.mean(sold)]

if __name__ == '__main__':
    pass
    #X, y = get_data()
