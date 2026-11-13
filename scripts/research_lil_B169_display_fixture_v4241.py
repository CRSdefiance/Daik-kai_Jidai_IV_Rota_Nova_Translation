"""Create paired B22 content fixtures retaining the whole B169 exchange and all effects."""
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B169_display_fixture_v4241')
PARENT = Path('out/all_routes_combined_v4204_candidate.nds')
PLAN = Path('work/analysis/lil_B169_relocation_v4233/nested_source_relocation_research.json')
DOC = Path('translations/lil_B169_editorial_manuscript_v4.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    plan, doc = read(PLAN), read(DOC)
    packet = read(doc['source_context'])
    parent, clean = NdsImage.open(PARENT), NdsImage.open('work/clean.nds')
    arm = parent.read_file('/__arm9__.bin')
    current = IlnkContainer.parse(parent.read_file('/data/SC2.DK4')).blocks
    jp = IlnkContainer.parse(clean.read_file('/data/SC2.DK4')).blocks
    en = IlnkContainer.parse(Path(plan['target_SC2']).read_bytes()).blocks
    assert sha(PARENT.read_bytes()) == doc['current_ROM_sha256'] == plan['candidate_sha256']
    inventory, _, _ = scoped_inventory()
    b22 = current[22]
    init, _ = inventory(arm, b22)
    first = next(command['offset'] for command in init if command['word'] == 0x4000)
    assert first == 56 and len(init[:9]) == 9 and sum(command['word'] == 0xA000 for command in init[:9]) == 4
    prelude = b22[8:first]
    group = packet['blocks'][0]
    ROOT.mkdir(parents=True)
    fixtures = []
    for case, bank in [('clean_Japanese', jp), ('reviewed_English', en)]:
        commands, _ = inventory(arm, bank[169])
        assert len(commands) == 53 and sum(command['word'] == 0xA000 for command in commands) == 1
        logical_end = 8 + struct.unpack_from('<H', bank[169], 4)[0]
        payload = bank[169][8:logical_end]
        logical = bytearray(b22[:8] + prelude + payload)
        struct.pack_into('<H', logical, 4, len(logical) - 8)
        target = bytes(logical) + bytes(-len(logical) % 4)
        walk, speeches = inventory(arm, target)
        assert len(walk) == 62 and len(speeches) == 36
        assert sum(command['word'] == 0x8000 for command in walk) == 3
        assert sum(command['word'] in [0x100, 0x200, 0x300, 0x400] for command in walk) == 12
        assert sum(command['word'] == 0 for command in walk) == 1
        assert sum(command['word'] == 0xA000 for command in walk) == 5
        objects, texts = [], []
        for source, command in zip(group['all_clean_native_commands'], commands, strict=True):
            at = command['offset'] + first - 8
            mapped = next(entry for entry in walk if entry['offset'] == at)
            assert mapped['word'] == source['word'] and mapped['whole_command_hex'] == command['whole_command_hex']
            row = next((row for row in group['records'] if row['source_reference']['header_offset'] == source['offset']), None)
            objects.append(dict(source_block=169, source_offset=source['offset'], source_word=source['word'],
                fixture_offset=at, native_extent=command['native_extent'], whole_command_hex=command['whole_command_hex'],
                text_ID=None if row is None else row['id']))
            if row is not None:
                texts.append(dict(id=row['id'], source_block=169, source_record_index=row['source_record_index'],
                    fixture_command_offset=at, source_selector=row['source_selector'], native_extent=command['native_extent'],
                    complete_preamble_hex=bytes.fromhex(command['whole_command_hex'])[:6].hex(), whole_command_hex=command['whole_command_hex']))
        path = Path(f'out/lil_B169_display_v4241_{case}_RESEARCH_ONLY.nds')
        assert not path.exists()
        image = NdsImage.open(PARENT)
        blocks = list(current)
        blocks[22] = target
        image.replace_file('/data/SC2.DK4', IlnkContainer(blocks).to_bytes())
        image.save(path)
        saved = NdsImage.open(path)
        assert [name for _, name, value in parent.iter_files() if saved.read_file(name) != value] == ['/data/SC2.DK4']
        assert all(saved.read_file(name) == value for name, value in parent.iter_components())
        after = IlnkContainer.parse(saved.read_file('/data/SC2.DK4')).blocks
        assert [n for n, (a, b) in enumerate(zip(current, after, strict=True)) if a != b] == [22]
        fixtures.append(dict(case=case, source_block=169, research_ROM=str(path), research_ROM_sha256=sha(path.read_bytes()),
            fixture_block=22, fixture_block_hex=target.hex(), fixture_block_sha256=sha(target),
            original_B22_prelude_hex=prelude.hex(), original_B22_prelude_commands=init[:9],
            selected_original_objects=objects, original_text_records=texts, explicitly_excluded_original_commands=[],
            all62_stored_fixture_commands=walk, all12_relative_operands_three_predicates_and_single_tail_end_preserved=True,
            all36_progressive_source_texts_and_later_A000_retained_without_flattening=True,
            all335_other_SC2_blocks_and_every_other_file_component_exact=True))
    save(ROOT / 'complete_effect_preserving_B22_fixtures.json', dict(parent=str(PARENT), parent_sha256=sha(PARENT.read_bytes()),
        manuscript=str(DOC), manuscript_sha256=sha(DOC.read_bytes()), relocation_plan=str(PLAN), relocation_plan_sha256=sha(PLAN.read_bytes()),
        fixtures=fixtures, source_port_not_stated_initialized_fixture_town_is_Amsterdam=True,
        source_event169_not_selected_or_eligibility_earned=True,
        original_B22_nine_init_commands_including_four_A000s_preserved=True,
        source_B169_later_numeric29_0001_A000_and_no_invented_resources_presentations_FE=True,
        all_three_original_membership_queries_retained_unforced=True,
        expected_conditional_speech_IDs=['DK4_MES_B169_R0067', 'DK4_MES_B169_R0082', 'DK4_MES_B169_R0097'],
        stored_speech_objects=36, actual_conditional_path_to_be_observed_without_forcing=True,
        no_savestate_or_RAM_or_funds_fixture=True, not_registered_candidate_or_new_release_parent=True,
        producer_sha256=sha(Path(__file__).read_bytes()), full_goal_complete=False))
    print('Paired B169 fixtures:36 progressive speeches,12 spans,three unforced predicates and later numeric29/0001 A000;no source command omitted.')
