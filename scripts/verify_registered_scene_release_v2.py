"""Verify cumulative scenes plus one independently qualified final name-data stage."""
from pathlib import Path
from dk4tool.patch.owned_name_glyph_v1 import plan_arm9_name_glyph
from scripts.source_locked_derivation_v5118 import checked_text

original=Path('scripts/verify_registered_scene_release.py')
source=checked_text(original.read_text(encoding='utf-8'),{
    "    assert manifest['batches'][:-2]==parent_manifest['batches'][:-1]":
        "    assert manifest['batches'][:-3]==parent_manifest['batches'][:-1]",
    "    assert manifest['batches'][-2:]==[str(Path(config['manuscript'])),str(Path(profile['ascii_glyph_right_bounds']))]":
        "    assert manifest['batches'][-3:]==[str(Path(config['manuscript'])),str(Path(profile['ascii_glyph_right_bounds'])),str(Path(profile['owned_name_glyph']))]",
    "    assert len(manifest['batches'])==len(parent_manifest['batches'])+1":
        "    assert len(manifest['batches'])==len(parent_manifest['batches'])+2",
    "    assert changed==[path] and all(candidate.read_file(p)==data for p,data in parent.iter_components())":
    """    assert changed==[path]
    name_config=load(profile['owned_name_glyph'])
    expected_arm,name_proof=plan_arm9_name_glyph(parent.read_file('/__arm9__.bin'),load(name_config['proposal']))
    assert candidate.read_file('/__arm9__.bin')==expected_arm
    changed_components=[p for p,data in parent.iter_components() if candidate.read_file(p)!=data]
    assert changed_components==['/__arm9__.bin']
    assert manifest['checks']['registered_owned_name_metadata_and_complete_parent_target_inverse']
    assert name_config['target_ROM_sha256']==manifest['candidate_sha256']""",
    "        assert added==(Counter(row['id'] for row in approved['records']) if internal==path else Counter())":
    """        expected=Counter(row['id'] for row in approved['records']) if internal==path else Counter()
        if internal=='/__arm9__.bin':expected=Counter(['ACTOR14_SURNAME_NORMAL_ASCII_F'])
        assert added==expected""",
    '        changed_internal_files=changed,changed_blocks={path:changed_blocks},':
        '        changed_internal_files=changed+changed_components,changed_blocks={path:changed_blocks},',
    '        all_other_files_components_graphics_names_andruntime_exact_to_parent=True,':
        '        all_unowned_files_components_graphics_names_fonts_andruntime_code_exact_to_parent=True,name_metadata_only_change_verified=True,name_metadata_proof=name_proof,',
})
exec(compile(source,__file__+'::cumulative-scenes-and-owned-name','exec'),globals())
