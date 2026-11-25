"""Observe the original fleet and company field loads from ordinary battery saves."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path

from scripts import observe_copenhagen_docking_20261124 as copenhagen
from scripts import observe_online_gallery_common_v1 as playback
from scripts import register_nagasaki_contract_wrap_20261124 as current
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import REGISTRY, digest, read, reference


ROOT = Path(".codex-release-work/shared_display_20261123/fleet_battery_reads_20261124")
BASE, WRAM_END = 0x02000000, 0x02400000
READS = {0x020342B8: ("docking", 10, 0x3C), 0x020342E8: ("destination", 10, 0x3F),
         0x0203CD98: ("headquarters", 5, 0x0B)}
CALLS = {pc + offset: (*field, bool(offset)) for pc, field in READS.items() for offset in (0, 4)}


def schedule(case):
    if case == "copenhagen":
        inputs, _, _, path, donor = copenhagen.schedule("landing")
        hold = 4000
    else:
        assert case == "nagasaki"
        path = current.build.REPLAY
        verified = read(current.build.PAIRED)
        assert verified["after"] == reference(path) and verified["ordinary_saved_game"]
        history = read(path)
        assert history["cold_boot"] and not history["savestate_loaded"] and not history["callback_errors"]
        assert not any(v for k, v in history.items() if k.startswith("synthetic_"))
        inputs, donor, hold = history["scripted_input_schedule"], history["battery_save_preloaded"], 3720
    assert digest(donor["source"]) == donor["source_sha256"]
    return [event for event in inputs if event["start"] < hold], (hold,), hold + 1, path, donor


def observe(rom, folder):
    source = checked_text(getsource(playback.observer), {
        'REQUESTS=REQUESTS, ONLINE=ONLINE, GALLERY=GALLERY)':
            'REQUESTS=REQUESTS, ONLINE=ONLINE, GALLERY=GALLERY, CALLS=CALLS, BASE=BASE, WRAM_END=WRAM_END, __file__=__file__)',
        '    ptr=v[6]\n': '''    field, register, offset, after = CALLS[pc]
    owner = v[4 + register]
    field_address = owner + offset
    assert BASE <= owner < field_address < WRAM_END
    byte = ct.c_ubyte.from_address(self.wram + field_address - BASE).value
    if after:
     self.rows.append(dict(PC=pc, frame=frame, field=field, owner=owner, phase="after", success=v[4], value=byte))
    else:
     assert v[5] == field_address and v[6] == 0
     stream = v[4]
     pointer, cursor, source_byte = None, None, None
     if BASE <= stream <= WRAM_END - 0x44:
      pointer, cursor = struct.unpack('<2I', ct.string_at(self.wram + stream + 0x1c - BASE, 8))
     else:
      dtcm = ct.c_uint32.from_address(self.dtcm_base).value
      if dtcm <= stream <= dtcm + 0x4000 - 0x44:
       pointer, cursor = struct.unpack('<2I', ct.string_at(self.dtcm + stream + 0x1c - dtcm, 8))
     if pointer is not None and BASE <= pointer + cursor < WRAM_END:
      source_byte = ct.c_ubyte.from_address(self.wram + pointer + cursor - BASE).value
     self.rows.append(dict(PC=pc, frame=frame, field=field, owner=owner, phase="before", stream=stream,
                           buffer=pointer, buffer_offset=cursor, saved_byte=source_byte, value=byte))
    return
    ptr=v[6]
''',
    })
    scope = vars(playback) | dict(TARGETS=tuple(CALLS), CALLS=CALLS, BASE=BASE, WRAM_END=WRAM_END, __file__=__file__)
    exec(compile(source, __file__ + "::battery-field-observer", "exec"), scope)
    return scope["observer"](rom, folder)


def main(case):
    assert digest(REGISTRY) == read(current.RELEASE)["registry_sha256"]
    source = checked_text(getsource(playback.main), {
        "'--capture-at', *map(str, frames)]": "'--dump-capture-ram', '--capture-at', *map(str, frames)]",
    })
    scope = vars(playback) | dict(ROOT=ROOT, parent=current, get_schedule=schedule, observer=observe, FOCUS=set(), __file__=__file__)
    exec(compile(source, __file__ + "::ordinary-battery-file", "exec"), scope)
    scope["main"](case)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=("copenhagen", "nagasaki"))
    main(parser.parse_args().case)
