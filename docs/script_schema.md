# Script schema

CSV is written as UTF-8 with a BOM for Excel compatibility. `script_meta.json`, written beside
the CSV, retains exact binary metadata.

| Column | Meaning |
|---|---|
| `id` | Stable SHA-1-derived row identifier |
| `file_path` | Absolute-style path inside the ROM filesystem |
| `container_path` | Nested container path, reserved for later formats |
| `encoding` | `shift_jis`, `utf-16le`, or another explicit codec |
| `source_offset` | Byte offset in the internal file |
| `source_length` | Original byte range length |
| `source_hex` | Exact original bytes, used as a safety check |
| `japanese` / `english` | Source and editable target text |
| `status` | Workflow state |
| `context`, `speaker`, `notes` | Translator context |
| `max_bytes` | Fixed-mode encoded-byte limit |
| `allow_expand` | Metadata for later rebuild modes; fixed mode never expands |
| `pointer_group` | Reserved pointer-table group |
| `control_profile` | Control-token profile |
| `wrap_width` | Character-count warning threshold |

Statuses are `untranslated`, `draft`, `reviewed`, `approved`, `do_not_translate`,
`technical`, `overflow`, `inserted`, and `failed`.

Blank English means no change. An approved row may not be blank. Required tokens such as
`{END}`, `{LB}`, `{HEX:0A}`, `{WAIT:01}`, and `{VAR:name}` must remain present.

