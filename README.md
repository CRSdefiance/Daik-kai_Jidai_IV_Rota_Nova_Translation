# DK4 Translation Tool

A local, ROM-free Python toolchain for researching an English translation of
**Daikoukai Jidai IV / Rota Nova** for Nintendo DS.

The repository contains tooling and synthetic tests only. You must supply your own
legally dumped ROM. The tool never downloads a ROM and never edits its input in place.

## Install

Requires Python 3.11+. Patch commands use the native `pyxdelta` dependency and
automatically fall back to a system `xdelta3` executable when one is available.

```powershell
python -m pip install -e ".[dev]"
dk4tool --help
```

## Safe first workflow

```powershell
dk4tool info clean.nds
dk4tool manifest clean.nds --out work/manifest.json
dk4tool extract-files clean.nds --out work/files
dk4tool scan clean.nds --out work/scan_report.json
dk4tool scan clean.nds --out work/messages/scan_report.json --include /COMMON/MESFILE.DK4 --include "/data/SC*.DK4"
dk4tool extract-script clean.nds --out work/script.csv --mode conservative
dk4tool extract-arm9-profile clean.nds --profile all --with-drafts --out work/arm9.csv
dk4tool extract-mesfile clean.nds --out work/mesfile.csv
dk4tool extract-mesfile clean.nds --file-path /data/SC0.DK4 --out work/sc0.csv
dk4tool insert-script clean.nds work/arm9.csv --out out/character_selection_en.nds
dk4tool make-xdelta clean.nds out/character_selection_en.nds --out out/character_selection_en.xdelta
dk4tool apply-xdelta clean.nds out/character_selection_en.xdelta --out out/rebuilt.nds
dk4tool validate-script work/script.csv
dk4tool insert-script clean.nds work/script.csv --out out/noop.nds --mode fixed
dk4tool compare clean.nds out/noop.nds --out out/noop_diff.json
```

Blank `english` cells are treated as unchanged during insertion. To replace text, set
`english` and use an appropriate status such as `draft` or `approved`. Fixed mode rejects
encoded text longer than the original byte range.

The first Raphael-route dialogue batch is in
`translations/raphael_opening.csv`. It covers 15 consecutive lines in `SC0.DK4`,
starting with Claudio's “Come on, come on. You'll see.” and ending at the ship reveal.
Build it on top of the character-selection ROM with:

```powershell
dk4tool validate-script translations/raphael_opening.csv
dk4tool insert-script out/character_selection_en_v2.nds translations/raphael_opening.csv --out out/raphael_opening_en.nds --mode ilnk
```

Larger translation sets can be stored as compact, source-hash-locked JSON batches and
combined in one rebuild:

```powershell
dk4tool insert-script out/character_selection_en_v2.nds translations/raphael_opening.csv `
  --batch translations/raphael_prologue_part2.json `
  --batch translations/raphael_tutorial.json `
  --batch translations/raphael_tutorial_deck.json `
  --batch translations/raphael_gap_and_tutorial.json `
  --batch translations/raphael_story_part3.json `
  --batch translations/common_early_prompts.json `
  --batch translations/help_early_game.json `
  --out out/expanded_translation_test.nds --mode ilnk
```

The current expanded build contains the Raphael prologue through the first continuous
trade and sailing tutorial, plus shared departure, docking, options, save-data,
battle-result, tavern recruitment, and item-shop bargaining prompts. A first
pointer-safe `HELP.DK4` batch covers the game overview and several tavern plots. The
`characters`, `character_ui`, `city`, `menus`, `world`, `shared`, `town`, and `market` ARM9
profiles translate character data and labels, Lisbon and Seville data, navigation and
deck commands, recurring port names and roles,
early-story speaker names, city icon hover labels, tavern commands, confirmation
buttons, sailor-allocation strategies, the global trading-category menu, and the first
global faction/commodity records.

See [LEGAL.md](LEGAL.md), [docs/workflow.md](docs/workflow.md), and
[docs/testing_plan.md](docs/testing_plan.md).
