from typing import Dict
import pandas as pd
from pathlib import Path

def load_csv_files(
    base_path: str,
    start_idx: int = 2,
    end_idx: int = 102,
    file_pattern: str = "output_{}.csv"
) -> Dict[str, pd.DataFrame]:
    """
    Load multiple CSV files into a dictionary of DataFrames
    
    Args:
        base_path: Base directory containing CSV files
        start_idx: Starting index for file numbering
        end_idx: Ending index for file numbering (exclusive)
        file_pattern: Pattern for file names
        
    Returns:
        Dictionary mapping DataFrame names to pandas DataFrames
    """
    def generate_df_name(i: int) -> str:
        """Generate DataFrame name from index"""
        return f'df_{i - start_idx}'
    
    def generate_file_path(i: int) -> Path:
        """Generate full file path from index"""
        return Path(base_path) / file_pattern.format(i)
    
    return {
        generate_df_name(i): pd.read_csv(generate_file_path(i))
        for i in range(start_idx, end_idx)
    }
