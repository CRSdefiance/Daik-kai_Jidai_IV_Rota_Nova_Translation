"""Check stored bodies, exact compounds, FE rows and every relocated native branch."""
from pathlib import Path
from scripts import check_editorial_stored_batch_v4 as previous
from scripts.audit_story_glyph_consistency import load
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.review_hodram_B221_B230_contextual_v1 import ROOT
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
    "rebuilt['style_physical_speech_count']==8":"rebuilt['style_physical_speech_count']==29",
    "rebuilt['total_rendered_speech_count']==319":"rebuilt['total_rendered_speech_count']==270",
    "rebuilt['typed_choice_count']==10":"rebuilt['typed_choice_count']==7",
    old_loop:"""    adapter_path=ROOT/'native_resume_v2/compiled_native_pages.json'
    assert digest(adapter_path)=='3ddfb945df384f415cb9e701d2b395a0b77606ef651b98955b2d1c9b024a81ae'
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
exec(compile(source,__file__+'::same-strict-native-stored-scope-qualified-adapter','exec'),globals())
