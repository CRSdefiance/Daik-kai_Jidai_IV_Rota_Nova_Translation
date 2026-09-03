# Build continuity protocol

This is the mandatory procedure for every model and every playable ROM candidate.
Its purpose is to let translation work accumulate without reverting previously
accepted menus, graphics, names, goods, or dialogue.

## Sources of truth

1. `AGENTS.md` contains the non-negotiable repository rules.
2. `translations/release_stack.json` is the machine-readable layer registry.
3. `out/raphael_natural_v2_accepted_base.nds` is the immutable binary baseline. Its
   current SHA-256 is
   `d8cb15aa23e2496510eba8feb18e4536a7da195522b7f5959298b0c1cc0fd1cf`;
   the registry and builder enforce it.
4. `docs/known_issues.md` records failed experiments and renderer hazards.

Never infer quality or ancestry from an output filename. A ROM is a valid candidate
only when its neighboring manifest proves its baseline, layer stack, changed files,
and checks.

## Layer states

- **Accepted:** the user cold-boot tested the layer and explicitly approved it. The
  layer is listed in `accepted_layers` and is applied automatically to every playable
  candidate.
- **Experimental:** the layer is incomplete, failed testing, or awaits testing. It
  belongs to a named profile and is never included in unrelated builds.
- **Revoked:** the build is documented in `known_issues.md` and must not be used as a
  parent, release, or source of bytes.

Only an explicit user statement that a candidate is accepted authorizes moving its
batches into `accepted_layers`. A model must never promote a layer merely because its
automated checks pass.

## Procedure for any requested change

1. **Read before editing:** read `AGENTS.md`, this protocol,
   `translations/release_stack.json`, and the relevant section of
   `docs/known_issues.md`.
2. **Classify the work:** use a disposable research probe when mapping an unknown
   format. Use a named profile for anything handed to the user as a playable test.
3. **Preserve source locks:** author batches against the canonical baseline's exact
   internal file. Never extract translation input from a derivative ROM.
4. **Register dependencies:** if a feature requires multiple batches, add one profile
   containing the complete set. Never rely on a long handwritten list of `--batch`
   arguments for a handoff build. The builder rejects batches that are not registered
   in the selected profile.
5. **Build once:** run `scripts/build_integrated_release.py --profile <name>`. The
   builder automatically prepends every accepted layer from the registry.
6. **Audit the manifest:** confirm the baseline hash, registry hash, profile, complete
   batch list, changed internal paths, and changed record IDs. Missing accepted layers
   or unexpected files are release blockers.
7. **Run targeted verification:** run the feature verifier plus syntax/unit tests. A
   byte-level pass proves preservation, not visual correctness.
8. **Cold-boot test:** never use a save state. At minimum test the title menu, New Game
   character selection, one established story scene, town UI, and every changed screen.
9. **Record the result:** update `known_issues.md` and `todo.md`. If a test fails, keep
   the profile experimental and revoke the candidate by name.
10. **Promote only on approval:** after the user explicitly accepts the candidate, add
    its stable batches to `accepted_layers`, mark them `baked_into_baseline`, retain the
    former baseline as a rollback artifact, and update every canonical hash guard. Do
    not replace the canonical baseline casually.

## Required handoff statement

Every ROM handoff must state:

- exact candidate filename and SHA-256;
- canonical base filename and SHA-256;
- named profile;
- accepted and experimental batches applied;
- changed internal files;
- automated verifiers run;
- cold-boot areas the user must test;
- whether the candidate is experimental, accepted, or revoked.

If any item is unknown, the ROM is not ready to hand off.

## Current Sound Setup status

The former `sound_selector_en_v5.nds` is superseded. The coordinated 38-title BGM
table, interior pointer map, and 57-title SFX table were accepted with the Extras and
Common V6 candidate on 2026-09-03 and are baked into the canonical parent. Their
source-locked batches remain as reproducibility records and must not be reapplied to
the promoted baseline.
