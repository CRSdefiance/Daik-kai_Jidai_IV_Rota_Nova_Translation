"""Own coldboot with unchanged RGB/consumer code and source-qualified static-data inverse."""
from pathlib import Path
from dk4tool.patch.hodram_static_labels_v1 import plan_static_labels
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/verify_registered_startup.py').read_text(encoding='utf-8'), {
    "    assert release['all_other_files_components_graphics_names_andruntime_exact_to_parent']":
        "    assert release['all_unowned_files_components_graphics_names_fonts_andruntime_code_exact_to_parent'] and release['static_data_only_change_verified']",
    "    unchanged=['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT']":
    """    registry=load('translations/release_stack.json');profile=registry['profiles'][release['profile']]
    static_config=load(profile['owned_static_text'])
    expected,static_proof=plan_static_labels(parent_image.read_file('/__arm9__.bin'),load(static_config['proposal']),NdsImage.open(static_config['clean_ROM']).read_file('/__arm9__.bin'))
    assert image.read_file('/__arm9__.bin')==expected and static_proof==release['static_data_proof']
    unchanged=['/COMMON/MESFILE.DK4','/GRP/KANJI.FNT']""",
    "    snapshot=next(p for p in capture['read_only_capture_RAM_snapshots'] if p['frame']==4000)":
        "    assert capture['read_only_RAM_snapshot']['read_only_export']\n    snapshot={**capture['read_only_RAM_snapshot'],'frame':capture['frames'],'source_report_key':'read_only_RAM_snapshot','recorded_after_final_frame_no_historical_overlay':True}",
    '        unchanged_runtime_resources=unchanged,ARM9_COMMON_HELP_font_equal_registered_runtime_parent=True,':
        '        unchanged_runtime_resources=unchanged,ARM9_except_source_qualified_static_labels_COMMON_HELP_font_equal_registered_runtime_parent=True,static_data_proof=static_proof,',
})
exec(compile(source, __file__ + '::own-4001-final-snapshot-static-data-and-all-original-startup-checks', 'exec'), globals())
