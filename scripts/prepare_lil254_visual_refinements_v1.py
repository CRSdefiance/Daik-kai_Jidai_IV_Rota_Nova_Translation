"""Correct Lil's company-name punctuation and bind visual wrap refinements."""

from hashlib import sha256
from pathlib import Path
import sys

from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.prepare_lil254_prose_v1 import PROSE, NAMES, ROOT
from scripts.prepare_lil278_layout_v1 import CAPTAIN_FORMATTER, prose_gate
from scripts.source_locked_derivation_v5118 import checked_text


def main():
    config = load(ROOT / 'prose_config_v1.json')
    config_path = ROOT / 'prose_config_v2.json'
    prose = PROSE.with_name(PROSE.name.replace('_v1', '_v2'))
    names = NAMES.with_name(NAMES.name.replace('_v1', '_v2'))
    prior = ROOT / 'formatting_v1'
    out = ROOT / 'formatting_v2'
    assert not any(p.exists() for p in (config_path, prose, names, out))
    original = load(PROSE)
    record_id = 'DK4_MES_B319_R0008'
    record = next(row for row in original['records'] if row['id'] == record_id)
    before = "Hey, mister. I happen to run FO. Don't call me little lady."
    assert record['english'] == before and record['decision'] == 'revision'
    assert record['source_macros']['FO'] == 1
    assert load(prior / 'native_macro_measurements.json')['defaults']['FO']['text'] == 'Argot Co.'
    config['amendments'][record_id] = dict(
        before=before,
        after="Hey, mister. I happen to run FO, so don't call me little lady.",
        reason="The native preview showed two periods after Argot Co. Connect Lil's claim and objection with a comma so the company macro can retain its own punctuation.",
    )
    config.update(out=str(prose), names_out=str(names), proof_out=str(ROOT / 'prose_gates_v2.json'))
    save(config_path, config)
    source = checked_text(prose_gate.source, {
        "runtime=runtime,current_ROM=runtime['candidate'],current_ROM_sha256=runtime['candidate_sha256'],":
            "runtime=runtime,current_ROM=proposals['current_ROM'],current_ROM_sha256=proposals['current_ROM_sha256'],\n"
            "        exact_existing_native_context_reuse=proposals['exact_native_context_reuse'],",
        "    assert len(terms['items'])==cfg['item_bindings']":
            "    assert len(terms['items'])==cfg['item_bindings']\n"
            "    reuse = proposals['exact_native_context_reuse']\n"
            "    assert reuse == terms['exact_native_context_reuse'] and reuse['native_runtime'] == runtime\n"
            "    assert reuse['target_candidate'] == proposals['current_ROM']\n"
            "    assert reuse['target_candidate_sha256'] == digest(proposals['current_ROM']) == proposals['current_ROM_sha256']\n"
            "    assert digest(reuse['target_release']) == reuse['target_release_sha256']",
    })
    sys.argv = [sys.argv[0], '--config', str(config_path)]
    env = {**prose_gate.env, '__file__': __file__}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()
    revised = load(prose)
    assert [b['id'] for a, b in zip(original['records'], revised['records'], strict=True)
            if a['english'] != b['english']] == [record_id]
    assert load(NAMES)['records'] == load(names)['records']

    source = checked_text(CAPTAIN_FORMATTER.read_text(encoding='utf-8'), {
        "args.root/'formatting_v1'": "args.root/'formatting_v2'",
        "args.root/'dynamic_roles_current_v1.json'": "args.root/'dynamic_roles_all_v1.json'",
        "    assert ctx.receipt()==runtime and digest('translations/release_stack.json')==ctx.release['registry_sha256']":
            "    assert ctx.receipt()==runtime\n"
            "    from scripts.check_editorial_compiled_pages_scope_reuse_v1 import qualified_current_native_context\n"
            "    assert qualified_current_native_context(doc,ctx)==current['exact_native_context_reuse']",
    })
    previous_fe = 'work/Lil361_B283_B298_clean_20261110/formatting_v1/native_macro_measurements.json'
    sys.argv = [sys.argv[0], '--root', str(ROOT), '--prose', str(prose),
                '--FE-source-macros', previous_fe, '--captain', '2']
    exec(compile(source, __file__, 'exec'), {'__file__': __file__, '__name__': '__main__'})
    old_macros = prior / 'native_macro_measurements.json'
    new_macros = out / 'native_macro_measurements.json'
    old_values, new_values = load(old_macros), load(new_macros)
    assert {k: v for k, v in old_values.items() if k != 'evidence'} == {
        k: v for k, v in new_values.items() if k != 'evidence'}
    new_macros.rename(out / 'fresh_macro_equivalence.json')
    new_macros.write_bytes(old_macros.read_bytes())
    manuscript_path = out / 'formatting_input.json'
    manuscript = load(manuscript_path)
    manuscript['macro_proof_sha256'] = digest(old_macros)
    manuscript['fresh_macro_equivalence_sha256'] = digest(out / 'fresh_macro_equivalence.json')
    save(manuscript_path, manuscript)

    prefs = load(prior / 'FE_and_phrase_preferences_v2.json')
    by_id = {row['id']: row for row in manuscript['records']}
    pairs = {
        'SC2_B312_STYLE_1694_0': [('right', 'away'), ('ran', 'off')],
        'SC2_B312_STYLE_1694_182': [('right', 'away')],
        'SC2_B312_STYLE_1694_236': [('right', 'away')],
        'SC2_B316_STYLE_914_136': [('came', 'through')],
        'SC2_B316_STYLE_1842_136': [('came', 'through')],
        'SC2_B316_STYLE_2354_148': [('cactus', 'spine')],
        'SC2_B316_STYLE_2354_206': [('cactus', 'spine')],
        'SC2_B316_STYLE_2924_158': [('easy', 'does'), ('does', 'it')],
        'DK4_MES_B317_R0039': [('from', 'what'), ('what', 'i'), ('i', 'hear')],
    }
    for ident, required in pairs.items():
        row = by_id[ident]
        bindings = {key: sha256(row[key].encode()).hexdigest() for key in ('source_hex', 'current_hex', 'english')}
        prefs['records'][ident] = dict(required_pairs=required, bindings=bindings)
    prefs['records']['DK4_MES_B315_R0010']['page_clause'] = (
        'It seems to show the ruins of an old kingdom somewhere near town.')
    save(out / 'visual_preferences_v3.json', prefs)


if __name__ == '__main__':
    main()
