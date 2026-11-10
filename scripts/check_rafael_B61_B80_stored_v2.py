"""Save each completed stored block and avoid an evidence-variable collision."""
from pathlib import Path
from scripts import check_rafael_B61_B80_stored as previous
from scripts.source_locked_derivation_v5118 import checked_text

check_FE_rows=previous.check_FE_rows
progressive_expand=previous.progressive_expand
FE_expand=previous.FE_expand
FRESH=previous.FRESH
OWN=previous.OWN
QUAL=previous.QUAL
PREVIOUS_PRODUCER=Path('scripts/check_rafael_early_tutorial_stored.py')
source=checked_text(previous.source,{
    'Path(previous.__file__)':'PREVIOUS_PRODUCER',
    "        print('Stored block',group['block'],'checked',flush=True)":
        """        save(args.out/('block_'+str(group['block'])+'_complete.json'),dict(
            reconstruction_sha256=sha(args.reconstruction.read_bytes()),native_sha256=sha(args.native.read_bytes()),
            runtime=runtime,block=group['block'],target_sha256=group['target_sha256'],
            records=[r for r in rows if r['block']==group['block']],
            relative_cases=[r for r in relatives if r['block']==group['block']],
            fresh_pages_cumulative=fresh_pages,reused_pages_cumulative=reused_pages,
            all_stored_planes_equal_directly_viewed_compiled_planes=True,
            producer_sha256=sha(Path(__file__).read_bytes()),actual_gameplay=False,new_credit=0))
        print('Stored block',group['block'],'checked andsaved',flush=True)""",
})
exec(compile(source,__file__+'::same-complete-stored-checks-with-per-block-checkpoints','exec'),globals())
