"""Fresh original parser/full-font checks on38 pages,with exact registered runtime binding."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/check_early_HELP23_native_pages.py').read_text(encoding='utf-8'),{
 'Shared_HELP_early23_formatting_20261104':'Shared_HELP_T44_T80_formatting_20261104',
 "OUT=ROOT/'native_pages_v2'":"OUT=ROOT/'native_pages_v1'",
 "PLAN=ROOT/'automatic_plans_v1.json'":"PLAN=ROOT/'refined_v2/automatic_plans_v1.json'",
 'Rafael_B51_B60_release_verified_20261104':'Early_HELP23_release_verified_20261104',
 "len(plan['pages'])==25 and plan['target_topic_count']==212":"len(plan['pages'])==38 and plan['target_topic_count']==217",
 "    assert ctx.receipt()['candidate_sha256']==plan['current_ROM_sha256']":
 """    from dk4tool.rom.nds import NdsImage
    planned_parent=NdsImage.open(plan['current_ROM']);verified_parent=NdsImage.open(load(RELEASE)['candidate'])
    assert sha(Path(plan['current_ROM']).read_bytes())==plan['current_ROM_sha256']
    assert all(planned_parent.read_file(p)==verified_parent.read_file(p) for p in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT'])
    assert planned_parent.read_file('/__arm9__.bin')==ctx.arm""",
 'len(proofs)==25 and len(sheets)==7':'len(proofs)==38 and len(sheets)==10',
 'native_pages=25,complete_articles=23':'native_pages=38,complete_articles=37',
 '25 native Help pages/23 articles pass;seven readable sheets needdirect view.':
 '38 native Help pages/37 articles pass;ten readable sheets needdirect view.',
 '        native_archive_loading_complete_widgets_actual_navigation_gameplay_andregistered_integration_pending=True,':
 "        verified_runtime_andplanned_parent_ARM9_COMMON_font_exact=True,planned_parent_ROM=plan['current_ROM'],planned_parent_ROM_sha256=plan['current_ROM_sha256'],\n        native_archive_loading_complete_widgets_actual_navigation_gameplay_andregistered_integration_pending=True,",
})
exec(compile(source,__file__+'::unchanged-native-parser-full-font-instruction-andmemory-guards-38-pages','exec'),globals())
