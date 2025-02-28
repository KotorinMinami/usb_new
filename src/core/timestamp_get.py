from typing import Dict, List, Optional
import pandas as pd
import re
from dataclasses import dataclass

@dataclass
class Transaction:
    len_value: str
    start_time: float
    end_time: float

def parse_row(row: pd.Series, pattern: str) -> Optional[str]:
    """Extract length value from row if pattern matches"""
    match = re.search(pattern, str(row['Info']))
    return match.group(1) if match else None

def extract_transaction(df: pd.DataFrame, idx: int, len_value: str) -> Optional[Transaction]:
    """Extract transaction details if enough rows exist"""
    if idx + 5 >= len(df):
        return None
    
    return Transaction(
        len_value=len_value,
        start_time=df.loc[idx, 'Time'],
        end_time=df.loc[idx + 5, 'Time']
    )

def calculate_time_diff(transaction: Transaction) -> float:
    """Calculate and round time difference"""
    return round(transaction.end_time - transaction.start_time, 9)

def group_by_length(transactions: List[float], len_value: str) -> Dict[str, List[float]]:
    """Group time differences by length value"""
    result: Dict[str, List[float]] = {}
    if len_value not in result:
        result[len_value] = []
    result[len_value].extend(transactions)
    return result

def get_timestamps(df: pd.DataFrame, pattern: str) -> List[float]:
    """
    Extract timestamps from DataFrame using functional approach
    
    Args:
        df: Input DataFrame
        pattern: Regex pattern for matching
    
    Returns:
        List of time differences for length value '1'
    """
    transactions: Dict[str, List[float]] = {}
    
    for idx in range(len(df)):
        len_value = parse_row(df.iloc[idx], pattern)
        if not len_value:
            continue
            
        transaction = extract_transaction(df, idx, len_value)
        if not transaction:
            continue
            
        time_diff = calculate_time_diff(transaction)
        
        if len_value not in transactions:
            transactions[len_value] = []
        transactions[len_value].append(time_diff)
    
    return transactions.get('1', [])

# Example usage
if __name__ == '__main__':
    pattern = r'your_pattern_here'
    df = pd.DataFrame({'Time': [], 'Info': []})
    result = get_timestamps(df, pattern)