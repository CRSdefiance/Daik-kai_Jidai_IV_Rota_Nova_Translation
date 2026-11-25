"""Rebind B168 to Rafael1860 and run the original complete native page checks."""
from pathlib import Path
from types import FunctionType

from dk4tool.patch.grand_race_menu_release import sha
from scripts import check_rafael_B166_B167_ordinary_v1 as native
from scripts.audit_story_glyph_consistency import load, save
from scripts.plan_rafael_B168_ordinary_v1 import FORMATTING, ROOT as PRIOR
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime


A = Path('work/analysis')
ROOT = A / 'Rafael_B168_current1860_20261105'
CURRENT = ROOT / 'current_effective.json/current_effective.json'
RELEASE = A / 'Rafael1860_extended_release_verified_v1_20261105/registered_release_verification.json'
STARTUP = RELEASE.with_name('own_registered_startup_verification.json')
IDENTITY = ROOT / 'native_identity_v1.json'
MANUSCRIPT = ROOT / 'formatting_manuscript_v1.json'
PLAN = ROOT / 'rebound_automatic_plans_v1.json'


def rebind():
    assert not any(p.exists() for p in (IDENTITY, MANUSCRIPT, PLAN))
    older = PRIOR / 'current_effective.json'
    old, new = map(load, (older, CURRENT))
    assert old['original_current_catalogue_lookups'] == new['original_current_catalogue_lookups'] == 47
    expected, actual = old['groups'][0], new['groups'][0]
    assert expected['block'] == actual['block'] == 168 and expected.keys() == actual.keys()
    assert all(expected[k] == actual[k] for k in expected.keys() - {'records'})
    for old_record, current_record in zip(expected['records'], actual['records'], strict=True):
        assert old_record.keys() == current_record.keys()
        assert all(old_record[k] == current_record[k] for k in old_record.keys() - {'selected_native_pointer'})
    ctx = RegisteredRuntime(RELEASE, STARTUP, captain=0)
    last = old['runtime']
    prior = RegisteredRuntime(last['release_proof'], last['startup_proof'], captain=0)
    assert ctx.receipt() == new['runtime']
    assert ctx.release['parent_sha256'] == old['current_ROM_sha256'] and ctx.release['only_owned_SC0_blocks_changed'] == [166, 167]
    assert (ctx.arm, ctx.common, ctx.actor_root, ctx.actor_bytes) == (prior.arm, prior.common, prior.actor_root, prior.actor_bytes)
    assert ctx.image.read_file('/GRP/KANJI.FNT') == prior.image.read_file('/GRP/KANJI.FNT')
    identity = load(native.planning.IDENTITY)
    assert identity['runtime'] == last and identity['exact_unchanged_actor0_macro_dependencies']
    hashes = {str(p): sha(p.read_bytes()) for p in (older, CURRENT, native.planning.IDENTITY, Path(__file__))}
    save(IDENTITY, {**identity, 'runtime': ctx.receipt(), 'evidence': {**identity['evidence'], **hashes},
                    'exact_prior_B168_group_and_all_47_records_except_volatile_RAM_pointer': True})
    doc = load(FORMATTING)
    plan_path = PRIOR / 'ordinary_plans_v3/automatic_plans.json'
    plan = load(plan_path)
    assert doc['runtime'] == last and plan['manuscript_sha256'] == sha(FORMATTING.read_bytes())
    assert len(doc['records']) == len(plan['records']) == 47 and not plan['failures']
    for row, reference in zip(doc['records'], actual['records'], strict=True):
        for k in ('id', 'source_reference', 'current_reference', 'source_hex', 'current_effective_hex'):
            assert row[k] == reference[k], (row['id'], k)
    save(MANUSCRIPT, {**doc, **{k: new[k] for k in ('current_ROM', 'current_ROM_sha256', 'current_archive_sha256', 'runtime')},
                     'scoped_identity_proof_sha256': sha(IDENTITY.read_bytes()),
                     'rebound_current_effective_evidence': str(CURRENT)})
    save(PLAN, {**plan, 'manuscript': str(MANUSCRIPT), 'manuscript_sha256': sha(MANUSCRIPT.read_bytes()),
                'exact_prior_plan_sha256': sha(plan_path.read_bytes()), 'native_display_fresh_on_successor': True})
    print('Rebound all 47 B168 effective bodies, preambles and approved plans to Rafael1860.')


if __name__ == '__main__':
    import sys
    if sys.argv[1:] == ['--rebind']:
        rebind()
    else:
        FunctionType(native.env['main'].__code__, {**native.env, 'IDENTITY': IDENTITY, '__file__': __file__})()
