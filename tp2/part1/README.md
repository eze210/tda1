# Parte 1

## Enunciado

Dos Agentes secretos intentan hacerse con unos informes clasificados. El espía 1 - que es el que los tiene - se encuentra en un punto de la ciudad escondido y tiene que ir al aeropuerto. El espía 2 se encuentra en otro punto de la ciudad y desea interceptarlo. Para eso tiene que llegar al aeropuerto antes que su rival y emboscarlo.

## Introducción a la Solución

El mapa de la ciudad lo modelizaremos como un grafo dirigido, donde cada vértice representa una posición geográfica del mapa. Cada vértice estará caracterizado por sus coordenadas X e Y. Cada uno de los espías se encontrará inicialmente en algún vértice, y el aeropuerto en otro.

## Item 1

Dado un mapa de una ciudad, las ubicaciones de los espías y el aeropuerto determine quién se quedará con los informes.

### Algoritmo de alto nivel

Esta parte del ejercicio la resolveremos utilizando una Breadth-first search (BFS) desde cada uno de los vértices de los espías. 

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

Para este algoritmo utilizamos un recorrido BFS del grafo.
Un algoritmo básico para recorrer un gráfico por niveles se puede escribir de la siguiente manera:

~~~{.python}
BFS(Grafo, VerticeInicial):
	Cola: estructura con invariante FIFO, con orden algorítmico constante para agregar y remover elementos.
	Visitados: estructura con orden algorítmico constante para agregar elementos o preguntar si están.

	Cola.agregar(VerticeInicial)
	While Cola no está vacía:
		V = Cola.remover()
		Visitados.agregar(V)

		# Si el grafo está representado como lista de adyacencias, obtener las adyacencias es de orden constante.
		Foreach A in adyacentes de V:
			If A not in Visitados:
				Cola.agregar(A)
~~~

Observando que los ordenes de cada operación en el algoritmo es de orden constante, y viendo que se deben recorrer todos los nodos y todas las aristas (adyacencias) una vez, se deduce que este algoritmo es de orden O(|V| + |E|). Sin embargo, este algoritmo no alcanza para obtener a cuántos niveles de distancia está cada uno de los otros nodos.
Para esto, necesitaremos algunas variables extra. Se puede modificar el algoritmo de la siguiente manera:

~~~{.python}
BFS(Grafo, VerticeInicial):
	Cola: estructura con invariante FIFO, con orden algorítmico constante para agregar y remover elementos.
	Visitados: estructura con orden algorítmico constante para agregar elementos o preguntar si están.
	Padres: estructura de acceso aleatorio que dice cuál es el "padre" de cada vértice
	Niveles: estructura de acceso aleatorio que dice cuál es el "nivel" de cada vértice

	Padres[VerticeInicial] = nil
	Niveles[VerticeInicial] = 0
	Cola.agregar(VerticeInicial)

	While Cola no está vacía:
		V = Cola.remover()
		Visitados.agregar(V)

		# Si el grafo está representado como lista de adyacencias, obtener las adyacencias es de orden constante.
		Foreach A in adyacentes de V:
			If A not in Visitados:
				If A not in Parents:
					Parents[A] = V
					Levels[A] = Levels[V] + 1
				Cola.agregar(A)
~~~

En el algoritmo modificado, sólo se agregaron operaciones de orden constante, por lo que se va a preservar el orden algorítmico que se tenía antes.

### Orden del algoritmo de alto nivel

Entonces, como tenemos que aplicar dos algoritmos de orden O(|V| + |E|) (llamamos dos veces a BFS), tendremos un algoritmo final de orden O(|V| + |E|) para resolver el problema propuesto.

## Item 2

Repita el procedimiento pero introduciendo costos en los caminos.

En este caso, en vez de utilizar un algoritmo que tenga en cuenta los niveles recorridos, utilizaremos uno que calcule las distancias mínimas.
El algoritmo a utilizar será el de Dijkstra, y también lo utilizaremos desde la posición de cada espía:

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

