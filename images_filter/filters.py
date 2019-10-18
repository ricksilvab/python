import numpy as np
from copy import deepcopy
from images_filter.histogram import histogram
from images_filter.common import RGB_MAX


def pixel_mask(matrix, line, column):
    pixels = []
    col_min = column - 1 if (column - 1) > -1 else column
    col_max = column + 1 if (column + 1) < len(matrix[0]) else column
    lin_min = line - 1 if (line - 1) > -1 else line
    lin_max = line + 1 if (line + 1) < len(matrix) else line
    for l in range(lin_min, lin_max + 1):
        for c in range(col_min, col_max + 1):
            pixels.append(matrix[l][c])
    return pixels


def median_rgb(pixels):
    column = list(zip(*pixels))
    return [np.median(column[0]), np.median(column[1]), np.median(column[2])]


def median_filter(matrix):
    filtered_matrix = deepcopy(matrix)
    for lin in range(len(matrix)):
        for col in range(len(matrix[0])):
            filtered_matrix[lin][col] = median_rgb(pixel_mask(matrix, lin, col))
    return filtered_matrix


def pixels_number(matrix):
    lines = len(matrix)
    columns = len(matrix[0])
    return (lines * columns) / RGB_MAX


def scale_equalization(histogram, ideal_number):
    scale_result = []
    count = 0
    for i in histogram:
        count += i
        q = int(round(count / ideal_number)) - 1
        if q < 0:
            q = 0
        scale_result.append(q)
    return scale_result


def equalization_filter(matrix):
    filtered_matrix = deepcopy(matrix)
    r, g, b = histogram(matrix)
    ideal_number = pixels_number(matrix)
    r_aux = scale_equalization(r, ideal_number)
    g_aux = scale_equalization(g, ideal_number)
    b_aux = scale_equalization(b, ideal_number)
    for lin in range(len(matrix)):
        for col in range(len(matrix[0])):
            color = matrix[lin][col]
            filtered_matrix[lin][col] = [r_aux[color[0]], g_aux[color[1]], b_aux[color[2]]]
    return filtered_matrix


def filter_passa_alta(matrix):
    filtered_matrix = deepcopy(matrix)
    multi_lin = 0
    multi_col = 0
    for lin in range(len(matrix)):
        multi_lin += 1
        for col in range(len(matrix[0])):
            cor = matrix[lin][col]
            if multi_lin == 2:
                if multi_col == 1:
                    filtered_matrix[lin][col] = [(cor[0] * 8) % (RGB_MAX + 1), (cor[1] * 8) % (RGB_MAX + 1),
                                                 (cor[2] * 8) % (RGB_MAX + 1)]
                    multi_col += 1
                elif multi_col > 1:
                    filtered_matrix[lin][col] = [cor[0] * -1, cor[1] * -1, cor[2] * -1]
                    multi_col = 0
                else:
                    filtered_matrix[lin][col] = [cor[0] * -1, cor[1] * -1, cor[2] * -1]
                    multi_col += 1
                multi_lin += 1
            elif multi_lin > 2:
                filtered_matrix[lin][col] = [cor[0] * -1, cor[1] * -1, cor[2] * -1]
                multi_lin = 0
            else:
                filtered_matrix[lin][col] = [cor[0] * -1, cor[1] * -1, cor[2] * -1]
                multi_lin += 1
    return filtered_matrix
