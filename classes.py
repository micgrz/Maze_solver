from dataclasses import dataclass


@dataclass
class Node:
    x: float
    y: float
    d: float = float('inf')
    parent_x_coordinate: float = None
    parent_y_coordinate: float = None
    visited: bool = False
    index_in_priority_queue: int = None
