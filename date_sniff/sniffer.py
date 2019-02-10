from string import punctuation, whitespace


class DateSniffer:

    SNIPPET_BEFORE = 40
    SNIPPET_AFTER = 40
    MONTH = [
        'january', 'february', 'march', 'april',
        'may', 'june', 'july', 'august',
        'september', 'october', 'november', 'december'
    ]
    MONTH_ABBR = [
        'jan', 'feb', 'mar', 'apr', 'may', 'jun',
        'jul', 'aug', 'sept', 'oct', 'nov', 'dec'
    ]
    MONTH_DAYS = [
        31, 29, 31, 30, 31, 30,
        31, 31, 30, 31, 30, 31
    ]
    BORDERS = punctuation + whitespace

    def __init__(self, year, month=None, keyword=None, distance=10):
        if not isinstance(year, int) or year > 3000 or year < 1000:
            raise ValueError("Invalid year format")

        if month is not None:
            if not isinstance(month, int) or month > 12 or month < 1:
                raise ValueError("Invalid month")

        self.distance = distance
        self.year = str(year)
        self.month = month
        self.keyword = keyword

        month_options = []
        if month:
            month_options.append('{:04}-{:02}-'.format(year, month))
            month_options.append('{:04}/{:02}/'.format(year, month))
            for i in range(1, 32):
                month_options.append('{:02}/{:02}/{:04}'.format(month, i, year))
        self.month_options = month_options

    def find_isolated(self, keyword, text):
        start = 0
        locations = []
        while True:
            found = text.find(keyword, start)
            if found == -1:
                break
            start = found + 1

            if found > 0 and text[found - 1] not in self.BORDERS:
                continue
            if found + len(keyword) < len(text) and text[found + len(keyword)] not in self.BORDERS:
                continue
            locations.append(found)
        return locations

    def find_month(self, snippet):
        start = len(snippet) // 2 - (self.distance + 10)  # compensate month length
        stop = len(snippet) // 2 + self.distance
        if start < 0:
            start = 0
        if stop >= len(snippet):
            stop = len(snippet) - 1

        text = snippet[start:stop + 1].lower()

        if self.find_isolated(keyword=self.MONTH[self.month - 1], text=text):
            return True

        if self.find_isolated(keyword=self.MONTH_ABBR[self.month - 1], text=text):
            return True

        for m in self.month_options:
            if m in text:
                return True

        return False

    def find_days(self, snippet):
        """
        Try to find isolated 1-{max days in the month} numbers.
        If there month == number: check patterns mon/day/year, year-month-day, year/month/day
        """
        snippet = snippet.replace(self.year, ' ')
        days = []
        for i in range(1, self.MONTH_DAYS[self.month] + 1):
            keys = [str(i)]
            if i < 10:
                keys.append('{:02}'.format(i))
            for key in keys:
                if key in snippet and self.find_isolated(keyword=key, text=snippet):
                    days.append(i)

        if not days:
            return []

        result = set()
        for d in days:
            if d == self.month:
                if '{:02}/{:02}/{}'.format(self.month, d, self.year) in snippet:
                    result.add(d)
                elif '{}-{:02}-{:02}'.format(self.year, self.month, d) in snippet:
                    result.add(d)
                elif '{}/{:02}/{:02}'.format(self.year, self.month, d) in snippet:
                    result.add(d)
                elif '{}/{}/{}'.format(self.month, d, self.year) in snippet:
                    result.add(d)
                elif '{}/{}/{}'.format(self.year, self.month, d) in snippet:
                    result.add(d)
            else:
                result.add(d)

        return list(result)

    def find_keyword(self, snippet):
        start = len(snippet) // 2 - self.distance
        stop = len(snippet) // 2 + self.distance
        if start < 0:
            start = 0
        if stop >= len(snippet):
            stop = len(snippet) - 1
        return self.keyword.lower() in snippet.lower()[start:stop + 1]

    def sniff(self, text):
        year_positions = self.find_isolated(keyword=self.year, text=text)

        results = {}
        for pos in year_positions:
            snippet_start = pos - self.SNIPPET_BEFORE
            if snippet_start < 0:
                snippet_start = 0
            snippet_stop = pos + len(str(self.year)) + self.SNIPPET_AFTER
            if snippet_stop >= len(text):
                snippet_stop = len(text) - 1

            while snippet_start > 0:
                if text[snippet_start] not in self.BORDERS:
                    snippet_start -= 1
                else:
                    snippet_start += 1
                    break

            while snippet_stop < len(text):
                if text[snippet_stop] not in self.BORDERS:
                    snippet_stop += 1
                else:
                    snippet_stop -= 1
                    break

            snippet = text[snippet_start: snippet_stop + 1]

            if self.month and not self.find_month(snippet=snippet):
                continue

            if self.keyword and not self.find_keyword(snippet=snippet):
                continue

            if self.month:
                days = self.find_days(snippet=snippet)
            else:
                days = []

            if snippet_start > 0:
                snippet = '... ' + snippet
            if snippet_stop < len(text) - 1:
                snippet = snippet + ' ...'

            snippet = snippet.replace('\n', ' ').replace('\t', ' ')

            if snippet not in results:
                results[snippet] = list(sorted(days))
            else:
                results[snippet] = list(sorted(set(results[snippet] + days)))

        return dict(results)
