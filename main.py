from __future__ import print_function
import cv2 as cv
import numpy as np
import argparse
import random as rng

rng.seed(12345)


def thresh_callback(image, threshold):
    canny_output = cv.Canny(image, threshold, threshold * 2)

    contours, _ = cv.findContours(canny_output, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    contours_poly = [None] * len(contours)
    bounding_boxes = [None] * len(contours)
    for i, c in enumerate(contours):
        contours_poly[i] = cv.approxPolyDP(c, 3, True)
        bounding_boxes[i] = cv.boundingRect(contours_poly[i])

    group_bounding_boxes = create_group_bounding_boxes(bounding_boxes, image)

    drawing = image.copy()
    draw_contours(drawing, contours_poly)
    # draw_bounding_boxes(drawing, bounding_boxes, (255, 0, 0))
    # draw_bounding_boxes(drawing, group_bounding_boxes, (0, 255, 0))
    cv.imwrite('processed.png', drawing)


def draw_contours(drawing, contours):
    color = (0, 0, 255)
    for i in range(len(contours)):
        cv.drawContours(drawing, contours, i, color)


def draw_bounding_boxes(drawing, bounding_boxes, color):
    for bounding_box in bounding_boxes:
        cv.rectangle(
            drawing,
            (int(bounding_box[0]), int(bounding_box[1])),
            (int(bounding_box[0] + bounding_box[2]), int(bounding_box[1] + bounding_box[3])),
            color,
            1
        )


distance_threshold = 16  # 1rem = 16px by default in modern browsers


def create_group_bounding_boxes(bounding_boxes, image):
    i = 0
    last_bounding_boxes_length = len(bounding_boxes)
    bounding_boxes = create_group_bounding_boxes_step(bounding_boxes)
    i += 1
    drawing = image.copy()
    draw_bounding_boxes(drawing, bounding_boxes, (0, 255, 0))
    cv.imwrite('processed' + str(i) + '.png', drawing)
    while len(bounding_boxes) < last_bounding_boxes_length:
        last_bounding_boxes_length = len(bounding_boxes)
        bounding_boxes = create_group_bounding_boxes_step(bounding_boxes)
        i += 1
        drawing = image.copy()
        draw_bounding_boxes(drawing, bounding_boxes, (0, 255, 0))
        cv.imwrite('processed' + str(i) + '.png', drawing)
    return bounding_boxes


def create_group_bounding_boxes_step(bounding_boxes):
    bounding_boxes = sort_bounding_boxes(bounding_boxes)
    group_bounding_boxes = []
    for bounding_box in bounding_boxes:
        is_assigned_to_group = False
        for index, group_bounding_box in enumerate(group_bounding_boxes):
            if are_bounding_boxes_nearby(bounding_box, group_bounding_box):
                left = min(group_bounding_box[0], bounding_box[0])
                top = min(group_bounding_box[1], bounding_box[1])
                right = max(group_bounding_box[0] + group_bounding_box[2], bounding_box[0] + bounding_box[2])
                bottom = max(group_bounding_box[1] + group_bounding_box[3], bounding_box[1] + bounding_box[3])
                width = right - left
                height = bottom - top
                group_bounding_box = (left, top, width, height)
                group_bounding_boxes[index] = group_bounding_box
                is_assigned_to_group = True
                break
        if not is_assigned_to_group:
            group_bounding_boxes.append(tuple(bounding_box))
    return group_bounding_boxes


def sort_bounding_boxes(bounding_boxes):
    if len(bounding_boxes) == 0:
        return bounding_boxes

    width = max(map(lambda bounding_box: bounding_box[0] + bounding_box[2], bounding_boxes))
    bounding_boxes = bounding_boxes.copy()
    bounding_boxes.sort(key=lambda bounding_box: bounding_box[1] * width + bounding_box[0])
    return bounding_boxes


def are_bounding_boxes_nearby(bounding_box, bounding_box2):
    return (
        (
            bounding_box[0] <= bounding_box2[0] <= bounding_box[0] + bounding_box[2] or
            bounding_box2[0] <= bounding_box[0] <= bounding_box2[0] + bounding_box2[2] or
            distance_smaller_than_threshold(bounding_box[0] + bounding_box[2], bounding_box2[0]) or
            distance_smaller_than_threshold(bounding_box2[0] + bounding_box2[2], bounding_box[0])
        ) and
        (
            bounding_box[1] <= bounding_box2[1] <= bounding_box[1] + bounding_box[3] or
            bounding_box2[1] <= bounding_box[1] <= bounding_box2[1] + bounding_box2[3] or
            distance_smaller_than_threshold(bounding_box[1] + bounding_box[3], bounding_box2[1]) or
            distance_smaller_than_threshold(bounding_box2[1] + bounding_box2[3], bounding_box[1])
        )
    )


def distance_smaller_than_threshold(a, b):
    return distance(a, b) < distance_threshold


def distance(a, b):
    return abs(b - a)


def main():
    parser = argparse.ArgumentParser(description='Code for Creating Bounding boxes and circles for contours tutorial.')
    parser.add_argument('--input', help='Path to input image.', default='2.png')
    args = parser.parse_args()
    image = cv.imread(args.input)
    if image is None:
        print('Could not open or find the image:', args.input)
        exit(0)

    threshold = 0  # 83
    thresh_callback(image, threshold)

    cv.waitKey()


if __name__ == "__main__":
    main()