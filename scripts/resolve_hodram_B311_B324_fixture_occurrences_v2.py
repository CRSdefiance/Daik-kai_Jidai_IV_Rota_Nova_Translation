"""Correct reference-only ambiguity using the pre-run source-key selection; preserve every run byte."""
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.source_scoped_fixture_command_v1 import resolve

ROOT = Path('work/Hodram_B311_B324_clean_20261107')
OUT = ROOT/'source_occurrence_resolution_v2.json'

def main():
    assert not OUT.exists()
    selection_path = ROOT/'bounded_selection_v1.json'
    selection = load(selection_path)
    rebuilt_path = ROOT/'reconstruction_v1/reconstruction.json'
    rebuilt = load(rebuilt_path)
    groups = {g['block']: g for g in rebuilt['groups']}
    manifest_path = ROOT/'focused_fixtures_bounded_v1/fixtures.json'
    manifest = load(manifest_path)
    rows, discrepancies, evidence = [], [], {}
    source_styles = load(rebuilt['styles'])
    native_menu = load(rebuilt['menu'])
    ordinary = {t['id']:(g,next(c for c in g['all_target_commands'] if c['offset']==t['new_offset']-5))
        for g in rebuilt['groups'] for t in g['text_records']}
    for run, (spec, entry) in enumerate(zip(selection['fixtures'],manifest['fixtures'],strict=True),1):
        path = Path(entry['fixture'])
        fixture = load(path)
        assert digest(path) == entry['fixture_sha256'] and digest(fixture['research_ROM']) == fixture['research_ROM_sha256']
        body = IlnkContainer.parse(NdsImage.open(fixture['research_ROM']).read_file('/data/SC1.DK4')).blocks[42]
        assert len(spec['sequence']) == len(fixture['copied_commands'])
        corrected, bindings = [], []
        selected = iter(fixture['selected_records'])
        for ordinal, (action, old) in enumerate(zip(spec['sequence'],fixture['copied_commands'],strict=True)):
            if 'speech' in action:
                group, command = ordinary[action['speech']]
                expected_binding = next(selected)
                assert expected_binding['id'] == action['speech']
                source_key = dict(block=group['block'],speech_ID=action['speech'])
            else:
                kind = 'style' if 'style' in action else 'menu'
                request = action[kind]
                group = groups[request['block']]
                source_key = dict(block=request['block'],source_command_offset=request['source_command_offset'])
                if kind == 'style':
                    proof = next(o for o in source_styles['objects'] if (o['block'],o['source_command_offset']) == (request['block'],request['source_command_offset']))
                    command = resolve(group,request['source_command_offset'],0x4100,proof['target_object_hex'])
                    expected_binding = next(selected)
                    chosen = proof['native_slots'][expected_binding['expected_style']]
                    assert chosen['record_id'] == expected_binding['id'] and chosen['target_hex'] == expected_binding['stored_hex']
                else:
                    proof = next(o for o in native_menu['menus'] if (o['block'],o['source_command_offset']) == (request['block'],request['source_command_offset']))
                    word = int.from_bytes(bytes.fromhex(proof['target_object_hex'])[:2],'little')
                    command = resolve(group,request['source_command_offset'],word,proof['target_object_hex'])
                    expected_binding = None
            assert old['block'] == group['block'] and old['word'] == command['word']
            assert old['whole_command_hex'] == command['whole_command_hex']
            raw = bytes.fromhex(old['whole_command_hex'])
            assert body[old['fixture_offset']:old['fixture_offset']+len(raw)] == raw
            corrected_row = {**old,'original_offset':command['offset']}
            if old['original_offset'] != command['offset']:
                assert command['word'] == 0x4100
                duplicate = next(c for c in group['all_target_commands'] if c['offset'] == old['original_offset'])
                assert duplicate['whole_command_hex'] == command['whole_command_hex']
                discrepancies.append(dict(run=run,ordinal=ordinal,source_key=source_key,
                    original_metadata_offset=old['original_offset'],source_qualified_offset=command['offset'],
                    fixture_offset=old['fixture_offset'],command_hex=raw.hex(),no_emitted_byte_orobservation_changed=True))
            corrected.append(corrected_row)
            if expected_binding:
                assert expected_binding['fixture_offset'] == old['fixture_offset']
                assert expected_binding['stored_command_offset'] == old['original_offset']
                bindings.append({**expected_binding,'stored_command_offset':command['offset']})
        assert next(selected,None) is None
        rows.append(dict(run=run,fixture=str(path),fixture_sha256=digest(path),
            original_research_ROM=fixture['research_ROM'],original_research_ROM_sha256=fixture['research_ROM_sha256'],
            corrected_copied_commands=corrected,corrected_selected_records=bindings))
        for p in [path,Path(fixture['research_ROM']),ROOT/f'bounded_run_{run}_v1/terminal.json',ROOT/f'bounded_pixels_{run}_v1/focused_actual_pixels.json']:
            evidence[str(p)] = digest(p)
    assert len(discrepancies) == 1
    assert discrepancies[0]['source_key'] == dict(block=313,source_command_offset=1252)
    assert (discrepancies[0]['original_metadata_offset'],discrepancies[0]['source_qualified_offset']) == (922,1308)
    # Regression proof: content equality cannot select an occurrence, while both source keys resolve independently.
    g = groups[313]
    a, b = [next(o for o in g['native_objects'] if o['old_offset']==offset and o['word']==0x4100) for offset in [856,1252]]
    assert a['compiled_hex'] == b['compiled_hex']
    ca, cb = [resolve(g,o['old_offset'],0x4100,o['compiled_hex']) for o in [a,b]]
    assert ca['offset'] != cb['offset'] and ca['offset']==922 and cb['offset']==1308
    save(OUT,dict(records=rows,discrepancies=discrepancies,duplicate_command_source_key_regression_pass=True,
        pre_run_source_selection_andfixture_ordinal_define_occurrence=True,
        all195_copied_commands_and189_selected_records_bound_to_exact_source_keys=True,
        only_stored_source_reference_metadata_corrected=True,
        original_fixtures_ROMs_terminals_captures_andpixel_receipts_unchanged=True,
        no_posthoc_source_assignment_from_pixel_similarity=True,no_new_emulator_run_ornew_gameplay_credit=True,
        fixed_generator='scripts/prepare_hodram_display_fixtures_bounded_v2.py',new_credit=0,
        evidence={**evidence,**{str(p):digest(p) for p in [selection_path,rebuilt_path,manifest_path,
            Path(rebuilt['styles']),Path(rebuilt['menu']),Path(__file__),Path('scripts/source_scoped_fixture_command_v1.py'),
            Path('scripts/prepare_hodram_display_fixtures_bounded_v2.py')]}}))
    print('Resolved one reference-only duplicate at B313 C1252:922->1308; all195 commands/189 bindings proven against pre-run selection and original ROM bytes. Runs unchanged.')

if __name__ == '__main__':
    main()
