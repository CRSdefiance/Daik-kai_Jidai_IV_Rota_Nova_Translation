"""Reuse an exact registered ROM's own ordinary-startup snapshot for native checks."""
from pathlib import Path
from types import FunctionType, SimpleNamespace

from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load
from scripts.probe_escape_direct_source_v1186 import machine as original_machine


class RegisteredRuntime:
    def __init__(self, release, startup):
        self.release_path, self.startup_path = Path(release), Path(startup)
        self.release, self.startup = load(release), load(startup)
        self.rompath = Path(self.release['candidate'])
        assert sha(self.rompath.read_bytes()) == self.release['candidate_sha256'] == self.startup['candidate_sha256']
        assert not self.release['own_registered_startup_pending'] and self.release['clean_input_patch_byte_exact']
        assert self.startup['cold_boot'] and not self.startup['savestate'] and self.startup['actual_captain_getter'] == 1
        self.image = NdsImage.open(self.rompath)
        self.arm = self.image.read_file('/__arm9__.bin')
        self.common = self.image.read_file('/COMMON/MESFILE.DK4')
        snapshot = self.startup['read_only_snapshot']
        self.raw = Path(snapshot['path']).read_bytes()
        assert snapshot['read_only_export'] and len(self.raw) == 0x400000 and sha(self.raw) == snapshot['sha256']
        self.sections = MainCodeFile(self.arm, BASE).sections
        payload = bytes(self.sections[3].data[:-48])
        assert len(payload) == 123264 and self.raw[POOL - BASE:POOL - BASE + len(payload)] == payload
        self.sections = [*self.sections, SimpleNamespace(ramAddress=POOL, data=payload)]
        self.plan = dict(patches=[])
        cpu, get, _ = original_machine(self.arm, self.common, self.raw, self.plan)
        self.actor_root = get(0xCB184)
        assert get(0x7F244) == 1
        self.actor_bytes = bytes(cpu.mem_read(self.actor_root, 0x1A04))
        self.calls = []

    def machine(self, arm, common, raw, plan):
        assert arm == self.arm and common == self.common and raw == self.raw and plan == self.plan
        cpu, get, provider = original_machine(arm, common, raw, plan)
        assert get(0xCB184) == self.actor_root and get(0x7F244) == 1
        assert bytes(cpu.mem_read(self.actor_root, 0x1A04)) == self.actor_bytes
        executed = set()
        def exact(u, pc, size, _):
            owners = [s for s in self.sections if s.ramAddress <= pc and pc + size <= s.ramAddress + len(s.data)]
            assert len(owners) == 1, hex(pc)
            s = owners[0]
            assert bytes(u.mem_read(pc, size)) == bytes(s.data[pc - s.ramAddress:pc - s.ramAddress + size]), hex(pc)
            executed.add(pc)
        cpu.hook_add(UC_HOOK_CODE, exact)
        provider.executed_current = executed
        self.calls.append(cpu)
        return cpu, get, provider

    def execute(self, fn, *args):
        assert not self.calls
        bound = FunctionType(fn.__code__, {**fn.__globals__, 'machine': self.machine,
                             'portrait_machine': self.machine}, argdefs=fn.__defaults__)
        try:
            result = bound(self.arm, self.common, self.raw, self.plan, *args)
            assert len(self.calls) == 1
            assert bytes(self.calls[0].mem_read(self.actor_root, 0x1A04)) == self.actor_bytes
            return result
        finally:
            self.calls.clear()

    def receipt(self):
        return dict(candidate=str(self.rompath), candidate_sha256=self.release['candidate_sha256'],
            ARM9_sha256=sha(self.arm), COMMON_sha256=sha(self.common),
            release_proof=str(self.release_path), release_proof_sha256=sha(self.release_path.read_bytes()),
            startup_proof=str(self.startup_path), startup_proof_sha256=sha(self.startup_path.read_bytes()),
            snapshot=self.startup['read_only_snapshot'], captain=1, current_own_snapshot_not_historical_overlay=True,
            complete_staged_payload_exact=True, original_COMMON_cache_reset_andhost_IO_boundaries_disclosed=True,
            native_offline_checks_not_new_gameplay=True)
