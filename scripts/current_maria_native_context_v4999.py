"""Bound native CPU research to a real snapshot from the exact current ROM.

No historical initialized RAM or immutable-span overlay is used. Native file
open/read are host contracts; machine setup resets the existing COMMON cache
descriptors. Every executed instruction must match the current decoded sections
or the exact current123040-byte deployed pool. This is not new gameplay.
"""
from pathlib import Path
from types import FunctionType,SimpleNamespace
from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_escape_direct_source_v1186 import machine
from scripts.probe_battle_aftermath_fonts_v1256 import consumer
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_village_wrap_v608 import read,save

BASE=0x02000000
POOL=0x02387A20


class CurrentContext:
    def __init__(self,manuscript,historical_rom,root):
        self.doc=read(manuscript);self.rompath=Path(self.doc['current_ROM']);self.rom=NdsImage.open(self.rompath)
        context=read(self.doc['native_context_proof']);report_path=Path(context['capture_report']);report=read(report_path)
        assert sha(report_path.read_bytes())==context['capture_report_sha256']
        assert report['ROM_sha256']==self.doc['current_ROM_sha256']==sha(self.rompath.read_bytes())
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        battery=report['battery_save_preloaded']
        assert battery['copied_byte_exact_before_cold_boot'] and not battery['savestate_loaded']
        assert battery['source_sha256']==sha(Path(battery['source']).read_bytes())=='295631dc76ae7b8c10b99a62dcbdbba815400a9463fc24df55e61abbf220d949'
        fp=Path(context['existing_system_unlock_manifest']);fixture=read(fp)
        assert sha(fp.read_bytes())==context['existing_system_unlock_manifest_sha256']
        assert fixture['only_system_low_four_bits_and_original_checksum_changed'] and fixture['all_six_route_save_slots_and_footer_unchanged'] and not fixture['earned_unlock_verified']
        assert report['synthetic_gallery_fixtures']==[dict(preloaded_save_manifest=str(fp),manifest_sha256=sha(fp.read_bytes()),synthetic_gallery_fixture=True,earned_unlock_verified=False,validated_selected_supported_site_ids=None)]
        assert not any(v for k,v in report.items() if k.startswith('synthetic_') and k!='synthetic_gallery_fixtures')
        snap=next(r for r in report['read_only_capture_RAM_snapshots'] if r['frame']==context['frame'])
        self.raw=Path(snap['path']).read_bytes()
        assert snap['read_only_export'] and len(self.raw)==0x400000 and sha(self.raw)==snap['sha256']==context['snapshot_sha256']
        self.arm,self.common=self.rom.read_file('/__arm9__.bin'),self.rom.read_file('/COMMON/MESFILE.DK4')
        assert sha(self.arm)==self.doc['current_ARM9_sha256'] and sha(self.common)==self.doc['current_COMMON_sha256']
        self.entries=owned_entries(self.common,self.arm,context['directory_sha256'])
        sections=MainCodeFile(self.arm,BASE).sections;payload=bytes(sections[3].data[:-48])
        assert len(payload)==123040 and self.raw[POOL-BASE:POOL-BASE+123040]==payload
        self.sections=[*sections,SimpleNamespace(ramAddress=POOL,data=payload)]
        self.plan=dict(patches=[]);self.machines=[]
        cpu,get,_=machine(self.arm,self.common,self.raw,self.plan)
        self.actor_root=get(0xCB184)
        assert get(0x7F244)==3
        class FontROM:
            @staticmethod
            def open(path):
                assert str(path)=='out/all_routes_combined_v255_candidate.nds'
                return self.rom
        self.raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':FontROM},argdefs=original_raster.__defaults__)
        root=Path(root);assert not root.exists();root.mkdir(parents=True)
        self.proof_path=root/'current_native_pipeline_plan.json'
        save(self.proof_path,dict(candidate=str(self.rompath),candidate_sha256=self.doc['current_ROM_sha256'],
            ARM9_sha256=sha(self.arm),COMMON_sha256=sha(self.common),capture_report=str(report_path),
            capture_report_sha256=sha(report_path.read_bytes()),actual_snapshot=snap,
            original_current123040_deployed_payload_exact=True,patches=[],no_initialized_RAM_overlay=True,
            legacy_historical_ROM_argument_ignored_and_never_read=str(historical_rom),
            snapshot_is_current_Maria_opening_not_B97_activation=True,
            machine_setup_resets_COMMON_owner_plus8_word_and_plus2C_byte=True,
            native_file_open_read_operations_are_explicit_host_contracts=True,
            helper_sha256=sha(Path(__file__).read_bytes()),new_emulator_runs=0,full_goal_complete=False))

    def machine(self,a,c,r,p):
        assert a==self.arm and c==self.common and r==self.raw and p==self.plan
        cpu,get,provider=machine(a,c,r,p)
        assert get(0xCB184)==self.actor_root
        before=bytes(cpu.mem_read(self.actor_root,0x1A04));executed=set()
        def exact(u,pc,size,unused):
            matches=[s for s in self.sections if s.ramAddress<=pc and pc+size<=s.ramAddress+len(s.data)]
            assert len(matches)==1,('executed outside current source sections',hex(pc),size)
            section=matches[0];at=pc-section.ramAddress
            assert bytes(u.mem_read(pc,size))==bytes(section.data[at:at+size]),('executed noncurrent instruction',hex(pc))
            executed.add(pc)
        cpu.hook_add(UC_HOOK_CODE,exact)
        provider.executed_current=executed;self.machines.append((cpu,before))
        return cpu,get,provider

    def execute(self,fn,*args,raw=None):
        assert raw is None or raw==self.raw
        bound=FunctionType(fn.__code__,{**fn.__globals__,'machine':self.machine,'portrait_machine':self.machine},argdefs=fn.__defaults__)
        result=bound(self.arm,self.common,self.raw,self.plan,*args)
        cpu,before=self.machines[-1];assert bytes(cpu.mem_read(self.actor_root,0x1A04))==before
        return result

    def speak(self,entry,actor_or_role,table,argument=None,raw=None):
        return self.execute(consumer,entry,actor_or_role,table,argument,raw=raw)
