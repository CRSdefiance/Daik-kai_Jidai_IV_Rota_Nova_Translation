"""Review the13 condition1 alternatives against original Japanese and native selection."""
from pathlib import Path
from shutil import copy2

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.battle_gunnery_deck_editorial import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/physical_fatigue_v959')
ROM=Path('out/all_routes_combined_v954_candidate.nds')
MANUSCRIPT=Path('translations/physical_fatigue_editorial_manuscript_v1.json')
IDS=tuple(range(1781,1794))
DATA='''1781|Politely reports a heavy,sluggish feeling in the body.|My body feels so heavy...|Retain the natural bodily heaviness description;this is subjective fatigue,not a diagnosis.
1782|Hesitantly wonders whether tiredness explains how the speaker feels.|Hmm... Maybe I'm tired...|Restore uncertainty in a personal spoken sentence;the old Just fatigue adds unwarranted minimization.
1783|The native first-person macro reports exhaustion and asks to be allowed to rest.|I'm exhausted... Let me rest...|Keep the fluent request and first person. Fifty original current/clean parser expansions prove IC is a pronoun,not a proper name. Replace the historical full-width I guard with ASCII only subject to complete native font and actual-scene proof.
1784|Says the speaker has become tired and trails off toward the Recreation Room.|I'm worn out... I need a break in the Recreation Room...|Use the established help112 room name and express the desired rest naturally. This speech does not move the officer,heal them or prove any completed reassignment.
1785|Roughly complains of lacking strength and wonders what has happened to the speaker.|I've got no strength left... What's wrong with me?|Restore the rough personal complaint and self-question without inventing a cause or diagnosis.
1786|An older voice says the speaker is tired and asks to rest briefly.|I'm tired... Let me rest for a bit...|Restore the personal request and chito brief-rest nuance in natural English;do not invent a family relationship or an exaggerated dialect.
1787|The informal first-person speaker says they have become completely exhausted.|I'm completely worn out...|Restore the explicit oira first-person subject while preserving the natural worn-out expression.
1788|Tentatively observes that fatigue seems to have accumulated.|The fatigue seems to be catching up with me...|Localize accumulated fatigue idiomatically and retain the tentative assessment rather than the old flat,clinical declaration.
1789|Rafael feels physically unwell and wonders whether he is tired.|I don't feel right... Maybe I'm tired...?|Restore the personal bodily unease and tentative question rather than declaring tiredness as a settled explanation.
1790|Hodram groans and reports dizziness.|Ugh... So dizzy...|Retain the natural weary fragment and dizziness;do not add a fall,injury or treatment.
1791|Lil emphasizes how very heavy and sluggish her body feels.|My whole body feels so heavy...|Retain the natural personal emphasis and heavy-body fatigue sensation.
1792|Maria stammers that she is all right and asks the listener not to worry.|I-I'm all right... Don't worry...|Place the stammer on the reassurance,where it occurs in Japanese;do not move it to the worry request or add still.
1793|Sera pauses and begins an unfinished first-person statement.|... I...|Preserve the hesitant pause and unfinished personal fragment. Do not invent an exhaustion diagnosis or complete her thought. Punctuation remains in one paragraph,with no leading blank line.'''
PROSE={}
for line in DATA.splitlines():
    n,meaning,english,note=line.split('|');n=int(n)
    PROSE[n]=(meaning,english,note,'retain' if n in (1781,1790,1791) else 'revise')


