from date_sniff.sniffer import DateSniffer


def test_years_separation():
    sniffer = DateSniffer(year=2019)
    assert sniffer.sniff('2019') == ['2019']
    assert sniffer.sniff('prefix 2019 and long text') == ['prefix 2019 and long text']
    res = [
        'prefix 2019 and long text another ...',
        '... and long text another 2019'
    ]
    assert sniffer.sniff('prefix 2019 and long text another 2019') == res
    assert sniffer.sniff('2019 two 2019') == ['2019 two 2019']


def test_month_search():
    sniffer = DateSniffer(year=2019, month=1)
    assert sniffer.sniff('prefix 2019') == []
    assert sniffer.sniff('prefix January 2019') == ['prefix January 2019']
    assert sniffer.sniff('prefix 2019-01-10') == ['prefix 2019-01-10']


def test_keyword_search():
    sniffer = DateSniffer(year=2019, month=1, keyword='test')
    assert sniffer.sniff('prefix 2019-01-10') == []
    assert sniffer.sniff('prefix 2019-01-10 test') == ['prefix 2019-01-10 test']
