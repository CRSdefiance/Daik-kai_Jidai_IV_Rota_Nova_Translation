"""Own cold boot with exact RGB reuse and a source-qualified name-data-only inverse."""
from pathlib import Path
from dk4tool.patch.owned_name_glyph_v1 import plan_arm9_name_glyph
from scripts.source_locked_derivation_v5118 import checked_text

original=Path('scripts/verify_registered_startup.py')
source=checked_text(original.read_text(encoding='utf-8'),{
    "    assert release['all_other_files_components_graphics_names_andruntime_exact_to_parent']":
        "    assert release['all_unowned_files_components_graphics_names_fonts_andruntime_code_exact_to_parent'] and release['name_metadata_only_change_verified']",
    "    unchanged=['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT']":
    """    registry=load('translations/release_stack.json');profile=registry['profiles'][release['profile']]
    name_config=load(profile['owned_name_glyph'])
    expected,name_proof=plan_arm9_name_glyph(parent_image.read_file('/__arm9__.bin'),load(name_config['proposal']))
    assert image.read_file('/__arm9__.bin')==expected and name_proof==release['name_metadata_proof']
    unchanged=['/COMMON/MESFILE.DK4','/GRP/KANJI.FNT']""",
    '        unchanged_runtime_resources=unchanged,ARM9_COMMON_HELP_font_equal_registered_runtime_parent=True,':
        '        unchanged_runtime_resources=unchanged,ARM9_except_owned_name_slot_COMMON_HELP_font_equal_registered_runtime_parent=True,name_metadata_proof=name_proof,',
})
exec(compile(source,__file__+'::own-coldboot-qualified-name-data','exec'),globals())
