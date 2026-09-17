# Lil SC2 block 23 control map

This map covers Lil's Deck-post tutorial in `/data/SC2.DK4`, block 23. It keeps
static facts separate from presentation details that still require a cold boot.

## Speaker and panel selectors

| Byte | Meaning | Correlation |
| --- | --- | --- |
| `02` | Lil Argot | Every `02` record is Lil's reply to Kamil or Fernando. |
| `09` | Kamil | Every `09` record carries Kamil's explanation or mediation. |
| `14` | Fernando | Every `14` record is Fernando's lookout exchange. |
| `FE` | System tutorial panel | Both records contain direct control instructions rather than character dialogue. |

These bytes are part of the record payload and must be preserved as leading
selectors. Their exact portrait/nameplate effects remain a runtime QA item.

## Tutorial choice grammar

Records 18 and 20 are choice labels, not inherited-speaker dialogue. The local
stream is:

| Record | Hex or text | Structural role |
| --- | --- | --- |
| R0015 | `21` | Opens the choice-command sequence. |
| R0017 | `10` | Choice-menu layout/control parameter. |
| R0018 | `それって初耳…` | First bare choice label. |
| R0020 | `聞かなくたって、分かってる` | Second bare choice label. |
| R0023 | `0204` | First option's branch descriptor. |
| R0025 | `0304` | Second option's branch descriptor. |
| R0027 | `0134` | Choice-flow continuation/join descriptor. |
| R0029 | `40FFFF` | Dialogue boundary before Kamil's response. |

This ordering matches the proven Raphael Lisbon tutorial pattern: `21`, a menu
parameter, two bare labels, branch descriptors, then the selected dialogue path.
The command records must remain byte-identical; only the two fixed-allocation
labels may be translated. The exact meaning of the parameter and descriptor bit
fields is intentionally not claimed without code-level or runtime proof.

## Other event controls

The remaining non-text records delimit dialogue, open interactive sailing
practice, and return to dialogue. They are retained byte-for-byte. In particular,
R0082-R0089 surround the sail-control exercise, and R0112-R0118 introduce
Fernando before his first `14` dialogue record. Their scene-level roles are known
from placement, but their individual bit fields are not rewritten.

## Default-route macros

The established Raphael profile proves that `FI`, `FA`, and `FO` expand to the
default protagonist's first name, surname, and company. Its measured lengths
match `Raphael`, `Castor`, and `Castor Co.` exactly. Lil's corresponding defaults
are therefore:

| Macro | Expansion | ASCII bytes | Pixel-width estimate |
| --- | --- | ---: | ---: |
| `FI` | `Lil` | 3 | 18 |
| `FA` | `Argot` | 5 | 30 |
| `FO` | `Argot Co.` | 9 | 54 |

The `lil-story-b23-probe` profile scopes these values to this experiment. They
must not be promoted globally until the in-game `FI` substitution is observed.

## Runtime probe

`translations/lil_sc2_b23_control_probe_v1.json` changes exactly seven fixed-size,
source-guarded records: one example of each selector, both bare choices, and one
`FI` line. The built ROM is `out/lil_b23_control_probe_v1.nds`. A cold-boot pass
must verify both choice branches and the normal transition into Deck before the
full 35-record manuscript can leave quarantine.
