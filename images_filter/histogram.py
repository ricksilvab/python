from images_filter.common import RGB_MAX


def fill_value(hist, value):
    if value in hist.keys():
        hist[value] += 1
    else:
        hist[value] = 1


def dict_to_list(hist):
    hist_list = []
    for i in range(RGB_MAX + 1):
        if i not in hist.keys():
            hist_list.append(0)
        else:
            hist_list.append(hist[i])

    #print(hist_list)
    return hist_list


def histogram(matrix):
    hist_red = {}
    hist_green = {}
    hist_blue = {}
    for line in matrix:
        for column in line:
            fill_value(hist_red, column[0])
            fill_value(hist_green, column[1])
            fill_value(hist_blue, column[2])
    return dict_to_list(hist_red), dict_to_list(hist_green), dict_to_list(hist_blue)
