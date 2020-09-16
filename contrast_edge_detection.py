import numpy as np

from contrast_ratio import contrast_ratio

MINIMUM_CONTRAST_RATIO = 4.5


def contrast_edge_detection(image):
    edges_horizontal = np.zeros((image[0] + 1, image[1]))
    max_row = image.shape[0] - 1
    for row in range(edges_horizontal.shape[0]):
        for column in range(edges_horizontal.shape[1]):
            if (
                    row == 0 or
                    row > max_row or
                    contrast_ratio(image[row - 1, column], image[row, column]) >= MINIMUM_CONTRAST_RATIO
            ):
                edges_horizontal[row, column] = 1

    edges_vertical = np.zeros((image[0], image[1] + 1))
    max_column = image.shape[1] - 1
    for row in range(edges_vertical.shape[0]):
        for column in range(edges_vertical.shape[1]):
            if (
                column == 0 or
                column > max_column or
                contrast_ratio(image[row, column - 1], image[row, column]) >= MINIMUM_CONTRAST_RATIO
            ):
                edges_vertical[row, column] = 1

    return edges_horizontal, edges_vertical
