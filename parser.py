import lxml.html as html
from pandas import DataFrame

main_domain_stat = 'http://hosteddb.fightmetric.com'
page = html.parse('%s/events/index/date/desc/1/all' % (main_domain_stat))
e = page.getroot().find_class('b-statistics__table-events').pop()

tbody = e.getchildren().pop()

events_tabl = DataFrame([{'EVENT':i[0].text, 'LINK':i[2]} for i in tbody.iterlinks()])

trs = tbody.getchildren()

event_date = DataFrame([{'EVENT': evt.getchildren()[0].getchildren()[0].getchildren()[0].text, 'DATE':evt.getchildren()[0].getchildren()[0].getchildren()[1].text} for evt in trs[1:]])

sum_event_link = events_tabl.set_index('EVENT').join(event_date.set_index('EVENT')).reset_index()

sum_event_link.to_csv('list_ufc_events.csv',';',index=False)
