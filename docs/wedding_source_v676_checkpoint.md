# V676: original Lil wedding movie command and ordinary live-path control

## Result

M26 has an original source consumer: `/data/SC2.DK4` block 70, command offset
4324, word `4906`. The original chapter-movie handler requests `[26,0,1,0]`.
This identifies the source path as Lil's wedding chapter, correcting the earlier
unresolved numeric mapping. It does not establish actual wedding playback,
ordinary branch reachability or an earned ending. No new ROM is built or edited.

The two original wedding pictures remain byte-identical to clean. Both source
views were visually inspected: portrait/group scene art, with no text change
indicated. Their native extents are256x192 in256x256 storage; the extra stored
rows are preserved. Actual M26 loading/composition/crops/transitions in the
emulator remain the next test. No picture receives gameplay-display credit from
a filename request or a source preview.

## Why the earlier operand search missed it

V674 examined the separate general movie family `4200..42FF`, whose argument is
`(low7)+1`. The original VM also has a chapter-movie family `4900..49FF`:

`0202A510 -> 02029AA0 -> 0202A0F8 -> 02028A28 -> 020D2B1C`.

The chapter handler adds20 to the low byte. `4906` therefore requests M26.
`4902` requests M22. These are distinct original command families; the prior
negative `4219/4299` byte search was not a global M26-use test.

## Original native source checks

- Complete decoder, chapter handler, CS constructor/loader, interpreter-loop and
  movie-factory spans match clean source.
- Two complete original CS constructors/block loaders select active-captain
  input2 and block70. Only SDK file I/O is bridged. Original filename generation
  requests `DATA/SC2.DK4`, whose unique case-insensitive filesystem match is
  `/data/SC2.DK4`. All6764 loaded block bytes match the corresponding clean/current
  source, and complete return ABI and outer buffer guards pass.
- Original per-command decoding walks the entire6762-byte logical block to its
  end in207 commands for each ROM:414 native extents. All command words, offsets
  and extents agree, including the two-byte `4906` command. Input/outer guards
  pass. Sixteen opaque scene/gameplay effect entries are explicitly bridged to
  zero in this linear extent test. This is syntax/argument evidence, not an
  executed conditional story path.
- All256 low-byte chapter commands execute the complete original dispatch and
  chapter handler in each ROM:512 cases. Saved-register/stack ABI, stream,
  result and length guards pass. Movie playback and scene reset are the two
  explicit bridges. These cases prove argument calculation, not the existence
  of every requested movie beyond the real file range.
- Four original filename-generation cases, M22/M26 in clean/current, reach the
  SDK open call with exact source filenames/hashes and stack guards. They stop
  before movie decoding and are not playback evidence.

## Two ordinary4000-frame Lil New Game runs

The unchanged V666 candidate is cold-booted twice with the retained Lil selection
schedule. There is no donor save, savestate, unlock, script substitution, story
fixture, movie substitution or emulated-state write. All12 complete two-screen
pairs and both terminal4MiB RAM states match.

The observed run records19744 native entries:19739 ordinary image entries with
zero guards and five separate loader/selector/factory records. Their first12
register fields alone are interpreted. Blitter-specific fields are inapplicable
to these five records; their guard flags13/13/29/4/5 are retained explicitly.

| Frame | Original entry | Actual inputs |
| --- | --- | --- |
|16|Movie factory|0,0,0,0|
|559|Movie factory|28,1,0,0|
|2222|CS block loader|Object0218F2A8, block22|
|2224|Chapter movie selector|Scene02276F88, chapter2|
|2224|Movie factory|22,0,1,0|

Every LR binds its original clean/current direct caller. The selector's actual
R3 points at `0218F2C2`, exactly loader-object+8+18. Four complete actual captured
3000-byte B22 buffers match the current source at2300/2400/2600/2800; the command
at offset18 is `4902`, and the original captain getter returns2. A separate
original linear decode confirms that same B22 command requests M22. This is a
live positive control for the loader/selector mechanism, not a wedding trigger.

## Host observation safeguards and rejected assumptions

The original push instructions occupy three opcode indices:921,927,92F. The
pinned core table independently shows all three point to the same original
handler RVA513F0. A private wrapper installs the already checked native recorder
on these three exact process-local pointers. Every call still executes that
original handler once; all pointers are restored before freeing the filter.
The core file remains exact. Three sets of13 native host controls verify each
new target, ABI/source immutability and negative guards:39 cases.

An initial assumption that all pushes occupy92F is rejected during preparation,
before any emulator capture. The adjacent A140 literal was also initially
misidentified; the original LDR at A0F8 uses PC+8+44=A144 and selects scene02276F88.
The SDK filename's uppercase `DATA` spelling is preserved, with its actual
filesystem match recorded separately. Initial failure logs are retained.

## Evidence and remaining work

- Analysis: `work/analysis/wedding_movie_v676`.
- Verifier/proof: `scripts/verify_wedding_source_v676.py`, `proof.json`.
- Runtime: `wedding_source_v676_observed` / `wedding_source_v676_baseline` under
  `E:/Rota Nova translations/Generated/work/emulation_v193`.
- Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V676 Lil wedding source`.
- Latest compiled ROM remains V666, SHA256
  `706350a55a058b7a87b67d396333ed397dac664ba36ea378161d18fd085ba121`.

Next use the verified original Lil CS loader for an explicitly isolated chapter70
test, then verify M26's actual native loading, texture bindings, full displayed
pixels and transitions. The source consumer is now identified; actual wedding
playback remains open. Other graphics gates, older record checks and acceptance
remain open. All18 plaque/hint entries remain incomplete and all22 original
requirement objects remain exact. No guide approval, canonical promotion or
full-goal completion. The preceding V675 turn and this turn are progress.
