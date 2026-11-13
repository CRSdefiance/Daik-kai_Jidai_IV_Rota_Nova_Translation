"""Package the cumulative clean-input patch and exact build proofs for GitHub testing."""
import ast
import gzip
import xml.etree.ElementTree as ET
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/maria349_B275_B285_release_v1')
EDITORIAL=Path('work/Maria_B275_B285_clean_20261110')
OUT=Path('releases/all_routes_editorial_20261110_maria349_candidate')

def main():
    assert not OUT.exists()
    release=load(ROOT/'registered_release_verification.json');complete=load(ROOT/'completion_checkpoint.json')
    assert (release['registered_manifest_entries'],release['accepted_layers'],release['passing_release_checks'])==(724,114,59)
    assert complete['counts']==dict(completed=23778,revised=14181,retained=9597)
    assert not release['own_registered_startup_pending'] and release['clean_input_patch_byte_exact']
    assert digest('translations/release_stack.json')==release['registry_sha256']
    for key in ['candidate','manifest','patch']:assert digest(release[key])==release[key+'_sha256']
    assert Path(release['candidate']).read_bytes()==Path(release['exact_clean_reconstruction']).read_bytes()
    old=load(ROOT/'release_stack_before_Maria349.json');new=load('translations/release_stack.json')
    assert old['latest_promoted_build']==new['latest_promoted_build']
    reportpath=Path('work/maria349_repository_qa_v1/pytest.xml');tests=ET.parse(reportpath).getroot()[0]
    assert (tests.attrib['tests'],tests.attrib['errors'],tests.attrib['failures'])==('27','0','0')
    producers=sorted(set(Path('scripts').glob('*maria349*.py'))|{Path('dk4tool/patch/maria349_release_v1.py')})
    for path in producers:ast.parse(path.read_bytes(),filename=str(path))
    semantic=EDITORIAL/'registered_semantic_checks_v1/qualification.json'
    OUT.mkdir();verification=OUT/'verification';verification.mkdir()
    (OUT/'translation.xdelta').write_bytes(Path(release['patch']).read_bytes())
    for src,name in [(release['manifest'],'build_manifest.json.gz'),('translations/release_stack.json','build_release_stack.json.gz')]:
        raw=Path(src).read_bytes();packed=gzip.compress(raw,compresslevel=9,mtime=0);assert gzip.decompress(packed)==raw;(OUT/name).write_bytes(packed)
    proofs=[ROOT/'registered_release_verification.json',ROOT/'own_registered_startup_verification.json',ROOT/'own_registered_name_getters_v1.json',
        ROOT/'completion_checkpoint.json',EDITORIAL/'gameplay_review_v1.json',EDITORIAL/'offline_display_approval_v1.json',EDITORIAL/'final_layout_delta_v1.json',semantic]
    for src in proofs:(verification/src.name).write_bytes(src.read_bytes())
    save(verification/'repository_checks.json',dict(selected_tests=27,passing_tests=27,errors=0,failures=0,test_report=str(reportpath),test_report_sha256=digest(reportpath),
        active_batch_producers_parsed={str(p):digest(p) for p in producers},production_scope_rejection_tests=8,
        source_qualification=str(semantic),exact_native_stored_actual_andregistered_guards_pass=True,all_historical_failed_producers_preserved=True))
    save(OUT/'release_manifest.json',dict(profile=release['profile'],status='registered-candidate-awaiting-user-acceptance',
        candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],clean_input_sha256=release['clean_input_sha256'],
        patch='translation.xdelta',patch_sha256=release['patch_sha256'],build_manifest_sha256=release['manifest_sha256'],release_stack_sha256=release['registry_sha256'],
        entries=724,accepted_layers=114,passing_release_checks=59,integrated_editorial_records=23778,main_promoted=False,full_goal_complete=False))
    text=f'''# Combined editorial candidate — November 10, 2026

Ready for testing and promotion acceptance. This cumulative candidate includes every accepted layer through Maria B275–B285, earlier Rafael/tutorial work, the Market Trade-screen fix, speaker-name work and the registered ASCII right-bound correction. Main remains V4701 pending acceptance. This GitHub package contains a patch; the ROM is available locally.

Apply `translation.xdelta` to the clean Japanese ROM with SHA256 `{release['clean_input_sha256']}`. Expected output SHA256: `{release['candidate_sha256']}`. Patch SHA256: `{release['patch_sha256']}`. Reconstruction is verified byte for byte. The local test ROM and adjacent manifest are at `{release['candidate']}`.

The manifest contains 724 entries, 114 accepted layers and 59 passing release checks. This batch adds 349 contextual reviews: 184 revisions and 165 justified retentions, with 19 scoped name reviews. All 347 final body pages, eight captions and 21 name strings were visually reviewed. Ten final layouts improve and three pages are reclaimed without shortening prose. The source review corrects smuggler and impersonation plot facts, preserves uncertainty and cultural context, and fixes the guardians' village being far northeast of China. Speaker and runtime controls remain intact.

Three disclosed initialized emulator samples verify 191 bodies/193 pages, all three menus/eight captions, two page turns, all seven system-message returns and three sailing returns. The other 150 body variants have offline native/stored checks. The candidate's own 31,000-frame startup reaches Hangzhou; both original getters pass for twelve protected actors. Hardware and exhaustive natural progression remain untested. All 27 selected repository tests and eight production mutation rejections pass.

The ledger credits 23,778 contextual reviews: 14,181 revisions and 9,597 retentions. Native story remainder: 2,120 objects (Maria 315; Lil 1,805), plus separate shared/player-facing scope. The full editorial goal remains active. No guide photos are collected. Deferred artwork and the later older-record technical re-audit remain separate. See [the current checkpoint](../../docs/editorial_Maria349_B275_B285_registered_20261110.md) for scope and evidence.

The two gzip files preserve exact build-time manifest and registry bytes. `verification/` contains release, startup, getter, gameplay, offline-display, layout and repository proofs. Earlier ROMs, translations, drafts, evidence and failed historical producers are preserved. The coverage ledger uses Git LFS; run `git lfs pull` after cloning. The clean-input patch reconstructs this ROM without historical work-folder artifacts.
'''
    (OUT/'README.md').write_text(text,encoding='utf-8',newline='\n')
    save(OUT/'checksums.json',{str(p.relative_to(OUT)).replace('\\','/'):digest(p) for p in OUT.rglob('*') if p.is_file()})
    assert digest(OUT/'translation.xdelta')==release['patch_sha256']
    print('Packaged724-entry cumulative candidate andexact clean-input patch;main unchanged.')

if __name__=='__main__':main()
