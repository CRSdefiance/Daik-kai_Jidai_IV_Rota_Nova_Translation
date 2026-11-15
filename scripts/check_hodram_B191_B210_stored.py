"""Use strict stored glyph/FE/relative checks and preserve completed block receipts."""
from scripts import check_editorial_stored_batch_v4 as previous
from scripts.source_locked_derivation_v5118 import checked_text

compound_storage = previous.compound_storage
check_FE_rows = previous.check_FE_rows
source = checked_text(previous.source, {
    "rebuilt['style_physical_speech_count']==8": "rebuilt['style_physical_speech_count']==0",
    "rebuilt['total_rendered_speech_count']==319": "rebuilt['total_rendered_speech_count']==352",
    "rebuilt['typed_choice_count']==10": "rebuilt['typed_choice_count']==21",
    "        print('Stored block',group['block'],'checked',flush=True)":
        """        save(args.out/('B'+str(group['block'])+'_checked.json'),dict(
            reconstruction=str(args.reconstruction),reconstruction_sha256=sha(args.reconstruction.read_bytes()),
            native=str(args.native),native_sha256=sha(args.native.read_bytes()),runtime=runtime,
            records=[r for r in rows if r['block']==group['block']],
            relative_cases=[r for r in relatives if r['block']==group['block']],
            typed_objects=[r for r in typed if r['block']==group['block']],all_checks_through_this_block_pass=True,new_credit=0))
        print('Stored block',group['block'],'checked',flush=True)""",
})
exec(compile(source, __file__ + '::same-strict-stored-consumers-mixed-menu-scope', 'exec'), globals())
