"""Prepare the complete Charlotte scene and bounded name/pagination QA fixtures."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/prepare_hodram_B171_B190_actual.py').read_text(encoding='utf-8'),{
    'Hodram_B171_B190_actual_fixtures_20261104':'Rafael_B61_B80_actual_fixtures_20261104',
    'Hodram_B171_B190_rebuilt_20261104/reconstruction.json':'Rafael_B61_B80_rebuilt_20261104/reconstruction.json',
    "STORED = Path('work/analysis/Hodram_B171_B190_stored_qualified_20261104/stored_native_verification.json')":
        "COMPILED = Path('work/analysis/Rafael_B61_B80_formatting_20261104/combined_native_v10.json')",
    'work/analysis/hodram_opening_context_v2018/ordinary_Hodram_NewGame_inputs.json':'work/analysis/Rafael_early_tutorial_B42_B43_clean_20261104/ordinary_Rafael_NewGame_inputs_v1.json',
    "    rebuilt, stored = map(load, [REBUILT, STORED])\n    assert stored['reconstruction_sha256'] == sha(REBUILT.read_bytes()) and stored['complete_stored_pages'] == 439\n    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']":
        """    rebuilt,compiled=map(load,[REBUILT,COMPILED])
    assert rebuilt['native_sha256']==sha(COMPILED.read_bytes()) and compiled['pages']==545
    assert len(compiled['records'])==rebuilt['speech_count']==539 and not compiled['direct_visual_review_pending']
    assert compiled['runtime']['candidate_sha256']==rebuilt['parent_sha256']""",
    '/data/SC1.DK4':'/data/SC0.DK4',
    'bank[42]':'bank[44]', 'changed[42]':'changed[44]',
    "assert first == 42 and len([c for c in opening if c['offset'] < first]) == 8":
        "assert first == 40 and len([c for c in opening if c['offset'] < first]) == 10",
    "    ROOT.mkdir()":
        """    native_path=Path('work/analysis/Rafael_B61_B80_formatting_20261104/combined_native_v10.json')
    native=load(native_path);assert native_path==COMPILED
    selected={'DK4_MES_B61_R0113'};by_actor={}
    for row in doc['records']:
        if row['source_selector']!=254:by_actor.setdefault(row['source_selector'],row['id'])
    assert len(by_actor)==22
    selected.update(by_actor.values())
    selected.update(r['id'] for r in native['records'] if len(r['complete_native_English_display'].get('pages',[]))>1)
    ROOT.mkdir()""",
    "[('sail_lesson', [171], True, 14001),\n                                       ('pirate_transition', [179], True, 14001),\n                                       ('town_exchanges', list(range(180, 191)), False, 44001)]":
        "[('Charlotte_complete_scene', [69], True, 24001),\n                                       ('scoped_names_andpagination', list(range(61,81)), False, 15001)]",
    "                    text = next(t for t in group['text_records'] if t['new_offset'] - 5 == command['offset'])":
        """                    text = next(t for t in group['text_records'] if t['new_offset'] - 5 == command['offset'])
                    if text['id'] not in selected:continue""",
    "b'Hodram'":"b'Rafael'", "b'Bergstrom'":"b'Castor'", "b'Bergstrom Fleet'":"b'Castor Co.'",
    'selected_records=bindings, selected_source_blocks=blocks, copied_commands=copied, original_initializers=initializers,':
        """selected_records=bindings, selected_source_blocks=blocks, copied_commands=copied, original_initializers=initializers,
            expected_pages=sum(1 if r['selector']==254 else len(next(v for v in native['records'] if v['id']==r['id'])['complete_native_English_display']['pages']) for r in bindings),
            ordinary_actor_IDs=sorted({r['selector'] for r in bindings if r['selector']!=254}),""",
    "[r['records'] for r in created] == [27, 30, 130]":"[r['records'] for r in created] == [66,len(selected)]",
    "[REBUILT, STORED, ORDINARY, Path(__file__)]":"[REBUILT, COMPILED, ORDINARY, native_path, Path(__file__)]",
    'not_registered_candidate_or_natural_activation=True, new_credit=0, guide_photos=False,':
        'not_registered_candidate_or_natural_activation=True, stored_native_gate_pending_at_fixture_preparation=True, new_credit=0, guide_photos=False,',
    "B171–B190 disclosed initialized English QA fixture":"Rafael B61-B80 disclosed initialized English QA fixture",
    'rom_retention_pins.B171_actual.pending.json':'rom_retention_pins.Rafael_B61_B80_actual.pending.json',
    'Prepared three pinned content fixtures: full B171 menu scene, full B179 transitions, 11 complete town exchanges.':
        'Prepared full66-speech Charlotte scene plus22-actor/six-pagination focused fixture. No natural activation claim.',
})
exec(compile(source,__file__+'::same-complete-source-command-fixture-andbounded-header-selection','exec'),globals())
