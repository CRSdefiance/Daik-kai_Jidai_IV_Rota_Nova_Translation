"""Record precise source/prose and fixed-footprint runtime progress;no release credit."""
from pathlib import Path
from shutil import copy2

from dk4tool.patch.grand_race_menu_release import sha
from scripts import battle_declaration_runtime_v993b as runtime
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/battle_declaration_v994')
PROOF = Path('work/analysis/battle_declaration_v993c/native_runtime_verification.json')
MANUSCRIPT = Path('translations/battle_declaration_editorial_manuscript_v2.json')
RETENTION = Path('work/rom_retention/20261021T0247168447601Z.json')


def main():
    final = ROOT/'runtime_checkpoint.json'
    assert not final.exists()
    proof = read(PROOF)
    assert proof['runtime_sha256'] == sha(Path(runtime.__file__).read_bytes())
    assert proof['old_and_new_complete_scope_cases_each'] == 54904
    assert proof['all3668_modal_outputs_and_wrap_choices_exact'] and proof['all140_status8MiB_ABI_guards_pass']
    for path, digest in proof['all_completed_source_proofs'].items():
        assert sha(Path(path).read_bytes()) == digest, path
    source = Path('work/analysis/battle_declaration_v991c/source_context_packet.json')
    context = read(source)
    assert len(context['all832_original_object_voice_selections']) == 832
    assert len(context['all45_original_role_wrapper_argument_and_UI_result_cases']) == 45
    assert len(context['all24_original_branch_fragment_cases']) == 24
    draft = read(MANUSCRIPT)
    assert len(draft['records']) == 22 and all(not r['review']['formatting'] for r in draft['records'])
    assert sum(r['editorial_decision'] == 'revise' for r in draft['records']) == 13
    assert sha(source.read_bytes()) == draft['native_context_proof_sha256']
    for key in ('source_context_supplement', 'native_name_preview_followup', 'reviewed_research_manuscript'):
        assert sha(Path(draft[key]).read_bytes()) == draft[key+'_sha256']
    plan = read(RETENTION)
    assert len(plan['roms']) == 215 and all(r['action'] == 'keep' for r in plan['roms'])
    assert sha(Path('scripts/prune_generated_roms.ps1').read_bytes()) == 'aacaca07b50f1bafcfc5bb8579b609b0be2a8e79e3107f336405ba370a435f6f'
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    candidate = ledger['current_integrated_candidate']
    assert candidate['sha256'] == proof['candidate_sha256'] == context['candidate_sha256']
    assert sha(Path(candidate['path']).read_bytes()) == candidate['sha256']
    manifest = read(Path(candidate['path']).with_suffix('.manifest.json'))
    assert manifest['candidate_sha256'] == candidate['sha256']
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert ledger['records_editorially_completed'] == 1174 and ledger['records_with_source_and_prose_pass'] == 1199
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values()) == 1199
    save(ROOT/'editorial_ledger_before_runtime_checkpoint.json', ledger)
    checkpoint = ('V994 completes fixed-footprint runtime research for the same22 battle/declaration drafts. Only native confirmation parent02053D24 with exact source table02117420 gains wrapping membership.54904 source and54904 research selector/ABI cases,all3668 prior complete modal outputs,238 wrong-parent controls,5 full-word edges and140 typed-status/8MiB guard cases pass. The public bank remains212 bytes and modal128;all sections,BSS,cache and entire123040-byte staged payload remain unchanged. A rejected research filter was corrected for ARMs low-eight-bit register-shift behavior before any ROM build. Four natural questions also avoid double periods after complete Co. labels. Native complete-font/name expansion matrix,registered integration,exact patch and actual scene/confirmation/dismissal/return verification remain pending. V987 remains current;1174 complete,1199 source/prose reviewed. No new completed-entry credit;global formatting watch,separate graphics/all18 plaques,older750-752,raw/source coverage,Samwell header and later older-record re-audit remain open;full goal active.')
    ledger['latest_checkpoint'] = checkpoint
    ledger['battle_declaration_v994']['native_runtime_research'] = str(PROOF)
    ledger['battle_declaration_v994']['runtime_status'] = 'bounded-native-selector-modal-status-regressions-pass-fonts-release-actual-pending'
    ledger['research_checkpoints'].append({'id': 'V994-battle-declaration-runtime-research', 'proof': str(PROOF),
        'manuscript': str(MANUSCRIPT), 'source_prose_reviews_added': 0, 'completed_entries_added': 0,
        'previous_goal_turn_classification': 'progress:current V987 repaired shop676/677 bytes freshly confirmed and earlier actual corrected image reviewed',
        'this_goal_turn_classification': 'progress:22 source/prose reviews13 revisions9 retentions plus source speaker/argument/cancel matrices and fixed-footprint runtime selector/modal/status proof',
        'full_goal_complete': False})
    previous = read(ROOT/'editorial_ledger_before_runtime_checkpoint.json')
    for key in ('current_integrated_candidate', 'source_pins', 'current_native_relocation_reference', 'formatting_watchlist',
                'unresolved_graphics_work', 'older_record_reaudit_after_full_editorial_goal', 'raw_source_coverage_revisit', 'approved_name_roles'):
        assert ledger[key] == previous[key]
    save(ledger_path, ledger)
    doc = Path('docs/battle_declaration_v993_runtime_checkpoint.md')
    assert not doc.exists()
    with doc.open('x', encoding='utf-8') as f:
        f.write('# V993-V994: battle/declaration bounded runtime research\n\n'+checkpoint+'\n\n')
        f.write('## Remaining gates\n\n- All22 complete native font planes and the complete runtime faction-name substitution matrix,with automatic source-consumer wrapping.\n- Native copy/cache checks and registered full-stack integration with an exact clean-input patch.\n- Actual cold-boot title/New Game regression and representative original announcement/known/unknown confirmation scenes,including cancellation,acceptance,dismissal and ordinary return.\n- Update completion coverage only after those gates pass;the global editorial and separate graphics goals remain incomplete.\n\n')
        f.write('The new public table grows176 to178 bytes inside its existing212-byte owner. Its neighboring unchanged24-byte phrase table moves two bytes,and the private filter shrinks12 to10 bytes. The128-byte modal wrapper uses its old alignment padding and removes a redundant comparison. Original164-byte selector gate remains exact. Whole-ROM changes are not claimed because this is an ARM9 research binary only.\n')
    for p in map(Path, ('docs/translation_progress.md', 'docs/editorial_review_goal.md', 'docs/todo.md', 'docs/known_issues.md')):
        with p.open('a', encoding='utf-8') as f:
            f.write('\n\n## V994: battle/declaration bounded runtime research\n\n'+checkpoint+' See [V993-V994 runtime checkpoint](battle_declaration_v993_runtime_checkpoint.md).\n')
    files = [PROOF, MANUSCRIPT, source, Path(__file__), doc, ledger_path, RETENTION]
    files += [Path(p) for p in proof['all_completed_source_proofs']]
    files += [Path(p) for p in ('scripts/battle_declaration_runtime_v993.py', 'scripts/battle_declaration_runtime_v993b.py',
        'scripts/verify_battle_declaration_runtime_v993.py', 'scripts/verify_battle_declaration_runtime_v993b.py',
        'scripts/finish_battle_declaration_runtime_v993c.py', 'work/analysis/battle_declaration_v993/successor_provenance.json')]
    archive = Path('E:/Rota Nova translations/Editorial review/V994 Battle declaration runtime research')
    assert not archive.exists()
    copies = []
    for source_path in dict.fromkeys(files):
        destination = archive/source_path.absolute().relative_to(Path.cwd())
        destination.parent.mkdir(parents=True, exist_ok=True)
        assert not destination.exists()
        copy2(source_path, destination)
        assert source_path.read_bytes() == destination.read_bytes()
        copies.append({'source': str(source_path), 'archive': str(destination), 'sha256': sha(destination.read_bytes())})
    archive_manifest = ROOT/'runtime_archive_manifest.json'
    save(archive_manifest, {'files': copies, 'all_hashes_verified': True, 'no_ROM_or_save_duplicated': True})
    before_completion = read('work/analysis/activity_special_v988/editorial_ledger_before_completion.json')
    for key in ('approved_name_roles', 'unresolved_graphics_work', 'older_record_reaudit_after_full_editorial_goal', 'raw_source_coverage_revisit'):
        assert ledger[key] == before_completion[key]
    assert sha(Path('work/clean.nds').read_bytes()) == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    assert sha(Path('out/raphael_natural_v2_accepted_base.nds').read_bytes()) == '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    save(final, {'candidate': candidate, 'native_runtime_proof': str(PROOF), 'native_runtime_proof_sha256': sha(PROOF.read_bytes()),
        'manuscript': str(MANUSCRIPT), 'manuscript_sha256': sha(MANUSCRIPT.read_bytes()),
        'completed_entries': 1174, 'source_prose_reviewed': 1199, 'new_completed_credit': 0,
        'new_source_prose_reviews_this_turn': 22, 'source_revision_retention_decisions': [13, 9],
        'all_archived_evidence_rehashed': all(sha(Path(r['archive']).read_bytes()) == r['sha256'] for r in copies),
        'current_ROM_clean_canonical_registry_global_formatting_watch_names_and_separate_audits_preserved': True,
        'retention_preview': str(RETENTION), 'keep215_delete0_no_apply': True,
        'no_playable_ROM_or_patch_built_no_actual_scene_claim': True,
        'next_action': 'Complete all22 native font/name-substitution matrix and source-consumer wrapping,then registered integration/exact patch/representative actual scenes.',
        'goal_status': 'active', 'full_goal_complete': False, 'producer_sha256': sha(Path(__file__).read_bytes())})
    print('Checkpoint saved and archived on E:1174 complete,1199 source/prose;22 reviewed drafts and bounded runtime proof. V987 unchanged;fonts,registered integration and actual scenes pending. Goal active.')


if __name__ == '__main__':
    main()
