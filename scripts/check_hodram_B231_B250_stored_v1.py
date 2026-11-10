"""Verify stored ordinary/style/menu bodies and relocated branches in the new scope."""
from scripts import check_editorial_stored_batch_v4 as previous
from scripts.audit_story_glyph_consistency import load
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.refine_hodram_B231_B250_visual_v1 import ROOT
from scripts.source_locked_derivation_v5118 import checked_text

compound_storage=previous.compound_storage
check_FE_rows=previous.check_FE_rows
old_loop="""    full_native=native;seen=set()
    while 'source_owned_target_page_adapter' not in full_native:
        prior=Path(full_native['previous_native']);assert str(prior) not in seen;seen.add(str(prior))
        assert sha(prior.read_bytes())==full_native['previous_native_sha256']
        full_native=load(prior)
        assert full_native['runtime']==native['runtime'] and full_native['font_sha256']==native['font_sha256']"""
source=checked_text(previous.source,{
    "rebuilt['style_physical_speech_count']==8":"rebuilt['style_physical_speech_count']==14",
    "rebuilt['total_rendered_speech_count']==319":"rebuilt['total_rendered_speech_count']==223",
    "rebuilt['typed_choice_count']==10":"rebuilt['typed_choice_count']==2",
    old_loop:"""    adapter_path=ROOT/'native_initial_v1/compiled_native_pages.json'
    assert digest(adapter_path)=='89de39104208d8e5a9f72c5c88ff22b66f5bb655e551b8f81669d4b80141b0cb'
    full_native=load(adapter_path)
    assert full_native['runtime']==native['runtime'] and full_native['font_sha256']==native['font_sha256']""",
    "        print('Stored block',group['block'],'checked',flush=True)":"""        save(args.out/('B'+str(group['block'])+'_checked.json'),dict(
            reconstruction=str(args.reconstruction),reconstruction_sha256=sha(args.reconstruction.read_bytes()),
            native=str(args.native),native_sha256=sha(args.native.read_bytes()),runtime=runtime,
            records=[r for r in rows if r['block']==group['block']],
            relative_cases=[r for r in relatives if r['block']==group['block']],
            typed_objects=[r for r in typed if r['block']==group['block']],
            style_records=[r for r in style_records if r['block']==group['block']],all_checks_through_this_block_pass=True,new_credit=0))
        print('Stored block',group['block'],'checked',flush=True)""",
})
exec(compile(source,__file__+'::same-strict-stored-contract-new-qualified-scope','exec'),globals())
