"""Faithful natural-English source review of24 sail/boarding alternatives."""

from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/sails_boarding_v879')
ROM=Path('out/all_routes_combined_v876_candidate.nds')
MANUSCRIPT=Path('translations/sails_boarding_editorial_manuscript_v1.json')
IDS=tuple(range(1523,1547))
PROSE={1523: ('Offers to handle both fair winds and headwinds.',
        "Fair wind or headwind, I'll handle it.",
        'Restore both wind conditions and the personal assurance without claiming magical weather control.',
        'revise'),
 1524: ('Says fore-and-aft and square sails must be used appropriately according to the wind.',
        'We need to use fore-and-aft and square sails to suit the wind.',
        'Restore both distinct sail types and matching their use to the wind;do not suggest rebuilding the rig or use lateen as a synonym '
        'for all fore-and-aft sails.',
        'revise'),
 1525: ('Feels likely to be blown away when the wind is strong.',
        "When the wind's strong, I feel like I'll blow away!",
        'Restore the strong-wind condition and personal feeling rather than reporting an actual fall.',
        'revise'),
 1526: ('Asks whether the speakers sail handling has improved.',
        "How's that? I've gotten better with the sails, haven't I?",
        'Restore the personal improvement and request for approval in the casual voice.',
        'revise'),
 1527: ('Explains setting sails half open when reducing speed.',
        'To slow down, set the sails to Half Open.',
        'Use the source-bound current HELP83 setting Half Open;preserve the instruction without unsupported button symbols.',
        'revise'),
 1528: ('Emphasizes that fore-and-aft and square sails are very different.',
        'Fore-and-aft sails and square sails are very different.',
        'Restore the actual two sail types and strong distinction;do not reduce them to unspecified types.',
        'revise'),
 1529: ('Says the speaker too can handle the wind.',
        'I can handle the wind, too!',
        'Restore the first-person boast and too without turning it into literal command over nature.',
        'revise'),
 1530: ('Says reading the wind is what makes a fully competent sail handler.',
        'A real sail handler knows how to read the wind.',
        'Keep wind-reading competence and the established job;do not invent a sailmaster rank.',
        'revise'),
 1531: ('Rafael says he has learned to read the wind.',
        'I can read the wind now!',
        'Restore the personal acquired ability and now in a natural enthusiastic statement.',
        'revise'),
 1532: ('Joakim says coordination between the sail handler and helmsman is important.',
        'The sail handler and helmsman need to work together.',
        'Use established job terms and restore the need for coordination as a full thought.',
        'revise'),
 1533: ('Lil reacts in alarm that the wind seems about to blow her away.',
        "Whoa! The wind's going to blow me away!",
        'Preserve the exaggerated anticipatory alarm and explicit wind;no actual fall or injury is reported.',
        'revise'),
 1534: ('Maria says a dead calm remains difficult no matter how much skill improves.',
        'No matter how good you get, a dead calm is still a struggle.',
        'Restore the despite-skill qualification and negative difficulty;remove the older ambiguous None beats a dead calm wording.',
        'revise'),
 1535: ('Says the speaker regularly trains like this.',
        'I make a habit of training like this.',
        'Restore the habitual training and demonstration without claiming every literal calendar day is spent training.',
        'revise'),
 1536: ('Offers to handle close combat during boarding.',
        'Leave boarding to me.',
        'Retain the natural concise assurance in the source boarding-combat context.',
        'retain'),
 1537: ('Resolves to become stronger and stronger.',
        "I'll keep getting stronger and stronger!",
        'Restore personal resolve and the repeated more-and-more emphasis.',
        'revise'),
 1538: ('Asks whether the current form looks the part.',
        "How's this? Do I look the part?",
        'Render sama ni natteru naturally as looking the part,without inventing an improvement claim or a new rank.',
        'revise'),
 1539: ('Offers to be relied on if a fight breaks out.',
        'Count on me in a fight!',
        'Retain the natural assurance and conditional combat setting.',
        'retain'),
 1540: ('Reacts that the speakers lower back has just made a cracking sound.',
        "Whoa! My back just went 'crack'...",
        'Preserve just-now timing,sound and comic reaction;do not diagnose an injury or add definite pain.',
        'revise'),
 1541: ('Complains that continued training makes the speaker hungry.',
        'All this training is making me hungry!',
        'Localize the continued-training hunger naturally as a personal complaint;this flavor text does not spend food or change hunger '
        'stats.',
        'revise'),
 1542: ('Says constant regular training is important.',
        'Regular training is essential.',
        'Restore the ongoing regularity as well as the importance of training.',
        'revise'),
 1543: ('Rafael asks whether his swordplay has improved a little.',
        "My swordplay's gotten a little better, hasn't it?",
        'Restore personal swordplay,the modest a little and the confirmation question.',
        'revise'),
 1544: ('Joakim says he must demonstrate swordsmanship for the sailors to follow.',
        'I need to show the crew some proper swordplay...',
        'Express the obligation to set a practical swordsmanship example naturally;do not reduce it to a disconnected subject label.',
        'revise'),
 1545: ('Lil asks for admiration of her elegant dazzling swordplay.',
        "Well? How's that for dazzling swordplay?",
        'Restore the confident flourish in karei rather than an unqualified generic swordplay question.',
        'revise'),
 1546: ('Maria says she will take the front and command in boarding combat.',
        "I'll take command from the front in boarding combat.",
        'Preserve both commanding and leading from the front without inventing troop numbers or a completed attack.',
        'revise')}


