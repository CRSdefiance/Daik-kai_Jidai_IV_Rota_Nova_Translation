"""Prepare an exact two-patch ARM9 research image; never write a playable ROM."""

from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch import recruitment_editorial_runtime as current
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.rom.nds import NdsImage
from scripts.research_scheme_selector_v775 import ROOT,assemble
from scripts.verify_village_wrap_v608 import read,save


def main():
    rom_path=Path('out/all_routes_combined_v773_candidate.nds')
    assert sha(rom_path.read_bytes())=='4b799e769123620bd4574b2dd6fc10ea38ce87d3d28ebc797a78349b1897415b'
    arm=NdsImage.open(rom_path).read_file('/__arm9__.bin')
    code=MainCodeFile(arm,current.BASE)
    assert bytes(code.save())==arm
    original=current.assemble()
    table,gate,_=assemble()
    before=[bytes(s.data) for s in code.sections]
    patches=[]
    for at,blob in ((current.CONTRACTS,table),(current.GATE,gate)):
        assert len(blob)<=len(original[at])
        off=at-code.sections[0].ramAddress
        assert before[0][off:off+len(original[at])]==original[at]
        patches.append({'address':at,'source_hex':before[0][off:off+len(blob)].hex(),
                        'target_hex':blob.hex(),'existing_owned_capacity':len(original[at]),'bytes':len(blob)})
        code.sections[0].data[off:off+len(blob)]=blob
    target=bytes(code.save())
    result=MainCodeFile(target,current.BASE)
    assert len(target)==len(arm) and cache_plan(target)==cache_plan(arm)
    assert [(s.ramAddress,len(s.data),s.bssSize) for s in result.sections]==[(s.ramAddress,len(s.data),s.bssSize) for s in code.sections]
    assert all(bytes(result.sections[n].data)==before[n] for n in range(1,len(before)))
    restored=bytearray(result.sections[0].data)
    for p in patches:
        off=p['address']-current.BASE
        restored[off:off+p['bytes']]=bytes.fromhex(p['source_hex'])
    assert bytes(restored)==before[0]
    for at,n in ((current.STATUS_CONSTANTS,24),(current.PACKED_PHRASES,24),
                 (current.DATA_ADDRESSES[7],13)):
        assert target[at-current.BASE:at-current.BASE+n]==arm[at-current.BASE:at-current.BASE+n]
    (ROOT/'ARM9_RESEARCH_ONLY.bin').write_bytes(target)
    scope=read(ROOT/'scope_proof.json')
    assert scope['cases']==34343 and scope['native_production_addresses_in_CPU_only']
    save(ROOT/'two_patch_plan.json',{'source_ROM_sha256':sha(rom_path.read_bytes()),
        'source_ARM9_sha256':sha(arm),'target_ARM9_sha256':sha(target),'patches':patches,
        'all_section_BSS_cache_and_staged_payload_geometry_exact':True,
        'all_other_ARM9_bytes_and_original_status_tables_exact':True,
        'prior_private_runtime_module_sha256':sha(Path(current.__file__).read_bytes()),
        'prior_ownership_proof':'work/analysis/recruitment_owned_v772/owned_runtime_plan.json',
        'prior_ownership_proof_sha256':sha(Path('work/analysis/recruitment_owned_v772/owned_runtime_plan.json').read_bytes()),
        'native_scope_proof_sha256':sha((ROOT/'scope_proof.json').read_bytes()),
        'revalidation_of_current_references_and_registered_integration_pending':True,
        'no_playable_ROM_or_completion_claim':True,'full_goal_complete':False,
        'producer_sha256':sha(Path(__file__).read_bytes())})
    print('Two exact research patches fit existing banks;all other ARM9 bytes and memory geometry preserved. No playable ROM.',flush=True)


if __name__=='__main__':main()
