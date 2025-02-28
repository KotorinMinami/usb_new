from typing import List, Tuple
from functools import reduce
import numpy as np
from itertools import product
import sys

sys.setrecursionlimit(10000)

def create_initial_matrix(n: int, m: int) -> np.ndarray:
    """Create and initialize the DTW matrix"""
    matrix = np.zeros((n + 1, m + 1))
    matrix[1:, 0] = np.inf
    matrix[0, 1:] = np.inf
    return matrix

def calculate_cost(point: Tuple[int, int], s1: List[float], s2: List[float]) -> float:
    """Calculate the cost between two points"""
    return abs(s1[point[0] - 1] - s2[point[1] - 1])

def get_min_adjacent(matrix: np.ndarray, i: int, j: int) -> float:
    """Get minimum value from adjacent cells"""
    return min(matrix[i - 1, j], matrix[i, j - 1], matrix[i - 1, j - 1])

def fill_matrix(matrix: np.ndarray, s1: List[float], s2: List[float]) -> np.ndarray:
    """Fill the DTW matrix using functional approach"""
    indices = product(range(1, len(s1) + 1), range(1, len(s2) + 1))
    
    def update_cell(mat: np.ndarray, idx: Tuple[int, int]) -> np.ndarray:
        i, j = idx
        cost = calculate_cost((i, j), s1, s2)
        mat[i, j] = cost + get_min_adjacent(mat, i, j)
        return mat
    
    return reduce(update_cell, indices, matrix.copy())

def trace_path(matrix: np.ndarray) -> List[Tuple[int, int]]:
    """Trace the optimal path through the matrix"""
    def next_step(i: int, j: int) -> Tuple[int, int]:
        choices = [(i-1, j), (i, j-1), (i-1, j-1)]
        values = [matrix[x, y] for x, y in choices]
        return choices[values.index(min(values))]
    
    def build_path(current: Tuple[int, int], path: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        i, j = current
        if i <= 1 or j <= 1:
            return path
        next_i, next_j = next_step(i, j)
        return build_path((next_i, next_j), path + [(i - 1 , j - 1)])
    
    n1, m1 = matrix.shape
    return build_path((n1 - 1, m1 - 1), [])

def dtw_distance_with_path(s1: List[float], s2: List[float]) -> Tuple[float, List[Tuple[int, int]]]:
    """
    Calculate DTW distance and path using functional programming approach
    
    Args:
        s1: First time series
        s2: Second time series
    
    Returns:
        Tuple of (distance, path)
    """
    matrix = create_initial_matrix(len(s1), len(s2))
    filled_matrix = fill_matrix(matrix, s1, s2)
    path = trace_path(filled_matrix)
    
    return filled_matrix[len(s1), len(s2)], path