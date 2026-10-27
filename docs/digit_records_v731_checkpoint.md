# V731: decimal sprite writer, not a raw-image opacity importer

The previous turn made progress through the current V730 five-long-hint
integration run. This checkpoint follows a different unresolved lead: the
`80008000` literal loaded at `020F412C`, identified in V704 as requiring a
complete consumer interpretation. The production ROM remains V712.

## Original routine and complete output

Original function `020F4120` divides a supplied number into decimal digits and
writes their tile attributes into the fixed array `02170774`, using the
halfword counter at `02170368`. It does not accept an image descriptor or pixel
pointer. Its packed `80008000` constant sets fields in the first two sprite
attributes, rather than setting opacity in individual BGR555 pixel words.
This interpretation follows the original output and the documented attribute
layout in the [libnds sprite definitions](https://github.com/devkitPro/libnds/blob/master/include/nds/arm9/sprite.h).

The complete original function passes 128 native cases with normal return,
stack and saved-register checks. Cases combine eight sampled values
`0,1,9,10,100,105,12345,99999999`, four field widths `0,1,3,8`, two priorities and
two coordinate/counter contracts. They cover leading-zero suppression, zero,
truncation to a shorter field, a maximum eight-digit sample, an empty field,
negative-X wrapping and low-byte Y selection. These are sampled contracts,
not every possible 32-bit value or a newly observed gameplay screen.

An independent decimal-string model predicts each digit and its three
attributes. All 4 MiB of main RAM match before/after except the exact predicted
counter and records. Every unused record byte, two-byte record padding and
neighbor guard stays intact. No image bytes, file-I/O outcome, formatter result
or native helper is substituted. All executed words match both clean and
current mapped code.

The aligned ARM BL census finds the three source call candidates at
`020F6530`, `020F6590` and `020F65E8`. Their complete recorded instruction
contexts are exact clean source. This census does not exclude computed calls,
Thumb, tail branches or pointer tables.

## Original transfer destination

Original wrapper `020E1F08` takes this source array to address `07000000` plus
its supplied offset. Four native boundary tests follow its actual DMA/CPU-copy
branch decisions, including the second screen's offset 1024. They stop before
the lower copy functions. They establish the destination/arguments, not a
completed DMA transaction, hardware behavior, full wrapper ABI or GPU display.
The ordinary source call at `02000EF8` supplies this array, offset zero and
length 640. Together with the record format, this identifies sprite attributes,
not an unclassified raw-color image conversion.

## What is closed and what remains

The V704 packed-mask writer lead is closed. It must not be reused as a proposed
comic importer or justify setting every production image's high bit. The
original raw-comic viewer, loading/import/alpha contract, geometry and native
readability remain open. This does not establish that the raw artwork is unused
or that other import paths do not exist.

The work ledger records this as a closed consumer lead. Its 23 completed
graphics/source/display scopes and six remaining work groups retain their
existing status. Original 18 overall plaque objects remain incomplete, and all
22 historical requirement objects remain exact. The full goal remains active.

No ROM, graphic, palette, patch, manifest, release registry, canonical baseline
or save is changed. No new screenshot, guide approval, commit or push occurs.
Four low-resolution Online bodies remain excluded and approved brown marks
remain preserved. The older-record follow-up remains due after goal completion.

## Evidence

- `scripts/verify_digit_records_v731.py` (targeted Ruff passes).
- `work/analysis/digit_records_v731/proof.json` and `native_cases.json`.
- Checked E archive:
  `Rota Nova translations/Screenshots/Audit comparisons/V731 Decimal sprite writer`.

The initial proof was retained before adding the explicit caller census and
rewording the sampled-domain metadata. The final native run includes those
checks; neither run supplies framebuffer or ordinary comic-viewer evidence.
