"""Save individual human-reviewed proposals against exact clean,current andindependent references."""
from copy import deepcopy
from pathlib import Path
from collections import Counter
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B58_B70_clean_20261109')
def key(row):return int(row['id'].rsplit('R',1)[1]) if row['kind']!='typed-choice-label' else row['id']
def write(decisions,filename,producer):
    out=ROOT/filename;assert not out.exists()
    draft_path=ROOT/'all303_clean_meanings_andindependent_drafts_v3.json'
    current_path=ROOT/'current_v1/current_effective.json';objects_path=ROOT/'current_objects_v1/current_objects.json'
    drafts,current,objects=map(load,[draft_path,current_path,objects_path])
    bound={r['id']:r for g in current['groups'] for r in g['records']};bound.update({r['id']:r for r in objects['choice_records']})
    assert len(bound)==len(drafts['records'])==303 and current['runtime']==objects['runtime']
    selected=[r for r in drafts['records'] if r['block'] in decisions]
    for block,items in decisions.items():assert set(items)=={key(r) for r in selected if r['block']==block}
    rows=[]
    for original in selected:
        old=bound[original['id']];row=deepcopy(original)
        assert row['source_hex']==old['source_hex'] and all(old['source_reference'][k]==v for k,v in row['source_reference'].items())
        for k,v in old.items():
            if k.startswith('current_') or k in ['selected_native_pointer','source_choice_object_hex','source_index','source_count','source_word','source_command_offset','native_choice_provider_not_run_as_message_catalogue']:
                row[k]=deepcopy(v)
        text,reason=decisions[row['block']][key(row)];prior=old['current_comparison_paragraph']
        proposed=prior if text is None else original['independent_English_draft'] if text=='D' else text
        decision='retention' if text is None else 'revision'
        assert reason and (proposed==prior)==(decision=='retention'),(row['id'],decision,prior,proposed)
        assert proposed.isascii() and proposed.strip()==proposed and not any(t in proposed for t in ['\n','\r','{LB','{ALIGN','{PAD'])
        assert all(proposed.count(t)==row['source_macros'].get(t,0) for t in ['FI','FA','FO','FU']),row['id']
        assert not any(row['review'].values())
        row.update(proposed_English=proposed,decision=decision,finding=reason,localization_note=reason,
            retention_reason=reason if decision=='retention' else '',contextual_comparison_saved=True,
            source_current_comparison_pending=False,contextual_comparison_pending=False,
            current_English_not_consulted=False,current_ROM_English_unconsulted=False,earlier_English_unconsulted=False,
            current_English_now_exposed=True,current_English_comparison_pending=False,current_comparison_pending=False,
            names_terms_consumers_andfresh_display_approval_pending=True,
            source_draft_provenance=str(draft_path),source_draft_provenance_sha256=digest(draft_path),
            no_proposal_may_ship_orreceive_completion_credit_yet=True,new_credit=0)
        rows.append(row)
    counts=Counter(r['decision'] for r in rows)
    save(out,dict(format='dk4-contextual-dialogue-proposals-v2',translation_policy='natural-dialogue-v2',target_locale='en-US',
        records=rows,records_count=len(rows),complete_exchanges=len(decisions),blocks=sorted(decisions),runtime=current['runtime'],
        revised=counts['revision'],retained=counts['retention'],all_individual_findings_andretention_reasons_saved=True,
        all_five_gates_still_pending=True,source_clean_meanings_andindependent_drafts_preceded_current_intake=True,
        scoped_names_terms_fresh_native_display_andintegration_pending=True,new_credit=0,full_goal_complete=False,
        evidence={str(p):digest(p) for p in [draft_path,current_path,objects_path,Path(__file__),Path(producer)]}))
    print('Saved',len(rows),'whole-exchange decisions:',dict(counts),'with exact references;all five gates pending.')
