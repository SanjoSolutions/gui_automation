def create_bounding_boxes(edges_horizontal, edges_vertical):
    points = []
    for row in range(edges_horizontal.shape[0] - 1):
        for column in range(edges_vertical.shape[1] - 1):
            if edges_horizontal[row, column] == 1:
                if edges_vertical[row, column] == 1:
                    points.append((row, column))
                if edges_vertical[row, column + 1] == 1:
                    points.append((row, column + 1))
            if edges_horizontal[row + 1, column] == 1:
                if edges_vertical[row, column] == 1:
                    points.append((row + 1, column))
                if edges_vertical[row, column + 1] == 1:
                    points.append((row + 1, column + 1))
    return points
