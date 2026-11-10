"""Author all32 contextual decisions with formatting/actual/integration gates explicitly open."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.maria_B97_prose_v5008 import REVISIONS,RETAIN_NOTES
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B97_author_v5008')
OUT=Path('translations/maria_B97_editorial_manuscript_v1.json')
SOURCE=Path('work/analysis/maria_B97_source_v4998/all32_clean_current_complete_context.json')
COMPARISON=Path('work/analysis/maria_B97_comparison_v5007/all32_current_effective_comparison_packet.json')
CONTEXT=Path('work/analysis/maria_B97_clean_glosses_v4996/all32_clean_exchange_and_fresh_glosses.json')
CONTROL=Path('work/analysis/maria_B97_controls_v5005/eight_source_leaves_resource633E_item4820_hide_and_two_effects.json')
VOICE=Path('work/analysis/maria_B97_voices_v5000/current207_catalog_eight_voices_and_three_Maria_selectors.json')
TERMS=Path('work/analysis/maria_B97_terms_v5006/bound_Maria_Xien_Bandit_Li_Clan_Sao_Jorge_Proof_and_tablet_context.json')
DISPATCH=Path('work/analysis/maria_B97_dispatches_v5001/all32_clean_current_Maria_dispatches_FE_and_FO.json')
ENTRY=Path('work/analysis/maria_B97_entry_v5002/source_EV3_B97_action_dependency_and_native_getter_binding.json')
NAMES=Path('work/analysis/maria_B97_names_v5003/six_original_progressive_and_catalogue_name_consumers.json')
MACROS=Path('work/analysis/maria_B97_macros_v5004/three_actors_default_and_real_FO20_alignment_cases.json')
PROSE=Path('scripts/maria_B97_prose_v5008.py')
if __name__=='__main__':
    assert not ROOT.exists() and not OUT.exists();source,comparison,context,control,voice,terms,dispatch,entry,names,macros=map(read,[SOURCE,COMPARISON,CONTEXT,CONTROL,VOICE,TERMS,DISPATCH,ENTRY,NAMES,MACROS]);assert context['read_no_predecessor_English'] and len(source['records'])==len(comparison['records'])==32 and len(dispatch['speech_dispatch_cases'])==64
    assert set(REVISIONS).isdisjoint(RETAIN_NOTES) and {r['source_record_index'] for r in source['records']}==set(REVISIONS)|set(RETAIN_NOTES)
    assert source['source_macro_counts']==dict(FI=0,FA=0,FO=1);speakers={3:'Maria Huamei Li',10:'Xien Yan',180:'Bandit',254:'Impersonal whispering cue'};rows=[]
    progression=' Whispers;identification;anger at lost raiding livelihood;village devastation;revenge;Maria names slave trading/plunder and rejects indiscriminate attacks;cycle of conflict;political alternative;confidence;voluntary invitation;consideration;trust;welcome;tentative ruins/tablet handover.'
    for original in comparison['records']:
        r=deepcopy(original);index=r['source_record_index'];old=r['effective_predecessor_paragraph'];body,note=REVISIONS[index] if index in REVISIONS else (old,RETAIN_NOTES[index]);assert body==body.strip() and '  ' not in body and '\n' not in body and all(32<=ord(c)<127 for c in body)
        assert not any(tag in body for tag in ['{LB','{ALIGN','{PAD','{SPEAKER:'])
        assert body.count('{MACRO:FO}')==(1 if index==22 else 0) and all(t not in body for t in ['{MACRO:FI}','{MACRO:FA}'])
        decision='retain-wording' if body==old else 'revise';assert (decision=='revise')==(index in REVISIONS)
        r.update(source_meaning=r['fresh_source_gloss'],english='{SPEAKER:'+format(r['source_selector'],'02X')+'}'+body,localization_note=note,editorial_decision=decision,current_English=r['current_raw_storage_English'],current_stored_English=r['current_raw_storage_English'],current_effective_paragraph=old,current_effective_macro_template_hex=r['current_hex'][2:],current_effective_macro_template_English=r['current_raw_storage_English'],comparison_basis='Exact current route3 native dispatch output with real FO expanded;NFKC presentation forms and collapsed legacy whitespace. Raw bytes,macro template and effective text remain distinct.',review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),speaker=speakers[r['source_selector']],context='Both complete clean and current exchanges read after all32 fresh clean-only glosses.'+progression+' Actual current Maria captain3 opening binds names/voices and default Li Clan,but does not activate B97. All40 commands/eight exact leaves,633E,4820/4700 and two A000 boundaries are separate;their resource/effect bodies and natural eligibility are not proved by offline tests.',status='source-context-localization-naturalness-reviewed;native-format-relocation-actual-release-pending',source_gloss_precedes_comparison=True,current_complete_native_display_pending=True,current_macro_dispatch_bound=True,original_native_display_consumer='original24310-null-actor-then5473C' if r['kind']=='system-FE' else 'original-progressive54020',prose_author_module=str(PROSE),prose_author_module_sha256=sha(PROSE.read_bytes()))
        if decision=='retain-wording':r['fresh_retained_wording_justification']=note
        rows.append(r)
    counts=Counter(r['editorial_decision'] for r in rows);assert counts=={'revise':23,'retain-wording':9}
    doc=dict(format='dk4-editorial-source-prose-draft-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],file_path='/data/SC3.DK4',current_ROM=source['current_ROM'],current_ROM_sha256=source['current_ROM_sha256'],source_ROM_sha256=source['source_ROM_sha256'],required_runtime_ARM9_sha256=source['current_ARM9_sha256'],records=rows,manuscript_kind='speech',prose_companions=[],revised=23,retained=9,formatting_review_pending=True,source_prose_or_completion_credit_added=0,status=rows[0]['status'])
    for key,path in [('source_context',SOURCE),('control_contract',CONTROL),('whole_exchange_context_notes',CONTEXT),('branch_proof',CONTROL),('item_terminology_reconciliation',TERMS),('actor_voice_contract',VOICE),('effective_current_comparison',COMPARISON),('source_dispatch_proof',DISPATCH),('source_entry_proof',ENTRY),('name_consumer_proof',NAMES),('macro_contract',MACROS)]:doc[key]=str(path);doc[key+'_sha256']=sha(path.read_bytes())
    ROOT.mkdir(parents=True);save(OUT,doc);save(ROOT/'all32_contextual_prose_or_retention_receipt.json',dict(manuscript=str(OUT),manuscript_sha256=sha(OUT.read_bytes()),decision_counts=dict(counts),all32_clean_first_glosses_then_complete_predecessor_comparison=True,all32_individual_revision_or_justified_retention_notes=True,source_revenge_grievance_atrocities_political_purpose_confidence_voluntary_agency_and_tablet_uncertainty_preserved=True,no_invented_kinship_rank_starvation_killing_specific_loss_or_earned_inventory=True,all40_commands_and_eight_leaves_require_exact_preservation=True,one_FO_runtime_macro_preserved=True,no_authored_layout_or_prose_shortening_for_legacy_allocation=True,formatting_review_false_and_actual_integration_gates_open=True,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,COMPARISON,CONTEXT,CONTROL,VOICE,TERMS,DISPATCH,ENTRY,NAMES,MACROS,PROSE,Path(__file__)]},new_review_credit=0,new_emulator_runs=0,no_ROM_registry_ledger_change=True,full_goal_complete=False))
    print(dict(objects=32,decisions=dict(counts),formatting=False,credit=0))
