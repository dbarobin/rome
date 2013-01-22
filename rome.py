from itertools import count


__version__ = '0.0.2'


_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}


class Roman(int):

    def __new__(class_, roman):
        try:
            roman = int(roman)
        except ValueError:
            roman = str(roman).upper().replace(' ', '')
            if not set(_map) >= set(roman):
                raise ValueError('Not a valid Roman numeral: %r' % roman)
            values = [_map[r] for r in roman]
            value = sum(-i if i < j else i
                        for i, j in zip(values, values[1:] + [0]))
            return super(Roman, class_).__new__(class_, value)
        else:
            if roman < 1:
                raise ValueError('Only n > 0 allowed, given: %r' % roman)
            return super(Roman, class_).__new__(class_, roman)

    def _negatively(self):
        base, s = sorted((v, k) for k, v in _map.items() if v >= self)[0]
        decrement = base - self
        if decrement == 0:
            return s
        else:
            return Roman(decrement)._positively() + s

    def _positively(self):
        value = self
        result = ''
        while value > 0:
            for v, r in reversed(sorted((v, k) for k, v in _map.items())):
                if v <= value:
                    value -= v
                    result += r
                    break
        return result

    def _split(self):
        result = []
        for i in (10 ** i for i in count()):
            if i > self:
                break
            result.append(self % (i * 10) / i * i)
        return result[::-1]

    def __str__(self):
        s = ''
        for n in self._split():
            if n == 0:
                continue
            pos = Roman(n)._positively()
            neg = Roman(n)._negatively()
            s += neg if len(neg) < len(pos) else pos
        return s

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.__str__())
