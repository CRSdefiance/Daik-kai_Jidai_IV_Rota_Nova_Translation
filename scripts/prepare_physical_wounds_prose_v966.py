"""Source-led English review of13 independently selected wound comments."""
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.physical_fatigue_editorial import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/physical_wounds_v966')
ROM=Path('out/all_routes_combined_v962_candidate.nds')
MANUSCRIPT=Path('translations/physical_wounds_editorial_manuscript_v1.json')
IDS=tuple(range(1794,1807))
DATA='''1794|Dismisses a wound of this extent and insists the speaker is still all right.|It's only a small wound... I'm still all right!|Restore the personal reassurance and the speaker's dismissive assessment of the wound;the old Still all right has no subject. This is the officer's claim,not an independently verified injury grade.
1795|Groans and dismissively trails off about a mere wound.|Gah... It's only a wound...|Keep the strained groan and dismissive hesitation in natural English. The final ellipsis preserves the unfinished thought;do not invent a recovery or a promised action.
1796|Reassures the listener and trails off that the wound is not serious.|I'm all right... It's not a serious wound...|Restore the omitted reassurance and the wound's stated lack of seriousness;retain the trailing hesitation rather than replacing the whole line with Only a scratch.
1797|Questions the wound,reassures the listener,and begins an unfinished first-person statement about still being able to continue.|A wound...? I'm all right... I can still...|Restore the personal unfinished clause. I can still is an idiomatic English lead-in for this faltering reassurance;leave its action unspoken,as in Japanese.
1798|Roughly boasts that applying spit will heal a wound like this.|A wound like this? Spit on it and it'll heal!|Restore the explicit dismissive wound reference and rough confident salesmanship. Retain the character's spit remedy as dialogue,without turning it into a measured treatment mechanic.
1799|The older speaker admits being in difficulty and trails off about strength limited by this wound.|I'm in a bad way... This wound's sapping my strength...|Restore the personal difficulty and the wound's effect on the speaker's strength. The natural sapping phrase conveys the implied weakness without inventing its severity or treatment.
1800|The informal first-person speaker says they have been hurt.|I got hurt...|Restore oira as a complete personal sentence and remove the old added Ow,which has no counterpart in the source.
1801|Politely observes that the wound prevents the speaker from showing their full ability.|This wound is holding me back...|Retain the natural idiomatic description of impaired performance,including the wound and personal limitation.
1802|Rafael says the bleeding will not stop,but begins an unfinished statement of personal resolve.|The bleeding won't stop... But I...|Restore the omitted first-person But I clause while leaving his intended action unfinished. Do not invent a vow,treatment or completed recovery.
1803|Hodram confidently rejects the idea that a wound this slight could bring him down.|A scratch won't stop me.|Retain the fluent confident localization. Scratch conveys his dismissive appraisal of this slight wound,and won't stop me preserves the rhetorical refusal to be brought down.
1804|Lil admits pain but reassures herself because she is the admiral.|It hurts, but I'm the admiral. I can take it.|Restore her personal pain and admiral's responsibility;the old generic maxim about what an admiral can endure loses her voice.
1805|Maria dismisses a wound of this extent and tells the listener not to worry.|Don't worry about a little wound like this.|Use natural American worry about and preserve the speaker's dismissive this-wound reference without requiring it to be literally a scratch.
1806|Sera says there is no need to worry and that the wound is not serious.|Don't worry. It's not a serious wound...|Repair the old No worry grammar while keeping Sera's brief reassurance and lack-of-seriousness claim. Do not impose caricatured broken English or invent a treatment.'''
PROSE={}
for line in DATA.splitlines():
    n,meaning,english,note=line.split('|');n=int(n)
    PROSE[n]=(meaning,english,note,'retain' if n in (1801,1803) else 'revise')


