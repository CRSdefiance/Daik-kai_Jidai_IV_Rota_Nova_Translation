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

`town` contains tavern commands, Barkeep role names, Yes/No buttons, Trends, and the
text-backed portions of the sailor-allocation screen.

`all` combines all seven sets.

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
retain its terminator. The fixed profile therefore keeps the harmless fallback `Sal`.
The verified post-build patch expands it to `Salt` by consuming the following duplicate
placeholder slot and redirects that placeholder's only pointer to an identical copy.

The Japanese row labels visible beside name, surname, organization, and birthday use a
second ARM9 table rather than the character-record table. Export and apply the
`character_ui` profile to translate those labels, the embedded edit-row captions, and
the complete birth-date formatter.
