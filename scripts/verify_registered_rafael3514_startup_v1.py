"""Verify the registered candidate's own startup with the exclusive field applied."""
from pathlib import Path

from dk4tool.patch.owned_name_fields_v2 import plan_arm9_name_fields
from scripts.prepare_rafael3514_Francisca_field_v1 import CLEAN, CONFIG
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_registered_rafael_startup_v2 import source as previous


source = checked_text(previous, {
    "    assert release['parent_sha256']==parent['candidate_sha256']\n    assert release['all_other_files_components_graphics_names_andruntime_exact_to_parent']":
        """    assert release['all_preceding_eight_stages_and_exclusive_field_preserved']
    cfg = load(CONFIG)
    proposal = load(cfg['proposal'])
    assert parent['candidate_sha256'] == proposal['runtime']['candidate_sha256']""",
    "    unchanged=['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT']":
        """    assert sha(Path(parent['candidate']).read_bytes()) == parent['candidate_sha256']
    expected, ownership = plan_arm9_name_fields(parent_image.read_file('/__arm9__.bin'),
        proposal, NdsImage.open(CLEAN).read_file('/__arm9__.bin'))
    assert image.read_file('/__arm9__.bin') == expected and sha(expected) == cfg['target_ARM9_sha256']
    assert ownership['all_unowned_ARM9_bytes_sections_pointer_tables_andallocations_exact']
    unchanged=['/COMMON/MESFILE.DK4','/GRP/KANJI.FNT']""",
    'ARM9_COMMON_HELP_font_equal_registered_runtime_parent=True':
        'COMMON_HELP_font_equal_registered_runtime_parent=True,only_owned_Francisca_field_differs_in_ARM9=True',
    "    release['own_registered_startup_pending']=False":
        "    release['own_registered_startup_pending']=False\n    release['registered_own_startup_pending']=False",
})


if __name__ == '__main__':
    exec(compile(source, __file__+'::same-own-startup-proof-with-exact-field-inverse', 'exec'), globals())
