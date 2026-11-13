# V740: stored PXL palette visibility

Every clean/current PXL file was classified: 660 per ROM, comprising 602 single-bank, 42 direct-color and 16 multi-bank files. Among used indices, only fontpanel has equal bank-zero RGB colors that become distinct in another stored bank. Both complete 44x32 interpretations were inspected at 8x; they contain panel texture, with no additional Japanese caption or instruction. Retain the clean-exact image and palettes. All 16 multi-bank palettes remain source-exact. This closes a bounded source RGB visibility check, not low-contrast legibility, bit15 opacity, external palettes, FLS or native contexts. Twenty-nine completed scoped checks now carry forward; five active groups remain. Original 18 incomplete audit objects and 22 historical requirements are preserved. V712 ROM/manifest/patch/registry/canonical and saves unchanged. Goal active, four Online-body exclusions and brown marks retained. See [V740 checkpoint](palette_domains_v740_checkpoint.md).

## Evidence and limits

- [Both stored panel palettes at 8x](<E:/Rota Nova translations/Screenshots/Audit comparisons/V740 Stored palette visibility/fontpanel_banks_8x.png>)
- `work/analysis/palette_domains_v740/proof.json` records the complete census, used indices, each concealed pair and distinguishing bank, and decoded PNG hashes.
- `translations/stored_palette_art_decision_v740.json` records the visual retention decision.

The comparison examines exact RGB equality: when bank zero distinguishes every used index pair that any stored bank distinguishes, another bank cannot reveal additional index geometry hidden by exact color equality. This does not imply every color contrast is readable or any bank is the native selection. Only the one newly identified hidden domain received new visual review. Existing full-source reviews carry forward. These PNGs are decoded artwork, not emulator screenshots.

Original comic playback, small-control parents, village-card triggers, legacy consumer relationships and final integrated acceptance remain open. The prior context-recognition question remains pending. No absence of response is treated as a retention decision. Revisit older record-based checks after actual completion.
