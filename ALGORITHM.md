# The Pehnkonen Algorithm

## Overview

An efficient algorithm for classifying items in sorted data using a sliding window approach with boolean pattern matching. Originally developed for the tabTools CLI suite for processing tab-delimited data.

## Problem Statement

Given a sorted list of items, efficiently identify and classify each item as:
- **Single**: Unique item with no duplicates
- **First**: First occurrence in a group of duplicates  
- **Last**: Last occurrence in a group of duplicates
- **Middle**: Middle occurrence in a group of duplicates

## Algorithm Description

### Core Mechanism

Uses a sliding window of 3 consecutive items, comparing each item with its neighbors:
- `prev_match`: Does current item match previous item?
- `next_match`: Does current item match next item?

### Boolean Pattern Table

| prev_match | next_match | Classification | Description |
|------------|------------|----------------|-------------|
| false      | false      | Single         | Unique item |
| false      | true       | First          | Start of group |
| true       | false      | Last           | End of group |
| true       | true       | Middle         | Interior of group |

### Edge Case Handling

- **BOF (Beginning of File)**: Treated as non-matching with first actual item
- **EOF (End of File)**: Treated as non-matching with last actual item
- Pre-populate comparison table with `false` values before processing
- Continue processing until EOF pattern is resolved

### CLI Flag Mapping

For tabTools-style interface:
- `--multiples`: `(prev_match || next_match)` → Return only items that are part of groups
- `--first`: `!prev_match && next_match` → Return only first of groups  
- `--last`: `prev_match && !next_match` → Return only last of groups
- Default: Return all items with classification

## Complexity

- **Time**: O(n) - Single pass through sorted data
- **Space**: O(1) - Constant space for window state
- **Requirement**: Input must be sorted on target column

## Use Cases

1. **Data deduplication**: Extract unique records from sorted datasets
2. **Group analysis**: Find boundaries in grouped data
3. **Log processing**: Identify event start/end markers in sorted logs
4. **Family extraction**: From people list, extract one record per family
5. **Pipeline processing**: Integrate into Unix-style data processing chains