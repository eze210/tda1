# Ejercicio 3

Una universidad quiere dictar un conjunto de cursos C1, C2 … Cn donde cada curso se puede dar solo en el intervalo de tiempo Ti, ya que los docentes tienen poca flexibilidad horaria.
Puede que varios cursos se den a la vez, por ejemplo el curso 1 puede dictarse de 3 a 6 y el curso 2 de 4 a 8.
Conocemos el horario de inicia y finalización de cada uno de los cursos.
El objetivo es ver cuál es la menor cantidad de aulas necesarias para acomodar todos los cursos (suponer que todas las aulas son iguales).


## Algoritmo propuesto

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
while(!horariosInicio.vacio()):
    # Comparo los últimos elementos
    if (horariosInicio[-1] < horariosFin[-1]):
        contador += 1
        horariosInicio.pop()
    else:
        contador -=1
        horariosFin.pop()
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

Lo que estamos demostrando es que un problema de tipo P puede ser transformado a un problema mucho más dificil, de tipo NP, y que esta transformación también es de tipo P. Esto no implica que podamos transformar todos los problemas de coloreo en el problema de las aulas. Por lo tanto, al no ser una transformación biyectiva, no puedo asegurar que *P = NP*

