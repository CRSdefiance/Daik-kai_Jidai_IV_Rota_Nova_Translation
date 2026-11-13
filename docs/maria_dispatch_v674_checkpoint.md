# V674: Maria New Game graphics and corrected movie ownership

## Result

One interactive pilot and two fresh frozen-input cold boots finish4000 frames
on the unchanged V666 ROM. They use the existing authorized checksum-valid
system-unlock save. Original New Game selection reaches Maria through three
Right inputs, followed by the ordinary confirmation. No code, movie, live RAM
or savestate is substituted. The existing isolated system flags do not establish
an earned unlock; all source saves remain unchanged.

All14 sampled complete two-screen pairs agree between the observed and baseline
runs, and all11 distinct pilot states agree with those fresh repeats. Complete
terminal4MiB RAM is also equal. The pilot/source-choice screenshots were visually
inspected. This is targeted automated emulator evidence, not full Maria route or
opening-sequence completion.

## Corrected initial hypothesis

The initial preflight incorrectly assumed M26 was the fourth captain's opening
movie, based on the three tested M20/M22/M24 intros. That assignment had not been
proved. The initial source/preflight and two M26 source previews remain retained.
Its images show a wedding; no character or story ownership is inferred from
appearance alone. The unsupported Maria/M26 assignment is retracted.

Full-interval original movie-factory observation adds authoritative evidence:
020D2B1C is called only twice, requesting index0 at frame16 and index28 at559.
Both return addresses bind original clean ARM BL instructions. No M26 request
passes through this factory in the tested4000-frame Maria sequence. This does
not establish global non-use or exclude a different caller/path elsewhere.

The actual court image resident at3800/3900/4000 is evstill084.pxl. Its entire
512-byte palette and49152 indices match the current file, which remains exact
to the Japanese source. At3900 and4000 every displayed upper-screen RGB5 pixel
matches that source:98304 comparisons. Original captain getter7F244 returns3
in both complete court views. Original scene artwork is retained; no new text
or graphical restoration is authored.

## Transition remains explicitly open

Frame3700 is a blank transition, with512 zero palette bytes and49152 black upper
pixels; it is not counted as loaded court artwork. Frame3800 has the complete
resident court source, but the display is partway through a horizontal-blinds
reveal. Exactly17245 nonblack source cells are still black. Every other cell
has its exact source color. The captured software upper buffer also matches
the entire display, as a diagnostic only, not independent expected painting.

The original reveal painter and timing still require verification. Neither
transition frame is silently discarded or counted as a complete source-image
paint. Failed initial four-court and full-reveal assertions, logs and sources
are retained. They were expectation errors, not ROM modifications or established
translation defects. No claim is made that the full Maria opening is complete.

## Instrumentation and script-operand evidence

The unchanged V669 host filter is configured in this private process with one
additional original PC. Its push instruction uses the same source-pinned92F
opcode slot/513F0 host handler. A host-only positive PC-matching/ABI witness and
12 retained filter controls pass. Neither the shared observer nor a live runner
is edited. The slot is restored and the pinned core remains exact.

There are19196 records:19194 ordinary primitive entries with zero guards and
the two FLS requests. Only the latter's first12 register/argument fields are
interpreted. Their guard13 records deliberately inapplicable blitter source,
header and size-pointer fields; it is not discarded or called a valid image
descriptor. These records establish original request inputs, not finished
individual paints or file/scene completion.

The original packed movie decoder and argument fragment are independently
executed for all256 low bytes in clean and current code:512 fragment cases.
Words4200..42FF produce index(low7)+1 and the bit7 option. M26's candidate words
are4219/4299. Byte searches cover all20 recognized script/data containers per
ROM, retaining alignment and surrounding bytes. They are not decoded event
boundaries. Some current candidates overlap speaker-control19 and Latin B42;
none is automatically treated as a wedding trigger. The fragment is not a full
native call/ABI, audio side effects, live trigger or global-unused proof.

## Evidence and remaining scope

- Actual proof: `work/analysis/maria_opening_v674/proof.json`.
- Packed operands: `work/analysis/maria_opening_v674/movie_operand_proof.json`.
- Runs: E Generated/work/emulation_v193/maria_{opening,dispatch}_v674_*.
- Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V674 Maria source dispatch`.
- Scripts: prepare/run_maria_opening_v674.py, run/verify_maria_dispatch_v674.py,
  factory_filter_controls_v674.py and inspect_movie_operand_v674.py.
- Candidate: `out/all_routes_combined_v666_candidate.nds`.
- SHA256: `706350a55a058b7a87b67d396333ed397dac664ba36ea378161d18fd085ba121`.

No ROM, graphics, patch, registry, canonical or release-pointer changes. No guide
promotion. M26's original consumer, the Maria reveal painter, six actual control
contexts, legacy/restoration and other broader gates remain open. All18 plaque
entries remain incomplete, all22 historical scopes stay exact and the graphics
goal stays active. Next follow the actual shared still-image reveal painter
rather than infer movie ownership from numeric ordering.
