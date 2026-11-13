"""Archive measured runtime space and rejected helper reuse;no release credit."""
from pathlib import Path
from shutil import copy2
import json

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/duel_renderer_checkpoint_v1127')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V1127 Duel renderer space and native equivalence')


def main():
    assert not ROOT.exists() and not ARCHIVE.exists()
    proposal_path = Path('work/analysis/duel_renderer_thumb_v1124/assembly_proposal.json')
    paired_path = Path('work/analysis/duel_thumb_equivalence_v1124/original_vs_thumb_equivalence.json')
    ownership_path = Path('work/analysis/duel_renderer_ownership_v1125/owned_function_transcription_and_tail.json')
    helper_path = Path('work/analysis/duel_existing_balancer_v1126b/existing_balancer24_matrix.json')
    proposal, paired, ownership, helper = [read(path) for path in (proposal_path, paired_path, ownership_path, helper_path)]
    assert proposal['transcription_bytes'] == 200 and proposal['remaining_function_tail_bytes'] == 108
    assert len(paired['cases']) == 159 and ownership['all195_context_widget_macro_timing_and_callee_saved_pairs_pass']
    assert ownership['private_tail_for_future_formatter'] == [0x0200DAF0, 0x0200DB5C]
    assert ownership['all_sections_BSS_cache_and_entire123040byte_staged_payload_exact']
    findings = helper['unacceptable_for_duel_without_additional_policy']
    assert len(helper['cases']) == 4160 and len(findings) == 218
    assert all('exceeds-visible24-columns' in row['findings'] for row in findings)
    assert sum('single-word-final-row' in row['findings'] for row in findings) == 1
    candidate = Path(proposal['candidate'])
    assert sha(candidate.read_bytes()) == proposal['candidate_sha256']
    baseline = Path('out/raphael_natural_v2_accepted_base.nds')
    assert sha(baseline.read_bytes()) == '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    retention_path = Path('work/rom_retention/20261021T1547187116749Z.json')
    retention = json.loads(retention_path.read_text(encoding='utf-8-sig'))
    assert len(retention['roms']) == 223 and all(Path(row['path']).is_file() for row in retention['roms'])
    manuscript_path = Path('translations/duel_editorial_manuscript_v3.json')
    assert all(not row['review']['formatting'] for row in read(manuscript_path)['records'])
    ROOT.mkdir(parents=True)
    summary = (
        'V1127 advances the duel runtime implementation by transcribing original DA28 into200 bytes '
        'of ARM-entry/Thumb code within its original308-byte function. Original stack footprint and '
        'all76 allocated context bytes remain exact.195 paired CPU checks cover53 caller paths in '
        'three duration/key modes plus36 empty,multiline,CP932,spacing and width controls. Complete '
        'widget state,macro output,callee-saved registers,stack restoration and modeled engine-call '
        'sequences/captured arguments match. A flagged multiline regression was exposed and corrected; '
        'the initial159 one-paragraph checks alone had not proven that branch. Source/current reference '
        'census finds only the two preserved external entry calls and no incoming tail references. '
        'Thumb1/ARMv5-BLX code,return/literal boundaries,and section/BSS/cache shapes are verified. '
        'The entire123040-byte staged payload is exact. This gives108 owned bytes at0200DAF0..0200DB5C '
        'for future formatter code,without repurposing mutable caption memory. A separate4160-case '
        'native balanced-helper24-column trial retains all words and ABI,but218 cases exceed the '
        'actual viewport,including one orphaned final word. Its width fallback/search policy is '
        'unsuitable unchanged;no shortened prose or widened box was substituted. The dedicated '
        'post-expansion24x3 formatter still needs implementation,complete native fonts,registered '
        'integration/exact patch and original scene transitions. No playable ROM,patch,registry or '
        'prose changed. All33 formatting gates stay false;1196 complete,1267 source/prose-reviewed, '
        'no completion credit. V1105 experimental,V997 fully scene-verified,canonical unchanged. '
        'Full editorial scope,global formatting and separate graphics audit remain active. The '
        'retention preview lists223 ROMs and all remain present;no deletion was applied.'
    )
    proof_path = ROOT / 'checkpoint.json'
    save(proof_path, {'summary': summary, 'research_proposal': str(proposal_path),
        'paired_native_checks': str(paired_path), 'ownership_and_extended_controls': str(ownership_path),
        'rejected_existing_helper_profile': str(helper_path), 'retention_preview': str(retention_path),
        'all223_ROMs_present_no_ApplyPlan_or_deletions': True,
        'candidate_sha256': proposal['candidate_sha256'],
        'experimental_transcription_not_a_production_formatter_or_actual_gameplay': True,
        'completion_credit': 0, 'full_goal_complete': False,
        'producer_sha256': sha(Path(__file__).read_bytes())})
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    assert ledger['records_editorially_completed'] == 1196 and ledger['records_with_source_and_prose_pass'] == 1267
    ledger['duel_prose_v1103'].update(renderer_implementation_checkpoint=str(proof_path),
        existing_shared_balancer24_rejected=str(helper_path),
        formatter_next_action='Implement dedicated post-expansion24x3 policy using proven owned code;old helper fallback is unsafe.',
        renderer_scope='195 paired CPU checks with explicit loader/UI/SDK/font/engine boundaries;not actual gameplay')
    ledger['formatting_watchlist']['duel_shared_balancer_policy'] = {
        'proof': str(helper_path), 'complete_name_cases': 4160, 'bounds_findings': 218,
        'status': 'unchanged-helper-reuse-rejected;dedicated-runtime-pending',
        'prose_font_border_and_viewport_preserved': True}
    ledger['latest_checkpoint'] = summary
    save(ledger_path, ledger)
    doc = Path('docs/duel_v1127_renderer_implementation_checkpoint.md')
    doc.write_text('# V1127: duel runtime implementation space and equivalence\n\n' + summary +
        '\n\n## Rejected intermediates\n\n'
        'V1121 rejected guessed engine-context constants before writing a proposal. The successor '
        'binds original literals022CF7DC/022CF784/023120B4. V1122 rejected an attempted outer-code '
        'constant adaptation;its successor changes exact nested callback source instead. The first '
        'compact frame moved the private context and failed strict comparison. V1123 reserves '
        'the original stack footprint;the test also limits its context read to the original '
        'allocated76 bytes,not four bytes beyond it. A separate three-line input exposed a Thumb '
        'MOVS clobbering comparison flags and incorrectly selecting Y12. V1124 moves that MOVS '
        'before CMP. All original and extended checks pass after the correction.\n\n'
        'CPU tests execute native selectors,printf,macro processing,constructors and teardown. '
        'They explicitly model message loading,SDK clear,UI registration,font entry and engine '
        'yield/event/key/sound boundaries. Engine traces compare the captured R0/R1 arguments; '
        'the source-bound call sequences explicitly set the key-query third argument to zero '
        'on both paths. This evidence is not full GPU,engine or gameplay verification.\n\n'
        'The native balanced helper trial initializes24/24 widths at its original internal run '
        'entry,using a CPU-only trampoline. Its original minimum-width/reset/fallback behavior '
        'can return wider text,so the profile fails218 source-name cases. For example1944 can '
        'return25 cells in a single row,although the dedicated Python prototype already finds '
        'complete natural two-row layouts. Do not shorten correct prose to accommodate that '
        'helper,accept its default-width fallback,or widen the original box.\n', encoding='utf-8')
    for filename in ('docs/translation_progress.md', 'docs/todo.md', 'docs/known_issues.md'):
        with Path(filename).open('a', encoding='utf-8') as stream:
            stream.write('\n\n## V1127: duel renderer implementation research\n\n' + summary +
                         ' See [V1127 evidence](duel_v1127_renderer_implementation_checkpoint.md).\n')
    sources = [Path(__file__), ledger_path, doc, proof_path, manuscript_path, retention_path]
    for pattern in ('*v1121*.py', '*v1122*.py', '*v1123.py', '*v1124.py', '*v1125.py', '*v1126*.py'):
        sources += list(Path('scripts').glob(pattern))
    for folder in ('duel_renderer_thumb_v1121b', 'duel_renderer_thumb_v1123', 'duel_renderer_thumb_v1124',
                   'duel_thumb_equivalence_v1124', 'duel_renderer_ownership_v1125', 'duel_existing_balancer_v1126b'):
        sources += list(Path('work/analysis', folder).rglob('*.json'))
        sources += list(Path('work/analysis', folder).rglob('*.bin'))
    sources += [Path(name) for name in ('docs/translation_progress.md', 'docs/todo.md', 'docs/known_issues.md')]
    ARCHIVE.mkdir(parents=True)
    files, seen = [], set()
    for source in sources:
        source = source.absolute()
        if source in seen:
            continue
        seen.add(source)
        target = ARCHIVE / source.relative_to(Path.cwd())
        target.parent.mkdir(parents=True, exist_ok=True)
        copy2(source, target)
        digest = sha(source.read_bytes())
        assert sha(target.read_bytes()) == digest
        files.append({'source': str(source), 'archived': str(target), 'sha256': digest})
    save(ARCHIVE / 'archive_manifest.json', {'files': files, 'all_hashes_verified': True,
        'not_a_playable_ROM_release_or_goal_completion': True, 'full_goal_complete': False})
    save(ROOT / 'archive_receipt.json', {'archive': str(ARCHIVE), 'files': len(files),
        'manifest_sha256': sha((ARCHIVE / 'archive_manifest.json').read_bytes())})
    print(f'V1127 archived {len(files)} hash-verified files;195 paired checks and108 owned bytes;dedicated formatter remains next.')


if __name__ == '__main__':
    main()
