import random
import numpy as np
import matplotlib.pyplot as plt

"""          INTELIGENCIA ARTIFICIAL : MOCHILA          

"""


def Cruza(poblacion):
    """
    Función para cruzar dos individuos
    :param: poblacion: Lista con la poblacion a cruzar
    :return: retorna los hijos de la poblacion (2 hijos por cada 2 padres)
    """

    hijos = poblacion.copy()  # Hacemos una copia de la poblacion a trabajar
    pob_hijos = []

    while len(hijos) > 1:
        padre1 = hijos.pop(
            random.randint(0, len(hijos) - 1)
        )  # Seleccionamos dos padres al azar y los sacamos de los
        padre2 = hijos.pop(random.randint(0, len(hijos) - 1))  # poblacion
        hijo1 = (
            padre2[:5] + padre1[5:]
        )  # Cruzamos los individuos(5 primeros bits del padre 1
        hijo2 = padre1[:5] + padre2[5:]  # y el resto de bits del padre 2 y alrevez
        pob_hijos.append(hijo1)
        pob_hijos.append(hijo2)

    return pob_hijos


def Mutacion(hijos, pro_mut):
    """Función para mutar un bit de un individuo si se cumple la probabilidad de mutacion
    :param hijos: Lista con los hijos a mutar
    :param pro_mut: Probabilidad de mutacion
    :return: Retorna las mutaciones de los hijos
    """

    mutaciones = []

    for elemento in hijos:  # Recorremos la lista de hijos
        # Si el número aleatorio es menor a la probabilidad de mutacion continua
        if random.random() < pro_mut:
            mutaciones.append(elemento)
        else:  # Si es mayor seleccionamos al azar u elemento y lo cambiamos de 0 a 1 o de 1 a 0
            cambio = random.randint(0, len(elemento) - 1)

            if elemento[cambio] == 0:
                elemento[cambio] = 1
                mutaciones.append(elemento)
            else:
                elemento[cambio] = 0
                mutaciones.append(elemento)

    return mutaciones


def FuncionEvaluacion(individuo, objetos):
    """
    :param individuo: Recibe un individuo de la poblacion
    :param objetos: Recibe los objetos de la mochila y sus pesos
    :return: Regresa el pero total de los objetos de cada individuo
    """

    pesos = []
    elementos = list(zip(individuo, objetos))  # Une los individuos con los objetos

    for i in elementos:  # Recorre la lista de elementos
        if i[0] == 1:  # Si el elemento es 1 lo agrega a la lista de pesos
            pesos.append(i[1])
    return sum(pesos)


def Remplazo(poblacion, peso_mochila, objetos_individuo, tam_poblacion, pro_mut):
    """
    Funcion que evalua a la poblacion, saca sus pesos y su número de objetos y los ordena de mayor a menor, en caso de
    que la poblacion resultante sea menor a la poblacion de entrada se agregan individuos aleatorios, en caso de que
    sea mayor se eliminan individuos

    :param poblacion: Recibe la poblacion a evaluar
    :param peso_mochila: Recibe el peso de la mochila
    :param objetos_individuo: Recibe los objetos creados mochila y sus pesos
    :param tam_poblacion: Recibe el tamaño de la poblacion
    :param pro_mut: Recibe la probabilidad de mutacion
    :return: Regresa la poblacion en condiciones de ser evaluada (individuo, peso, objetos)
    """

    pob = []
    cruzar = Cruza(poblacion)  # Cruzamos los individuos de entrada: poblacion
    mutar = Mutacion(cruzar, pro_mut)  # Mutamos los hijos de la poblacion
    pob_final = (
        poblacion + mutar
    )  # Unimos la poblacion de entrada con los hijos mutados

    # Obtenemos peso y cantidad de objetos de cada individuo
    for individuo in pob_final:
        p = FuncionEvaluacion(individuo, objetos_individuo)
        obj = individuo.count(1)
        pob.append((individuo, round(p, 2), obj))
    pob.sort(
        key=lambda x: (x[1], x[2]), reverse=True
    )  # Ordenamos la poblacion de mayor a menor peso
    pob = [
        i for i in pob if i[1] <= peso_mochila
    ]  # Eliminamos los individuos que superan el peso de la mochila
    if len(pob) < tam_poblacion:
        # Si la poblacion resultante es menor a la poblacion de entrada se agregan individuos aleatorios
        while len(pob) < tam_poblacion:
            individuo = [random.randint(0, 1) for _ in range(len(objetos_individuo))]
            p = FuncionEvaluacion(individuo, objetos_individuo)
            obj = individuo.count(1)
            if p <= peso_mochila:
                # Se agrega el individuo a la poblacion
                pob.append((individuo, round(p, 2), obj))
            else:
                continue

    else:  # Si la poblacion resultante es mayor a la poblacion de entrada se eliminan individuos
        pob = pob[:tam_poblacion]

    return pob


