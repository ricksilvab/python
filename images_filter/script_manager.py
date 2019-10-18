import os
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec
from images_filter.histogram import histogram
from images_filter.brightness import brightness
from images_filter.filters import median_filter
from images_filter.filters import equalization_filter
from images_filter.filters import filter_passa_alta

def plot_hist_from_filename(file, name):
    red_histogram, green_histogram, blue_histogram = histogram(read_image(file))
    plot_hist(red_histogram, green_histogram, blue_histogram, name)


def plot_hist(red_histogram, green_histogram, blue_histogram, name):
    red_index = np.arange(len(red_histogram))
    green_index = np.arange(len(green_histogram))
    blue_index = np.arange(len(blue_histogram))

    fig = plt.figure(figsize=(1, 1))
    fig.suptitle("Histogram")
    gs = gridspec.GridSpec(4, 2, height_ratios=[1, 1, 1, 1, ])
    fig.set_figheight(5)
    fig.set_figwidth(5)
    ax1 = fig.add_subplot(gs[0:2])
    ax1.set_title("Red Histogram")
    ax1.bar(red_index, red_histogram, color='red')

    ax2 = fig.add_subplot(gs[2:4])
    ax2.set_title("Green Histogram")
    ax2.bar(green_index, green_histogram, color='green')

    ax3 = fig.add_subplot(gs[4:6])
    ax3.set_title("Blue Histogram")
    ax3.bar(blue_index, blue_histogram, color='blue')
    fig.subplots_adjust(hspace=.8)
    fig.savefig("histogram_" + name + ".png")
    plt.clf()


def read_image(filename):
    return np.asarray(Image.open(filename, 'r'))


def user_enter():
    print('Please enter the image path.\nExample: image.png, /home/image.png')
    filename = input()
    return filename


def save_image(image, name):
    img = Image.fromarray(image, 'RGB')
    img.save(name)


def image_filters(filename):
    image_filter_median(filename)


def image_brightness(filename, const):
    matrix = brightness(read_image(filename), const)
    dest_image = 'brightness_' + os.path.basename(filename)
    save_image(matrix, dest_image)


def image_filter_median(filename):
    filtered_matrix = median_filter(read_image(filename))
    dest_image = 'median_filter_' + os.path.basename(filename)
    save_image(filtered_matrix, dest_image)

def image_filter_passa_alta(filename):
    filtered_matrix = filter_passa_alta(read_image(filename))
    dest_image = 'passa_alta_filter_' + os.path.basename(filename)
    save_image(filtered_matrix, dest_image)

def image_filter_equalization(filename):
    plot_hist_from_filename(filename, "teste")
    filtered_matrix = equalization_filter(read_image(filename))
    dest_image = 'equalization_filter_' + os.path.basename(filename)
    r, g, b = histogram(filtered_matrix)
    plot_hist(r, g, b, "teste2")
    save_image(filtered_matrix, dest_image)



#if __name__ == "__main__":
#    file = 'images/cachorro.png'
#    image_filter_passa_alta(file)
#    plot_hist_from_filename("passa_alta_filter_cachorro.png","passa_alta")



