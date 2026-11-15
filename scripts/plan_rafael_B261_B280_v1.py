"""Prepare and format all B261–B280 speech objects on the registered runtime."""
from pathlib import Path
from types import FunctionType

from scripts import plan_rafael_B121_B140_withstyles_v1 as planner
from scripts import plan_rafael_B221_B240_v1 as earlier
from scripts.generic_name_macro_owned_v5886b import expand as original_expand
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.write_rafael_B261_B280_contextual_v1 import BLOCKS, INPUTS, OUT, ROOT, load, save, sha


_, CURRENT, OBJECTS, GETTERS, ROLES = INPUTS
IDENTITY = ROOT / 'scoped_runtime_v1.json'
FORMATTING = ROOT / 'ordinary_formatting_manuscript_v1.json'
PREFERENCES = ROOT / 'ordinary_visual_preferences_v1.json'
STAGED = ROOT / 'source_staged_layouts_v1.json'
MACROS = ROOT / 'native_macro_measurements_v1.json'
ADAPTERS = Path('work/analysis/Rafael_early_tutorial_B42_B43_source_display_20261104/40_native_selectors_macros_andcomplete_preamble_bindings.json')


def prepare():
    assert not any(path.exists() for path in (IDENTITY, FORMATTING, PREFERENCES, STAGED, MACROS))
    doc, names, roles = map(load, (OUT, GETTERS, ROLES))
    runtime = doc['runtime']
    ctx = RegisteredRuntime(runtime['release_proof'], runtime['startup_proof'], captain=0)
    assert ctx.receipt() == runtime == names['runtime'] == roles['runtime']
    release = load(runtime['release_proof'])
    assert earlier.digest(Path('translations/release_stack.json')) == release['registry_sha256']
    assert release['all_preceding_eight_stages_and_exclusive_field_preserved']
    adapter = load(ADAPTERS)['source_owned_progressive_adapter']
    env = dict(original_expand.__globals__)
    exec(compile(adapter, __file__ + '::original-wrapper-on-registered-runtime', 'exec'), env)
    expand = env['expand']
    measured = dict(FI='Rafael', FA='Castor', FO='Castor Co.', FU='Rafael Castor')
    defaults = {}
    for token, text in measured.items():
        native = ctx.execute(expand, token.encode('ascii'), 0)
        assert len(native['cases']) == 4
        assert all(case['output_hex'] == text.encode('ascii').hex() for case in native['cases'])
        defaults[token] = native

    checks = []
    for row in doc['records']:
        if not row['native_literal_tokens']:
            continue
        assert row['native_literal_tokens'] == ['FI']
        native = ctx.execute(expand, row['english'].encode('ascii'), row['source_selector'])
        expected = row['english'].replace('FI', measured['FI']).encode('ascii').hex()
        assert len(native['cases']) == 4 and all(case['output_hex'] == expected for case in native['cases'])
        checks.append(dict(
            id=row['id'], source_reference=row['source_reference'], current_reference=row['current_reference'],
            expected_hex=expected, native_wrapper=native,
        ))
    assert len(checks) == 3
    lengths = {token: len(text) for token, text in measured.items()}
    assert lengths == dict(FI=6, FA=6, FO=10, FU=13)
    save(MACROS, dict(runtime=runtime, macro_ascii_lengths=lengths, current_default_expansions=defaults,
         complete_ARM9_COMMON_font_andactor0_macro_dependencies_qualified=True,
         three_logical_FI_records=checks, source_owned_progressive_adapter=adapter,
         evidence={str(path): earlier.digest(path) for path in (OUT, ADAPTERS)}, new_credit=0))

    names.update(
        actors=[row['actor_ID'] for row in names['name_bindings']],
        dynamic_selectors=[row['source_selector'] for row in roles['native_roles']['rows']],
        macro_ascii_lengths=lengths, current_native_macro_proof=str(MACROS),
        current_native_macro_proof_sha256=earlier.digest(MACROS),
    )
    names['evidence'].update({str(path): earlier.digest(path) for path in (MACROS, ROLES)})
    save(IDENTITY, names)
    for row in doc['records']:
        assert not row['review']['formatting']
        row['editorial_logical_English'] = row['english']
        if row['kind'] == 'typed-choice-label':
            continue
        assert earlier.TOKEN.findall(row['english']) == row['native_literal_tokens']
        row['english'] = earlier.TOKEN.sub(lambda match: '{MACRO:' + match[0] + '}', row['english'])
        row['planned_English_markup'] = f"{{SPEAKER:{row['source_selector']:02X}}}" + row['english']
        row['prior_macro_normalized_comparison'] = None
    proof = dict(
        manuscript_sha256=earlier.digest(OUT), scoped_identity_proof_sha256=earlier.digest(IDENTITY),
        reused_macro_proof_sha256=earlier.digest(MACROS), no_prose_changes_or_manual_breaks=True,
    )
    save(FORMATTING, {**doc, **proof, 'physical_speech_objects': 130, 'style_physical_speech_objects': 16,
         'style_command_objects': 2, 'pending_staged_merge': []})
    save(STAGED, {**proof, 'runtime': runtime, 'records': [], 'source_staging_only_no_display_approval': True})
    save(PREFERENCES, dict(records={}, progressive_width_px=216, FE_physical_width_px=228,
         no_old_record_specific_guard_orsemantic_preference_inherited=True, author_inserted_ordinary_breaks=0,
         new_credit=0))
    print('Measured four default substitutions and all three FI-bearing logical paragraphs on Rafael3514.')


def qualify_source(doc):
    import inspect

    source = checked_text(inspect.getsource(earlier.qualify_source), {
        "selector in set(identity['actors']) | {254}":
            "selector in set(identity['actors']) | set(identity['dynamic_selectors']) | {254}",
    })
    env = {**earlier.qualify_source.__globals__, **{
        key: globals()[key] for key in ('CURRENT', 'OBJECTS', 'IDENTITY', 'ROLES', 'STAGED', 'MACROS', 'BLOCKS')
    }}
    exec(compile(source, __file__ + '::exact-source-binding', 'exec'), env)
    return env['qualify_source'](doc)


if __name__ == '__main__':
    import sys

    if sys.argv[1:] == ['--prepare']:
        prepare()
    else:
        FunctionType(planner.main.__code__, {**planner.env, 'qualify_source': qualify_source, '__file__': __file__})()
