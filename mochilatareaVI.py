from scipy.optimize import linprog
import numpy as np

class Objeto:
    """
    Representa un objeto con un peso y un valor.
    """
    def __init__(self, peso, valor):
        """
        Inicializa un objeto con su peso y valor.

        Args:
            peso (int): El peso del objeto.
            valor (int): El valor del objeto.
        """
        self.peso = peso
        self.valor = valor

    def __str__(self):
        """
        Retorna una representación legible del objeto.
        """
        return f"Objeto(peso={self.peso}, valor={self.valor})"

class Mochila:
    """
    Representa una mochila con una capacidad máxima y una lista de objetos.
    """
    def __init__(self, capacidad_maxima, objetos):
        """
        Inicializa una mochila con su capacidad máxima y la lista de objetos disponibles.

        Args:
            capacidad_maxima (int): La capacidad máxima de peso de la mochila.
            objetos (list): Una lista de objetos (instancias de la clase Objeto).
        """
        self.capacidad_maxima = capacidad_maxima
        self.objetos = objetos

    def resolver_mochila(self):
        """
        Calcula la mejor combinación de objetos para maximizar el valor total
        sin exceder la capacidad máxima de la mochila utilizando programación entera.

        Returns:
            tuple: Una tupla que contiene:
                - list: La lista de objetos seleccionados.
                - int: El valor total de los objetos seleccionados.
                - int: El peso total de los objetos seleccionados.
        """
        num_objetos = len(self.objetos)
        pesos = [objeto.peso for objeto in self.objetos]
        valores = [objeto.valor for objeto in self.objetos]

        # Coeficientes de la función objetivo (negativos porque linprog minimiza)
        c = [-valor for valor in valores]

        # Coeficientes de la restricción de peso
        A = [pesos]
        b = [self.capacidad_maxima]

        # Límites de las variables (0 <= x_i <= 1)
        bounds = [(0, 1)] * num_objetos

        # Especifica que las variables deben ser enteras
        integrality = [1] * num_objetos

        # Resuelve el problema de programación entera
        resultado = linprog(c, A_ub=A, b_ub=b, bounds=bounds, integrality=integrality, method='highs')

        objetos_seleccionados = []
        valor_total = 0
        peso_total = 0

        if resultado.success:
            for i in range(num_objetos):
                if resultado.x[i] > 0.99:  # Verificar si está muy cerca de 1
                    objeto_seleccionado = self.objetos[i]
                    objetos_seleccionados.append(objeto_seleccionado)
                    valor_total += objeto_seleccionado.valor
                    peso_total += objeto_seleccionado.peso

        return objetos_seleccionados, valor_total, peso_total

def main():
    """
    Función principal para ejecutar el problema de la mochila.
    """
    capacidad_maxima = 10
    objetos_data = [
        {"peso": 5, "valor": 10},
        {"peso": 4, "valor": 40},
        {"peso": 6, "valor": 30},
        {"peso": 3, "valor": 50}
    ]
    objetos = [Objeto(data["peso"], data["valor"]) for data in objetos_data]

    mochila = Mochila(capacidad_maxima, objetos)
    objetos_seleccionados, valor_total, peso_total = mochila.resolver_mochila()

    print("Objetos seleccionados:")
    for objeto in objetos_seleccionados:
        print(objeto)
    print(f"Valor total: {valor_total}")
    print(f"Peso total: {peso_total}")

if __name__ == "__main__":
    main()


"""
Salida:
Objetos seleccionados:
Objeto(peso=4, valor=40)
Objeto(peso=3, valor=50)
Valor total: 90
Peso total: 7
"""