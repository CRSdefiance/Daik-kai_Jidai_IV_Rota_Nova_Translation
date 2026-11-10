"""Build disclosed coldboot content fixtures from exact reviewed stored commands."""
import os
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory

ROOT = Path('work/analysis/Hodram_B171_B190_actual_fixtures_20261104')
REBUILT = Path('work/analysis/Hodram_B171_B190_rebuilt_20261104/reconstruction.json')
STORED = Path('work/analysis/Hodram_B171_B190_stored_qualified_20261104/stored_native_verification.json')
ORDINARY = Path('work/analysis/hodram_opening_context_v2018/ordinary_Hodram_NewGame_inputs.json')


if __name__ == '__main__':
    assert not ROOT.exists()
    rebuilt, stored = map(load, [REBUILT, STORED])
    assert stored['reconstruction_sha256'] == sha(REBUILT.read_bytes()) and stored['complete_stored_pages'] == 439
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    parent = Path(rebuilt['research_ROM'])
    assert sha(parent.read_bytes()) == rebuilt['research_ROM_sha256']
    image = NdsImage.open(parent)
    arm = image.read_file('/__arm9__.bin')
    archive = image.read_file('/data/SC1.DK4')
    bank = IlnkContainer.parse(archive).blocks
    inventory, _, _ = scoped_inventory()
    opening, texts = inventory(arm, bank[42])
    first = texts[0]['offset']
    assert first == 42 and len([c for c in opening if c['offset'] < first]) == 8
    initializers = [c for c in opening if c['offset'] < first]
    doc = load(rebuilt['manuscript'])
    by_id = {r['id']: r for r in doc['records']}
    groups = {g['block']: g for g in rebuilt['groups']}
    ROOT.mkdir()
    created = []
    for name, blocks, whole, frames in [('sail_lesson', [171], True, 14001),
                                       ('pirate_transition', [179], True, 14001),
                                       ('town_exchanges', list(range(180, 191)), False, 44001)]:
        logical = bytearray(bank[42][:first])
        bindings, copied, excluded = [], [], []
        for block in blocks:
            group = groups[block]
            if whole:
                start, end = 8, group['new_logical_end']
                assert len(blocks) == 1
                shift = len(logical) - start
                logical += bank[block][start:end]
                for command in group['all_target_commands']:
                    copied.append(dict(block=block, original_offset=command['offset'],
                        fixture_offset=command['offset'] + shift, whole_command_hex=command['whole_command_hex'], word=command['word']))
                for fix in group['relative_fixups']:
                    assert start <= fix['new_offset'] < end and start <= fix['new_target'] <= end
                for text in group['text_records']:
                    row = by_id[text['id']]
                    bindings.append(dict(id=row['id'], block=block, fixture_offset=text['new_offset'] - 5 + shift,
                        stored_command_offset=text['new_offset'] - 5, stored_hex=text['stored_hex'],
                        selector=row['source_selector'], logical_English=row['english']))
            else:
                for command in group['all_target_commands']:
                    if command['word'] != 0x4000:
                        excluded.append(dict(block=block, **command))
                        continue
                    text = next(t for t in group['text_records'] if t['new_offset'] - 5 == command['offset'])
                    row = by_id[text['id']]
                    assert command['whole_command_hex'][:12] == row['source_complete_preamble_hex']
                    copied.append(dict(block=block, original_offset=command['offset'], fixture_offset=len(logical),
                        whole_command_hex=command['whole_command_hex'], word=command['word']))
                    bindings.append(dict(id=row['id'], block=block, fixture_offset=len(logical),
                        stored_command_offset=command['offset'], stored_hex=text['stored_hex'],
                        selector=row['source_selector'], logical_English=row['english']))
                    logical += bytes.fromhex(command['whole_command_hex'])
        if not whole:
            logical += bytes.fromhex(groups[blocks[-1]]['all_target_commands'][-1]['whole_command_hex'])
        struct.pack_into('<H', logical, 4, len(logical) - 8)
        fixture_block = bytes(logical) + bytes(-len(logical) % 4)
        commands, actual_texts = inventory(arm, fixture_block)
        assert commands[-1]['word'] == 0 and commands[-1]['offset'] + 4 == len(logical)
        assert len(actual_texts) == len(bindings)
        for item in copied:
            command = next(c for c in commands if c['offset'] == item['fixture_offset'])
            assert command['word'] == item['word'] and command['whole_command_hex'] == item['whole_command_hex']
        for row in bindings:
            command = next(c for c in actual_texts if c['offset'] == row['fixture_offset'])
            raw = bytes.fromhex(command['whole_command_hex'])
            encoded = bytes.fromhex(row['stored_hex'])
            assert raw[:6].hex() == by_id[row['id']]['source_complete_preamble_hex']
            assert raw[5:6 + len(encoded)] == encoded + b'\0'
            row['expected_expanded_body_hex'] = encoded[1:].replace(b'FI', b'Hodram').replace(b'FA', b'Bergstrom').replace(b'FO', b'Bergstrom Fleet').hex()
        changed = list(bank)
        changed[42] = fixture_block
        fixture = NdsImage.open(parent)
        fixture.replace_file('/data/SC1.DK4', IlnkContainer(changed).to_bytes())
        assert [p for _, p, v in image.iter_files() if fixture.read_file(p) != v] == ['/data/SC1.DK4']
        assert all(fixture.read_file(p) == v for p, v in image.iter_components())
        path = ROOT / (name + '_RESEARCH_ONLY.nds')
        fixture.save(path)
        restored = NdsImage.open(path)
        restored.replace_file('/data/SC1.DK4', archive)
        assert bytes(restored.rom.save()) == parent.read_bytes()
        inputs = ROOT / (name + '_inputs.json')
        save(inputs, load(ORDINARY) + [dict(start=f, duration=5, buttons=['A']) for f in range(4000, frames - 500, 240)])
        proof = ROOT / (name + '_fixture.json')
        save(proof, dict(research_ROM=str(path), research_ROM_sha256=sha(path.read_bytes()), parent=str(parent), parent_sha256=sha(parent.read_bytes()),
            text_language='reviewed-English', purpose=name, frames=frames, inputs=str(inputs), inputs_sha256=sha(inputs.read_bytes()),
            expected_FE_bodies_hex=[r['expected_expanded_body_hex'] for r in bindings if r['selector'] == 254],
            selected_records=bindings, selected_source_blocks=blocks, copied_commands=copied, original_initializers=initializers,
            complete_original_scene_including_transitions_andbranches_retained=whole,
            excluded_nontext_commands=excluded, town_condition_andmarket_effects_excluded=not whole,
            all_selected_speech_commands_andpreambles_byte_exact=True, original_held_menu_selection_andrelative_branches_unchanged=whole,
            outer_natural_activation_excluded=True, initialized_opening_content_fixture=True,
            synthetic_cross_scene_QA_sequence_not_a_story_exchange=not whole,
            original_location_earned_chronology_fullroute_andhardware_unvisited=True,
            no_savestate_battery_RAM_roster_money_RNG_orcondition_result_override=True,
            all_unowned_files_components_andserialized_parent_inverse_exact=True,
            not_registered_candidate_or_natural_activation=True, new_credit=0, guide_photos=False,
            evidence={str(p): sha(p.read_bytes()) for p in [REBUILT, STORED, ORDINARY, Path(__file__)]}))
        created.append(dict(fixture=str(proof), fixture_sha256=sha(proof.read_bytes()), path=str(path), sha256=sha(path.read_bytes()), records=len(bindings)))
    assert [r['records'] for r in created] == [27, 30, 130]
    pins = Path('translations/rom_retention_pins.json')
    before = pins.read_bytes()
    values = load(pins)
    for item in created:
        path = Path(item['path'])
        assert not any(Path(v['path']).resolve() == path.resolve() for v in values)
        values.append(dict(path=str(path.resolve()), reason='B171–B190 disclosed initialized English QA fixture; preserve all ROMs. SHA256 ' + item['sha256']))
    (ROOT / 'pins.before.json').write_bytes(before)
    staged = pins.with_name('rom_retention_pins.B171_actual.pending.json')
    assert not staged.exists()
    save(staged, values)
    assert pins.read_bytes() == before
    os.replace(staged, pins)
    save(ROOT / 'fixtures.json', dict(fixtures=created, actual_observation_pending=True, guide_photos=False, new_credit=0))
    print('Prepared three pinned content fixtures: full B171 menu scene, full B179 transitions, 11 complete town exchanges. Actual observations pending.')
