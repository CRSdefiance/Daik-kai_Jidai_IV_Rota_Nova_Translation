"""Source-led English review of24 independent SailHandling/Boarding battle comments."""
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.battle_survey_lookout_editorial import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.prepare_work_comments_v842 import reference
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/battle_sails_boarding_v944')
ROM=Path('out/all_routes_combined_v938_candidate.nds')
MANUSCRIPT=Path('translations/battle_sails_boarding_editorial_manuscript_v1.json')
IDS=tuple(range(1733,1757))
DATA='''1733|Offers to try using the wind to evade enemy shots.|I'll try using the wind to dodge enemy fire.|Restore the personal attempt instead of an impersonal order or guaranteed evasion.
1734|Will coordinate with the helmsman to evade cannon fire.|I'll coordinate with the helmsman to dodge the cannon fire.|Restore the personal cooperative action and object being evaded.
1735|Warns that panicking just because it is battle could cause a fall.|Don't panic just because we're in battle, or you'll fall!|Preserve the warning and falling risk from the mast;do not invent falling overboard or another accident.
1736|Calm sail handling should allow the speaker to evade any shot.|If I handle the sails calmly, I should be able to dodge any shot.|Preserve the condition and should expectation,not an unconditional dodge-every-shot command or mechanical invulnerability promise.
1737|Casually says they are heading windward and asks the admiral whether that is all right.|I'm heading windward. All right with you, Admiral?|Restore the personal action and explicit admiral being asked.
1738|Says fighting from windward gives an advantage.|Windward gives us an edge.|Retain the natural nautical shorthand for an advantage in this battle context.
1739|Fears that staying here could result in being hit.|If I stay up here, I could get hit!|Preserve the personal conditional risk,not a guaranteed hit.
1740|Says gaining the windward position is fundamental in naval battle.|Taking the windward position is fundamental in a sea battle.|Restore the naval-battle scope and natural expression for taking windward;not a rule for all seamanship.
1741|Rafael asks the helmsman to coordinate with his actions.|Helmsman, match my movements!|Retain the natural direct coordination request.
1742|Hodram orders the helmsman to coordinate with the masts as practiced in drills.|Helmsman, work with the mast crew, just as we practiced!|Masts is the established location for Sail Handlers in help125. Mast crew naturally expresses the source metonymy;restore cooperation and the practiced drill,not a generic mast-drill order.
1743|Lil screams at cannonballs flying immediately in front of her.|Eek! Cannonballs are flying right in front of me!|Restore the ongoing immediate danger and closeness instead of a completed past event.
1744|Maria orders the other helmsmen to coordinate with her too.|The other helmsmen need to follow my lead, too.|Restore other and too in the coordinated fleet context;no new appointment is implied.
1745|Politely asks the listener to see the results of regular training.|Let me show you how all that training has paid off.|Express the accumulated training and invitation naturally without inventing a victory already achieved.
1746|Says at last there is a chance to play an active part.|At last, time to shine.|Retain the natural opportunity idiom and anticipation.
1747|The speaker uses native IC first-person pronoun to promise to take the lead in hand-to-hand combat.|I'll lead the way in hand-to-hand combat!|Fifty current/clean native expansions prove IC is a first-person pronoun,not a name. Use complete ASCII I and preserve personal leadership during naval melee,not a guaranteed boarding result.
1748|Asks the admiral to count on the speaker and asks whether everyone is ready.|Admiral, you can count on me! Everyone ready?|Restore the personal assurance and explicit everyone in the readiness question.
1749|Roughly expresses eagerness to show skill in a naval battle.|A sea battle! I'm itching to show what I can do!|Localize ude ga naru as eagerness to exercise skill;the old blood-is-up wording changes the idiom into anger or bloodlust.
1750|The elderly veteran tells the listener to watch a veterans fighting.|Watch how a veteran fights.|Retain the natural confident instruction without inventing family address.
1751|Promises to excel and asks to be treated to a feast afterward.|I'll do great out there, so treat me to a feast afterward!|Restore the personal promise and direct request for a later treat;do not turn it into a guaranteed win or an earned reward.
1752|Politely addresses the sailors and asks whether they are ready.|All right, sailors. Are you ready?|Retain the natural respectful readiness question.
1753|Rafael promises personally to create an opening in hand-to-hand combat.|I'll make an opening for us in hand-to-hand combat!|Restore explicit I and creating a breakthrough in naval melee;the old boarding fragment loses both grammar and personal resolve.
1754|Hodram reasons that a duel is the only way to win with fewer casualties.|If we're to win with fewer casualties, it'll have to be a duel...|Preserve the personal tactical judgment and lower casualties,not a promise that no one will die or a universal engine rule.
1755|Lil asks the listener to trust her and follow her.|Trust me and follow my lead!|Restore a complete natural personal invitation to follow.
1756|Maria expects everyone to be ready and announces boarding.|Ready? We're boarding!|Retain the natural concise combat order and imminent action.'''
PROSE={}
for line in DATA.splitlines():
    n,meaning,english,note=line.split('|');n=int(n)
    PROSE[n]=(meaning,english,note,'retain' if n in (1738,1741,1746,1750,1752,1756) else 'revise')

