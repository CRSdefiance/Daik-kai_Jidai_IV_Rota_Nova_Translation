"""Consolidate301 individually justified proposals andbind the Berio spelling tocurrent getters."""
from copy import deepcopy
from pathlib import Path
import re
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Maria_B0_B32_clean_20261109')


def main():
    out = ROOT / 'all301_contextual_proposals_v1.json'
    qualification = ROOT / 'all301_contextual_proposals_qualification_v1.json'
    assert not out.exists() and not qualification.exists()
    paths = [ROOT/f'contextual_proposals_{part}_v1.json' for part in ['B0_B10','B11_B21','B22_B32']]
    pieces = [load(p) for p in paths]
    rows = [deepcopy(r) for p in pieces for r in p['records']]
    drafts_path = ROOT/'all301_clean_meanings_andindependent_drafts_v1.json'
    drafts = load(drafts_path)
    byid = {r['id']:r for r in drafts['records']}
    assert len(rows)==len({r['id'] for r in rows})==len(byid)==301
    assert {r['id'] for r in rows}==byid.keys()
    assert all(p['current_ROM_sha256']==pieces[0]['current_ROM_sha256'] for p in pieces)
    names_path = ROOT/'scoped_names_items_macros_reference_v1.json'
    names = load(names_path)
    actor = next(r for r in names['records'] if r['actor_ID']==72)
    assert {c['text'] for c in actor['current_consumers']}=={'Hernan Berio'}
    amended = next(r for r in rows if r['id']=='DK4_MES_B11_R0004')
    assert amended['decision']=='revision' and 'Hernan Berrio' in amended['proposed_English']
    before = amended['proposed_English']
    amended['proposed_English'] = before.replace('Hernan Berrio','Hernan Berio')
    amended['finding'] = ('Make Maria’s challenge spoken and pointed, and reconcile the old Berrio spelling to '
        'the current source-bound Hernan Berio nameplate/catalogue. No new name or historical identity is invented.')
    amended['localization_note'] = amended['finding']
    amended['scoped_name_binding_amendment'] = dict(previous_proposal=before,
        actor_ID=72,evidence=str(names_path),evidence_sha256=digest(names_path))
    for row in rows:
        source = byid[row['id']]
        assert row['source_hex']==source['source_hex'] and row['source_reference']==source['source_reference']
        assert row['source_meaning']==source['source_meaning'] and row['whole_exchange_context']==source['whole_exchange_context']
        assert not any(row['review'].values()) and row['contextual_comparison_saved']
        assert row['finding'] and row['decision'] in ['revision','retention']
        english = row['proposed_English']
        assert english.isascii() and english==english.strip() and not any(s in english for s in ['\n','\r','\t','{LB','{PAD}','{ALIGN'])
        assert {t:english.count(t) for t in row['source_macros']}==row['source_macros']
        assert set(re.findall(r'F[A-Z]',english))==set(row['source_macros'])
        if row['decision']=='retention':
            assert english==row['current_comparison_paragraph'] and row['retention_reason']
    assert rows[:67]==pieces[0]['records']
    revisions = sum(r['decision']=='revision' for r in rows)
    assert (revisions,301-revisions)==(178,123)
    save(out,dict(records=rows,records_count=301,complete_exchanges=32,
        translation_policy='natural-dialogue-v2',target_locale='en-US',
        revised=178,retained=123,current_ROM=pieces[0]['current_ROM'],current_ROM_sha256=pieces[0]['current_ROM_sha256'],
        all301_contextual_comparisons_saved=True,all_five_gates_still_pending=True,
        source_meanings_drafts_andpartial_proposals_preserved=True,
        only_postcomparison_draft_amendment_is_bound_Berio_spelling=True,
        no_authored_linebreaks_orallocation_driven_shortening=True,
        names_roles_terms_andfresh_final_display_approval_pending=True,
        no_ROM_orcompletion_credit_changes=True,new_credit=0,
        evidence={str(p):digest(p) for p in [*paths,drafts_path,names_path,Path(__file__)]}))
    glyph_targets = [dict(id=r['id'],current=r['current_comparison_paragraph'],proposed=r['proposed_English'])
        for r in rows if not r['current_comparison_paragraph'].isascii()]
    save(qualification,dict(records=301,complete_exchanges=32,revisions=178,justified_retentions=123,
        all_exact_source_current_references_andmeanings_preserved=True,
        first67_proposals_byte_equivalent_as_objects=True,one_bound_name_amendment='DK4_MES_B11_R0004:Hernan Berio',
        logical_paragraphs_andnative_literal_substitutions_exact=True,
        glyph_consistency_targets=glyph_targets,all_final_proposed_paragraphs_ASCII=True,
        ASCII_checks_are_not_font_orcomplete_glyph_approval=True,
        all301=str(out),all301_sha256=digest(out),all_five_gates_pending=True,
        remaining_current_comparisons=0,new_credit=0,full_goal_complete=False))
    print('Consolidated301 contextual proposals:178 revisions/123 retentions;Berio bound;first67 unchanged;glyph targets',len(glyph_targets),';zero credit.')


if __name__=='__main__':
    main()
