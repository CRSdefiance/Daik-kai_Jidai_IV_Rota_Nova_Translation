"""Read/gloss the whole following clean exchange before exposing predecessor English."""
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B169_clean_context_v4210')
INVENTORY = Path('work/analysis/lil_B161_B180_clean_scope_v3910/complete_clean_B161_B180_next_exchange_inventory.json')
CONTEXT = '''Lil finds Camille researching a treasure called the Proof of the ruler/conqueror; its exact approved current English terminology must be bound independently. Camille hesitates to reveal who knows a clue. Mikhail proudly announces himself and greets FI with overfamiliar affection. Lil shrieks, calls him a sexually harassing old man and explicitly warns that she will hit him again if he touches her. This subsequent exchange supplies an explicit again/hit statement; do not retroactively invent a named blow or body part in B168's yelp. Camille tells FI she is going too far. Mikhail complains that she is cold despite being so cute; this is his intrusive characterization, not consent or a family/romantic relationship. Camille is thrown off balance and tries again with a flattering, elaborately respectful address to Mikhail Letzel as a natural-history expert. The literal source title 博物博士/博士 is an honorific/flattery here; reconcile its wording without asserting an academic degree or unrelated navigator rank. No surname/middle name beyond the printed source is invented.
Mikhail responds to the flattering title, theatrically clears his throat and addresses FI instead of Camille. Lil points out who asked, then asks whether he really knows what the Proof is. Mikhail describes treasures scattered among the regions' seas, said to be held by those who rule the sea; detailed knowledge remains mysterious. Ancient documents say there are exactly seven treasures and that the ancient Seven Sages marked their locations on maps of various shapes. One day a person who rules that sea is destined to receive its map. Keep legend/evidential qualifications, seven treasures/seven sages, location-marking, map shapes and future destiny. Do not add numeric dominance thresholds, guaranteed rewards, treasure ownership, assembled map pieces, an eighth region or a historical verification claim.
Camille excitedly imagines FO acquiring it; Lil reflects on a token of a ruler of the seas. Three optional actor6/21/20 remarks comment separately: Mikhail sometimes says something sensible; FO would be proven the strongest in that sea; the speaker is unsure but thinks they must collect all the Proofs to get anywhere. Bind actors, complete source branches and chronology before localization. These are comments, not source instructions to invent a new fleet/family rank, actual collection or a choice menu. Mikhail asks whether his learning has impressed them. Lil reluctantly admits it, says he must be useful aboard her ship and repeats the no-touch boundary. His laughing reassurance does not convince her.
Camille asks how they should collect the Proofs. Mikhail first advises becoming the strongest power in a sea; influential people in the regions often possess clues. If an evil-minded person has one, defeating that person may be necessary. Keep often/if/likely and the distinction between a clue and the Proof itself. Lil paraphrases this as beating the bad guys. He also tells them to discover ruins in cities and unravel the mystery of sealed Proofs. Lil asks how to find ruins. He answers women, provoking her bafflement, then explains that large towns should offer clues to nearby ruins. Lil presses him to explain. Tavern women hear sailors' stories from around the world every day and must know something. Such important information is unlikely to be given for nothing. Lil complains about stinginess; Mikhail calls it give-and-take and a small price compared with the treasure they seek. Preserve the tavern/information/payment context and comic delayed explanation. Add no bribery rule, explicit gifts, romance/seduction, exact price, named port, stat threshold or real-world gender generalization by the narrator.
All36 source speeches belong to one contextual review, including the optional remarks. No predecessor English has been exposed. Current name/voice/catalogue, source controls/eligibility, approved Proof/ruins/sea-region terminology, runtime substitutions, native formatting, representative actual behavior and registered integration remain pending. This clean/gloss pass adds no ledger or completion credit. Every wider storyline, shared shop/town dialogue, random scene, Help and other prose remains within the active goal; graphics and the later older-record technical re-audit remain separate.'''
MEANINGS = {
5: 'Lil notices Camille and casually asks what he is doing. This is an immediate conversation opener, not a new meeting or invented location.',
8: 'Camille acknowledges FI and explains he was researching a treasure called the Proof of a conqueror/ruler, then trails off before identifying who knows a clue. Preserve FI, the reported name and unfinished hesitation; approved current terminology must be bound.',
12: 'Lil asks who knows. Her eager question sets up the reveal, without supplying a name prematurely.',
16: 'Mikhail proudly reveals that he is the person who knows and gives FI an enthusiastic overfamiliar greeting. Preserve the boast and FI; the familiar suffix creates no relationship.',
20: 'Lil shrieks at the lecherous old man appearing and explicitly warns she will hit him again if he touches her. Preserve the unwanted-contact boundary, again and conditional hit; no body part or particular blow is stated.',
24: 'Camille tells FI that she is saying too much/going too far. Keep his awkward moderating response and exact FI, not a judgment that her boundary is wrong.',
28: 'Mikhail complains that FI is cold/unfriendly even though she is so cute. Preserve his intrusive compliment and exact FI; add no consent, age or established intimacy.',
32: 'Camille says this throws him off, then addresses Mikhail, correcting himself to an elaborate respectful form naming Mikhail Letzel and his natural-history expertise, before asking about the Proof. Preserve hesitation, self-correction, printed name and unfinished question without asserting a formal degree.',
35: 'Mikhail says the flattering expert/doctor title leaves him no choice, theatrically clears his throat, then asks FI whether she is interested in the Proof. Preserve the title response and comic redirection to FI rather than Camille.',
38: 'Lil points out that Camille is the one asking, then lets it pass and asks whether Mikhail really knows what the Proof is. Preserve mild irritation, skepticism and the central question.',
41: 'Mikhail says these treasures are scattered among the seas of different regions and are said to be acquired by those who rule the sea, though the details remain mysterious. Keep hearsay and uncertainty, not a verified numeric mechanic.',
44: 'According to ancient documents there are exactly seven treasures, and the ancient Seven Sages marked their locations on maps of various shapes. Preserve both sevens, documentary attribution, location-marking and different shapes; no map-piece assembly is stated.',
47: 'Mikhail explains that someday whoever comes to rule that sea is destined to receive its map. Preserve future/legendary destiny and that sea/map referent, not an immediate award.',
51: 'Camille begins an excited speculation about their FO acquiring the treasure and leaves the result unfinished. Preserve exact FO and the conditional, incomplete thought.',
55: 'Lil reflects on it as a sign/token of a ruler of the seas. Keep her thoughtful fragment and thematic sense; reconcile the approved Proof term later.',
67: 'Optional actor6 recognizes the explanation and says Mikhail occasionally says something sensible. Preserve the dry backhanded compliment; identity and membership must be bound.',
82: 'Optional actor21 infers that this would prove FO is the strongest power in that sea. Preserve FO, strongest and the inferred question/thought rather than claiming earned status.',
97: 'Optional actor20 admits not really understanding but thinks they must try collecting all the Proofs to get anywhere. Preserve rough uncertainty and all, not a formal new quest acceptance or reward.',
104: 'Mikhail asks whether they are impressed/awed by his learning. Keep his self-satisfied demand for praise.',
107: 'Lil reluctantly agrees, says he must be useful since he is aboard her ship, and firmly warns that touching her will have consequences. Preserve reluctant praise, usefulness and the boundary without specifying a punishment.',
111: 'Mikhail laughingly assures her there is no need to worry. Preserve the breezy old-man laugh and reassurance, not actual trustworthy consent or guaranteed safety.',
115: 'Lil says she cannot trust him at all. This directly undercuts his reassurance.',
119: 'Camille returns to the practical question and asks Mikhail how they should collect the Proofs. Preserve the renewed focus and plural collection goal.',
123: 'Mikhail first advises becoming the strongest power in that sea and notes that influential people in different places often have clues to the Proof. Preserve first, strongest, often, and clues rather than conflating clue and treasure.',
126: 'If an evil-minded person has the relevant clue/Proof, they may need to defeat that person. Preserve the conditional referent and tentative necessity; no indiscriminate attack rule is stated.',
130: 'Lil paraphrases this as beating the bad guys. Keep her brisk practical simplification in response to the previous conditional advice.',
133: 'Mikhail adds that they should discover ruins lying in cities and solve the mysteries of sealed Proofs. Preserve the ruins/discovery and sealed-mystery tasks; bind current site terminology later.',
137: 'Lil asks how they can find the ruins. This is the immediate practical question, not a request for a particular location.',
141: 'Mikhail pauses and answers women. Preserve the comic delayed/suggestive answer as his speech, without explaining it earlier or adding romance.',
145: 'Lil gives a drawn-out baffled reaction. Keep her incredulity, not agreement.',
149: 'Mikhail explains that in a large town they should find some clue about nearby ruins. Preserve large-town condition, nearby and expected clue; do not invent a named port or guaranteed exact ruin.',
152: 'Lil impatiently asks what he means/gets at. Preserve her demand that he connect the women answer with his explanation.',
156: 'Mikhail explains that tavern women hear sailors from all over the world every day and therefore must know something. Preserve who hears what, worldwide visitors and daily repetition; do not make it a narrator claim about all women.',
160: 'He adds that such important information probably will not be provided for free. Preserve significance, likely expectation and payment implication without inventing a price or specific required gift.',
163: 'Lil exclaims that they are stingy. Keep her irritated reaction to the implied cost, not a new factual refusal by a named person.',
167: 'Mikhail says everything in the world is give-and-take and it is inexpensive compared with the value of the treasure they are seeking. Preserve reciprocal exchange, relative value and collective goal, without a numeric price or guaranteed profit.',
}

