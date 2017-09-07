## Pre-EDA Notes
- Data from ads (possibly google) (has_analytics, fb info, venue, paid)
- Time columns are in seconds (from unix time, 1/1/1970)
- Toss categorical columns. Do not have explanation
- Some key columns (like currency, payout type), some signal in NLP (html code)

## EDA Notes
- Ticket columns seem much more likely to contain the signal
    - Cannot split data into ticket per row (rather than event per row) since the labels were not applied that way. We would be making an assumption that each ticket type in a fraudulent event is equally guilty when that may not be the case.

## Model
- Ticket and payout columns have event ids. If i could get that id out we could see if a current fraudulent event had past events in our data set that were also fraudulent. Also applies to the live stream of data
- Feature importances for ticket, event age model:
    - avg_ticket_sold_cnt is      54.1% part of the signal
    - event_age_at_start(days) is 24.0% part of the signal
    - avg_ticket_cost is          11.0% part of the signal
    - avg_ticket_tot_cnt is       8.6% part of the signal
    - num_ticket_type is          2.4% part of the signal
- Feature importances for all numerical model (parsed tickets, payouts and dropped text columns):
    - Importances looked like they were distributed normally. Range was 0% - 10%. with most btwn 1%-5%
- Other classes (spam, etc) have huge payouts, some bigger than fraud. To be conservative, we assume these are all possible fraud. This may help with the class imbalance too
