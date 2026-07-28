# ARM9 translation profiles

The game stores several user-interface and character-selection tables directly in ARM9.
These are not part of the Nintendo DS filename table, so they are represented by the
special script path `/__arm9__.bin`.

## Profiles

`startup` contains:

- title menu choices;
- shared `Back`, `Done`, and `Edit` controller labels;
- the character-selection heading and `Born` suffix.

`characters` contains the given name, surname, organization, and three biography lines
for:

- Lil Argot;
- Raphael Castor;
- Hodram Bergstrom;
- Maria Lee.

`city` contains the first verified city-screen vocabulary:

- the four information headings and the `City` / `Normal` values;
- the `Port` and `Common` buttons;
- both Lisbon name slots;
- Salt, Guns, Saffron, Almond, and Olive Oil.

`menus` contains 51 reusable labels for common commands, deck rooms and policies,
crew assignment, and the city navigation choices. It is the first large shared-menu
pass, so its labels recur across several menus rather than only one screenshot.

`world` contains 29 recurring port names, including Seville, Malacca, Algiers, London,
Genoa, Valencia, Marseille, Calicut, Batavia, and other major locations.

`shared` contains recurring early-story names and the city icon hover labels for the
Tavern, Market, Palace, Square, Shipyard, and other locations.

`all` combines all six sets.

```powershell
dk4tool extract-arm9-profile clean.nds `
  --profile all `
  --with-drafts `
  --out work/arm9_all.csv
```

The current records are fixed-width. Biography drafts deliberately use trailing ASCII
spaces when needed so that replacements occupy the exact original byte length and leave
the game's line-break delimiters untouched. Some city vocabulary entries use the
verified zero padding at the end of their fixed table slot, allowing `Normal`, `Common`,
and `Lisbon` to fit without moving pointers or neighboring records. The Salt slot must
retain its terminator, so it uses the safe abbreviation `Sal`.

The Japanese row labels visible beside name, surname, organization, and birthday do not
respond to either mapped ARM9 text table. Emulator tests indicate those labels are
graphics and require a separate tile-resource workflow.
