"""Record all11 clean-first contextual decisions; native formatting remains pending."""
from pathlib import Path
import re
from copy import deepcopy
from collections import Counter
from dk4tool.patch.grand_race_menu_release import sha
from scripts import lil_B194_prose_v5498 as prose
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B194_author_v5499')
COMPARISON=Path('work/analysis/lil_B194_comparison_v5497/all11_complete_clean_and_predecessor_exchange.json')
OUTPUT=Path('translations/lil_B194_editorial_manuscript_v1.json')
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists();comparison=read(COMPARISON);source=read(comparison['source_context'])
    gp=Path(source['whole_exchange_context_notes']);gloss=read(gp);terms=read(comparison['terms'])
    assert gloss['read_no_predecessor_English'] and len(gloss['records'])==11
    assert set(prose.REVISIONS)|set(prose.RETAIN_NOTES)=={r['source_record_index'] for r in source['records']}
    assert not set(prose.REVISIONS)&set(prose.RETAIN_NOTES)
    doc=dict(format='dk4-editorial-source-prose-draft-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',
        review_gates=['source','context','localization','naturalness','formatting'],file_path='/data/SC2.DK4',current_ROM=source['current_ROM'],
        current_ROM_sha256=source['current_ROM_sha256'],source_ROM_sha256=source['source_ROM_sha256'],required_runtime_ARM9_sha256=source['current_ARM9_sha256'],
        source_prose_or_completion_credit_added=0,formatting_review_pending=True,status='source-context-localization-naturalness-reviewed;native-layout-relocation-actual-release-pending',
        whole_exchange_context=gloss['complete_exchange_progression'],manuscript_kind='speech',prose_companions=[])
    deps=dict(source_context=comparison['source_context'],whole_exchange_context_notes=str(gp),
        actor_voice_contract='work/analysis/lil_B194_voices_v5490/current207_catalog_eight_voices_and_three_source_selectors.json',
        control_contract='work/analysis/lil_B194_dispatches_v5491/all11_source_current_dispatches_one_FI_and6_control_leaves.json',
        branch_proof='work/analysis/lil_B194_branches_v5493/original_relative_skip_operand_proof.json',
        source_entry_proof='work/analysis/lil_B194_entry_v5492/source_EV2_B194_action_dependency_and_native_getter_binding.json',
        source_effect_and_predicate_contract='work/analysis/lil_B194_controls_v5495/one_unforced_predicate_resource42_two_C200_paths_and6_source_leaves.json',
        current_C200_source_ownership_proof='work/analysis/lil_B194_controls_v5495/one_unforced_predicate_resource42_two_C200_paths_and6_source_leaves.json',
        source_nameplate_consumer_proof='work/analysis/lil_B194_names_v5494/six_original_progressive_and_catalogue_name_consumers.json',
        actor_terminology_reconciliation=comparison['terms'],effective_current_comparison=str(COMPARISON))
    for key,path in deps.items():doc[key]=path;doc[key+'_sha256']=sha(Path(path).read_bytes())
    rows=[]
    for original in comparison['records']:
        row=deepcopy(original);index=row['source_record_index'];old=row['previous_paragraph']
        body,note=prose.REVISIONS[index] if index in prose.REVISIONS else (old,prose.RETAIN_NOTES[index])
        decision='revise' if index in prose.REVISIONS else 'retain-wording'
        assert body.isascii() and body==' '.join(body.split()) and not any(v in body for v in ['%','{LB','{PAD'])
        assert re.findall(rb'FI|FA|FO',bytes.fromhex(row['source_hex'])[1:])==[m.encode('ascii') for m in re.findall(r'\{MACRO:(FI|FA|FO)\}',body)]
        assert (body!=old)==(decision=='revise')
        speaker='Impersonal fashion notice' if row['kind']=='system-FE' else terms['approved_prose_names'][str(row['source_selector'])]
        row.update(source_meaning=row['fresh_source_gloss'],english='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+body,
            speaker=speaker,context=gloss['complete_exchange_progression'],localization_note=note,editorial_decision=decision,
            effective_predecessor_paragraph=old,record_index=row['current_record_index'],full_clean_context_precedes_comparison=True,
            editorial_predecessor_English_comparison_pending=False,current_macro_dispatch_bound=True,current_complete_native_display_pending=True,
            current_native_UI_body_explicit_unexecuted_boundary=True,review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            status=doc['status'],prose_author_module=str(Path(prose.__file__)),
            original_native_display_consumer='original_null_actor_24310_then5473C_FE' if row['kind']=='system-FE' else 'original_progressive_54020')
        if decision=='retain-wording':row['fresh_retained_wording_justification']=note
        rows.append(row)
    counts=Counter(r['editorial_decision'] for r in rows);assert counts=={'revise':4,'retain-wording':7}
    doc.update(records=rows,revised=4,retained=7,
        source_Julio6_voice5_Sailor156_voice4_Port_Worker117_voice0_and_original_names_preserved=True,
        source_FI_Admiral_address_casual_gossip_reported_rice_and_excited_personal_purchase_intention_preserved=True,
        source_Sake37_Hangzhou_and_all21_conditional_commands_preserved=True,full_goal_complete=False)
    ROOT.mkdir(parents=True);save(OUTPUT,doc)
    save(ROOT/'all11_clean_first_contextual_decisions.json',dict(manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),decision_counts=dict(counts),
        all7_retentions_individually_justified=True,all11_records_reviewed_as_one_exchange=True,
        source_context_localization_naturalness_true_formatting_false=True,new_emulator_runs=0,new_review_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [COMPARISON,gp,Path(prose.__file__),Path(__file__)]},full_goal_complete=False))
    print('B194:11 whole-exchange decisions,4 revisions/7 justified retentions. Native formatting pending;zero credit.')
