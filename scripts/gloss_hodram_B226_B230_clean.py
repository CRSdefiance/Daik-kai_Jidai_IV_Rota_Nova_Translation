"""Preserve source meanings for armor leads,romantic banter andhero stories."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/analysis/Hodram_B211_B230_clean_20261104')
DECISIONS = {
    226: dict(context='Ian’s letter summarizes an antique book about Timur andstolen armor lost in the desert. The admiral is surprised by his interest;Cesare suggests a Russian historical connection.', meanings=[
        'Ian recently found an interesting book at an antique shop.',
        'It concerns Timur,who about two hundred years ago carried on the declining Mongol imperial line andbuilt a great empire from Central Asia to Western Asia.',
        'According to the book,he wore extraordinarily sturdy mail that deflected enemy arrows andchipped the edges of swords andspears in battle.',
        'It was buried in his tomb at his death,but several decades later thieves stole it with other grave goods.',
        'To evade pursuers,the thieves fled into the scorching desert,but finally collapsed anddied just short of reaching a place with a view of the sea.',
        'This apparently remained unknown for a long time,andthe mail has still not been found.',
        'If the admiral is interested,Ian suggests investigating. Signed Ian Dukov.',
        'The admiral expresses surprise that Ian is interested in Asian history.',
        'Cesare says the Mongol Empire once ruled the Russian people andwas their longstanding enemy,so Ian’s interest probably arose naturally.',
        'The admiral acknowledges this thoughtfully.',
    ], notes=['Preserve the book’s claims andCesare’s inference without silently correcting history oradding ancestry to Ian’s biography. The desert,the sea andthe tomb’s exact location remain unnamed. The dynamic letter announcements are separate 4100 objects.']),
    227: dict(context='Julian’s flattery of Safia’s eyes turns into a Medusa comparison. She objects to being likened to a monster;he recasts it as romantic captivity. She parries,butprivately admits his strange image made her heart race.', meanings=[
        'Julian greets Safia andcalls her eyes as mysterious as ever.',
        'She recognizes andwelcomes him.',
        'He pauses silently.',
        'She asks what is wrong andwhether something is on her face.',
        'He says looking into her eyes nearly drew him in;wonders whether this is what being turned to stone feels like.',
        'She asks what he means.',
        'He has been thinking about Medusa’s Shield,said to be in the Tasman Sea;her eyes brought it back to mind.',
        'She identifies Medusa as the snake-haired monster,andasks whether he means she too is frightening andugly.',
        'He protests: even without revealing the hair she keeps covered,her beautiful eyes alone could capture him.',
        'She chides him for always joking.',
        'He imagines her turning him to stone,then living forever near her in the moonlight;he calls it romantic.',
        'She says she will not look after him even if he turns to stone.',
        'He calls her cold butfinds that aloofness attractive;then says it is time to leave andbids farewell.',
        'She says goodbye.',
        'She calls it a strange comparison,butprivately admits that it made her heart race a little;the musical note gives a pleased/light ending.',
    ], notes=['The Medusa transformation is flirtatious imagination,not a confirmed power of Safia. Covered hair is in the source;do not invent marriage,veil rules orreligious biography. The geographic lead is the Tasman Sea.']),
    228: dict(context='A boy plays Charles Martel while another participant pretends to surrender. Gerhard explains the local hero andhis view of a historical turning point,thenflatters the admiral’s own achievements.', meanings=[
        'In his hero role,the boy threatens an infidel andboasts that he,Charles Martel,will defeat him.',
        'The other participant cries that it hurts,surrenders,andstammers a call to retreat.',
        'The admiral asks what they are doing.',
        'Gerhard says they are playing heroes;children everywhere admire their own country’s heroes.',
        'The admiral concludes the local hero is Charles,butcannot remember the rest of the name.',
        'Gerhard supplies Charles Martel,a figure from more than eight hundred years ago.',
        'He says Martel decisively repelled Muslim forces advancing north after invading the Iberian Peninsula,between nearby Tours andPoitiers.',
        'The admiral says winning a battle is admirable,butbeing called a hero for that alone seems exaggerated.',
        'Gerhard says the significance of the victory is what matters.',
        'Gerhard asserts that had Martel lost,all Europe would have become Islamic andhistory would have changed greatly.',
        'The admiral reflects that this person could have changed history;the children probably idolize him because they think he protected Europe.',
        'Gerhard says the admiral’s own achievements are by no means inferior to Charles Martel’s.',
        'He already looks forward to how posterity will speak of the admiral’s name.',
    ], notes=['Keep the boy’s hostile religious term within the playacting andGerhard’s counterfactual as his asserted historical interpretation. Do not turn either into narrator endorsement,add modern political commentary orerase the source’s religious context.']),
    229: dict(context='Manuel andthe admiral meet while gathering information in the square. Attila prompts a reflection on the impermanence of dominance,then a rumored armor lead tentatively toward northern Europe.', meanings=[
        'Manuel politely greets the admiral.',
        'The admiral recognizes Manuel.',
        'Manuel asks whether he is inspecting trends,andremarks on how busy he always is.',
        'The admiral says it is not only that;it is also an occasional break.',
        'Manuel acknowledges this.',
        'Gerhard asks whether Manuel has some business in the square.',
        'Manuel says he is doing the same as the admiral: gathering information while taking a stroll.',
        'He asks whether the admiral knows Attila,king of the Huns.',
        'The admiral has heard the name butinvites an explanation.',
        'Manuel describes the Huns as Asian nomadic horsemen;Attila reportedly threatened even both the Eastern andWestern Roman Empires.',
        'Gerhard marvels that someone could put Rome under pressure,andconcludes he must have been formidable.',
        'Manuel reflects that however mighty an empire,some stronger foe eventually appears;supremacy does not last forever.',
        'The admiral finds that pointed: does Manuel mean they too must remain vigilant?',
        'Manuel agrees;everything depends on effort.',
        'The admiral agrees,thenasks what brought up Attila in the first place.',
        'Manuel just heard a story here about armor associated with Attila,butit remains no more than a rumor.',
        'The admiral asks about the armor.',
        'After Attila’s death,someone reportedly carried it away to a land in the northwest.',
        'Gerhard reflects on the king’s armor taken northwest;someone who threatened Rome must have been greatly feared.',
        'Manuel suggests that northwest from here might mean the region of northern Europe.',
    ], notes=['The northwestern destination andnorthern-Europe identification remain rumor andtentative inference,not a new exact map coordinate. The reflection on power is a pointed friendly exchange,not a threat of betrayal.']),
    230: dict(context='Yi-Fa trains late andexplains the resolve needed against a blade. A rumor of extraordinary martial clothing tempts her,butshe catches herself relying on gear andreturns to practice,recalling her teacher’s lesson.', meanings=[
        'Training exertion cries.',
        'The admiral notes that she is training this late,andwishes the marines would follow her example.',
        'She says facing an opponent holding a sword takes considerable courage.',
        'If fear of the blade makes you step in halfheartedly,you can instead be badly injured;mental strength that does not fear things is important.',
        'She recalls hearing of martial-arts clothing so sturdy that a striking sword’s edge chips;asks whether he knows of it.',
        'The admiral reacts with interest to a sword chipping.',
        'With something that useful,she thinks she could fight more freely/without holding back.',
        'She catches herself: her teacher would scold her for relying on equipment,saying to strengthen herself first.',
        'She returns to training with further exertion cries.',
    ], notes=['The garment’s durability remains reported;do not assert invulnerability. お師匠様 is an actual martial teacher relationship here,not a familial honorific orfeudal rank.']),
}

if __name__ == '__main__':
    path=ROOT/'B226_B230_clean_meanings_before_English.json'; decisions=ROOT/'B226_B230_source_meaning_decisions.json'
    assert not path.exists() and not decisions.exists()
    packet_path=ROOT/'clean_source_packet.json';packet=load(packet_path)
    save(decisions,dict(blocks=DECISIONS,source_only_meanings_not_localized_drafts=True));rows=[]
    for group in packet['groups']:
        if group['block'] not in DECISIONS:continue
        d=DECISIONS[group['block']];assert len(group['records'])==len(d['meanings'])
        for r,meaning in zip(group['records'],d['meanings'],strict=True):
            assert bytes.fromhex(r['source_hex'])[1:].decode('cp932')==r['source_Japanese']
            rows.append(dict(**r,source_meaning=meaning,exchange_context=d['context'],native_identity_terms_localization_andformatting_pending=True,new_credit=0))
    assert len(rows)==67
    save(path,dict(records=rows,source_meanings=67,complete_exchanges=list(DECISIONS),source_fidelity_notes={k:v['notes'] for k,v in DECISIONS.items()},
        no_current_ROM_English_intake_for_this_batch=True,source_only_not_localized_English=True,no_all_historical_exposure_claim=True,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [packet_path,decisions,Path(__file__)]}))
    print('67 clean meanings saved across five whole exchanges;no current-English intake orcompletion credit.')
