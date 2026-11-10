"""One final files-list commit; whole output must equal the pinned B50 research reference."""
from pathlib import Path
from dk4tool.patch import rafael_B50_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.Rafael_B50_release_paths_v8164 import PARENT,ROM
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B50_atomic_positive_v8169')
if __name__=='__main__':
    assert not ROOT.exists()
    baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');parent=NdsImage.open(PARENT);image=NdsImage.open(PARENT)
    files=image.rom.files;calls=[];commit=owned.commit_files
    def tracked(im,values):
        assert im is image and im.rom.files is files and values is not files
        calls.append(dict(changed_indices=[i for i,(a,b) in enumerate(zip(files,values,strict=True)) if a!=b]))
        return commit(im,values)
    owned.commit_files=tracked
    try:proof=owned.apply_release(image,baseline)
    finally:owned.commit_files=commit
    assert len(calls)==1 and len(calls[0]['changed_indices'])==1 and len(proof['changed_records'])==28
    assert [p for _,p,v in parent.iter_files() if image.read_file(p)!=v]==[owned.PATH]
    assert all(image.read_file(p)==v for p,v in parent.iter_components())
    actual=bytes(image.rom.save());assert actual==ROM.read_bytes()
    ROOT.mkdir(parents=True);save(ROOT/'positive_reconstruction.json',proof)
    save(ROOT/'positive_receipt.json',dict(config=owned.CONFIG,config_sha256=sha(Path(owned.CONFIG).read_bytes()),
        positive_proof=str(ROOT/'positive_reconstruction.json'),positive_proof_sha256=sha((ROOT/'positive_reconstruction.json').read_bytes()),
        parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),reference_ROM=str(ROM),reference_ROM_sha256=sha(actual),
        positive_records=28,one_final_files_list_commit_after_complete_reconstruction=True,
        single_changed_file_indices=calls[0]['changed_indices'],all_other_files_components_exact=True,
        whole_ROM_equals_pinned_research_reference=True,all37_commands_zero_relative_predicate_query_sites_source00_02_09_FA2_FI1_4821_A000_4720_4681_full_end_inverse_exact=True,
        all28_single_pages_two_narrow_warnings18_infos_all28_actual_speeches_preserved=True,
        no_new_output_ROM_orregistry_mutation=True,production_challenges_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()),new_credit=0,full_goal_complete=False))
    print('28-record atomic positive:one final SC0 commit;whole ROM equals approved reference. No output ROM/registry/credit change;negative tests pending.')
