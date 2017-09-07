import pandas as pd
import numpy as np
import json

def get_data(json_object):
    '''
    Unpacking the fraud ticket information and dropping irrelevant data. 'Live' data will not have labels

    Input:
    json file or buffer

    Returns:
    X - feature matrix without indicies
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
    Collapse differet ticket types into numerical representations.

    Input:
    ticket_types column for single event

    Returns:
    [number of types, average cost, average total number of each type, average sold, total payout]
    '''
    num_ticket_type = len(ticket_types)
    costs = []
    totals = []
    sold = []
    payout = 0
    for ticket in ticket_types:
        costs.append(ticket['cost'])
        totals.append(ticket['quantity_total'])
        sold.append(ticket['quantity_sold'])
        payout += ticket['cost'] * ticket['quantity_sold']
    return [num_ticket_type, np.mean(costs), np.mean(totals), np.mean(sold), payout]

def parse_payouts(payout_history):
    '''
    Summary of payout history.

    Input:
    Previous_payouts column for single event
    Returns:
    [number of previous payouts, the average payout amount, total paid out]
    '''
    num_payouts = len(payout_history)
    avg_payout = []
    total_payout = []
    amounts = []
    for payout in payout_history:
        amounts.append(payout['amount'])
    avg_payout = np.mean(amounts)
    total_payout = np.sum(amounts)
    return [num_payouts, avg_payout, total_payout]

if __name__ == '__main__':
    pass
    #X, y = get_data()
