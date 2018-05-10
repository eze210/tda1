# Ejercicio 1

Dadas dos cadenas de texto S1 y S2 de longitud *n*, se desea determinar si la segunda es una rotación cíclica de la primera.


## Solución por fuerza bruta

Este algoritmo consiste en realizar una comparación caracter a carater para cada rotación de S2. Si S2 es una cadena de largo *n*, entonces son necesarias hasta *n* rotaciones. En el peor de los casos, se deberán realizar *n* comparaciones entre caracteres por cada rotación, como se muestra en el siguiente ejemplo:

S1 = AAAAB\
S2 = AAAAA

donde se realizan 4 rotaciones de S2, las cuales realizan 5 comparaciones (hasta fallar en la B).

Esto permite demostrar que el algoritmo es O(n<sup>2</sup>).


## Solución por fuerza bruta utilizando KMP

Este algoritmo es una versión modificada del anterior, donde en lugar de realizar una comparación byte a byte para cada rotación, se utiliza el algoritmo KMP.

Se conoce que KMP es O(n), por lo que la solución resulta en ()