def main():
    assert not MANUSCRIPT.exists();ROOT.mkdir(parents=True,exist_ok=True)
    packet_path=Path('work/analysis/physical_wounds_v965/source_context_packet.json');packet=read(packet_path)
    ledger=read('translations/editorial_review_current_v1.json')
    assert ledger['records_editorially_completed']==1079 and ledger['records_with_source_and_prose_pass']==1082
    assert sha(ROM.read_bytes())==packet['candidate_sha256']==ledger['current_integrated_candidate']['sha256']
    assert packet['source_condition_IDs']==[2,3] and packet['Sera24_special_ID']==1806
    assert len(packet['all150_original_direct_main_battle_and_ordinary_wound_selections'])==150
    assert len(packet['all25_healthy_direct_helper_no_message_controls'])==len(packet['all25_condition1_prior_fatigue_discriminating_controls'])==25
    current,clean=map(NdsImage.open,(ROM,'work/clean.nds'))
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    en=current_entries(current.read_file('/COMMON/MESFILE.DK4'),current.read_file('/__arm9__.bin'))
    sources={r['message_id']:r for r in packet['records_with_immediate_storage_neighbors']}
    supplement=ROOT/'source_context_and_terms.json'
    save(supplement,{'candidate_sha256':sha(ROM.read_bytes()),'established_term_documents':{'translations/character_name_localization_policy_v1.json':sha(Path('translations/character_name_localization_policy_v1.json').read_bytes())},
        'source_condition2_and3_share_these_dialogue_alternatives':True,'other_condition_effects_not_claimed_identical':True,
        'physical_status_precedes_job_mood_and_battle_work':True,'independent_alternatives_not_consecutive_dialogue':True,
        'all13_source_IC_macros':[{'message_id':n,'IC_count':jp[n].text.count(b'IC')} for n in IDS],
        'no_IC_native_macro_in_selected_Japanese':all(b'IC' not in jp[n].text for n in IDS),
        'literal_Japanese_first_person_preserved_as_natural_English':True,'source1802_But_I_and1797_unfinished_clause_preserved':True,
        'source1804_personal_pain_and_admiral_responsibility_preserved':True,'source1798_spit_remedy_is_character_speech':True,
        'neighbors_no_new_review_credit':[1793,1807]})
    rows=[]
    for n,(meaning,english,note,decision) in PROSE.items():
        s=sources[n];voice=n-1794 if n<1802 else None;hero=n-1802 if 1802<=n<=1805 else None;special=24 if n==1806 else None
        speaker='Sera (native actor24 special response)' if special is not None else f'Native NPC voice class{voice}' if voice is not None else ['Rafael','Hodram Joakim Bergstrom (genuine captain1)','Lil','Maria'][hero]
        assert jp[n].text.hex()==s['source_hex'] and en[n].text.hex()==s['current_text_hex']
        assert english==' '.join(english.split()) and english.isascii() and not any(c in english for c in '%{}\n')
        if decision=='retain':assert english==s['current_English'].strip()
        rows.append({'id':f'COMMON_MESSAGE_{n}','message_id':n,'physical_condition_IDs':[2,3],'role_ID':2,
            'role_ID_is_CPU_layout_fixture_only_not_source_semantics':True,'voice_class':voice,'protagonist_ID':hero,'special_actor_ID':special,'speaker':speaker,
            'context':'Independent activity0 wound response for original actor conditions2 or3. Main12104 checks physical state before job,mood or battle working comments. Original1250C selects eight NPC voices,12584 the four genuine protagonists,and12494 Sera24 special1806. Both conditions and ordinary/battle controls select this family;their other effects need separate evidence. Neighbors are independent alternatives,not a conversation. Role2 is a CPU formatting fixture only. Reassurance and remedies are character speech;the dialogue does not execute recovery or assert a clinical injury grade.',
            'source_Japanese':s['source_Japanese'],'source_hex':s['source_hex'],'source_reference':s['source_reference'],
            'canonical_source_hex':s['canonical_text_hex'],'current_reference':s['current_reference'],'current_text_hex':s['current_text_hex'],'current_English':s['current_English'],
            'source_meaning':meaning,'english':english,'localization_note':note,'editorial_decision':decision,'native_argument_count':0,'source_native_macros':[],
            'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False}})
    assert tuple(r['message_id'] for r in rows)==IDS and sum(r['editorial_decision']=='revise' for r in rows)==11
    save(MANUSCRIPT,{'format':'dk4-natural-dialogue-source-manuscript-v2','translation_policy':'natural-dialogue-v2','target_locale':'en-US','encoder':'dialogue-relocatable-v1',
        'consumer_layout_profile':'deck-physical-wounds-visible-v1','review_gates':['source','context','localization','naturalness'],'formatting_review_pending':True,
        'status':'13-source-prose-reviewed-native-format-integration-and-actual-pending','file_path':'/COMMON/MESFILE.DK4',
        'source_clean_ROM_sha256':packet['source_clean_ROM_sha256'],'current_ROM':str(ROM),'current_ROM_sha256':sha(ROM.read_bytes()),
        'current_COMMON_sha256':packet['COMMON_sha256'],'current_ARM9_sha256':packet['ARM9_sha256'],
        'native_context_proof':str(packet_path),'native_context_proof_sha256':sha(packet_path.read_bytes()),'source_context_supplement':str(supplement),
        'source_context_supplement_sha256':sha(supplement.read_bytes()),'records':rows,'full_goal_complete':False})
    save(ROOT/'editorial_ledger_before_source_review.json',ledger)
    ledger['records_with_source_and_prose_pass']=ledger['records_with_source_prose_drafts']=1095
    ledger['source_prose_reviewed_counts_by_file']['/COMMON/MESFILE.DK4']=1094
    ledger['reviewed_but_incomplete_COMMON_IDs']=[750,751,752,*IDS]
    ledger['active_source_prose_drafts']={'native_message_IDs':[750,751,752,*IDS],'manuscripts':['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json',str(MANUSCRIPT)],
        'status':'three-older-context-unmapped-and13-physical-wounds-source-prose-reviewed-format-release-pending',
        'note':'These16 pending reviewed entries are not the full remaining shared/routes/player prose or raw-source scope.'}
    checkpoint='V966 source/prose-reviews13 wound comments1794-1806 for original conditions2/3:11 revisions and2 retentions. All150 original direct/main battle/ordinary selections,25 healthy and25 prior-fatigue discriminating controls pass. Drafts restore personal reassurance,unfinished resolve,Rafaels bleeding and But I,Lils pain and admiral responsibility,and Seras natural brief reassurance. Native layout,registered integration and actual scenes remain pending. V962 stays current;1079 complete,1095 source/prose reviewed. Other physical states,older750-752,mood1833,special1885-1888,abandon-caption0x134E54,remaining shared/routes/player prose/raw coverage,separate graphics/all18 plaques,Samwell header and later older-record re-audit remain open;full goal active.'
    ledger['latest_checkpoint']=checkpoint
    ledger['physical_wounds_v966']={'status':'source-prose-reviewed-native-release-and-actual-pending','native_message_IDs':list(IDS),'manuscript':str(MANUSCRIPT),
        'source_context_proof':str(packet_path),'proposed_revisions':11,'justified_retentions':2,'completed_entries_added':0}
    ledger['research_checkpoints'].append({'id':'V966-Physical-Wounds13-source-prose','proof':str(packet_path),'manuscript':str(MANUSCRIPT),'new_source_prose_reviews':13,'completed_entries_added':0,
        'previous_goal_turn_classification':'progress:13 fatigue messages completed in V962,26 native fonts,four actual scenes/returns,exact patch and next13 wound source contexts verified',
        'this_goal_turn_classification':'progress:13 faithful glosses,natural English decisions,exact source references,200 original selector controls and restored personal/unfinished clauses','full_goal_complete':False})
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==1095
    save('translations/editorial_review_current_v1.json',ledger)
    doc=Path('docs/physical_wounds_v966_source_review.md')
    with doc.open('x',encoding='utf-8') as f:f.write('# V966: physical wound source review\n\n'+checkpoint+'\n')
    for d in map(Path,('docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')):
        with d.open('a',encoding='utf-8') as f:f.write('\n\n## V966: physical wound source review\n\n'+checkpoint+' See [V966 source review](physical_wounds_v966_source_review.md).\n')
    archive=Path('E:/Rota Nova translations/Editorial review/V966 Physical Wounds source review');assert not archive.exists();copied=[]
    for source in (MANUSCRIPT,packet_path,supplement,Path(__file__),doc,Path('translations/editorial_review_current_v1.json')):
        target=archive/source.absolute().relative_to(Path.cwd());target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target)
        assert sha(source.read_bytes())==sha(target.read_bytes());copied.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    save(ROOT/'archive_manifest.json',{'files':copied,'all_hashes_verified':True,'completed_entries_added':0})
    print('13 source/prose reviews:11 revisions,2 retentions.1079 complete,1095 source/prose;native/release/actual pending.',flush=True)


if __name__=='__main__':main()
