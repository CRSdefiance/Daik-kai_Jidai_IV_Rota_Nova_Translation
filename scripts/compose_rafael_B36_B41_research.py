"""Compose already tested blocks only after the tutorial successor is verified."""
import argparse
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime

BLOCKS=Path('work/analysis/Rafael_B36_B41_stored_blocks_20261104/block_reconstruction.json')
STORED=Path('work/analysis/Rafael_B36_B41_stored_native_20261104/stored_native_verification.json')
LOOKUP=Path('work/analysis/Rafael_B36_B41_stored_catalogue_20261104/all175_stored_effective_body_bindings.json')

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    for key in ('parent-release','parent-startup','out'):
        ap.add_argument('--'+key,type=Path,required=True)
    args=ap.parse_args()
    assert not args.out.exists()
    ctx=RegisteredRuntime(args.parent_release,args.parent_startup,captain=0)
    assert ctx.release['profile']=='all-routes-rafael-early-tutorial-static-text-20261104'
    assert ctx.release['candidate_sha256']=='c555f555a0e6a15b35e10a27b87ac98ed17601ba814cfeb9ba3d98dcc87344a8'
    assert ctx.release['complete_stack_entries']==665 and ctx.release['accepted_layers']==114
    rebuilt,stored,lookup=map(load,[BLOCKS,STORED,LOOKUP])
    assert stored['reconstruction_sha256']==sha(BLOCKS.read_bytes())
    assert stored['complete_stored_pages']==177 and lookup['stored_sha256']==sha(STORED.read_bytes())
    assert len(lookup['records'])==rebuilt['speech_count']==175
    old=RegisteredRuntime(stored['runtime']['release_proof'],stored['runtime']['startup_proof'],captain=0)
    assert old.receipt()==stored['runtime']==lookup['runtime']
    assert ctx.arm==old.arm and ctx.common==old.common and ctx.actor_bytes==old.actor_bytes
    assert ctx.image.read_file('/GRP/KANJI.FNT')==old.image.read_file('/GRP/KANJI.FNT')
    assert sha(Path(rebuilt['parent']).read_bytes())==rebuilt['parent_sha256']==old.release['candidate_sha256']
    doc=load(rebuilt['manuscript']);path=doc['file_path']
    archive=ctx.image.read_file(path);container=IlnkContainer.parse(archive)
    previous=IlnkContainer.parse(old.image.read_file(path))
    assert len(container.blocks)==len(previous.blocks)==343
    assert [n for n,(a,b) in enumerate(zip(previous.blocks,container.blocks,strict=True)) if a!=b]==[42,43]
    blocks=list(container.blocks)
    for group in rebuilt['groups']:
        number=group['block'];target=Path(group['target_block']).read_bytes()
        assert blocks[number]==previous.blocks[number] and sha(blocks[number])==group['current_sha256']
        assert sha(target)==group['target_sha256']
        blocks[number]=target
    result=IlnkContainer(blocks).to_bytes();parsed=IlnkContainer.parse(result)
    assert [n for n,(a,b) in enumerate(zip(container.blocks,parsed.blocks,strict=True)) if a!=b]==list(range(36,42))
    assert parsed.blocks[42:44]==container.blocks[42:44]
    inverse=list(parsed.blocks)
    for number in range(36,42):inverse[number]=container.blocks[number]
    assert IlnkContainer(inverse).to_bytes()==archive
    planned=deepcopy(ctx.image);planned.replace_file(path,result)
    assert [p for _,p,data in ctx.image.iter_files() if planned.read_file(p)!=data]==[path]
    assert all(planned.read_file(p)==data for p,data in ctx.image.iter_components())
    restored=deepcopy(planned);restored.replace_file(path,archive)
    assert bytes(restored.rom.save())==Path(ctx.rompath).read_bytes()
    args.out.mkdir(parents=True)
    archive_path=args.out/'reviewed_RESEARCH_ONLY.DK4';archive_path.write_bytes(result)
    research=args.out/'reviewed_RESEARCH_ONLY.nds';planned.save(research)
    reopened=NdsImage.open(research)
    assert reopened.read_file(path)==result and reopened.read_file('/__arm9__.bin')==ctx.arm
    save(args.out/'reconstruction.json',dict(**{k:rebuilt[k] for k in ['manuscript','manuscript_sha256','plan','plan_sha256','packet','packet_sha256','native','native_sha256','groups','command_count','speech_count','relative_sites']},
        parent=str(ctx.rompath),parent_sha256=ctx.release['candidate_sha256'],source_archive_sha256=sha(archive),
        target_archive=str(archive_path),target_archive_sha256=sha(result),research_ROM=str(research),research_ROM_sha256=sha(research.read_bytes()),
        unchanged_blocks=337,all_other_files_components_exact=True,full_clean_current_block_archive_andserialized_NDS_inverses_exact=True,
        all_prior_tutorial_changes_preserved=True,registered_right_bound_runtime_preserved=True,
        old_block_reconstruction=str(BLOCKS),old_block_reconstruction_sha256=sha(BLOCKS.read_bytes()),
        old_stored_native=str(STORED),old_stored_native_sha256=sha(STORED.read_bytes()),
        old_stored_catalogue_lookup=str(LOOKUP),old_stored_catalogue_lookup_sha256=sha(LOOKUP.read_bytes()),
        unchanged_complete_ARM9_COMMON_font_actor_bytes_andall_six_source_blocks=True,
        stored_native_plane_andbranch_proofs_reused_on_exact_dependency_match=True,
        current_own_Rafael_runtime=ctx.receipt(),new_native_calls_claimed=0,
        actual_headers_transitions_archive_loaders_andregistered_release_pending=True,
        catalogue_name_changes_not_applied=True,new_credit=0,guide_photos=False,
        evidence={str(p):sha(p.read_bytes()) for p in [BLOCKS,STORED,LOOKUP,args.parent_release,args.parent_startup,Path(__file__)]}))
    print('Six tested blocks composed on verified tutorial successor;complete archive/ROM inverses pass;research only.')

if __name__=='__main__':main()
