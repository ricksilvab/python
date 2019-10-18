import numpy as np
from copy import deepcopy
from PIL import Image

RGB_MAX = 255

HIGH_PASS = [[1, 1, 1],
             [1, -8, 1],
             [1, 1, 1]]

SOBEL_VERTICAL = [[1, 2, 1],
                  [0, 0, 0],
                  [-1, -2, -1]]

SOBEL_HORIZONTAL = [[1, 0, -1],
                    [2, 0, -2],
                    [1, 0, -1]]


def read_image(filename):
    return np.asarray(Image.open(filename, 'r'))


def save_image(image, name):
    img = Image.fromarray(image, 'RGB')
    img.save(name)


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


def masks_sum(matrix, mask, line, column):
    sum = 0
    for lin in range(len(mask)):
        for col in range(len(mask[0])):
            line_aux = line + (lin - 1)
            column_aux = column + (col - 1)
            if line_aux < 0 or line_aux >= len(matrix) or \
                    column_aux < 0 or column_aux >= len(matrix[0]):
                continue
            value = np.ndarray(shape=(3,), dtype="int")
            value[0] = mask[lin][col] * matrix[line_aux][column_aux][0]
            value[1] = mask[lin][col] * matrix[line_aux][column_aux][0]
            value[2] = mask[lin][col] * matrix[line_aux][column_aux][0]
            sum = value + sum
    return sum


def median_rgb(pixels):
    column = list(zip(*pixels))
    return [np.average(column[0]), np.average(column[1]), np.average(column[2])]


def average_filter(matrix):
    filtered_matrix = deepcopy(matrix)
    for lin in range(len(matrix)):
        for col in range(len(matrix[0])):
            filtered_matrix[lin][col] = median_rgb(pixel_mask(matrix, lin, col))
    save_image(filtered_matrix, "average_image.jpg")
    return filtered_matrix


def filter_passa_alta(matrix):
    copy = deepcopy(matrix)
    for lin in range(len(matrix)):
        for col in range(len(matrix[0])):
            sum = masks_sum(matrix, HIGH_PASS, lin, col)
            if sum[0] < 0:
                sum[0] = 0
            if sum[0] > RGB_MAX:
                sum[0] = RGB_MAX
            if sum[1] < 0:
                sum[1] = 0
            if sum[1] > RGB_MAX:
                sum[1] = RGB_MAX
            if sum[2] < 0:
                sum[2] = 0
            if sum[2] > RGB_MAX:
                sum[2] = RGB_MAX
            copy[lin][col] = sum
    save_image(copy, "passa_alta_filter.jpg")
    return copy


def gradients(lin, col, matrix):
    gx = masks_sum(matrix, SOBEL_HORIZONTAL, lin, col)
    gy = masks_sum(matrix, SOBEL_VERTICAL, lin, col)
    return gx, gy


def gradient_normalization(g):
    g = np.abs(g)
    if g[0] > RGB_MAX:
        g[0] = RGB_MAX
    if g[1] > RGB_MAX:
        g[1] = RGB_MAX
    if g[2] > RGB_MAX:
        g[2] = RGB_MAX
    return g


def angle(gx, gy):
    pi = 3.1415926
    if gx[0] == 0 or gx[1] == 0 or gx[2] == 0:
        value = np.ndarray(shape=(3,), dtype="int")
        value[0] = -1
        value[1] = -1
        value[2] = -1
        return value
    theta = np.arctan(gy / gx) * 180 / pi
    return theta % 180


def concatenate_boards(matrix):
    copy = deepcopy(matrix)
    teste = []
    for lin in range(len(copy)):
        for col in range(len(copy[0])):
            if copy[lin][col][0] == 0:
                continue
            g_x1, g_y1 = gradients(lin, col, copy)
            mag = np.abs(g_x1) + np.abs(g_y1)
            a_lim = np.abs(angle(g_x1, g_y1))
            if mag[0] > 0:
                teste.append(a_lim)
                copy[lin][col][0] = 0
                copy[lin][col][1] = 155
                copy[lin][col][2] = 0
    save_image(copy, "concatenate_board.jpg")


def check_image(filename):
    matrix = average_filter(read_image(filename))
    concatenate_boards(filter_passa_alta(matrix))


check_image('/home/bortoletti/projects/python/images_segmentation/images/borda_circulo.bmp')
