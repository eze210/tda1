# Parte 1



## Enunciado

Dos Agentes secretos intentan hacerse con unos informes clasificados. El espía 1 - que es el que los tiene - se encuentra en un punto de la ciudad escondido y tiene que ir al aeropuerto. El espía 2 se encuentra en otro punto de la ciudad y desea interceptarlo. Para eso tiene que llegar al aeropuerto antes que su rival y emboscarlo.



## Introducción a la Solución

El mapa de la ciudad se modelizará como un grafo dirigido, donde cada vértice representa una posición geográfica del mapa. Cada vértice estará caracterizado por sus coordenadas X e Y. Cada uno de los espías se encontrará inicialmente en algún vértice, y el aeropuerto en otro.



## Paso 1

Dado un mapa de una ciudad, las ubicaciones de los espías y el aeropuerto determine quién se quedará con los informes.


### Algoritmo de alto nivel

Esta parte del ejercicio se resolverá utilizando una Breadth-first search (BFS) desde cada uno de los vértices de los espías. 

~~~{.python}
G: Digrafo que representa el mapa de la ciudad.
S1: Vértice en el que se encuentra el espía 1.
S2: Vértice en el que se encuentra el espía 2.
A: Vértice en el que se encuentra el aeropuerto.

PasosS1 := BFS(G, S1).obtenerNivelDeVertice(A)
PasosS2 := BFS(G, S2).obtenerNivelDeVertice(A)

If PasosS1 < PasosS2:
	Decir que llega primero el espía 1.

Else If PasosS1 > PasosS2:
	Decir que llega primero el espía 2.

Else:
	Decir que llegan al mismo tiempo.
~~~


### Breadth First Search

Para este algoritmo se utiliza un recorrido BFS del grafo.
Un algoritmo básico para recorrer un gráfico por niveles se puede escribir de la siguiente manera:

~~~{.python}
BFS(Grafo, VerticeInicial):
	Cola: estructura con invariante FIFO, con orden algorítmico
		constante para agregar y remover elementos.
	Visitados: estructura con orden algorítmico constante para
		agregar elementos o preguntar si están.

	Cola.agregar(VerticeInicial)
	While Cola no está vacía:
		V = Cola.remover()
		Visitados.agregar(V)

		# Si el grafo está representado como lista de adyacencias,
		# obtener las adyacencias es de orden constante.
		Foreach A in adyacentes de V:
			If A not in Visitados:
				Cola.agregar(A)
~~~

Observando que los ordenes de cada operación en el algoritmo es de orden constante, y viendo que se deben recorrer todos los nodos y todas las aristas (adyacencias) una vez, se deduce que este algoritmo es de orden $O(|V| + |E|)$. Sin embargo, este algoritmo no alcanza para obtener a cuántos niveles de distancia está cada uno de los otros nodos.

Para esto, necesitaremos algunas variables extra. Se puede modificar el algoritmo de la siguiente manera:

~~~{.python}
BFS(Grafo, VerticeInicial):
	Cola: estructura con invariante FIFO, con orden algorítmico
		constante para agregar y remover elementos.
	Visitados: estructura con orden algorítmico constante para agregar
		elementos o preguntar si están.
	Padres: estructura de acceso aleatorio que dice cuál es el "padre"
		de cada vértice
	Niveles: estructura de acceso aleatorio que dice cuál es el "nivel"
		de cada vértice

	Padres[VerticeInicial] = nil
	Niveles[VerticeInicial] = 0
	Cola.agregar(VerticeInicial)

	While Cola no está vacía:
		V = Cola.remover()
		Visitados.agregar(V)

		# Si el grafo está representado como lista de adyacencias, obtener
		# las adyacencias es de orden constante.
		Foreach A in adyacentes de V:
			If A not in Visitados:
				If A not in Padres:
					Padres[A] = V
					Niveles[A] = Niveles[V] + 1
				Cola.agregar(A)
~~~

En el algoritmo modificado, sólo se agregaron operaciones de orden constante, por lo que se va a preservar el orden algorítmico que se tenía antes.


### Orden del algoritmo de alto nivel

Entonces, como tenemos que aplicar dos algoritmos de orden $O(|V| + |E|)$ (llamamos dos veces a BFS), tendremos un algoritmo final de orden $O(|V| + |E|)$ para resolver el problema propuesto.



## Paso 2

Repita el procedimiento pero introduciendo costos en los caminos.

En este caso, en vez de utilizar un algoritmo que tenga en cuenta los niveles recorridos, se utilizará otro que calcule las distancias mínimas.

El algoritmo a utilizar será el de Dijkstra, y también se utilizará desde la posición de cada espía:

~~~{.python}
G: Digrafo pesado que representa el mapa de la ciudad.
S1: Vértice en el que se encuentra el espía 1.
S2: Vértice en el que se encuentra el espía 2.
A: Vértice en el que se encuentra el aeropuerto.

DistanciaS1 := Dijkstra(G, S1).obtenerDistanciaAlVertice(A)
DistanciaS2 := Dijkstra(G, S2).obtenerDistanciaAlVertice(A)

If DistanciaS1 < DistanciaS2:
	Decir que llega primero el espía 1.

