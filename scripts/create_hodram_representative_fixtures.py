"""Two complete revised scenes after original initializers; not natural event activation."""
import argparse
import struct
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    assert not args.out.exists()
    rebuild_path = Path('work/analysis/Hodram_B61_B70_stored_20261101/reconstruction.json')
    native_path = Path('work/analysis/Hodram_B61_B70_stored_native_20261101/stored_native_verification.json')
    rebuilt, native = load(rebuild_path), load(native_path)
    assert native['research_ROM_sha256'] == rebuilt['research_ROM_sha256']
    reference = Path(rebuilt['research_ROM'])
    assert sha(reference.read_bytes()) == rebuilt['research_ROM_sha256']
    image = NdsImage.open(reference)
    arm = image.read_file('/__arm9__.bin')
    path = '/data/SC1.DK4'
    archive = image.read_file(path)
    bank = IlnkContainer.parse(archive).blocks
    clean = IlnkContainer.parse(NdsImage.open('work/clean.nds').read_file(path)).blocks
    inventory, _, _ = scoped_inventory()
    commands, speeches = inventory(arm, bank[42])
    first = speeches[0]['offset']
    prelude = bank[42][8:first]
    initializers = [c for c in commands if c['offset'] < first]
    assert first == 42 and len(prelude) == 34 and len(initializers) == 8
    assert prelude == clean[42][8:first]
    assert all(c['word'] not in (0x4000, 0x100, 0x200, 0x300, 0x400, 0x8000, 0x8100, 0) for c in initializers)
    ordinary_path = Path('work/analysis/hodram_opening_context_v2018/ordinary_Hodram_NewGame_inputs.json')
    ordinary = load(ordinary_path)
    assert sum(r['buttons'] == ['RIGHT'] for r in ordinary) == 1
    args.out.mkdir(parents=True)
    fixtures = []
    for number, frames in [(67, 16001), (69, 8001)]:
        group = next(g for g in rebuilt['groups'] if g['block'] == number)
        selected = bank[number]
        assert sha(selected) == group['target_sha256']
        end = group['new_logical_end']
        assert not any(selected[end:])
        assert selected[:4] == bank[42][:4] and selected[6:8] == bank[42][6:8]
        logical = bytearray(bank[42][:8] + prelude + selected[8:end])
        struct.pack_into('<H', logical, 4, len(logical) - 8)
        fixture_block = bytes(logical) + bytes(-len(logical) % 4)
        actual, actual_texts = inventory(arm, fixture_block)
        assert len(actual) == len(group['all_target_commands']) + 8
        assert len(actual_texts) == len(group['text_records']) and len(fixture_block) < 0x2400
        for command in group['all_target_commands']:
            moved = next(c for c in actual if c['offset'] == command['offset'] + 34)
            assert moved['word'] == command['word'] and moved['whole_command_hex'] == command['whole_command_hex']
            assert moved['native_extent'] == command['native_extent']
            assert moved['ancestor_0100_offsets'] == [a + 34 for a in command['ancestor_0100_offsets']]
        assert actual[-1]['word'] == 0 and actual[-1]['offset'] + 4 == len(logical)
        current = NdsImage.open(reference)
        blocks = list(bank)
        blocks[42] = fixture_block
        current.replace_file(path, IlnkContainer(blocks).to_bytes())
        assert all(current.read_file(p) == v for p, v in image.iter_components())
        assert [p for _, p, v in image.iter_files() if current.read_file(p) != v] == [path]
        restored = list(blocks)
        restored[42] = bank[42]
        assert IlnkContainer(restored).to_bytes() == archive
        rom = args.out / f'Hodram_B{number}_initialized_RESEARCH_ONLY.nds'
        rom.write_bytes(bytes(current.rom.save()))
        inputs = args.out / f'B{number}_ordinary_inputs.json'
        save(inputs, ordinary + [dict(start=f, duration=5, buttons=['A'])
                                 for f in range(4000, frames - 480, 240)])
        fixtures.append(dict(block=number, frames=frames, research_ROM=str(rom), research_ROM_sha256=sha(rom.read_bytes()),
            source_script_sha256=sha(selected), source_command_count=len(group['all_target_commands']),
            source_speech_count=len(group['text_records']), fixture_block=42,
            original_initializer_commands=initializers, prelude_hex=prelude.hex(),
            every_original_command_preamble_relative_andnormal_end_preserved=True,
            only_opening_block_replaced_with_exact_archive_inverse=True,
            inputs=str(inputs), inputs_sha256=sha(inputs.read_bytes()),
            no_savestate_RAM_eventflag_RNG_roster_money_orconditional_result_override=True,
            initialized_scene_fixture_not_natural_optional_event_activation=True,
            capture_folder=f'work/emulation_v193/Hodram_pending_B{number}_20261101'))
    save(args.out / 'fixtures.json', dict(reference=str(reference), reference_sha256=rebuilt['research_ROM_sha256'],
        fixtures=fixtures, native_proof=str(native_path), native_proof_sha256=sha(native_path.read_bytes()),
        ordinary_inputs=str(ordinary_path), ordinary_inputs_sha256=sha(ordinary_path.read_bytes()),
        producer_sha256=sha(Path(__file__).read_bytes()), actual_coverage_pending=True, new_credit=0))
    print('Two full-script initialized scene fixtures prepared; no natural activation or gameplay coverage claimed yet.')


if __name__ == '__main__':
    main()
