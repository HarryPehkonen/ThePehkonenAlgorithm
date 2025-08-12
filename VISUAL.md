# Visual Documentation

## Sliding Window Progression

### Example Data: Last Names
```
Input: [Johnson, Johnson, Johnson, Jones, Smith, Smith]
```

### Window States

```
Step 1: Initialize
BOF | Johnson | Johnson
  ↓      ↓        ↓
false | true  → First of group

Step 2: Advance window  
Johnson | Johnson | Johnson
   ↓        ↓        ↓
  true  |  true   → Middle of group

Step 3: Advance window
Johnson | Johnson | Jones
   ↓        ↓       ↓
  true  |  false  → Last of group

Step 4: Advance window
Johnson | Jones | Smith
   ↓       ↓       ↓
  false | false  → Single item

Step 5: Advance window
Jones | Smith | Smith
  ↓       ↓       ↓
false |  true   → First of group

Step 6: Advance window
Smith | Smith | EOF
  ↓       ↓      ↓
 true | false  → Last of group
```

## Boolean Pattern Visualization

```
Pattern Matrix:
┌─────────────┬─────────────┬───────────────┬─────────────┐
│ prev_match  │ next_match  │ Pattern       │ Result      │
├─────────────┼─────────────┼───────────────┼─────────────┤
│    false    │    false    │    [F,F]      │   Single    │
│    false    │    true     │    [F,T]      │   First     │
│    true     │    false    │    [T,F]      │   Last      │
│    true     │    true     │    [T,T]      │   Middle    │
└─────────────┴─────────────┴───────────────┴─────────────┘
```

## Data Flow Diagram

```
Input Stream (Sorted)
         │
         ▼
   ┌──────────────┐
   │ Sliding      │
   │ Window (3)   │ ← BOF/EOF handling
   └──────┬───────┘
          │
          ▼
   ┌──────────────┐
   │ Boolean      │
   │ Comparison   │
   └──────┬───────┘
          │
          ▼
   ┌──────────────┐
   │ Pattern      │
   │ Lookup       │
   └──────┬───────┘
          │
          ▼
   ┌──────────────┐
   │ Filter by    │
   │ CLI Flags    │
   └──────┬───────┘
          │
          ▼
    Output Stream
```

## TabTools Pipeline Visualization

```
Raw Data File
      │
      ▼ tabSort -t "column"
Sorted Data
      │
      ▼ tabUnique --flag -t "column"  
Classified Data
      │
      ▼ Filter by flag
Final Output

Example:
people.tab
    │ tabSort -t "Last Name"  
    ▼
┌─────────────────┐
│ Alice Johnson   │ ← First
│ Mary  Johnson   │ ← Middle  
│ Tom   Johnson   │ ← Last
│ Bob   Jones     │ ← Single
│ Jane  Smith     │ ← First
│ John  Smith     │ ← Last
└─────────────────┘
    │ tabUnique --multiples -t "Last Name"
    ▼
┌─────────────────┐
│ Bob   Jones     │ ← Only singles
└─────────────────┘
```

## Memory Usage Pattern

```
Constant Space O(1):
┌─────────┬─────────┬─────────┐
│ Window  │ State   │ Flags   │
│ [3]     │ [2 bool]│ [bits]  │
└─────────┴─────────┴─────────┘
     │         │         │
   12-24     2 bytes   1 byte
   bytes
   
Total: ~15-27 bytes regardless of input size
```

## Performance Visualization

```
Traditional Approach:
Sort: O(n log n) ████████████████
Uniq: O(n)        ████
Total:            ████████████████████

Pehnkonen Algorithm:  
Sort: O(n log n) ████████████████
Scan: O(n)       ████
Total:           ████████████████████

Same complexity, but:
✓ Single pass classification
✓ Multiple output types in one scan
✓ Constant memory usage
✓ Pipeline friendly
```

## Edge Case Handling

```
Single Item List:
BOF → [Item] → EOF
 ↓      ↓      ↓
false false → Single

Empty List:
BOF → EOF
(No processing needed)

All Same Items:
BOF → A → A → A → A → EOF
 ↓    ↓   ↓   ↓   ↓    ↓
    First Middle Middle Last

Mixed Pattern:
BOF → A → B → B → C → EOF  
 ↓    ↓   ↓   ↓   ↓    ↓
   Single First Last Single
```