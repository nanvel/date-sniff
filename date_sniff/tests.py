from date_sniff.sniffer import DateSniffer


def test_years_separation():
    sniffer = DateSniffer(year=2019)
    assert sniffer.sniff('2019') == {'2019': []}
    assert sniffer.sniff('prefix 2019 and long text') == {'prefix 2019 and long text': []}
    res = {'prefix 2019 and long text another 2019': []}
    assert sniffer.sniff('prefix 2019 and long text another 2019') == res
    assert sniffer.sniff('2019 two 2019') == {'2019 two 2019': []}


def test_month_search():
    sniffer = DateSniffer(year=2019, month=1)
    assert sniffer.sniff('prefix 2019') == {}
    assert sniffer.sniff('prefix January 2019') == {'prefix January 2019': []}
    assert sniffer.sniff('prefix 2019-01-10') == {'prefix 2019-01-10': [10]}

    sniffer = DateSniffer(year=2019, month=3)
    res = sniffer.sniff('EXPANSION PLAN  Germany  Finland  Denmark  2019 Norway  Egypt  UAE  France  Spain  2021')
    assert res == {}
    res = sniffer.sniff('EXPANSION PLAN  Germany  Finland  March. 2019 Norway  Egypt  UAE  France  Spain  2021')
    assert res == {'EXPANSION PLAN  Germany  Finland  March. 2019 Norway  Egypt  UAE  France  Spain  2021': []}


def test_find_isolated():
    sniffer = DateSniffer(year=2019, month=3)
    res = sniffer.find_isolated('10', '2019-03-04 101')
    assert res == []


def test_keyword_search():
    sniffer = DateSniffer(year=2019, month=1, keyword='test')
    assert sniffer.sniff('prefix 2019-01-10') == {}
    print(sniffer.sniff('prefix 2019-01-10 test'))
    assert sniffer.sniff('prefix 2019-01-10 test') == {'prefix 2019-01-10 test': [10]}


def test_days():
    sniffer = DateSniffer(year=2019, month=3)
    res = sniffer.sniff('2019-03-04 101')
    assert res == {'2019-03-04 101': [4]}
