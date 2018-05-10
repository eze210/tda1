def Z(s):
    """Runs the Z algorithm on the string `s` and the returns
    the array of Z boxes."""

    Z = [len(s)] + [-1] * (len(s) - 1)
    l = r = 0
    for k in range(1, len(s)):
        if k > r:
            n = 0
            while n + k < len(s) and s[n + k] == s[n]:
                n += 1
            Z[k] = n
            r = n + k - 1
            l = k
        else:
            if Z[k - l] < r - k + 1:
                Z[k] = Z[k-l]
            else:
                n = r + 1
                while n < len(s) and s[n] == s[n - r + l]:
                    n += 1
                Z[k] = n - k
                l, r = k, n - 1
    return Z


def get_shift_table(P):
    """Returns the table that handles the shifts of the KMP algorithm."""

    z = Z(P)
    T2 = [0] * len(P)
    for i in reversed(range(1, len(P))):
        T2[i + z[i] - 1] = z[i]

    T = [0] * len(P)
    T[-1] = T2[-1]
    for i in reversed(range(1, len(P) - 1)):
        T[i] = max(T2[i], T[i+1] - 1)

    return T


def kmp(S, P, T=None):
    """Finds the first repetition of `P` in `S` and returns the index in `S` where it starts
    or None if it wasn't found.
    Optionally, the table of shifts for the pattern can be passed if already computed."""

    # builds the shiting table
    T = T or get_shift_table(P)

    # begins searching
    s = p = 0
    while s < len(S) - len(P) + p + 1:
        while p < len(P) and S[s] == P[p]:
            s += 1
            p += 1
        if p == len(P):
            return s - len(P)
        elif p == 0:
            s += 1
        else:
            p = T[p-1]

    # no match found
    return None


if __name__ == '__main__':
    # some unit tests
    assert Z('aabcaabxaaaz') == [12, 1, 0, 0, 3, 1, 0, 0, 2, 2, 1, 0], Z('aabcaabxaaaz')
    assert Z('aaaaa') == [5, 4, 3, 2, 1], Z('aaaaa')
    assert Z('baaaaa') == [6, 0, 0, 0, 0, 0], Z('baaaaa')
    assert Z('baabaa') == [6, 0, 0, 3, 0, 0], Z('baaaaa')
    assert Z('macri gato') == [10, 0, 0, 0, 0, 0, 0, 0, 0, 0], Z('macri gato')
    assert Z('ana banana') == [10, 0, 1, 0, 0, 3, 0, 3, 0, 1], Z('ana banana')
    assert Z('anana banana') == [12, 0, 3, 0, 1, 0, 0, 5, 0, 3, 0, 1], Z('anana banana')
    assert Z('anana bananana') == [14, 0, 3, 0, 1, 0, 0, 5, 0, 5, 0, 3, 0, 1], Z('anana bananana')
    assert Z('anana anana anana') == [17, 0, 3, 0, 1, 0, 11, 0, 3, 0, 1, 0, 5, 0, 3, 0, 1], Z('anana banana')

    assert kmp('hola', 'la') == 2, kmp('hola', 'la')
    assert kmp('hola', 'ho') == 0, kmp('hola', 'ho')
    assert kmp('hola', 'holas') == None, kmp('hola', 'holas')
    assert kmp('bananas', 'anas') == 3, kmp('bananas', 'anas')
    assert kmp('aaaabaaabaaabaaaaab', 'aaaaab') == 13, kmp('aaaabaaabaaabaaaaab', 'aaaaab')
    assert kmp('aaabbbaabbbaabbaaabbbaaa', 'aabbbaaa') == 16, kmp('aaabbbaabbbaabbaaabbbaaa', 'aabbbaaa')

    print('OK!')
