import numpy as np
from PIL import Image
import sys


def read_image(filename):
    return np.array(Image.open(filename))


def matrix_copy(matrix):
    copy = 255 * np.ones((len(matrix), len(matrix[0])))
    for line in range(len(copy)):
        for column in range(len(copy[0])):
            copy[line][column] = matrix[line][column][0]
    return copy


def is_valid(line, column, matrix):
    if line < 0 or line >= len(matrix) or column < 0 or column >= len(matrix[0]) or \
            matrix[line][column] == -1 or matrix[line][column] == 255:
        return False
    return True


def check_objects(line, column, matrix):
    if not is_valid(line, column, matrix):
        return matrix
    matrix[line][column] = -1
    check_objects(line, column - 1, matrix)
    check_objects(line, column + 1, matrix)
    check_objects(line + 1, column, matrix)
    check_objects(line - 1, column, matrix)
    return matrix


def objects_in_image(matrix):
    number_of_objects = 0
    matrix = matrix_copy(matrix)
    recursion_limit = len(matrix) * len(matrix[0])
    sys.setrecursionlimit(recursion_limit)
    for line in range(len(matrix)):
        for column in range(len(matrix[0])):
            if matrix[line][column] == -1:
                continue
            matrix = check_objects(line, column, matrix)
            if matrix[line][column] == -1:
                number_of_objects += 1
    print("Image has: " + str(number_of_objects) + " distinct objects.")


def check_image(filename):
    objects_in_image(read_image(filename))


check_image('/home/bortoletti/projects/python/images_segmentation/images/2objetos.bmp')
check_image('/home/bortoletti/projects/python/images_segmentation/images/3objetos.bmp')
check_image('/home/bortoletti/projects/python/images_segmentation/images/4objetos.bmp')
