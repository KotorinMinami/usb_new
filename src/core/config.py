from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Config:
    """Configuration data class"""

    """need for divide"""
    divide_input_path: Optional[str] = None
    divide_output_prefix: Optional[str] = None
    divide_filter: Optional[List[str]] = None

    """need for data load"""
    load_base_path: Optional[str] = None
    load_start_idx: Optional[int] = None
    load_end_idx: Optional[int] = None
    load_file_pattern: Optional[str] = None

    """need for timestamp get"""
    timestamp_pattern: Optional[str] = None

    """need for draw"""
    draw_title: Optional[str] = None
    draw_xlabel: Optional[str] = None
    draw_ylabel: Optional[str] = None
    draw_save_path: Optional[str] = None

    """need for check"""
    finger: Optional[List[float]] = None
    check_range: Optional[List[float]] = None