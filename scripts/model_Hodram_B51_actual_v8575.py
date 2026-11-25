"""Bind already verified B51 source/stored pages and four names to actual captures."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/Hodram_B51_models_v8575')
SOURCE = Path('work/analysis/Hodram_B51_source_display_v8556/source_display.json')
STORED = Path('work/analysis/Hodram_B51_stored_v8566/stored_native_controls_andrefs.json')
VIEWED = Path('work/analysis/Hodram_B51_pages_v8563/compiled_native_pages.json')
FIXTURES = Path('work/analysis/Hodram_B51_fixtures_v8573/two_whole_scripts.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    source, stored, viewed, fixtures = map(read, [SOURCE, STORED, VIEWED, FIXTURES])
    assert source['source_macro_counts'] == dict(FI=0, FA=0, FO=0) and source['source_FE_count'] == 0
    models = {'clean_Japanese': [], 'revised_English': []}
    for row in source['records']:
        body = deepcopy(row['complete_native_source_display'])
        raw = bytes.fromhex(row['source_hex'])
        assert len(body['pages']) == 1 and body['complete_consumed_bytes'] == len(raw) - 1
        models['clean_Japanese'].append({**body, 'id': row['id'], 'block': 51, 'source_selector': row['source_selector'],
            'input_hex': raw.hex(), 'expanded_native_hex': raw[1:].hex()})
    for row in stored['records']:
        body = deepcopy(row['complete_native_stored_proof'])
        for page in body['pages']:
            if 'native_plane' not in page:
                page.update(native_plane=page['viewed_native_plane'], native_plane_sha256=page['viewed_native_plane_sha256'])
        raw = bytes.fromhex(row['stored_hex'])
        assert len(body['pages']) == 1 and body['complete_consumed_bytes'] == len(raw) - 1
        models['revised_English'].append({**body, 'id': row['id'], 'block': 51, 'source_selector': row['source_selector'],
            'input_hex': raw.hex(), 'expanded_native_hex': raw[1:].hex()})
    assert all(len(rows) == 5 for rows in models.values())
    for rows in models.values():
        for row in rows:
            assert row['source_selector'] in [1, 16, 18, 113]
            for page in row['pages']:
                assert sha(Path(page['native_plane']).read_bytes()) == page['native_plane_sha256']
    names = [deepcopy(binding['reused_current_original_style11_plane'])
        for binding in source['scoped_clean_current_four_names_andreused_native_consumers']]
    assert {row['actor_ID'] for row in names} == {1, 16, 18, 113}
    for row in names:
        assert sha(Path(row['native_plane']).read_bytes()) == row['native_plane_sha256']
    for fixture in fixtures['fixtures']:
        image = NdsImage.open(fixture['research_ROM'])
        assert sha(Path(fixture['research_ROM']).read_bytes()) == fixture['research_ROM_sha256']
        assert sha(image.read_file('/__arm9__.bin')) == source['ARM9_sha256'] == viewed['ARM9_sha256']
        assert sha(image.read_file('/GRP/KANJI.FNT')) == source['font_sha256'] == viewed['font_sha256']
    ROOT.mkdir(parents=True)
    save(ROOT / 'native_models.json', dict(native_models=models, name_planes=names, ARM9_sha256=source['ARM9_sha256'], font_sha256=source['font_sha256'],
        source_original5_andreviewed_stored5_planes_reused_by_exact_hash=True, four_current_nameplanes_reused_by_exact_code_font_wholeactor_binding=True,
        no_native_reexecution=True, actual_selected_body_header_path_transition_andnormal_return_binding_pending=True,
        unvisited_conditional_rows_are_models_not_actual_coverage=True, new_credit=0, new_emulator_runs=0, full_goal_complete=False,
        evidence={str(p): sha(p.read_bytes()) for p in [SOURCE, STORED, VIEWED, FIXTURES, Path(__file__)]}))
    print('B51 actual models: five Japanese/five stored body planes and four nameplanes reused by exact hashes. No new native execution or actual coverage claimed.')
