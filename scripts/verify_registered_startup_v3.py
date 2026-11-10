"""Own startup with exact RGB reuse andthe qualified exclusive-name-fields inverse."""
from pathlib import Path
from dk4tool.patch.owned_name_fields_v2 import plan_arm9_name_fields
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/verify_registered_startup.py').read_text(encoding='utf-8'),{
    "    assert release['all_other_files_components_graphics_names_andruntime_exact_to_parent']":
    "    assert release['all_unowned_files_components_graphics_names_fonts_andruntime_code_exact_to_parent'] and release['name_metadata_only_change_verified']",
    "    unchanged=['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT']":
    """    registry=load('translations/release_stack.json');profile=registry['profiles'][release['profile']]
    name_config=load(profile['owned_name_fields'])
    expected,name_proof=plan_arm9_name_fields(parent_image.read_file('/__arm9__.bin'),load(name_config['proposal']),NdsImage.open(name_config['clean_ROM']).read_file('/__arm9__.bin'))
    assert image.read_file('/__arm9__.bin')==expected and name_proof==release['name_metadata_proof']
    unchanged=['/COMMON/MESFILE.DK4','/GRP/KANJI.FNT']""",
    '        unchanged_runtime_resources=unchanged,ARM9_COMMON_HELP_font_equal_registered_runtime_parent=True,':
    '        unchanged_runtime_resources=unchanged,ARM9_except_exclusive_name_fields_COMMON_HELP_font_equal_registered_runtime_parent=True,name_metadata_proof=name_proof,',
})
exec(compile(source,__file__+'::own-coldboot-qualified-name-fields','exec'),globals())
