#!/usr/bin/env python3
"""
tabUnique - Implementation of the Pehnkonen Algorithm
Classifies items in sorted data using sliding window boolean pattern matching.

Usage:
    cat data.tab | tabunique.py [-t column] [--multiples|--first|--last|--all]
"""

import sys
import csv
import argparse
from typing import Iterator, List, Optional, Tuple
from enum import Enum

class Classification(Enum):
    SINGLE = "single"
    FIRST = "first" 
    LAST = "last"
    MIDDLE = "middle"

def pehnkonen_algorithm(items: List[str]) -> Iterator[Tuple[int, str, Classification]]:
    """
    Core Pehnkonen Algorithm implementation.
    
    Args:
        items: Sorted list of items to classify
        
    Yields:
        Tuple of (index, item, classification)
    """
    if not items:
        return
        
    n = len(items)
    
    for i in range(n):
        # Handle BOF: previous item treated as non-matching
        prev_match = False if i == 0 else items[i-1] == items[i]
        
        # Handle EOF: next item treated as non-matching  
        next_match = False if i == n-1 else items[i] == items[i+1]
        
        # Boolean pattern lookup table
        if not prev_match and not next_match:
            classification = Classification.SINGLE
        elif not prev_match and next_match:
            classification = Classification.FIRST
        elif prev_match and not next_match:
            classification = Classification.LAST
        else:  # prev_match and next_match
            classification = Classification.MIDDLE
            
        yield (i, items[i], classification)

def filter_by_flag(results: Iterator[Tuple[int, str, Classification]], 
                   flag: str) -> Iterator[Tuple[int, str, Classification]]:
    """Filter results based on CLI flag."""
    for index, item, classification in results:
        if flag == "multiples" and classification != Classification.SINGLE:
            yield (index, item, classification)
        elif flag == "first" and classification == Classification.FIRST:
            yield (index, item, classification)
        elif flag == "last" and classification == Classification.LAST:
            yield (index, item, classification)
        elif flag == "all":
            yield (index, item, classification)

def process_tabulated_data(input_stream, target_column: Optional[str] = None, 
                          flag: str = "all", delimiter: str = "\t") -> None:
    """Process tab-delimited data through the algorithm."""
    
    reader = csv.DictReader(input_stream, delimiter=delimiter)
    rows = list(reader)
    
    if not rows:
        return
        
    # If no target column specified, use first column
    if target_column is None:
        target_column = reader.fieldnames[0]
    
    if target_column not in reader.fieldnames:
        print(f"Error: Column '{target_column}' not found", file=sys.stderr)
        sys.exit(1)
    
    # Extract values for target column
    target_values = [row[target_column] for row in rows]
    
    # Run algorithm
    results = pehnkonen_algorithm(target_values)
    filtered_results = filter_by_flag(results, flag)
    
    # Output results
    writer = csv.DictWriter(sys.stdout, fieldnames=reader.fieldnames + ["classification"], 
                           delimiter=delimiter)
    writer.writeheader()
    
    for index, _, classification in filtered_results:
        output_row = rows[index].copy()
        output_row["classification"] = classification.value
        writer.writerow(output_row)

def main():
    parser = argparse.ArgumentParser(
        description="Classify items in sorted data using the Pehnkonen Algorithm",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    tabSort -t "Last Name" people.tab | tabunique.py --multiples -t "Last Name"
    cat events.log | tabunique.py --first -t "user_id" 
    tabunique.py --last -t "product_id" < products.tab
        """
    )
    
    parser.add_argument("-t", "--target", dest="target_column",
                       help="Target column name for comparison")
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--multiples", action="store_const", const="multiples", dest="flag",
                      help="Return only items that are part of groups (no singles)")
    group.add_argument("--first", action="store_const", const="first", dest="flag", 
                      help="Return only first occurrence of each group")
    group.add_argument("--last", action="store_const", const="last", dest="flag",
                      help="Return only last occurrence of each group")
    group.add_argument("--all", action="store_const", const="all", dest="flag",
                      help="Return all items with classification (default)")
    
    parser.add_argument("--delimiter", default="\t",
                       help="Field delimiter (default: tab)")
    
    parser.set_defaults(flag="all")
    args = parser.parse_args()
    
    try:
        process_tabulated_data(sys.stdin, args.target_column, args.flag, args.delimiter)
    except KeyboardInterrupt:
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()