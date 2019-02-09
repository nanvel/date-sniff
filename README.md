# Date sniffer

Looks for specified year or year/month dates in text.
Also can look for keywords around.

## Dependencies

Python 3.

`pytest` for tests.

## Usage

```python
from date_sniff import DateSniffer


sniffer = DateSniffer(year=2019, month=1, keyword="test", distance=10)
finds = sniffer.sniff("some text")
```
