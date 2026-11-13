"""Save explicit individual whole-exchange decisions against sealed source/current text."""
import argparse
from collections import Counter
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    for name in ['drafts','current','objects','decisions','out']:ap.add_argument('--'+name,type=Path,required=True)
    args=ap.parse_args();assert not args.out.exists()
    drafts,current,objects,decisions=map(load,[args.drafts,args.current,args.objects,args.decisions])
    bound={r['id']:r for g in current['groups'] for r in g['records']}
    bound.update({r['id']:r for r in objects['style_records']+objects['choice_records']})
    assert len(bound)==len(drafts['records']) and current['runtime']==objects['runtime']
    blocks=decisions['blocks'];assert blocks==sorted(set(blocks))
    selected=[r for r in drafts['records'] if r['block'] in blocks]
    specs={r[0]:r for r in decisions['records']}
    assert len(specs)==len(decisions['records'])==len(selected) and specs.keys()=={r['id'] for r in selected}
    rows=[]
    for original in selected:
        ident,mode,reason,*amendment=specs[original['id']]
        assert mode in ['R','D','T'] and reason.strip()
        old=bound[ident];assert all(original[k]==old[k] for k in ['source_hex','source_reference'])
        row=deepcopy(original)
        for k,v in old.items():
            if k.startswith(('current_','source_')) or k in ['selected_native_pointer','native_choice_provider_not_run_as_message_catalogue']:
                row[k]=deepcopy(v)
        prior=old['current_comparison_paragraph']
        if mode=='R':assert not amendment;proposed=prior
        elif mode=='D':assert not amendment;proposed=original['independent_English_draft']
        else:assert len(amendment)==1;proposed=amendment[0]
        decision='retention' if mode=='R' else 'revision'
        assert (proposed==prior)==(mode=='R'),(ident,mode,proposed)
        assert proposed.isascii() and proposed.strip()==proposed and not any(t in proposed for t in ['\n','\r','{LB','{ALIGN','{PAD'])
        assert all(proposed.count(t)==row['source_macros'].get(t,0) for t in ['FI','FA','FO','FU']),ident
        assert not any(row['review'].values())
        row.update(proposed_English=proposed,decision=decision,finding=reason,localization_note=reason,
            retention_reason=reason if mode=='R' else '',contextual_comparison_saved=True,
            source_current_comparison_pending=False,contextual_comparison_pending=False,
            current_English_not_consulted=False,current_ROM_English_unconsulted=False,earlier_English_unconsulted=False,
            current_English_now_exposed=True,current_English_comparison_pending=False,
            names_terms_consumers_andfresh_display_approval_pending=True,
            source_draft_provenance=str(args.drafts),source_draft_provenance_sha256=digest(args.drafts),
            complete_exchange_source_current_English_flow_reviewed=True,
            no_proposal_may_ship_orreceive_completion_credit_yet=True,new_credit=0)
        rows.append(row)
    counts=Counter(r['decision'] for r in rows)
    save(args.out,dict(format='dk4-contextual-dialogue-proposals-v2',translation_policy='natural-dialogue-v2',target_locale='en-US',
        records=rows,records_count=len(rows),complete_exchanges=len(blocks),blocks=blocks,runtime=current['runtime'],
        revised=counts['revision'],retained=counts['retention'],all_individual_findings_andretention_reasons_saved=True,
        all_five_gates_still_pending=True,source_clean_meanings_andindependent_drafts_preceded_current_intake=True,
        scoped_names_terms_fresh_native_display_andintegration_pending=True,new_credit=0,full_goal_complete=False,
        evidence={str(p):digest(p) for p in [args.drafts,args.current,args.objects,args.decisions,Path(__file__)]}))
    print(dict(records=len(rows),complete_exchanges=len(blocks),revisions=counts['revision'],retentions=counts['retention'],all_gates_pending=True,new_credit=0))


if __name__=='__main__':main()
