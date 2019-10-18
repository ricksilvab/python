from copy import  deepcopy
from images_filter.common import RGB_MAX

def brightness(matrix, const):
    matrix = deepcopy(matrix)
    for linha in range(len(matrix)):
        for coluna in range(len(matrix[0])):
            for color in range(len(matrix[0][0])):
                sum_const = matrix[linha][coluna][color] + const
                if sum_const < 0:
                    sum_const = 0
                elif sum_const > RGB_MAX:
                    sum_const = RGB_MAX
                matrix[linha][coluna][color] = sum_const
    return matrix
