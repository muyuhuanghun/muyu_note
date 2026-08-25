---
name: "source-command-edit-canvas"
description: "Edit Obsidian Canvas (.canvas) whiteboard files - add/remove/modify nodes and edges"
---

# source-command-edit-canvas

Use this skill when the user asks to run the migrated source command `edit-canvas`.

## Command Template

# Obsidian Canvas (.canvas) Editor Skill

This skill enables Codex to read and edit Obsidian `.canvas` whiteboard files.

## Canvas File Format

`.canvas` files are JSON with two top-level arrays: `nodes` and `edges`.

### Node Schema

```json
{
  "id": "16-hex-chars",
  "type": "text" | "file",
  "text": "content (for type=text)",
  "file": "relative/path/to/file (for type=file)",
  "x": 0,
  "y": 0,
  "width": 250,
  "height": 60,
  "color": "1"  // optional, Obsidian color index as string
}
```

**Node types:**
- `text`: Contains inline content in the `text` field. Supports markdown, LaTeX (`$$...$$`), and wikilinks (`[[page]]`).
- `file`: Embeds an external file (image, markdown, another canvas). Path is relative to the vault root.

**Sides** (used by edges): `left`, `right`, `top`, `bottom`

### Edge Schema

```json
{
  "id": "16-hex-chars",
  "fromNode": "node-id",
  "fromSide": "right",
  "toNode": "node-id",
  "toSide": "left",
  "label": "optional label text"
}
```

## Editing Rules

1. **Always use the Read tool first** to read the full `.canvas` file before editing.
2. **Use the Edit tool** (not Write) for modifications — canvas files can be large.
3. **Preserve all existing `id` fields** — never change IDs of nodes/edges that you are not replacing.
4. **Generate new 16-hex-char IDs** for any new nodes or edges. Use `crypto.randomBytes(8).toString('hex')` style IDs (e.g., `"a1b2c3d4e5f6a7b8"`).
5. **Coordinate system**: x increases rightward, y increases downward. When placing new nodes, check existing node positions to avoid overlaps.
6. **JSON must be valid**: no trailing commas, proper escaping of special characters in strings.
7. **When adding nodes near existing ones**, leave at least 40px gap between node boundaries.

## Common Operations

### Add a text node
```json
{"id":"NEW_16_HEX","type":"text","text":"Your text here","x":100,"y":100,"width":250,"height":60}
```

### Add a file embed node
```json
{"id":"NEW_16_HEX","type":"file","file":"path/to/file.md","x":100,"y":100,"width":400,"height":600}
```

### Add an edge between two nodes
```json
{"id":"NEW_16_HEX","fromNode":"SOURCE_ID","fromSide":"right","toNode":"TARGET_ID","toSide":"left","label":"optional"}
```

### Add a colored node
Use the `color` field with Obsidian's color index as a string:
- `"1"` = red, `"2"` = orange, `"3"` = yellow, `"4"` = green, `"5"` = cyan, `"6"` = purple

## Workflow

When asked to edit a canvas file:
1. Read the file with the Read tool
2. Parse the JSON mentally and identify relevant nodes/edges
3. Plan the edit (which nodes/edges to add/modify/remove)
4. Use the Edit tool with exact old_string/new_string to make targeted changes
5. If adding content, find the right insertion point (before the closing `]` of the `nodes` or `edges` array)
