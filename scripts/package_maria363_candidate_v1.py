"""Package the registered cumulative candidate for acceptance without promoting main."""
import ast
import gzip
import json
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/maria363_B216_B252_release_v1')
OUT=Path('releases/all_routes_editorial_20261110_candidate')

def main():
    assert not OUT.exists()
    release=load(ROOT/'registered_release_verification.json')
    complete=load(ROOT/'completion_checkpoint.json')
    ledger=load('translations/editorial_review_current_v1.json')
    assert (release['registered_manifest_entries'],release['accepted_layers'],release['passing_release_checks'])==(722,114,57)
    assert complete['counts']==dict(completed=23070,revised=13778,retained=9292)
    assert not release['own_registered_startup_pending'] and release['clean_input_patch_byte_exact']
    assert ledger['current_integrated_candidate']['sha256']==release['candidate_sha256']
    assert not ledger['full_goal_complete']
    registry=load('translations/release_stack.json')
    before_registry=load(ROOT/'release_stack_before_Maria363.json')
    assert registry['latest_promoted_build']==before_registry['latest_promoted_build']
    assert digest('translations/release_stack.json')==release['registry_sha256']
    for k in ['candidate','manifest','patch']:
        assert digest(release[k])==release[k+'_sha256']
    assert Path(release['candidate']).read_bytes()==Path(release['exact_clean_reconstruction']).read_bytes()
    OUT.mkdir();verification=OUT/'verification';verification.mkdir()
    (OUT/'translation.xdelta').write_bytes(Path(release['patch']).read_bytes())
    for src,name in [(release['manifest'],'build_manifest.json.gz'),('translations/release_stack.json','build_release_stack.json.gz')]:
        raw=Path(src).read_bytes();packed=gzip.compress(raw,compresslevel=9,mtime=0)
        assert gzip.decompress(packed)==raw;(OUT/name).write_bytes(packed)
    proofs=[ROOT/'registered_release_verification.json',ROOT/'own_registered_startup_verification.json',ROOT/'own_registered_name_getters_v1.json',
        ROOT/'completion_checkpoint.json',Path('work/Maria_B216_B252_clean_20261110/gameplay_review_v1.json'),
        Path('work/Maria_B216_B252_clean_20261110/offline_display_approval_v1.json')]
    for src in proofs:
        (verification/src.name).write_bytes(src.read_bytes())
        assert digest(verification/src.name)==digest(src)
    retry=load_xml=Path('work/github_candidate_qa_20261110/hardlink_retry_v1.xml')
    assert retry.exists() and 'failures="0"' in retry.read_text() and 'tests="1"' in retry.read_text()
    syntax_failures=[]
    for p in Path('scripts').glob('*.py'):
        try:ast.parse(p.read_bytes(),filename=str(p))
        except (SyntaxError,UnicodeError) as e:syntax_failures.append(dict(path=str(p),error=str(e)))
    assert len(syntax_failures)==18
    save(verification/'repository_checks.json',dict(selected_pytest_tests=92,passing_tests=92,
        initial_result=dict(passed=88,temp_setup_errors=4),writable_temp_retry=dict(passed=3,hardlink_sandbox_denial=1),
        unsandboxed_existing_hardlink_test=dict(passed=1,XML=str(retry),sha256=digest(retry)),
        syntax_scan='Broad diagnostic, not a clean all-producers syntax claim',
        preserved_historical_failed_producers=syntax_failures,
        active_candidate_release_chain_all_gates_pass=True,failed_historical_producers_not_rewritten=True,
        ROMs_and_work_evidence_preserved_locally=True))
    save(OUT/'release_manifest.json',dict(profile=release['profile'],status='registered-candidate-awaiting-user-acceptance',
        candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],clean_input_sha256=release['clean_input_sha256'],
        patch='translation.xdelta',patch_sha256=release['patch_sha256'],build_manifest_sha256=release['manifest_sha256'],
        release_stack_sha256=release['registry_sha256'],entries=722,accepted_layers=114,passing_release_checks=57,
        integrated_editorial_records=23070,main_promoted=False,full_goal_complete=False))
    text=f'''# Combined editorial candidate — November 10, 2026

This registered cumulative build is ready for testing and acceptance. It includes the entire accepted stack through Maria B216–B252, the Rafael/tutorial work already integrated, the Market Trade-screen correction, localized speaker names and the registered ASCII right-bound fix. Main remains V4701 until the user accepts this candidate. No ROM is distributed in this package.

Apply `translation.xdelta` to a clean Japanese ROM with SHA256 `{release['clean_input_sha256']}`. Expected output SHA256: `{release['candidate_sha256']}`. Patch SHA256: `{release['patch_sha256']}`. The clean-input reconstruction has been verified byte for byte. The local ready-to-test ROM and its adjacent manifest are at `{release['candidate']}`.

The cumulative manifest has 722 entries, 114 accepted layers and 57 passing release checks. The latest batch adds 363 contextual reviews: 202 revisions and 161 justified retentions, with 29 scoped name reviews. All 353 final body pages, 12 captions and 31 name strings were visually reviewed. Three native FE wrapping defects are corrected. Three initialized emulator samples cover 252 bodies, 254 unique pages and all 12 captions; 99 bodies have offline native/stored checks only. Own-candidate startup reaches Hangzhou, and both original getters pass for 12 protected actors. Hardware and exhaustive natural progression are untested.

The ledger now credits 23,070 contextual reviews. The remaining native story census is 2,828 objects, plus separate shared/player-facing scope. This candidate does not complete the editorial goal. Deferred graphics artwork and the later older-record technical re-audit remain separate. See [the current checkpoint](../../docs/editorial_Maria363_B216_B252_registered_20261110.md) for exact scope and evidence.

`build_manifest.json.gz` and `build_release_stack.json.gz` preserve exact build-time bytes. `verification/` contains the final scoped proofs and repository-check results. All 92 selected repository tests pass after resolving temporary-directory and sandbox hard-link restrictions. Eighteen historical failed producer scripts remain preserved as evidence; the broad syntax diagnostic is not an all-producers pass. The active candidate chain passes its complete registered guards. Earlier ROMs, drafts, translations and local evidence are preserved.

The coverage ledger uses Git LFS because it exceeds GitHub's regular blob limit. Run `git lfs pull` after cloning if needed; the hydrated ledger must retain its exact bytes. The clean-input patch provides standalone ROM reconstruction without historical work-folder artifacts.
'''
    (OUT/'README.md').write_text(text,encoding='utf-8',newline='\n')
    save(OUT/'checksums.json',{str(p.relative_to(OUT)).replace('\\','/'):digest(p) for p in OUT.rglob('*') if p.is_file()})
    assert digest(OUT/'translation.xdelta')==release['patch_sha256']
    pins=Path('translations/rom_retention_pins.json');old=load(pins);entry=dict(path=str(Path(release['candidate']).resolve()).replace('\\','/'),
        reason='User-requested cumulative November 10 test/promotion candidate; preserve until acceptance and later explicit retention review.')
    if not any(p['path']==entry['path'] for p in old):
        save(pins,[*old,entry]);assert load(pins)[:-1]==old
    print('Packaged registered cumulative Maria363 candidate; main andROM bytes unchanged.')

if __name__=='__main__':main()
