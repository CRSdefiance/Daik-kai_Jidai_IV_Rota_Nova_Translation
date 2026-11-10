"""Pure321-source SC3 transaction with exact read-only research rehearsal."""
from pathlib import Path
from dk4tool.patch import maria301_release_v2 as previous
from scripts import finalize_maria321_research_v3 as finisher
from scripts.source_locked_derivation_v5118 import checked_text

load, sha, require = previous.env['load'], previous.env['sha'], previous.env['require']
BLOCKS = [196,197,198,199,200,201,202,203,204,206,208,209,210,211,212,213,214,215]
FINISHER = Path('scripts/finalize_maria321_research_v3.py')
replay_source = checked_text(finisher.source, {
    'assert not any(p.exists() for p in [FINAL, NAMES, OUT])':
        'assert all(p.exists() for p in [FINAL, NAMES, OUT])',
    '    OUT.mkdir()\n    save(FINAL, doc)\n    save(NAMES, names)':
        '    assert load(FINAL) == doc\n    assert load(NAMES) == names',
    '    save(source_plan, final_plan)': '    assert load(source_plan) == final_plan',
    "    save(OUT/'research_completion.json', dict(": '    expected_completion = dict(',
    'Path(__file__)]}))':
        "Path(__file__)]})\n    assert load(OUT/'research_completion.json') == expected_completion",
    "    print('Sealed321 five-gate reviews and24 scoped names:171 revisions/150 retentions. Registration/once-only credit remain.')": '',
})
require('save(' not in replay_source and 'mkdir(' not in replay_source, 'read-only complete research rehearsal')
replay_env = {'__file__':str(FINISHER.resolve()), '__name__':'maria321_complete_research_rehearsal'}
exec(compile(replay_source,str(FINISHER)+'::pure-exact-artifact-rehearsal','exec'),replay_env)


def qualify_evidence(conf, doc, stored):
    require(tuple(conf[k] for k in ['record_count','speech_count','ordinary_count','style_count','typed_choice_count',
        'menu_count','scoped_name_count','native_pages','relative_cases','FE_count','actual_frames'])
        == (321,317,296,21,4,2,24,325,120,2,73443), 'exact mixed source/native scope')
    require(doc['blocks']==conf['reviewed_blocks']==conf['blocks']==BLOCKS, '18 complete reviewed exchanges')
    require(conf['captain']==3 and conf['FE_owner_IDs']==[], 'route and no new continuation controls')
    ready, sealed = map(load,[conf['research_completion'],conf['sealed_inputs']])
    require(ready['manuscript']==conf['manuscript'] and ready['manuscript_sha256']==sha(Path(conf['manuscript']).read_bytes()), 'exact sealed final review')
    require(sealed['research_completion_sha256']==sha(Path(conf['research_completion']).read_bytes()), 'sealed research identity')
    for key in ['manuscript','plan','reconstruction','stored_native','stored_lookup','loaders','compiled_native',
        'typed_menu','native_styles','actual','visual_review','scoped_names']:
        require(sealed['inputs'][key]==dict(path=conf[key],sha256=sha(Path(conf[key]).read_bytes())), 'sealed '+key)
    replay_env['main']()
    native, names, reconstructed = map(load,[conf['compiled_native'],conf['scoped_names'],conf['reconstruction']])
    require(names==load(ready['names']) and sha(Path(conf['scoped_names']).read_bytes())==ready['names_sha256'], 'exact24 scoped name reviews')
    require(stored==load(sealed['inputs']['stored_native']['path']), 'exact stored evidence')
    require(native['runtime']['candidate_sha256']==conf['parent_ROM_sha256'] and native['runtime']['ARM9_sha256']==conf['pre_runtime_ARM9_sha256'], 'exact current runtime and parent')
    require(load(conf['plan'])['manuscript_sha256']==sha(Path(conf['manuscript']).read_bytes()), 'final source plan identity')
    require(sum(bytes.fromhex(r['stored_hex'])[0]==254 for r in stored['records'])==2, 'two complete original FE panels')
    require(max(r['target_bytes'] for r in reconstructed['groups'])<=9216 and not any(r.get('qa_waivers') for r in doc['records']), 'allocation and no QA waivers')
    parent = previous.env['NdsImage'].open(conf['parent_ROM'])
    require(sha(parent.read_file('/GRP/KANJI.FNT'))==native['font_sha256'], 'exact current native font')
    for index in range(3):
        path = Path('work/Maria_B196_B215_clean_20261110')/f'display_run_menu{index}_v1/run_plan.json'
        require(conf['dependencies'].get(str(path))==sha(path.read_bytes()), 'frozen actual run plan')
        plan = load(path)
        fixture = load(plan['fixture'])
        require(sha(Path(plan['fixture']).read_bytes())==plan['fixture_sha256'] and fixture['QA_block_inside_original_stack_buffer'] and fixture['padded_QA_block_bytes']<=9216, 'exact bounded initialized fixture')
        require(fixture['all_original_host_nonspeech_setup_effects_andcleanup_after_first_speech_retained'] and len(fixture['original_initializers'])+len(fixture['source_bound_QA_host_opening_exit'])==47, 'complete native QA host')


source = checked_text(previous.previous.source, {
    "'dk4-reviewed-maria301-release-v1'": "'dk4-reviewed-maria321-release-v1'",
    "len(styles['objects']) == 1": "len(styles['objects']) == 3",
})
env = {**previous.env, 'qualify_evidence':qualify_evidence, '__file__':__file__}
exec(compile(source,__file__+'::same-pure-complete-mixed-SC3-transaction-andinverses','exec'),env)
plan_release = env['plan_release']