def main():
    assert not MANUSCRIPT.exists();ROOT.mkdir(parents=True,exist_ok=True)
    packet_path=Path('work/analysis/physical_fatigue_v957/source_context_packet.json');packet=read(packet_path)
    pronoun_path=Path('work/analysis/physical_fatigue_v958/source_pronoun_proof.json');pronoun=read(pronoun_path)
    ledger=read('translations/editorial_review_current_v1.json')
    assert ledger['records_editorially_completed']==1066 and ledger['records_with_source_and_prose_pass']==1069
    assert sha(ROM.read_bytes())==packet['candidate_sha256']==pronoun['candidate_sha256']==ledger['current_integrated_candidate']['sha256']
    assert len(packet['all75_original_direct_main_battle_and_ordinary_fatigue_selections'])==75
    assert len(packet['all25_healthy_direct_helper_no_message_controls'])==25
    assert packet['source_condition_ID']==1 and packet['Sera24_special_ID']==1793
    assert packet['job_role_and_mood_not_queried_in_physical_status_branch']
    assert pronoun['IC_is_first_person_not_actor_name'] and len(pronoun['all25_current_and_clean_parser_control_cases'])==25
    assert all(len(r['variants'])==2 for r in pronoun['all25_current_and_clean_parser_control_cases'])
    current,clean=map(NdsImage.open,(ROM,'work/clean.nds'))
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    en=current_entries(current.read_file('/COMMON/MESFILE.DK4'),current.read_file('/__arm9__.bin'))
    sources={r['message_id']:r for r in packet['records_with_immediate_storage_neighbors']}
    help112=next(r for r in read('translations/crew_help_manuscript_v1.json')['records'] if r['topic_id']==112)
    assert help112['heading']=='Recreation Room' and '娯楽室' in help112['source_Japanese_with_link_IDs']
    supplement=ROOT/'source_context_and_terms.json'
    save(supplement,{'candidate_sha256':sha(ROM.read_bytes()),'reference_help112':help112,
        'established_term_documents':{p:sha(Path(p).read_bytes()) for p in ('translations/crew_help_manuscript_v1.json','translations/character_name_localization_policy_v1.json')},
        'physical_condition1_precedes_mood_and_work_roles':True,'source_actor_byte6_not_an_inferred_medical_diagnosis':True,
        'storage_neighbors_are_independent_selections_not_consecutive_speech':True,
        'all13_source_IC_macros':[{'message_id':n,'IC_count':jp[n].text.count(b'IC')} for n in IDS],
        'source_pronoun_proof':str(pronoun_path),'source_pronoun_proof_sha256':sha(pronoun_path.read_bytes()),
        'prior_actual_Manuel_is_source_context_only_not_new_gameplay_credit':True,'neighbors_no_new_review_credit':[1780,1794]})
    rows=[]
    for n,(meaning,english,note,decision) in PROSE.items():
        s=sources[n];voice=n-1781 if n<1789 else None;hero=n-1789 if 1789<=n<=1792 else None;special=24 if n==1793 else None
        speaker=('Sera (native actor24 special response)' if special is not None else f'Native NPC voice class{voice}' if voice is not None else ['Rafael','Hodram Joakim Bergstrom (genuine captain1)','Lil','Maria'][hero])
        assert jp[n].text.hex()==s['source_hex'] and en[n].text.hex()==s['current_text_hex']
        assert english==' '.join(english.split()) and english.isascii() and not any(c in english for c in '%{}\n')
        if decision=='retain':assert english==s['current_English'].strip()
        rows.append({'id':f'COMMON_MESSAGE_{n}','message_id':n,'physical_condition_ID':1,
            'role_ID':2,'role_ID_is_CPU_layout_fixture_only_not_source_semantics':True,'voice_class':voice,'protagonist_ID':hero,'special_actor_ID':special,'speaker':speaker,
            'context':'Independent activity0 physical-condition1 fatigue response. Original main12104 checks actor byte6 before job,mood or battle working comments. Native1250C selects eight NPC voices,12584 selects four genuine protagonists,and12494 selects Sera24 special1793. Ordinary and battle source controls select the same fatigue message. Storage neighbors are independently selected variants,not a conversation. Role2 is an isolated formatting fixture only. Other physical conditions,wound and illness families remain outside this review.',
            'source_Japanese':s['source_Japanese'],'source_hex':s['source_hex'],'source_reference':s['source_reference'],
            'canonical_source_hex':s['canonical_text_hex'],'current_reference':s['current_reference'],'current_text_hex':s['current_text_hex'],'current_English':s['current_English'],
            'source_meaning':meaning,'english':english,'localization_note':note,'editorial_decision':decision,'native_argument_count':0,
            'source_native_macros':['IC'] if n==1783 else [],'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False}})
    assert tuple(r['message_id'] for r in rows)==IDS and sum(r['editorial_decision']=='revise' for r in rows)==10
    save(MANUSCRIPT,{'format':'dk4-natural-dialogue-source-manuscript-v2','translation_policy':'natural-dialogue-v2','target_locale':'en-US','encoder':'dialogue-relocatable-v1',
        'consumer_layout_profile':'deck-physical-fatigue-visible-v1','review_gates':['source','context','localization','naturalness'],'formatting_review_pending':True,
        'status':'13-source-prose-reviewed-native-format-integration-and-actual-pending','file_path':'/COMMON/MESFILE.DK4',
        'source_clean_ROM_sha256':packet['source_clean_ROM_sha256'],'current_ROM':str(ROM),'current_ROM_sha256':sha(ROM.read_bytes()),
        'current_COMMON_sha256':packet['COMMON_sha256'],'current_ARM9_sha256':packet['ARM9_sha256'],
        'native_context_proof':str(packet_path),'native_context_proof_sha256':sha(packet_path.read_bytes()),
        'source_context_supplement':str(supplement),'source_context_supplement_sha256':sha(supplement.read_bytes()),'records':rows,'full_goal_complete':False})
    save(ROOT/'editorial_ledger_before_source_review.json',ledger)
    ledger['records_with_source_and_prose_pass']=ledger['records_with_source_prose_drafts']=1082
    ledger['source_prose_reviewed_counts_by_file']['/COMMON/MESFILE.DK4']=1081
    ledger['reviewed_but_incomplete_COMMON_IDs']=[750,751,752,*IDS]
    ledger['active_source_prose_drafts']={'native_message_IDs':[750,751,752,*IDS],'manuscripts':['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json',str(MANUSCRIPT)],
        'status':'three-older-context-unmapped-and13-physical-fatigue-source-prose-reviewed-format-release-pending',
        'note':'These16 pending reviewed entries are not the full remaining shared/routes/player prose or raw-source scope.'}
    checkpoint='V959 source/prose-reviews13 physical-condition1 fatigue comments1781-1793:10 revisions and3 retentions. All75 original direct/main battle/ordinary selections,25 healthy no-message controls and50 current/clean first-person expansions pass. Drafts restore tentative personal fatigue,Recreation Room rest,rough self-question,brief-rest request,accumulated fatigue,Rafaels question,Marias reassurance stammer and Seras unfinished first-person fragment. Native layout,registered integration and actual scenes remain pending. V954 stays current;1066 complete,1082 source/prose reviewed. Older750-752,mood1833,special1885-1888,abandon-caption0x134E54,other physical states,remaining shared/routes/player prose/raw inventory,separate graphics/all18 plaques,Samwell header and later older-record re-audit remain open;full goal active.'
    ledger['latest_checkpoint']=checkpoint
    ledger['physical_fatigue_v959']={'status':'source-prose-reviewed-native-release-and-actual-pending','native_message_IDs':list(IDS),'manuscript':str(MANUSCRIPT),
        'source_context_proof':str(packet_path),'source_pronoun_proof':str(pronoun_path),'proposed_revisions':10,'justified_retentions':3,'completed_entries_added':0}
    ledger['research_checkpoints'].append({'id':'V959-Physical-Fatigue13-source-prose','proof':str(packet_path),'manuscript':str(MANUSCRIPT),'new_source_prose_reviews':13,'completed_entries_added':0,
        'previous_goal_turn_classification':'progress:current V954 exact user screenshot repair676/677 and earlier targeted actual capture verified;fatigue source context mapped',
        'this_goal_turn_classification':'progress:13 faithful source glosses,natural English decisions,source-specific50 first-person parser controls,exact source references and Recreation Room terminology',
        'full_goal_complete':False})
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==1082
    save('translations/editorial_review_current_v1.json',ledger)
    doc=Path('docs/physical_fatigue_v959_source_review.md')
    with doc.open('x',encoding='utf-8') as f:f.write('# V959: physical fatigue source review\n\n'+checkpoint+'\n')
    for d in map(Path,('docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')):
        with d.open('a',encoding='utf-8') as f:f.write('\n\n## V959: physical fatigue source review\n\n'+checkpoint+' See [V959 source review](physical_fatigue_v959_source_review.md).\n')
    archive=Path('E:/Rota Nova translations/Editorial review/V959 Physical Fatigue source review');assert not archive.exists();copied=[]
    for source in (MANUSCRIPT,packet_path,pronoun_path,supplement,Path(__file__),Path('scripts/probe_physical_fatigue_pronoun_v958.py'),doc,Path('translations/editorial_review_current_v1.json')):
        target=archive/source.absolute().relative_to(Path.cwd());target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target)
        assert sha(source.read_bytes())==sha(target.read_bytes());copied.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    save(ROOT/'archive_manifest.json',{'files':copied,'all_hashes_verified':True,'completed_entries_added':0})
    print('13 source/prose reviews:10 revisions,3 retentions.1066 complete,1082 source/prose;native/release/actual pending.',flush=True)


if __name__=='__main__':main()
