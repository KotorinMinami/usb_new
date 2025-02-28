from typing import List, Tuple, Callable
from functools import partial
import numpy as np

def calculate_z_scores(data: List[float], 
                      central_tendency: Callable[[List[float]], float],
                      dispersion: Callable[[List[float]], float],
                      scale_factor: float = 1.0) -> List[float]:
    """Calculate Z-scores using specified measures of central tendency and dispersion"""
    center = central_tendency(data)
    spread = dispersion(data)
    return [(scale_factor * (x - center) / spread) for x in data]

def filter_outliers(data: List[float], 
                   z_scores: List[float], 
                   threshold: float) -> List[float]:
    """Filter out values with absolute Z-scores above threshold"""
    return [x for i, x in enumerate(data) if abs(z_scores[i]) <= threshold]

def get_range_stats(cleaned_data: List[float]) -> Tuple[Tuple[float, float], float]:
    """Calculate range statistics from cleaned data"""
    central_range = (min(cleaned_data), max(cleaned_data))
    average = round(float(np.mean(cleaned_data)), 6)
    return central_range, average

def concentrated_range(data: List[float],
                      threshold: float = 1.0,
                      use_robust: bool = False) -> Tuple[Tuple[float, float], float]:
    """
    Calculate concentrated range using either standard or robust statistics
    
    Args:
        data: Input data list
        threshold: Z-score threshold for outlier detection
        use_robust: If True, use median/MAD instead of mean/std
    
    Returns:
        Tuple of ((min_range, max_range), average)
    """
    if use_robust:
        # Robust statistics using median and MAD
        z_scores = calculate_z_scores(
            data,
            central_tendency=np.median,
            dispersion=lambda x: np.median(np.abs(np.array(x) - np.median(x))),
            scale_factor=0.6745
        )
    else:
        # Standard statistics using mean and standard deviation
        z_scores = calculate_z_scores(
            data,
            central_tendency=np.mean,
            dispersion=np.std
        )
    
    cleaned_data = filter_outliers(data, z_scores, threshold)
    range_stats = get_range_stats(cleaned_data)
    
    return range_stats

# Create partially applied functions for common use cases
standard_range = partial(concentrated_range, threshold=1.0, use_robust=False)
robust_range = partial(concentrated_range, threshold=1.0, use_robust=True)

# Example usage:
if __name__ == '__main__':
    sample_data = [1.0, 2.0, 3.0, 100.0, 2.5, 2.7, 2.8]
    central_range, avg = concentrated_range(
        data=sample_data,
        threshold=2.0,  # More permissive threshold
        use_robust=True  # Use robust statistics
    )