Else If DistanciaS1 > DistanciaS2:
	Decir que llega primero el espía 2.

Else:
	Decir que llegan al mismo tiempo.
~~~


### Algoritmo de Dijkstra

Como en el ítem anterior, se plantea una versión del algoritmo de Dijkstra que usa una estructura para guardar los vértices por recorrer. Como siempre se querrá obtener de esa estructura intermedia el elemento con distancia mínima, se utilizará una cola de prioridad:

~~~{.python}
Dijkstra(Grafo, VerticeInicial):
	Heap: cola de prioridad, con orden algorítmico O(logN) para agregar
		y remover el mínimo elemento.
	Distancias: Distancia a cada uno de los vértices.
	Padres: estructura de acceso aleatorio que dice cuál es el "padre"
		de cada vértice

	Distancias[TodosLosVertices] = Infinito

	Heap.agregar(VerticeInicial)
	Distancias[VerticeInicial] = 0
	Padres[VerticeInicial] = nil

	While Heap no está vacío:
		V = Heap.removerMinimo()

		Foreach A in adyacentes de V:
			If Distancias[A] > (Distancias[V] + GetPeso(Grafo, V, A):
				Distancias[A] = (Distancias[V] + GetPeso(Grafo, V, A)
				Padres[A] = V
				Heap.agregar(A)
~~~

Se puede observar que la manera de iterar el grafo es muy similar en BFS y en Dijkstra (y también en DFS, aunque no hace falta para el ejercicio). En el código fuente se implementó una iteración genérica del grafo, y la función de los algoritmos es definir qué hacer en cada sección de la iteración.


### Orden algorítmico

Las operaciones de agregar o quitar elementos de la cola de prioridad son de orden $O(log N)$, con N igual a la cantidad de elementos que contiene la misma.

Como la cola de prioridad contendrá vértices, y eventualmente podrían entrar todos los vértices menos uno (si el VerticeInicial tuviera grado de salida N-1, por ejemplo), el orden de cada operación sobre la cola de prioridad estará dado por $O(log |V|)$ (se reemplaza N por |V|).

Se observa en el pseudocódigo que se recorrerán todos los nodos y aristas del grafo, entonces el orden de la iteración ignorando el orden de las operaciones sobre la cola de prioridad será, como en BFS, $O(|V| + |E|)$.

Además, se observa que en cada iteración se puede agregar un elemento a la cola de prioridad, y que dicho elemento será removido antes de terminar el algoritmo. Por lo tanto, el orden del algorimo considerando la iteración del grafo y las operaciones que se hacen en cada paso de la misma, será $O((|V| + |E|) log |V|)$.



## Paso 3

Analice la complejidad añadida si se solicita retornar el camino realizado por cada espía en los pasos 1 y 2.


### Análisis

En ambos casos se tuvo que guardar el "padre" de cada vértice.
Suponiendo que ya se calcularon los valores mínimos y el diccionario de Padres, el algoritmo para obtener el camino mínimo consiste en partir de un vértice y obtener el padre del mismo, el padre del padre, y continuar así hasta llegar al vértice inicial.
Una versión recursiva de dicho algoritmo se escribe como:

~~~{.python}
CaminoMinimo(VérticeInicial, VérticeFinal):
	Si VérticeInicial == VérticeFinal:
		return [VérticeInicial]

	Padre = Padres[VérticeFinal]
	camino = CaminoMinimo(VérticeInicial, Padre):
	camino.agregar(VérticeFinal)
	return camino
~~~

Este algoritmo recorre a lo sumo |V| vértices, y aplica operaciones de orden constante en cada paso. Por lo tanto, el orden que se agrega es $O(|V|)$.
Por lo tanto:
 - En el caso del paso 1, como el orden de la iteración BFS era $O(|V| + |E|)$, no se agrega complejidad al calcular el camino mínimo.
 - En el caso del paso 2, como el orden de la iteración de Dijkstra era $O((|V| + |E|) log |V|)$, tampoco se agrega complejidad al calcular el camino mínimo.



## Paso 4

Realiza los pasos 1 y 2 nuevamente retornando como salida de ejecución los caminos realizados por cada espía.


### Ejecución del código

Para la resolución de este paso, las clases Dijkstra y BreadthFirstSearch tienen un método `getShortestPath()`, que implementa el algoritmo recursivo mostrado en el pseudocódigo del paso 3.

Se provee un script python `spy_vs_spy.py` que ejecuta los cuatro pasos mostrando en salida estándar los resultados.
Para ejecutar el script:

~~~{.python}
 $ python3 spy_vs_spy.py indice_espia_1 \
 						 indice_espia_2 \
 						 indice_aeropuerto \
 						 [dir]
~~~

- indice_espia_1 Es el indice del vertice del espia 1 en un archivo de nombre mapa.coords
- indice_espia_2 Es el indice del vertice del espia 2 en un archivo de nombre mapa.coords
- indice_aeropuerto Es el indice del vertice del aeropuerto en un archivo de nombre mapa.coords
- directorio Es el directorio en el que se debe buscar el archivo mapa.coords

Para ver esta ayuda por salida estándar, se puede ejecutar también:
~~~{.python}
 $ python3 spy_vs_spy.py --help

~~~
