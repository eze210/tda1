# Ejercicio 3

Una universidad quiere dictar un conjunto de cursos C1, C2 … Cn donde cada curso se puede dar solo en el intervalo de tiempo Ti, ya que los docentes tienen poca flexibilidad horaria.
Puede que varios cursos se den a la vez, por ejemplo el curso 1 puede dictarse de 3 a 6 y el curso 2 de 4 a 8.
Conocemos el horario de inicio y finalización de cada uno de los cursos.
El objetivo es ver cuál es la menor cantidad de aulas necesarias para acomodar todos los cursos (suponer que todas las aulas son iguales).


## Algoritmo propuesto

El algoritmo consistirá en barrer los arreglos de los horarios ordenados de mayor a menor, desde la última posición hasta la primera. Entonces, la iteración representará un avance en el tiempo, y cada ciclo de la misma representará un intervalo de tiempo.
Mantendremos el número de cursos que se deben dictar en ese intervalo en una variable (que llamaremos "contador"), de tal manera que podamos guardar su máximo valor en otra variable, que representará la máxima cantidad de cursos que tienen un conflicto de horarios en algún instante.
Como vamos a iterar sobre dos arreglos ordenados, eliminando en O(1) algún elemento de alguno de los arreglos en cada ciclo, la parte del algoritmo que consiste en la iteración tendrá orden lineal (O(N)).
Además, vamos a necesitar tener los arreglos de horarios ordenados, por lo que nuestro algoritmo necesitaría un preprocesamiento de orden O(N log(N)).
Por lo tanto, el algoritmo completo, considerando el preprocesamiento y la iteración, será de orden O(N log(N)).

~~~{.python}
'''
HorariosInicio es una lista ordenada de los horarios en donde inician los cursos.
HorariosFin es una lista ordenada de los horarios de finalización.
Ambas listas están ordenadas de mayor a menor
'''
horariosInicio = obtenerHorariosInicio(cursos)
horariosFin = obtenerHorariosFin(cursos)
contador = 0
maxContador = 0
while not horariosInicio.vacio():
    # Comparo los últimos elementos
    if (horariosInicio[-1] < horariosFin[-1]):
        # Empezó un curso: sumo uno a los "actuales"
        contador += 1
        # Borro el horario que ya conté
        horariosInicio.popBack()
    else:
        # Terminó un curso: resto uno a los "actuales"
        contador -= 1
        # Borro el horario que ya desconté
        horariosFin.popBack()

    # Mantengo el máximo número de cursos simultáneos en una variable
    if (contador > maxContador):
        maxContador = contador
~~~


## Reducción a instancia de coloreo

Declaramos las siguientes clases:

**Grafo**: representa un grafo compuesto por vértices y aristas. Posee las siguientes operaciones:

    *Grafo()*: Crea una instancia vacía de un grafo no dirigido.

    *agregarVertice(curso)*: Agrega un curso como vértice del grafo.

    *agregarArista(cursoA, cursoB)*: Agrega una arista que une un par de vértices.

**HeapPorHoraFin**: Representa un heap de minimos, con las siguientes operaciones:

    *HeapPorHoraFin()*: Crea una instancia vacía del heap de mínimos. Este heap almacena cursos y los ordena según su horario de finalización.

    *limpiarFinalizados(horario)*: Recibe un horario por parámetro, y elimina del heap los cursos con horario de finalización menores a este horario.
    Es como aplicar *pop()* recursivamente mientras el horario por parámetro sea mayor que el tope del heap.

    *agregar(curso)*: agrega un curso al heap.

~~~{.python}
grafo = new Grafo()
# Ordeno cursos segun inicio de menor a mayor
cursos = ordenarPorInicio(cursos)
# Armo un minHeap segun el horario de finalizacion
heapActivos = new HeapPorHoraFin()
for cursoActual in cursos:
    grafo.agregarVertice(cursoActual)
    # elimino del heap los cursos que terminan antes que el curso actual
    heapActivos.limpiarFinalizados(cursoActual.horaInicio)
    for cursoActivo in heapActivos.cursos():
        grafo.agregarArista(cursoActual, cursoActivo)
    heapActivos.agregar(cursoActual)

return grafo
~~~

Con esta transformación, resolver el problema de los cursos equivale a resolver el problema de coloreo para el grafo armado con el algoritmo anterior. La cantidad de colores necesaria es equivalente a la cantidad de aulas necesarias.

Dentro del ciclo while, la operación más costosa es la de recorrer el heap de cursos activos y agregar aristas. Esta operación es de orden $O(n)$, y como este heap se recorre N veces (una por cada curso), hacer esta transformación es $O(n^2)$


## En base a los puntos anteriores ¿Es P = NP?

No, ¡Sino seríamos millonarios!

Al reducir el problema de las aulas en el de coloreo de grafos, lo que se está demostrando es que un problema de tipo P puede ser transformado en un problema mucho más dificil, de tipo NP-Hard, siendo esta transformación también polinomial. Esto quiere decir que el coloreo es al menos tan difícil como el problema de las aulas.
Esto no implica que podamos transformar todas las instancias del problema de coloreo en el problema de las aulas y ,por lo tanto, al no ser una transformación biyectiva, no se puede asegurar que *P = NP*
