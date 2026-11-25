"""Test whether the original company-information text planes reach the DS screen."""

from pathlib import Path
from struct import unpack_from

from scripts import replay_faction_information_20261115 as replay
from scripts.prepare_all_routes_promotion_20261111 import verify_runtime
from scripts.verify_release_baseline import files


current, base, ROOT = replay.current, replay.base, replay.ROOT
ROM = ROOT / 'faction_information_english_RESEARCH_ONLY.nds'
PLAN = ROOT / 'probe_plan.json'
BASE = 0x02000000
# The Power formatter supplies global power first and regional power second.
FIELDS = (
    (0x3D914, 0x137914, 12, '所持金　', 'Funds ', (0x0203D678,),
     'The faction’s available funds. Funds is the label the related DS panel uses.'),
    (0x3D920, 0x137928, 28, '勢力値（%s）　%6d（%4d）', 'Pwr %s %d(%d)', (0x0203D70C,),
     'The region, the faction’s global power and its power in the selected region. Keep both values in order and distinguish the regional one in parentheses.'),
    (0x3D924, 0x137944, 12, '勢力値　%6d', 'Power %6d', (0x0203D728,),
     'The faction’s global power. The separate unfiltered view has one number.'),
    (0x3D92C, 0x137950, 12, '本拠地　', 'Home ', (0x0203D750,),
     'The faction’s home base. Home is the existing compact DS label beside the town name.'),
    (0x3D934, 0x13795C, 8, '友好度', 'Ties ', (0x0203D7B4,),
     'The faction’s standing with the player’s company. Ties matches the related relationship chart.'),
)


def main():
    assert not ROM.exists() and not PLAN.exists()
    release = base.load(current.RELEASE)
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    assert base.digest(current.ROM) == release['candidate_sha256']
    assert base.digest(current.stage.CLEAN) == release['clean_input_sha256']
    assert base.digest(current.MANIFEST) == release['manifest_sha256']
    clean, previous = [base.NdsImage.open(path) for path in (current.stage.CLEAN, current.ROM)]
    arm_path = current.stage.ARM
    source, before = [image.read_file(arm_path) for image in (clean, previous)]
    target = bytearray(before)
    values = []
    for literal, offset, size, japanese, english, calls, note in FIELDS:
        assert before[literal:literal + 4] == source[literal:literal + 4]
        assert unpack_from('<I', before, literal)[0] == BASE + offset
        old = (japanese.encode('cp932') + b'\0').ljust(size, b'\0')
        new = (english.encode('ascii') + b'\0').ljust(size, b'\0')
        assert len(old) == len(new) == size and source[offset:offset + size] == before[offset:offset + size] == old
        assert old.count(b'%') == new.count(b'%')
        target[offset:offset + size] = new
        values.append(dict(ARM9_literal=literal, ARM9_offset=offset, capacity_bytes=size, clean_Japanese=japanese,
                           current_bytes_hex=old.hex(), proposed_bytes_hex=new.hex(), proposed_English=english,
                           native_caller_addresses=list(calls), localization_note=note))
    verify_runtime(bytes(target), release)
    inverse = bytearray(target)
    for row in values:
        offset, size = row['ARM9_offset'], row['capacity_bytes']
        inverse[offset:offset + size] = before[offset:offset + size]
    assert inverse == before
    prior_files = files(previous)
    previous.replace_file(arm_path, bytes(target))
    assert {name for name, raw in files(previous).items() if raw != prior_files[name]} == {arm_path}
    previous.save(ROM)
    previous.replace_file(arm_path, before)
    assert bytes(previous.rom.save()) == current.ROM.read_bytes()
    base.save(PLAN, dict(previous_ROM_sha256=release['candidate_sha256'], research_ROM=str(ROM),
                         research_ROM_sha256=base.digest(ROM), source_and_current_values=values,
                         whole_parent_inverse_exact=True, source_controls_and_numeric_arguments_preserved=True,
                         release_status='research only, pending visible consumer and native display checks'))
    print('Staged five temporary English strings for the company-information visibility probe.')


if __name__ == '__main__':
    main()
