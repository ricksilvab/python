import numpy as np
from PIL import Image


def read_image(filename):
    return np.asarray(Image.open(filename, 'r'))


def horizontal_mask():
    return [[-1, -1, -1],
            [2, 2, 2],
            [-1, -1, -1]]


def vertical_mask():
    return [[-1, 2, -1],
            [-1, 2, -1],
            [-1, 2, -1]]


def negative_inclined_mask():
    return [[2, -1, -1],
            [-1, 2, -1],
            [-1, -1, 2]]


def positive_inclined_mask():
    return [[-1, -1, 2],
            [-1, 2, -1],
            [2, -1, -1]]


def matrix_mask(line, column, matrix):
    return [[matrix[line - 1][column - 1], matrix[line - 1][column], matrix[line - 1][column + 1]],
            [matrix[line][column - 1], matrix[line][column], matrix[line][column + 1]],
            [matrix[line + 1][column - 1], matrix[line + 1][column], matrix[line + 1][column + 1]]]


def sum_masks(mask_1, mask_2):
    sum = 0
    for line in range(len(mask_1)):
        for column in range(len(mask_2)):
            sum += mask_1[line][column] * mask_2[line][column]
    return sum


def matrix_copy(matrix):
    copy = np.ones((len(matrix) + 2, len(matrix[0]) + 2))
    for line in range(len(matrix)):
        for column in range(len(matrix[0])):
            value = matrix[line][column][0]
            if value == 255:
                value = 1
            else:
                value = 10
            copy[line + 1][column + 1] = value
    return copy


def line_direction(matrix):
    horizontal = 0
    vertical = 0
    inclined = 0
    copy = matrix_copy(matrix)
    for line in range(len(matrix)):
        for column in range(len(matrix[0])):
            if copy[line + 1][column + 1] != 10:
                continue
            mask = matrix_mask(line + 1, column + 1, copy)
            horizontal += sum_masks(mask, horizontal_mask())
            vertical += sum_masks(mask, vertical_mask())
            aux_pi = sum_masks(mask, positive_inclined_mask())
            aux_ni = sum_masks(mask, negative_inclined_mask())
            if aux_pi > aux_ni:
                inclined += aux_pi
            else:
                inclined += aux_ni
    if horizontal > vertical and horizontal > inclined:
        print("Horizontal")
    elif vertical > inclined:
        print("Vertical")
    else:
        print("Inclinada")


def check_image(filename):
    line_direction(read_image(filename))


check_image('/home/bortoletti/projects/python/images_segmentation/images/horizontal.bmp')
check_image('/home/bortoletti/projects/python/images_segmentation/images/vertical.bmp')
check_image('/home/bortoletti/projects/python/images_segmentation/images/inclinada.bmp')
