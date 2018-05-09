# Ejercicio 2

El problema propuesto es el del viajante (TSP) en su versión de optimización, pero se busca el camino máximo en lugar del mínimo.

De esta forma se puede intuir que el problema debe ser NP-hard. Para demostrar esto, basta ver que TSP puede reducirse en tiempo polinómico a este otro problema y, además, éste no pertenece a NP.


## TSP

Dado un grafo pesado no dirigido G(V, E), se busca el ciclo Hamiltoniano en el cual la suma de los pesos de las aristas sea mínima.


## TSP máximo

Para demostrar que el TSP máximo (TSPM) es NP-hard, basta con lograr reducir un problema también NP-hard a una instancia del mismo, resolverla y luego obtener la solución.

Para obtener el menor ciclo Hamiltoniano (el ciclo en el cual suma de los pesos de las aristas que lo componen es mínima), se puede utilizar la siguiente reducción de TSP (que se sabe es NP-hard):

 1. Se busca la arista con mayor peso d<sub>m</sub>.
 2. Se multiplican los pesos de todas las aristas por -1 y se les suma d<sub>m</sub> + 1.
 3. Se busca el ciclo Hamiltoniano máximo en el nuevo grafo (TSPM).
 4. De existir, el camino corresponde al mínimo en el grafo original.

<p align="center">
    <img src="img/reduccion-transparente.png" />
</p>


## Demostración

Sea d<sub>i</sub> > 0 el peso de la i-ésima arista en el grafo original y d'<sub>i</sub>=d<sub>m</sub> - d<sub>i</sub> + 1 el peso de la misma arista en la solución de TSPM, el recorrido total es:

<p align="center">
    <img src="img/eq1.png" />
    <br />
    <img src="img/eq2.png" />
    <br />
    <img src="img/eq3.png" />
</p>

Se puede ver que el máximo se alcanza cuando la sumatoria de d<sub>i</sub> es mínima, ya que *k* es un número siempre positivo.

Como al grafo original solamente se le modificaron los pesos, entonces si la solución de TSPM es un camino Hamiltoniano también debe serlo la misma secuencia en el grafo original.

Por lo tanto, se comprueba que la secuencia de aristas d<sub>i</sub> es un camino Hamiltoniano mínimo.


## Certificación

Dada una secuencia de aristas que componen el máximo ciclo Hamiltoniano en un grafo, se puede observar que para verificar que esto es cierto, es necesario evaluar todos los ciclos posibles, lo cual equivale a resolver el problema. Como se demuestra luego, TSPM es NP-hard, y por lo tanto no puede pertenecer a NP.


## Complejidad

El paso 1 requiere recorrer todas las aristas del grafo, por lo que resulta O(|V| + |E|) si se tiene una representación con listas.

El paso 2 también implica recorrer todas las aristas, por lo que resulta O(|V| + |E|).

El paso 3 corresponde a la reducción.

EL paso 4 no requiere ningún cambio, ya que la correspondencia entre aristas y nodos en la transformación es 1 a 1. Es decir que la lista de aristas que conforman una solución de TSPM conforman la solución de TSP.

Como puede observarse, la reducción se llevó a cabo en tiempo polinómico. Al poder resolver TSP utilizando TSPM, se puede afirmar que TSP <=<sub>p</sub> TSPM y, como TSP es NP-hard, TSPM también lo es.
