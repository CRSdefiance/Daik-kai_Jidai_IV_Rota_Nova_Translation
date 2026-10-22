# V816-V817: Athens scenes; climb world-state comparison remains open

This is gameplay and editorial evidence for the existing registered experimental
V809 ROM, SHA-256
`4b85eae04e1f1654022433c2a9a2aafd8b719daf10cc5f2120a32f9781728ae2`.
No ROM, patch, manuscript, frozen release dependency or graphics asset changed.
The next integrated build must retain profile `all-routes-unified-v809`.

## Original access and saved test setups

An isolated copy of the V814 donor completes the original Angelo recruitment,
resupply, departure, Athens docking and item-award conversations. Only the
declared active-ship coordinates, original calendar word, Athens facility mask
and site-7 discovery flag are supplied as fixtures. The game performs docking,
story events, eligibility, dialogue, effects and time advancement itself.
Normal in-game saves create two new donors under `E:/Rota Nova translations/Saves/Test fixtures`:

- `V816 Athens day21 Temple ready.dsv`, SHA-256
  `d67dd0fd0acb880b174de62416e3dfb50c7dc0184916a58dadbb13deccf68178`.
- `V816 Athens day21 site ready.dsv`, SHA-256
  `a9e58e5b96a86d98ca23eacd9da4ac9572052d400dad7e1ffc4e34bc0e719db4`.

Original donors remain unchanged. These fixtures do not establish natural
travel, earned access or the simulation of elapsed days. No savestates are used.
Source code and captured-RAM code spans are checked. Forty paired date/access
preflight cases and the coordinate preflight preserve all undeclared RAM bytes.
The original discovery method is executed privately to prove its bit; its fame
award is discarded, and only the declared flag is copied.

The native site getter identifies Athens as Town 19, site 7, **Parthenon**, with
ceremony start day 21. Original button IDs and rectangles distinguish facility
9 from 11. Initial load snapshots contained uninitialized button IDs; later
snapshots contain initialized controls. Early ignored touches and an unintended
departure are navigation evidence only. The folder named
`ceremony_v809_Athens_Temple_chant` does not contain a verified ceremony.
The valid Temple run is `ceremony_v809_Athens_Temple_actual`.

## Verified display; outcome evidence has separate limits

The alternate Temple chant has seven complete dialogue/result holds, 19 strict
whole-screen controls and 23 state pairs. All complete native and independent
font planes, real-parent wrapped buffers, substitutions, resident templates,
leading/trailing letters, visible margins, bounds and blank paper pass. Portraits,
speaker labels and all pixels outside the body match V803. Original actors,
towns, items, goods, ship models, tasks, funds and calendar agree, including the
one-day/48-tick advance and normal town return.

The site run plays dance, fast and sacred-peak rites, off-day refusal and an
eligible cancellation. Its 26 complete glyph holds and 22 whole-screen controls
pass before the independent state stage fails. The full state gate is retained
and **FAILED**, not relaxed or replaced by the glyph-only result.

Evidence under `work/analysis/ceremony_Athens_v816`:

- `Athens_Temple_chant_gameplay_verification_v816.json`: complete Temple pass.
- `Athens_site_glyph_stage_only_v817.json`: complete glyph stage only.
- `Athens_site_full_gate_failure_v817.json`: exact retained failure/traceback.
- `climb_original_state_difference_research.json`: byte-level differences.
- `ordinary_PRNG_samples_research.json`: actual random-state samples.
- `post_climb_PRNG_step_count_research.json`: original generator reachability.

At frame 18,200, before the final climb acknowledgment, all covered persistent
objects and the PRNG state match. At 18,600 the calendar advances four days/192
ticks in both ROMs; money, ship models and task records match, but 123 actor bytes
and 87 town bytes differ. The difference persists in later holds. From the common
seed, the original linear-congruential generator reaches the two post-return
states after 860 and 870 calls. The source of that post-dismissal call-count
difference is **not yet mapped**. Do not claim ordinary world-outcome parity or
declare this merely harmless randomness without further evidence.

Fine probes preserve the exact controller/fixture schedule and export RAM at
every frame from 18,200 through 18,240, plus read-only CPU/TCM state at six holds.
Both runs exited normally. Eight selected entire-4-MiB snapshots are identical
to their unprobed counterparts, including the eventual divergent returns. The
first random-state difference is frame 18,203; the streams briefly agree again
at 18,205-18,207. Actor/town data first separates at 18,220. Calendar ticks still
match in the sampled early interval. `read_only_frame_probe_v817.json` pins these
observations. They narrow the post-dismissal investigation; they do not explain
the exact caller/interleaving difference or approve the failed state gate.

One date fixture was applied during a dance level-up notice, before its time
handler. Its 48-tick input change is declared separately; the measured native
four-day increment is 8,600 to 10,200. No uninterrupted action-start-to-end time
claim is made across that fixture. Fast and climb have uninterrupted measured
192-tick intervals. Eligible cancellation advances zero ticks.

The seven Temple plus 26 site captures add 33 glyph-verified holds. Together
with V815 this is 59 holds across 37 distinct revised IDs; this is **not** 59
editorially completed entries. The site outcome gate and other protagonists'
14 distinct reactions remain outstanding, as does final family approval.

## New source/context findings

`Angelo_route_prose_leads_v816.json` pins three clean/current SC1 records and
actual recruitment context. In `DK4_MES_B158_R0039`, 暗いおっさん describes a
gloomy older man; the current "dark old man" is opaque in English. Full neighboring
dialogue review and a natural-dialogue-v2 revision remain required. No black
clothing, racial interpretation or completed route-review credit is inferred.

`levelup_formatting_leads_v816.json` pins clean/current COMMON 335/336 and actual
captures. The combined stat notices can split ability names across lines, for
example `...1!A` / `gility...` and `...1!L` / `uck...`. The letters are present but
the words and adjacent notices are badly separated. This is an open formatting
defect even though those unchanged screens match the old ROM. Map the original
compound-result builder and repair its actual consumer through the registered
workflow. The earlier sulfur-quantity omission remains open too.

Rafael/Maria donor hashes are inventoried without edits in
`remaining_hero_donor_inventory_v816.json`; actual hero identity and load schedule
must be revalidated. A Lil donor was not found in the top-level Saves/Test fixtures
inventory; do not synthesize Lil dialogue under Hodram's identity and call it a
genuine Lil scene.

The ledger remains **550 completed COMMON / 605 source-and-prose reviewed / 55
pending**, with no new whole-family completion credit. V803 remains the last
whole-batch gameplay-verified reference; V809 remains the required integrated
continuation stack. The editorial goal stays active. Graphics and all 18 plaque
audit entries remain separate and unfinished.
