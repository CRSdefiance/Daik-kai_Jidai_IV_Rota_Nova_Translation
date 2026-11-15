"""Trace the DS checksum error using a one-bit change in a disposable save copy."""

from argparse import ArgumentParser
from hashlib import sha256
from inspect import getsource
from pathlib import Path
from struct import unpack_from

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.damaged_save_release import OFFSET, formatted_suffix
from scripts import observe_continue_empty_slot_20261115 as prior
from scripts import observe_online_gallery_common_v1 as playback
from scripts import register_expedition_report_wraps_20261115 as current
from scripts import observe_market_context_v2112 as native
from scripts.execute_map_entity_tooltip_copy import machine_for
from scripts.probe_button_prompt_native import call
from scripts.source_locked_derivation_v5118 import checked_text


base = current.base
ROOT = Path('work/damaged_save_20261115_v1')
DONOR = prior.historical.DONOR
COPY = ROOT / 'checksum_only_slot1.dsv'
FIXTURE = ROOT / 'checksum_fixture.json'
LOAD_BRANCH = 0x020EE75C
ERROR_MODAL = 0x020EE780
REQUESTS = {0x020534F4: 5, 0x0205528C: 4}
TARGETS = (*REQUESTS, LOAD_BRANCH, ERROR_MODAL)
BASE = 0x02000000


def prepare_save():
    source = DONOR.read_bytes()
    assert len(source) == 262266 and source[:4] == b'DK4R' and source[0x3C000:0x3C004] == b'DK4R'
    assert source[0xA000:0x3C000] == b'\xFF' * (0x3C000 - 0xA000)
    modified = source[:4] + bytes((source[4] ^ 1,)) + source[5:]
    assert [i for i, (a, b) in enumerate(zip(source, modified, strict=True)) if a != b] == [4]
    clean, arm = (base.NdsImage.open(path).read_file(current.stage.ARM) for path in (current.stage.CLEAN, current.ROM))
    spans = ((0xEE078, 0xEE0C4), (0xEE67C, 0xEE7E0), (0xEEC78, 0xEED18))
    assert all(clean[lo:hi] == arm[lo:hi] for lo, hi in spans)
    assert arm[OFFSET:].split(b'\0', 1)[0] == formatted_suffix().encode('ascii')
    pointer = 0x02400000
    checks = []
    for data in (source, modified):
        u = machine_for(arm)
        u.mem_write(pointer, data[:0xA000])
        call(u, 0xEEC78, (pointer,), instruction_limit=400_000)
        checks.append(dict(stored=unpack_from('<I', data, 4)[0], calculated=u.reg_read(UC_ARM_REG_R0)))
        assert bytes(u.mem_read(pointer, 0xA000)) == data[:0xA000]
    assert checks[0]['stored'] == checks[0]['calculated'] == checks[1]['calculated']
    assert checks[1]['stored'] == checks[0]['stored'] ^ 1
    ROOT.mkdir()
    COPY.write_bytes(modified)
    base.save(FIXTURE, dict(donor=str(DONOR), donor_sha256=sha256(source).hexdigest(),
        disposable_copy=str(COPY), copy_sha256=sha256(modified).hexdigest(), single_changed_file_offset=4,
        slot_index=0, native_checksum_results=checks, source_exact_ARM9_ranges=spans,
        donor_and_copy_same_size=True, original_unchanged=base.digest(DONOR) == sha256(source).hexdigest()))


def observer(rom, folder):
    env = vars(native) | dict(ROOT=folder, ROM=rom, TARGETS=TARGETS, REQUESTS=REQUESTS,
                              LOAD_BRANCH=LOAD_BRANCH, ERROR_MODAL=ERROR_MODAL)
    setup = checked_text(getsource(native.prepare_contract), {'for pc in(REQUEST,FONT):': 'for pc in TARGETS:'})
    exec(compile(setup, __file__ + '::source-locked-checksum-observer', 'exec'), env)
    env['prepare_contract']()
    original = getsource(native.Observer)
    start = original.index('    if frame<31000:return')
    end = original.index('   except BaseException as exc:', start)
    body = """    if pc in REQUESTS:
     self.requests.append(dict(frame=frame,PC=pc,message_ID=v[REQUESTS[pc]],caller_LR=v[18]))
     return
    if pc==LOAD_BRANCH:
     self.rows.append(dict(frame=frame,PC=pc,slot=v[14],calculated=v[4],stored=v[5]))
     return
    assert pc==ERROR_MODAL and 0x02000000<=v[4]<0x023fffc4
    stack=ct.string_at(self.wram+v[4]-0x02000000,60)
    end=stack.index(0)
    self.rows.append(dict(frame=frame,PC=pc,body_hex=stack[:end].hex(),pointer=v[4]))
"""
    exec(compile(original[:start] + body + original[end:], __file__ + '::watch-checksum-branch-and-modal', 'exec'), env)
    return env['Observer']


def schedule(case):
    assert case == 'corrupt_slot'
    events, _, _, _, _ = prior.schedule('continue')
    events = events[:6] + [dict(start=4101, duration=8, buttons=['A']),
                          dict(start=4501, duration=8, buttons=['B']),
                          dict(start=4901, duration=8, buttons=['B'])]
    frames = [2200, 2600, 3000, 3400, 3700, 3800, 4200, 4400, 4700, 5100]
    return events, frames, 5150, prior.historical.HISTORY, dict(source=str(COPY), source_sha256=base.digest(COPY))


def main():
    prepare_save()
    env = vars(playback) | dict(ROOT=ROOT, parent=current, FOCUS=set(range(98, 125)),
                                get_schedule=schedule, observer=observer, __file__=__file__)
    exec(compile(getsource(playback.main), __file__ + '::original-load-navigation', 'exec'), env)
    env['main']('corrupt_slot')
    fixture = base.load(FIXTURE)
    assert base.digest(DONOR) == fixture['donor_sha256'] and base.digest(COPY) == fixture['copy_sha256']


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--attempt', type=int, default=1, choices=range(1, 100))
    attempt = parser.parse_args().attempt
    ROOT = ROOT.with_name(f'damaged_save_20261115_v{attempt}')
    COPY, FIXTURE = ROOT / COPY.name, ROOT / FIXTURE.name
    main()
