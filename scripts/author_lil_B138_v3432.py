"""Author44 contextual reviews with individual retention/revision findings."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.lil_B138_dignity_prose_v3432 import SPEECH
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B138_author_v3432')
SOURCE=Path('work/analysis/lil_remaining_B138_B140_source_v3422/next44_B138_clean_current_context.json')
COMPARISON=Path('work/analysis/lil_B138_comparison_v3431/all44_current_effective_comparison_packet.json')
CONTEXT=Path('work/analysis/lil_B138_clean_context_v3428/all44_complete_clean_context_and_fresh_glosses.json')
CONTROL=Path('work/analysis/lil_B138_controls_v3426e/all44_source_current_dispatches10_predicates_and1_query.json')
VOICE=Path('work/analysis/lil_B138_voices_v3425/current_seven_static_names_voices_and207_catalog_rebind.json')
TERMS=Path('work/analysis/lil_B138_terms_v3429/clean_current_names_leaf_price_macro_and_entry_reconciliation.json')
BRANCH=Path('work/analysis/lil_B138_branches_v3427b/original_relative_skip_operand_proof.json')
PROSE=Path('scripts/lil_B138_dignity_prose_v3432.py')
OUT=Path('translations/lil_B138_editorial_manuscript_v1.json')
if __name__=='__main__':
    assert not ROOT.exists() and not OUT.exists();source,comparison,context,control,voice,terms=map(read,[SOURCE,COMPARISON,CONTEXT,CONTROL,VOICE,TERMS])
    assert context['all44_complete_clean_source_objects_read_before_older_English_comparison'] and context['all44_fresh_source_glosses_precede_localized_English'] and len(comparison['records'])==44 and comparison['registered_runtime_catalog_replacement_count']==0
    assert len(control['speech_dispatch_cases'])==88 and len(control['current_original_predicate_cases'])==11 and not source['typed_choice_records']
    assert {(r['block'],r['source_record_index']) for r in source['records']}==set(SPEECH)
    for d in [comparison,control,terms,voice]:assert d['source_context_sha256']==sha(SOURCE.read_bytes())
    gloss={r['id']:r for r in context['records']};speakers={2:'Lil Argot',14:'Emilio',20:'Fernando',21:'Ian',22:'Samwell',23:'Manuel',92:'Barkeep;unnamed'};rows=[]
    for original in comparison['records']:
        r=deepcopy(original);body,note=SPEECH[r['block'],r['source_record_index']]
        assert body==body.strip() and '  ' not in body and '\n' not in body and all(32<=ord(c)<127 for c in body) and not any(tag in body for tag in ['{LB','{ALIGN','{PAD','{SPEAKER:'])
        for m in ['FI','FA','FO']:assert bytes.fromhex(r['source_hex']).count(m.encode())==body.count('{MACRO:'+m+'}')
        old=r['current_effective_paragraph']
        for m in ['FI','FA','FO']:old=old.replace(m,'{MACRO:'+m+'}')
        decision='retain-wording' if body==old else 'revise'
        r.update(source_meaning=gloss[r['id']]['fresh_source_gloss'],english='{SPEAKER:'+format(r['source_selector'],'02X')+'}'+body,localization_note=note,editorial_decision=decision,current_stored_English=r['current_raw_storage_English'],effective_predecessor_paragraph=old,comparison_basis='Exact current native template,NFKC presentation forms andcollapsed legacy whitespace;raw/effective/catalogue provenance separate.',review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),speaker=speakers[r['source_selector']],context='Whole clean exchange andfresh glosses precede older-English comparison. '+context['complete_exchanges'][str(r['block'])]+' All seven static actors,Lil-context FO,ten predicates andone event137 query are bound;no selected gameplay or earned progress claimed.',prose_author_module=str(PROSE),prose_author_module_sha256=sha(PROSE.read_bytes()),status='source-context-localization-naturalness-reviewed;native-format-references-representative-release-pending',editorial_older_English_comparison_pending=False,full_clean_context_precedes_comparison=True,current_complete_native_display_pending=True,source_kind=r['kind'],current_macro_dispatch_bound=True,original_native_display_consumer='original_progressive_54020')
        if decision=='retain-wording':r['fresh_retained_wording_justification']=note
        rows.append(r)
    counts=Counter(r['editorial_decision'] for r in rows)
    doc=dict(format='dk4-editorial-source-prose-draft-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],file_path='/data/SC2.DK4',current_ROM=source['current_ROM'],current_ROM_sha256=source['current_ROM_sha256'],source_ROM_sha256=source['source_ROM_sha256'],required_runtime_ARM9_sha256=source['current_ARM9_sha256'],records=rows,manuscript_kind='speech',prose_companions=[],revised=counts['revise'],retained=counts['retain-wording'],fresh_source_glosses_precede_current_comparison_and_localized_English=True,broad_Proof_terminology_editorial_consistency_lead_still_open=True,source_prose_or_completion_credit_added=0,formatting_review_pending=True,status=rows[0]['status'])
    for key,path in [('source_context',SOURCE),('control_contract',CONTROL),('whole_exchange_context_notes',CONTEXT),('branch_proof',BRANCH),('item_terminology_reconciliation',TERMS),('actor_voice_contract',VOICE),('effective_current_comparison',COMPARISON)]:doc[key]=str(path);doc[key+'_sha256']=sha(path.read_bytes())
    assert len(rows)==44 and counts['revise']+counts['retain-wording']==44;ROOT.mkdir(parents=True);save(OUT,doc)
    save(ROOT/'all44_contextual_prose_or_retention_receipt.json',dict(manuscript=str(OUT),manuscript_sha256=sha(OUT.read_bytes()),evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,COMPARISON,CONTEXT,CONTROL,VOICE,TERMS,BRANCH,PROSE,Path(__file__)]},all44_clean_then_current_complete_exchanges_read=True,all44_fresh_glosses_precede_localized_English=True,all44_individual_revision_or_retention_notes=True,decision_counts=dict(counts),zero_registered_catalogue_replacements_raw_and_effective_provenance_separate=True,alternative_map_leaf_transaction_and_dignity_arc_price100_nested_replies_and_wordless_questions_reviewed=True,source_context_localization_naturalness_true_formatting_false=True,no_authored_layout=True,no_ROM_registry_ledger_orreviewcredit_change=True,new_emulator_runs=0,full_goal_complete=False))
    print(dict(objects=44,decisions=dict(counts),formatting=False,credit=0))
