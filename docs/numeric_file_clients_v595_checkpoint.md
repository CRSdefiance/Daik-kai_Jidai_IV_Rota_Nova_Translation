# Numeric filesystem clients V595

Evidence checkpoint on unchanged combined V593. The graphics goal remains active.

## Question and result

Earlier filename/archive-open searches explicitly left numeric file IDs and
direct byte-range reads open. This checkpoint follows those two original SDK
entry points across all five ARM9 main sections and the declared ARM9 overlay.
It identifies the direct client families; it does not find a raw-comic viewer.

The six direct calls to numeric open `020DEDA0` are:

| Call site | Original data source |
| --- | --- |
| `020DED78` | Normal pathname open, after pathname-to-ID conversion |
| `020DF768` | Overlay-info file-ID field at offset24 |
| `020DF850` | Cached original overlay-table record |
| `020DF9B8` | Original overlay-table record read from the ROM |
| `020EA8B4` | Sound archive pathname converted to an ID |
| `020EC99C` | The selected sound archive ID returned by `020EA2DC` |

The three direct calls to direct-range open `020DEE1C` are `020DE374` and
`020DE3D8` in the filesystem archive-table buffer loader, and `020DF94C` in the
overlay-table record reader. The first function has one stored pointer at
`020DF11C`, used by the original tail-call wrapper `020DF104`; this reference is
retained rather than dismissed because it is indirect.

The twelve-target census also includes the five direct callers of the lower
filesystem command dispatcher `020DE5F4`. ARM B/BL, Thumb BL/BLX and pointers at
every byte position are recorded separately. Both ROMs have the same target
references; no Thumb references to these twelve targets were found. There are
no other stored pointers to these targets within the scanned ARM9 units.

## Original native contracts and explicit boundaries

`scripts/trace_numeric_file_clients_v595.py` executes original ARM instructions
with supplied SDK I/O outcomes backed by each ROM's own physical bytes.

- Twelve complete overlay lookup cases cover clean/current ROMs, cached/direct
  ARM9 table paths, the real overlay index0, the out-of-range index1, and the empty
  ARM7 overlay-table choice. Four successful cases also execute the complete
  original overlay-load function, copy all6208 file bytes exactly and clear its
  32-byte BSS. The real overlay record selects file ID0.
- Original overlay-ID construction reads the actual record's file-ID field.
  Direct-table reads use each source ROM's actual header offsets and lengths.
  The supplied numeric-open boundary uses its actual FAT entry. All handles close;
  caller ABI and neighboring output guards pass.
- The original three-call sound setup sequence and original sound-open function
  execute in each ROM. Their filename is `sound_data.sdat`, actual FNT file ID2,
  with the original SDAT header. All six calls reach the original numeric-open
  function with that ID. The original selected-ID getter returns the same pair.
  Allocation outputs, pathname resolution, filesystem-command success and SDAT
  parser success are explicitly supplied. Actual filesystem resolution, sound
  parsing, streaming and audio playback are not proved by this test.
- Physical table/FAT positions differ between the repacked candidate and clean
  ROM. Both exact ranges are retained; payload hashes, sizes, call events and
  native semantics match. No offsets are silently treated as equal.

Cache-maintenance calls are bridged without hardware effects. Filesystem-command
dispatch, reads and closes are bridged; this is not cartridge-device verification
or a GPU test. The helper's initial missing allocation return was corrected at
the original caller boundary before successful verification; no production code
was changed to accommodate it.

## What this changes next

`/GRP/SLACKIMG.DK4` is actual file ID619, distinct from these observed overlay and
sound inputs. The original normal pathname-open wrapper remains generic; its
presence is not evidence that any archive is unreachable. Computed/relative
references, other filesystem routes, ARM7 readers and runtime-selected resources
are not excluded. No global unused-art claim is made, and all eleven legacy
storage/layout/composition gates remain open.

The next useful comic leads are non-SDK image conversion/compositing code and
runtime-generated resource references. Repeating the already identified overlay
or sound numeric paths would not supply comic-display evidence.

## Preservation and archive

No ROM, patch, translated artwork, source asset or save changed. Candidate V593
remains SHA-256 `d4d572f3356aef8e1d03ee61c18a89f57db01761c381d95b867f1acf25032642`.
The proof, script, checkpoint and hash receipt are archived under
`E:/Rota Nova translations/Screenshots/Test fixtures/V595 Numeric file clients`.
No screenshot or guide credit is claimed. All18 original plaque/hint entries
remain incomplete, and all22 historical requirement objects retain exact scope.
