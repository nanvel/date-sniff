from string import punctuation, whitespace


class DateSniffer:

    SNIPPET_BEFORE = 20
    SNIPPET_AFTER = 20
    MONTHS = [
        'january', 'february', 'march', 'april',
        'may', 'june', 'july', 'august',
        'september', 'october', 'november', 'december'
    ]

    def __init__(self, year, month=None, keyword=None, distance=20):
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

    def find_month(self, snippet):
        start = len(snippet) // 2 - self.distance
        stop = len(snippet) // 2 + self.distance
        if start < 0:
            start = 0
        if stop >= len(snippet):
            stop = len(snippet) - 1

        text = snippet[start:stop + 1].lower()

        month_name = self.MONTHS[self.month - 1]
        if month_name in text:
            return True

        for m in self.month_options:
            if m in text:
                return True

        return False

    def find_keyword(self, snippet):
        start = len(snippet) // 2 - self.distance
        stop = len(snippet) // 2 + self.distance
        if start < 0:
            start = 0
        if stop >= len(snippet):
            stop = len(snippet) - 1
        return self.keyword.lower() in snippet.lower()[start:stop + 1]

    def sniff(self, text):
        year_positions = []
        start = 0
        borders = punctuation + whitespace
        while True:
            found = text.find(self.year, start)
            if found == -1:
                break
            start = found + 1
            if found > 0 and text[found - 1] not in borders:
                continue
            if found + len(self.year) < len(text) - 1 and text[found + len(self.year)] not in borders:
                continue
            year_positions.append(found)

        results = []
        for pos in year_positions:
            snippet_start = pos - self.SNIPPET_BEFORE
            if snippet_start < 0:
                snippet_start = 0
            snippet_stop = pos + len(str(self.year)) + self.SNIPPET_AFTER
            if snippet_stop >= len(text):
                snippet_stop = len(text) - 1

            while snippet_start > 0:
                if text[snippet_start] not in borders:
                    snippet_start -= 1
                else:
                    snippet_start += 1
                    break

            while snippet_stop < len(text):
                if text[snippet_stop] not in borders:
                    snippet_stop += 1
                else:
                    snippet_stop -= 1
                    break

            snippet = text[snippet_start: snippet_stop + 1]

            if self.month and not self.find_month(snippet=snippet):
                continue

            if self.keyword and not self.find_keyword(snippet=snippet):
                continue

            if snippet_start > 0:
                snippet = '... ' + snippet
            if snippet_stop < len(text) - 1:
                snippet = snippet + ' ...'

            if snippet not in results:
                results.append(snippet)

        return results
