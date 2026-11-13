"""Author14 complete-context decisions; native formatting and integration remain pending."""
import unicodedata
from collections import Counter
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.lil_B141_funding_prose_v3542 import SPEECH
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B141_author_v3542')
SOURCE=Path('work/analysis/lil_B141_source_v3532b/all14_clean_current_complete_context.json')
COMPARISON=Path('work/analysis/lil_B141_comparison_v3540/all14_current_effective_comparison_packet.json')
CONTEXT=Path('work/analysis/lil_B141_clean_context_v3534/all14_complete_clean_context_and_fresh_glosses.json')
CONTROL=Path('work/analysis/lil_B141_controls_v3538b/all14_source_current_dispatches_FI_C200_and630A_contract.json')
VOICE=Path('work/analysis/lil_B141_voices_v3533/current_four_static_names_voices_and207_catalog_rebind.json')
TERMS=Path('work/analysis/lil_B141_terms_v3541/source_current_polder_and_distinct_monetary_amounts.json')
BRANCH=Path('work/analysis/lil_B141_branches_v3539/original_relative_skip_operand_proof.json')
ENTRY=Path('work/analysis/lil_B141_entry_v3536/source_EV2_B141_action_dependency_and_native_getter_binding.json')
FUNDS=Path('work/analysis/lil_B141_funds_v3537b/source_million_threshold_and900000_payment_seven_boundary_cases.json')
PROSE=Path('scripts/lil_B141_funding_prose_v3542.py')
OUT=Path('translations/lil_B141_editorial_manuscript_v1.json')
if __name__=='__main__':
    assert not ROOT.exists() and not OUT.exists();source,comparison,context,control,voice,terms,branch,entry,funds=map(read,[SOURCE,COMPARISON,CONTEXT,CONTROL,VOICE,TERMS,BRANCH,ENTRY,FUNDS]);assert context['complete_clean_B141_read'] and len(context['records'])==len(comparison['records'])==14 and len(control['speech_dispatch_cases'])==28 and comparison['registered_runtime_catalog_replacement_count']==0
    assert source['source_macro_counts']=={'FI':1,'FA':0,'FO':0} and len(branch['operands_requiring_adjustment_when_resizing'])==13 and len(branch['cases'])==130
    gloss={r['id']:r for r in context['records']};speakers={2:'Lil',9:'Camille',20:'Fernando',171:'Research Student'};rows=[]
    for original in comparison['records']:
        r=deepcopy(original);body,note=SPEECH[r['source_record_index']];assert body==body.strip() and '  ' not in body and '\n' not in body and all(32<=ord(c)<127 for c in body) and not any(t in body for t in ['{LB','{ALIGN','{PAD','{SPEAKER:'])
        raw=bytes.fromhex(r['current_hex'])[1:];template=' '.join(unicodedata.normalize('NFKC',raw.decode('cp932')).split())
        for k in ['FI','FA','FO']:template=template.replace(k,'{MACRO:'+k+'}')
        decision='retain-wording' if body==template else 'revise';runtime=r['effective_predecessor_paragraph']
        r.update(source_meaning=gloss[r['id']]['fresh_source_gloss'],english='{SPEAKER:'+format(r['source_selector'],'02X')+'}'+body,localization_note=note,editorial_decision=decision,current_English=r['current_raw_storage_English'],current_stored_English=r['current_raw_storage_English'],current_effective_paragraph=runtime,effective_predecessor_runtime_paragraph=runtime,effective_predecessor_macro_paragraph=template,effective_predecessor_paragraph=template,current_effective_macro_template_hex=raw.hex(),current_effective_macro_template_English=raw.decode('cp932'),comparison_basis='Exact current route2 native output;NFKC and collapsed legacy whitespace for comparison. Preserve source FI in a logical macro template separately from actual default Lil expansion.',review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),speaker=speakers[r['source_selector']],context='Complete clean andcurrent exchanges read after fresh source glosses. '+context['whole_exchange_context'],prose_author_module=str(PROSE),prose_author_module_sha256=sha(PROSE.read_bytes()),status='source-context-localization-naturalness-reviewed;native-format-references-release-pending',editorial_older_English_comparison_pending=False,full_clean_context_precedes_comparison=True,current_complete_native_display_pending=True,source_kind='progressive',current_macro_dispatch_bound=True,original_native_display_consumer='original_progressive_54020')
        assert all(bytes.fromhex(r['source_hex']).count(k.encode())==body.count('{MACRO:'+k+'}') for k in ['FI','FA','FO'])
        if decision=='retain-wording':r['fresh_retained_wording_justification']=note
        rows.append(r)
    counts=Counter(r['editorial_decision'] for r in rows);assert counts=={'revise':7,'retain-wording':7},counts
    doc=dict(format='dk4-editorial-source-prose-draft-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],file_path='/data/SC2.DK4',current_ROM=source['current_ROM'],current_ROM_sha256=source['current_ROM_sha256'],source_ROM_sha256=source['source_ROM_sha256'],required_runtime_ARM9_sha256=source['current_ARM9_sha256'],records=rows,manuscript_kind='speech',prose_companions=[],revised=7,retained=7,fresh_source_glosses_precede_current_comparison_and_localized_English=True,source_prose_or_completion_credit_added=0,formatting_review_pending=True,status=rows[0]['status'])
    for key,path in [('source_context',SOURCE),('control_contract',CONTROL),('whole_exchange_context_notes',CONTEXT),('branch_proof',BRANCH),('item_terminology_reconciliation',TERMS),('actor_voice_contract',VOICE),('effective_current_comparison',COMPARISON),('source_entry_proof',ENTRY),('source_finance_contract',FUNDS)]:doc[key]=str(path);doc[key+'_sha256']=sha(path.read_bytes())
    ROOT.mkdir(parents=True);save(OUT,doc);save(ROOT/'all14_contextual_prose_or_retention_receipt.json',dict(manuscript=str(OUT),manuscript_sha256=sha(OUT.read_bytes()),evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,COMPARISON,CONTEXT,CONTROL,VOICE,TERMS,BRANCH,ENTRY,FUNDS,PROSE,Path(__file__)]},all14_complete_clean_then_current_exchanges_read=True,all14_fresh_glosses_precede_localized_English=True,all14_individual_revision_or_retention_notes=True,decision_counts=dict(counts),million_total900000_shortfall_borrowing_and_two_conditional_paths_preserved=True,source_FI_macro_separate_from_runtime_default_Lil=True,no_invented_relationship_rank_degree_interest_terms_or_construction_outcome=True,source_context_localization_naturalness_true_formatting_false=True,no_authored_layout=True,no_ROM_registry_ledger_or_reviewcredit_change=True,new_emulator_runs=0,full_goal_complete=False));print(dict(objects=14,decisions=dict(counts),formatting=False,credit=0))
