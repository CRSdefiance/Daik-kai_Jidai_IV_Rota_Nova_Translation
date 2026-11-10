"""Compose qualified scene/name data and disclose a bounded source-command display fixture."""
import os
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.owned_name_fields_v2 import plan_arm9_name_fields
from scripts.audit_story_glyph_consistency import load, save
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory

ROOT = Path('work/analysis/Rafael_B51_B60_focused_20261104')
RUNTIME = Path('work/analysis/Rafael_B51_B60_current_runtime_20261104')
REBUILT = Path('work/analysis/Rafael_B51_B60_rebuilt_20261104/reconstruction.json')
STORED = Path('work/analysis/Rafael_B51_B60_stored_native_20261104/stored_native_verification.json')
ORDINARY = Path('work/analysis/Rafael_early_tutorial_B42_B43_clean_20261104/ordinary_Rafael_NewGame_inputs_v1.json')
RISKS = {'DK4_MES_B52_R0005', 'DK4_MES_B52_R0018', 'DK4_MES_B55_R0078',
         'DK4_MES_B55_R0168', 'DK4_MES_B55_R0102', 'DK4_MES_B60_R0335',
         'DK4_MES_B60_R0399', 'DK4_MES_B60_R0486'}


def pin_roms(paths):
    pins = Path('translations/rom_retention_pins.json')
    before = pins.read_bytes()
    values = load(pins)
    for path in paths:
        assert not any(Path(v['path']).resolve() == path.resolve() for v in values)
        values.append(dict(path=str(path.resolve()), reason='Preserve Rafael B51-B60 disclosed scene/name display research; all earlier ROMs retained. SHA256 ' + sha(path.read_bytes())))
    (ROOT / 'pins.before.json').write_bytes(before)
    temporary = pins.with_name('rom_retention_pins.Rafael_B51_B60_focused.pending.json')
    assert not temporary.exists()
    save(temporary, values)
    assert pins.read_bytes() == before
    os.replace(temporary, pins)


