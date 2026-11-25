"""Bind 678's own RAM/RGB to the verified composite Help and Rafael release."""
from scripts.verify_registered_rafael_startup_v2 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    "release['all_other_files_components_graphics_names_andruntime_exact_to_parent']":
        "release['only_HELP_andSC0_B81_B84_changed_all_other_files_components_graphics_names_andruntime_exact_to_parent']",
    "if 'HELP' in Path(path).name.upper())":
        "if 'HELP' in Path(path).name.upper() and path!='/COMMON/HELP.DK4')",
    "    assert all(image.read_file(path)==parent_image.read_file(path) for path in unchanged)":
        """    assert all(image.read_file(path)==parent_image.read_file(path) for path in unchanged)
    from dk4tool.formats.ilnk import IlnkContainer
    coverage_path=Path(release['composite_page_coverage'])
    assert sha(coverage_path.read_bytes())==release['composite_page_coverage_sha256']
    coverage=load(coverage_path)
    assert coverage['candidate_sha256']==release['candidate_sha256']
    assert coverage['exact_dependency_qualified_existing_native_visual_andactual_evidence_reused']
    assert not coverage['all_content_observed_on_one_final_ROM']
    assert coverage['help']==dict(native_pages=103,observed_pages=56,offline_only_pages=47,observed_articles=51)
    assert coverage['story']['native_commands']==327 and coverage['story']['observed_source_speeches']==75
    bindings_path=Path(release['exact_record_bindings'])
    assert sha(bindings_path.read_bytes())==release['exact_record_bindings_sha256']
    bindings=load(bindings_path)
    assert len(bindings['records'])==428 and bindings['candidate_sha256']==release['candidate_sha256']
    helpraw=image.read_file('/COMMON/HELP.DK4');helpblocks=IlnkContainer.parse(helpraw).blocks
    storyraw=image.read_file('/data/SC0.DK4');storyblocks=IlnkContainer.parse(storyraw).blocks
    assert sha(helpraw)==release['target_HELP_sha256'] and sha(storyraw)==release['target_SC0_sha256']
    oldblocks=IlnkContainer.parse(parent_image.read_file('/data/SC0.DK4')).blocks
    assert len(oldblocks)==len(storyblocks)==343
    assert [i for i,(a,b) in enumerate(zip(oldblocks,storyblocks,strict=True)) if a!=b]==[81,82,83,84]
    assert storyblocks[44]==oldblocks[44]
    for row in bindings['records']:
        if row['file_path']=='/COMMON/HELP.DK4':
            for page in row['registered_pages']:
                raw=bytes.fromhex(page['exact_stored_hex']);at=page['archive_offset']
                assert helpraw[at:at+len(raw)]==helpblocks[page['block']]==raw
                proof=Path(page['source_page_proof'])
                assert sha(proof.read_bytes())==page['source_page_proof_sha256']
        else:
            ref=row['registered_reference'];raw=bytes.fromhex(ref['exact_stored_hex']);at=ref['offset']
            assert storyblocks[row['block']][at:at+len(raw)+1]==raw+b'\\0'
    assert release['complete_stack_entries']==678 and release['all_eight_registered_final_stages_preserved']""",
    'ARM9_COMMON_HELP_font_equal_registered_runtime_parent=True,':
        'ARM9_COMMON_font_equal_registered_runtime_parent=True,changed_HELP_andSC0_exact_composite_refs_bound=True,',
})
exec(compile(source, __file__+'::same-own-Rafael-startup-with-exact-composite-resources', 'exec'), globals())
