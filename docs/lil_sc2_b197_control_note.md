# Lil SC2 B197 celestial-maiden book control note

B197 has 25 source records: 24 natural-English text records and one four-byte
packed event payload. The complete text scene covers the mysterious woman's
book offer to Ian, all three Buy/Pass/Trust choices, the purchase and refusal
branches, her gift when he cannot pay, her disappearance, and the charm reward.
The payload at R0022 is `21 48 8C A8`, correlated with the same nontext
portrait/scene event in Hodram SC1 B201, and is explicitly excluded unchanged.

The woman's `A9`, Ian's `15`, and the reward notice's `FE` presentation states
are preserved. The three choices begin with source byte `94`, the Shift-JIS
first byte of Japanese text. Like B196, this batch removes `94` from its
speaker-state profile, so the English `Buy it`, `Pass`, and `Trust` labels
begin with their visible first letters. Literal uppercase `I` and `F` are
avoided in prose because they are unsafe renderer bytes.

All 24 text records pass the fixed-byte, speaker, choice, wrap, pair-phase,
and first-glyph audit. Both exact-font contact sheets were visually reviewed;
the three choice initials and the charm notice are intact. Direct saved-ROM
verification confirms all 24 records and the unchanged payload. Runtime
cold-boot is still needed for the branches, portraits, nameplates, reward,
and first-letter behavior.
