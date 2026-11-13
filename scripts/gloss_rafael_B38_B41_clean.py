"""Save complete clean rescue, Dutch signal, rematch and ruins guidance meanings."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Rafael_early_story_B36_B41_B51_B60_clean_20261104')
DECISIONS={
38:dict(context='A Spanish commander confronts Rafael about alleged cooperation with pirates. Claudio blusters despite the fleet’s weakness. Another fleet approaches: Hayreddin intervenes, mocks Pedro and orders Rafael away. Rafael leaves at full speed, while the Spanish commander withdraws with a threat. Janus and Julio inserts are conditional.',notes=[
    'The initial cooperation claim is a rumor voiced by an adversary, not proof of a formal alliance.',
    'Hayreddin uses Pedro and is called Barbarossa. Bind the actor’s native full name instead of inventing another Spanish commander.',
    'Keep the separate orders: Hayreddin tells Rafael to leave; the Spaniard then announces his own withdrawal.'],meanings=[
    'The lookout reports a Spanish fleet to the admiral.',
    'The Spanish commander insults the Portuguese youths and asks whether the rumor that they have joined with pirates against Spain is true.',
    'Rafael is startled and asks where he heard that.',
    'The commander demands an answer, threatening that hundreds of cannon could fire together on their weak fleet depending on the reply.',
    'Claudio grits his teeth and says this does not look like a situation they can bluff their way out of.',
    'Rafael worries that their current strength may not be enough to win.',
    'Claudio defiantly invites the enemy to come at them.',
    'Julio observes that their actual strength does not live up to that bravado.',
    'The lookout reports sighting another fleet.',
    'Rafael fears that this is the end for them.',
    'The lookout reacts in surprise.',
    'Janus reacts in surprise.',
    'Hayreddin addresses Pedro, mocking the idea that he would need children’s help to deal with someone like him.',
    'Rafael recognizes Hayreddin.',
    'The Spaniard reacts angrily and recognizes Barbarossa.',
    'Hayreddin offers to give him an opponent to play with if he has so much time on his hands.',
    'The Spaniard asks whether the Algiers pirates mean to make an enemy of the Spanish navy.',
    'Hayreddin says their identity makes no difference: foolish ships passing through these waters are merely prey for his men.',
    'The Spaniard reacts with irritation.',
    'Hayreddin dismisses Rafael as being in the way and tells him to leave.',
    'Rafael thanks him, then orders everyone to make full speed and leave these waters.',
    'Hayreddin turns back to the confrontation and suggests they begin.',
    'The Spanish commander angrily says he will withdraw this time, but will make Barbarossa regret making an enemy of Spain.',
]),
39:dict(context='A vessel that appears to be a Dutch merchantman signals Rafael. A sailor or Janus reads the signal, depending on companion state. Claudio eagerly assumes a fight; Arcadius needles him in a conditional exchange. The signal tells them to dock at Amsterdam. Arcadius recommends caution rather than risking an ambush; Rafael appreciates Claudio’s strength but chooses to call at port.',notes=[
    'The ship’s Dutch merchant identity is initially a question, not independent certainty.',
    'Arcadius’s advice is a suspicion and risk assessment, not proof that an ambush has been set.',
    'Read the sailor and Janus alternatives as equivalent conditional functions; do not concatenate them into a repeated live signal exchange.'],meanings=[
    'A sailor points out a distant ship that may be a Dutch merchantman and says it appears to be signaling something.',
    'Rafael wonders what the message is and asks if the sailor can understand it.',
    'The sailor answers affirmatively and says he will decode the signal.',
    'In the companion alternative, Janus addresses Admiral FI and points out a possible Dutch merchantman that seems to be signaling them.',
    'Rafael asks Janus whether he understands it.',
    'Janus considers it and says he will try to decode the signal.',
    'Claudio eagerly wonders whether this means a fight and says he is itching for action.',
    'Arcadius mutters that Claudio is a barbarian.',
    'Claudio asks whether Arcadius said something.',
    'Arcadius lightly asks whether Claudio heard that.',
    'Rafael checks Clau: they are not traveling the world to pick fights with everyone.',
    'Claudio answers with exaggerated deference to Admiral FI and says he knows.',
    'Rafael returns to the signal and asks what it says.',
    'The sailor reports that the message tells them to dock at Amsterdam.',
    'In the Janus alternative, he says it appears to be a signal telling them to dock at Amsterdam, and asks what they will do.',
    'Rafael wonders what to make of it.',
    'The sailor asks whether they should at least call at Amsterdam once.',
    'Arcadius finds it suspicious, but thinks complying is preferable to risking an ambush at sea.',
    'Rafael privately notices, with surprise, that Arcadius also has this sort of strategic insight.',
    'Claudio argues that the other fleet is not especially large, so they should ignore it and force their way through.',
    'Rafael says he will rely on Clau in situations that require that, but hesitates.',
    'Rafael decides they should be cautious here and call at port.',
]),
40:dict(context='In a later encounter, Hayreddin acknowledges Rafael’s increased strength and his intention to seek Mediterranean supremacy. He warns about the Ottoman Pasha force and directs Rafael to the Algiers dock before promising no mercy in their next decisive battle. His assistance is indirect; Rafael takes up the challenge.',notes=[
    'This is a later rematch lead, not established first-voyage chronology. Preserve it in scope without claiming early-game activation.',
    'Do not invent the nature of any dock gift or assistance; this exchange only directs Rafael there.',
    'Bind パシャ軍 to the registered faction/name terminology instead of confusing it with companion Janus Pasar.'],meanings=[
    'Hayreddin remarks that Rafael seems to have become stronger.',
    'Rafael is startled to see Hayreddin.',
    'Hayreddin says Rafael has exceeded his expectations and appears finally ready to begin seeking control of the Mediterranean.',
    'Rafael says that is his intention, although he does not yet know how it will turn out.',
    'Hayreddin reminds him that the Ottoman Pasha force is powerful and asks whether he understands that.',
    'Rafael says he does.',
    'Hayreddin responds by telling him to stop at the dock in Algiers.',
    'Rafael reacts with surprise.',
    'Hayreddin warns that he will show no mercy when they next meet on the decisive battlefield.',
    'Rafael stammers a defiant acceptance of the challenge.',
    'Hayreddin laughs and approves of the determination on Rafael’s face.',
]),
41:dict(context='The companions ask Hans about finding the African 証. His explanation becomes guidance about power, regional ruins, cultural centers and earning the locals’ trust. Each companion interprets strength differently; Hans allows that all may matter. He explicitly presents the ruins theory as an inference. Claudio jokes about charity; Hans answers that a would-be hegemon needs the stature to win trust.',notes=[
    'Keep 証 and 覇者 as source concepts pending exact registered item/terminology binding. Do not silently invent a certificate, deity, rank or modern political program.',
    'Hans’s idea about ruins is a hypothesis, not an omniscient guarantee. Religious/cultural symbolism and outsiders’ need for trust are substantive context.',
    'Source 水夫 are sailors and 航海士 are navigators; do not merge crew categories. Here companionship, not family, motivates the exchange.',
    'The instruction about helping locals includes requests, people in difficulty, and confronting abusive merchants or military men. Do not omit those concrete examples.'],meanings=[
    'Claudio asks Hans whether it is about time they found a clue to the 証 said to be in Africa.',
    'Hans says that being impatient will not help.',
    'Rafael asks how they should go about looking for such clues.',
    'Hans says they must first gain strength worthy of a 覇者; without it the 証 will never reveal itself to them.',
    'Claudio asks whether strength means having a huge fleet.',
    'Rafael wonders whether it means becoming a fully capable navigator or voyager.',
    'Janus suggests that strength might instead mean financial resources.',
    'Julio wonders whether it means having a large trading sphere.',
    'Hans observes that everyone interprets it differently and suggests it might mean all of those things.',
    'Rafael reacts that this sounds dauntingly far off.',
    'Hans adds that possessing strength alone is not enough.',
    'Rafael asks in surprise whether there is still more to it.',
    'Hans qualifies what follows as his own inference.',
    'He thinks the mysteries of the 証 are likely sealed within ruins around the world.',
    'Rafael asks about ruins.',
    'Hans confirms that he means ruins.',
    'Rafael asks where those ruins are.',
    'Hans thinks they would be within or near major cities representing the different cultural regions.',
    'Claudio complains that this is still not enough information to know how to search.',
    'Hans says some residents should know, and that first they must earn the trust of the people of the city.',
    'Rafael asks about earning their trust.',
    'Hans explains that ruins and old churches symbolize the locals’ religion and culture, so they will not readily share their locations with outsiders like the voyagers.',
    'Hans gives examples: listen to townspeople’s requests, help those in difficulty, and chastise corrupt merchants or military men who are making people suffer.',
    'Claudio remarks that this sounds like charity work.',
    'Hans says that in any case, someone qualified to be a 覇者 needs enough character and capacity to earn the trust of many people.',
    'Rafael sighs that becoming a 覇者 is difficult.',
    'Hans chuckles that naturally it is, since no one has yet accomplished it.',
]),
}

if __name__=='__main__':
    output=ROOT/'B38_B41_83_clean_meanings_v1.json'
    assert not output.exists()
    source=ROOT/'clean_source_packet.json'
    packet=load(source)
    rows=[]
    for group in packet['groups']:
        if group['block'] not in DECISIONS:continue
        review=DECISIONS[group['block']]
        assert len(group['records'])==len(review['meanings'])
        for row,meaning in zip(group['records'],review['meanings'],strict=True):
            assert bytes.fromhex(row['source_hex'])[1:].decode('cp932')==row['source_Japanese']
            rows.append(dict(**row,source_meaning=meaning,exchange_context=review['context'],
                source_macros_complete={m:row['source_Japanese'].count(m) for m in ['FI','FA','FO','FU']},
                source_context_notes=review['notes'],native_identity_andEnglish_localization_andformatting_pending=True,new_credit=0))
    assert len(rows)==83
    save(output,dict(source=str(source),source_sha256=sha(source.read_bytes()),blocks=[38,39,40,41],records=rows,
        source_meanings_saved=83,all_complete_exchanges_reread=True,current_orhistorical_English_dialogue_not_consulted=True,
        chronological_priority_not_inferred_from_block_numbers=True,no_new_completion_credit=True,new_credit=0,guide_photos=False,
        producer_sha256=sha(Path(__file__).read_bytes())))
    print('83 clean meanings saved;later Hayreddin rematch andsource 証 terminology explicitly distinguished.')