def main():
    assert not MANUSCRIPT.exists();ROOT.mkdir(parents=True,exist_ok=True)
    packet_path=Path('work/analysis/battle_sails_boarding_v940/source_context_packet.json');packet=read(packet_path)
    ledger=read('translations/editorial_review_current_v1.json')
    assert ledger['records_editorially_completed']==1018 and ledger['records_with_source_and_prose_pass']==1021
    assert sha(ROM.read_bytes())==packet['candidate_sha256']==ledger['current_integrated_candidate']['sha256']
    assert len(packet['all150_original_battle_helper_main_and_ordinary_control_selections'])==150
    current,clean=map(NdsImage.open,(ROM,'work/clean.nds'))
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    en=current_entries(current.read_file('/COMMON/MESFILE.DK4'),current.read_file('/__arm9__.bin'))
    ordinary=[{'message_id':n,'source_Japanese':jp[n].text.decode('cp932'),'source_hex':jp[n].text.hex(),'source_reference':reference(jp[n]),'current_English':en[n].text.decode('cp932'),'current_text_hex':en[n].text.hex(),'current_reference':reference(en[n]),'already_reviewed_ordinary_context_no_new_credit':True} for n in range(1523,1547)]
    supplement=ROOT/'ordinary_context_and_terms.json'
    save(supplement,{'candidate_sha256':sha(ROM.read_bytes()),'source_clean_ROM_sha256':packet['source_clean_ROM_sha256'],'records':ordinary,
        'independent_alternatives_not_consecutive_dialogue':True,'established_term_documents':{p:sha(Path(p).read_bytes()) for p in ('translations/crew_help_manuscript_v1.json','translations/skill_terms_help_manuscript_v1.json','translations/character_name_localization_policy_v1.json')},
        'established_roles':{'SailHandling':0,'Boarding':7},
        'mast_crew_metonymy_supported_by_help125':True,
        'source_pronoun_proof':'work/analysis/battle_sails_boarding_v943/source_pronoun_proof.json',
        'source_pronoun_proof_sha256':sha(Path('work/analysis/battle_sails_boarding_v943/source_pronoun_proof.json').read_bytes()),
        'source1736_conditional_expected_evasion_not_invulnerability':True,
        'source1739_risk_not_guaranteed_hit':True,'source1754_personal_tactical_judgment_not_universal_duel_rule':True})
    pronouns=read('work/analysis/battle_sails_boarding_v943/source_pronoun_proof.json')
    assert pronouns['candidate_sha256']==sha(ROM.read_bytes()) and pronouns['IC_is_first_person_not_actor_name']
    assert len(pronouns['all25_current_and_clean_parser_control_cases'])==25
    assert all(len(case['variants'])==2 for case in pronouns['all25_current_and_clean_parser_control_cases'])
    sources={r['message_id']:r for r in packet['records_with_immediate_storage_neighbors']};rows=[]
    for n,(meaning,english,note,decision) in PROSE.items():
        s=sources[n];role,first=(0,1733) if n<1745 else (7,1745);index=n-first;hero=index-8 if index>=8 else None;voice=index if hero is None else None
        speaker=f'Native NPC voice class{voice}' if hero is None else ['Rafael','Hodram Joakim Bergstrom (genuine captain1)','Lil','Maria'][hero]
        assert english==' '.join(english.split()) and english.isascii() and not any(c in english for c in '%{}\n')
        if decision=='retain':assert english==s['current_English'].strip()
        rows.append({'id':f'COMMON_MESSAGE_{n}','message_id':n,'role_ID':role,'voice_class':voice,'protagonist_ID':hero,'speaker':speaker,
            'context':f'Independent activity0 battle working comment for SailHandling0 or Boarding7,selected role{role}. Original12600 selects eight NPC alternatives and12720 selects the four genuine protagonists. Main12104 uses original battle fields8/12=0/1. Storage neighbors are independently selected variants,not consecutive dialogue or the separate activity1 helper126A8. Flavor lines do not execute maneuvers,guarantee evasion or victory,or grant a later feast.',
            'source_Japanese':s['source_Japanese'],'source_hex':s['source_hex'],'source_reference':s['source_reference'],'canonical_source_hex':s['canonical_text_hex'],'current_reference':s['current_reference'],'current_text_hex':s['current_text_hex'],'current_English':s['current_English'],
            'source_meaning':meaning,'english':english,'localization_note':note,'editorial_decision':decision,'native_argument_count':0,'source_native_macros':['IC'] if n==1747 else [],'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False}})
    assert tuple(r['message_id'] for r in rows)==IDS and sum(r['editorial_decision']=='revise' for r in rows)==18
    save(MANUSCRIPT,{'format':'dk4-natural-dialogue-source-manuscript-v2','translation_policy':'natural-dialogue-v2','target_locale':'en-US','encoder':'dialogue-relocatable-v1','consumer_layout_profile':'deck-battle-sails-boarding-visible-v1','review_gates':['source','context','localization','naturalness'],'formatting_review_pending':True,'status':'24-source-prose-reviewed-native-format-integration-and-actual-pending','file_path':'/COMMON/MESFILE.DK4','source_clean_ROM_sha256':packet['source_clean_ROM_sha256'],'current_ROM':str(ROM),'current_ROM_sha256':sha(ROM.read_bytes()),'current_COMMON_sha256':packet['COMMON_sha256'],'current_ARM9_sha256':packet['ARM9_sha256'],'native_context_proof':str(packet_path),'native_context_proof_sha256':sha(packet_path.read_bytes()),'ordinary_context_supplement':str(supplement),'ordinary_context_supplement_sha256':sha(supplement.read_bytes()),'records':rows,'full_goal_complete':False})
    save(ROOT/'editorial_ledger_before_source_review.json',ledger)
    ledger['records_with_source_and_prose_pass']=ledger['records_with_source_prose_drafts']=1045
    ledger['source_prose_reviewed_counts_by_file']['/COMMON/MESFILE.DK4']=1044
    ledger['reviewed_but_incomplete_COMMON_IDs']=[750,751,752,*IDS]
    ledger['active_source_prose_drafts']={'native_message_IDs':[750,751,752,*IDS],'manuscripts':['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json',str(MANUSCRIPT)],'status':'three-older-context-unmapped-and24-battle-sails-boarding-source-prose-reviewed-format-release-pending','note':'These27 pending reviewed entries are not the full remaining shared/routes/player prose or raw-source scope.'}
    checkpoint='V944 source/prose-reviews24 battle SailHandling0/Boarding7 comments1733-1756:18 revisions and6 retentions. All150 original battle/main/ordinary controls and50 current/clean IC1747 expansions pass. Drafts restore personal wind/helm cooperation,conditional evasion and hit risk,mast-crew drill coordination,immediate danger,training demonstration,complete first-person melee leadership,eagerness to show skill,personal feast request,breakthrough and fewer-casualty duel judgment. Native layout,registered integration and actual scenes remain pending. V938 stays current;1018 complete,1045 source/prose reviewed. Remaining shared/routes/player prose/raw inventory,older750-752,mood1833,special1885-1888,abandon-caption0x134E54,separate graphics/all18 plaques,Samwell header and later older-record re-audit remain open;full goal active.'
    ledger['latest_checkpoint']=checkpoint
    ledger['battle_sails_boarding_v944']={'status':'source-prose-reviewed-native-release-and-actual-pending','native_message_IDs':list(IDS),'manuscript':str(MANUSCRIPT),'source_context_proof':str(packet_path),'proposed_revisions':18,'justified_retentions':6,'completed_entries_added':0}
    ledger['research_checkpoints'].append({'id':'V944-Battle-Sails-Boarding24-source-prose','proof':str(packet_path),'manuscript':str(MANUSCRIPT),'new_source_prose_reviews':24,'completed_entries_added':0,'previous_goal_turn_classification':'progress:24 Survey/Lookout entries completed in V938;four actual cases,exact patch and next24 source contexts verified','this_goal_turn_classification':'progress:24 faithful glosses,natural English decisions,50 source pronoun expansions,exact references and ordinary-context supplement','full_goal_complete':False})
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==1045
    save('translations/editorial_review_current_v1.json',ledger)
    doc=Path('docs/battle_sails_boarding_v944_source_review.md')
    with doc.open('x',encoding='utf-8') as f:f.write('# V944: battle SailHandling/Boarding source review\n\n'+checkpoint+'\n')
    for d in map(Path,('docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')):
        with d.open('a',encoding='utf-8') as f:f.write('\n\n## V944: battle SailHandling/Boarding source review\n\n'+checkpoint+' See [V944 source review](battle_sails_boarding_v944_source_review.md).\n')
    archive=Path('E:/Rota Nova translations/Editorial review/V944 Battle Sails Boarding source review');assert not archive.exists();copied=[]
    for source in (MANUSCRIPT,packet_path,supplement,Path(__file__),doc,Path('translations/editorial_review_current_v1.json')):
        target=archive/source.absolute().relative_to(Path.cwd());target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target);assert sha(source.read_bytes())==sha(target.read_bytes());copied.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    save(ROOT/'archive_manifest.json',{'files':copied,'all_hashes_verified':True,'completed_entries_added':0})
    print('24 source/prose reviews:18 revisions,6 retentions.1018 complete,1045 source/prose;native/release/actual pending.',flush=True)
if __name__=='__main__':main()
