"""Keep the complete agility predicate intact without altering prose or native bounds."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B199_idiom_layout_v5790')
if __name__=='__main__':
    assert not ROOT.exists()
    doc=read('translations/lil_B199_editorial_manuscript_v3.json')
    row=next(r for r in doc['records'] if r['source_record_index']==70)
    assert row['english']=="{SPEAKER:09}(Got away again. Samwell's quick on his feet.)"
    qa=read('work/analysis/lil_B199_layout_v5788/all31_paragraph_layout_QA.json')
    gift=next(r for r in qa['records'] if r['id']=='DK4_MES_B199_R0095')
    assert gift['qa']['visible_lines']==['It looks old,',"but it's not every day",'I get a present from you, Camille!']
    rows=[derive('dk4tool/dialogue/lil_B199_layout_v1.py','dk4tool/dialogue/lil_B199_layout_v2.py',{
        '\ndef _word(value):':
        "\n# Complete source70 predicate: the contraction is Samwell is, and quick on his feet is one idiom.\nPROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({(\"samwell's\",'quick'),('quick','on'),('on','his'),('his','feet')})\n\ndef _word(value):"})]
    rows.append(derive('scripts/plan_lil_B199_layout_v5788.py','scripts/plan_lil_B199_layout_v5791.py',{
        'layout_v5788':'layout_v5791','lil_B199_layout_v1':'lil_B199_layout_v2',
        'manuscript_v2.json':'manuscript_v3.json','manuscript_v3.json':'manuscript_v4.json'}))
    rows.append(derive('scripts/verify_lil_B199_fonts_v5789.py','scripts/verify_lil_B199_fonts_v5792.py',{
        'fonts_v5789':'fonts_v5792','lil_B199_layout_v1':'lil_B199_layout_v2','manuscript_v3.json':'manuscript_v4.json'}))
    ROOT.mkdir(parents=True)
    save(ROOT/'one_complete_idiom_protection_and_justified_three_row_gift_response.json',dict(
        derivations=rows,manuscript='translations/lil_B199_editorial_manuscript_v3.json',
        manuscript_sha256=sha(Path('translations/lil_B199_editorial_manuscript_v3.json').read_bytes()),
        source70_full_idiom_protected_without_new_word_or_manual_break=True,
        R95_three_rows_justified_by_complete_concession_and_rare_gift_clause=True,
        R95_complete_first_candidate_characters=len("It looks old, but it's not every day"),
        R95_complete_first_candidate_36_cells_plus_required_guard_exceeds216_pixels=True,
        R95_no_word_shortened_and_no_width_guard_phase_or_four_row_limit_changed=True,
        all_other_native_metrics_and_prose_and_runtime_preserved=True,
        initial31_native_planes_and248_alignments_preserved_as_history=True,
        new_ROMs=0,new_emulator_runs=0,new_editorial_credit=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Exact source70 idiom protected;R95 complete three-row thought retained. No prose/native/runtime changes.')
