"""Read five complete clean exchanges; preserve meanings before current English intake."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/analysis/Hodram_B211_B230_clean_20261104')
DECISIONS = {
    211: dict(context='A food-loving companion requests the Minotaur axe. The admiral offers only to look someday,then expressly declines to promise ownership;the eager companion celebrates prematurely.', meanings=[
        'Drawn-out familiar address to the admiral: there is a weapon the speaker wants.',
        'The admiral asks what the companion said/wants.',
        'The companion wants a weapon because he too wants to get stronger.',
        'The admiral teases that the companion wants something besides food;asks the weapon name.',
        'The companion names the Axe of the Minotaur.',
        'The admiral supposes it must be a very large weapon,andasks where it is.',
        'The companion does not know;all he knows is that the Minotaur reportedly lived on this island long ago.',
        'The admiral says they will try looking for it sometime.',
        'The companion cheers.',
        'The admiral stresses that he said sometime.',
        'The companion cheers anyway.',
        'The admiral adds that he has not decided to give it to the companion either.',
        'The companion protests in disappointment.',
    ], notes=['The island is mentioned without a name. Neither a location nor ownership is promised. The Minotaur report remains hearsay.']),
    212: dict(context='An old man stops a strong-looking woman;her bearing reminds him of a formidable female pirate. He offers an intriguing but imprecise Caribbean sword lead;her attraction increases after the exchange.', meanings=[
        'The old man asks for the attention of the person over there.',
        'The woman asks whether he means her.',
        'He confirms he means her.',
        'She asks what he wants.',
        'Seeing her reminds him of a strong female pirate from long ago;he emphasizes how strong that pirate was.',
        'She asks whether she resembles the pirate that much,perhaps in facial features.',
        'He says not her face,but her air/bearing;perhaps because she too looks strong.',
        'She asks whether she looks strong,then says she must become stronger in that pirate’s example.',
        'He asks if she wants to become stronger,andproposes seeking the treasured sword the pirate possessed.',
        'She repeats the female pirate’s treasured sword questioningly.',
        'He confirms it is a sword the pirate is said to have used;he does not know how valuable it is.',
        'She is intrigued andasks where the sword is.',
        'He says the Caribbean Sea.',
        'She repeats the Caribbean Sea thoughtfully.',
        'There was reportedly a major naval battle in the Caribbean in which the pirate participated;the sword was reportedly lost during that battle.',
        'She asks what else.',
        'He says that is all.',
        'She protests that if that is all,how is she supposed to find it?',
        'He cannot answer that,but feels she could find it.',
        'She says she will remember the lead.',
        'He expresses confidence she will find it andencourages her.',
        'She thanks him.',
        'Her internal thought: a female pirate’s treasured sword lost in the Caribbean;she would like to see it.',
        'System notice: Cristina’s Charm increases by one.',
    ], notes=['Resemblance is bearing/strength,explicitly not facial resemblance. No kinship or named historical pirate is established. Exact sword label requires clean catalogue binding.']),
    213: dict(context='A delivered letter from Yukihisa reports a rumored Muramasa blade hidden in East Asia. Dynamic companion styles announce/comment on the letter;Jam has a separate comment andthe admiral finds the lead interesting.', meanings=[
        'Formal written report: the writer has heard rumors of the legendary cursed blade Muramasa. It is a fine blade held to be a bane of Tokugawa,the leader of Japan,andis being eradicated from the world.',
        'A clan bearing a grudge against Tokugawa has apparently hidden one such blade somewhere in East Asia;the writer sends this preliminary report.',
        'The writer is certain this is the item he has sought for many years. Signed 白樹玄丞行尚,withユキヒサ reading supplied in parentheses.',
        'Jam remarks that the writing is rather difficult/pompous;that is like Yukihisa.',
        'After a thoughtful pause,the admiral says he sees,andfinds this interesting.',
    ], notes=['The letter deliberately uses formal archaic written language. Retain reported beliefs/rumors;do not turn them into independently verified history orinvent a hereditary curse mechanism. Source says one among such blades. Opening/comment personality alternatives are separately inventoried 4100 objects.']),
    214: dict(context='A companion enthusiastically reports a lord’s ominous red-bladed sword,sealed away unused. The admiral is intrigued andpartly sympathetic to the frightened lord;the companion suggests looking if an opportunity arises.', meanings=[
        'The companion urgently asks the admiral to listen: he obtained useful news.',
        'A lord in this region reportedly acquired a sword with a marvelous cutting edge.',
        'The admiral invites him to continue.',
        'The blade reportedly has a faint red color,as though it had drunk the blood of many people.',
        'The admiral finds that unusual.',
        'The lord reportedly found it unsettling andsealed it away somewhere without using it even once;the companion mocks him as very timid.',
        'The admiral says that nevertheless it is a waste.',
        'The companion calls the lord an astonishing fool,andasks what he intended to use a sword for.',
        'The admiral says he can understand the feeling somewhat,butasks what became of the sword.',
        'The companion did not learn the hiding place;he suggests they look for it if they get an opportunity.',
    ], notes=['A bloodstained appearance is hearsay/imagery,not proof the blade has consumed blood ormagical powers. The lord is not named.']),
    215: dict(context='Cristina admires a square andspeaks playfully to a pair of swans. They depart carrying a long shining object toward the Amsterdam area;she tells the admiral andsuggests investigating.', meanings=[
        'Cristina admires the attractive square,then notices something in the little pond andtries to identify it.',
        'A swan cries out.',
        'She recognizes a pair of white swans,is surprised they come even here,andasks whether they too are traveling.',
        'Swan calls: a loud cry,paired soft clucking calls,andfurther cries.',
        'She chuckles that they get along well andsays she envies them.',
        'Sound of fluttering/flapping wings.',
        'She exclaims,wonders where they are going,andnotices they are carrying something.',
        'She considers the direction in which they flew.',
        'The admiral finds Cristina here.',
        'She addresses Admiral FI andsays there was a pair of swans.',
        'The admiral says it is unusual for swans to come this far into town.',
        'She says they were carrying something long andshining,andseem to have flown near Amsterdam;asks whether they should go look.',
    ], notes=['The pair’s closeness supports her wistful envy,not a claim about her own partner ormarriage. Do not identify the shining object before the source does. Preserve FI substitution.']),
}

if __name__ == '__main__':
    path = ROOT / 'B211_B215_clean_meanings_before_English.json'
    decisions = ROOT / 'B211_B215_source_meaning_decisions.json'
    assert not path.exists() and not decisions.exists()
    packet_path = ROOT / 'clean_source_packet.json'; packet = load(packet_path)
    save(decisions, dict(blocks=DECISIONS, source_only_meanings_not_localized_drafts=True))
    rows = []
    for group in packet['groups']:
        if group['block'] not in DECISIONS: continue
        d = DECISIONS[group['block']]
        assert len(group['records']) == len(d['meanings'])
        for r, meaning in zip(group['records'], d['meanings'], strict=True):
            assert bytes.fromhex(r['source_hex'])[1:].decode('cp932') == r['source_Japanese']
            rows.append(dict(**r, source_meaning=meaning, exchange_context=d['context'],
                native_identity_terms_localization_andformatting_pending=True, new_credit=0))
    assert len(rows) == 64
    save(path, dict(records=rows, source_meanings=64, complete_exchanges=list(DECISIONS),
        source_fidelity_notes={k:v['notes'] for k,v in DECISIONS.items()}, no_current_ROM_English_intake_for_this_batch=True,
        source_only_not_localized_English=True, no_all_historical_exposure_claim=True, new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [packet_path, decisions, Path(__file__)]}))
    print('64 clean meanings saved across five whole exchanges;no current-English intake orcompletion credit.')