def main():
    assert not MANUSCRIPT.exists();ROOT.mkdir(parents=True,exist_ok=True)
    path=Path('work/analysis/sails_boarding_v878/source_context_packet.json');packet=read(path)
    ledger=read('translations/editorial_review_current_v1.json')
    assert sha(ROM.read_bytes())==packet['candidate_sha256']==ledger['current_integrated_candidate']['sha256']
    assert ledger['records_editorially_completed']==808 and ledger['records_with_source_and_prose_pass']==811
    assert len(packet['all50_original_role_helper_selections'])==50
    sources={r['message_id']:r for r in packet['records_with_immediate_storage_neighbors']};rows=[]
    for n,(meaning,english,note,decision) in PROSE.items():
        source=sources[n];assert english==' '.join(english.split()) and english.isascii() and not any(c in english for c in '%{}\n')
        if decision=='retain':assert english==source['current_English'].strip()
        role,first,label=(0,1523,'Sail Handling') if n<1535 else (7,1535,'Boarding');index=n-first
        hero=index-8 if index>=8 else None
        speaker=f'Native NPC voice class{index}' if hero is None else ['Rafael','Joakim (native captain1)','Lil','Maria'][hero]
        rows.append({'id':f'COMMON_MESSAGE_{n}','message_id':n,'role_ID':role,'voice_class':index if hero is None else None,'protagonist_ID':hero,
            'speaker':speaker,'context':f'Independent {label}{role} work comment. Original1278C chooses eight NPC voices;128B4 uses the genuine captain. Storage neighbors are independent alternatives,not consecutive speech. No measurement,discovery,report or gameplay action is performed by this flavor text.',
            'source_Japanese':source['source_Japanese'],'source_hex':source['source_hex'],'source_reference':source['source_reference'],
            'canonical_source_hex':source['canonical_text_hex'],'current_reference':source['current_reference'],
            'current_text_hex':source['current_text_hex'],'current_English':source['current_English'],
            'source_meaning':meaning,'english':english,'localization_note':note,'editorial_decision':decision,
            'native_argument_count':0,'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False}})
    assert tuple(r['message_id'] for r in rows)==IDS and sum(r['editorial_decision']=='revise' for r in rows)==22
    terms=Path('work/analysis/sails_boarding_v879/terminology_proof.json');assert read(terms)['candidate_sha256']==sha(ROM.read_bytes())
    save(MANUSCRIPT,{'format':'dk4-natural-dialogue-source-manuscript-v2','translation_policy':'natural-dialogue-v2','target_locale':'en-US',
        'encoder':'dialogue-relocatable-v1','consumer_layout_profile':'deck-sails-boarding-visible-v1',
        'review_gates':['source','context','localization','naturalness'],'formatting_review_pending':True,
        'status':'24-source-prose-reviewed-native-format-integration-and-actual-pending','file_path':'/COMMON/MESFILE.DK4',
        'source_clean_ROM_sha256':packet['source_clean_ROM_sha256'],'current_ROM':str(ROM),'current_ROM_sha256':sha(ROM.read_bytes()),
        'current_COMMON_sha256':packet['COMMON_sha256'],'current_ARM9_sha256':packet['ARM9_sha256'],
        'native_context_proof':str(path),'native_context_proof_sha256':sha(path.read_bytes()),'native_terminology_proof':str(terms),'native_terminology_proof_sha256':sha(terms.read_bytes()),'records':rows,'full_goal_complete':False})
    save(ROOT/'editorial_ledger_before_source_review.json',ledger)
    ledger['records_with_source_and_prose_pass']=ledger['records_with_source_prose_drafts']=835
    ledger['source_prose_reviewed_counts_by_file']['/COMMON/MESFILE.DK4']=834
    ledger['reviewed_but_incomplete_COMMON_IDs']=[750,751,752,*IDS]
    ledger['active_source_prose_drafts']={'native_message_IDs':[750,751,752,*IDS],
        'manuscripts':['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json',str(MANUSCRIPT)],
        'status':'three-older-context-unmapped-and24-sails-boarding-source-prose-reviewed-format-release-pending',
        'note':'These27 reviewed pending entries are not the full remaining shared/route/player prose or raw-source scope.'}
    checkpoint=('V879 source/prose-reviews24 SailHandling0/Boarding7 comments1523-1546:22 proposed revisions and2 retentions. '
        'All50 original selections cover eight NPC voices and four genuine captains per duty. Drafts restore fair/head winds,both sail types,Half Open setting,wind-reading competence,the difficulty of a dead calm despite skill,regular training,personal reactions and command from the front in boarding combat. '
        'Native layout,registered integration and actual scenes remain pending. V876 remains current;808 complete,835 source/prose reviewed. Older750-752 and all unreviewed shared/routes/player prose/raw coverage remain;separate graphics/all18 plaques and later older-record re-audit stay open;full goal active.')
    ledger['latest_checkpoint']=checkpoint
    ledger['sails_boarding_v879']={'status':'source-prose-reviewed-native-release-and-actual-pending','native_message_IDs':list(IDS),
        'manuscript':str(MANUSCRIPT),'source_context_proof':str(path),'proposed_revisions':22,'justified_retentions':2,'completed_entries_added':0}
    ledger['research_checkpoints'].append({'id':'V879-Sails-Boarding24-source-prose','proof':str(path),'manuscript':str(MANUSCRIPT),
        'new_source_prose_reviews':24,'completed_entries_added':0,'previous_goal_turn_classification':'progress:Survey/Lookout24 completed inV876,next24 original contexts proved',
        'this_goal_turn_classification':'progress:24 faithful source glosses,natural English reviews and exact source/current references','full_goal_complete':False})
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==835
    save('translations/editorial_review_current_v1.json',ledger)
    doc=Path('docs/sails_boarding_v879_source_review.md');doc.write_text('# V879: sail handling and boarding source review\n\n'+checkpoint+'\n',encoding='utf-8')
    for p in map(Path,('docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')):
        with p.open('a',encoding='utf-8') as f:f.write('\n\n## V879: sail handling and boarding source review\n\n'+checkpoint+' See [V879 review](sails_boarding_v879_source_review.md).\n')
    archive=Path('E:/Rota Nova translations/Editorial review/V879 Sail handling and boarding source review');assert not archive.exists();copied=[]
    for source in (MANUSCRIPT,path,Path(__file__),doc,Path('translations/editorial_review_current_v1.json'),Path('scripts/prepare_sails_boarding_context_v878.py')):
        target=archive/source.absolute().relative_to(Path.cwd());target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target)
        assert sha(source.read_bytes())==sha(target.read_bytes());copied.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    save(ROOT/'archive_manifest.json',{'files':copied,'all_hashes_verified':True,'completed_entries_added':0})
    print('Sails/Boarding24 source/prose reviewed:22 revisions,2 retentions.808 complete,835 source/prose;native/release/actual pending.',flush=True)


if __name__=='__main__':main()
