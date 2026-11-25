# Assign Sailors and Sailor Info: translation review V247

Sources: Japanese artwork in `work/clean.nds`, native ARM9 strings, and the skill-name pointer table at `0x021483E4`. Displayed character and ship names follow the established name policy.

## Plaques

| Japanese | English | Reason |
|---|---|---|
| 艦隊水夫数 | Fleet Crew | Total sailors in the fleet, rather than an assignment command. |
| 未編成水夫数 | Unassigned | Sailors who have not been allocated to ships. |
| 航行可能日数 | Endurance | How many days the fleet can remain at sea; the value explicitly says days. |
| 海兵詰所 | Quarters | Marine quarters count; compact label denotes the rooms, not the number of marines. |
| 砲種 | Cannon | Cannon type, with its gun name displayed immediately to the right. |
| 縦帆性能 | Fore/Aft | Fore-and-aft sail performance, including more than lateen sails. |
| 横帆性能 | Square | Square-sail performance, paired with Fore/Aft. |
| 身体 | Health | Physical condition, followed by Healthy, Sick, Injured or another condition. |
| 精神 | Mood | Current mental condition; distinct from the permanent Spirit stat. |
| レベル | Level | Character level. |
| HP | HP | Current hit points. |
| 体力 | Stamina | Physical stamina attribute. |
| 敏捷 | Agility | Agility attribute. |
| 魅力 | Charm | Personal charm attribute. |
| 知力 | Wits | Intellectual ability; concise natural English stat label. |
| 精神 | Spirit | Mental fortitude attribute, separate from the current Mood condition. |
| 運勢 | Luck | Luck attribute; exact native source is 運勢. |

## Equipment heading

| Japanese | English | Reason |
|---|---|---|
| 装備アイテム | Equipped Items | Items currently equipped; source at clean ARM9 0x148CC8. |

## Lower sailor abilities

| Japanese | English | Reason |
|---|---|---|
| 生命力 | Vigor | Life force or vitality, distinct from current condition and HP. Vigor is a natural synonym that fits the native label/value line. |
| 説得力 | Speech | Ability to persuade through speech and negotiation. Speech names the persuasion/negotiation skill in familiar game terminology; the six-letter label leaves room for complete numeric values in the narrow right column. |
| 剣闘術 | Swords | Sword-fighting skill. Swords is a familiar compact skill category and fits the six-character native field without dropping numeric digits. |
| 謀略術 | Guile | Skill in plots and schemes. Guile captures cunning rather than battlefield maneuvers and fits the native line; eight-letter Intrigue wraps the value. |
| 統率力 | Command | Leadership/command ability. |
| 操船術 | Sailing | Ship-handling skill. |
| 測量術 | Survey | Surveying skill. |
| 会計術 | Finance | Accounting skill; compact established label. |
| 命中力 | Aim | Accuracy/hit ability. |
| 観察力 | Observe | Observation ability; compact established label. |

## Headings, conditions and controls

| Japanese | English | Reason |
|---|---|---|
| 水夫を編成して下さい | Assign Sailors | Instruction to allocate sailors. |
| 必要数　現在数　最大数 | Need / Now / Max | Required, current and maximum sailor counts. |
| 約%d日 | %d days | Approximate possible sailing duration; whole days displayed. |
| %s艦長 | %s Cap | Ship captain name and compact Captain abbreviation. |
| 自動 | Auto | Automatic allocation. |
| 最小 | Lo | Set the minimum count; native button leaves only two letters after its L icon. Min was tested and clipped, so retain compact Lo. |
| 最大 | Hi | Set the maximum count; native button leaves only two letters after its R icon. Max was tested and clipped, so retain compact Hi. |
| 完了 | Finish | Complete crew allocation. |
| 航海士情報 | Sailor Info | Information about a navigator/ship officer. |
| 総帥 | Admiral | Fleet/company leader, localized as the naval leadership role. |
| 健康 | Healthy | Healthy physical condition. |
| 通常 | Normal | Normal mental condition. |
| 戻る | Back | Return to the previous screen. |
| 決定 | Select | Confirm the highlighted entry. |

## Native layout constraints

The shared lower skill format is corrected from `%6s%4d` to `%7s%3d`: seven label columns and three numeric columns, with the same total width. Existing seven-letter labels previously clipped numeric digits. The original native getter clamps values to500, so three digits cover its complete range. Fifty native formatting cases verify every label at0/9/97/107/500 with exact text and memory guards. Final live checks verify all ten complete sixty-pixel rows, including every blank and digit. The upper stat plaques retain their own full names and separate bars.

The two compact L/R controls retain **Lo/Hi**, meaning minimum/maximum. Their native button chrome clips the third letter of Min/Max. No truncated three-letter variant is shipped.

## Artwork style

All 17 plaques reuse the original port-information Type plaque: textured paper, native indexed colors and intact two-pixel corners/edges. Interiors are tiled to their widths. The original game font is centered within the bevel, with every glyph row preserved.

The Cannon plaque ends at x122, before the count at x123. Two old right-edge columns are restored from the repeating wallpaper. The dynamic equipment hint uses the same texture through the original native drawing primitive; unrelated managers and cleared hints retain their prior style.

The candidate remains experimental until user acceptance. This source review covers the requested screens; it does not certify every alternate condition or menu throughout the game.

## User-required ongoing plaque audit

On2026-10-09 the user explicitly requested that all17 plaques and the Equipped
Items hint remain in the graphics audit and are not marked fully completed.
Their state is **pending continued audit and user review**. Existing source,
native and two cold-boot proofs remain scoped evidence. They do not close the
plaque audit or establish all alternate states, contexts, characters or devices.
