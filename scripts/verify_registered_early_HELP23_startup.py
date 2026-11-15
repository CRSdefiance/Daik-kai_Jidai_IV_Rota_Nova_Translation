"""Same own Rafael snapshot/code/name checks;qualify changed Help through its separate full actual proof."""
from scripts.verify_registered_rafael_startup_v2 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    "release['all_other_files_components_graphics_names_andruntime_exact_to_parent']":
        "release['only_HELP_changed_all_other_files_components_graphics_names_andruntime_exact_to_parent']",
    "if 'HELP' in Path(path).name.upper())":
        "if 'HELP' in Path(path).name.upper() and path!='/COMMON/HELP.DK4')",
    "    assert all(image.read_file(path)==parent_image.read_file(path) for path in unchanged)":
        """    assert all(image.read_file(path)==parent_image.read_file(path) for path in unchanged)
    actual_help_path=Path(release['actual_help_proof']);actual_help=load(actual_help_path)
    assert sha(actual_help_path.read_bytes())==release['actual_help_proof_sha256']
    assert actual_help['all25_complete_actual_pages_andnative_child_targets_pass']
    help_image=NdsImage.open(actual_help['research_ROM'])
    assert sha(Path(actual_help['research_ROM']).read_bytes())==actual_help['research_ROM_sha256']
    assert image.read_file('/COMMON/HELP.DK4')==help_image.read_file('/COMMON/HELP.DK4')
    assert sha(image.read_file('/COMMON/HELP.DK4'))==release['target_HELP_sha256']""",
    'ARM9_COMMON_HELP_font_equal_registered_runtime_parent=True,':
        'ARM9_COMMON_font_equal_registered_runtime_parent=True,changed_HELP_exact_to_separately_observed25_pages=True,',
})
exec(compile(source,__file__+'::same-own-snapshot-with-separate-changed-Help-actual-qualification','exec'),globals())
