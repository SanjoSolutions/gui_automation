from main import are_bounding_boxes_nearby

print(are_bounding_boxes_nearby((0, 0, 2, 2), (1, 0, 2, 2)))
print(are_bounding_boxes_nearby((0, 0, 2, 2), (1, 1, 1, 1)))
print(are_bounding_boxes_nearby((1, 1, 1, 1), (0, 0, 2, 2)))