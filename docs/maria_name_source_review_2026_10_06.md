# Maria name source review

**Confirmed by the user:** Maria Huamei Li. The research recommendation below is
now the selected spelling. ROM implementation and its formatting/native checks
remain pending. The user also confirmed Camille; the full naming rationale is
recorded in `docs/glossary.md`.

The user confirmed **Rafael** and **Joakim** on 2026-10-06 and asked to resolve
Maria's inconsistent full name. The subsequent discussion settled Camille.

## Primary source evidence

The Japanese publisher's [official character manual](https://www.gamecity.ne.jp/manual/dk4HeN38/jp/1500.html)
names her **マリア・ホアメイ・リー** and identifies her as a Ming female admiral.
This agrees with the clean DS source's Maria, ホアメイ and リー fields.

The licensed series operator's [official announcement](https://gvo.wasabii.com.tw/notice/noticeContent.aspx?K=34443),
dated 2017-06-08, names Lil's associate **瑪莉亞・華梅・李** in a series crossover
event. The announcement also names Lil Argot and Camille/Kamil Overijssel in its
cast/rewards. This is primary Chinese series-name evidence from a later game;
it is not an exact DS scene transcript or an English localization.

The publisher's [Chinese HD site](https://www.gamecity.com.tw/d4/hd/index.html)
also identifies the character as **瑪麗亞・李**, supporting retention of Maria
and the surname character 李. The full middle name is not supplied there.

## Recommended English spelling

**Maria Huamei Li** preserves Maria and uses Mandarin romanization for 華梅 and 李.
Huamei is one given name; the Chinese characters do not require an English space
or hyphen between Hua and Mei. This is a localization recommendation inferred
from the primary spellings, not a claim of an official English release spelling.
Lee is a legitimate alternative surname spelling; the recommendation is to choose
one consistent scheme for this Chinese character and her family/faction labels.

**Maria Hoamei Lee** follows the Japanese sound-based rendering more closely and
can be defended as a consistent adaptation. The current project mixes it with
**Maria Hoa-mei Lee** and **Maria Huamei Li**; the mixture needs correction.

Retain Maria. Do not invent a baptism, birthplace or religious explanation merely
from the presence of a Western name. Secondary sources make such claims, but they
have not been verified against the DS narrative and are not a translation basis.

## Current implementation evidence and required checks

`work/analysis/name_decision_inventory_2026_10_06.json` locks V190's exact ARM9
identity, stored surname Lee, untranslated middle-name field ホアメイ and four
active full-name story variants. The ordinary given-name-only audit did not cover
this middle-name field; it cannot prove complete full-name translation.

Selecting Li changes surname length from three ASCII bytes to two. Recheck actual
name/faction macro expansion lengths, source-locked route formatting and parity,
allocated name ownership, native drawing, full source context and story variants
before integration. Do not replace encoded bytes indiscriminately.

The initial research changed no ROM, patch or accepted layer. The user subsequently
confirmed Maria Huamei Li; that decision is recorded in the glossary and naming
policy. The playable ROM remains unchanged.
