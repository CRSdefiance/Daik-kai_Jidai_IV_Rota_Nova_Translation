"""Source-led natural-English review of12 independent battle Finance comments."""

from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.battle_chapel_planning_editorial import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.prepare_work_comments_v842 import reference
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_finance_v919')
ROM=Path('out/all_routes_combined_v916_candidate.nds')
MANUSCRIPT=Path('translations/battle_finance_editorial_manuscript_v1.json')
IDS=tuple(range(1669,1681))
PROSE={
1669:('Wonders what a purser should do during a naval battle.',
      'What should a purser do in a sea battle...?',
      'Restore the naval-battle context and the question about what to do,rather than a detached general ability question.','revise'),
1670:('Considers working on the financial report while there is a chance.',
      'I might as well work on the financial report while I have the chance...',
      'Restore the actual report,the personal tentative intention,and making use of the available time. Do not add a monthly or annual reporting period absent from this line.','revise'),
1671:('Reflects that a purser has nothing to do in a naval battle.',
      'A purser has nothing to do in a sea battle...',
      'Restore the limited naval-combat scope. The old at sea incorrectly implies that the purser has no role throughout ordinary sailing.','revise'),
1672:('Wishes it were possible to haggle while fighting.',
      'I wish I could haggle and fight at the same time...',
      'Restore the personal wish and simultaneous actions. This is a fanciful purser comment,not a claim that the game allows combat haggling.','revise'),
1673:('Roughly observes that one cannot haggle during a naval battle.',
      "You can't haggle in a sea battle, can you...?",
      'Restore the naval-battle context and the casual reflective question. Keep the rough voice natural without adding an invented expletive.','revise'),
1674:('Muses over this months profits,then is startled by a loud roaring noise.',
      "This month's profits... Whoa! What's that racket?!",
      'Restore this month and the interruption of the financial thought. Racket gives the startled old-fashioned voice a natural reaction to the deafening battle noise;no actual profit or damage value is reported.','revise'),
1675:('Says the speaker also wants to fight,but trails off.',
      'I want to fight, too...',
      'Restore first-person oira and the hesitant wish to join in. Preserve the trailing thought rather than adding an order or reassignment.','revise'),
1676:('Politely says the speaker cannot play an active part from this room during a naval battle.',
      "I can't do much here during a sea battle.",
      'Restore the personal modest reflection,the room location and naval-combat scope. Do not deny the pursers usefulness during all sailing.','revise'),
1677:('Rafael reflects that a purser is powerless in battle.',
      'A purser is helpless in battle...',
      'Restore battle as the source context instead of generic now. This is a reflection on his current assigned role,not an engine rule that the character can never fight.','revise'),
1678:('Hodram firmly says this is no time to calculate profits.',
      'No time to calculate profits!',
      'Retain the natural forceful exclamation and source urgency;the situation supplies the time reference.','retain'),
1679:('Lil complains about what she is supposed to do in the pursers office.',
      "What am I supposed to do in the Purser's Office?!",
      'Restore the personal complaint and explicit room. Purser\'s Office is the established help label for shukei shitsu;the old generic one/this office loses her voice and the reference.','revise'),
1680:('Maria says she cannot give everyone directions from here.',
      "I can't give the crew orders from here!",
      'Restore the personal speaker and the people receiving her orders. In this naval-battle room context everyone is the ships company;do not turn the line into a general inability to command anywhere.','revise')}


