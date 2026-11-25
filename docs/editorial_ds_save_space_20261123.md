# Legacy save-space warnings and DS cartridge paths

The six archived prompts distinguish four free blocks for game data, one for system data, and five for both. COMMON 108–110 ask whether to start anyway. COMMON 113–115 report the shortfall when saving. The ledger preserves those distinctions, the existing English drafts, and exact Japanese and installed references for each prompt. [Source and native case ledger](../translations/editorial_checkpoints/shared_display_20261123/ds_save_space_20261123.json)

The clean and current ROMs agree in 56 offline runs. The title reads six game-slot headers and the system header. An occupied game slot enables Continue. New Game proceeds with no occupied slots or with all six occupied. In the tested read-failure cases, the title reaches the game-card read warning before offering New Game.

Choosing an unused or occupied slot selects the corresponding native confirmation. Declining writes nothing. Accepting writes the checked system record to its fixed address, then the checked game record to the selected slot. All six addresses passed. A supplied failure at either write reaches the game-card write warning. The prior ordinary Lisbon replay verifies cancellation, the complete progress text, the new slot's checksum, and the return to System. [Lisbon gameplay evidence](editorial_lisbon_new_save_20261123.md)

These dispositions cover the tested DS title and Save paths. Direct callers for the archived free-block prompts elsewhere remain unverified. **269 of 276 shared entries** now have scoped dispositions. The seven open entries include three Market records and four artwork descriptions.
