"""Calibrated full-width automatic speech plans; typed captions have a separate consumer."""
import argparse
import inspect
from dataclasses import replace
from pathlib import Path
from types import FunctionType
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
from scripts import plan_hodram_B71_B80 as previous
from scripts.audit_story_glyph_consistency import load,save
from scripts.source_locked_derivation_v5118 import checked_text

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manuscript',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args();assert not args.out.exists()
    doc=load(args.manuscript)
    source_rows=[r for r in doc['records'] if r['kind'] in ['progressive','system-FE']]
    assert len(source_rows)==doc['physical_speech_objects']
    selectors=sorted({r['source_selector'] for r in source_rows if r['kind']=='progressive'})
    native_literals={r['id']:dict(source_hex=r['source_hex'],current_hex=r['current_hex'],
        english=r['english'],prior=r['prior_macro_normalized_comparison']) for r in source_rows if any(ord(c)>127 for c in r['english'])}
    assert all(row['english']==row['prior'] for row in native_literals.values())
    def source_bound_existing_literal(row,body):
        return native_literals.get(row['id'])==dict(source_hex=row['source_hex'],current_hex=row['current_hex'],
            english=body,prior=row['prior_macro_normalized_comparison'])
    def get_profile(row):
        assert (row['kind']=='progressive' and row['source_selector'] in selectors) or (row['kind']=='system-FE' and row['source_selector']==254)
        profile=get_dialogue_profile('hodram-story-live')
        assert profile.window_width_px==216 and profile.max_lines==4 and profile.default_ascii_width==6 and profile.default_multibyte_width==12
        assert profile.macro_ascii_lengths==dict(FI=6,FA=9,FO=15) and profile.guard_linebreaks and profile.pair_phase_safe_breaks
        return replace(profile,window_width_px=228 if row['kind']=='system-FE' else 216,
            leading_speaker_bytes=frozenset({row['source_selector']}))
    adapter=checked_text(previous.ADAPTER,{
        'cells=36;limit=4;':"cells=38 if row['kind']=='system-FE' else 36;limit=4;",
        'Hodram B71-B80 plan:':'Hodram complete-exchange plan:',
        'Hodram-B71-B80-RESEARCH-ONLY:':'Hodram-complete-exchange-RESEARCH-ONLY:',
        "if not final and words[stop-1]=='I':continue":
            "if not final and words[stop-1].endswith(('I','F')):continue",
    })
    pairs=previous.PAIRS|{('proof','of'),('of','conquest'),('indian','ocean'),('black','sea'),
        ('military','investment'),('cargo',"holds'"),('golden','crown'),('of','silla'),
        ('back','of'),('my','blade'),('sword','matches'),('world','by'),('by','sea'),
        ('give','up'),('hold','on'),('port','office'),('i','wish'),('i','shall'),('i','can'),
        ('i','could'),('i','might'),('i','would'),('will','you'),("won't",'you'),('do','you'),
        ('fear','of'),('of','the'),('the','sea'),('sea','>'),('>','cristina'),('sea','<'),('<','cristina'),
        ('wrong','idea'),('like','that'),('for','it'),('as','well'),('on','purpose')}
    env={**previous.ENV,'SELECTORS':selectors,'PAIRS':pairs,'get_profile':get_profile,
        'source_bound_existing_literal':source_bound_existing_literal}
    exec(compile(adapter,__file__+'::same-guard-phase-planner','exec'),env)
    plan=env['plan']
    base_qa=FunctionType(previous.base_qa.__code__,{**previous.base_qa.__globals__,'get_profile':get_profile},argdefs=previous.base_qa.__defaults__)
    rows,failures=[],[]
    for row in source_rows:
        try:
            assert not row['review']['formatting']
            planning={**row,'english':row['planned_English_markup']}
            result=plan(planning)
            assert ' '.join(result['lines'])==row['english']
            raw=bytes.fromhex(result['encoded_hex']);assert raw[0]==row['source_selector'] and b'\0' not in raw[1:]
            if row['kind']=='system-FE':assert len(result['lines'])<=4 and result['expected_native_pages']==1
            result.update(file_path=row['file_path'],block=row['block'],source_record_index=row['source_record_index'],
                source_selector=row['source_selector'],kind=row['kind'],logical_English=row['english'],
                planning_record=planning,base_QA=base_qa(planning,result),
                original_usable_width_px=228 if row['kind']=='system-FE' else 216)
            rows.append(result)
        except (ValueError,AssertionError) as error:
            failures.append(dict(id=row['id'],error_type=type(error).__name__,error=str(error)))
    issues=[dict(id=row['id'],**issue) for row in rows for issue in row['base_QA']['issues']]
    args.out.mkdir(parents=True)
    save(args.out/'automatic_plans.json',dict(manuscript=str(args.manuscript),manuscript_sha256=sha(args.manuscript.read_bytes()),
        records=rows,failures=failures,source_owned_planner=adapter,source_owned_profile_function=inspect.getsource(get_profile),
        source_owned_literal_predicate=inspect.getsource(source_bound_existing_literal),exact_literal_bindings=native_literals,
        coherent_pairs=sorted(pairs),progressive_width_px=216,FE_original_width_px=228,
        FE_geometry_source='scripts/Rafael_B45_FE_source_painter_v7894.py:source-proven context/view228x48,6x12 metrics andfour original logical rows',
        typed_choice_labels_not_formatted_as_speech=doc['typed_choice_objects'],
        no_prose_shortened_no_manual_breaks_no_font_viewport_orengine_changes=True,
        native_pixels_visual_stored_actual_andregistered_release_pending=True,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [args.manuscript,Path(previous.__file__),Path(__file__),Path('scripts/Rafael_B45_FE_source_painter_v7894.py')]}))
    save(args.out/'diagnostics.json',dict(issues=issues,failures=failures))
    print(dict(records=len(rows),pages=sum(r['expected_native_pages'] for r in rows),
        issues={severity:sum(i['severity']==severity for i in issues) for severity in ['error','warning','info']},failures=failures))
    assert len(rows)==len(source_rows) and not failures
    assert not any(i['severity'] in ['error','warning'] for i in issues)

if __name__=='__main__':main()
