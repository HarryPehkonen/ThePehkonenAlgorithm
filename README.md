# The Pehkonen Algorithm

Classifies items in sorted data using sliding window boolean pattern matching. Compares each item with its neighbors to identify singles, first/last of groups, and middle items in O(n) time.

Uses a 3-item sliding window with boolean patterns:
- `[false, false]` → Single item
- `[false, true]` → First of group  
- `[true, false]` → Last of group
- `[true, true]` → Middle of group

## Documentation

- **[ALGORITHM.md](ALGORITHM.md)** - Complete specification and complexity analysis
- **[EXAMPLES.md](EXAMPLES.md)** - Practical examples with tabTools CLI usage
- **[VISUAL.md](VISUAL.md)** - Diagrams and visual explanations
- **[tabunique.py](tabunique.py)** - Reference implementation
