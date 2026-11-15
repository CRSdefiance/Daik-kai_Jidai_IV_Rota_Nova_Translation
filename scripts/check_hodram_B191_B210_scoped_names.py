"""Reuse 29 exact name planes and render seven newly scoped strings on the registered runtime."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/check_hodram_B171_B190_scoped_names.py').read_text(encoding='utf-8'), {
    'Hodram_B171_B190_scoped_name_planes_20261104': 'Hodram_B191_B210_scoped_name_planes_20261104',
    'Hodram_B171_B190_clean_20261102/native_identity_and_term_checkpoint_v1.json':
        'Hodram_B191_B210_clean_20261104/native_identity_checkpoint_v1.json',
    'hodram_B171_B190_scoped_names_andterms_v1.json': 'hodram_B191_B210_scoped_names_andterms_v1.json',
    'Hodram_B151_B170_release_verified_20261102/registered_release_verification.json':
        'Hodram_B171_B190_release_verified_20261104/registered_release_verification.json',
    "    assert bound['runtime'] == ctx.receipt() and prior['runtime'] == bound['previous_runtime']\n    assert bound['all32_actor_inputs_models_COMMON_font_andname_consumer_dependencies_match']\n    inverse = bound['complete_latest_static_data_inverse']\n    assert inverse['complete_parent_inverse_exact'] and inverse['all_unowned_bytes_pointer_fields_sections_fonts_andallocations_unchanged']\n    assert (inverse['parent_ARM9_sha256'], inverse['target_ARM9_sha256']) == (prior['runtime']['ARM9_sha256'], sha(ctx.arm))":
    """    assert bound['runtime'] == ctx.receipt()
    old = RegisteredRuntime(prior['runtime']['release_proof'], prior['runtime']['startup_proof'])
    assert old.receipt() == prior['runtime']
    assert old.actor_root == ctx.actor_root and old.actor_bytes == ctx.actor_bytes and old.common == ctx.common
    assert old.image.read_file('/GRP/KANJI.FNT') == ctx.image.read_file('/GRP/KANJI.FNT')
    static = load(ctx.release['manifest'])['relocations']['/__arm9__.bin']['owned_static_text']['proof']['complete_owned_data_plan']
    assert static['parent_ARM9_sha256'] == sha(old.arm) and static['target_ARM9_sha256'] == sha(ctx.arm)
    restored = bytearray(old.arm)
    for field in static['fields']:
        at = field['physical_offset']; before = bytes.fromhex(field['parent_prefix_hex']); after = bytes.fromhex(field['target_prefix_hex'])
        assert restored[at:at+len(before)] == before and len(before) == len(after)
        restored[at:at+len(before)] = after
    assert bytes(restored) == ctx.arm
    second_path = Path('work/analysis/Hodram_B171_B190_scoped_name_planes_20261104/native_name_planes.json')
    second = load(second_path)
    second_context = RegisteredRuntime(second['runtime']['release_proof'],second['runtime']['startup_proof'])
    assert second_context.receipt() == second['runtime']
    assert second_context.arm == ctx.arm and second_context.common == ctx.common and second_context.actor_bytes == ctx.actor_bytes
    assert second_context.image.read_file('/GRP/KANJI.FNT') == ctx.image.read_file('/GRP/KANJI.FNT')""",
    "assert len(consumers) == 64 and len(bound['records']) == 32": "assert len(consumers) == 86 and len(bound['records']) == 43",
    "previous = {r['text']: r for r in prior['planes']}":
        "previous = {r['text']: r for r in prior['planes']}\n    previous.update({r['text']:r for r in second['planes']})",
    "dict(path=str(PRIOR), sha256=sha(PRIOR.read_bytes()), text=text,":
        "dict(path=str(second_path if text in {r['text'] for r in second['planes']} else PRIOR), sha256=sha((second_path if text in {r['text'] for r in second['planes']} else PRIOR).read_bytes()), text=text,",
    '(len(planes), fresh, reused) == (31, 13, 18)': '(len(planes), fresh, reused) == (36, 7, 29)',
    'actors=32, consumer_bindings=consumers, current_getters_reused_not_replayed=64, fresh_planes=13, exact_reused_planes=18':
        'actors=43, consumer_bindings=consumers, current_getters_reused_not_replayed=86, fresh_planes=7, exact_reused_planes=29',
    'distinct_current_strings=31': 'distinct_current_strings=36',
    '[BINDINGS, NAMES, PRIOR, Path(__file__)]': '[BINDINGS, NAMES, PRIOR, second_path, Path(__file__)]',
    'PASS 32 actors / 64 bound consumers / 31 native strings: 13 fresh planes, 18 exact reused.':
        'PASS 43 actors / 86 bound consumers / 36 native strings: 7 fresh planes, 29 exact reused.',
})
exec(compile(source, __file__ + '::same-name-style-complete-static-inverse-and-exact-runtime-reuse', 'exec'), globals())
