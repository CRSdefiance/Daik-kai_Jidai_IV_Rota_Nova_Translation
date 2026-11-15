"""Create paired B22 content fixtures retaining B166's actual conditions and advice paths."""
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B166_display_fixture_v4101')
PARENT = Path('out/all_routes_combined_v4046_candidate.nds')
PLAN = Path('work/analysis/lil_B166_relocation_v4093/nested_source_relocation_research.json')
DOC = Path('translations/lil_B166_editorial_manuscript_v5.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    plan, doc = map(read, [PLAN, DOC])
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
    first = next(c['offset'] for c in init if c['word'] == 0x4000)
    assert first == 56 and len(init[:9]) == 9 and sum(c['word'] == 0xA000 for c in init[:9]) == 4
    prelude = b22[8:first]
    group = packet['blocks'][0]
    ROOT.mkdir(parents=True)
    fixtures = []
    for case, bank in [('clean_Japanese', jp), ('reviewed_English', en)]:
        commands, _ = inventory(arm, bank[166])
        omitted = [c for c in commands if c['word'] == 0xA000]
        assert len(omitted) == 1 and omitted[0]['native_extent'] == 8
        cut = omitted[0]['offset']
        assert cut > next(c['offset'] for c in commands if c['word'] == 0x2100)
        for command in commands:
            if command['word'] in [0x100, 0x200, 0x300, 0x400]:
                span = int.from_bytes(bank[166][command['offset']+2:command['offset']+4], 'little')
                assert command['offset'] + 4 + span <= cut
        logical_end = 8 + struct.unpack_from('<H', bank[166], 4)[0]
        payload = bank[166][8:cut] + bank[166][cut+8:logical_end]
        logical = bytearray(b22[:8] + prelude + payload)
        struct.pack_into('<H', logical, 4, len(logical)-8)
        target = bytes(logical) + bytes(-len(logical) % 4)
        walk, speeches = inventory(arm, target)
        assert len(walk) == 70 and len(speeches) == 42
        assert sum(c['word'] == 0x2100 for c in walk) == sum(c['word'] == 0x8000 for c in walk) == 1
        assert sum(c['word'] in [0x100,0x200,0x300,0x400] for c in walk) == 8
        assert sum(c['word'] == 0 for c in walk) == 1
        objects, texts = [], []
        for source, command in zip(group['all_clean_native_commands'], commands, strict=True):
            if command['word'] == 0xA000:
                continue
            at = command['offset'] + first - 8 - (8 if command['offset'] > cut else 0)
            mapped = next(w for w in walk if w['offset'] == at)
            assert mapped['word'] == source['word'] and mapped['whole_command_hex'] == command['whole_command_hex']
            row = next((r for r in group['records'] if r['source_reference']['header_offset'] == source['offset']), None)
            objects.append(dict(source_block=166, source_offset=source['offset'], source_word=source['word'],
                fixture_offset=at, native_extent=command['native_extent'], whole_command_hex=command['whole_command_hex'],
                text_ID=None if row is None else row['id']))
            if row is not None:
                texts.append(dict(id=row['id'], source_block=166, source_record_index=row['source_record_index'],
                    fixture_command_offset=at, source_selector=row['source_selector'], native_extent=command['native_extent'],
                    complete_preamble_hex=bytes.fromhex(command['whole_command_hex'])[:6].hex(), whole_command_hex=command['whole_command_hex']))
        path = Path(f'out/lil_B166_display_v4101_{case}_RESEARCH_ONLY.nds')
        assert not path.exists()
        image = NdsImage.open(PARENT)
        blocks = list(current)
        blocks[22] = target
        image.replace_file('/data/SC2.DK4', IlnkContainer(blocks).to_bytes())
        image.save(path)
        saved = NdsImage.open(path)
        assert [p for _, p, value in parent.iter_files() if saved.read_file(p) != value] == ['/data/SC2.DK4']
        assert all(saved.read_file(p) == value for p, value in parent.iter_components())
        fixtures.append(dict(case=case, source_block=166, research_ROM=str(path), research_ROM_sha256=sha(path.read_bytes()),
            fixture_block=22, fixture_block_hex=target.hex(), fixture_block_sha256=sha(target),
            original_B22_prelude_hex=prelude.hex(), original_B22_prelude_commands=init[:9],
            selected_original_objects=objects, original_text_records=texts,
            explicitly_excluded_original_commands=[dict(source_block=166, source_offset=2940, word=0xA000,
                original_command=c, reason='Only the late recruitment effect is omitted in the content fixture; no earned recruitment claim.') for c in omitted],
            all70_stored_fixture_commands=walk, all8_relative_operands_one_predicate_and_single_end_preserved=True,
            original_choice_and42_texts_retained_without_flattening=True,
            all335_other_SC2_blocks_and_every_other_file_component_exact=True))
    save(ROOT / 'complete_choice_preserving_B22_fixtures.json', dict(parent=str(PARENT), parent_sha256=sha(PARENT.read_bytes()),
        manuscript=str(DOC), manuscript_sha256=sha(DOC.read_bytes()), relocation_plan=str(PLAN), relocation_plan_sha256=sha(PLAN.read_bytes()),
        fixtures=fixtures, source_port_not_stated_initialized_fixture_town_is_Amsterdam=True,
        source_event166_not_selected_or_eligibility_earned=True,
        original_B22_nine_init_commands_including_four_A000s_preserved=True,
        one_late_recruitment_effect_excluded_after_choice_without_changing_any_branch_span=True,
        original_Fernando_membership_query_retained_unforced=True,
        all_original_choice_relative_containers_presentation_resources_and_single_end_preserved=True,
        expected_conditional_Fernando_speech_ID='DK4_MES_B166_R0087',
        stored_speech_objects=42, actual_conditional_path_to_be_observed_without_forcing=True,
        no_savestate_or_RAM_or_funds_fixture=True, not_registered_candidate_or_new_release_parent=True,
        producer_sha256=sha(Path(__file__).read_bytes()), full_goal_complete=False))
    print('Paired B166 B22 fixtures created:42 speeches,8 spans,Fernando query,original advice menu,single end;late recruitment effect omitted.')
