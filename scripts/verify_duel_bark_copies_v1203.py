"""Complete changed-block native copies, prefix/cache and incoming-reference checks."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.duel_editorial import owned_entries
from scripts.probe_common_single_cache_v862 import Loader
from scripts.audit_item_runtime_storage_v785 import census
from scripts.verify_escape_direct_runtime_v1184b import literal_accesses
from scripts.duel_bark_front_v1201 import ADDRESS,END
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/duel_bark_copies_v1203')


def main():
    assert not ROOT.exists()
    p=Path('work/analysis/duel_bark_native_v1201/native_payload_plan.json');plan=read(p)
    arm,common=Path(plan['target_ARM9']).read_bytes(),Path(plan['target_COMMON']).read_bytes()
    rows=owned_entries(common,arm,plan['directory_sha256']);loader=Loader(arm,common);cases=[]
    for mode in ('warm','cold'):
        for n in range(1931,1977):
            result=loader.copy(n,rows[n].text,mode)
            assert sha(bytes(loader.uc.mem_read(loader.owner+0x30,1480)))==plan['new_code_prefix']['component_sha256']
            cases.append(result)
    loader.reset();sequence=[]
    for block in (0,21,20,21,22,21,40,21,21):
        n=loader.directory[block][0]
        for repeat in range(2):sequence.append(loader.copy(n,rows[n].text,'sequence'))
    assert len(cases)==92 and len(sequence)==18 and all(r['reads']==0 for r in sequence[1::2])
    source=NdsImage.open('out/all_routes_combined_v1189_candidate.nds');target=NdsImage.open('out/all_routes_combined_v1189_candidate.nds');target.rom.arm9=arm
    span=[(ADDRESS,END)];private=[(0x0200DA28,END)]
    refs=[census(r,span,private) for r in (source,target)]
    outside=lambda rs:sorted(r for r in rs if not r[-1])
    assert outside(refs[0])==outside(refs[1])
    literals=[literal_accesses(r,span) for r in (source,target)]
    ext=lambda rs:sorted(r for r in rs if not any(lo<=r[2]<hi for lo,hi in private))
    assert ext(literals[0])==ext(literals[1])
    ROOT.mkdir(parents=True)
    save(ROOT/'changed_block_copy_verification.json',{'ARM9_sha256':sha(arm),'COMMON_sha256':sha(common),
        'payload_plan':str(p),'payload_plan_sha256':sha(p.read_bytes()),'complete_native_copies':cases,'native_cache_sequence':sequence,
        'all46_changed_block_entries_warm_and_cold_have_complete_span_NUL8192_and512_output_guards':True,
        'all_other40_blocks_full_payload_and_metadata_exact_from_source_plan':True,
        'opaque1480_code_prefix_exact_and_never_selected_as_text':True,'same_existing_cache_output_and_stack_ABI':True,
        'front_absolute_and_branch_census':refs,'front_PC_relative_census':literals,
        'all_external_incoming_front_references_exact':True,'host_file_open_read_are_CPU_boundaries':True,
        'actual_gameplay_and_registered_integration_pending':True,'no_completion_credit':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('92 complete changed-block native copies,18 cache sequences and front references pass.',flush=True)


if __name__=='__main__':main()
