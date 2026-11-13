"""Bind675's own startup/RAM while preserving separate39-observed/21-offline page provenance."""
from scripts.verify_registered_rafael_startup_v2 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    "release['all_other_files_components_graphics_names_andruntime_exact_to_parent']":
        "release['only_HELP_changed_all_other_files_components_graphics_names_andruntime_exact_to_parent']",
    "if 'HELP' in Path(path).name.upper())":
        "if 'HELP' in Path(path).name.upper() and path!='/COMMON/HELP.DK4')",
    "    assert all(image.read_file(path)==parent_image.read_file(path) for path in unchanged)":
        """    assert all(image.read_file(path)==parent_image.read_file(path) for path in unchanged)
    from dk4tool.formats.ilnk import IlnkContainer
    coverage_path=Path(release['composite_page_coverage']);coverage=load(coverage_path)
    assert sha(coverage_path.read_bytes())==release['composite_page_coverage_sha256']
    assert coverage['candidate_sha256']==release['candidate_sha256']
    assert coverage['every_selected_page_byte_andARM9_COMMON_font_dependency_exact_to_its_own_observed_research_image']
    assert not coverage['all60_observed_on_one_final_ROM']
    assert (coverage['native_andvisually_reviewed_pages'],coverage['observed_pages'],coverage['observed_articles'],coverage['offline_only_pages'])==(60,39,38,21)
    bindings_path=Path(release['exact_record_bindings'])
    assert sha(bindings_path.read_bytes())==release['exact_record_bindings_sha256']
    bindings=load(bindings_path);assert len(bindings['records'])==59 and bindings['candidate_sha256']==release['candidate_sha256']
    resource=image.read_file('/COMMON/HELP.DK4');blocks=IlnkContainer.parse(resource).blocks
    assert sha(resource)==release['target_HELP_sha256']
    for row in bindings['records']:
        for page in row['registered_pages']:
            raw=bytes.fromhex(page['exact_stored_hex']);at=page['archive_offset']
            assert resource[at:at+len(raw)]==blocks[page['block']]==raw
            proof=Path(page['source_page_proof']);assert sha(proof.read_bytes())==page['source_page_proof_sha256']
    assert release['complete_stack_entries']==675 and release['all_eight_registered_final_stages_preserved']""",
    'ARM9_COMMON_HELP_font_equal_registered_runtime_parent=True,':
        'ARM9_COMMON_font_equal_registered_runtime_parent=True,changed_HELP_bound_to60_native_39_observed_21_offline_pages_across_three_proof_groups=True,',
})
exec(compile(source,__file__+'::same-own-Rafael-startup-with-honest-composite-page-provenance','exec'),globals())
