"""Plan both complete scenes and isolate the 69 records requiring fresh native checks."""
import inspect
from pathlib import Path
import sys
from types import FunctionType

from dk4tool.patch.grand_race_menu_release import sha
from scripts import check_rafael_B168_pages_on1860_v1 as b168
from scripts import check_rafael_B166_B167_ordinary_v1 as native
from scripts import plan_rafael_B166_B167_ordinary_v1 as planning
from scripts import write_rafael_B169_contextual_v1 as b169
from scripts.audit_story_glyph_consistency import load, save
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = b168.A / 'Rafael_B168_B169_current1860_20261105'
CURRENT = ROOT / 'current_effective.json'
IDENTITY = ROOT / 'names_and_terms.json'
MANUSCRIPT = ROOT / 'formatting_manuscript_v1.json'
PREFERENCES = ROOT / 'visual_preferences_v1.json'
PLAN = ROOT / 'plans_v1/automatic_plans.json'
DELTA_M = ROOT / 'delta_manuscript_v1.json'
DELTA_P = ROOT / 'delta_plan_v1.json'
SPARSE = 'DK4_MES_B168_R0114'


def digest(path):
    return sha(Path(path).read_bytes())


def prepare():
    assert not ROOT.exists()
    older, new = map(load, (b168.CURRENT, b169.CURRENT))
    assert all(older[k] == new[k] for k in ('current_ROM', 'current_ROM_sha256', 'runtime', 'current_archive_sha256'))
    assert older['all_source_preambles_andcommand_kinds_preserved'] and new['all_source_preambles_andcommand_kinds_preserved']
    assert (older['records'], new['records']) == (47, 68)
    i1, i2 = map(load, (b168.IDENTITY, b169.IDENTITY))
    assert i1['runtime'] == i2['runtime'] == older['runtime']
    by_actor = {r['actor_ID']: r for r in i1['name_bindings']}
    for row in i2['name_bindings']:
        actor = row['actor_ID']
        if actor in by_actor:
            assert all(row[k] == by_actor[actor][k] for k in row.keys() - {'fresh'})
        by_actor[actor] = row
    assert {0, 5, 6, 15, 21, 92, 96, 152, 164, 165} <= set(by_actor)
    ROOT.mkdir()
    save(CURRENT, {**older, 'groups': older['groups'] + new['groups'], 'records': 115, 'original_current_catalogue_lookups': 115,
                   'bound_per_block_proofs': {str(p): digest(p) for p in (b168.CURRENT, b169.CURRENT)}})
    save(IDENTITY, {**i2, 'actors': sorted(by_actor), 'name_bindings': list(by_actor.values()),
                    'evidence': {**i1['evidence'], **i2['evidence']}})
    part1, part2 = map(load, (b168.MANUSCRIPT, b169.OUT))
    prefs = load(b168.PRIOR / 'visual_preferences_v3.json')
    row = next(r for r in part1['records'] if r['id'] == SPARSE)
    assert row['english'] == "...You're pretty strange yourselves. I'm Angelo Puccini."
    replacement = "...You're an odd bunch, too. I'm Angelo Puccini."
    note = "Keep Angelo's pause, reciprocal tease and full introduction. The shorter idiom keeps his thought together in the native window."
    row.update(english=replacement, editorial_logical_English=replacement, planned_English_markup='{SPEAKER:0F}'+replacement,
               finding=note, localization_note=note, visual_revision_previous_English="...You're pretty strange yourselves. I'm Angelo Puccini.")
    prefs['records'][SPARSE] = dict(line_phrases=["You're an odd bunch, too.", "I'm Angelo Puccini."], reason=note,
        bindings={k: sha(row[k].encode('utf-8')) for k in ('source_hex', 'current_hex', 'english')})
    for row in part2['records']:
        assert not row['native_literal_tokens']
        row['editorial_logical_English'] = row['english']
        row['planned_English_markup'] = '{SPEAKER:'+format(row['source_selector'], '02X')+'}'+row['english']
        row['prior_macro_normalized_comparison'] = None if row['english'].isascii() else row['current_comparison_paragraph']
    rows = part1['records'] + part2['records']
    assert len(rows) == 115 and sum(len(r['native_literal_tokens']) for r in rows) == 4
    save(PREFERENCES, prefs)
    save(MANUSCRIPT, {**part1, 'blocks': [168, 169], 'records': rows, 'source_objects': 115, 'physical_speech_objects': 115,
                      'ordinary_speech_objects': 115, 'proposed_revisions': 90, 'justified_retentions': 25,
                      'scoped_identity_proof_sha256': digest(IDENTITY), 'no_prose_changes_or_manual_breaks': False,
                      'single_B168_read_aloud_refinement_and_no_manual_breaks': SPARSE,
                      'current_glyph_defect_records': part1['current_glyph_defect_records']+part2['current_glyph_defect_records'],
                      'rebound_current_effective_evidence': str(CURRENT),
                      'evidence': {**part1['evidence'], **part2['evidence'], str(b168.MANUSCRIPT): digest(b168.MANUSCRIPT),
                                   str(b169.OUT): digest(b169.OUT), str(Path(__file__)): digest(Path(__file__))}})


def isolate():
    doc, plan, old = map(load, (MANUSCRIPT, PLAN, b168.PLAN))
    assert not DELTA_M.exists() and not DELTA_P.exists()
    assert plan['manuscript_sha256'] == digest(MANUSCRIPT) and not plan['failures']
    assert len(doc['records']) == len(plan['records']) == 115
    before = {r['id']: r for r in old['records']}
    delta = []
    for row in plan['records']:
        if row['id'] not in before or row['id'] == SPARSE:
            delta.append(row)
            continue
        expected = before[row['id']]
        assert all(row[k] == expected[k] for k in ('encoded_hex', 'lines', 'expected_native_pages', 'base_QA')), row['id']
    assert len(delta) == 69 and sum(r['block'] == 168 for r in delta) == 1
    chosen = {r['id'] for r in delta}
    save(DELTA_M, {**doc, 'records': [r for r in doc['records'] if r['id'] in chosen],
                   'physical_speech_objects': 69, 'ordinary_speech_objects': 69})
    save(DELTA_P, {**plan, 'records': delta, 'manuscript': str(DELTA_M), 'manuscript_sha256': digest(DELTA_M),
                   'complete_plan_sha256': digest(PLAN), 'reused46_prior_native_exact_encodings': True})
    print('46 prior body proofs remain exact. Fresh native scope contains 69 records.')


scope = checked_text(inspect.getsource(planning.qualify_source), {
    "doc['blocks']==[166,167]": "doc['blocks']==[168,169]", 'len(bindings)==164': 'len(bindings)==115',
})
scope_env = {**planning.qualify_source.__globals__, 'CURRENT': CURRENT, 'IDENTITY': IDENTITY}
exec(compile(scope, __file__+'::exact-115-source-bindings', 'exec'), scope_env)


if __name__ == '__main__':
    if sys.argv[1:] == ['--prepare']:
        prepare()
    elif sys.argv[1:] == ['--isolate']:
        isolate()
    elif sys.argv[1] == '--native':
        del sys.argv[1]
        FunctionType(native.env['main'].__code__, {**native.env, 'IDENTITY': IDENTITY, '__file__': __file__})()
    else:
        FunctionType(planning.env['main'].__code__, {**planning.env, 'qualify_source': scope_env['qualify_source'], '__file__': __file__})()
