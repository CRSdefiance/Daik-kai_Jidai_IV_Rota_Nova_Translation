"""Bind286 individual contextual decisions to sealed source and native current text."""
from copy import deepcopy
from pathlib import Path
from collections import Counter
import re
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts import maria_B37_B40_contextual_proposals_v1 as p1
from scripts import maria_B41_B44_contextual_proposals_v1 as p2
from scripts import maria_B45_B46_contextual_proposals_v1 as p3
from scripts import maria_B47_contextual_proposals_v1 as p4
from scripts import maria_B48_contextual_proposals_v1 as p5
from scripts import maria_B49_B50_contextual_proposals_v1 as p6

ROOT = Path('work/Maria_B37_B50_clean_20261109')

def main():
    out = ROOT/'all286_contextual_proposals_v1.json'
    assert not out.exists()
    paths = [ROOT/'all286_clean_meanings_andindependent_drafts_v2.json',
             ROOT/'current_v1/current_effective.json', ROOT/'current_objects_v1/current_objects.json']
    drafts, current, objects = map(load, paths)
    byid = {r['id']: r for g in current['groups'] for r in g['records']}
    byid.update({r['id']: r for r in objects['choice_records']})
    decisions = {}
    for part in [p1,p2,p3,p4,p5,p6]:
        assert not set(decisions).intersection(part.DECISIONS)
        decisions.update(part.DECISIONS)
    keyed = {(b,i):(text,reason) for b,ds in decisions.items() for i,text,reason in ds}
    assert len(keyed) == len(byid) == len(drafts['records']) == 286
    assert keyed.keys() == {(r['block'],r['source_record_index']) for r in drafts['records']}
    rows = []
    for source in drafts['records']:
        row = deepcopy(byid[source['id']])
        assert row['source_hex']==source['source_hex'] and row['source_reference']==source['source_reference']
        assert row['source_meaning']==source['source_meaning'] and row['independent_English_draft']==source['independent_English_draft']
        text,reason = keyed[(source['block'],source['source_record_index'])]
        decision = 'retention' if text is None else 'revision'
        proposed = row['current_comparison_paragraph'] if text is None else source['independent_English_draft'] if text=='D' else text
        assert proposed.isascii() and proposed==proposed.strip()
        assert not any(x in proposed for x in ['\n','\r','\t','{LB','{PAD','{ALIGN'])
        assert dict(Counter(re.findall(r'F[A-Z]',proposed))) == source['source_macros']
        assert (proposed==row['current_comparison_paragraph']) == (decision=='retention'), row['id']
        assert not any(row['review'].values()) and reason
        row.update(proposed_English=proposed,decision=decision,finding=reason,localization_note=reason,
            retention_reason=reason if decision=='retention' else '',contextual_comparison_saved=True,
            current_English_unconsulted=False,current_ROM_English_unconsulted=False,
            earlier_English_unconsulted=False,current_English_now_exposed=True,
            current_English_comparison_pending=False,names_terms_consumers_andfresh_display_approval_pending=True,
            source_draft_provenance=str(paths[0]),source_draft_provenance_sha256=digest(paths[0]))
        rows.append(row)
    counts = Counter(r['decision'] for r in rows)
    assert counts == {'revision':170,'retention':116}
    glyphs = [dict(id=r['id'],source_reference=r['source_reference'],current_reference=r['current_reference'],
        current=r['current_comparison_paragraph'],proposed=r['proposed_English'])
        for r in rows if not r['current_comparison_paragraph'].isascii()]
    save(out,dict(format='dk4-contextual-dialogue-proposals-v2',translation_policy='natural-dialogue-v2',target_locale='en-US',
        records=rows,records_count=286,complete_exchanges=14,revised=170,retained=116,
        current_ROM=current['current_ROM'],current_ROM_sha256=current['current_ROM_sha256'],runtime=current['runtime'],
        all286_contextual_comparisons_saved=True,all_five_gates_still_pending=True,
        names_roles_terms_consumers_andfresh_display_pending=True,glyph_consistency_targets=glyphs,
        current_English_intake_follows_sealed286_source_meanings_andindependent_drafts=True,
        original_drafts_andcurrent_native_bindings_preserved=True,no_ROM_orcompletion_credit_changes=True,new_credit=0,
        evidence={str(p):digest(p) for p in [*paths,*[Path(p.__file__) for p in [p1,p2,p3,p4,p5,p6]],Path(__file__)]}))
    save(ROOT/'contextual_proposals_qualification_v1.json',dict(records=286,complete_exchanges=14,
        revisions=170,justified_retentions=116,remaining_comparisons=0,
        native_macro_occurrences=sum(sum(r['source_macros'].values()) for r in rows),
        current_nonASCII_record_targets=len(glyphs),all_proposed_ASCII_not_font_approval=True,
        all_exact_source_current_references_preserved=True,all_five_gates_pending=True,
        new_credit=0,full_goal_complete=False,proposals_sha256=digest(out)))
    print('Saved286 contextual proposals:170 revisions/116 justified retentions;glyph targets',len(glyphs),';zero credit.')

if __name__=='__main__':
    main()