if __name__ == '__main__':
    assert not ROOT.exists()
    rebuilt, stored = map(load, [REBUILT, STORED])
    doc = load(rebuilt['manuscript'])
    assert len(doc['records']) == 249 and rebuilt['speech_count'] == 245
    parent = Path(rebuilt['parent'])
    scene = Path(rebuilt['research_ROM'])
    assert sha(parent.read_bytes()) == rebuilt['parent_sha256']
    assert sha(scene.read_bytes()) == rebuilt['research_ROM_sha256']
    parent_image, image = NdsImage.open(parent), NdsImage.open(scene)
    proposal_path = RUNTIME / 'Fernan_owned_fields_proposal.json'
    proposal = load(proposal_path)
    arm = image.read_file('/__arm9__.bin')
    assert arm == parent_image.read_file('/__arm9__.bin')
    target_arm, plan = plan_arm9_name_fields(arm, proposal, NdsImage.open('work/clean.nds').read_file('/__arm9__.bin'))
    assert plan == load(RUNTIME / 'Fernan_owned_fields_plan.json')
    assert target_arm == (RUNTIME / 'Fernan_proposed_ARM9_RESEARCH_ONLY.bin').read_bytes()
    image.replace_file('/__arm9__.bin', target_arm)
    assert [p for _, p, v in parent_image.iter_files() if image.read_file(p) != v] == [doc['file_path']]
    assert [p for p, v in parent_image.iter_components() if image.read_file(p) != v] == ['/__arm9__.bin']
    ROOT.mkdir()
    combined = ROOT / 'scenes_Fernan_RESEARCH_ONLY.nds'
    image.save(combined)
    inverse = NdsImage.open(combined)
    inverse.replace_file('/__arm9__.bin', arm)
    assert bytes(inverse.rom.save()) == scene.read_bytes()
    inverse.replace_file(doc['file_path'], parent_image.read_file(doc['file_path']))
    assert bytes(inverse.rom.save()) == parent.read_bytes()
    save(ROOT / 'composition.json', dict(parent=str(parent), parent_sha256=sha(parent.read_bytes()),
        scene_ROM=str(scene), scene_ROM_sha256=sha(scene.read_bytes()),
        research_ROM=str(combined), research_ROM_sha256=sha(combined.read_bytes()), name_plan=plan,
        only_SC0_andexclusive_seven_byte_Fernan_field_differ_from_verified_parent=True,
        serialized_scene_only_andcomplete_verified_parent_inverses_exact=True,
        stored_pages_catalogue_andloaders_reused_by_exact_archive_code_font_andunowned_component_identity=True,
        no_new_native_execution_orregistered_release_claim=True, new_credit=0,
        evidence={str(p): sha(p.read_bytes()) for p in [REBUILT, STORED, proposal_path, Path(__file__)]}))
    bank = IlnkContainer.parse(image.read_file(doc['file_path'])).blocks
    inventory, _, _ = scoped_inventory()
    opening, texts = inventory(target_arm, bank[44])
    first = texts[0]['offset']
    assert first == 40 and len([c for c in opening if c['offset'] < first]) == 10
    by_actor = {}
    speeches = [r for r in doc['records'] if r['kind'] != 'typed-choice-label']
    for row in speeches:
        by_actor.setdefault(row['source_selector'], row['id'])
    assert set(by_actor) == {0, 1, 4, 5, 6, 7, 8, 11, 14, 20, 24, 35, 37, 39, 84, 114, 116, 151, 254}
    selected = RISKS | set(by_actor.values()) | {r['id'] for r in speeches if r['source_selector'] == 254}
    assert selected <= {r['id'] for r in speeches}
    commands = {t['id']: (g, next(c for c in g['all_target_commands'] if c['offset'] == t['new_offset'] - 5), t)
                for g in rebuilt['groups'] for t in g['text_records']}
    expanded = {r['id']: r['expanded_hex'] for r in stored['records']}
    native = {r['id']: r for r in load(RUNTIME / 'compatible_native_pages.json')['records']}
    logical = bytearray(bank[44][:first])
    bindings, copied = [], []
    pages = 0
    for row in speeches:
        if row['id'] not in selected:
            continue
        group, command, text = commands[row['id']]
        raw, encoded = bytes.fromhex(command['whole_command_hex']), bytes.fromhex(text['stored_hex'])
        assert raw[:6].hex() == row['source_complete_preamble_hex'] and raw[5:6+len(encoded)] == encoded + b'\0'
        at = len(logical)
        logical += raw
        bindings.append(dict(id=row['id'], block=row['block'], selector=row['source_selector'], fixture_offset=at,
            stored_command_offset=command['offset'], stored_hex=text['stored_hex'], expected_expanded_body_hex=expanded[row['id']], logical_English=row['english']))
        copied.append(dict(block=row['block'], original_offset=command['offset'], fixture_offset=at,
                           whole_command_hex=command['whole_command_hex'], word=command['word']))
        pages += 1 if row['source_selector'] == 254 else len(native[row['id']]['complete_native_English_display']['pages'])
    terminal = rebuilt['groups'][-1]['all_target_commands'][-1]
    assert terminal['word'] == 0
    logical += bytes.fromhex(terminal['whole_command_hex'])
    struct.pack_into('<H', logical, 4, len(logical) - 8)
    block = bytes(logical) + bytes(-len(logical) % 4)
    actual, actual_texts = inventory(target_arm, block)
    assert len(actual_texts) == len(selected) and actual[-1]['word'] == 0 and actual[-1]['offset'] + 4 == len(logical)
    assert all(next(c for c in actual if c['offset'] == r['fixture_offset'])['whole_command_hex'] == r['whole_command_hex'] for r in copied)
    changed = list(bank)
    changed[44] = block
    fixture = NdsImage.open(combined)
    fixture.replace_file(doc['file_path'], IlnkContainer(changed).to_bytes())
    assert [p for _, p, v in image.iter_files() if fixture.read_file(p) != v] == [doc['file_path']]
    assert all(fixture.read_file(p) == v for p, v in image.iter_components())
    rom = ROOT / 'focused_display_RESEARCH_ONLY.nds'
    fixture.save(rom)
    inverse = NdsImage.open(rom)
    inverse.replace_file(doc['file_path'], image.read_file(doc['file_path']))
    assert bytes(inverse.rom.save()) == combined.read_bytes()
    frames = 4001 + (pages + 4) * 240
    inputs = ROOT / 'focused_inputs.json'
    save(inputs, load(ORDINARY) + [dict(start=f, duration=5, buttons=['A']) for f in range(4000, frames-200, 240)])
    save(ROOT / 'focused_fixture.json', dict(research_ROM=str(rom), research_ROM_sha256=sha(rom.read_bytes()),
        parent=str(combined), parent_sha256=sha(combined.read_bytes()), text_language='reviewed-English',
        purpose='Rafael_B51_B60_eighteen_headers_three_FE_three_I_Fernan_F_andpage_transitions', frames=frames,
        inputs=str(inputs), inputs_sha256=sha(inputs.read_bytes()),
        expected_FE_bodies_hex=[r['expected_expanded_body_hex'] for r in bindings if r['selector'] == 254],
        selected_records=bindings, expected_pages=pages, selected_source_blocks=list(range(51, 61)), copied_commands=copied,
        original_initializers=[c for c in opening if c['offset'] < first], required_risk_IDs=sorted(RISKS),
        ordinary_actor_IDs=sorted(set(by_actor)-{254}), initialized_opening_content_fixture=True,
        synthetic_cross_scene_QA_sequence_not_a_story_exchange=True,
        complete_original_scene_including_transitions_andbranches_retained=False,
        all_selected_speech_commands_andpreambles_byte_exact=True, omitted_source_speeches=245-len(selected),
        omitted_conditions_branches_andscene_effects=True, all245_complete_conversations_reviewed_offline_butnot_claimed_observed=True,
        original_location_earned_chronology_fullroute_andhardware_unvisited=True,
        no_savestate_battery_RAM_roster_money_RNG_orcondition_result_override=True,
        all_unowned_files_components_andserialized_parent_inverse_exact=True,
        not_registered_candidate_or_natural_activation=True, Fernan_field_correction_applied=True,
        new_credit=0, guide_photos=False, evidence={str(p): sha(p.read_bytes()) for p in [REBUILT, STORED, ORDINARY, RUNTIME/'compatible_native_pages.json', Path(__file__)]}))
    pin_roms([combined, rom])
    print(f'Composed scene+Fernan research ROM; prepared {len(selected)} utterances/{pages} pages,18 actors/3 FE;{frames} frames. No natural activation claim.')
