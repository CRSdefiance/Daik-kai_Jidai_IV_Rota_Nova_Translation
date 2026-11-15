"""Bind a source-owned archive rebuild to its unchanged verified native lookup context."""
import argparse
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for key in ['reconstruction','current','out']:p.add_argument('--'+key,type=Path,required=True)
    args=p.parse_args();assert not args.out.exists()
    rebuilt,current=map(load,[args.reconstruction,args.current]);native_path=Path(rebuilt['native']);native=load(native_path)
    assert sha(native_path.read_bytes())==rebuilt['native_sha256'] and native['runtime']==current['runtime']
    runtime=current['runtime'];ctx=RegisteredRuntime(runtime['release_proof'],runtime['startup_proof'],captain=0)
    assert ctx.receipt()==runtime and rebuilt['parent_sha256']==runtime['candidate_sha256']
    research=NdsImage.open(rebuilt['research_ROM']);assert sha(Path(rebuilt['research_ROM']).read_bytes())==rebuilt['research_ROM_sha256']
    assert all(research.read_file(k)==ctx.image.read_file(k) for k in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT'])
    file=current['file_path'];parent=ctx.image.read_file(file);assert sha(parent)==rebuilt['source_archive_sha256']==current['current_archive_sha256']
    blocks=IlnkContainer.parse(parent).blocks
    assert all(sha(blocks[g['block']])==g['current_sha256'] for g in rebuilt['groups'])
    assert all(blocks[g['block']].hex()==g['current_block_hex'] for g in current['groups'])
    save(args.out,dict(current_runtime=runtime,previous_runtime=current['runtime'],
        exact_ARM9_COMMON_font_andcomplete_actor_array=True,owned_source_blocks_exact=True,
        identical_verified_own_snapshot_andactor_array_not_an_historical_overlay=True,
        no_new_native_oractual_gameplay_claim=True,new_credit=0,
        evidence={str(x):sha(x.read_bytes()) for x in [args.reconstruction,args.current,native_path,Path(__file__)]}))
    print('Verified unchanged ARM9/COMMON/font/own actor context andall source-owned parent blocks;no repeated getter characterization.')
