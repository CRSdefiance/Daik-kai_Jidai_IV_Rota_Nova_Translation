# Rafael opening: missables and review queue

Research date: 2026-10-11. This file accompanies [the opening chapter](../chapters/02-rafael-opening.md); it is not a complete scenario missables list.

## Checklist for the opening

- [ ] Read the ship warning before R01.
- [ ] Preserve a pre-R04 save for branch testing.
- [ ] Confirm each recruitment in the roster, not just a dialogue screenshot.
- [ ] Reconcile R04's alternate-condition report before publishing a workaround.
- [ ] Verify the R10 reward through a before/after funds comparison.

The [mixed-version general wiki](https://w.atwiki.jp/offlinedaikoukai/pages/19.html), ４PKの難易度 → ラファエル, also warns that losing the original ship blocks Cesare. This corroborates the warning but does not independently prove DS behavior.

Dekuno's R04 note describes **docking the original and naming an active ship カルテイラ**. This does not establish that selling the original and renaming another is safe. [DS article, スタート → アレキサンドリア](https://dekunobou-rotanova.seesaa.net/article/48270717.html). Test ownership and naming separately; do not recommend this alternate condition yet.

## Advance warning for the next Africa chapter

At Sofala's 聖母の像 event, **「その通り」** grants the **Madonna Figurehead**; **「まさか」** forfeits it for different stat gains. [Dekuno, アフリカ → ソファラ遺跡](https://dekunobou-rotanova.seesaa.net/article/48270717.html). Status: DS-source-reported; recovery possibilities untested.

Updated for v0.2: use Rafael's own **Exactly / No.** wording, retaining the Japanese alongside it. Translation provenance: [Rafael figurehead batch](../../translations/raphael_deep_route_v65.json), `DK4_MES_B260_R0049` and `DK4_MES_B260_R0051`, in `/data/SC0.DK4`. This supersedes the provisional labels borrowed from Lil's route. Item name provenance: [accepted item-name batch](../../translations/all_item_names_arm9_v1.json), `DK4_ITEM_POINTER_123`. Exact Japanese-to-item-ID mapping and current ROM display remain to be checked.

This warning is outside the opening chapter's endpoint. Retain it in the review queue so it can be placed before the relevant choice when that chapter is written.

## Unresolved protagonist bonuses

| Topic | Evidence tension | Editorial decision |
|---|---|---|
| Guild rewards | Dekuno's ラファエルの特徴 mentions gold/share rewards. The general wiki's trait table distinguishes PK guild bonuses from a Rota Nova discovery bonus. | Do not promise an enhanced DS guild reward formula. |
| Military investment | Both sources report 80% of normal cost. | Corroborated source claim; measure an equivalent DS comparison before certification. |
| Discovery bonus | Wiki table attributes doubled discovery influence to the Rota Nova book. | Secondary attribution only; the book has not been read. |

Sources: [Dekuno, ラファエルの特徴](https://dekunobou-rotanova.seesaa.net/article/48270717.html); [general wiki, はじめてプレイするなら and ４PKの難易度 trait table](https://w.atwiki.jp/offlinedaikoukai/pages/19.html). Both accessed 2026-10-11. Wiki reports remain Cross-platform-unverified; the DS article remains DS-source-reported.

## Branch-test protocol

Begin with an identified ROM and reproducible pre-event save. Preserve the untouched branch. Change one condition at a time, trigger the same facility/event, and record whether recruitment or reward appears. Include failures as evidence. A portrait or item screenshot demonstrates an outcome in that branch; it does not prove the full set of required conditions.
