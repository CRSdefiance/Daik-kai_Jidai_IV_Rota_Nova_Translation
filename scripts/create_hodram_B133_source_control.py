"""Retain the original Japanese monster script in the same declared startup fixture."""
import struct
from copy import deepcopy
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory

ROOT = Path('work/analysis/Hodram_B133_source_control_20261102')


def main():
    assert not ROOT.exists()
    original_fixture = Path('work/analysis/Hodram_B131_B150_English_fixtures_20261102/fixtures.json')
    base = load(original_fixture)
    old = next(f for f in base['fixtures'] if f['block'] == 133)
    reference = Path(base['reference'])
    assert sha(reference.read_bytes()) == base['reference_sha256']
    image = NdsImage.open(reference)
    path = '/data/SC1.DK4'
    archive = image.read_file(path)
    bank = IlnkContainer.parse(archive).blocks
    clean = IlnkContainer.parse(NdsImage.open('work/clean.nds').read_file(path)).blocks[133]
    end = 8 + struct.unpack_from('<H', clean, 4)[0]
    assert not any(clean[end:])
    prelude = bytes.fromhex(old['prelude_hex'])
    assert prelude == bank[42][8:42]
    logical = bytearray(bank[42][:8] + prelude + clean[8:end])
    struct.pack_into('<H', logical, 4, len(logical) - 8)
    target = bytes(logical) + bytes(-len(logical) % 4)
    inventory, _, _ = scoped_inventory()
    source_commands, _ = inventory(image.read_file('/__arm9__.bin'), clean)
    commands, _ = inventory(image.read_file('/__arm9__.bin'), target)
    for command in source_commands:
        moved = next(c for c in commands if c['offset'] == command['offset'] + 34)
        assert moved['word'] == command['word'] and moved['whole_command_hex'] == command['whole_command_hex']
    assert source_commands[-2]['word'] == 0xC600
    altered = deepcopy(image)
    blocks = list(bank)
    blocks[42] = target
    altered.replace_file(path, IlnkContainer(blocks).to_bytes())
    restored = list(blocks)
    restored[42] = bank[42]
    assert IlnkContainer(restored).to_bytes() == archive
    assert all(altered.read_file(p) == value for p, value in image.iter_components())
    assert [p for _, p, value in image.iter_files() if altered.read_file(p) != value] == [path]
    ROOT.mkdir(parents=True)
    rom = ROOT / 'original_Japanese_B133_initialized_RESEARCH_ONLY.nds'
    rom.write_bytes(bytes(altered.rom.save()))
    inputs = Path(old['inputs'])
    schedule = [r for r in load(inputs) if r['start'] < 5001]
    input_path = ROOT / 'ordinary_inputs.json'
    save(input_path, schedule)
    fixture = {**old, 'frames': 5001, 'research_ROM': str(rom), 'research_ROM_sha256': sha(rom.read_bytes()),
               'source_script_sha256': sha(clean), 'source_command_count': len(source_commands),
               'inputs': str(input_path), 'inputs_sha256': sha(input_path.read_bytes()),
               'capture_folder': 'work/emulation_v193/Hodram_B133_Japanese_control_20261102',
               'original_Japanese_control_not_target_English': True,
               'next_battle_command_C600_preserved': True}
    save(ROOT / 'fixtures.json', dict(reference=str(reference), reference_sha256=sha(reference.read_bytes()),
         original_English_fixture=str(original_fixture), original_English_fixture_sha256=sha(original_fixture.read_bytes()),
         fixtures=[fixture], source_commands=source_commands, all_nontext_commands_exact=True,
         source_scene_battle_state_not_naturally_earned=True, new_credit=0,
         producer_sha256=sha(Path(__file__).read_bytes())))
    print('Original Japanese B133 control prepared; same initializers, role and C600 battle command; no source-result claim yet.')


if __name__ == '__main__':
    main()
