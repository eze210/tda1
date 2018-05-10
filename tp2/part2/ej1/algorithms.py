import kmp


class Shifted(object):
    """A class that allows shifting the index of an iterable.
    The iterable must support random access.

    >>> s = Shifted('hi!', 1)
    >>> assert s[0] == 'i'
    >>> assert s[1] == '!'
    >>> assert s[2] == 'h'
    """

    def __init__(self, iterable, start):
        self._iterable, self.start = iterable, start
        self._iterable_len = len(iterable)

    def __len__(self):
        return self._iterable_len

    def __getitem__(self, index):
        if not isinstance(index, int):
            raise TypeError
        return self._iterable[(index + self.start) % self._iterable_len]


def _strcmp(s1, s2):
    """Compares 2 string char by char and returns `True` if both are equal.
    Both strings are assumed to be of the same length."""

    for i in range(len(s1)):
        if s1[i] != s2[i]:
            return False
    return True


def naive(s1, s2):
    """Checks if `s2` is a permutation of `s1` using a naive algorithm."""

    if len(s1) != len(s2):
        return False
    for i in range(len(s2)):
        if _strcmp(s1, Shifted(s2, i)):
            return True
    return False


def naive_kmp(s1, s2):
    """Same as `naive` but using KMP instead of `_strcmp`."""

    if len(s1) != len(s2):
        return False

    # builds the shift table once
    T = kmp.get_shift_table(s1)
    for i in range(len(s2)):
        if kmp.kmp(Shifted(s2, i), s1, T=T) is not None:
            return True
    return False


def is_rotation(s1, s2):
    """Returns True if `s2` is a rotation of `s1` using one pass of KMP."""

    if len(s1) != len(s2):
        return False
    return kmp.kmp(s2 + s2, s1) is not None


if __name__ == '__main__':
    # runs a simple test for the algorithms
    for alg in (naive, naive_kmp, is_rotation):
        assert not alg('HOLA', 'HOLA!'), alg.__name__
        assert not alg('HOLAS', 'HOLSA'), alg.__name__
        assert not alg('HOLAS', 'HOALS'), alg.__name__
        assert alg('HOLAS', 'HOLAS'), alg.__name__
        assert alg('HOLAS', 'SHOLA'), alg.__name__
        assert alg('HOLAS', 'ASHOL'), alg.__name__
        assert alg('HOLAS', 'LASHO'), alg.__name__
        assert alg('HOLAS', 'OLASH'), alg.__name__

    print('OK!')
