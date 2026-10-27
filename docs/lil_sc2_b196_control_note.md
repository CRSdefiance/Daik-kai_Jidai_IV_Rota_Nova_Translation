# Lil SC2 B196 haggling control note

B196 contains 35 source records, all translated in
`translations/lil_deep_route_v90.json`. A seller offers a charm-enhancing
item for 200,000 coins, then lowers the price through six Buy/Pass choice
pairs to 30,000 coins. All purchase, bargaining, rejection, companion-advice,
and reward branches are covered.

The seller's `AD` presentation state is added to the Lil V90 profile.
`14`, `13`, `06`, `19`, and `FE` are inherited crew and notice states. The
12 choice records all start with source byte `94`, the Shift-JIS first byte
of the Japanese choice text. For this batch, `94` is removed from the
presentation-state set; encoding `Buy` or `Pass` starts directly with its
visible English first letter. The system reward retains exactly one live
`FI` name macro. English prose avoids literal uppercase `I` and `F`, which
are unsafe renderer bytes.

All 35 records pass the fixed-byte, speaker, choice, macro, wrap, pair-phase,
and first-glyph audit. Both exact-font contact sheets were visually
reviewed; every Buy/Pass initial is intact. The `FI` macro appears as a
preview placeholder and still needs runtime name-expansion review. Direct
saved-ROM verification confirms all 35 inserted records. Runtime cold-boot
remains necessary to check every price, choice, purchase outcome, reward,
portrait, nameplate, and first letter.
