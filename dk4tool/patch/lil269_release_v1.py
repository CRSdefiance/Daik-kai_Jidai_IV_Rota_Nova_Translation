"""Pure269-object SC2 transaction with complete read-only research rehearsal."""
from pathlib import Path
from dk4tool.patch import maria301_release_v2 as previous
from scripts import finalize_lil269_research_v1 as finisher
from scripts.source_locked_derivation_v5118 import checked_text

load, sha, require = previous.env['load'], previous.env['sha'], previous.env['require']
BLOCKS = list(range(243, 283))
FINISHER = Path('scripts/finalize_lil269_research_v1.py')
replay_source = checked_text(finisher.source, {
    'assert not any(p.exists() for p in [FINAL, NAMES, OUT])': 'assert all(p.exists() for p in [FINAL, NAMES, OUT])',
    '    OUT.mkdir()\n    save(FINAL, doc)\n    save(NAMES, names)': '    assert load(FINAL) == doc\n    assert load(NAMES) == names',
    '    save(source_plan, final_plan)': '    assert load(source_plan) == final_plan',
    "    save(OUT/'research_completion.json', dict(": '    expected_completion = dict(',
    'Path(__file__)]}))': "Path(__file__)]})\n    assert load(OUT/'research_completion.json') == expected_completion",
    "    print('Sealed269 five-gate reviews and25 scoped names:104 revisions/165 retentions. Registration/once-only credit remain.')": '',
})
require('save(' not in replay_source and 'mkdir(' not in replay_source, 'read-only complete research rehearsal')
replay_env = {'__file__': str(FINISHER.resolve()), '__name__': 'lil269_complete_research_rehearsal'}
exec(compile(replay_source, str(FINISHER) + '::pure-exact-artifact-rehearsal', 'exec'), replay_env)


def qualify_evidence(conf, doc, stored):
    require(tuple(conf[k] for k in ['record_count', 'speech_count', 'ordinary_count', 'style_count', 'typed_choice_count',
        'menu_count', 'scoped_name_count', 'native_pages', 'relative_cases', 'FE_count', 'actual_frames'])
        == (269, 262, 246, 16, 7, 3, 25, 264, 990, 36, 64563), 'exact mixed source/native scope')
    require(doc['blocks'] == conf['reviewed_blocks'] == conf['blocks'] == BLOCKS, '40 complete reviewed exchanges')
    require(conf['captain'] == 2 and conf['FE_owner_IDs'] == [], 'Lil route without new continuation controls')
    ready, sealed = map(load, [conf['research_completion'], conf['sealed_inputs']])
    require(ready['manuscript'] == conf['manuscript'] and ready['manuscript_sha256'] == sha(Path(conf['manuscript']).read_bytes()), 'exact sealed final review')
    require(sealed['research_completion_sha256'] == sha(Path(conf['research_completion']).read_bytes()), 'sealed research identity')
    for key in ['manuscript', 'plan', 'reconstruction', 'stored_native', 'stored_lookup', 'loaders', 'compiled_native',
        'typed_menu', 'native_styles', 'actual', 'visual_review', 'scoped_names']:
        require(sealed['inputs'][key] == dict(path=conf[key], sha256=sha(Path(conf[key]).read_bytes())), 'sealed ' + key)
    replay_env['main']()
    native, names, rebuilt = map(load, [conf['compiled_native'], conf['scoped_names'], conf['reconstruction']])
    require(names == load(ready['names']) and sha(Path(conf['scoped_names']).read_bytes()) == ready['names_sha256'], '25 scoped name reviews')
    require(stored == load(sealed['inputs']['stored_native']['path']), 'exact stored evidence')
    require(native['runtime']['candidate_sha256'] == conf['parent_ROM_sha256']
        and native['runtime']['ARM9_sha256'] == conf['pre_runtime_ARM9_sha256'], 'exact parent runtime')
    require(load(conf['plan'])['manuscript_sha256'] == sha(Path(conf['manuscript']).read_bytes()), 'final source plan')
    require(sum(bytes.fromhex(r['stored_hex'])[0] == 254 for r in stored['records']) == 36, '36 complete original FE panels')
    require(max(r['target_bytes'] for r in rebuilt['groups']) <= 9216 and not any(r.get('qa_waivers') for r in doc['records']), 'allocation without waivers')
    parent = previous.env['NdsImage'].open(conf['parent_ROM'])
    require(sha(parent.read_file('/GRP/KANJI.FNT')) == native['font_sha256'], 'unchanged native font')
    for index in range(3):
        path = Path('work/Lil269_B243_B282_clean_20261110') / f'display_run{index}_v1/run_plan.json'
        require(conf['dependencies'].get(str(path)) == sha(path.read_bytes()), 'frozen actual run plan')
        plan = load(path)
        fixture = load(plan['fixture'])
        require(sha(Path(plan['fixture']).read_bytes()) == plan['fixture_sha256']
            and fixture['QA_block_inside_original_stack_buffer'] and fixture['padded_QA_block_bytes'] <= 9216, 'bounded exact fixture')
        require(fixture['all_original_host_nonspeech_setup_effects_andcleanup_after_first_speech_retained']
            and len(fixture['original_initializers']) + len(fixture['source_bound_QA_host_opening_exit']) == 41, 'complete native Lil host')


source = checked_text(previous.previous.source, {
    "'dk4-reviewed-maria301-release-v1'": "'dk4-reviewed-lil269-release-v1'",
    "len(styles['objects']) == 1": "len(styles['objects']) == 2",
    "path == '/data/SC3.DK4'": "path == '/data/SC2.DK4'",
    'len(clean_blocks) == 303': 'len(clean_blocks) == 336',
    'native_loads=303': 'native_loads=336',
})
env = {**previous.env, 'qualify_evidence': qualify_evidence, '__file__': __file__}
exec(compile(source, __file__ + '::same-complete-source-current-transaction-andwhole-inverses', 'exec'), env)
plan_release = env['plan_release']
