# Cliff and cave routes, offshore ruins and the missing monk

Reviewed 477 source records in 14 blocks across all four routes. The ledger records 147 prose revisions, 11 wrap-only fixes, one choice-label revision and 318 justified retentions. Rafael's cliff joke still draws a skeptical reply. The snake and bat branches retain their different consequences, and the boat crossing preserves the guide's request to keep the ruins' location from the sailors. Hodram's reunion now echoes what the guide actually says about asking everyone who looks strong enough. [Exact review ledger](../releases/all_routes_editorial_20261118_caves_offshore_monk_candidate/verification/registered_review.json)

Native checks covered 158 revised dialogue and notice bodies, a full set of name-width cases, and both fog menus. The visual pass refined 20 revised layouts. Verisa's warning now uses the available first line and the guide's request keeps the map to the ruins together. The earlier fog choice remains Keep going. The dead-end choice now reads Push on anyway. [Final crossing dialogue](../releases/all_routes_editorial_20261118_caves_offshore_monk_candidate/verification/before_after_1.png) [Both native menu captions](../releases/all_routes_editorial_20261118_caves_offshore_monk_candidate/verification/fog_1984_captions.png)

Initialized gameplay confirmed both fog selections, five dialogue holds and Rafael's arrival response. Separate initialized replays checked all eight dialogue holds from Verisa's two original entry points on Maria's route. Verisa addresses Maria in the opening. The later replies show Rafael Castor with the fixed source selector. The final build reuses these observations where the tested commands and native dependencies are byte-identical. Natural event activation, the unselected branches and hardware remain unverified. [Rafael fog replay](../releases/all_routes_editorial_20261118_caves_offshore_monk_candidate/verification/fog_live_1.png) [Verisa's opening](../releases/all_routes_editorial_20261118_caves_offshore_monk_candidate/verification/verisa_live_1.png) [Verisa and Rafael](../releases/all_routes_editorial_20261118_caves_offshore_monk_candidate/verification/reply_live_1.png)

The clean-input patch reconstructs the exact candidate. It carries all 114 accepted layers and the ASCII right-bound correction. Six cold-boot holds, 24 protected name getters and 32 targeted tests passed. These records already had coverage credit. The ledger remains at 27,700 with 276 pending shared keys. Main awaits acceptance. [Test ROM and patch](../releases/all_routes_editorial_20261118_caves_offshore_monk_candidate/README.md)

## Next exchanges

Paired 550 records in 29 blocks for the fog branches on the other routes, the warrior trials, the village handovers, and the account of the monk's medicine. Rafael's training includes the Tlaloc Knife, the city square, the later map request and the city gate. Keep the individual training branches and the original speakerless Agility notices. The catalog names are Tlaloc Knife, Sextant and Ancient City Map. [Paired clean and current records](../work/warrior_village_handovers_source_20261118/paired_source.json) [Item catalog](../translations/all_item_names_arm9_v1.json)

Packet SHA-256 `c500e30b3716c5c3962c8dd86e78b6bc49b07a25b5a734bdfa6442110352bbb1`.

| Native record | Clean offset | Current offset | First editorial decision |
| --- | ---: | ---: | --- |
| SC0 B336 R18 | 99 | 101 | “Forgive me for asking, but I'd like to put you to the test.” The speaker apologizes before testing a stranger. |
| SC0 B336 R39 | 297 | 339 | Retain the reported origin and purpose. Reflow “to honor their warriors” as a phrase. |
| SC0 B336 R42 | 363 | 421 | “Legend says only someone worthy of the title 'greatest warrior' can find the ruins.” Preserve the legend and the title, and keep the title together. |
| SC0 B336 R51 | 477 | 547 | “It takes more than strength to be the greatest warrior. It takes integrity and wisdom, too.” Preserve all three qualities. |
| SC0 B336 R89 | 879 | 997 | Retain “Those ruins may hold a key to the Proof. Don't you think it's worth a try?” The possibility gives Rafael a reason to accept the challenge. |
| SC0 B336 R112 | 1249 | 1307 | “First, I need to see how you handle a sword. There's something I'd like you to find.” Make the link between the weapon request and the test clear. |
| SC0 B336 R121 and R130 | 1355 and 1481 | 1427 and 1559 | Retain the reported New World location and the promise to use the Tlaloc Knife to teach how the ancient warriors fought. Keep “ancient warriors” together. |
| SC0 B337 R88 and B338 R122 | 669 and 615 | 773 and 707 | Retain the same named map and the city gate rendezvous across the two outcomes. Revisit the break around “meet me.” |
| SC0 B337 R95 and B338 R106 | 791 and 489 | 877 and 557 | Retain the exact FI substitution, Agility and increase by one in both speakerless notices. |
| SC0 B338 R117 | 557 | 619 | “Huh? We still have more to do before we can look for the ruins?” Preserve Rafael's surprise before the map requirement. |

The packet is open. Confirm these decisions in the complete exchanges and check
their final display before integration.
