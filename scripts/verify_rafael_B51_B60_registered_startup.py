"""Reuse exact startup RGB andbind the candidate's own RAM withthe one proved name-field inverse."""
from scripts.verify_registered_rafael_startup_v2 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    'from dk4tool.rom.nds import NdsImage':
        'from dk4tool.rom.nds import NdsImage\nfrom dk4tool.patch.owned_name_fields_v2 import plan_arm9_name_fields',
    "    assert release['all_other_files_components_graphics_names_andruntime_exact_to_parent']":
        "    assert release['all_unowned_files_components_graphics_names_fonts_andruntime_code_exact_to_parent'] and release['only_reviewed_SC0_ten_blocks_andone_owned_name_field_changed']",
    "    unchanged=['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT']":
        """    registry=load('translations/release_stack.json');profile=registry['profiles'][release['profile']]
    field_config=load(profile['owned_Fernan_name_field'])
    expected,field_proof=plan_arm9_name_fields(parent_image.read_file('/__arm9__.bin'),load(field_config['proposal']),NdsImage.open(field_config['clean_ROM']).read_file('/__arm9__.bin'))
    assert image.read_file('/__arm9__.bin')==expected
    assert all(release['Fernan_name_field_proof'][key]==value for key,value in field_proof.items())
    unchanged=['/COMMON/MESFILE.DK4','/GRP/KANJI.FNT']""",
    '        unchanged_runtime_resources=unchanged,ARM9_COMMON_HELP_font_equal_registered_runtime_parent=True,':
        '        unchanged_runtime_resources=unchanged,ARM9_except_one_owned_Fernan_field_COMMON_HELP_font_equal_registered_runtime_parent=True,Fernan_name_field_inverse=field_proof,',
})
exec(compile(source,__file__+'::same-own-Rafael-RAM-and-RGB-one-typed-name-field','exec'),globals())
