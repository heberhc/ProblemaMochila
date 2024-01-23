import random
from mochila import *

"""             INTELIGENCIA ARTIFICIAL : MOCHILA 

"""


def Mochila(poblacion):
    """Función para elegir al mejor individuo de la poblacion
    :param poblacion: Lista con la poblacion a evaluar
    :return: El mejor individuo de la poblacion total"""

    pesos_to = []  # Lista para guardar los pesos de cada individuo
    ob_total = []  # Lista para guardar el número de objetos de cada individuo
    t_med = []  # Lista para guardar la media de pesos de cada generacion
    t_mediana = []  # Lista para guardar la mediana de pesos de cada generacion
    t_des = []  # Lista para guardar la desviacion standar de pesos de cada generacion

    print("Generando resultados...")
    for i in range(generaciones):  # Ciclo de generaciones
        # Generamos la poblacion de manera recursiva e imprimimos cada generacion
        poblacion = Remplazo(
            poblacion, tam_mochila, objetos_mochila, tam_poblacion, prob_mutacion
        )

        # Obtenemos las estadisticas de la generacion actual para graficar
        graf = Estadisticas(None, None, poblacion)
        t_med.append(graf[0])
        t_mediana.append(graf[1])
        t_des.append(graf[2])

        # imprime las generaciones (desactivado para no saturar la consola)
        """print(f"\n------------Generacion: {i + 1}--------------------------------")
        # ordena la impression de la poblacion de la generacion actual
        for _ in poblacion:
            print(_)"""

        # Limpiamos la poblacion para volver a generar una nueva
        poblacion = Limpiar(poblacion)

    mejor_individuo = []
    for individuos in poblacion:  # Evaluamos la poblacion final
        p_i = FuncionEvaluacion(
            individuos, objetos_mochila
        )  # Obtenemos el peso de cada individuo
        pesos_to.append(p_i)
        obj = individuos.count(1)  # Contamos sus objetos
        ob_total.append(obj)
        mejor_individuo.append((individuos, p_i, obj))
    mejor_individuo.sort(
        key=lambda x: (x[1], x[2]), reverse=True
    )  # Ordenamos la lista de mayor peso a menor peso

    mejor_individuo = mejor_individuo[
        0
    ]  # Elegimos el primer individuo que es el de mayor peso
    # y mayor número de objetos

    medi, med, des = Estadisticas(
        pesos_to, ob_total
    )  # Obtenemos las estadisticas de la poblacion final

    return mejor_individuo, medi, med, des, t_med, t_mediana, t_des


# -----------------------------PROGRAMA PRINCIPAL--------------------------------------------

# Pedimos los datos necesarios para el programa
tam_poblacion = int(
    input("Ingrese el tamaño de la poblacion: ")
)  # Tamaño de la poblacion
generaciones = int(input("Ingrese el numero de generaciones: "))
prob_mutacion = float(
    input("Ingrese la probabilidad de mutacion(en rango de 0-1): ")
)  # Probabilidad de mutacion
if prob_mutacion > 1 or prob_mutacion < 0:
    print("La probabilidad de mutacion debe estar en el rango de 0-1")
    prob_mutacion = float(
        input("Ingrese la probabilidad de mutacion(en rango de 0-1): ")
    )  # Probabilidad de mutacion

num_objetos = 20  # Número de objetos que tendrá la mochila
tam_mochila = 40  # Peso máximo de la mochila en kilos

objetos = [
    (f"Objeto {i}", round(random.uniform(0, 10), 1)) for i in range(num_objetos)
]  # Creamos los objetos
objetos_mochila = []  # Nombre del objeto + peso
for peso in objetos:  # El peso es aleatorio con
    p = peso[1]  # un maxima de 20
    objetos_mochila.append(p)

poblacion_inicial = []  # Creamos la poblacion inicial y la guardamos
for i in range(tam_poblacion):
    individuo = [
        random.randint(0, 1) for i in range(len(objetos))
    ]  # Creamos un individuo con 0 y 1 aleatorios
    poblacion_inicial.append(individuo)  # hasta que complete la poblacion inicial


# Llamamos a la función Mochila (la función principal)
resultado, m, me, d_es, tm, tmed, tdes = Mochila(poblacion_inicial)

# Graficamos los resultados de media mediana y desviacion estandar
Graficas(tm, tmed, tdes)


# imprimimos el resultado del algoritmo
print("\n----------------------------RESULTADOS-----------------------------\n")
print(
    f"Mejor individuo: {resultado[0]} \ncon peso de {resultado[1]} / {tam_mochila} Kg y un total de {resultado[2]}"
    f" objetos\n"
)
print("------------------ESTADISTICAS DE EJECUCIÓN---------------------------\n")
print(
    f"Media de pesos: {m[0]} Kg\nMedia de objetos: {m[1]}\n\nMediana pesos: {me[0]} Kg\nMediana objetos: {me[1]}\n\n"
    f"Desviacion standard pesos: {d_es[0]}\nDesviacion estandar objetos: {d_es[1]}"
)
print("\n---------------------------------------------------------------------\n")
