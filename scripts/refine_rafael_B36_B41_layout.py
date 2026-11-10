"""Record direct visual wrap findings and prepare only changed native-page inputs."""
import argparse
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Rafael_B36_B41_formatting_20261104')
DOC=ROOT/'formatting_input.json'
INITIAL=ROOT/'initial_plans_v1/automatic_plans.json'
NATIVE=Path('work/analysis/Rafael_B36_B41_native_20261104/initial_v1/compiled_native_pages.json')


def preferences():
    output=ROOT/'visual_preferences_v2.json'
    assert not output.exists()
    doc,plans,native=map(load,[DOC,INITIAL,NATIVE])
    assert native['pages']==177 and len(native['records'])==175
    assert native['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass']
    rows={r['id']:r for r in doc['records']}
    old={r['id']:r for r in plans['records']}
    settings={
        'DK4_MES_B36_R0046':dict(ordinary_boundaries=[['hm','those']],reason='The four-character Hm?! opening wastes a row; allow the opening reaction to share a line with the identification while retaining the Algiers pirates phrase.'),
        'DK4_MES_B37_R0254':dict(one_page=True,reason='The initial five-row result strands for needless trouble on page two. Test an ordinary four-row plan without shortening the125-character paragraph or weakening QA.'),
        'DK4_MES_B37_R0267':dict(ordinary_boundaries=[['you','my']],reason='Allow a normal boundary after the complete conditional Spanish attack you, before the main clause; the initial84-character paragraph uses four sparse rows.'),
        'DK4_MES_B41_R0131':dict(page_clause='teach them',reason='The145-character paragraph cannot fit the141 visible cells of one native page. Keep the complete final action teach them a lesson together after the page turn instead of stranding only a lesson.'),
    }
    for ident,item in settings.items():
        item.update(bindings={k:sha(rows[ident][k].encode('utf-8')) for k in ['source_hex','current_hex','english']},initial_lines=old[ident]['lines'])
    sheets=[dict(**s,directly_viewed=True) for s in native['review_sheets']]
    assert len(sheets)==17 and sum(s['pages'] for s in sheets)==177
    assert all(sha(Path(s['path']).read_bytes())==s['sha256'] for s in sheets)
    save(output,dict(records=settings,all177_initial_pages_directly_viewed=True,directly_viewed_sheets=sheets,
        native=str(NATIVE),native_sha256=sha(NATIVE.read_bytes()),initial_plan=str(INITIAL),initial_plan_sha256=sha(INITIAL.read_bytes()),
        no_prose_shortening_authored_breaks_geometry_orQA_waivers=True,normal_ASCII_I_andcomplete_FU_viewed=True,new_credit=0,guide_photos=False))
    print('Four observed layout findings bound;all177 initial pages directly viewed;fresh plans required.')


def preferences_v3():
    original=ROOT/'visual_preferences_v2.json'
    output=ROOT/'visual_preferences_v3.json'
    assert not output.exists()
    doc=deepcopy(load(original))
    opening=doc['records']['DK4_MES_B36_R0046']
    opening.pop('ordinary_boundaries')
    opening['coherent_pairs']=[['hm','those']]
    opening['reason']='Keep Hm?! with the following identification rather than on a four-character opening row. This is an ordinary coherent pair, not an authored line break.'
    page=doc['records']['DK4_MES_B37_R0254']
    page.pop('one_page')
    page['page_clause']='I have no patience'
    page['reason']='The tested one-page attempt ends a row with for and correctly fails QA. Keep the complete closing sentence on page two instead; preserve prose and all QA rules.'
    doc.update(previous_preferences=str(original),previous_preferences_sha256=sha(original.read_bytes()),
        rejected_one_page_plan=str(ROOT/'visual_plans_v2/automatic_plans.json'),no_warning_waived=True)
    save(output,doc)
    print('Preserved the rejected one-page attempt;full closing sentence andcoherent opening are required instead.')


def subset():
    out=ROOT/'changed_native_inputs_v3'
    assert not out.exists()
    final=ROOT/'visual_plans_v3/automatic_plans.json'
    doc,plans,initial=map(load,[DOC,final,INITIAL])
    assert not plans['failures'] and not any(i['severity'] in ['warning','error'] for r in plans['records'] for i in r['base_QA']['issues'])
    old={r['id']:r for r in initial['records']}
    changed={r['id'] for r in plans['records'] if r['encoded_hex']!=old[r['id']]['encoded_hex']}
    assert changed and changed<={*load(ROOT/'visual_preferences_v3.json')['records']}
    subset=deepcopy(doc)
    subset.update(records=[r for r in doc['records'] if r['id'] in changed],physical_speech_objects=len(changed),ordinary_speech_objects=len(changed),
        subset_of=str(DOC),subset_of_sha256=sha(DOC.read_bytes()))
    out.mkdir()
    manuscript=out/'changed_records.json'
    save(manuscript,subset)
    tested=deepcopy(plans)
    tested.update(records=[r for r in plans['records'] if r['id'] in changed],manuscript=str(manuscript),manuscript_sha256=sha(manuscript.read_bytes()),
        full_plan=str(final),full_plan_sha256=sha(final.read_bytes()))
    save(out/'changed_plans.json',tested)
    print('Fresh native subset',sorted(changed),'unchanged record proofs',175-len(changed))


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('stage',choices=['preferences','preferences_v3','subset'])
    globals()[ap.parse_args().stage]()
