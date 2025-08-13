# Practical Examples

## Example 1: People to Families

### Input Data (people.tab)
```
First Name	Last Name	Age
John	Smith	25
Jane	Smith	23
Bob	Jones	30
Alice	Johnson	28
Tom	Johnson	35
Mary	Johnson	32
```

### Processing Pipeline
```bash
tabSort -t "Last Name" people.tab | tabUnique --multiples -t "Last Name" > people_with_families.tab
```

### Step-by-step Breakdown

1. **After sorting by Last Name:**
```
First Name	Last Name	Age
Alice	Johnson	28
Mary	Johnson	32
Tom	Johnson	35
Bob	Jones	30
Jane	Smith	23
John	Smith	25
```

2. **Algorithm processing (sliding window on Last Name):**

| Position | Item | prev_match | next_match | Classification | Action |
|----------|------|------------|------------|----------------|---------|
| BOF | - | - | - | - | Initialize |
| 1 | Johnson | false | true | First | **Output** (part of group) |
| 2 | Johnson | true | true | Middle | **Output** (part of group) |
| 3 | Johnson | true | false | Last | **Output** (part of group) |
| 4 | Jones | false | false | Single | Skip (not part of group) |
| 5 | Smith | false | true | First | **Output** (part of group) |
| 6 | Smith | true | false | Last | **Output** (part of group) |
| EOF | - | - | - | - | Complete |

3. **Output (people_with_families.tab):**
```
First Name	Last Name	Age
Alice	Johnson	28
Mary	Johnson	32
Tom	Johnson	35
Jane	Smith	23
John	Smith	25
```

## Example 2: Log Event Boundaries

### Input Data (events.log)
```
timestamp	event_type	user_id
10:00:01	login	user123
10:00:05	page_view	user123
10:00:12	page_view	user123
10:00:18	logout	user123
10:01:03	login	user456
10:01:07	logout	user456
10:02:15	login	user789
```

### Find Session Starts
```bash
tabSort -t "user_id" events.log | tabUnique --first -t "user_id" > session_starts.log
```

### Output:
```
timestamp	event_type	user_id
10:00:01	login	user123
10:01:03	login	user456
10:02:15	login	user789
```

### Find Session Ends  
```bash
tabSort -t "user_id" events.log | tabUnique --last -t "user_id" > session_ends.log
```

### Output:
```
timestamp	event_type	user_id
10:00:18	logout	user123
10:01:07	logout	user456
10:02:15	login	user789
```

## Example 3: Data Deduplication

### Input Data (products.tab)
```
product_id	name	category
101	Widget	Tools
102	Gadget	Electronics
102	Gadget	Electronics
103	Doohickey	Tools
103	Doohickey	Tools
103	Doohickey	Tools
104	Thingamajig	Electronics
```

### Remove Duplicates (Keep First)
```bash
tabSort -t "product_id" products.tab | tabUnique --first -t "product_id" > unique_products.tab
```

### Output:
```
product_id	name	category
101	Widget	Tools
102	Gadget	Electronics
103	Doohickey	Tools
104	Thingamajig	Electronics
```

## Example 4: Group Analysis

### Find All Singletons and Group Boundaries
```bash
tabSort -t "category" products.tab | tabUnique -t "category"
```

### Output with Classifications:
```
product_id	name	category	classification
101	Widget	Tools	first
103	Doohickey	Tools	last
102	Gadget	Electronics	first
104	Thingamajig	Electronics	last
```

## Performance Comparison

### Traditional Approach (Multiple Passes)
```bash
# Find uniques: O(n log n) sort + O(n²) comparisons
sort file.tab | uniq
```

### Pehkonen Algorithm (Single Pass)
```bash
# O(n log n) sort + O(n) classification  
tabSort -t "column" file.tab | tabUnique -t "column"
```

**Result**: Significantly faster for large datasets with complex grouping requirements.
