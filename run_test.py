# coding: utf-8

import sys
import timeit
import dataset
import sorting

TESTS = ["basico", "ordenado", "ordenado_inverso"]
ALGORITHMS = [f for f in dir(sorting) if callable(getattr(sorting, f)) and not f.startswith('_')]
USAGE = """
Calcula los tiempos de ejecución de un algoritmo de ordenamiento para distintos
tamaños de listas, promediando entre varias ejecuciones.

Uso: ./{} semilla tipo_test algoritmo 

  semilla       La semilla utilizada para generar los datos (int).
  tipo_test     El tipo de test a ejecutar (basico, ordenado, ordenado_inverso)
  algoritmo     El algoritmo al cuál ejecutarle las pruebas:
				  * """.format(__file__) + '\n                  * '.join(ALGORITHMS)

TIMEIT_SETUP = """
from copy import copy
from sorting import {algorithm}

data = copy(basedata)
"""


def test(algorithm, basedata_func, seed=None):
	"""Runs the test on a given `algorithm` with the given `basedata`."""

	iterations = 100

	print(algorithm)
	print('n,time (ms)')
	for n in (50, 100, 500, 1000, 2000, 3000, 4000, 5000, 7500, 10000):
		if seed is not None:
			basedata = basedata_func(10000, seed=seed)[:n]
		else:
			basedata = basedata_func(10000)[:n]

		rv = timeit.timeit('{}(data)'.format(algorithm),
						   setup=TIMEIT_SETUP.format(algorithm=algorithm),
						   number=iterations,
						   globals={'basedata': basedata})
		print('{},{:.4f}'.format(n, rv/iterations * 1000))

def test_basic(algorithm, seed):
	"""Runs the test on a given `algorithm`, obtaining a dataset with the given `seed`."""
	return test(algorithm, dataset.get_data, seed)

def test_ordered_data(algorithm):
	"""Runs the test on a given `algorithm` with a ordered dataset"""
	return test(algorithm, dataset.get_ordered_data)

def test_inverse_ordered_data(algorithm):
	"""Runs the test on a given `algorithm` with a inverse ordered dataset"""
	return test(algorithm, dataset.get_inverse_ordered_data)

if __name__ == '__main__':
	if '--help' in sys.argv or '-h' in sys.argv:
		print(USAGE)
		exit(0)
	if len(sys.argv) != 4:
		print(USAGE)
		exit(1)

	seed, test_type, algorithm = int(sys.argv[1]), sys.argv[2], sys.argv[3]

	if (algorithm not in ALGORITHMS) or (test_type not in TESTS):
		if algorithm not in ALGORITHMS:
			print('Algoritmo "{}" no soportado'.format(algorithm))
		else:
			print('Tipo de test "{}" no soportado'.format(test_type))
		print("Usar './{} --help' para ver las opciones".format(__file__))
		exit(1)
	
	if test_type == "ordenado":
		test_ordered_data(algorithm)
	if test_type == "ordenado_inverso":
		test_inverse_ordered_data(algorithm)
	else:
		test_basic(algorithm, seed)

