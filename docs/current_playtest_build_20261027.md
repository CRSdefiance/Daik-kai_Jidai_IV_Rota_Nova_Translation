# Current combined playtest build — Lisbon Guild/Ruins repair, 2026-11-01

Use `out/all_routes_combined_lisbon_guild_fixed_20261101.nds`, SHA-256 `7470d392590fed3ee70d7301f42d9acdbf500e771e2191c522cec575f3c1cd94`. This retains the complete V8865 translation/graphics/font stack and fixes the Guild and Ruins tooltip bitmap-header overwrite. All twelve town building types pass both native caption layouts; all eight available Lisbon buildings pass actual hover, entry and return checks. The registered 649-entry/114-accepted-layer manifest passes all 19 release checks and exactly matches the tested image and clean-input patch reconstruction. The sibling `.xdelta` is the verified clean-input patch. Status is experimental, awaiting user 3DS cold-boot acceptance; canonical/promoted builds remain unchanged.

See [complete build identity, fix and coverage](lisbon_guild_hover_fix_20261101.md). The earlier handoffs below are preserved as historical records.

# Historical combined playtest build — V4766

Use `out\all_routes_combined_v4766_candidate.nds` (SHA-256 `c3a9a133f7d149995a5d0feae824da32bc6741603f023ba7cda1cefb79ff4503`). It contains the complete repaired font/Square stack and latest integrated translation, plus the two-line shopkeeper correction. All561 registered entries/114 accepted layers and18 release checks pass. The clean-input patch is `out\all_routes_combined_v4766_candidate.xdelta` (SHA-256 `eb5b29424464d83d1cc206cb32ee6bd6d9a4e90aca21e8b78469b2953aed7af0`). Only one COMMON message changes from the previous repaired playtest build; every word is retained. The changed reply was viewed during ordinary shop gameplay; startup, town return and complete-pixel checks pass. Status remains experimental; promoted main and canonical baseline are unchanged. The earlier tutorial/crowd/Lisbon gameplay acceptance request remains open; this formatting test does not certify that sequence.

Details: [V4771 checkpoint](shop657_full_width_reflow_v4771.md). The previous handoff follows as historical evidence.

# Current combined playtest build — 2026-10-27

Use `out/all_routes_combined_font_and_square_fixed_20261027.nds`. This is a fresh registered build of the complete latest
integrated V4749 translation stack with all five font/punctuation/Square repair
layers. It reproduces the complete earlier repaired ROM byte for byte. V138 was
an October 1 historical test input restored during the audit; its fresh file date
did not make it a current release.

- Candidate SHA-256: `89860905d61e348ae053d40836159bc86bff5d85d3206ce3a0961a6d60142077`.
- Status: **experimental**, awaiting gameplay acceptance; no promotion.
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`.
- Base SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- Profile: `font-v2-square-scratch-fix-20261027`.
- Accepted content: all 114 accepted layers remain baked into the immutable base.
- Applied cumulative content: all 560 manifest entries, including the latest
  integrated editorial content, font design, one-pixel drawing offset, both
  punctuation repairs and the per-call Square scratch repair. No retired V138
  bytes are used as a parent.
- Manifest: `out/all_routes_combined_font_and_square_fixed_20261027.manifest.json`; it lists every batch, changed record, source
  lock and all 18 passing release checks.
- Verifiers: fresh registered build, complete prior-repair byte equality,
  manifest/registry/baseline checks, exact font fingerprint, disjoint Square
  code/scratch contract and 30 font/integration/text-safety tests pass.
- Fresh automated headless cold boot: 2,400 ordinary-input frames, no save/state
  or gameplay fixture, no callback errors. Lil's confirmation frame 2000 was
  viewed: complete “Everything correct?” prompt and current font.
- User gameplay acceptance still needed: cold-boot this exact file, choose
  Raphael's guided tutorial, finish it, observe the crowd alert, then enter and
  leave Lisbon's Square. That exact sequence remains pending; this handoff
  does not claim it passed. Do not load the frozen state, which restores the
  overwritten instructions from the failed build.

Detailed verification: `work/combined_handoff_20261027/verification.json`.
The new candidate is pinned for retention. Existing ROMs, sources, canonical,
registry and promoted main are preserved.

## Changed internal files relative to the canonical base

All 53 paths are inherited from the complete repaired stack;
there are zero byte differences from the previously verified repaired ROM.

```text
/COMMON/HELP.DK4
/COMMON/MESFILE.DK4
/FLS/M22.fls
/FLS/M24.fls
/FLS/M28.fls
/FLS/logo.fls
/GRP/CMMNIMG.DK4
/GRP/DSOBJR.DK4
/GRP/SLACKIMG.DK4
/GRP/WINFRAME.DK4
/Iseki/dock.pxl
/__arm9__.bin
/_pxl/__frame.pxl
/_pxl/__marker.pxl
/_pxl/chihofleetinfo.pxl
/_pxl/deck04.pxl
/_pxl/dividecrewinfo.pxl
/_pxl/forceinfo.pxl
/_pxl/goldsearoutediscovery.pxl
/_pxl/goldsearoutelog.pxl
/_pxl/goldsearoutelog2.pxl
/_pxl/haifuhin.pxl
/_pxl/kakutei.pxl
/_pxl/logo.pxl
/_pxl/mysterymap/mys_hunt_d.pxl
/_pxl/online/Online24.pxl
/_pxl/online/Online27.pxl
/_pxl/online/Online31.pxl
/_pxl/online/Online33.pxl
/_pxl/personinfo.pxl
/_pxl/saveloadinfo.pxl
/_pxl/senrihin.pxl
/_pxl/shipinfo.pxl
/_pxl/slackimg12.pxl
/_pxl/slackimg20.pxl
/_pxl/startmenu0.pxl
/_pxl/tempcargo.pxl
/_pxl/title/title03.pxl
/_pxl/title/title05.pxl
/_pxl/towninfo.pxl
/_pxl/winframe00.pxl
/data/SC0.DK4
/data/SC1.DK4
/data/SC2.DK4
/data/SC3.DK4
/evstill/evstill168.pxl
/evstill/evstill169.pxl
/evstill/evstill170.pxl
/evstill/evstill171.pxl
/evstill/evstill206.pxl
/evstill/evstill207.pxl
/evstill/evstill208.pxl
/evstill/evstill209.pxl
```
