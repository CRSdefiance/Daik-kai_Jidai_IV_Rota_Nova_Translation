"""Read whole exchanges for mythic weapons,flirtation andcompeting historical views."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/analysis/Hodram_B211_B230_clean_20261104')
DECISIONS = {
    221: dict(context='Ian reports a spear associated with Ares. His evasive location answer gives way to unexpectedly personal enthusiasm for mythology;the admiral listens with surprise.', meanings=[
        'Ian has heard information in town about a splendid weapon.',
        'The admiral asks its name.',
        'It is called the Holy Spear of Ares because legend says Ares,one of the twelve Olympians,possessed it.',
        'The admiral finds a spear of the war god Ares interesting and asks whether its location is known.',
        'Rumor suggests armor bearing another Olympian’s name might lie nearby together with it.',
        'The admiral points out that this does not answer his question.',
        'Judging by the townspeople’s way of speaking,Ian infers that it may be in this region;he very much wants to find it.',
        'The admiral privately notes with surprise that Ian is interested.',
        'Ian asks why the admiral has an odd expression;is it surprising that he is interested in legends?',
        'The admiral admits it is.',
        'Ian acknowledges that may be so,but says mysterious tales move him: the gods of myth once ranged across this land;the thought continues.',
        'Merely imagining weapons they may have used surviving in this world sends his thoughts back to antiquity.',
        'After a pause,the admiral acknowledges this.',
    ], notes=['Retain the movement from seemingly practical information to reflective wonder. Weapons possibly used by gods are Ian’s imaginative interest,not confirmed divine provenance. The accompanying armor’s Olympian is not named here.']),
    222: dict(context='A control-only block has no spoken or compound text.',meanings=[],notes=['One source command;no omitted prose andno dialogue completion credit for this block alone.']),
    223: dict(context='Julian flatters Lucia,compares her to a beautiful but domineering legendary Chinese empress,andromanticizes an armored gown. Lucia prefers jewelry;he changes the subject andleaves before she can ask him for a gift.', meanings=[
        'Julian warmly greets Lucia,asks how she has been,and says he comes here to see her noble,beautiful eyes.',
        'Lucia welcomes him and says his flattering tongue has not changed.',
        'He pauses thoughtfully or notices something.',
        'She asks what is wrong and whether something is on her face.',
        'He muses that the legendary empress may have been someone like Lucia.',
        'She asks what he means.',
        'He apologizes for the abrupt remark;he just heard of armor called the Empress’s Gown and it prompted the thought.',
        'She asks about the Empress’s Gown.',
        'It was reportedly worn by a beautiful Chinese empress;after ruling with extreme tyranny,she apparently met a tragic end.',
        'He imagines a woman so beautiful it was frightening,able to pierce a man’s heart with one glance;asks whether that is just like Lucia.',
        'She points out that extreme tyranny means being selfish and overbearing;asks whether she is really so spiteful.',
        'He fondly calls her silly and says a little selfishness makes a woman cute—just about as much as she has.',
        'He finds a gown made to protect a beautiful woman romantic and asks whether she agrees.',
        'She questions how a gown is romantic;she would be more interested in the woman’s rings or necklaces.',
        'He asks whether she means their prices,exclaims that women are practical,and promptly says it is time to leave.',
        'She bids him farewell.',
        'She complains that he always runs away when she is about to ask him for something.',
    ], notes=['No particular empress is named. Piercing a heart is flirtatious imagery,not a supernatural power. Her closing complaint reveals the gift-request dodge;do not reduce the ending to mere disappointment at his departure.']),
    224: dict(context='A square shopkeeper challenges a European account of the Crusades. Al Ferid backs his criticism andpraises Saladin’s humane conduct,then supplies a missing-armor lead. Both knowledge-menu branches converge on the debate.', meanings=[
        'The shopkeeper stops the passerby: surely he will not simply pass through this town’s square without stopping.',
        'The admiral asks whether there is something in this town.',
        'The shopkeeper asks whether he knows the Crusades.',
        'On the familiar branch,he scoffs: presumably as an army that valued chivalry and fought to reclaim the Holy Land?',
        'On the unfamiliar branch,he scoffs that Europe apparently calls them an army that valued chivalry and fought to reclaim the Holy Land.',
        'He calls that all a convenient lie;the people of this town know the truth of what those Crusaders were like.',
        'The admiral asks about this truth.',
        'Al Ferid says he has heard some of it too: their real goal was this region’s wealth,and they reportedly allowed plunder and slaughter along the way.',
        'The shopkeeper cannot tolerate history being conveniently rewritten;the real hero was their own Saladin,not the Crusaders.',
        'The admiral asks who Saladin was.',
        'Al Ferid calls him a great figure of Islamic history;his importance extends beyond repelling the Crusaders.',
        'He praises Saladin’s humane principles in battle,treatment of captives and civilians,and peace terms;he was admirable and did not stoop to dishonorable acts.',
        'The admiral calls him a true hero.',
        'Al Ferid recalls hearing that Saladin’s armor is missing;if the admiral wishes to follow his example,he suggests seeking it.',
    ], notes=['Keep the shopkeeper’s anger and Al Ferid’s viewpoint as dialogue;do not turn them into omniscient historical narration oradd an ethnicity/religion insult. Preserve both menu branches. Do not add an armor location the source withholds.']),
    225: dict(context='Gerhard watches the sunset,moved by a Japanese account of Noritsune’s final battle. The admiral recognizes his admiration andnotices the submerged-armor clue before Gerhard returns to duty.', meanings=[
        'Gerhard is silent.',
        'The admiral asks what is wrong: watching the sunset,is Gerhard thinking about something?',
        'Gerhard says he heard of a certain person here in Japan,and unexpectedly found himself deeply moved.',
        'The admiral asks whose story it is.',
        'A warrior from several hundred years ago,named Noritsune.',
        'The admiral asks what that person did so long ago.',
        'He belonged to a once-glorious clan. Repeated defeats against a rival force gradually drove the clan toward destruction.',
        'Among weak clansmen falling one after another,he alone stood bravely against the enemy;the account continues.',
        'During the final naval battle,he reportedly leapt across seven ships toward the vessel carrying the enemy commander.',
        'At last exhausted,he reportedly gripped an enemy soldier under each arm and vanished into the bottom of the strait together with his magnificent armor.',
        'Gerhard marvels that such a resolute man lived in this small Eastern country,and feels he has glimpsed the essence/spirit of its people.',
        'The admiral calls it a fearsome death and judges that he must have been a true warrior.',
        'Gerhard emphatically agrees.',
        'The admiral notes how strongly Gerhard seems to have been affected.',
        'The admiral reflects on the clue: into the strait,together with magnificent armor.',
        'Gerhard remarks that he has uncharacteristically talked at length and suggests returning to work.',
    ], notes=['Preserve the account’s seven-ship figure and two enemy soldiers;do not silently harmonize it with another version of the legend. The commander,the clan andthe strait are unnamed here. Gerhard’s cultural generalization is his personal reaction,not narration.']),
}

if __name__ == '__main__':
    path = ROOT / 'B221_B225_clean_meanings_before_English.json'; decisions = ROOT / 'B221_B225_source_meaning_decisions.json'
    assert not path.exists() and not decisions.exists()
    packet_path = ROOT / 'clean_source_packet.json'; packet = load(packet_path)
    save(decisions, dict(blocks=DECISIONS,source_only_meanings_not_localized_drafts=True)); rows=[]
    for group in packet['groups']:
        if group['block'] not in DECISIONS: continue
        d=DECISIONS[group['block']]; assert len(group['records']) == len(d['meanings'])
        for r,meaning in zip(group['records'],d['meanings'],strict=True):
            assert bytes.fromhex(r['source_hex'])[1:].decode('cp932') == r['source_Japanese']
            rows.append(dict(**r,source_meaning=meaning,exchange_context=d['context'],native_identity_terms_localization_andformatting_pending=True,new_credit=0))
    assert len(rows)==60
    save(path,dict(records=rows,source_meanings=60,complete_exchanges=list(DECISIONS),source_fidelity_notes={k:v['notes'] for k,v in DECISIONS.items()},
        no_current_ROM_English_intake_for_this_batch=True,source_only_not_localized_English=True,no_all_historical_exposure_claim=True,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [packet_path,decisions,Path(__file__)]}))
    print('60 clean meanings saved across five whole blocks,including one control-only block;no new credit.')
