import math


def array(arr):
    """
    Esta funcion devuelve un objeto de tipo MyArray
    :param arr: (lista o tupla) Este parametro es un vector de n dimensiones
    :return: MyArray: el resultado del producto escalar
    """
    return MyArray(arr)


def norm(vector):
    """
    Esta funcion devuelve la magnitud de un vector de n dimensiones

    :param
    value (lista o tupla): Este parametro es un vector de n dimensiones
    :return:
    float: devuelve la magnitud del vector
    """

    # Ensure the vector is not empty
    if len(vector) == 0:
        raise ValueError("Input vector cannot be empty.")

    # Calculate the sum of squares of each component
    sum_of_squares = sum(x ** 2 for x in vector)

    # Calculate the square root of the sum of squares
    magnitude = math.sqrt(sum_of_squares)
    return magnitude


def dot(vector1, vector2):
    """
    Esta funcion devuelve el producto punto de dos vectores de n dimensiones

    :param vector1 : (lista o tupla) Este parametro es un vector de n dimensiones
    :param vector2 : (lista o tupla Este parametro es un vector de n dimensiones
    :return:
    float: devuelve el producto punto de los vectores
    """

    if len(vector1) != len(vector2):
        raise ValueError("Input vectors must have the same dimension.")

    result = sum(x * y for x, y in zip(vector1, vector2))
    return result


def add(vector1, vector2):
    """
    Esta funcion devuelve la suma de dos vectores de n dimensiones
    :param vector1: (lista o tupla) Este parametro es un vector de n dimensiones
    :param vector2: (lista o tupla) Este parametro es un vector de n dimensiones
    :return: list: el resultado de la suma de los vectores
    """

    if len(vector1) != len(vector2):
        raise ValueError("Input vectors must have the same dimension.")

    result = [x + y for x, y in zip(vector1, vector2)]
    return array(result)


def subtract(vector1, vector2):
    """
    Esta funcion devuelve la resta de dos vectores de n dimensiones
    :param vector1: (lista o tupla) Este parametro es un vector de n dimensiones
    :param vector2: (lista o tupla) Este parametro es un vector de n dimensiones
    :return: list: el resultado de la resta de los vectores
    """

    if len(vector1) != len(vector2):
        raise ValueError("Input vectors must have the same dimension.")

    result = [x - y for x, y in zip(vector1, vector2)]
    return array(result)


def multiply(vector, scalar):
    """
    Esta funcion devuelve el producto escalar de un vector de n dimensiones
    :param vector: (lista o tupla) Este parametro es un vector de n dimensiones
    :param scalar: (float) Este parametro es un escalar
    :return: list: el resultado del producto escalar
    """

    if isinstance(scalar, (list, tuple, MyArray)) and isinstance(vector, (int, float)):
        vector, scalar = scalar, vector

    result = [x * scalar for x in vector]
    return result


class MyArray:
    def __init__(self, value):
        """
        Constructor for MyArray class. This class represents a vector of n dimensions.
        :param value:
        """
        self.value = value

    def __getitem__(self, index):
        if 0 <= index < len(self.value):
            return self.value[index]
        else:
            raise IndexError("Index out of range")

    def __iter__(self):
        return iter(self.value)

    def __mul__(self, scalar):
        if isinstance(scalar, (int, float)):
            return MyArray([x * scalar for x in self.value])
        else:
            raise TypeError("Multiplication is only supported by a scalar (int or float).")

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __len__(self):
        """
        Override the len() function for MyArray instances.

        Returns:
        int: The length of the array.
        """
        return len(self.value)

    def __truediv__(self, scalar):
        """
        Override the behavior of the / operator for MyArray objects.

        Args:
        scalar: The value to divide the vector by.

        Returns:
        MyArray: A new MyArray instance representing the result of the division.
        """
        if isinstance(scalar, (int, float)):
            if scalar == 0:
                raise ZeroDivisionError("Division by zero is not allowed.")
            # Perform scalar division
            return MyArray([x / scalar for x in self.value])
        else:
            raise TypeError("Division is only supported by a scalar (int or float).")

    def __add__(self, vector):
        """
        Override the behavior of the + operator for MyArray objects.

        :param vector: The vector to add to the current instance.
        :return: MyArray: A new MyArray instance representing the result of the addition.
        """

        if len(self.value) != len(vector):
            raise ValueError("Input vectors must have the same dimension.")

        # Perform vector addition
        return MyArray([x + y for x, y in zip(self.value, vector)])

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, vector):
        """
        Override the behavior of the - operator for MyArray objects.

        :param vector: The vector to subtract from the current instance.
        :return: MyArray: A new MyArray instance representing the result of the subtraction.
        """

        if len(self.value) != len(vector):
            raise ValueError("Input vectors must have the same dimension.")

        # Perform vector subtraction
        return MyArray([x - y for x, y in zip(self.value, vector)])

    def __rsub__(self, other):
        return self.__sub__(other)

    def __str__(self):
        return f"MyVector({self.x}, {self.y})"



