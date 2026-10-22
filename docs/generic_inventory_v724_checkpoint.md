# V724: current name plaques and generic button prompt

V712 remains the registered combined ROM. This checkpoint adds current native
display evidence for the last two original inventory entries that lacked an
explicit current evidence link. Their ordinary scene contexts remain unresolved.

## Current artwork and wording

| Resource | English | Meaning and review |
|---|---|---|
| `/_pxl/slackimg12.pxl` | Name, Middle, Last, Company, Birth | Given name, middle name, surname, merchant organization and date of birth. These concise field labels remain faithful and consistent with captain selection. |
| `/_pxl/slackimg20.pxl` | Press a button! | The original asks for an unspecified button. The English preserves that meaning and exclamation. |

The name atlas has changed since the V538 fixture. Its old screenshot was not
used to establish the current artwork's appearance. The prompt file is unchanged
since that test; both resources now have fresh current-parent fixture evidence.

## Targeted automated emulator tests

Two research ROM fixtures derive from the exact V712 parent. Each substitutes
one four-byte original generic-image instruction in SC0 block 44, offset 30.
Every other file, component, script byte, instruction length and asset is
unchanged. These are isolated widget tests, not ordinary event progression or
playable candidates for distribution.

Both runs cold-boot the pinned DeSmuME core and finish at 5,000 frames with no
savestate or callback errors. The recorded input schedule is the existing opening
schedule. Five captures per asset at frames 3600, 3900, 4200, 4500 and 4800 show:

- All 2,581 nonzero source pixels of the 44 by 60 name atlas, at (106, 20).
- All 3,331 nonzero source pixels of the 156 by 24 prompt, at (50, 20).
- Complete visible letters, edges and shadows inside the native screen bounds.
- The actual original widget view, resource owner, filename and source extent.
- The original native cache getter returning the entire current file. Executed
  getter code matches the registered ROM code, including the mapped pool copy.

That is 29,560 checked visible source pixels across ten complete image matches.
Palette index zero's composition, every fade/transition, other parent layouts
and normal story reachability are outside these tests. Visual review of the
unmodified frame 3900 captures found all five fields and the complete prompt
readable, without a missing leading or trailing letter.

## Source lead investigation

A bounded census covers all byte positions of twenty COMMON, data and testdata
ILNK/VE containers in each ROM: 3,259,562 clean positions and 3,260,220 current
positions. Positive byte patterns are not decoded instructions.

No kind-3 pattern with the canonical 03/83 operand high byte and an index of 12
or above occurs outside WORLDMAP in the clean set. Other flag combinations and
computed consumers remain possible. WORLDMAP matches remain data candidates;
this checkpoint does not execute them as script instructions.

The closest exact-4800 route matches are inside the original inline dialogue
record in SC1 block 24 and SC3 block 26, in both data and testdata. Eight native
decoder cases, covering clean and current sources, start at the enclosing text
instruction. They consume that complete text record and call the text consumer,
with only that display call bridged. They never select the image helper. Thus
these byte matches do not justify navigating to those scenes as prompt tests.
This is a decoder-boundary result, not normal event progression evidence.

## Audit and preservation

The original inventory's two missing current native-evidence links can close
with explicit fixture limits. Their unidentified ordinary parents stay in the
legacy/context queue. All eighteen original plaque/hint audit objects remain
incomplete and the twenty-two historical requirement objects remain exact.
Accepted wood material and the four excluded low-resolution Online bodies are
unchanged. The full graphics goal remains active.

The V723 matrix is retained as an immutable snapshot before updating the live
matrix. V712 ROM, manifest, patch, registry and canonical baseline hashes remain
unchanged. No new combined release, promotion, commit or push is made.

Evidence: `work/analysis/generic_inventory_v724/proof.json` and its two scripts.
Unmodified screenshots and provenance are archived under
`E:/Rota Nova translations/Screenshots/Test fixtures/V724 Generic inventory graphics`.
These fixture captures are not guide screenshots or publication-approved images.

After actual goal completion, revisit the older record-based checks as requested.
