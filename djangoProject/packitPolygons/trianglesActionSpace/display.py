from . import data_convertions as dc


def print_triangle(triangle):
    '''
    Prints a matrix-like representation of a triangle.

    Args:
        triangle (list[list[int]]): A matrix-like representation of a triangle.
    '''
    assert isinstance(triangle, list) , f'Invalid data types. board: {type(triangle)}'


    for row in triangle:
        s = (len(triangle[-1]) - len(row))//2
        print('   '*s + str(row))


def print_numpy_triangle(np_triangle):
    '''
    Prints a NumPy array representation of a triangle.

    Args:
        np_triangle (numpy.ndarray): A matrix-like representation of a triangle.
    '''
    print_triangle(
        dc.convert_numpy_array_to_triangle(np_triangle)
    )
