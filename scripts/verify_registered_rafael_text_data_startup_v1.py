"""Reuse exact reviewed startup RGB after the six typed data-only differences."""
from scripts.verify_registered_rafael_startup_v2 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    'from dk4tool.rom.nds import NdsImage':
        'from dk4tool.rom.nds import NdsImage\nfrom dk4tool.patch.registered_reviewed_text_data_v3 import plan_release',
    "    assert release['all_other_files_components_graphics_names_andruntime_exact_to_parent']":
        "    assert release['all_unowned_files_components_graphics_names_fonts_andruntime_code_exact_to_parent'] and release['six_owned_text_data_spans_only']",
    "    unchanged=['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT']":
        """    registry=load('translations/release_stack.json');profile=registry['profiles'][release['profile']]
    expected,data_proof=plan_release(parent_image,profile['owned_reviewed_text_data'])
    assert image.read_file('/__arm9__.bin')==expected and data_proof==release['owned_text_data_proof']
    unchanged=['/COMMON/MESFILE.DK4','/GRP/KANJI.FNT']""",
    '        unchanged_runtime_resources=unchanged,ARM9_COMMON_HELP_font_equal_registered_runtime_parent=True,':
        '        unchanged_runtime_resources=unchanged,ARM9_except_six_owned_text_spans_COMMON_HELP_font_equal_registered_runtime_parent=True,owned_text_data_proof=data_proof,',
})
exec(compile(source, __file__ + '::same-own-Rafael-startup-with-six-typed-text-data-spans', 'exec'), globals())
