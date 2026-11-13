"""Freeze the corrected31-entry native research; release/gameplay gates stay open."""

import ast
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_memory_streams_v682 import copy
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/tavern_coordinates_v766')
LEDGER = Path('translations/editorial_review_current_v1.json')
DOC = Path('docs/tavern_coordinates_v766_research.md')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V766 Tavern coordinate and dialogue research')


def main():
    assert not ARCHIVE.exists()
    verification = read(ROOT / 'verification.json')
    layouts = read(ROOT / 'native_layout_matrix.json')
    assert verification['complete_native_layouts'] == layouts['count'] == 38957
    assert layouts['findings_count'] == 0 and not verification['native_bank_writes']
    assert verification['all94_coordinate_pairs_intact'] and verification['all38863_other_outputs_byte_exact_to_V764']
    assert len(verification['complete_font_planes']) == 166
    compare = read(ROOT / 'unchanged_font_comparison.json')
    assert compare['all_other_complete_font_planes_byte_identical'] == 162 and compare['new_coordinate_planes'] == 4
    assert read(ROOT / 'coordinate_buffer_contracts.json')['count'] == 104
    inherited = read(ROOT / 'inherited_outputs.json')
    assert len(inherited['all1124_Yard_outputs']) == 1124 and len(inherited['all40_Port_cases']) == 40
    assert len(inherited['all180_earlier_parent_output_controls']) == 180 and not inherited['native_bank_writes']
    assert read(ROOT / 'actual_leader_layout_matrix.json')['count'] == 14400
    providers = read(ROOT / 'owned_provider_fragments.json')
    assert len(providers['cases']) == 202 and len(providers['all94_global_coordinate_provider_outputs_unchanged']) == 94
    save(ROOT / 'visual_review.json', {
        'all14_original_full_preview_sheets_visually_inspected': [
            {'path': str(p), 'sha256': sha(p.read_bytes())} for p in sorted(Path('work/analysis/tavern_conversations_v764').glob('complete_fonts_*_2x.png'))],
        'all162_unmodified_font_planes_byte_identical_to_inspected_set': True,
        'four_new_coordinate_planes_visually_inspected': compare,
        'review': 'Aligned visible left margins,complete first/final characters,whole words,bounds and readable compass/number pairs. Original V76474 and V76594 semantic coordinate findings remain in their research evidence;the final typed formatter resolves all94.',
        'actual_revised_ROM_scene_not_yet_verified': True})
    ledger = read(LEDGER)
    assert (ledger['records_editorially_completed'], ledger['records_with_source_and_prose_pass']) == (167, 201)
    save(ROOT / 'editorial_ledger_before_v766.json', ledger)
    ledger['latest_checkpoint'] = 'V766:31 Tavern drafts pass38957 native layouts,166 complete font planes and14400 real leader-name layouts. Direct842-only post-printf coordinate compaction fixes letter/number splits;104 whole8MiB memory/register contracts,202 provider fragments,94 unchanged global coordinate outputs and all1124 Yard/40 Port/180 earlier controls pass. All prior font planes or changed coordinates visually inspected. No new ROM;167 completed/201 source-prose unchanged;registered copies/patch and revised actual scenes pending.'
    ledger['active_source_prose_drafts']['manuscripts'][-1] = 'translations/tavern_conversations_editorial_manuscript_v3.json'
    ledger['active_source_prose_drafts']['groups'][-1]['remaining'] = 'Full native research passed. Complete registered31-entry COMMON integration,all copies,exact clean-input patch and paired actual Tavern scenes/New Game/transitions.'
    ledger['active_source_prose_drafts']['note'] = 'V3 preserves actual native person names and faithful natural prose. A source-scoped842-only typed formatter keeps compass letters with their numbers without changing the shared coordinate provider. Native research passes do not grant release/gameplay completion credit;all34 drafts remain incomplete.'
    ledger['research_checkpoints'].append({'id': 'V766-Tavern-typed-coordinate-and-full-native-research', 'documentation': str(DOC),
        'manuscript': 'translations/tavern_conversations_editorial_manuscript_v3.json', 'new_editorially_completed': 0,
        'new_ROM': False, 'full_native_layouts': 38957, 'evidence': str(ROOT / 'verification.json')})
    ledger['findings'].append({'id': 'COMMON-842-compass-letter-number-line-split', 'native_message_ids': [842],
        'status': 'fixed-in-source-scoped-native-research-not-yet-integrated',
        'detail': 'Full visual review found74 pair splits in the first draft despite basic width/word checks. Natural revised prose alone still split94 cases. Exact direct842 post-printf compaction producesN24 E120 style tokens;all94 native inputs and104 whole8MiB/register cases pass. No letters/digits are removed and the global51580 provider is unchanged.'})
    save(LEDGER, ledger)
    DOC.write_text('''# V766: complete Tavern native research and typed coordinate repair

The31 drafts820-850 now pass38957 native layout cases,166 complete independent font planes,14400 current-company-leader name combinations,202 original provider fragments and94 byte-identical global coordinate outputs. All1124 previous Yard layouts,40 Port cases and180 earlier complete native output controls are preserved. Completed167/source-prose201 and34 active drafts remain unchanged;no playable ROM,profile or patch is emitted.

## Visual finding and correction

All14 V764 preview sheets were inspected. The basic byte/bounds/weak-ending checks missed74 cases where a compass letter and its number appeared on separate rows. The revised natural source-faithful sentence,Where exactly? Hmm... Around %s,I think,still exposed94 such breaks under an explicit new pair check. Both failed unpublished drafts and reports are retained.

The final helper runs only for direct842,after original printf expansion and before the existing literal paragraph formatter. It removes alignment spaces inside pairs such asN 24 andE 120,displayingN24 E120 consistently with the game's coordinate headings. It preserves every non-whitespace byte and leaves the shared coordinate formatter,all94 original provider strings and shared compass arrays unchanged. Original printf bytes are still checked before the typed transformation.

The88-byte helper occupies an exactly mapped retired source allocation. Four profession pointers and their unchanged English labels move to three further complete retired allocations;all original replacement owners are preserved. The new164-byte gate fits its168-byte owned bank. Section sizes,staged payload and cache plan stay fixed. All36680 earlier parent/ID/table cases and50 gift/player contracts pass;only direct842 reaches coordinate compaction. All256 profession enum outputs remain correct.

All94 coordinate outputs retain their compass-number pairs on individual rows.104 complete8MiB memory/register comparisons prove only the owned input prefix and24 saved stack bytes change;every code/table/other buffer/guard byte remains exact and all registers/SP/LR are restored. All38863 non842 cases are byte-identical to V764.162 unchanged full font planes match the previously inspected images exactly,and all four new coordinate planes were visually inspected. No ordinary line gains an alignment indent or loses its first/final letter.

## Test-driver continuity

The first long V764 host session failed in Unicorn;the failed producer/log are archived. Final runs refresh initialized CPU instances every64 cases and retain instruction bounds and full callee-saved ABI checks. A scoped registration preserves the exact original ARM946 alignment callback while avoiding its no-op execution at unrelated instructions.1408 full source/destination/guard/ABI comparisons across clean/current code and every alignment phase prove equivalent copy behavior. Explicit provider/dispatcher boundary hooks and immutable-bank write checks remain active. Historical source files are unchanged.

## Remaining release gates

The ordinary original V762 pilot has already mapped a real821 rumor hold at frame5000,with the protected Istanbul save,full native cache/printf/wrap evidence and no RAM fixture. The revised candidate still requires registered COMMON integration,all3668 warm/cold selections,exact clean-input patch reconstruction,paired actual Tavern/New Game evidence and normal returns/scene transitions. Formatting release gates remain false until those offline integration prerequisites pass;no completion credit is awarded here.

V762 remains latest.750-752 caller context,851 onward,wider shared prose,Lil/all other routes,help/remaining prose and the unresolved graphics audit remain open. The thirteen unclassified ordinary name-table entries also require consumer/source classification;they are not assumed visible defects or excluded from the broader audit. The earlier676/677 user-photo formatting check and the older-record follow-up remain active.
''', encoding='utf-8')
    summary = '\n\n## V766 research: Tavern coordinates and complete native review\n\n31 drafts pass38957 layouts,166 full font planes,14400 leader-name layouts,202 provider fragments and94 unchanged global coordinate outputs. A direct842-only post-printf helper resolves compass/number splits;104 whole8MiB/register checks and all1124 Yard/40 Port/180 prior output controls pass. Visual review covers162 identical prior planes and4 changed coordinate planes. No new ROM or completion credit;167 completed/201 source-prose remain. Registered copies/patch,actual revised scenes and broader shared/routes/prose/graphics remain open. See [V766 research](tavern_coordinates_v766_research.md).\n'
    for name in ('translation_progress.md', 'todo.md', 'known_issues.md'):
        path = Path('docs') / name; text = path.read_text(encoding='utf-8')
        assert '## V766 research: Tavern coordinates and complete native review' not in text
        path.write_text(text.rstrip() + summary, encoding='utf-8')
    script_paths = [Path('scripts') / name for name in ('verify_tavern_coordinates_v766.py', 'verify_coordinate_buffers_v766.py',
        'verify_tavern_prior_v766.py', 'verify_tavern_providers_v766.py', 'record_tavern_coordinates_v766.py',
        'refine_tavern_coordinates_v765.py', 'verify_tavern_full_v765.py', 'native_machine_scoped_v764.py', 'verify_scoped_machine_v764.py')]
    modules = [Path('dk4tool/patch') / name for name in ('tavern_coordinate_runtime.py', 'tavern_editorial_runtime.py', 'tavern_conversations_editorial.py')]
    for path in (*script_paths, *modules): ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
    save(ROOT / 'checkpoint_proof.json', {'previous_goal_turn': 'progress: user-photo fix rechecked in V762',
        'this_goal_turn': 'progress: source ownership,typed coordinate fix,full native matrices/fonts/ABI and actual baseline rumor context mapped',
        'completed': 167, 'source_prose': 201, 'drafts': 34, 'latest_ROM': read('out/editorial_review_latest.json'),
        'registry_sha256': sha(Path('translations/release_stack.json').read_bytes()),
        'new_ROM_or_patch': False, 'goal_status': 'active', 'full_goal_complete': False})
    paths = [p for p in ROOT.rglob('*') if p.is_file()]
    paths += [DOC, LEDGER, Path('translations/tavern_conversations_editorial_manuscript_v3.json'), *script_paths, *modules]
    paths += [Path('work/analysis/tavern_storage_v764/scoped_machine_equivalence.json'),
              Path('work/analysis/tavern_conversations_v765/coordinate_visual_finding.json'),
              Path('work/analysis/tavern_conversations_v765/layout_findings.json')]
    for path in paths: copy(path, ARCHIVE / path.as_posix())
    save(ARCHIVE / 'provenance.json', {'files': {p.relative_to(ARCHIVE).as_posix(): sha(p.read_bytes()) for p in ARCHIVE.rglob('*') if p.is_file()},
        'research_complete_registered_release_and_revised_actual_scenes_pending': True})
    for path, digest in read(ARCHIVE / 'provenance.json')['files'].items(): assert sha((ARCHIVE / path).read_bytes()) == digest
    print('V766 full native research hash-archived on E;goal active;no ROM or editorial-completion credit yet.', flush=True)


if __name__ == '__main__': main()
