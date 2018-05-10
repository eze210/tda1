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

Se conoce que KMP es O(n+m) donde *n* es el largo de la cadena de búsqueda y *m* el largo del patrón a buscar.
Como en este caso *n=m* KMP es O(n) en cada rotación y, por lo tanto, el algoritmo resulta en O(n<sup>2</sup>).

Es una reducción porque el problema que se quiere resolver es la verificación de que una cadena es una rotación de otra, y para esto se utiliza un algortimo de string matching. La transformación de los datos de entrada consiste en las rotaciones que se realizan.


## Solución utilizando una única ejecución de KMP

Sea S3=S2+S2, es decir la concatencación de S2 consigo misma, se puede demostrar que de ser S2 un rotación de S1, entonces S1 será una sub-cadena de S3.

Luego basta con utilizar KMP para buscar a S1 dentro de S3. De ser así, podemos afirmar que S2 es efectivamente una rotación de S1. De lo contrario, no lo es.


### Demostración

**TODO:** demonstrar lo anterior
