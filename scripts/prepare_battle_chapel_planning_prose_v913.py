"""Faithful American-English review of24 battle Chapel/Planning alternatives."""

from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.battle_cooking_livestock_editorial import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.prepare_work_comments_v842 import reference
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_chapel_planning_v913')
ROM=Path('out/all_routes_combined_v910_candidate.nds')
MANUSCRIPT=Path('translations/battle_chapel_planning_editorial_manuscript_v1.json')
IDS=tuple(range(1645,1669))
PROSE={
1645:('Prays to the Lord to save the speakers fleet.',
      'Lord, deliver our fleet...',
      'Retain the natural formal prayer:deliver means save in this religious context. Preserve the trailing prayerful pause.','retain'),
1646:('Prays for peace for those killed in battle.',
      'Grant peace to those who fell.',
      'Retain the natural prayer and established English fell idiom for battle deaths;do not add named casualties.','retain'),
1647:('Asks God to protect the speakers companions.',
      'God, please protect my friends.',
      'Retain the natural personal plea. Friends naturally conveys the close companions in this crew context without adding kinship.','retain'),
1648:('Says the speaker is praying that everyone stays safe.',
      "I'm praying everyone stays safe.",
      'Restore the complete personal statement rather than the clipped Praying all stay safe.','revise'),
1649:('Roughly says the speaker would rather fight than pray.',
      "I'd rather fight than pray!",
      'Restore the personal preference with a natural contraction and blunt exclamation.','revise'),
1650:('Reassures everyone that God is with them.',
      'God is with us, everyone!',
      'Retain the natural reassurance and inclusive everyone/us. This is religious confidence,not a proved game effect.','retain'),
1651:('Casually asks God to save the speakers friends.',
      'God, please save my friends.',
      'Retain the natural direct plea;do not invent particular injuries or a rescue result.','retain'),
1652:('Grieves to the Lord that many lives are again being lost;the source trails off before stating their fate.',
      'Lord... So many more lives lost...',
      'Preserve the broken-off grieving thought. Lost makes the casualty implication of the battle-prayer context natural in English;it is a contextual inference,not a report of a game casualty count. More conveys another round of losses.','revise'),
1653:('Rafael asks the listener to lend strength to Claudio and his other friends.',
      'Please lend your strength to Claudio and my other friends.',
      'Restore the named Claudio reference and personal prayer. Source nickname Kurau is expanded to the established Claudio,as in already-reviewed1409;no new naming decision or relationship is introduced.','revise'),
1654:('Hodram prays for victory for his own fleet.',
      'Grant victory to my fleet...',
      'Restore my fleet and the reflective pause rather than replacing the fleet with generic us.','revise'),
1655:('Lil confidently says victory is certain because she prayed to God.',
      "I prayed to God, so we're sure to win!",
      'Restore her personal prayer and explicit God. Preserve her cheerful confidence as characterization;no guaranteed game outcome is asserted.','revise'),
1656:('Maria wishes that all her companions remain safe.',
      'May everyone stay safe...',
      'Restore remaining safe and the soft trailing wish. The old come home adds a return journey that the source does not mention. The crew context identifies everyone.','revise'),
1657:('Observes that schemes cannot be used in a naval battle.',
      "We can't use schemes in a sea battle.",
      'Preserve inability to use schemes during naval combat. The old at sea incorrectly extends the limitation to all sailing;cannot use is not the same as schemes being ineffective.','revise'),
1658:('Says that using schemes in naval combat is out of the question.',
      "Scheming's out of the question in a sea battle...",
      'Use a natural frustrated thought and keep the naval-battle scope instead of all activity at sea.','revise'),
1659:('Remarks that even a strategist has idle time during a naval battle.',
      'Even a strategist has nothing to do in a sea battle.',
      'Restore even and a natural complete observation. Do not imply strategists are always idle while sailing.','revise'),
1660:('Says one has to use direct or conventional tactics in a naval battle.',
      'We have to rely on direct tactics in a sea battle.',
      'Keep the naval-battle limitation and established direct tactics wording from1456. Do not turn seikouhou into a moral claim about fighting fairly or a specific order to ram head-on.','revise'),
1661:('Roughly says the speaker has no schemes and asks to be allowed to fight.',
      "I've got no schemes! Just let me fight!",
      'Restore the personal lack of schemes. The old No schemes can sound like an order forbidding others to scheme.','revise'),
1662:('Wishes schemes could be used even during naval battles.',
      'I wish we could use schemes in sea battles, too...',
      'Restore the personal wish,the even/too contrast and the distinction between using schemes and their effectiveness.','revise'),
1663:('Casually considers sneaking a bite because naval battle leaves the speaker with nothing to do.',
      "I've got nothing to do in a sea battle. Maybe I'll sneak a bite...",
      'Restore the battle context and personal tentative intention. Sneak a bite conveys tsumamigui rather than merely noticing hunger.','revise'),
1664:('Politely says the speaker has no part to play once a naval battle begins.',
      'I have no part to play in a sea battle.',
      'Use the familiar no-part-to-play idiom for deru maku ga nai,in a natural complete sentence. This is the assigned strategists reflection,not a blanket claim about an officer.','revise'),
1665:('Rafael says schemes are unnecessary now and direct tactics are the only way.',
      "We don't need schemes now. Direct tactics are the only way!",
      'Restore explicit lack of need now and the established direct tactics term,keeping his confident voice.','revise'),
1666:('On hearing there is a sea battle,Hodram wants to be assigned to the Marine Barracks.',
      'A sea battle?! Assign me to the Marine Barracks...',
      'Restore the explicit room request and source trailing thought. Marine Barracks is the established help term for kaihei tsumesho;the speaker is not joining a different military service.','revise'),
1667:('Lil trails off about there being little point staying in the Strategy Room during a sea battle.',
      "There's not much point staying in the Strategy Room during a sea battle...",
      'Restore the full battle context and natural personal complaint. Strategy Room matches the established help label for sanbou shitsu.','revise'),
1668:('Maria reflects that she has nothing to do by staying here.',
      'Nothing for me to do here...',
      'Retain the natural self-directed trailing thought. Here is identified by her assigned Strategy Room;do not add a new activity or order.','retain')}


