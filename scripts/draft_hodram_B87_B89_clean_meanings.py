"""Finish the 304 clean-first speech meanings; typed-choice scope remains explicit."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

SOURCE=Path('work/analysis/Hodram_B81_B90_clean_20261101/clean_source_packet.json')
OUT=SOURCE.with_name('B87_B89_clean_meanings_before_English.json')
MEANINGS={
87:[
(5,'Actor4 begins an abrupt, hesitant request.'),
(9,'Hodram gives him an opening to continue.'),
(14,'The man politely asks Hodram to hire him.'),
(17,'Hodram recognizes a volunteer to enlist and says he may consider it if the man has useful skills; this is not yet acceptance.'),
(20,'The man likes machinery and says he is good at handling ships and making repairs.'),
(23,'Hodram asks what his terms are.'),
(27,'The man asks to be given one thousand gold coins. Do not relabel the request as wages, a loan, or a fixed repair contract before the reveal.'),
(42,'In the acceptance branch he thanks Hodram and excitedly says he can now make the repair.'),
(45,'He apologizes and asks Hodram to delay departure for just one day.'),
(48,'He says he will meet them at the port office tomorrow.'),
(55,'At the later meeting he says he has been waiting and invites Hodram to look at something nearby.'),
(58,'Hodram reacts with surprise.'),
(62,'The man says yesterday’s money allowed him to finish repairing the ship and that he has just repaid his debts too.'),
(66,'He apologizes for testing Hodram, explaining that an admiral to whom he entrusts his life must have the right qualities.'),
(69,'He says he trusts Hodram and offers him the use of this ship.'),
(72,'Hodram asks to hear his name.'),
(76,'The man misunderstands this as the ship’s name and says Hodram is welcome to choose any name for it.'),
(80,'Hodram clarifies that he means the man’s name, which he still has not heard; preserve the two-turn misunderstanding.'),
(83,'The man apologizes for forgetting to introduce himself because he was so excited yesterday.'),
(87,'He introduces himself as ジェナス・パサー and looks forward to serving together. This identity is distinct from the Ottoman commander Pasha.'),
(93,'The FE instruction says to take the ship out of the dock and use the 改造 menu to give it a preferred name. Bind the actual localized menu term later; do not substitute an invented naming command.'),
(98,'In the refusal branch he accepts the answer reluctantly and says he will try elsewhere.'),
(101,'Hodram is silent after the refusal. Do not connect this silence directly to the acceptance branch.'),
],
88:[
(5,'Hodram recognizes that this is Japan and finds the country unfamiliar or unusual; keep his outsider perspective without adding a stronger insult.'),
(8,'Gerhard calls FI’s attention to a man eating with two sticks, with surprised polite address; do not invent kinship or an extra rank from 殿.'),
(19,'Charles explains that the eating utensils are called 箸, chopsticks.'),
(22,'Gerhard finds this unfamiliar practice peculiar.'),
(29,'Actor41 confronts the group loudly and asks if they are 南蛮人. Review the period term in this hostile outsider exchange without adding a modern racial slur or stripping the confrontation.'),
(32,'He accuses them of swaggering around the land of Japan lately, with an aggressive demand for an answer.'),
(36,'Hodram dryly observes that the man seems to want something from them.'),
(40,'Gerhard agrees that this appears to be the case.'),
(52,'Charles reacts in alarm.'),
(59,'The subordinate cries that he is hurt and calls to his boss. 親分 means his gang leader here, not a parent.'),
(63,'Actor41 claims they deliberately collided with his dear subordinate and broke a bone, feigning alarm. The later rebuttal makes this an accusation or staged pretext, not an objective medical fact.'),
(67,'Hodram reacts sharply.'),
(71,'Gerhard objects that the other side were the ones who bumped into them.'),
(82,'Charles backs up Gerhard’s account.'),
(89,'The subordinate twists the objection into a challenge to fight and claims they both caused the collision and picked a quarrel.'),
(93,'The leader names himself 来島 and theatrically declares that even if heaven forgives this, he will not; he orders his men to attack.'),
(97,'The subordinate obeys.'),
(102,'Hodram observes that the other side have quite a number of men.'),
(114,'Charles says he cannot fight, sounding frightened.'),
(121,'Gerhard says that he and FI are more than enough for this rabble; localize the change-left-over idiom without literal money.'),
(125,'Actor12 announces that he will help them fight.'),
(129,'Hodram reacts with bewilderment.'),
(136,'The newcomer asks them to leave this to him, using a restrained archaic self-reference.'),
(140,'The subordinate challenges the newcomer for being a samurai yet siding with 南蛮人; this identifies the newcomer’s role without establishing a lord or rank.'),
(144,'The samurai says he will judge right and wrong for himself.'),
(148,'The gang leader calls him insolent or too clever and again orders his men to attack.'),
(152,'The subordinate obeys again.'),
(157,'A subordinate cries out as the fight turns against them.'),
(161,'A subordinate theatrically says he has been defeated; do not turn this into a death announcement.'),
(165,'The leader threatens that they will remember this.'),
(169,'The samurai explains that he used the back of his blade and did not cut them. Preserve nonlethal intent; do not invent precise injury outcomes.'),
(173,'Hodram is astonished to find such skill in this island country; his sentence trails off.'),
(177,'Gerhard agrees that the man’s swordsmanship is extraordinary.'),
(188,'Charles says the speed was scientifically impossible, using his characteristic scientific framing.'),
(195,'The samurai apologizes for the shameful side of his country they have witnessed; this is his courteous response, not omniscient judgment of the whole country.'),
(198,'Hodram says they are the ones who should bow and thanks him for helping.'),
(201,'The samurai politely infers that they sail around the world.'),
(204,'He asks if they would let him travel with them.'),
(207,'He says he wants to see the wider world.'),
(210,'Hodram warns that he may never be able to return to Japan. This is a possibility, not an imposed permanent exile.'),
(214,'The samurai says he does not intend to return and, having been born a man, wants to test himself in a wider world. Preserve his period self-conception without inventing a martial order or political banishment.'),
(217,'Hodram approves of his ambition, introduces himself with FI FA, and welcomes their future association.'),
(221,'The samurai introduces himself as ユキヒサ・ゲンジョウ・シラキ. Bind all current name components later rather than swapping in an assumed historical identity.'),
],
89:[
(11,'Gerhard recognizes the item called 新羅の金冠; resolve its approved item name later without importing unrelated historical facts.'),
(15,'Hodram admires both its substantial craftsmanship or weight and its elegance.'),
(19,'Gerhard remarks that one need not be a woman to understand wanting it. Preserve the character’s jewelry joke without making a new narration claim about everyone’s preferences.'),
(24,'Actor26 suddenly notices what Hodram is holding.'),
(28,'Hodram recalls his name as ユリアン and says that despite leaving first he arrived a little too late.'),
(32,'ユリアン asks who Hodram is and whether they have met.'),
(35,'Hodram gives FI and explains that he overheard ユリアン discussing 新羅の金冠 in a Hangzhou tavern.'),
(39,'Hodram says that story interested him and brought him here to search for the crown as well.'),
(43,'ユリアン complains that he had intended to give the item to her as a present. 彼女 alone does not establish a girlfriend, engagement or marriage.'),
(47,'Hodram pauses silently.'),
(51,'ユリアン says his reputation is ruined and he cannot face 美華, then begs Hodram to give him the crown.'),
(55,'Gerhard asks what Hodram wishes to do. Review any intervening player choice separately from the spoken records.'),
(59,'Hodram agrees to the request in the giving branch.'),
(63,'ユリアン asks in delighted surprise whether he really means it.'),
(67,'Hodram tells him to take it: as seafarers they have no use for it and would be wasting the treasure. He permits ユリアン to claim he found it himself; preserve this deliberate generosity.'),
(70,'ユリアン praises his generosity, promises to repay the favor someday, and leaves.'),
(77,'Gerhard starts explaining that such generosity is only to be expected of this distinguished person from FO, but his sentence is cut short. Preserve the runtime faction/fleet macro.'),
(80,'Hodram observes that ユリアン has already left and says he would like a leisurely conversation if they meet again; no future meeting is guaranteed.'),
],
}

if __name__=='__main__':
    assert not OUT.exists();packet=load(SOURCE);rows=[]
    for group in packet['groups']:
        if group['block'] not in MEANINGS:continue
        meanings=dict(MEANINGS[group['block']]);assert len(meanings)==len(group['records'])
        for source in group['records']:
            row=deepcopy(source)
            row.update(source_meaning_gloss=meanings.pop(source['source_reference']['record_index']),
                meaning_read_in_complete_clean_exchange=True,earlier_English_unconsulted=True,
                localization_andfive_gate_approval_pending=True)
            rows.append(row)
        assert not meanings
    assert len(rows)==84
    save(OUT,dict(source_packet=str(SOURCE),source_packet_sha256=sha(SOURCE.read_bytes()),records=rows,
        meanings=84,blocks=list(MEANINGS),source_only_no_English_comparison_orlocalization=True,
        typed_choice_records_not_counted_as_speeches_andrequire_separate_intake=True,
        B90_zero_speech_control_block_still_retained_in_source_packet=True,
        exact_individual_source_references_retained=True,new_credit=0,
        producer_sha256=sha(Path(__file__).read_bytes())))
    parts=[SOURCE.with_name(name) for name in ['B81_B85_clean_meanings_before_English.json',
        'B86_clean_meanings_before_English.json','B87_B89_clean_meanings_before_English.json']]
    combined=[row for path in parts for row in load(path)['records']]
    source_rows=[row for group in packet['groups'] for row in group['records']]
    assert len(combined)==len(source_rows)==304
    assert [r['id'] for r in combined]==[r['id'] for r in source_rows]
    assert all(all(r[key]==source[key] for key in source) for r,source in zip(combined,source_rows,strict=True))
    save(SOURCE.with_name('all304_clean_meanings_before_English.json'),dict(
        records=combined,meanings=304,source_packet=str(SOURCE),source_packet_sha256=sha(SOURCE.read_bytes()),
        parts={str(path):sha(path.read_bytes()) for path in parts},
        earlier_English_unconsulted=True,nine_complete_spoken_exchanges_andone_control_only_block=True,
        typed_choices_identity_terminology_opaque_actions_andlinked_context_pending=True,
        no_localization_orfive_gate_approval_orcompletion_credit=True,new_credit=0))
    print('All304 clean-first speech meanings saved;typed choices/context/names/current comparison remain pending.')
