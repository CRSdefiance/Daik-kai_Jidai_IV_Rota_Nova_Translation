# Zodiac names and stat bonuses

All 12 Japanese sign names sit in the first word of their original 28-byte table entries. The mapped actor-stat routine selects that entry and reads six numeric coefficients starting in its second word. The clean and current table, selector, caller and access instructions match. Native execution verified all 72 coefficient reads and rejected both out-of-range sign indices. [Exact table, names, and caller evidence](../translations/editorial_checkpoints/shared_display_20261123/zodiac_stat_table_scope_20261123.json)

The aligned address scan of ARM9, its autoload sections and overlays found the 12 name pointers only in this table. Earlier character-profile QA shows the sign through an icon. Preserve the original numeric table and keep the exact names on file for any indirect caller that turns up. This is an offline disposition for the mapped stat path. [Earlier character-profile checks](small_controls_v701_checkpoint.md)
