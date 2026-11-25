"""Package the cumulative clean-input patch and exact build proofs for GitHub testing."""
import ast
import gzip
import xml.etree.ElementTree as ET
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/maria359_B253_B274_release_v1')
EDITORIAL=Path('work/Maria_B253_B274_clean_20261110')
OUT=Path('releases/all_routes_editorial_20261110_maria359_candidate')

def main():
    assert not OUT.exists()
    release=load(ROOT/'registered_release_verification.json');complete=load(ROOT/'completion_checkpoint.json')
    assert (release['registered_manifest_entries'],release['accepted_layers'],release['passing_release_checks'])==(723,114,58)
    assert complete['counts']==dict(completed=23429,revised=13997,retained=9432)
    assert not release['own_registered_startup_pending'] and release['clean_input_patch_byte_exact']
    assert digest('translations/release_stack.json')==release['registry_sha256']
    for key in ['candidate','manifest','patch']:assert digest(release[key])==release[key+'_sha256']
    assert Path(release['candidate']).read_bytes()==Path(release['exact_clean_reconstruction']).read_bytes()
    old=load(ROOT/'release_stack_before_Maria359.json');new=load('translations/release_stack.json')
    assert old['latest_promoted_build']==new['latest_promoted_build']
    testroot=Path('work/maria359_repository_qa_v1')
    first,second=[ET.parse(testroot/p).getroot()[0] for p in ['pytest.xml','temp_retry.xml']]
    assert (first.attrib['tests'],first.attrib['errors'],first.attrib['failures'])==('27','2','0')
    assert (second.attrib['tests'],second.attrib['errors'],second.attrib['failures'])==('2','0','0')
    # Parse only this new batch's producers; historical failed producers are preserved.
    producers=sorted(set(Path('scripts').glob('*maria359*.py'))|{Path('dk4tool/patch/maria359_release_v1.py'),
        Path('scripts/check_scoped_clean_menus_v2.py'),Path('scripts/rebind_unchanged_native_style_plan_v1.py'),Path('scripts/seal_clean_editorial_parts_v1.py')})
    for path in producers:ast.parse(path.read_bytes(),filename=str(path))
    OUT.mkdir();verification=OUT/'verification';verification.mkdir()
    (OUT/'translation.xdelta').write_bytes(Path(release['patch']).read_bytes())
    for src,name in [(release['manifest'],'build_manifest.json.gz'),('translations/release_stack.json','build_release_stack.json.gz')]:
        raw=Path(src).read_bytes();packed=gzip.compress(raw,compresslevel=9,mtime=0);assert gzip.decompress(packed)==raw;(OUT/name).write_bytes(packed)
    proofs=[ROOT/'registered_release_verification.json',ROOT/'own_registered_startup_verification.json',ROOT/'own_registered_name_getters_v1.json',
        ROOT/'completion_checkpoint.json',EDITORIAL/'gameplay_review_v1.json',EDITORIAL/'offline_display_approval_v1.json',EDITORIAL/'final_layout_delta_v1.json']
    for src in proofs:(verification/src.name).write_bytes(src.read_bytes())
    save(verification/'repository_checks.json',dict(selected_tests=27,passing_tests=27,initial=dict(passed=25,temp_parent_setup_errors=2),
        targeted_retry=dict(passed=2,failed=0),test_reports={str(testroot/p):digest(testroot/p) for p in ['pytest.xml','temp_retry.xml']},
        active_batch_producers_parsed={str(p):digest(p) for p in producers},production_scope_rejection_tests=8,
        source_qualification=str(EDITORIAL/'registered_semantic_checks_v1/qualification.json'),
        exact_native_stored_actual_andregistered_guards_pass=True,all_historical_failed_producers_preserved=True))
    save(OUT/'release_manifest.json',dict(profile=release['profile'],status='registered-candidate-awaiting-user-acceptance',
        candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],clean_input_sha256=release['clean_input_sha256'],
        patch='translation.xdelta',patch_sha256=release['patch_sha256'],build_manifest_sha256=release['manifest_sha256'],release_stack_sha256=release['registry_sha256'],
        entries=723,accepted_layers=114,passing_release_checks=58,integrated_editorial_records=23429,main_promoted=False,full_goal_complete=False))
    text=f'''# Combined editorial candidate — November 10, 2026

Ready for testing and promotion acceptance. This cumulative candidate includes every accepted layer through Maria B253–B274, earlier Rafael/tutorial work, the Market Trade-screen fix, speaker-name work andthe registered ASCII right-bound correction. Main remains V4701 pending acceptance. No ROM is distributed in this GitHub package.

Apply `translation.xdelta` to the clean Japanese ROM with SHA256 `{release['clean_input_sha256']}`. Expected output SHA256: `{release['candidate_sha256']}`. Patch SHA256: `{release['patch_sha256']}`. Reconstruction is verified byte for byte. The local test ROM and adjacent manifest areat `{release['candidate']}`.

The manifest contains723 entries,114 accepted layers and58 passing release checks. This batch adds359 contextual reviews:219 revisions and140 justified retentions,with18 scoped name reviews. All350 final body pages,ten captions and21 name strings were visually reviewed;34 final layouts improve,one page is reclaimed andthree mixed-width text glyphs are corrected. Three disclosed initialized emulator samples verify164 bodies/165 pages,allfive menus/ten captions,one page turn,eleven FE returns andthree sailing returns. The185 remaining bodies have offline native/stored checks only. The candidate's own31,000-frame startup reaches Hangzhou;both original getters pass for12 protected actors. Hardware andexhaustive natural progression are untested.

The ledger credits23,429 contextual reviews. Native story remainder:2,469 objects (Maria664;Lil1,805),plus separate shared/player-facing scope. The full editorial goal remains active. No guide photos are collected. Deferred artwork andthe later older-record technical re-audit remain separate. See [the current checkpoint](../../docs/editorial_Maria359_B253_B274_registered_20261110.md) for exact scope andevidence.

The two gzip files preserve exact build-time manifest andregistry bytes. `verification/` contains release,startup,getter,gameplay,offline-display andtally-correction proofs. All27 selected repository tests pass after rerunning two temporary-directory setup errors. Eight production scope mutations are rejected. Earlier ROMs,drafts,translations,evidence andfailed historical producers are preserved. A historical informational35-layout tally is corrected to34 by `final_layout_delta_v1.json`;no text orROM change is involved.

The coverage ledger uses Git LFS. Run `git lfs pull` after cloning to obtain its exact hydrated bytes. The clean-input patch reconstructs the ROM without historical work-folder artifacts.
'''
    (OUT/'README.md').write_text(text,encoding='utf-8',newline='\n')
    save(OUT/'checksums.json',{str(p.relative_to(OUT)).replace('\\','/'):digest(p) for p in OUT.rglob('*') if p.is_file()})
    assert digest(OUT/'translation.xdelta')==release['patch_sha256']
    print('Packaged723-entry cumulative candidate andexact clean-input patch;main unchanged.')

if __name__=='__main__':main()
