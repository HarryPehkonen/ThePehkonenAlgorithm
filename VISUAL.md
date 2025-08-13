# Visual Documentation

## Sliding Window Progression

### Example Data: Last Names
```
Input: [Johnson, Johnson, Johnson, Jones, Smith, Smith]
```

### Window States

```
┌──────────┬────────────┬────────────┬────────────┬────────────┬─────────────┐
│   Step   │  Position  │    Item    │ prev_match │ next_match │    Result   │
├──────────┼────────────┼────────────┼────────────┼────────────┼─────────────┤
│    1     │    BOF     │  Johnson   │   false    │    true    │    First    │
│    2     │     1      │  Johnson   │    true    │    true    │   Middle    │
│    3     │     2      │  Johnson   │    true    │   false    │    Last     │
│    4     │     3      │   Jones    │   false    │   false    │   Single    │
│    5     │     4      │   Smith    │   false    │    true    │    First    │
│    6     │     5      │   Smith    │    true    │   false    │    Last     │
└──────────┴────────────┴────────────┴────────────┴────────────┴─────────────┘
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
      ▼ tabUnique -t "column"  
Classified Data
      │
      ▼ Filter by "column"
Final Output

Example:
people.tab
    │ tabSort -t "Last Name"  
    ▼
┌────────────┬─────────────┬──────────────┐
│ First Name │ Last Name   │ Type         │
├────────────┼─────────────┼──────────────┤
│ Alice      │ Johnson     │ First        │
│ Mary       │ Johnson     │ Middle       │
│ Tom        │ Johnson     │ Last         │
│ Bob        │ Jones       │ Single       │
│ Jane       │ Smith       │ First        │
│ John       │ Smith       │ Last         │
└────────────┴─────────────┴──────────────┘
    │ tabUnique --singles -t "Last Name"
    ▼
┌────────────┬─────────────┐
│ First Name │ Last Name   │
├────────────┼─────────────┤
│ Bob        │ Jones       │
└────────────┴─────────────┘
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
Sort: O(n log n)  ████████████████
Uniq: O(n)        ████
Total:            ████████████████████

Pehkonen Algorithm:  
Sort: O(n log n)  ████████████████
Scan: O(n)        ████
Total:            ████████████████████

Same complexity, but:
✓ Single pass classification
✓ Multiple output types in one scan
✓ Constant memory usage
✓ Pipeline friendly
```

## Edge Case Handling

```
┌─────────────────┬───────────────────────────────────┬─────────────────────┐
│   Case Type     │            Sequence               │      Results        │
├─────────────────┼───────────────────────────────────┼─────────────────────┤
│ Single Item     │ BOF → [Item] → EOF                │ Item = Single       │
│ Empty List      │ BOF → EOF                         │ (No processing)     │
│ All Same        │ BOF → A → A → A → A → EOF         │ First,Mid,Mid,Last  │
│ Mixed Pattern   │ BOF → A → B → B → C → EOF         │ Single,First,Last,  │
│                 │                                   │ Single              │
└─────────────────┴───────────────────────────────────┴─────────────────────┘
```
