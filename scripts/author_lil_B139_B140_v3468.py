"""Author67 contextual reviews with individual retention/revision findings."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.lil_B139_B140_map_polder_prose_v3468 import SPEECH
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B139_B140_author_v3468')
SOURCE=Path('work/analysis/lil_remaining_B139_B140_source_v3456/next67_B139_B140_clean_current_context.json')
COMPARISON=Path('work/analysis/lil_B139_B140_comparison_v3467/all67_current_effective_comparison_packet.json')
CONTEXT=Path('work/analysis/lil_B139_B140_clean_context_v3465/all67_complete_clean_context_and_fresh_glosses.json')
CONTROL=Path('work/analysis/lil_B139_B140_controls_v3464/all67_dispatches12_predicates1_query_and_C200_contract.json')
VOICE=Path('work/analysis/lil_B139_B140_voices_v3460/current_seven_static_names_voices_and207_catalog_rebind.json')
TERMS=Path('work/analysis/lil_B139_B140_terms_v3466/clean_current_items_polder_names_entries_and_copy_census.json')
BRANCH=Path('work/analysis/lil_B139_B140_branches_v3463b/original_relative_skip_operand_proof.json')
PROSE=Path('scripts/lil_B139_B140_map_polder_prose_v3468.py')
OUT=Path('translations/lil_B139_B140_editorial_manuscript_v1.json')
if __name__=='__main__':
    assert not ROOT.exists() and not OUT.exists();source,comparison,context,control,voice,terms=map(read,[SOURCE,COMPARISON,CONTEXT,CONTROL,VOICE,TERMS])
    assert context['all67_complete_clean_source_objects_read_before_older_English_comparison'] and context['all67_fresh_source_glosses_precede_localized_English'] and len(comparison['records'])==67 and comparison['registered_runtime_catalog_replacement_count']==1
    assert len(control['speech_dispatch_cases'])==134 and len(control['current_original_predicate_cases'])==13 and not source['typed_choice_records']
    assert {(r['block'],r['source_record_index']) for r in source['records']}==set(SPEECH)
    for d in [comparison,control,terms,voice]:assert d['source_context_sha256']==sha(SOURCE.read_bytes())
    gloss={r['id']:r for r in context['records']};speakers={2:'Lil Argot',4:'Janus',9:'Camille',16:'Gerhard',20:'Fernando',21:'Ian',171:'Research Student;unnamed'};rows=[]
    for original in comparison['records']:
        r=deepcopy(original);body,note=SPEECH[r['block'],r['source_record_index']]
        assert body==body.strip() and '  ' not in body and '\n' not in body and all(32<=ord(c)<127 for c in body) and not any(tag in body for tag in ['{LB','{ALIGN','{PAD','{SPEAKER:'])
        for m in ['FI','FA','FO']:assert bytes.fromhex(r['source_hex']).count(m.encode())==body.count('{MACRO:'+m+'}')
        old=r['current_effective_paragraph']
        for m in ['FI','FA','FO']:old=old.replace(m,'{MACRO:'+m+'}')
        decision='retain-wording' if body==old else 'revise'
        r.update(source_meaning=gloss[r['id']]['fresh_source_gloss'],english='{SPEAKER:'+format(r['source_selector'],'02X')+'}'+body,localization_note=note,editorial_decision=decision,current_stored_English=r['current_raw_storage_English'],effective_predecessor_paragraph=old,comparison_basis='Exact current native template,NFKC presentation forms andcollapsed legacy whitespace;raw/effective/catalogue provenance separate.',review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),speaker=speakers[r['source_selector']],context='Whole clean exchange andfresh glosses precede older-English comparison. '+context['complete_exchanges'][str(r['block'])]+' All seven static actors,Lil-context FI7,twelve predicates,query129 andC200 source-owned UI request are bound;no selected gameplay or earned progress claimed.',prose_author_module=str(PROSE),prose_author_module_sha256=sha(PROSE.read_bytes()),status='source-context-localization-naturalness-reviewed;native-format-references-representative-release-pending',editorial_older_English_comparison_pending=False,full_clean_context_precedes_comparison=True,current_complete_native_display_pending=True,source_kind=r['kind'],current_macro_dispatch_bound=True,original_native_display_consumer='original_progressive_54020')
        if decision=='retain-wording':r['fresh_retained_wording_justification']=note
        rows.append(r)
    counts=Counter(r['editorial_decision'] for r in rows)
    doc=dict(format='dk4-editorial-source-prose-draft-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],file_path='/data/SC2.DK4',current_ROM=source['current_ROM'],current_ROM_sha256=source['current_ROM_sha256'],source_ROM_sha256=source['source_ROM_sha256'],required_runtime_ARM9_sha256=source['current_ARM9_sha256'],records=rows,manuscript_kind='speech',prose_companions=[],revised=counts['revise'],retained=counts['retain-wording'],fresh_source_glosses_precede_current_comparison_and_localized_English=True,broad_Proof_terminology_editorial_consistency_lead_still_open=True,source_prose_or_completion_credit_added=0,formatting_review_pending=True,status=rows[0]['status'])
    for key,path in [('source_context',SOURCE),('control_contract',CONTROL),('whole_exchange_context_notes',CONTEXT),('branch_proof',BRANCH),('item_terminology_reconciliation',TERMS),('actor_voice_contract',VOICE),('effective_current_comparison',COMPARISON)]:doc[key]=str(path);doc[key+'_sha256']=sha(path.read_bytes())
    assert len(rows)==67 and counts['revise']+counts['retain-wording']==67;ROOT.mkdir(parents=True);save(OUT,doc)
    save(ROOT/'all67_contextual_prose_or_retention_receipt.json',dict(manuscript=str(OUT),manuscript_sha256=sha(OUT.read_bytes()),evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,COMPARISON,CONTEXT,CONTROL,VOICE,TERMS,BRANCH,PROSE,Path(__file__)]},all67_clean_then_current_complete_exchanges_read=True,all67_fresh_glosses_precede_localized_English=True,all67_individual_revision_or_retention_notes=True,decision_counts=dict(counts),one_registered_Camille_replacement_raw_and_effective_provenance_separate=True,leaf_platter_joke_polder_definition_personal_motive_and_conditional_Camille_pairs_reviewed=True,source_context_localization_naturalness_true_formatting_false=True,no_authored_layout=True,no_ROM_registry_ledger_orreviewcredit_change=True,new_emulator_runs=0,full_goal_complete=False))
    print(dict(objects=67,decisions=dict(counts),formatting=False,credit=0))
