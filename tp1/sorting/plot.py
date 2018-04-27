# coding: utf-8

__doc__ = f"""
Uso: {__file__} [-h/--help] DATOS.CSV FUNC

Donde DATOS.CSV es un archivo CSV con los datos de las mediciones.
FUNC es en nombre de la función con la cual comparar.

Al ejecutarse exitosamente el script, se crea un archivo llamado <DATOS>.png
que contiene el gráfico con los datos.

DATOS.CSV debe tener un formato como el siguiente:

  encabezado_1,encabezado_2
  n_2,medicion_1
  ...
  n_n,medicion_n

FUNC puede tomar los valores:
  * n2 (cuandratico)
  * nlogn (n*log(n))
"""

import os
import sys
import numpy as np
import matplotlib
matplotlib.use('agg')
from matplotlib import pyplot as plt


def least_squares(A, b):
    """Given a matrix `A` and a vector `b`, returns an approximated solution to the equation Ax=b"""

    # x = inv(A'A)A'b
    m = np.linalg.inv(A.transpose().dot(A))
    return m.dot(A.transpose()).dot(b)


def parse_csv(fname):
    with open(fname, 'r') as fp:
        data = fp.read().strip()

    # skips the first row (titles)
    data = data.split('\n')[1:]

    # gets a matrix of floats from the data
    data = [[float(e) for e in line.split(',')] for line in data]
    data = np.asarray(data)

    n, b = data[:, 0], data[:, 1]
    return b.reshape((b.size, 1)), n.reshape((n.size, 1))


def nlogn(x):
    nlogn.__name__ = 'n log(n)'
    return x * np.log2(x)

def n2(x):
    n2.__name__ = 'n^2'
    return x**2


def fit(b, n, f):
    x = f(n)
    return least_squares(x, b).flatten()[0]


def plot(n, b, k, func, alg_name):
    plt.scatter(n, b, label='mediciones')

    x = np.linspace(n[0], n[-1], num=100)
    plt.plot(x, k * func(x), 'r', label=f'$k {func.__name__}$ (k={k:.4g})')

    plt.title(alg_name.replace('_', ' ').capitalize())
    plt.legend()
    plt.xlabel('n')
    plt.ylabel('Tiempo (ms)')
    plt.show()

    plt.savefig(alg_name)


if __name__ == '__main__':
    if '-h' in sys.argv or '--help' in sys.argv:
        print(__doc__)
        exit(0)
    elif len(sys.argv) != 3:
        print(__doc__)
        exit(1)

    csv_file, func = sys.argv[1], sys.argv[2]
    alg_name = os.path.basename(csv_file).replace('.csv', '')

    func = globals()[func]
    b, n = parse_csv(csv_file)
    k = fit(b, n, func)

    plot(n, b, k, func, alg_name)
    print(f'k={k}')
