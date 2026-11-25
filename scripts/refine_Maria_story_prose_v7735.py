"""Natural compact rephrasing for three measured wrap risks; preserve every earlier draft."""
import inspect
from copy import deepcopy
from pathlib import Path
from scripts import plan_Maria_story_layout_v7733 as layout
from scripts.generic_name_macro_owned_v5886b import expand
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.maria_unlocked_current_context_v7680 import MariaUnlockedCurrentContext
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/maria_story_refined_v7735')
PREVIOUS=Path('translations/maria_B34_B108_B35_editorial_manuscript_v1.json')
OUTPUT=Path('translations/maria_B34_B108_B35_editorial_manuscript_v2.json')
LOGICAL=Path('work/analysis/maria_story_logical_v7732/67_logical_paragraphs268_original_native_macro_literal_alignments.json')
PRIOR_PLAN=Path('work/analysis/maria_story_wrap_v7734/67_refined_full_width_plans_no_prose_changes_all_QA_preserved.json')
NAMES=Path('work/analysis/maria_story_names_macros_v7727/eight_static_speakers_sixteen_getters_clean_fields_actual_source_macros.json')
CHANGES={
'DK4_MES_B108_R0111':("I hear the Argot Company's young leader has a strong sense of justice. They say she was furious and said she'd never forgive FO.","Keep both reports, young female leader, strong justice and angry declaration; replace the wordier hearsay framing with natural direct clauses. No sworn oath, commodity or fact of actual dishonest trade is added."),
'DK4_MES_B35_R0032':("Now let me ask you something. You said you were with the Swedish navy. Do you know the Argot Company in the North Sea?","The reciprocal Now let me ask you retains Maria's turn-taking; remove redundant in return/up wording while preserving Swedish navy and the shared North Sea context."),
'DK4_MES_B35_R0068':("Camille's a young man with the Argot Company. He's close to Admiral Argot. They're just traveling separately for now...","The effective predecessor already preserved membership, youth, closeness and temporary separate travels, so the initial retention was justified. Focused wrapping exposed two weak boundaries. This compact natural rephrasing retains every fact and the pause without inventing romance, kinship, resignation, Swedish fleet membership or a cause of separation."),
}
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists();old,logical,prior,names=map(read,[PREVIOUS,LOGICAL,PRIOR_PLAN,NAMES])
    assert logical['manuscript_sha256']==prior['manuscript_sha256']==sha(PREVIOUS.read_bytes())
    assert {r['id'] for r in prior['unresolved']}==set(CHANGES)
    doc=deepcopy(old);rows=doc['records'];oldby={r['id']:r for r in old['records']}
    for row in rows:
        if row['id'] not in CHANGES:continue
        english,reason=CHANGES[row['id']];row.update(english=english,decision='revision',
            decision_reason=row['decision_reason']+' Follow-up: '+reason,previous_draft_decision=oldby[row['id']]['decision'],
            previous_draft_English=oldby[row['id']]['english'],measured_wrap_revision_reason=reason)
        for token in ['FI','FA','FO']:assert english.count(token)==oldby[row['id']]['english'].count(token)
    assert sum(r['decision']=='revision' for r in rows)==48 and sum(r['decision']=='retention' for r in rows)==19
    doc.update(previous_manuscript=str(PREVIOUS),previous_manuscript_sha256=sha(PREVIOUS.read_bytes()),three_wrap_findings_andearlier_retention_preserved=True)
    save(OUTPUT,doc);ROOT.mkdir(parents=True)
    adapter=checked_text(inspect.getsource(expand),{'assert identity==prefix and captain==2':'assert identity==prefix and captain==3'})
    ns=dict(expand.__globals__);exec(compile(adapter,__file__+'::three-refined-logical-inputs','exec'),ns)
    ctx=MariaUnlockedCurrentContext(names['current_native_input'],'unused-no-historical-ROM',ROOT/'current_context');native=[]
    for row in rows:
        previous=next(r for r in logical['records'] if r['id']==row['id'])
        body=row['english'].encode('cp932')
        if row['id'] in CHANGES:
            r=ctx.execute(ns['expand'],body,row['source_selector']);ctx.machines.pop()
            expected=body.replace(b'FI',b'Maria').replace(b'FA',b'Li').replace(b'FO',b'Li Clan')
            assert all(c['output_hex']==expected.hex() for c in r['cases'])
            native.append(dict(id=row['id'],mode='four-fresh-alignments',logical_body_hex=body.hex(),native_alignment=r))
        else:
            assert body.hex()==previous['logical_body_hex'] and row['source_selector']==previous['source_selector']
            native.append(dict(id=row['id'],mode='four-exact-own-current-alignments-reused',logical_body_hex=body.hex(),original_proof=str(LOGICAL),original_proof_sha256=sha(LOGICAL.read_bytes())))
    assert not ctx.machines
    plan_adapter=checked_text(layout.ADAPTER,{'cost[0]+tiny,cost[1]+1,cost[2]+weak':'cost[0]+tiny+weak,cost[1]+1,cost[2]+weak'})
    env=dict(layout.ENV);exec(compile(plan_adapter,__file__+'::same-scoped-automatic-planner','exec'),env)
    plans=[];unresolved=[]
    for row in rows:
        planning=deepcopy(row);body=row['english']
        for token in ['FI','FA','FO']:body=body.replace(token,'{MACRO:'+token+'}')
        planning['english']='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+body
        p=env['plan'](planning);assert ' '.join(p['lines'])==body
        p.update(file_path=row['file_path'],block=row['block'],source_record_index=row['source_record_index'],source_selector=row['source_selector'],
            logical_English=row['english'],planning_record=planning,base_QA=layout.base_qa(planning,p))
        info=[i for i in p['base_QA']['issues'] if i['code']=='line-break-count' and i['severity']=='info']
        if info:p['row_count_reason']=row['decision_reason']+' Complete English uses '+str(len(p['lines']))+' automatic rows of '+str(p['line_lengths'])+' cells within the original native four-row page. Every word, punctuation mark and source macro remains; Japanese wrapping is not an English dramatic pause.'
        issues=[i for i in p['base_QA']['issues'] if i['severity'] in ['warning','error']]
        if issues:unresolved.append(dict(id=p['id'],issues=issues,lines=p['lines']))
        plans.append(p)
    save(ROOT/'67_refined_decisions_native_logical_bindings_automatic_plans_QA.json',dict(
        manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),previous_manuscript=str(PREVIOUS),previous_manuscript_sha256=sha(PREVIOUS.read_bytes()),
        decisions=dict(revision=48,retention=19),records=plans,logical_bindings=native,fresh_logical_alignment_cases=12,exact_own_current_logical_alignment_cases_reused=256,
        source_owned_macro_adapter=adapter,source_owned_automatic_plan_adapter=plan_adapter,unresolved=unresolved,
        prior_five_weak_boundary_warnings_andfailed_cost_only_refinement_preserved=True,no_QA_warning_waiver=True,
        all_source_meaning_runtime_macros_names_emotional_progression_preserved=True,physical_viewport=[216,64],physical_rows_per_native_page=4,
        all_formatting_gates_false=True,compiled_byte_native_fonts_bounds_pages_stored_controls_actual_production_registry_pending=True,
        existing_system_only_unlock_fixture=True,earned_unlock_verified=False,new_emulator_runs=0,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [PREVIOUS,OUTPUT,LOGICAL,PRIOR_PLAN,NAMES,Path(__file__)]},full_goal_complete=False))
    print('67draft decisions:48revisions19retentions;12fresh+256exact reused logical alignments;pages',sum(r['expected_native_pages'] for r in plans),'unresolved',unresolved)
    if unresolved:raise SystemExit(1)
