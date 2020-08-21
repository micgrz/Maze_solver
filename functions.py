from classes import Node
from cv2 import line
import numpy as np


def heapify_up(queue: list, index: int) -> list:
    if index <= 0:  # if we reach the root element
        return queue

    p_index = (index - 1) // 2  # parent node index calculation

    if queue[index].d < queue[p_index].d:  # if the distance of node is smaller than the distance of the parent node
        queue[index], queue[p_index] = queue[p_index], queue[index]  # exchange place with parent node

        # Fulfilling the Node object attributes, exchanging their index parameters
        queue[index].index_in_priority_queue = index
        queue[p_index].index_in_priority_queue = p_index

        queue = heapify_up(queue, p_index)  # recursion, executing the same function on parent node up to the point
        # when the queue is prioritized by the distance from the source

    return queue  # if the distance of the child node is not smaller than the distance of the parent node return
    # unchanged queue


def heapify_down(queue: list, index: int) -> list:
    length = len(queue)

    lc_index = 2 * index + 1
    rc_index = 2 * index + 2

    if lc_index >= length:  # stop when bottom of the tree is reached
        return queue

    if lc_index < length <= rc_index:
        if queue[index].d > queue[lc_index].d:
            queue[index], queue[lc_index] = queue[lc_index], queue[index]
            queue[index].index_in_priority_queue = index
            queue[lc_index].index_in_priority_queue = lc_index
            queue = heapify_down(queue, lc_index)
    else:
        small = lc_index
        if queue[lc_index].d > queue[rc_index].d:
            small = rc_index
        if queue[small].d < queue[index].d:
            queue[index], queue[small] = queue[small], queue[index]
            queue[index].index_in_priority_queue = index
            queue[small].index_in_priority_queue = small
            queue = heapify_down(queue, small)
    return queue


def get_neighbors(matrix: np.ndarray, column: float, row: float) -> list:
    rows_amount, columns_amount = matrix.shape
    neighbors = []
    # verification whether neighbors are in the image boundaries and were have not been already visited
    if row > 1 and not matrix[row - 1][column].visited:  # top boundary verification
        neighbors.append(matrix[row - 1][column])
    if row < rows_amount - 1 and not matrix[row + 1][column].visited:  # bottom boundary verification
        neighbors.append(matrix[row + 1][column])
    if column > 0 and not matrix[row][column - 1].visited:  # left boundary verification
        neighbors.append(matrix[row][column - 1])
    if column < columns_amount - 1 and not matrix[row][column + 1].visited:  # right boundary verification
        neighbors.append(matrix[row][column + 1])
    return neighbors


# Implementation of Euclidean squared distance formula, the coordinates of an analyzed point, the R [0], G [1], B [2]
# for Euclidean distance formula https://en.wikipedia.org/wiki/Color_difference#Euclidean
def get_distance(image: np.ndarray, u: tuple, v: tuple) -> float:
    return 0.1 + (float(image[v][0]) - float(image[u][0])) ** 2 + (float(image[v][1]) - float(image[u][1])) ** 2 + (
            float(image[v][2]) - float(image[u][2])) ** 2


def find_solution(img: np.ndarray, start: tuple, finish: tuple) -> list:
    priority_queue = []  # using binary (min) heap as the priority queue

    start_x_coordinate = start[0]
    start_y_coordinate = start[1]

    finish_x_coordinate = finish[0]
    finish_y_coordinate = finish[1]

    image_rows, image_columns = img.shape[0], img.shape[1]

    image_matrix = np.full((image_rows, image_columns), None)  # creating a matrix of the image size filled with Nones

    # fill matrix with vertices
    for r in range(image_rows):
        for c in range(image_columns):
            image_matrix[r][c] = Node(c, r)  # creating of the objects of class Node
            image_matrix[r][c].index_in_priority_queue = len(priority_queue)
            priority_queue.append(image_matrix[r][c])  # adding the vertices to the priority queue

    # setting the distance of the source to 0 as we are already there, else have d = inf
    image_matrix[start_y_coordinate][start_x_coordinate].d = 0

    # putting nodes in their places according to min-heap structure by distance to source
    priority_queue = heapify_up(priority_queue,
                                image_matrix[start_y_coordinate][start_x_coordinate].index_in_priority_queue)

    # continue while there are nodes in the priority queue (unvisited)
    while len(priority_queue) > 0:
        u = priority_queue[0]  # setting currently processed node to the top of min heap (smallest value)

        # remove node of interest from the queue - process for heap
        priority_queue[0] = priority_queue[-1]  # moving the last element to the top
        priority_queue[0].index_in_priority_queue = 0
        priority_queue.pop()  # deletion of the element that was moved to the top (previous last)

        priority_queue = heapify_down(priority_queue, 0)  # restoring the heap structure after deleting the min node

        # Assigning parents to the nodes
        neighbors = get_neighbors(image_matrix, u.x, u.y)
        for v in neighbors:
            distance = get_distance(img, (u.y, u.x), (v.y, v.x))  # getting the distance between current node and all
            # of the neighbors

            if u.d + distance < v.d:  # checking if the root through currently processed root is smaller that current
                # one (if the neighbor node is analyzed for the first time its distance is inf so the conditional
                # statement will execute)
                v.d = u.d + distance  # the distance is changed to the distance through the currently processed root and
                # the parent is set to the currently processed node as below

                # assigning parent coordinates for backtracking via the shortest path
                v.parent_x_coordinate = u.x
                v.parent_y_coordinate = u.y

                # restoring the min heap structure, placing the neighbor correctly in the priority_queue by distance
                idx = v.index_in_priority_queue
                priority_queue = heapify_down(priority_queue, idx)
                priority_queue = heapify_up(priority_queue, idx)

        u.visited = True  # marking u as a visited node

    path = [
        (finish_x_coordinate, finish_y_coordinate)]  # setting beginning of the solution path to the finish point

    path_point = image_matrix[finish_y_coordinate][finish_x_coordinate]  # setting first path_point to the finish point
    while path_point.x != start_x_coordinate or path_point.y != start_y_coordinate:
        path.append((path_point.x, path_point.y))  # adding points (x,y) to the path list
        # going node by node back to the start point via backtracking via the parent nodes
        path_point = image_matrix[path_point.parent_y_coordinate][path_point.parent_x_coordinate]

    path.append((start_x_coordinate, start_y_coordinate))

    return path


def draw_solution(img: list, path: list, thickness: int = 1) -> None:
    x0, y0 = path[0]
    for point in path[1:]:
        x1, y1 = point
        line(img, (x0, y0), (x1, y1), (255, 0, 0), thickness)
        x0, y0 = point
