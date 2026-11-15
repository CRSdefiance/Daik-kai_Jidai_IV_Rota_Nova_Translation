"""Capture prose with the bounded exact-caller runtime repair;research only."""
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.rom.nds import NdsImage
from scripts import enemy_capture_native_plan_v1415 as prose
from scripts import enemy_capture_runtime_v1417b as runtime
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/enemy_capture_payload_v1419')
MANUSCRIPT = prose.MANUSCRIPT
IDS,PROFILE,SOURCE_COMMON,SOURCE_ARM = prose.IDS,prose.PROFILE,prose.SOURCE_COMMON,prose.SOURCE_ARM
compiled = prose.compiled

def plan(common,arm,doc):
    c,a,proof = prose.plan(common,arm,doc)
    runtime_arm,runtime_plan = runtime.apply(arm)
    target = bytearray(a)
    for patch in runtime_plan['patches']:
        at = patch['address']-runtime.BASE
        source,value = bytes.fromhex(patch['source_hex']),bytes.fromhex(patch['target_hex'])
        assert target[at:at+len(source)]==source
        target[at:at+len(value)] = value
    target = bytes(target)
    patches = runtime_plan['patches']+proof['patches']
    restored = bytearray(target)
    for patch in patches:
        at = patch['address']-runtime.BASE
        value = bytes.fromhex(patch['source_hex'])
        restored[at:at+len(value)] = value
    assert bytes(restored)==arm
    old,new = [MainCodeFile(v,runtime.BASE) for v in [arm,target]]
    shape = lambda obj:[(s.ramAddress,len(s.data),s.bssSize) for s in obj.sections]
    assert shape(old)==shape(new) and cache_plan(arm)==cache_plan(target)
    assert all(old.sections[i].data==new.sections[i].data for i in [1,2,3,4])
    assert len(new.sections[3].data)-48==123040
    del proof['entire188_byte_selector_172_byte_gate_and_all_code_fonts_sections_BSS_cache_arena_ITCM_staged123040_exact']
    del proof['only_COMMON22_and_original_native_offset_directory_data_changed']
    del proof['original_direct_consumer_no_authored_alignment_or_new_formatter_membership']
    proof.update(target_ARM9_sha256=sha(target),patches=patches,runtime_plan=runtime_plan,
        only_COMMON22_native_metadata_and_owned188_byte_table172_byte_gate_changed=True,
        all_other_code_fonts_sections_BSS_cache_arena_ITCM_and123040_staged_bytes_exact=True,
        exactly_one_proven_capture_membership_added_no_allocation_growth=True)
    return c,target,proof

if __name__=='__main__':
    assert not ROOT.exists()
    doc = read(MANUSCRIPT)
    rom = NdsImage.open(doc['current_ROM'])
    c,a,proof = plan(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),doc)
    ROOT.mkdir(parents=True)
    cp,ap = ROOT/'COMMON_RESEARCH_ONLY.DK4',ROOT/'ARM9_PAYLOAD_RESEARCH_ONLY.bin'
    cp.write_bytes(c);ap.write_bytes(a)
    save(ROOT/'native_payload_plan.json',{**proof,'target_COMMON':str(cp),'target_ARM9':str(ap),
        'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'producer_sha256':sha(Path(__file__).read_bytes()),'no_ROM_registry_or_completion_change':True,'full_goal_complete':False})
    print('Research capture payload includes one exact scoped caller;188/172 owned bytes and123040 staged bytes retained.',flush=True)
