# coding: utf-8

import sys
import timeit
import dataset
import sorting


ALGORITHMS = [f for f in dir(sorting) if callable(getattr(sorting, f)) and not f.startswith('_')]
USAGE = """
Calcula los tiempos de ejecución de un algoritmo de ordenamiento para distintos
tamaños de listas, promediando entre varias ejecuciones.

Uso: ./{} semilla algoritmo

  semilla       La semilla utilizada para generar los datos (int).
  algoritmo     El algoritmo al cuál ejecutarle las pruebas:
                  * """.format(__file__) + '\n                  * '.join(ALGORITHMS)

TIMEIT_SETUP = """
from copy import copy
from sorting import {algorithm}

data = copy(basedata)
"""


def test(algorithm, seed):
    """Runs the test on a given `algorithm`, obtaining a dataset with the given `seed`."""

    iterations = 100

    print(algorithm)
    print('n,time (ms)')
    for n in (50, 100, 500, 1000, 2000, 3000, 4000, 5000, 7500, 10000):
        basedata = dataset.get_data(10000, seed=seed)[:n]

        rv = timeit.timeit('{}(data)'.format(algorithm),
                           setup=TIMEIT_SETUP.format(algorithm=algorithm),
                           number=iterations,
                           globals={'basedata': basedata})
        print('{},{:.4f}'.format(n, rv/iterations * 1000))


if __name__ == '__main__':
    if '--help' in sys.argv or '-h' in sys.argv:
        print(USAGE)
        exit(0)
    if len(sys.argv) != 3:
        print(USAGE)
        exit(1)

    seed, algorithm = int(sys.argv[1]), sys.argv[2]
    if algorithm not in ALGORITHMS:
        print('Algoritmo "{}" no soportado'.format(algorithm))
        print("Usar './{} --help' para ver las opciones".format(__file__))
        exit(1)

    test(algorithm, seed)
