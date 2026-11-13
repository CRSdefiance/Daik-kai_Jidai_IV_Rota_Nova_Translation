"""Merge explicit whole-exchange decisions without awarding any five-gate approval."""
from collections import Counter
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B196_B215_clean_20261110')


def main():
    out=ROOT/'contextual_comparisons_v1.json';assert not out.exists()
    packet=load(ROOT/'clean_source_packet.json');rows=[];evidence={}
    for part in ['B196_B201','B202_B209','B210_B215']:
        path=ROOT/f'contextual_{part}_v1.json';p=load(path)
        assert p['all_five_gates_still_pending'] and p['source_clean_meanings_andindependent_drafts_preceded_current_intake']
        rows.extend(p['records']);evidence.update(p['evidence']);evidence[str(path)]=digest(path)
    original=[r for g in packet['groups'] for r in g['records']]
    assert len(rows)==len({r['id'] for r in rows})==len(original)==321
    for a,b in zip(original,rows,strict=True):
        assert all(a[k]==b[k] for k in ['id','source_hex','source_reference'])
        assert b['contextual_comparison_saved'] and b['finding'] and not any(b['review'].values())
        assert b['retention_reason'] if b['decision']=='retention' else not b['retention_reason']
    counts=Counter(r['decision'] for r in rows);assert counts=={'revision':171,'retention':150}
    current=load(ROOT/'current_v1/current_effective.json')
    evidence[str(Path(__file__))]=digest(Path(__file__))
    save(out,dict(format='dk4-contextual-dialogue-proposals-v2',translation_policy='natural-dialogue-v2',target_locale='en-US',
        records=rows,records_count=321,complete_exchanges=18,blocks=packet['selected_blocks'],runtime=current['runtime'],
        revised=171,retained=150,all_individual_findings_andretention_reasons_saved=True,
        all_five_gates_still_pending=True,source_clean_meanings_andindependent_drafts_preceded_current_intake=True,
        scoped_names_terms_fresh_native_display_andintegration_pending=True,evidence=evidence,new_credit=0,full_goal_complete=False))
    print('Saved321 contextual decisions:171 revisions/150 retentions; names/terms/allgates pending;zero credit.')


if __name__=='__main__':main()
