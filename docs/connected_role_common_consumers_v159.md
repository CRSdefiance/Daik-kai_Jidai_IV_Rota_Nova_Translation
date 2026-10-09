# Connected crew-duty COMMON consumers on V159

The two native callers at `02012720` and `020128B4` now have connected execution
evidence from duty search through their actual shared-text copy and return.
This resolves the previously unknown ship virtual in their upstream chain.
It does not establish global live assignment bounds or display layout.

| Step | Native operation |
| --- | --- |
| Caller | Resolve global faction state through `020CB1A8`, add `2090`, pass crew index |
| `02081F54` | Search 31 duty bytes through `020820DC`; resolve a ship through `02082E04` and `02036C94` |
| Ship virtual `020132C0` | Read the byte at `ship + 1E + matched duty position` |
| Ordinary role | Index the caller's 21-word pointer region, select current route through `02053C6C` / `0207F244` |
| Role 12 or 16 | Select crew index + `623` or + `551`, respectively for the two callers |
| Shared text | Execute `0205528C` and the native COMMON selector/copy with ARM946 alignment modeled |
| Unassigned or null ship | Return role sentinel 24; caller returns null without touching output |

160 cases cover both complete callers, four controlled current-route values,
all 16 nonnull ordinary role tables, both special role attributes, unassigned
crew and native null-ship sentinel 155. Assignment uses the last duty position,
30, to exercise the end of the 31-byte search. Native crew/faction constructors
and ship initialization execute; no role, table-selection or COMMON getter is
replaced by a callback. Complete text, first/final bytes, NUL, output guards,
caller return, stack and R4–R11 are checked. Eight focused tests and Ruff pass.

Loaded sections, outer tables/vtable, assignment/current-route state and warm
cache initialization are controlled inputs. These are native selection/copy
proofs, not physical gameplay or glyph/pixel proof. Null table indices 9–11
are not run as valid role assignments; their exclusion by live writers remains
unproved. The source-pinned virtual reads a byte without a range clamp.

The selected messages in this scope do not overlap the remaining 245 COMMON
IDs. This does not establish that promotional or scene-name selections are
unused, and those messages receive no translation completion credit here.
No ROM, release configuration, registry or editorial gates changed in this step.

Evidence: `work/analysis/connected_role_common_v159_proof.json`.
Reproduce: `python scripts/probe_connected_role_common_consumers.py`.
Fresh remaining-record inventory: `work/analysis/common_remaining_v159.json`;
rough source-record progress: `work/analysis/translation_coverage_v159.md`.
