import csv
from typing import List, Iterator
from contextlib import contextmanager

@contextmanager
def managed_csv_writer(filename: str) -> Iterator[csv.writer]:
    """Creates a context-managed CSV writer"""
    with open(filename, 'w', newline='') as f:
        yield csv.writer(f)

def meets_conditions(row: List[str], conditions: List[str]) -> bool:
    """Check if a row meets all filter conditions"""
    return all(condition in row for condition in conditions)

def write_chunk(header: List[str], chunk: List[List[str]], output_prefix: str, split_num: int) -> None:
    """Write a chunk of rows to a new CSV file"""
    with managed_csv_writer(f'{output_prefix}{split_num}.csv') as writer:
        writer.writerow(header)
        for row in chunk:
            writer.writerow(row)

def split_csv(input_file: str, output_prefix: str, filter_conditions: List[str]) -> None:
    """
    Split a CSV file into multiple files based on filter conditions using functional approach
    
    Args:
        input_file (str): Path to input CSV file
        output_prefix (str): Prefix for output CSV files
        filter_conditions (list): List of strings to match in a row for splitting
    """
    with open(input_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        rows = list(reader)
        
        # Group rows based on conditions
        chunks = []
        current_chunk = []
        
        for row in rows:
            if meets_conditions(row, filter_conditions):
                chunks.append(current_chunk)
                current_chunk = []
            current_chunk.append(row)
        
        if current_chunk:
            chunks.append(current_chunk)
            
        # Write chunks to files
        for i, chunk in enumerate(chunks, 1):
            write_chunk(header, chunk, output_prefix, i)

# Example usage:
if __name__ == '__main__':
    input_file = '/home/kotori/Downloads/usb_new/chapter_6/test/Kingston_32GB_1.csv'
    output_prefix = '/home/kotori/Downloads/usb_new/chapter_6/test//outputTest_'
    filter_conditions = ["host", "2.60.0", "USBMS", "64", "GET MAX LUN Request"]
    split_csv(input_file, output_prefix, filter_conditions)