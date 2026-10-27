# Combined four-route ROM, Lil V110 checkpoint

Status: experimental; runtime cold-boot and explicit acceptance pending.

- Candidate: `out/all_routes_unified_lil_v110_candidate.nds`
- SHA-256: `93ebdc03eae0ab7686b620951741eb59532fb408e3ac36c49ccd97bcee732bba`
- Unified V76: 377 batches; Lil V110: 120 batches.

B293-B294 adds 98 source-reviewed natural-English cliff/fog records, all
companion variants, Wait/Hurry choices, one-day wait and lost-sailor outcome,
rockfall, dangerous cliff alternative and Mediterranean map hint.
Two packed events remain unchanged. Ten exact-font sheets reviewed.
Zero blockers, 64 Lil tests, Ruff, baseline and nine changed paths pass.
Saved-ROM verification: 21,448 exact experimental records, comprising
Raphael 5,802, Hodram 5,004, Lil 5,689 and Maria 4,953; 218 effective
exclusions unchanged. Another 49 Lil opening records are in the base.
Coverage: 5,738/6,608 translated, 821 remaining, 49 excluded. Continue B295.


## Coverage correction from V829 actual playback

The historical complete-scope claim counted exported decodable rows. A real native speech record,SC2 B294 R73 with presentation94,was omitted by whole-record CP932 decoding and remained Japanese. V829 repairs it with exact source controls and actual display/transition verification. Further raw/native-object coverage is required before broader completeness claims. See [V829 evidence](editorial_v829_completion.md).
