"""Run all reviewed service layouts with the production component and write watch."""

from pathlib import Path

from unicorn import UC_HOOK_MEM_WRITE

from dk4tool.patch import port_services_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.shipyard_editorial import BANKS
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, machine
import scripts.probe_port_services_v761 as probe
from scripts.verify_market_gameplay_v753 import snapshot
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/port_services_v762')


def main():
    source = NdsImage.open(probe.CURRENT).read_file('/__arm9__.bin')
    target, plan = owned.runtime_transform(source)
    assert target == (ROOT / 'research_runtime_ARM9.bin').read_bytes()
    raw = snapshot(read(probe.RAM_REPORT), 3200)
    writes, machines = [], []
    def load(unused_arm, changed=True):
        u = machine(target if changed else source); u.mem_write(BASE, raw)
        if changed:
            for p in plan['patches']:
                before, after = bytes.fromhex(p['source_hex']), bytes.fromhex(p['target_hex'])
                assert bytes(u.mem_read(p['address'], len(before))) == before
                u.mem_write(p['address'], after)
        def watch(cpu, kind, at, length, value, unused):
            if any(at < hi and at + length > lo for lo, hi in BANKS):
                writes.append([at, length, value]); raise AssertionError('Native write into immutable bank')
        u.hook_add(UC_HOOK_MEM_WRITE, watch); machines.append(changed)
        return u
    probe.loaded = load
    probe.DEST = ROOT / 'native_owned'
    probe.main()
    before = read('work/analysis/shipyard_continuation_v761/native_RESEARCH/verification.json')
    after = read(probe.DEST / 'verification.json')
    assert after['dispatch'] == before['dispatch'] and after['all1124_prior_Yard_layouts_identical']
    for a, b in zip(before['complete_native_font_cases'], after['complete_native_font_cases'], strict=True):
        for key in ('id', 'values_hex', 'template_hex', 'formatted_hex', 'lines', 'preview_sha256'):
            assert a[key] == b[key]
    assert not writes
    save(ROOT / 'owned_native_verification.json', {'source_ARM9_sha256': sha(source), 'runtime_ARM9_sha256': sha(target),
        'all40_complete_layout_font_planes_identical_to_reviewed_research': True,
        'all1124_prior_Yard_outputs_and36680_dispatch_cases_pass': True,
        'writes_into_all_four_immutable_banks': writes, 'write_watched_initialized_machines': len(machines),
        'all_actual_initialized_source_spans_match_before_install': True,
        'native_case_report_sha256': sha((probe.DEST / 'verification.json').read_bytes()),
        'producer_sha256': sha(Path(__file__).read_bytes()), 'borrowed_driver_sha256': sha(Path(probe.__file__).read_bytes()),
        'whole_ROM_loading_and_actual_gameplay_still_pending': True})
    print('Production locations pass40 complete native planes,1124 prior outputs,36680 memberships;no immutable-bank writes.', flush=True)


if __name__ == '__main__': main()
