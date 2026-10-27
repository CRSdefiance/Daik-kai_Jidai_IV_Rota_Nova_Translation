# V784: item-shop and diplomatic-letter editorial research

COMMON1070-1145 receive76 clean-source/context/prose reviews:63 proposed revisions
and13 retained wordings. They are drafts,with all production-formatting gates false.
496 entries have source/prose review,79 are drafts and417 remain completed
(293 revised/124 retained). V783 remains the current integrated candidate;no ROM,
patch,registry,canonical input,original save or frozen production dependency changes.
The full editorial goal and separate unfinished graphics audit remain active.

## Meaning and fluent English

The group contains item buying/selling and bargain voices,letter delivery,recipient
and joint-enemy selection,pact confirmations,letter drafting,no-recipient/no-enemy
responses,and warnings that a target is unlikely to submit. Sixteen current entries
repeat the unrelated question "Which faction should we oppose?" in those other
contexts. The drafts restore each actual meaning instead of polishing the wrong
question. Full source/current bytes and native offsets are pinned in the manuscript.

1072 is an insufficient-funds taunt,not another purchase confirmation. The invented
"Buy it?" is removed there. Actual source1073 still asks whether to buy. Numeric
prices come from originalABF50 as full-width digits without units;coins is supplied
once by the prose. Source1097 charges1000 gold coins for courier service;it is not
a job reward. The original dispatch subtracts1000 at5BB00. Source1130 preserves
the five-or-six-day courier wait rather than inventing an exact guaranteed date.

The original bargain calls select role3 Purser,not the captain. Diplomatic speech
selects role1 First Mate,with the game's own fallback. Ten voice tables cover2080
original actor selections plus null fallbacks. SourceIC in1118/1140 is a first-
person pronoun;English uses I/our without inventing an actor name. Unlike the old
V115 snapshot,current53914 has two registered F/I literal guards. Those exact two
branch slots and the complete resident guard bytes are verified;restoring only
those slots reproduces the entire clean parser span. IC behavior is retained.

## Six diplomatic type arguments

Original93D5C still returns Japanese for types0-5:goodwill,pact formation,pact
termination,truce,war declaration and intimidation. New drafts propose contextual
nominal English phrases:goodwill letter,pact proposal,notice of pact termination,
truce proposal,declaration of war,and demand for submission. This lets recipient
questions and confirmations read naturally without mistaking the type for a
letter's owner or leaving Japanese inside English sentences. All source argument
positions remain intact:recipient first,type second;partner before opponent in
the separate pact confirmation. Established menu action names are not renamed.

The proposed phrases are explicit research inputs,not current getter results.
Their owned storage,routing and complete consumer preservation are still required.
Three original direct-call leads reach this getter. The third,56F34,belongs to the
earlier Strategist table915-920 and supplies action indices6-9. Those four labels
are already English and must remain exact. No global getter rewrite is performed.
Indirect references and full caller closure remain an implementation gate.

## Prospective formatting and visual checks

2774 original printf/existing literal-formatter prototype cases pass complete-word,
four-row/35-byte bounds,guard and weak-ending checks. They cover the original20
named faction values,all supplied partner/opponent combinations,six proposed type
phrases and explicit numeric-width stress values. Not every supplied combination
or numeric bound is claimed eligible or earned. Slot20 is an empty sentinel,
excluded according to the original diplomatic loops'0-19 bound. An initial21-slot
assumption failed on that empty slot and was corrected without changing game data.

76 complete native font planes independently match the original game font. All
seven sheets are visually reviewed for natural reading,full leading/trailing
letters,consistent visible margins,complete substitutions and bounds. There are
no remaining prototype findings. These directly invoke an existing formatter;
they do not prove the future private dispatcher,provider implementation,all
portrait/confirmation consumers or actual player-visible scenes. No formatting
approval or completed-entry credit is granted from these previews.

## Next work and preservation

Finish the Guild NPC constructor/core binding and full branches/argument/filter
contracts. Implement the six contextual type phrases in verified owned storage,
preserving earlier6-9 behavior. Extend exact native routing without growing a
section,BSS,cache,arena or the123040-byte staged payload. Then integrate all prose
through the registered stack,verify native copies and exact clean-input patch,
and exercise actual buy/sell/bargain and diplomatic scenes plus ordinary startup.
750-752 remain queued for original context mapping;1146 onward,all routes and other
prose remain in scope. The18 plaques,Online-body exclusion,preserved brown marks
and older-record follow-up remain unchanged. No commit or GitHub push is made.

Research and preview sheets are archived under E:/Rota Nova translations/Editorial
review/V784 Item and diplomacy research. They are CPU previews,not gameplay or
finished guide screenshots. The previous goal turn completed50 entries;this turn
makes progress on the next76 through source review and prototype verification.