def Limpiar(poblacion):
    """
    Función que limpia las listas para qué otras funciones trabajen solo con los individuos
    :param poblacion: Recibe una poblacion a limpiar (individuo, peso, objetos)
    :return: retorna solo los individuos de la poblacion (individuo)
    """

    poblacion_final = []
    for i in poblacion:  # Recorremos la poblacion
        poblacion_final.append(
            i[0]
        )  # Obtenemos solo los individuos y los agregamos a la lista final
    return poblacion_final


def Estadisticas(w, o, pob=None):
    """
    Funcion que recibe los pesos y objetos de la poblacion y calcula la media, mediana y desviación
    estándar de los pesos y objetos, si se recibe una poblacion se filtran los pesos y objetos y se calculan los valores
    :param w: Recibe la lista total de pesos
    :param o: Recibe una lista total de objetos
    :param pob: Poblacion a evaluar en cada generacion (individuo, peso, objetos)
    :return: Regresa la media, mediana y desviación estándar de los pesos y objetos
    """

    # Si se recibe lista de datos se filtran los pesos y objetos
    if pob is not None:
        w = []
        o = []
        for i in pob:
            w.append(i[1])
            o.append(i[2])

    # Media
    media = [np.mean(w), np.mean(o)]

    # Mediana
    mediana = [np.median(w), np.median(o)]

    # Desviación estándar
    desviacion = [round(np.std(w), 5), round(np.std(o), 5)]

    return media, mediana, desviacion


def Graficas(med, medi, desv):
    """
    Función que grafica las estadisticas de la poblacion al final de todas las generaciones
    :param med: Media de los pesos y objetos
    :param medi: Mediana de los pesos y objetos
    :param desv: Desviación estándar de los pesos y objetos
    :return: Retorna una gráfica con las estadisticas de todas las generaciones
    """

    pesos_media = []
    pesos_mediana = []
    pesos_desviacion = []
    objetos_media = []
    objetos_mediana = []
    objetos_desviacion = []

    # Separar los datos de los pesos y los objetos y egregarlos a sus respectivas listas
    for i in med:
        pesos_media.append(i[0])
        objetos_media.append(i[1])
    for i in medi:
        pesos_mediana.append(i[0])
        objetos_mediana.append(i[1])
    for i in desv:
        pesos_desviacion.append(i[0])
        objetos_desviacion.append(i[1])

    # Creamos los ejes y las tablas
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

    # Graficar los datos de los pesos en el primer eje
    ax1.plot(pesos_media, label="Media")
    ax1.plot(pesos_mediana, label="Mediana")
    ax1.plot(pesos_desviacion, label="Desviación estándar")
    ax1.legend()

    # Graficar los datos de los objetos en el segundo eje
    ax2.plot(objetos_media, label="Media")
    ax2.plot(objetos_mediana, label="Mediana")
    ax2.plot(objetos_desviacion, label="Desviación estándar")
    ax2.legend()

    #  Añadimos etiquetas a nuestra grafica
    ax1.set_title("Pesos")
    ax2.set_title("Objetos")
    ax1.set_ylabel("Kilogramos")
    plt.xlabel("Generaciones")
    plt.ylabel("Objetos mochila")

    plt.show()  # Mostramos la gráfica final
