import lxml.html as html
from pandas import DataFrame

main_domain_stat = 'http://www.fightmetric.com'
page = html.parse('%s/statistics/events/completed?page=all' % (main_domain_stat))
e = page.getroot().find_class('b-statistics__table-events').pop()
tbody = e.getchildren().pop()

events_tabl = DataFrame([{'EVENT':i[0].text, 'LINK':i[2]} for i in tbody.iterlinks()][2:])

trs = tbody.getchildren()

event_date = DataFrame([{'EVENT': evt.getchildren()[0].getchildren()[0].getchildren()[0].text, 'DATE':evt.getchildren()[0].getchildren()[0].getchildren()[1].text} for evt in trs[2:]])

sum_event_link = events_tabl.set_index('EVENT').join(event_date.set_index('EVENT')).reset_index()


all_fights = []
for i in sum_event_link.itertuples():
    detail_page_link = i[2]
    detail_page = html.parse(detail_page_link)
    table = detail_page.getroot().find_class("b-fight-details__table b-fight-details__table_style_margin-top b-fight-details__table_type_event-details js-fight-table")[0]
    tbody = table.getchildren()[1]
    tr = tbody.getchildren()[0]
    tds = tr.getchildren()[1:]

    fighter_win = tds[0].getchildren()[0].getchildren()[0].text
    fighter_lose = tds[0].getchildren()[1].getchildren()[0].text
    method = tds[6].getchildren()[0].text
    method_desc = tds[6].getchildren()[1].text
    round_ = tds[7].getchildren()[0].text
    time = tds[8].getchildren()[0].text

    all_fights.append({
        'FIGHTER LOSE': fighter_lose,
        'FIGHTER_WIN': fighter_win,
        'METHOD': method,
        'METHOD_DESC': method_desc,
        'ROUND': round_,
        'TIME': time
    })
    history_stat = DataFrame(all_fights)
    history_stat.to_csv('all_fights.csv',';',index=False)
#===============================================================================
