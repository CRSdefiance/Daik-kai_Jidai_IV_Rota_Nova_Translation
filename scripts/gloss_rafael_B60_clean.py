"""Read Pereira's complete branching exchange from clean Japanese before old English."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.gloss_rafael_B51_B59_clean import ROOT

MEANINGS = '''
6|Pereira checks that the visitor is FA.
17|Pereira asks whether Rafael brought the Proof.
21|Rafael says he found the key needed to search for the Proof of Conquest.
25|Pereira considers this with a noncommittal response.
31|Alternative fulfillment:Rafael says he found the promised Proof of Conquest in East Asia.
35|Pereira examines it and confirms it is genuine.
41|Pereira agrees to proceed and tells Rafael to follow.
44|Pereira repeats that his position prevents him from openly helping them.
48|Rafael listens silently.
53|Pereira says they share a desire to strike at Coen and Spain,who are common enemies.
57|Rafael asks whether that alone is not sufficient reason for an agreement to defeat Coen and Spain together.
62|Pereira says it would be so if the problem were simple.
66|Rafael asks whether it is not simple.
71|Pereira bluntly asks what their true enemy is and tells them to consider carefully before answering.
75|Rafael is surprised and thinks about the question of their true enemy.
111|In the Spain-oriented answer branch,Pereira asks whether they truly intend to defy Spain's Invincible Armada,noting that even Albuquerque has joined Spain's side.
114|Rafael says he is entirely serious.
119|Pereira finds that interesting but asks whether they would still act if he refused to help.
123|Rafael says that if necessary they will defeat Spain and restore Portugal on their own,even if it takes longer.
127|Pereira pauses silently.
131|Pereira says that makes matters straightforward.
135|Rafael is puzzled.
140|Pereira says many hypocrites flaunt halfhearted patriotism,and no number of lives would suffice if he allied with people like that.
143|Pereira concludes he was worrying unnecessarily and can trust Rafael.
147|Pereira says they must hurry to finish Coen off and return to their homeland.
150|Rafael addresses Pereira with emotion.
155|Pereira decides to give Rafael something.
160|Rafael asks what it is.
165|Pereira says it is apparently a key needed to decipher the map to a Proof of Conquest,and urges Rafael to accomplish deeds worthy of a conqueror.
169|The blunt companion asks whether they may really take it.
173|Pereira says he is not interested and cannot be bothered to gather all seven,so it now belongs to them.
177|Rafael accepts and asks Pereira to make an agreement against Coen here and now.
182|Pereira asks what follows from that proposal.
201|First strategy branch:Rafael proposes cooperating to defeat Coen before anything else.
205|Pereira understands this as eliminating a threat in their rear and admits that even he would have considerable difficulty fighting Coen alone.
208|Rafael says that if he were Spain's king,he would use every means to strip Portugal's royal family of its succession rights permanently,and warns that there is no time.
212|Rafael wants defeating Coen to give his group enough strength to challenge Spain's Valdes even on their own.
217|Pereira is shocked that they mean to do it alone and asks whether they are sane.
220|Rafael says Pereira is responsible for this region and cannot simply abandon his post.
225|Pereira angrily rejects worrying about his post when they are about to rebel against Spain's king.
229|Rafael says failure of this plan would permanently cost Pereira his office as governor of Indochina.
234|Pereira laughs and says that is something he already understands perfectly.
238|Rafael insists that if their own strength proves insufficient,there must still be someone to whom Portugal's fate can be entrusted.
242|Pereira is struck by the explanation.
246|Rafael says all Europe covets the Spice Islands;holding them would someday permit an equal contest with mighty Spain.
250|Rafael says that if Pereira becomes Portugal's final stronghold,his group can fight without holding back.
255|Pereira lets out a quiet amused breath.
259|Pereira laughs,finds Rafael fascinating,andadmits he is impressed.
263|Pereira agrees to stake his hopes on Rafael andtells him to leave what comes afterward to Pereira.
267|Rafael earnestly asks him to do so.
273|Alternative strategy branch:Pereira asks what Rafael means.
277|Rafael says they will leave Southeast Asia immediately.
281|Pereira asks what comes next.
285|Rafael says they will sail to Europe to defeat Spain's Valdes.
289|Pereira is startled and asks him to repeat that.
293|Rafael repeats the warning that Spain's king would use every means to strip Portugal's royal family of succession rights permanently,andthat there is no time.
297|Pereira acknowledges the concern,but asks whether that means putting Coen off until later.
301|Rafael says no;he will entrust everything here to Pereira,the governor of Indochina responsible for Southeast Asia.
306|Pereira realizes Rafael is asking him to guard their rear.
309|Rafael says that if someone dependable is looking after this region,his group can face Valdes with all their strength.
314|Pereira laughs that Rafael has already incorporated him as a piece in his strategy.
318|Pereira agrees to handle it,but asks what happens if he drives Coen out himself.
322|Rafael says he has received the key to the Proof of Conquest andhas no objection to letting Pereira have this region's trading rights.
327|Pereira laughs andasks whether that is charity;he says Rafael may later defeat Pereira as well andtake Southeast Asia if he wishes.
330|Rafael protests awkwardly at the suggestion.
335|Pereira asks whether business is supposed to be fair,with free competition.
338|Rafael agrees,but hesitates.
343|Pereira says that in exchange he expects Rafael to deal properly with Valdes,andseeks his agreement.
346|Rafael emphatically agrees.
354|Pereira reflects that this group might truly be able to restore their homeland Portugal,repeating that he means them in particular.
362|Pause before the alternate true-enemy branch.
366|Pereira changes the question andasks FA who is currently the strongest power in the world.
370|The blunt companion says it must be whoever has the largest trading sphere,either them orsomeone else;the sentence trails off.
374|Pereira says that isnot what he means:he isasking who would be best positioned if they seriously set out to conquer the world.
377|Rafael tentatively suggests Spain because it has the Invincible Armada.
382|Pereira concedes that has some merit,then asks whether FA knows the Spice Islands.
386|Rafael says they are in this region.
391|Pereira confirms andsays the Spice Islands are treasure islands to present-day Europe,asking whether Rafael understands.
394|Rafael acknowledges this after a pause.
399|Pereira explains that products from this region,not just spices,yield immense profits,andstarts describing what would happen if whoever controlled them used that wealth for conquest.
402|Rafael realizes that such a person could take over the world.
407|Pereira confirms.
411|The blunt companion isappalled by the idea of Antony Coen becoming ruler of the world andvehemently rejects it.
423|The boisterous companion says that even if God permits it,he will not.
430|Rafael reflects that controlling the Spice Islands means controlling the world.
442|The fiery companion says this cannot simply be dismissed as good fortune.
448|Pereira observes that they now seem to understand the situation.
451|Pereira isnot currently waging all-out war against Coen because if he lost,there would be no one left to stop Coen.
454|Rafael is silent.
459|Pereira approves of restoring their homeland,but says they cannot focus on that alone andlet Coen take the world.
462|Rafael asks what they should do.
467|Pereira tells them to defeat Spain's Valdes first;with the strength gained there,they andPereira would have a chance against Coen.
470|Rafael thinks about Valdes's forces andSpain's Invincible Armada.
474|Pereira says that if he were Spain's king,he would use every means to deprive Portugal's royal family of succession rights permanently,andwarns that there isno time.
477|Pereira says he can give his full support once Spain is subdued andPortugal restored.
481|Rafael agrees that this follows.
486|Pereira says Valdes should know where the Mediterranean Proof of Conquest lies,andtaunts that anyone unable to defeat that little-mustached man will not defeat Coen for another hundred years.
489|Rafael agrees andpromises to defeat Valdes andreturn.
493|Pereira entrusts this task to Admiral FA.
'''

if __name__ == '__main__':
    output = ROOT / 'B60_99_clean_meanings_v1.json'; assert not output.exists()
    packet_path = ROOT / 'clean_source_packet.json'; packet = load(packet_path)
    source_path = Path(packet['source_ROM']); assert sha(source_path.read_bytes()) == packet['source_ROM_sha256']
    source = NdsImage.open(source_path).read_file('/data/SC0.DK4'); blocks = IlnkContainer.parse(source).blocks
    group = next(g for g in packet['groups'] if g['block'] == 60)
    assert sha(blocks[60]) == group['clean_block_sha256'] and blocks[60].hex() == group['clean_block_hex']
    meanings = {int(k):v for k,v in (line.split('|',1) for line in MEANINGS.strip().splitlines())}
    assert set(meanings) == {r['source_reference']['record_index'] for r in group['records']}
    records = []
    context = ('Complete branching Pereira negotiation:proof/key prerequisites,his constraint on open aid,andquestions about the true enemy. '
        'Spain-first conviction leads to two alternate Coen/Valdes strategies;the other branch explains the Spice Islands andasks Rafael to confront Valdes first. '
        'Rafael is earnest andstrategic;Pereira is blunt,testing andultimately impressed. Branches are alternatives,not one linear conversation. '
        'Portugal restoration androyal succession are explicit source facts;do not invent Rafael’s ancestry orPereira’s allegiance beyond what is said.')
    for row in group['records']:
        current = deepcopy(row); current.update(source_meaning=meanings[row['source_reference']['record_index']], whole_exchange_context=context,
            source_read_with_all_previous_andfollowing_speeches_in_block=True,
            review=dict(source=True,context=False,localization=False,naturalness=False,formatting=False),
            event_branch_identity_native_controls_andproper_name_bindings_pending=True)
        records.append(current)
    assert len(records)==99 and all(r['earlier_English_unconsulted'] for r in records)
    save(output,dict(format='dk4-clean-source-meaning-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        source_packet=str(packet_path),source_packet_sha256=sha(packet_path.read_bytes()),records=records,
        all99_clean_meanings_before_current_English=True,no_localized_draft_orROM_orcompletion_credit=True,
        event_membership_not_natural_activation=True,new_credit=0,guide_photos=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print('Saved99 clean meanings for the complete branching Pereira exchange;245 next-story meanings now saved,zero completion credit.')