def main():
    assert not MANUSCRIPT.exists();ROOT.mkdir(parents=True,exist_ok=True)
    packet_path=Path('work/analysis/battle_chapel_planning_v912/source_context_packet.json');packet=read(packet_path)
    ledger=read('translations/editorial_review_current_v1.json')
    assert ledger['records_editorially_completed']==930 and ledger['records_with_source_and_prose_pass']==933
    assert sha(ROM.read_bytes())==packet['candidate_sha256']==ledger['current_integrated_candidate']['sha256']
    assert len(packet['all150_original_battle_helper_main_and_ordinary_control_selections'])==150
    current,clean=map(NdsImage.open,(ROM,'work/clean.nds'))
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    en=current_entries(current.read_file('/COMMON/MESFILE.DK4'),current.read_file('/__arm9__.bin'))
    context=[]
    for n in (*range(1435,1459),1409):
        context.append({'message_id':n,'source_Japanese':jp[n].text.decode('cp932'),'source_hex':jp[n].text.hex(),
            'source_reference':reference(jp[n]),'current_English':en[n].text.decode('cp932'),
            'current_text_hex':en[n].text.hex(),'current_reference':reference(en[n]),
            'already_reviewed_ordinary_context_no_new_credit':True})
    source_context=ROOT/'ordinary_context_and_terms.json'
    arm=current.read_file('/__arm9__.bin');assert arm[0x143B3C:0x143B44]==b'Schemes\0'
    save(source_context,{'candidate_sha256':sha(ROM.read_bytes()),'source_clean_ROM_sha256':packet['source_clean_ROM_sha256'],
        'records':context,'independent_alternatives_not_consecutive_dialogue':True,
        'established_term_documents':{p:sha(Path(p).read_bytes()) for p in ('translations/skill_terms_help_manuscript_v1.json','translations/crew_help_manuscript_v1.json','translations/character_name_localization_policy_v1.json')},
        'native_ARM9_Schemes_caption_offset':0x143B3C,'native_ARM9_Schemes_caption_hex':arm[0x143B3C:0x143B44].hex(),
        'established_room_terms':{'海兵詰所':'Marine Barracks','参謀室':'Strategy Room'},
        'Claudio_nickname_expansion_consistent_with_completed1409':True,
        'casualty_loss_1652_is_documented_contextual_inference_not_native_casualty_count':True})
    sources={r['message_id']:r for r in packet['records_with_immediate_storage_neighbors']};rows=[]
    for n,(meaning,english,note,decision) in PROSE.items():
        s=sources[n];role,first,label=(18,1645,'Chapel') if n<1657 else (19,1657,'Planning');index=n-first
        hero=index-8 if index>=8 else None;voice=index if hero is None else None
        speaker=f'Native NPC voice class{voice}' if hero is None else ['Rafael','Hodram Joakim Bergstrom (genuine captain1)','Lil','Maria'][hero]
        assert english==' '.join(english.split()) and english.isascii() and not any(c in english for c in '%{}\n')
        if decision=='retain':assert english==s['current_English'].strip()
        rows.append({'id':f'COMMON_MESSAGE_{n}','message_id':n,'role_ID':role,'voice_class':voice,'protagonist_ID':hero,'speaker':speaker,
            'context':f'Independent battle {label}{role} working comment. Original12600 selects eight NPC voice alternatives and12720 selects the genuine captain. Main12104 state0 uses battle mode fields8/12=0/1 for eligible working responses. Storage neighbors are independent alternatives,not consecutive speech. Chapel prayers and strategists reflections are flavor dialogue,not issued battle commands or guaranteed outcomes.',
            'source_Japanese':s['source_Japanese'],'source_hex':s['source_hex'],'source_reference':s['source_reference'],
            'canonical_source_hex':s['canonical_text_hex'],'current_reference':s['current_reference'],
            'current_text_hex':s['current_text_hex'],'current_English':s['current_English'],
            'source_meaning':meaning,'english':english,'localization_note':note,'editorial_decision':decision,
            'native_argument_count':0,'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False}})
    assert tuple(r['message_id'] for r in rows)==IDS and sum(r['editorial_decision']=='revise' for r in rows)==18
    save(MANUSCRIPT,{'format':'dk4-natural-dialogue-source-manuscript-v2','translation_policy':'natural-dialogue-v2','target_locale':'en-US',
        'encoder':'dialogue-relocatable-v1','consumer_layout_profile':'deck-battle-chapel-planning-visible-v1',
        'review_gates':['source','context','localization','naturalness'],'formatting_review_pending':True,
        'status':'24-source-prose-reviewed-native-format-integration-and-actual-pending','file_path':'/COMMON/MESFILE.DK4',
        'source_clean_ROM_sha256':packet['source_clean_ROM_sha256'],'current_ROM':str(ROM),'current_ROM_sha256':sha(ROM.read_bytes()),
        'current_COMMON_sha256':packet['COMMON_sha256'],'current_ARM9_sha256':packet['ARM9_sha256'],
        'native_context_proof':str(packet_path),'native_context_proof_sha256':sha(packet_path.read_bytes()),
        'ordinary_context_supplement':str(source_context),'ordinary_context_supplement_sha256':sha(source_context.read_bytes()),
        'records':rows,'full_goal_complete':False})
    save(ROOT/'editorial_ledger_before_source_review.json',ledger)
    ledger['records_with_source_and_prose_pass']=ledger['records_with_source_prose_drafts']=957
    ledger['source_prose_reviewed_counts_by_file']['/COMMON/MESFILE.DK4']=956
    ledger['reviewed_but_incomplete_COMMON_IDs']=[750,751,752,*IDS]
    ledger['active_source_prose_drafts']={'native_message_IDs':[750,751,752,*IDS],
        'manuscripts':['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json',str(MANUSCRIPT)],
        'status':'three-older-context-unmapped-and24-battle-chapel-planning-source-prose-reviewed-format-release-pending',
        'note':'These27 pending reviewed entries are not the full remaining shared/routes/player prose or raw-source scope.'}
    checkpoint=('V913 source/prose-reviews24 battle Chapel18/Planning19 comments1645-1668:18 revisions and6 retentions. '
        'All150 original battle-helper/main/ordinary controls pass. Drafts restore Claudio in Rafaels prayer,my fleet in Hodrams prayer,Lils personal prayer,companions safety without an invented return home,and the naval-battle scope of schemes/strategists comments. '
        'Strategy Room,Marine Barracks and Schemes match established terminology. Native layout,registered integration and actual scenes remain pending. V910 stays current;930 complete,957 source/prose reviewed. '
        'Older750-752,mood1833,special actors1885-1888,raw abandon caption0x134E54,other shared/routes/player prose/raw inventory,separate graphics/all18 plaques,Samwell header and later older-record re-audit remain open;full goal active.')
    ledger['latest_checkpoint']=checkpoint
    ledger['battle_chapel_planning_v913']={'status':'source-prose-reviewed-native-release-and-actual-pending','native_message_IDs':list(IDS),
        'manuscript':str(MANUSCRIPT),'source_context_proof':str(packet_path),'proposed_revisions':18,'justified_retentions':6,'completed_entries_added':0}
    ledger['research_checkpoints'].append({'id':'V913-Battle-Chapel-Planning24-source-prose','proof':str(packet_path),'manuscript':str(MANUSCRIPT),
        'new_source_prose_reviews':24,'completed_entries_added':0,
        'previous_goal_turn_classification':'progress:25 cooking/livestock entries completed in V910 and next24 original contexts mapped',
        'this_goal_turn_classification':'progress:24 faithful glosses,natural English decisions,exact references and ordinary-context/terminology supplement',
        'full_goal_complete':False})
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==957
    save('translations/editorial_review_current_v1.json',ledger)
    doc=Path('docs/battle_chapel_planning_v913_source_review.md')
    with doc.open('x',encoding='utf-8') as f:f.write('# V913: battle Chapel and Planning source review\n\n'+checkpoint+'\n')
    for d in map(Path,('docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')):
        with d.open('a',encoding='utf-8') as f:f.write('\n\n## V913: battle Chapel and Planning source review\n\n'+checkpoint+' See [V913 source review](battle_chapel_planning_v913_source_review.md).\n')
    archive=Path('E:/Rota Nova translations/Editorial review/V913 Battle Chapel Planning source review');assert not archive.exists();copied=[]
    for source in (MANUSCRIPT,packet_path,source_context,Path(__file__),doc,Path('translations/editorial_review_current_v1.json')):
        target=archive/source.absolute().relative_to(Path.cwd());target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target)
        assert sha(source.read_bytes())==sha(target.read_bytes());copied.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    save(ROOT/'archive_manifest.json',{'files':copied,'all_hashes_verified':True,'completed_entries_added':0})
    print('24 source/prose reviews:18 revisions,6 retentions.930 complete,957 source/prose;native/release/actual pending.',flush=True)


if __name__=='__main__':main()
