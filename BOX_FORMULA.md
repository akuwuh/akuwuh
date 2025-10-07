# 3D Box Drawing Formula for GitHub README (HTML `<samp>` approach)

## Variables
- `content_length` = length of the longest content line (in characters)
- `inner_width` = `2 + content_length + 3` (2 spaces left padding + content + 3 spaces right padding)

---

## Formula 1: Simple Border (No Extrusion)

### Structure:
```
┌───────────────┐
│  content     │
│  content     │
└───────────────┘
```

### Line Breakdown:
1. **Top border**: `┌` + `inner_width` × `─` + `┐`
2. **Content lines**: `│` + `  ` (2 spaces left) + `content` + `   ` (3 spaces right) + `│`
3. **Bottom border**: `└` + `inner_width` × `─` + `┘`

### Character Counts:
- Top/Bottom: `inner_width + 2` characters total
- Content: `inner_width + 2` characters total

---

## Formula 2: 3D Border with Extrusion

### Structure:
```
┌───────────────┐
  │  content     ├─┐
  │  content     │ │
  └┬──────────────┘ │
   └────────────────┘
```

### Line Breakdown:
1. **Top border**: `┌` + `inner_width` × `─` + `┐`
   - Length: `inner_width + 2` chars
   - No left padding

2. **First content line**: `  ` (2 spaces outside) + `│` + `  ` (2 spaces left) + `content` + `   ` (3 spaces right) + `├─┐`
   - Length: `inner_width + 6` chars
   - Right extrusion starts with `├─┐`

3. **Other content lines**: `  ` (2 spaces outside) + `│` + `  ` (2 spaces left) + `content` + `   ` (3 spaces right) + `│ │`
   - Length: `inner_width + 6` chars
   - Right extrusion continues with `│ │`

4. **Bottom line 1**: `  ` (2 spaces) + `└┬` + `(inner_width - 1)` × `─` + `┘ │`
   - Length: `inner_width + 6` chars
   - Left extrusion: 2 spaces indent
   - Right extrusion: ` │` at end

5. **Bottom line 2**: `   ` (3 spaces) + `└` + `inner_width` × `─` + `┘`
   - Length: `inner_width + 5` chars
   - Left extrusion: 3 spaces indent (1 more than line 1)

### Character Counts:
- Top: `inner_width + 2` chars
- Content/Bottom line 1: `inner_width + 6` chars (all same length)
- Bottom line 2: `inner_width + 5` chars

### Key Rules:
1. **Left padding inside box**: Always 2 spaces
2. **Right padding inside box**: Always 3 spaces
3. **Left extrusion spacing**: 
   - Content lines: 2 spaces before `│`
   - Bottom line 1: 2 spaces before `└┬`
   - Bottom line 2: 3 spaces before `└` (1 space deeper)
4. **Right extrusion**:
   - First line: `├─┐` (starts the extrusion)
   - Other lines: `│ │` (continues the extrusion)
   - Bottom: ` │` (connects to bottom extrusion)

---

## HTML Implementation Notes

### Converting to HTML with `<samp>`:
1. Wrap entire structure in `<div align="center"><samp>...</samp></div>`
2. Replace all spaces with `&nbsp;` to preserve alignment
3. Add `<br>` at the end of each line (except the last)

### Example:
```html
<div align="center">
<samp>
┌────────────────┐<br>
&nbsp;&nbsp;│&nbsp;&nbsp;content&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├─┐<br>
&nbsp;&nbsp;└┬───────────────┘&nbsp;│<br>
&nbsp;&nbsp;&nbsp;└────────────────┘
</samp>
</div>
```

---

## Python Implementation Pattern

```python
# Calculate dimensions
max_content_length = max(len(line) for line in content_lines)
inner_width = 2 + max_content_length + 3

# Build box
lines = []

# Top (no extrusion)
lines.append('┌' + '─' * inner_width + '┐')

# Content with right extrusion
for i, content in enumerate(content_lines):
    padded = f'  {content}'.ljust(inner_width)
    if i == 0:
        lines.append(f'  │{padded}├─┐')  # Start extrusion
    else:
        lines.append(f'  │{padded}│ │')  # Continue extrusion

# Bottom with both extrusions
lines.append('  └┬' + '─' * (inner_width - 1) + '┘ │')
lines.append('   └' + '─' * inner_width + '┘')

# Convert to HTML
html_lines = [line.replace(' ', '&nbsp;') for line in lines]
html = '<br>\n'.join(html_lines)
```

---

## Verification Checklist

✓ All content lines have the same total character count  
✓ Bottom line 1 matches content line length  
✓ Top border has `inner_width` dashes  
✓ Bottom line 1 has `inner_width - 1` dashes (accounts for `┬`)  
✓ Bottom line 2 has `inner_width` dashes  
✓ Left extrusion increases by 1 space for each level  
✓ Right extrusion is consistent (`├─┐` → `│ │` → ` │`)
