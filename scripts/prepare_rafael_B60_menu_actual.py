"""Copy complete reviewed choice objects into a disclosed ordinary-initialized UI fixture."""
import os
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory

ROOT = Path('work/analysis/Rafael_B60_menu_actual_fixture_20261104')
COMPOSITION = Path('work/analysis/Rafael_B51_B60_focused_20261104/composition.json')
REBUILT = Path('work/analysis/Rafael_B51_B60_rebuilt_20261104/reconstruction.json')
STORED = Path('work/analysis/Rafael_B51_B60_stored_native_20261104/stored_native_verification.json')
ORDINARY = Path('work/analysis/Rafael_early_tutorial_B42_B43_clean_20261104/ordinary_Rafael_NewGame_inputs_v1.json')
SEQUENCE = ['DK4_MES_B60_R0071', 'DK4_MES_B60_R0075', 768,
            'DK4_MES_B60_R0177', 'DK4_MES_B60_R0182', 1852, 'DK4_MES_B60_R0041']

if __name__ == '__main__':
    assert not ROOT.exists()
    composition, rebuilt, stored = map(load, [COMPOSITION, REBUILT, STORED])
    parent = Path(composition['research_ROM'])
    assert sha(parent.read_bytes()) == composition['research_ROM_sha256']
    image = NdsImage.open(parent)
    arm, archive = image.read_file('/__arm9__.bin'), image.read_file('/data/SC0.DK4')
    bank = IlnkContainer.parse(archive).blocks
    inventory, _, _ = scoped_inventory()
    opening, texts = inventory(arm, bank[44])
    assert texts[0]['offset'] == 40
    logical = bytearray(bank[44][:40])
    doc = load(rebuilt['manuscript'])
    rows = {r['id']: r for r in doc['records']}
    expanded = {r['id']: r['expanded_hex'] for r in stored['records']}
    group = next(g for g in rebuilt['groups'] if g['block'] == 60)
    commands = {c['offset']: c for c in group['all_target_commands']}
    bodies, menus, copied = [], [], []
    for item in SEQUENCE:
        if isinstance(item, int):
            obj = next(o for o in group['native_objects'] if o['old_offset'] == item)
            command = commands[obj['new_offset']]
            assert command['word'] == 0x2100 and command['whole_command_hex'] == obj['compiled_hex']
            menus.append(dict(source_command_offset=item, fixture_offset=len(logical),
                complete_original_typed_object_hex=obj['compiled_hex'], source_index_order=obj['source_index_order'], count=obj['count']))
        else:
            text = next(t for t in group['text_records'] if t['id'] == item)
            command = commands[text['new_offset'] - 5]
            assert command['word'] == 0x4000 and command['whole_command_hex'][:12] == rows[item]['source_complete_preamble_hex']
            bodies.append(dict(id=item, block=60, fixture_offset=len(logical), selector=rows[item]['source_selector'],
                stored_hex=text['stored_hex'], expected_expanded_body_hex=expanded[item], logical_English=rows[item]['english']))
        copied.append(dict(block=60, original_offset=command['offset'], fixture_offset=len(logical),
            whole_command_hex=command['whole_command_hex'], word=command['word']))
        logical += bytes.fromhex(command['whole_command_hex'])
    terminal = group['all_target_commands'][-1]
    assert terminal['word'] == 0
    logical += bytes.fromhex(terminal['whole_command_hex'])
    struct.pack_into('<H', logical, 4, len(logical) - 8)
    block = bytes(logical) + bytes(-len(logical) % 4)
    actual, actual_texts = inventory(arm, block)
    assert len(actual_texts) == 5 and actual[-1]['word'] == 0 and actual[-1]['offset'] + 4 == len(logical)
    for row in copied:
        assert next(c for c in actual if c['offset'] == row['fixture_offset'])['whole_command_hex'] == row['whole_command_hex']
    changed = list(bank)
    changed[44] = block
    fixture = NdsImage.open(parent)
    fixture.replace_file('/data/SC0.DK4', IlnkContainer(changed).to_bytes())
    assert [p for _, p, v in image.iter_files() if fixture.read_file(p) != v] == ['/data/SC0.DK4']
    assert all(fixture.read_file(p) == v for p, v in image.iter_components())
    ROOT.mkdir()
    rom = ROOT / 'two_menus_RESEARCH_ONLY.nds'
    fixture.save(rom)
    inverse = NdsImage.open(rom)
    inverse.replace_file('/data/SC0.DK4', archive)
    assert bytes(inverse.rom.save()) == parent.read_bytes()
    schedule = [(4000, 'A'), (4240, 'A'), (4460, 'DOWN'), (4580, 'UP'), (4720, 'A'),
                (4960, 'A'), (5200, 'A'), (5400, 'DOWN'), (5680, 'A'), (6000, 'A')]
    inputs = ROOT / 'menu_inputs.json'
    save(inputs, load(ORDINARY) + [dict(start=f, duration=5, buttons=[button]) for f, button in schedule])
    save(ROOT / 'menu_fixture.json', dict(research_ROM=str(rom), research_ROM_sha256=sha(rom.read_bytes()),
        parent=str(parent), parent_sha256=sha(parent.read_bytes()), text_language='reviewed-English',
        purpose='two_complete_B60_choice_objects_controller_highlight_andmodal_continuation', frames=6501,
        inputs=str(inputs), inputs_sha256=sha(inputs.read_bytes()), expected_FE_bodies_hex=[], selected_records=bodies,
        selected_source_blocks=[60], copied_commands=copied, copied_menus=menus,
        original_initializers=[c for c in opening if c['offset'] < 40], initialized_opening_content_fixture=True,
        synthetic_cross_scene_QA_sequence_not_a_story_exchange=True,
        original_questions_andtwo_complete2100_objects_copied_byte_exact=True,
        final_source_R41_is_display_continuation_sentinel_not_an_original_menu_branch_outcome=True,
        original_conditions_branches_andnarrative_outcomes_excluded=True,
        intended_selected_indices=[0, 1], controller_success_highlight_andreturn_not_yet_claimed=True,
        no_savestate_battery_RAM_roster_money_RNG_orcondition_result_override=True,
        all_unowned_files_components_andserialized_parent_inverse_exact=True,
        original_location_earned_chronology_fullroute_andhardware_unvisited=True,
        not_registered_candidate_or_natural_activation=True, new_credit=0, guide_photos=False,
        evidence={str(p): sha(p.read_bytes()) for p in [COMPOSITION, REBUILT, STORED, ORDINARY, Path(__file__)]}))
    pins = Path('translations/rom_retention_pins.json')
    before = pins.read_bytes()
    values = load(pins)
    assert not any(Path(v['path']).resolve() == rom.resolve() for v in values)
    values.append(dict(path=str(rom.resolve()), reason='Preserve disclosed two complete B60 menu object fixture; all earlier ROMs retained. SHA256 ' + sha(rom.read_bytes())))
    (ROOT/'pins.before.json').write_bytes(before)
    temporary = pins.with_name('rom_retention_pins.Rafael_B60_menus.pending.json')
    assert not temporary.exists()
    save(temporary, values)
    assert pins.read_bytes() == before
    os.replace(temporary, pins)
    print('Prepared two exact choice objects/five exact speeches;6501 ordinary-input frames. Highlights/returns pending.')