if __name__ == '__main__':
    assert not ROOT.exists()
    lead = deepcopy(next(block for block in read(INVENTORY)['blocks'] if block['block'] == 169))
    clean = Path('work/clean.nds')
    image = NdsImage.open(clean)
    block = IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[169]
    assert sha(clean.read_bytes()) == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    assert sha(block) == lead['clean_block_sha256'] == '02bd3e65cbc585df1f6598e5a2f8cbf7423ea085118124eba5cd77686a511537'
    assert len(block) == 2564 and lead['speeches'] == len(lead['records']) == 36
    assert lead['FE_panels'] == lead['typed_menu_2100_commands'] == lead['typed_actor_style_4100_commands'] == 0
    for command in lead['complete_native_commands']:
        at = command['offset']
        assert block[at:at + command['native_extent']].hex() == command['whole_command_hex']
    assert {row['source_record_index'] for row in lead['records']} == set(MEANINGS)
    for row in lead['records']:
        at, raw = row['source_reference']['offset'], bytes.fromhex(row['source_hex'])
        assert block[at:at + len(raw)] == raw and block[at + len(raw)] == 0
        assert block[at - 5:at + 1].hex() == row['source_complete_preamble_hex']
        assert raw[1:].decode('cp932') == row['source_Japanese']
        row.update(fresh_source_gloss=MEANINGS[row['source_record_index']], whole_exchange_context=CONTEXT,
                   clean_source_complete_exchange_read_before_predecessor_English=True)
    ROOT.mkdir(parents=True)
    transcript = ROOT / 'SC2_B169_complete_clean_exchange_and_glosses.txt'
    lines = [CONTEXT]
    for row in lead['records']:
        lines.extend(['\n' + row['id'] + ' selector' + format(row['source_selector'], '02X'), row['source_Japanese'], row['fresh_source_gloss']])
    transcript.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    save(ROOT / 'all36_complete_B169_exchange_and_fresh_glosses.json', dict(format='dk4-editorial-clean-source-context-v1',
        source_ROM=str(clean), source_ROM_sha256=sha(clean.read_bytes()), source_SC2_sha256=sha(image.read_file('/data/SC2.DK4')),
        block=lead, total_editorial_objects=36, whole_exchange_context=CONTEXT, source_transcript=str(transcript),
        source_transcript_sha256=sha(transcript.read_bytes()), all36_clean_source_read_and_individually_glossed_before_predecessor_English=True,
        current_names_voices_terms_entry_conditions_macros_native_layout_actual_and_release_still_pending=True,
        no_predecessor_English_exposed=True, no_new_ROM_registry_ledger_orreview_credit=True,
        source_prose_or_completion_credit_added=0, new_emulator_runs=0, full_goal_complete=False,
        evidence={str(path): sha(path.read_bytes()) for path in [INVENTORY, transcript, Path(__file__)]}))
    print(dict(clean_objects=36, FE=0, menus=0, current_English_unexposed=True, ledger_credit=0, full_goal_active=True))
