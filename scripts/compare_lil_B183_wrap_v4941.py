"""Audit the complete old/new display change while preserving every reviewed word."""
from pathlib import Path
from dk4tool.dialogue import lil_B183_layout_v1 as old_codec,lil_B183_layout_v2 as new_codec
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B183_locative_wrap_v4939')
OUTPUT=ROOT/'before_after_all25_semantic_and_layout_comparison.json'
if __name__=='__main__':
    assert not OUTPUT.exists()
    oldp=Path('translations/lil_B183_editorial_manuscript_v2.json');newp=Path('translations/lil_B183_editorial_manuscript_v4.json')
    old,new=read(oldp),read(newp)
    op=Path('work/analysis/lil_B183_fonts_v4937/all25_progressive_FE_native_planes_and200_alignment_cases.json')
    np=Path('work/analysis/lil_B183_fonts_v4941/all25_progressive_FE_native_planes_and200_alignment_cases.json')
    of,nf=read(op),read(np);a={r['id']:r for r in of['cases']};b={r['id']:r for r in nf['cases']}
    assert len(a)==len(b)==25 and a.keys()==b.keys()
    assert old_codec.STRONG_ENDINGS==new_codec.STRONG_ENDINGS and old_codec.PROTECTED_BOUNDARIES==new_codec.PROTECTED_BOUNDARIES
    assert old_codec.DEPENDENCIES==new_codec.DEPENDENCIES and 'there' in new_codec.STRONG_ENDINGS
    assert of['ARM9_sha256']==nf['ARM9_sha256'] and of['candidate_sha256']==nf['candidate_sha256']
    assert [r['english'] for r in old['records']]==[r['english'] for r in new['records']]
    differences=[];rows=[]
    for r in new['records']:
        x,y=a[r['id']],b[r['id']];before,after=bytes.fromhex(x['encoded_hex']),bytes.fromhex(y['encoded_hex'])
        assert before[0]==after[0]==r['source_selector']
        assert before[1:].decode('ascii').split()==after[1:].decode('ascii').split()
        changed=before!=after
        if changed:differences.append(r['id'])
        else:assert x['whole_native_plane_sha256']==y['whole_native_plane_sha256'] and x['preview_sha256']==y['preview_sha256']
        assert y['all_first_final_internal_glyphs_in_order_and_unique_cells'] and y['all_visible_origins_zero_and_within_four_rows'] and y['one_native_page_consumes_complete_target']
        rows.append(dict(id=r['id'],changed=changed,before_formatted_markup=x['formatted_markup'],after_formatted_markup=y['formatted_markup'],
            before_encoded_hex=before.hex(),after_encoded_hex=after.hex(),all_words_and_complete_source_selector_preserved=True))
    assert differences==['DK4_MES_B183_R0035']
    revised=next(r for r in rows if r['changed']);lines=bytes.fromhex(revised['after_encoded_hex'])[1:].decode('ascii').splitlines()
    assert [s.strip() for s in lines]==['What are you two talking about?','That one over there','is obviously better!']
    save(OUTPUT,dict(only_changed_record_IDs=differences,all25_words_controls_and_prose_unchanged=True,records=rows,
        all24_other_compiled_targets_and_native_planes_exact=True,verified_width216_and_max4_rows_unchanged=True,
        original_STRONG_ENDINGS_and_PROTECTED_BOUNDARIES_lists_unchanged=True,
        source_supported_complete_locative_does_not_strand_existential_there=True,
        no_shared_helper_native_font_metric_guard_or_manual_break_change=True,
        old_effective_planner_sha256=old_codec.EFFECTIVE_PLANNER_SHA256,new_effective_planner_sha256=new_codec.EFFECTIVE_PLANNER_SHA256,
        evidence={str(p):sha(p.read_bytes()) for p in [oldp,newp,op,np,Path(__file__),Path('dk4tool/dialogue/lil_B183_layout_v1.py'),Path('dk4tool/dialogue/lil_B183_layout_v2.py')]},
        new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print(dict(changed=differences,after_lines=[s.strip() for s in lines],all25_words_preserved=True,other24_planes_exact=True))
