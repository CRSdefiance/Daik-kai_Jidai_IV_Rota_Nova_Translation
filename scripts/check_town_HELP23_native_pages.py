"""Same qualified Help parser/current font on29 new pages;own verified runtime matches planned parent exactly."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/check_early_HELP23_native_pages.py').read_text(encoding='utf-8'),{
    'Shared_HELP_early23_formatting_20261104':'Shared_HELP_T21_T43_formatting_20261104',
    "OUT=ROOT/'native_pages_v2'":"OUT=ROOT/'native_pages_v1'",
    'Rafael_B51_B60_release_verified_20261104':'Rafael_B61_B80_release_verified_20261104',
    "len(plan['pages'])==25 and plan['target_topic_count']==212":"len(plan['pages'])==29 and plan['target_topic_count']==216",
    "    assert ctx.receipt()['candidate_sha256']==plan['current_ROM_sha256']":
        """    from dk4tool.rom.nds import NdsImage
    planned_parent=NdsImage.open(plan['current_ROM']);verified_parent=NdsImage.open(load(RELEASE)['candidate'])
    assert sha(Path(plan['current_ROM']).read_bytes())==plan['current_ROM_sha256']
    assert all(planned_parent.read_file(p)==verified_parent.read_file(p) for p in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT'])
    assert planned_parent.read_file('/__arm9__.bin')==ctx.arm""",
    'len(proofs)==25 and len(sheets)==7':'len(proofs)==29 and len(sheets)==8',
    'native_pages=25,complete_articles=23':'native_pages=29,complete_articles=23',
    '25 native Help pages/23 articles pass;seven readable sheets needdirect view.':'29 native Help pages/23 articles pass;eight readable sheets needdirect view.',
    '        native_archive_loading_complete_widgets_actual_navigation_gameplay_andregistered_integration_pending=True,':
        "        verified_runtime_andplanned_parent_ARM9_COMMON_font_exact=True,planned_parent_ROM=plan['current_ROM'],planned_parent_ROM_sha256=plan['current_ROM_sha256'],\n        native_archive_loading_complete_widgets_actual_navigation_gameplay_andregistered_integration_pending=True,",
})
exec(compile(source,__file__+'::unchanged-complete-source-Help-parser-andfont-guards-29-pages','exec'),globals())
