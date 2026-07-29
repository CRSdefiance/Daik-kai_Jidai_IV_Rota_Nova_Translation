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
  --batch translations/raphael_mediterranean_story.json `
  --batch translations/common_early_prompts.json `
  --batch translations/tavern_and_recruitment.json `
  --batch translations/help_early_game.json `
  --out out/expanded_translation_test.nds --mode ilnk
```

The current expanded build contains the Raphael prologue through the first continuous
trade and sailing tutorial, the following Mediterranean strategy scene, plus shared
departure, docking, options, save-data, battle-result, tavern recruitment, and
item-shop bargaining prompts. The pointer-safe `HELP.DK4` batch now covers game goals,
captain advantages, taverns, trade, diplomacy, palaces, shipbuilding, dock and regional
fleet management, ports, sailing controls, exploration, and naval combat. The
`characters`, `character_ui`, `city`, `menus`, `world`, `shared`, `town`, and `market` ARM9
profiles translate character data and labels, Lisbon and Seville data, navigation and
deck commands, recurring port names and roles,
early-story speaker names, city icon hover labels, tavern commands, confirmation
buttons, sailor-allocation strategies, the global trading-category menu, and the first
global faction/commodity records.

The shared graphics pass redraws character-selection, city, fleet, faction, sailor,
person, save/load, ship, and Golden Route interface captions in English. It also
replaces the Japanese Rekoeition production card and four Japanese cutscene subtitle
cards:

```powershell
python scripts/build_graphics_translation.py out/market_and_deck_tutorial.nds `
  --out out/graphics_ui_and_cutscenes.nds `
  --preview-dir work/graphics_preview
```

See [LEGAL.md](LEGAL.md), [docs/workflow.md](docs/workflow.md), and
[docs/testing_plan.md](docs/testing_plan.md).

## Dedicated input and calendar build

`out/input_calendar_en.nds` rebuilds the complete current translation and adds the
character-input/calendar pass. It clears the full character-editor heading before
drawing each title, relocates the fixed-width `Name` and `Last` popup labels so they
are safely terminated, translates the popup Done button and birthday heading, and
labels the shared built-in Latin and symbol keyboard pages `ABC` and `#+`.

The calendar audit covers the shared numeric month suffix used by all twelve birthday
months, work and voyage duration formats, the 3/10/30-day inn choices, continued
stays, current/previous/relative-month reports, both arrival-month labels, departure
dates, and the related inn and sailing-range dialogue. The post-build binary changes
are verified rather than applied to unknown bytes:

```powershell
python scripts/build_input_calendar_patch.py out/input_calendar_text_stage.nds `
  --out out/input_calendar_en.nds
python scripts/verify_input_calendar_build.py out/input_calendar_en.nds
```