def main():
    assert not MANUSCRIPT.exists();ROOT.mkdir(parents=True,exist_ok=True)
    packet_path=Path('work/analysis/battle_finance_v918/source_context_packet.json');packet=read(packet_path)
    ledger=read('translations/editorial_review_current_v1.json')
    assert ledger['records_editorially_completed']==954 and ledger['records_with_source_and_prose_pass']==957
    assert sha(ROM.read_bytes())==packet['candidate_sha256']==ledger['current_integrated_candidate']['sha256']
    assert len(packet['all75_original_battle_helper_main_and_ordinary_control_selections'])==75
    current,clean=map(NdsImage.open,(ROM,'work/clean.nds'))
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    en=current_entries(current.read_file('/COMMON/MESFILE.DK4'),current.read_file('/__arm9__.bin'))
    ordinary=[]
    for n in range(1459,1471):
        ordinary.append({'message_id':n,'source_Japanese':jp[n].text.decode('cp932'),'source_hex':jp[n].text.hex(),
            'source_reference':reference(jp[n]),'current_English':en[n].text.decode('cp932'),
            'current_text_hex':en[n].text.hex(),'current_reference':reference(en[n]),
            'already_reviewed_ordinary_context_no_new_credit':True})
    supplement=ROOT/'ordinary_context_and_terms.json'
    save(supplement,{'candidate_sha256':sha(ROM.read_bytes()),'source_clean_ROM_sha256':packet['source_clean_ROM_sha256'],
        'records':ordinary,'independent_alternatives_not_consecutive_dialogue':True,
        'established_term_documents':{p:sha(Path(p).read_bytes()) for p in ('translations/crew_help_manuscript_v1.json','translations/skill_terms_help_manuscript_v1.json','translations/character_name_localization_policy_v1.json')},
        'established_room_term':{'主計室':"Purser's Office"},'financial_report1670_has_no_invented_reporting_period':True,
        'explicit_this_month1674_preserved':True,'sea_battle_not_all_sailing_scope1671_1676_preserved':True})
    sources={r['message_id']:r for r in packet['records_with_immediate_storage_neighbors']};rows=[]
    for n,(meaning,english,note,decision) in PROSE.items():
        s=sources[n];index=n-1669;hero=index-8 if index>=8 else None;voice=index if hero is None else None
        speaker=f'Native NPC voice class{voice}' if hero is None else ['Rafael','Hodram Joakim Bergstrom (genuine captain1)','Lil','Maria'][hero]
        assert english==' '.join(english.split()) and english.isascii() and not any(c in english for c in '%{}\n')
        if decision=='retain':assert english==s['current_English'].strip()
        rows.append({'id':f'COMMON_MESSAGE_{n}','message_id':n,'role_ID':20,'voice_class':voice,'protagonist_ID':hero,'speaker':speaker,
            'context':'Independent battle Finance20 working comment. Original12600 selects eight NPC alternatives and12720 selects the genuine captain. Main12104 state0 uses original battle fields8/12=0/1 for eligible working responses. Storage neighbors are independently selected alternatives,not consecutive speech. These financial musings and combat complaints do not calculate or credit profits,issue orders or change assignment.',
            'source_Japanese':s['source_Japanese'],'source_hex':s['source_hex'],'source_reference':s['source_reference'],
            'canonical_source_hex':s['canonical_text_hex'],'current_reference':s['current_reference'],
            'current_text_hex':s['current_text_hex'],'current_English':s['current_English'],
            'source_meaning':meaning,'english':english,'localization_note':note,'editorial_decision':decision,
            'native_argument_count':0,'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False}})
    assert tuple(r['message_id'] for r in rows)==IDS and sum(r['editorial_decision']=='revise' for r in rows)==11
    save(MANUSCRIPT,{'format':'dk4-natural-dialogue-source-manuscript-v2','translation_policy':'natural-dialogue-v2','target_locale':'en-US',
        'encoder':'dialogue-relocatable-v1','consumer_layout_profile':'deck-battle-finance-visible-v1',
        'review_gates':['source','context','localization','naturalness'],'formatting_review_pending':True,
        'status':'12-source-prose-reviewed-native-format-integration-and-actual-pending','file_path':'/COMMON/MESFILE.DK4',
        'source_clean_ROM_sha256':packet['source_clean_ROM_sha256'],'current_ROM':str(ROM),'current_ROM_sha256':sha(ROM.read_bytes()),
        'current_COMMON_sha256':packet['COMMON_sha256'],'current_ARM9_sha256':packet['ARM9_sha256'],
        'native_context_proof':str(packet_path),'native_context_proof_sha256':sha(packet_path.read_bytes()),
        'ordinary_context_supplement':str(supplement),'ordinary_context_supplement_sha256':sha(supplement.read_bytes()),
        'records':rows,'full_goal_complete':False})
    save(ROOT/'editorial_ledger_before_source_review.json',ledger)
    ledger['records_with_source_and_prose_pass']=ledger['records_with_source_prose_drafts']=969
    ledger['source_prose_reviewed_counts_by_file']['/COMMON/MESFILE.DK4']=968
    ledger['reviewed_but_incomplete_COMMON_IDs']=[750,751,752,*IDS]
    ledger['active_source_prose_drafts']={'native_message_IDs':[750,751,752,*IDS],
        'manuscripts':['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json',str(MANUSCRIPT)],
        'status':'three-older-context-unmapped-and12-battle-finance-source-prose-reviewed-format-release-pending',
        'note':'These15 pending reviewed entries are not the full remaining shared/routes/player prose or raw-source scope.'}
    checkpoint=('V919 source/prose-reviews12 battle Finance20 comments1669-1680:11 revisions and1 retention. '
        'All75 original battle-helper/main/ordinary controls pass. Drafts restore the financial report,available time,this months profits,simultaneous haggling/fighting,personal wishes,the Purser\'s Office,and the crew receiving Marias orders. Naval battle is distinguished from all sailing. '
        'Native layout,registered integration and actual scenes remain pending. V916 stays current;954 complete,969 source/prose reviewed. '
        'Older750-752,mood1833,special actors1885-1888,raw abandon-caption0x134E54,remaining shared/routes/player prose/raw inventory,separate graphics/all18 plaques,Samwell header and later older-record re-audit remain open;full goal active.')
    ledger['latest_checkpoint']=checkpoint
    ledger['battle_finance_v919']={'status':'source-prose-reviewed-native-release-and-actual-pending','native_message_IDs':list(IDS),
        'manuscript':str(MANUSCRIPT),'source_context_proof':str(packet_path),'proposed_revisions':11,'justified_retentions':1,'completed_entries_added':0}
    ledger['research_checkpoints'].append({'id':'V919-Battle-Finance12-source-prose','proof':str(packet_path),'manuscript':str(MANUSCRIPT),
        'new_source_prose_reviews':12,'completed_entries_added':0,
        'previous_goal_turn_classification':'progress:24 Chapel/Planning entries completed in V916 and next12 Finance contexts mapped',
        'this_goal_turn_classification':'progress:12 faithful glosses,natural English decisions,exact references and ordinary-context/terminology supplement',
        'full_goal_complete':False})
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==969
    save('translations/editorial_review_current_v1.json',ledger)
    doc=Path('docs/battle_finance_v919_source_review.md')
    with doc.open('x',encoding='utf-8') as f:f.write('# V919: battle Finance source review\n\n'+checkpoint+'\n')
    for d in map(Path,('docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')):
        with d.open('a',encoding='utf-8') as f:f.write('\n\n## V919: battle Finance source review\n\n'+checkpoint+' See [V919 source review](battle_finance_v919_source_review.md).\n')
    archive=Path('E:/Rota Nova translations/Editorial review/V919 Battle Finance source review');assert not archive.exists();copied=[]
    for source in (MANUSCRIPT,packet_path,supplement,Path(__file__),doc,Path('translations/editorial_review_current_v1.json')):
        target=archive/source.absolute().relative_to(Path.cwd());target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target)
        assert sha(source.read_bytes())==sha(target.read_bytes());copied.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    save(ROOT/'archive_manifest.json',{'files':copied,'all_hashes_verified':True,'completed_entries_added':0})
    print('12 source/prose reviews:11 revisions,1 retention.954 complete,969 source/prose;native/release/actual pending.',flush=True)


if __name__=='__main__':main()
