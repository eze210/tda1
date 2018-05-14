# Parte 2

## Ejercicio 1

Dadas dos cadenas de texto S1 y S2 de longitud *n*, se desea determinar si la segunda es una rotación cíclica de la primera.


### Solución por fuerza bruta

Este algoritmo consiste en realizar una comparación caracter a carater para cada rotación de S2. Si S2 es una cadena de largo *n*, entonces son necesarias hasta *n* rotaciones, y cada una de las rotaciones puede tener hasta *n* comparaciones.


#### Orden algoritmico

A continuación veremos un análisis de complejidad paso por paso.


#### Orden de la comparación

Sean S1 y S2 dos cadenas de largo *n*.

~~~{.python}
sonIguales(s1, s2):
    for i in range(0,len(s1)):
        if s1[i] != s2 :
            return false
    # no hubo diferencias
    return true
~~~

`sonIguales` es una operación de orden $\mathcal{O}(n)$, ya que se recorre la cadena s1 en un bucle haciendo una comparación por cada ciclo.


#### Orden de la rotación

`rotar(cadena)` es una función que traslada un caracter desde el comienzo de la cadena al final de la misma. Si se utiliza un buffer cíclico, la operación es $\mathcal{O}(1)$


#### Orden del algoritmo

Verificar que una cadena sea rotación de la otra consiste en verificar que ambas cadenas sean iguales, y en caso contrario, rotar una de las cadenas de a un caracter, y reintentar hasta encontrar match o hasta haber hecho *n* rotaciones.

~~~{.python}
esRotacion(s1, s2):
    for i in range(0, len(s1)):
        if sonIguales(s1, s2) :
            return true
        rotar(s2)

    # no hubo match
    return false
~~~

En el peor de los casos, se deberán realizar *n* comparaciones entre caracteres por cada rotación, como se muestra en el siguiente ejemplo:

S1 = AAAAB\
S2 = AAAAA

donde se realizan 4 rotaciones de S2, las cuales realizan 5 comparaciones (hasta fallar en la B).

Esto permite demostrar que el algoritmo es O(n<sup>2</sup>).


### Solución por fuerza bruta utilizando KMP

Este algoritmo es una versión modificada del anterior, donde en lugar de realizar una comparación caracter a caracter para cada rotación, se utiliza el algoritmo KMP.

Se conoce que KMP es O(n+m) donde *n* es el largo de la cadena de búsqueda y *m* el largo del patrón a buscar.

Como en este caso *n=m*, KMP es O(n) en cada rotación y, por lo tanto, el algoritmo final tiene complejidad cuadrática O(n<sup>2</sup>). Lo único que se cambia es un algoritmo lineal de comparación por otro del mismo orden.

Es una reducción porque el problema que se quiere resolver es la verificación de que una cadena es una rotación de otra, y para esto se utiliza un algortimo de string matching. La transformación de los datos de entrada consiste en las rotaciones que se realizan.


### Solución utilizando una única ejecución de KMP

Sea S3 = S2+S2, es decir la concatencación de S2 consigo misma. Se puede demostrar que de ser S2 una rotación de S1, entonces S1 será una sub-cadena de S3.

Primero debemos chequear que los largos de S1 y S2 coincidan, y luego basta con utilizar KMP para buscar a S1 dentro de S3. De ser así, podemos afirmar que S2 es efectivamente una rotación de S1. De lo contrario, no lo es.

En este caso, el algoritmo propuesto es una reducción porque transformamos una de las cadenas (S2) en una copia de la cadena concatenada consigo misma (S3 = S2+S2), y luego llamamos a KMP con la nueva cadena junto con la otra cadena original como parámetros.
Esta reducción será lineal en el largo de las cadenas porque requerirá copiar una de ellas.

Entonces este algoritmo tendrá:
 - La concatenación, de orden O(|S2|),
 - La delegación en KMP, de orden lineal en la suma de los largos de los strings que toma como entrada KMP: O(|S1| + |S3|) = O(3 |S1|) = O(|S1|)

 A continuación analizaremos la complejidad del algoritmo de KMP.


#### Algoritmo Z para preprocesamiento de prefijos

El *algoritmo Z* es la base de varios algoritmos de string matching, incluyendo a *KMP*

Dado un string S, el algoritmo Z genera un array con las longitudes de los prefijos que comienzan en S[i]. Sea Z[] el array resultado de aplicar el algoritmo al string S, Z[i] nos indica la *longitud máxima* del prefijo de S que coincide con un substring que *comienza en S[i]*

El algoritmo Z se comporta de la siguiente forma:

Armo un intervalo [L, R], buscando maximizar R, tal que S[L,R] es un prefijo de S
Inicializo el intervalo en 0,0

~~~{.python}
for i in range (0, range(S)):
    if (i > R):
        # i está fuera de [L,R]
        L = i
        R = BusquedaNaive()
        Z[i] = R - L + 1
    else :
        # i está en una ventana
        # K pertenece al prefijo correspondiente a la ventana
        K = i-L
        # Si Z[k] es más chico que el intervalo remanente de la ventana
        # entonces no hay más matching
        if (Z[k] < R-i+1):
            Z[i] = Z[k]
        else:
            # Expando la ventana hasta terminar el matching
            L = i
            R = BusquedaNaive()
            Z[i] = R - L + 1
~~~

El algoritmo Z es $\mathcal{O}(n)$, ya que *i* recorre linealmente el string al igual que el puntero R.

#### Tabla de saltos

Para optimizar la búsqueda, el algoritmo KMP utiliza una tabla de saltos (Shift table). Esta tabla se construye apartir del array Z precalculado. Se recorre dos veces la tabla en orden inverso, por lo que la construcción de la tabla sigue siendo $\mathcal{O}(n)$

TODO: pseudocódigo de como armar la tabla, ¡Axel soy muy duro!


#### Orden algorítmico

Una vez calculada la tabla de saltos, se puede realizar una búsqueda lineal sobre S.

~~~
    # s: posicion en texto S, p: posicion en pattern P
    s = p = 0
    while s < len(S) - len(P) + p + 1:
        # Similar a la búsqueda naive
        while p < len(P) and S[s] == P[p]:
            s += 1
            p += 1
        if p == len(P):
            return s - len(P)
        elif p == 0:
            s += 1
        else:
            # Utilizo la tabla de saltos para evitar búsquedas innecesarias
            p = T[p-1]

    # no match found
    return None
~~~

TODO: Por qué esto es lineal? A simple vista tiene un bucle adentro de otro.
