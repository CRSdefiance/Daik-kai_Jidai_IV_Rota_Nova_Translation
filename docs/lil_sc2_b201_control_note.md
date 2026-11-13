# Lil SC2 B201 mast-rope bargaining control note

All 25 B201 records are translated from the clean Japanese source. A seller
claims Lil's mast rope is worn and offers a supposedly enchanted replacement
for 300,000 coins. Carlo bargains through 200,000, 150,000, and 100,000 coin
offers, with his 30,000 and 75,000 coin counters. Both Buy/Pass outcomes,
the purchase handoff, refusal, and three stat notices are covered.

The seller's `69`, Lil's `02`, Carlo's `13`, and notice `FE` presentation
states are preserved. Both choice records begin with `94`, the Shift-JIS
lead of Japanese choice text; the English `Buy` and `Pass` labels begin
directly with their visible first letters. The admiral's charm and spirit
rewards retain exactly two live `FI` name macros. English prose avoids
literal uppercase `I` and `F`, which are unsafe renderer bytes.

All 25 records pass the fixed-byte, speaker, choice, macro, wrap, pair-phase,
and first-glyph audit. Three exact-font contact sheets were visually
reviewed; both choice initials and the price steps render cleanly. Direct
saved-ROM verification confirms all 25 insertions. Runtime cold-boot remains
necessary to check both branches, prices, stat changes, name expansion,
portraits, nameplates, and first letters.
