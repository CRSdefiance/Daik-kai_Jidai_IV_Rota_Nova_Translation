"""Fresh-check the completed mood batch, preservation and external evidence archive."""
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_mood_comments_completion_v982 import ROOT,ROM,LEDGER,ARCHIVE,GUIDE
from scripts.verify_village_wrap_v608 import read,save

def main():
    target=ROOT/'final_goal_turn_check.json';assert not target.exists()
    ledger=read(LEDGER);release=read('work/analysis/mood_comments_v981/registered_release_verification.json')
    closure=read(ROOT/'registered_release_completion.json');archive=read(ROOT/'archive_manifest.json')
    assert ledger['records_editorially_completed']==1157 and ledger['records_revised_and_integrated']==864
    assert ledger['retained_wordings_editorially_completed']==293 and ledger['records_with_source_and_prose_pass']==1160
    assert sum(ledger['completed_editorial_record_counts_by_file'].values())==1157
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==1160
    before=read(ROOT/'editorial_ledger_before_completion.json')
    for key in ('unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','raw_source_coverage_revisit','approved_name_roles'):
        assert ledger[key]==before[key]
    assert not ledger['full_goal_complete'] and ledger['goal_status']=='active'
    assert read('out/editorial_review_latest.json')==ledger['current_integrated_candidate']
    digest=sha(ROM.read_bytes());assert digest==release['candidate_sha256']==closure['candidate_sha256']
    assert sha(Path(release['exact_clean_input_patch_reconstruction']).read_bytes())==digest
    assert sha(ROM.with_suffix('.xdelta').read_bytes())==release['patch_sha256']
    manifest=read(ROM.with_suffix('.manifest.json'))
    assert manifest['candidate_sha256']==digest and manifest['profile']=='all-routes-unified-v981'
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    for row in archive['files']:
        assert sha(Path(row['archive']).read_bytes())==row['sha256'],row['archive']
    guide=read(GUIDE/'provenance.json');assert len(guide['files'])==6
    for row in guide['files']:
        assert sha(Path(row['source']).read_bytes())==sha(Path(row['guide_candidate']).read_bytes())==row['sha256']
    assert sha(Path('work/clean.nds').read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    assert sha(Path('out/raphael_natural_v2_accepted_base.nds').read_bytes())=='3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    root=Path('work/analysis/mood_comments_v981');block=(root/'builder_added_optional_stage.bin').read_bytes()
    assert Path('scripts/build_integrated_release.py').read_bytes().replace(block,b'',1)==(root/'builder_before.py').read_bytes()
    retention=Path('work/rom_retention/20261021T0056221288766Z.json');plan=read(retention)
    assert len(plan['roms'])==213 and all(r['action']=='keep' for r in plan['roms'])
    assert sha(Path('scripts/prune_generated_roms.ps1').read_bytes())=='aacaca07b50f1bafcfc5bb8579b609b0be2a8e79e3107f336405ba370a435f6f'
    save(target,{'candidate':str(ROM),'candidate_sha256':digest,'patch_sha256':release['patch_sha256'],
        'completed_entries':1157,'revised':864,'retained':293,'source_prose_reviewed':1160,
        'all632_archived_evidence_files_fresh_rehash_pass':len(archive['files'])==632,
        'all6_unmodified_guide_candidate_PNG_hashes_pass':True,
        'clean_canonical_and_prior_builder_bytes_preserved':True,'registered_manifest_patch_and_ledger_agree':True,
        'separate_graphics_names_raw_inventory_and_later_older_reaudit_unchanged':True,
        'retention_preview':str(retention),'retention_keep213_delete0_no_apply':True,
        'actual_folder_inherited_975_suffix_is_a_name_only_all_reports_verify_V981_ROM_hash':True,
        'previous_turn_classification':'progress:current screenshot shop676/677 native layout and full glyph-plane recheck',
        'this_turn_classification':'progress:39 complete reviewed entries,registered V981,exact patch,six actual samples and updated coverage',
        'canonical_not_promoted':True,'full_goal_complete':False,'goal_status':'active',
        'producer_sha256':sha(Path(__file__).read_bytes())})
    supplement=[]
    for source in (target,Path(__file__),retention,ROOT/'archive_manifest.json'):
        dest=ARCHIVE/'final_supplement'/source.absolute().relative_to(Path.cwd())
        dest.parent.mkdir(parents=True,exist_ok=True);assert not dest.exists();copy2(source,dest)
        assert source.read_bytes()==dest.read_bytes()
        supplement.append({'source':str(source),'archive':str(dest),'sha256':sha(dest.read_bytes())})
    save(ROOT/'final_supplement_archive.json',{'files':supplement,'all_hashes_verified':True})
    print('Fresh final check:1157 complete;632 archive files+6 guide PNGs rehashed;ROM/patch/registry/ledger/protected sources exact;goal active.')
    print('ROM SHA256',digest);print('Patch SHA256',release['patch_sha256'])

if __name__=='__main__':main()
