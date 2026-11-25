"""Preserve complete source meanings for literary leads,letters andlegends."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/analysis/Hodram_B211_B230_clean_20261104')
DECISIONS = {
    216: dict(context='A sociable man asks about Romance of the Three Kingdoms andfavorite commanders. A matching preference for Zhao Yun leads to a rumored spear on a nearby peninsula;other choices receive individual comments.', meanings=[
        'He greets the group andasks whether they know Romance of the Three Kingdoms.',
        'On the unfamiliar branch,he recommends reading it because it is entertaining.',
        'On the familiar branch,he is pleased andasks their favorite military commander.',
        'He exclaims that their choice is the same as his;they should get along well.',
        'He enthusiastically recalls the scene at Changban Bridge in which Zhao Yun holds A Dou to his chest andrides alone through Cao Cao’s army.',
        'He has heard a rumor that the legendary spear said to have been used by Zhao Yun is on a peninsula in this region.',
        'He too wanted it andsearched extensively,but ultimately could not find it;he thinks this group might succeed.',
        'For Guan Yu: asks whether they like the Lord of the Beautiful Beard;not his own favorite,but a valiant man with both wisdom andcourage.',
        'For Zhuge Kongming: approves the strategist choice;his memorial before departure is moving enough for tears;he is about the speaker’s second favorite.',
    ], notes=['おじさん is self-reference by an older/middle-aged man,not a claim to be the player’s uncle. Keep the novel discussion as his enthusiasm;do not silently replace the source’s Changban Bridge account with a different literary/historical episode.']),
    217: dict(context='An old man asks to inspect an object andrecognizes a sign from a family tradition. He recounts Kublai Khan’s prophecy andentrusts a sword to the admiral,who modestly rejects the exalted identification.', meanings=[
        'The old man politely addresses the person over there.',
        'The admiral asks whether he means him.',
        'The old man asks to be shown that object.',
        'The admiral asks which object.',
        'The old man indicates that one.',
        'After examining it,he says it is unmistakable andmatches the handed-down account.',
        'The admiral is puzzled.',
        'More than three hundred years ago,the mainland was ruled by the great emperor Kublai Khan.',
        'Even that great emperor eventually reached the time of his death.',
        'He told his retainer that two hundred years later,a conqueror of the oceans would come to this land;the quotation continues.',
        'The foretold sea king would command many foreigners andcarry a golden seal from a land the emperor had not managed to rule. The emperor ordered that his sword be given to that hero.',
        'The old man’s clan descends from that retainer;they have awaited the sea king.',
        'Now at last the admiral has appeared;the old man solemnly welcomes the conqueror of the oceans he awaited.',
        'The admiral incredulously asks whether he means him,chuckles,andasks the old man to spare him;he is not such a grand figure.',
        'The old man insists his eyes do not deceive him;this person is indeed the sea king.',
        'He instructs the admiral to search south of the Shandong Peninsula,where the emperor’s great sword should be found.',
        'He entrusts that great sword to the admiral andtakes his leave.',
    ], notes=['Preserve both the more-than300-year introduction andthe quoted200-year prophecy;do not harmonize their chronology. The golden seal’s land is not named here. 爺さん addresses an old man without establishing kinship. Prophetic titles are the old man’s claim,not a new rank awarded by narration.']),
    218: dict(context='A letter from Jenas on a road to Rome relays a Judas-associated sword rumor. He distinguishes the object from its owner’s guilt;the admiral notes his pragmatism,anddevout Manuel conditionally leaves the decision to the admiral.', meanings=[
        'The letter addresses the admiral;the writer is sending it from a road leading to Rome.',
        'Along this road,he inevitably hears accounts of missionaries overcoming many persecutions long ago in their efforts to spread the faith.',
        'He is not interested in religion,but has heard one intriguing story.',
        'A sword once owned by Judas,one of Jesus’s twelve disciples,apparently still lies in a place associated with him.',
        'Because Judas betrayed Jesus,people find the sword unsettling simply because it was his possession,andnobody wants to acquire it.',
        'He has heard it is exceptionally sharp andfine. The sword itself committed no sin,andhe thinks it would be worth seeking.',
        'Devout Manuel would likely dislike hearing this story,however.',
        'He will write again if anything else arises. Signed ジェナス・パサー.',
        'The admiral considers a traitor’s sword;disregarding provenance if the item is good is characteristic of practical Jenas.',
        'Manuel says he is not absolutely opposed;Judas repented in the end,after all. He leaves it to the admiral.',
    ], notes=['Preserve the characters’ religious language andviewpoints respectfully,including Manuel’s repentance statement. Do not add holy/demonic powers,an exact burial site ora verified historical provenance. The author’s lack of interest is not contempt for believers. Source-native dynamic letter announcements are separately reviewed.']),
    219: dict(context='A mysterious woman searches for the king andthe sword’s rightful hero while a vendor angrily tries to dismiss her. She identifies herself as Vivienne andsends the admiral to Avalon for Excalibur;a companion suggests a tavern lead.', meanings=[
        'The woman asks where the king is.',
        'The vendor angrily recognizes her again,says she is interfering with business,andorders her away.',
        'She again asks for the king,andwhere the hero who will own the sword may be.',
        'The admiral asks what is happening andwho she is.',
        'She identifies herself as ヴィヴィアン,the one who once made King Arthur’s holy sword.',
        'The admiral reacts incredulously to the mention of King Arthur.',
        'She says the king has fallen asleep,but the holy sword continues seeking a hero.',
        'She addresses a hero andcommands a search for the holy sword Excalibur;at Avalon,where the king sleeps,the sword seeks this person.',
        'The admiral has never heard of Avalon.',
        'A companion suggests someone at the tavern might know that place.',
    ], notes=['Treat Vivienne’s identity andcreation of the sword as her stated claim. The king sleeps;do not replace this with an explicit death. The vendor’s hostility contrasts with her solemn,otherworldly delivery.']),
    220: dict(context='The admiral asks a tavern host about Avalon. Tired of repeated questions,the host distrusts the self-proclaimed witch andArthur story,butprovides a vague nearby-west location.', meanings=[
        'The admiral familiarly addresses the tavern host andasks whether he knows Avalon.',
        'The host complains that this is happening again;asks whether the admiral too believes the nonsense of the woman who calls herself a witch.',
        'Avalon was reportedly somewhere just west of here.',
        'He calls the Arthur story a fairy tale. He has been asked this repeatedly,butnever heard that anyone found it.',
    ], notes=['親父 is familiar address to the host,not Father/Dad. Preserve the host’s skepticism andthe uncertainty of the location,without deciding whether the magic is real.']),
}

if __name__ == '__main__':
    path = ROOT / 'B216_B220_clean_meanings_before_English.json'; decisions = ROOT / 'B216_B220_source_meaning_decisions.json'
    assert not path.exists() and not decisions.exists()
    packet_path = ROOT / 'clean_source_packet.json'; packet = load(packet_path)
    save(decisions, dict(blocks=DECISIONS, source_only_meanings_not_localized_drafts=True))
    rows = []
    for group in packet['groups']:
        if group['block'] not in DECISIONS: continue
        d = DECISIONS[group['block']]; assert len(group['records']) == len(d['meanings'])
        for r, meaning in zip(group['records'], d['meanings'], strict=True):
            assert bytes.fromhex(r['source_hex'])[1:].decode('cp932') == r['source_Japanese']
            rows.append(dict(**r, source_meaning=meaning, exchange_context=d['context'], native_identity_terms_localization_andformatting_pending=True,new_credit=0))
    assert len(rows) == 50
    save(path, dict(records=rows, source_meanings=50, complete_exchanges=list(DECISIONS), source_fidelity_notes={k:v['notes'] for k,v in DECISIONS.items()},
        no_current_ROM_English_intake_for_this_batch=True,source_only_not_localized_English=True,no_all_historical_exposure_claim=True,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [packet_path,decisions,Path(__file__)]}))
    print('50 clean meanings saved across five whole exchanges;no current-English intake orcompletion credit.')
