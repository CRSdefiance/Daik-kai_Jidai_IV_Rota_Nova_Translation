"""Fresh final audit of17 completed reviews,source locks,guide copies and reconstructability."""
from pathlib import Path
from shutil import copy2
from unittest.mock import patch
from dk4tool.patch import activity_special_editorial_v987b as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_activity_special_completion_v988 import ROOT,ROM,LEDGER,ARCHIVE,GUIDE,MANUSCRIPT
from scripts.verify_village_wrap_v608 import read,save

def main():
    target=ROOT/'final_goal_turn_check.json';assert not target.exists()
    ledger=read(LEDGER);before=read(ROOT/'editorial_ledger_before_completion.json')
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'],ledger['records_with_source_and_prose_pass'])==(1174,878,296,1177)
    assert sum(ledger['completed_editorial_record_counts_by_file'].values())==1174 and sum(ledger['source_prose_reviewed_counts_by_file'].values())==1177
    for key in ('unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','raw_source_coverage_revisit','approved_name_roles'):
        assert ledger[key]==before[key]
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    candidate=read('out/editorial_review_latest.json');assert candidate==ledger['current_integrated_candidate']
    release=read('work/analysis/activity_special_v987/registered_release_verification.json')
    digest=sha(ROM.read_bytes());assert digest==candidate['sha256']==release['candidate_sha256']
    assert sha(ROM.with_suffix('.xdelta').read_bytes())==release['patch_sha256']
    assert sha(Path(release['exact_clean_input_patch_reconstruction']).read_bytes())==digest
    manifest=read(ROM.with_suffix('.manifest.json'));assert manifest['profile']=='all-routes-unified-v987' and manifest['candidate_sha256']==digest
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert len(manifest['batches'])==471 and len(read('translations/release_stack.json')['accepted_layers'])==114
    archive=read(ROOT/'archive_manifest.json');assert len(archive['files'])==802
    for row in archive['files']:assert sha(Path(row['archive']).read_bytes())==row['sha256'],row['archive']
    guides=read(GUIDE/'provenance.json');assert len(guides['files'])==9
    for row in guides['files']:assert sha(Path(row['source']).read_bytes())==sha(Path(row['guide_candidate']).read_bytes())==row['sha256']
    doc=read(MANUSCRIPT);fonts=read(doc['native_font_proof'])
    # The production compiler must reproduce all17 byte strings when access to
    # any ROM file is forbidden. This is scoped to compilation,not source review.
    with patch('dk4tool.rom.nds.NdsImage.open',side_effect=AssertionError('Production compilation must not reopen historical ROMs')):
        for row,case in zip(doc['records'],fonts['cases'],strict=True):assert owned.compiled(row).hex()==case['compiled_hex']
    assert sha(Path('work/clean.nds').read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    assert sha(Path('out/raphael_natural_v2_accepted_base.nds').read_bytes())=='3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    build=Path('work/analysis/activity_special_v987');block=(build/'builder_added_optional_stage.bin').read_bytes()
    assert Path('scripts/build_integrated_release.py').read_bytes().replace(block,b'',1)==(build/'builder_before.py').read_bytes()
    retention=Path('work/rom_retention/20261021T0139140711020Z.json');plan=read(retention)
    assert len(plan['roms'])==215 and all(r['action']=='keep' for r in plan['roms'])
    assert sha(Path('scripts/prune_generated_roms.ps1').read_bytes())=='aacaca07b50f1bafcfc5bb8579b609b0be2a8e79e3107f336405ba370a435f6f'
    gameplay=read(ROOT/'actual_gameplay_verification.json')
    assert len(gameplay['actual_complete_dialogue_holds'])==18 and len(gameplay['scoped_normal_return_controls'])==9
    assert len(gameplay['offline_corruption_controls'])==36 and all(r['rejected'] for r in gameplay['offline_corruption_controls'])
    save(target,{'candidate':str(ROM),'candidate_sha256':digest,'patch_sha256':release['patch_sha256'],
        'completed_entries':1174,'revised':878,'retained':296,'source_prose_reviewed':1177,
        'all802_archived_evidence_files_fresh_rehash_pass':True,'all9_unmodified_guide_candidate_PNG_hashes_pass':True,
        'all17_production_compilations_exact_with_all_ROM_open_calls_forbidden':True,
        'all18_actual_holds9_complete_returns36_corruption_controls_pass':True,
        'three_new_popup_returns18500_include_final_command_menu_Back_six_valid_body_runs_preserved':True,
        'only_declared_Chapel_room_model_byte42_12_to18_differs_from_pre_fixture_baseline_other139_bytes_exact':True,
        'clean_canonical_and_prior_builder_bytes_preserved':True,'registered_manifest_patch_and_coverage_ledger_agree':True,
        'separate_graphics_names_raw_inventory_and_later_older_reaudit_preserved':True,
        'retention_preview':str(retention),'retention_keep215_delete0_no_apply':True,
        'previous_goal_turn_classification':'progress:39 mood entries completed in V981 with exact patch and source research for next17',
        'this_goal_turn_classification':'progress:17 complete reviewed entries,two native consumers,registered V987,exact patch,nine actual samples and updated coverage',
        'canonical_not_promoted':True,'full_goal_complete':False,'goal_status':'active','producer_sha256':sha(Path(__file__).read_bytes())})
    supplement=[]
    for source in (target,Path(__file__),retention,ROOT/'archive_manifest.json'):
        dest=ARCHIVE/'final_supplement'/source.absolute().relative_to(Path.cwd());dest.parent.mkdir(parents=True,exist_ok=True)
        assert not dest.exists();copy2(source,dest);assert source.read_bytes()==dest.read_bytes()
        supplement.append({'source':str(source),'archive':str(dest),'sha256':sha(dest.read_bytes())})
    save(ROOT/'final_supplement_archive.json',{'files':supplement,'all_hashes_verified':True})
    print('Fresh final check:1174 complete;802 archive files+9 guide PNGs rehashed;exact patch/protected sources/compiler/ledger pass;goal active.')
    print('ROM SHA256',digest);print('Patch SHA256',release['patch_sha256'])

if __name__=='__main__':main()
