"""Reuse calibrated consumer formatting for this source-bound 144-record manuscript."""
import argparse
import inspect
from dataclasses import replace
from pathlib import Path
from types import FunctionType

from dk4tool.dialogue.profiles import get_dialogue_profile
from scripts import plan_Hodram_B61_B70_v8893 as previous
from scripts.audit_story_glyph_consistency import load, save
from scripts.source_locked_derivation_v5118 import checked_text
from dk4tool.patch.grand_race_menu_release import sha

DOC = Path('translations/hodram_B71_B80_editorial_manuscript_v1.json')
document = load(DOC)
SELECTORS = [1,3,10,16,18,24,34,43,78,115,156]
NATIVE_LITERALS = {r['id']:dict(source_hex=r['source_hex'],current_hex=r['current_hex'],
    english=r['english'],prior=r['prior_macro_normalized_comparison'])
    for r in document['records'] if any(ord(c)>127 for c in r['english'])}
assert all(v['english']==v['prior'] or key=='DK4_MES_B79_R0005' and
    v['prior']=='…？' and v['english']=='…?' for key,v in NATIVE_LITERALS.items())

def source_bound_existing_literal(row, body):
    binding = NATIVE_LITERALS.get(row['id'])
    return binding is not None and binding == dict(source_hex=row['source_hex'],
        current_hex=row['current_hex'],english=body,prior=row['prior_macro_normalized_comparison'])

def get_profile(row):
    assert (row['kind']=='progressive' and row['source_selector'] in SELECTORS) or (
        row['kind']=='system-FE' and row['source_selector']==254)
    profile = get_dialogue_profile('hodram-story-live')
    assert (profile.window_width_px,profile.max_lines,profile.default_ascii_width,
        profile.default_multibyte_width)==(216,4,6,12)
    assert profile.macro_ascii_lengths==dict(FI=6,FA=9,FO=15)
    assert profile.guard_linebreaks and profile.pair_phase_safe_breaks
    return replace(profile,leading_speaker_bytes=frozenset({row['source_selector']}))

ADAPTER = checked_text(previous.ADAPTER,{
    'row[\'source_selector\'] in [1,2,3,9,10,16,17,18,20,23,24,38,78,105,116,154]':
        "row['source_selector'] in SELECTORS",
    'Hodram B61-B70 plan:':'Hodram B71-B80 plan:',
    'Hodram-B61-B70-RESEARCH-ONLY:':'Hodram-B71-B80-RESEARCH-ONLY:',
    'if result is None:limit=8;solve.cache_clear();result=solve(0,0)':
        'if result is None or result[0][0]>0:limit=8;solve.cache_clear();result=solve(0,0)',
})
PAIRS = previous.PAIRS | {('new','world'),('trading','rights'),('christian','nations'),
    ('feeling','the'),('the','heat'),('king','of'),('of','legend'),('take','the'),
    ('the','field'),('commander','in'),('in','chief'),('pirate','fleet'),('my','father'),
    ('two','or'),('or','three'),('three','years'),('that','tone'),('at','all'),
    ("can't",'face'),('face','my'),('why','not'),('not','head'),('head','back'),
    ("don't",'get'),('get','so'),('so','worked'),('worked','up'),
    ('here','is'),('place','is'),('pride','of')}
# Do not force king/of away from an otherwise readable ordinary boundary.
PAIRS.discard(('king','of'))
ENV = {**previous.ENV,'get_profile':get_profile,'SELECTORS':SELECTORS,
    'PAIRS':PAIRS,'source_bound_existing_literal':source_bound_existing_literal}
exec(compile(ADAPTER,__file__+'::calibrated-planner','exec'),ENV)
plan = ENV['plan']
base_qa = FunctionType(previous.base_qa.__code__,{**previous.base_qa.__globals__,
    'get_profile':get_profile},argdefs=previous.base_qa.__defaults__)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    assert not args.out.exists()
    rows,failures=[],[]
    for row in document['records']:
        try:
            assert not row['review']['formatting']
            planning={**row,'english':row['planned_English_markup']}
            result=plan(planning)
            assert ' '.join(result['lines'])==row['english']
            raw=bytes.fromhex(result['encoded_hex'])
            assert raw[0]==row['source_selector'] and b'\0' not in raw[1:]
            qa=base_qa(planning,result)
            result.update(file_path=row['file_path'],block=row['block'],
                source_record_index=row['source_record_index'],source_selector=row['source_selector'],
                kind=row['kind'],logical_English=row['english'],planning_record=planning,base_QA=qa)
            rows.append(result)
        except (ValueError,AssertionError) as exc:
            failures.append(dict(id=row['id'],error_type=type(exc).__name__,error=str(exc)))
    args.out.mkdir(parents=True)
    save(args.out/'automatic_plans.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        records=rows,failures=failures,source_owned_planner=ADAPTER,
        source_owned_profile_function=inspect.getsource(get_profile),
        source_owned_literal_predicate=inspect.getsource(source_bound_existing_literal),
        exact_source_literal_bindings=NATIVE_LITERALS,coherent_pairs=sorted(PAIRS),
        calibrated_dependency_reference=str(previous.MEASUREMENT),
        calibrated_dependency_sha256=sha(previous.MEASUREMENT.read_bytes()),
        preserved_native_guard_pair_phase_font_macro_metrics_andfull_usable_width=True,
        FE_short_notice_only_no_new_FE_macro=True,no_prose_shortened_for_fit=True,
        new_credit=0,native_visual_stored_actual_andregistered_release_pending=True,
        evidence={str(p):sha(p.read_bytes()) for p in [DOC,Path(previous.__file__),Path(__file__)]}))
    issues=[dict(id=r['id'],**issue) for r in rows for issue in r['base_QA']['issues']]
    save(args.out/'diagnostics.json',dict(issues=issues,failures=failures))
    print(dict(records=len(rows),pages=sum(r['expected_native_pages'] for r in rows),
        issues={severity:sum(i['severity']==severity for i in issues) for severity in ['error','warning','info']},
        failures=failures))
    assert not failures and len(rows)==144
    assert not any(i['severity'] in ['error','warning'] for i in issues)

if __name__=='__main__':
    main()
