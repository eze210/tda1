# coding: utf-8

"""
Genera un set de datos con números ordenados aleatoriamente en formato csv.

Uso: ./dataset.py n [archivo de salida]

  n   Cantidad de números
  Si el archivo de salida no se especifica, imprime por stdout
"""

import sys
import random


def get_data(n, seed=None):
    if seed is not None:
        random.seed(seed)
    l = [i for i in range(n)]
    random.shuffle(l)
    return l


if __name__ == '__main__':
    if len(sys.argv) not in (2, 3):
        print(__doc__)
        exit(1)

    n = int(sys.argv[1])
    output = sys.stdout
    if len(sys.argv) == 3:
        output = open(sys.argv[2], 'w')

    data = get_data(n, seed=0)
    output.write(','.join(map(str, data)))

    output.close()
