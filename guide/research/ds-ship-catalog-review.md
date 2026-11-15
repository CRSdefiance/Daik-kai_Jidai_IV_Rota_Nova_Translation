# Original DS ship catalog field mapping

October 12, 2026. Clean ARM9 read directly from clean.nds; hash locked in ds-ship-catalog-reference.json. Thirty-four consecutive56-byte records starting0x11C7A8 and ending0x11CEE0. Pointer +0 resolves original Japanese hull type; halfword+4 correlates small/medium/large; halfword+6 matches Kurogane hull value; word+8 matches Kurogane base price. All34 hull/price pairs agree, not a selected example. Field semantics are source-correlated; no purchase consumer execution or actual equipped quote test performed. +52 availability word retained raw and not promoted as fully decoded runtime stock flags.

Thirty English type labels read at the same pointer fields in the existing generated_item_advice_research_arm9.bin snapshot; four later labels follow entity_ship_names_arm9_v2.json: LineShip/Sekibune/Sueyoshi/Ironclad. Existing compact labels Hanse Cog/Lt Galleon/Sm Galley/Lg Galley/Atake retained, and original Japanese paired in14.6. No new name decision or translation edit made.

Wiki66 standard-equipped prices and some hull figures differ. Distinguish catalog base values from actual equipped/refitted quote rather than assuming every difference proves platform behavior. Full capacities, room-specific crew calculation, and unlock thresholds remain incomplete. No ROM/save/source/screenshot edits.

## Starting layout comparison

Parsed five-row vessel groups from Kurogane ship table; all34 existing DS names mapped. Cargo/supply/marine/gun/extra/total holds and required/maximum sailors remain source-reported layout figures, not decoded DS crew calculations. Masts count occupied published fore/main/aft positions. Neither this count nor the table proves speed or stock/unlock rules. New section09.20 explicitly distinguishes these from source-correlated original base fields.
