"""Record bounded native formatting progress without a ROM completion claim."""

from copy import deepcopy
from pathlib import Path
from shutil import copy2

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts import refit_dialogue_runtime_v833 as runtime
from scripts.review_refit_dialogue_v832 import MANUSCRIPT as DRAFT
from scripts.verify_village_wrap_v608 import read, save

ROOT = runtime.ROOT
PRODUCTION = Path('translations/refit_dialogue_editorial_manuscript_v2.json')
LEDGER = Path('translations/editorial_review_current_v1.json')
DOC = Path('docs/refit_dialogue_v833_runtime.md')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V833 Refit dialogue bounded runtime and layouts')


def main():
    assert not PRODUCTION.exists() and not DOC.exists()
    proof = read(ROOT / 'native_runtime_verification.json')
    fonts = read(ROOT / 'native_font_proof.json')
    matrix = read(ROOT / 'native_layout_matrix.json')
    target = (ROOT / 'ARM9_RESEARCH_ONLY.bin').read_bytes()
    assert proof['research_ARM9_sha256'] == fonts['ARM9_sha256'] == matrix['ARM9_sha256'] == sha(target)
    assert proof['runtime_sha256'] == sha(Path(runtime.__file__).read_bytes())
    assert proof['verifier_sha256'] == sha(Path('scripts/verify_refit_runtime_v833.py').read_bytes())
    assert fonts['matrix_case_count'] == matrix['count'] == 525 and not fonts['findings']
    assert len(fonts['complete_native_font_planes']) == 26 and len(fonts['review_sheets']) == 4
    assert fonts['manuscript_sha256'] == matrix['manuscript_sha256'] == sha(DRAFT.read_bytes())
    for sheet in fonts['review_sheets']:
        assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
    fonts.update(visual_review_pending=False, visual_review={
        'all_four_complete_sheets_opened': True,
        'all12_records_and26_complete_native_glyph_planes_reviewed': True,
        'consistent_left_origins_complete_first_final_letters_and_all_words': True,
        'all256_day_values_include_1_day_and_plural_days': True,
        'zero_stranded_word_or_weak_end_findings': True,
        'extreme_percent_values_are_bounds_controls_not_claimed_game_outcomes': True,
        'controlled_fonts_not_actual_new_gameplay_captures': True})
    save(ROOT / 'native_font_proof.json', fonts)
    manuscript = read(DRAFT)
    manuscript.update(status='native-format-reviewed-registered-integration-and-actual-scenes-pending',
                      reviewed_research_manuscript=str(DRAFT),
                      reviewed_research_manuscript_sha256=sha(DRAFT.read_bytes()),
                      native_runtime_proof=str(ROOT / 'native_runtime_verification.json'),
                      native_runtime_proof_sha256=sha((ROOT / 'native_runtime_verification.json').read_bytes()),
                      native_font_proof=str(ROOT / 'native_font_proof.json'),
                      native_font_proof_sha256=sha((ROOT / 'native_font_proof.json').read_bytes()))
    manuscript['layout_authoring'] = 'One natural paragraph. Current exact queued/direct native consumers and525 printf/quantity/layout cases verified;26 complete font planes visually reviewed. Registered integration and revised gameplay scene samples remain separate gates.'
    for row in manuscript['records']:
        row['review']['formatting'] = True
        if row['message_id'] == 1267:
            row['argument_contract'] = 'Original full-width duration number plus grammatically singular/plural day unit,through only source return02017B90;all256 native byte values verified.'
            row['localization_note'] = row['localization_note'].replace('REQUIRED PENDING:', 'Verified:').replace(
                'all256 source duration bytes are mapped and the unit/runtime gate remains pending.',
                'all256 source duration bytes now receive the correct unit in the bounded native prototype. Registered integration and actual completion scenes remain pending.')
    validate_natural_dialogue_batch(manuscript)
    save(PRODUCTION, manuscript)
    save(ROOT / 'research_corrections.json', {
        'initial_rejected_encoding': 'Different numeric/pointer biases broke special coordinate routing at842;native scope rejected it before any ROM build. Archive:work/analysis/refit_dialogue_v833_initial_encoding.',
        'final_encoding': 'Universal384 bias after the original pointer normalization preserves all relative coordinate/status keys;40,056 native routing and ABI cases pass against exact source sets.',
        'scratch_thunk_cache_correction': 'Use fresh machines when the baseline direct branch changes from the old quantity helper to the original bare-number getter. This avoids a cached translated branch target;77 old and256 new results pass.',
        'bank_verifier_extent_correction': 'Check the separate168/216-byte banks,not the intervening address gap. Actual patches never borrowed that gap.',
        'layout_probe_guard_correction': 'The16-byte suffix guard follows a256-byte body,at+256 rather than+272.',
        'raster_budget_correction': 'Long complete font paints need the established2,000,000-instruction allowance. Early100,000 limit was not a completed native call.',
        'no_failed_probe_counted_as_a_final_pass': True,
        'no_ROM_built_modified_or_promoted': True})
    ledger = read(LEDGER)
    save(ROOT / 'ledger_before_V833.json', ledger)
    assert ledger['records_editorially_completed'] == 634 and ledger['records_with_source_and_prose_pass'] == 649
    entry = {
        'documentation': str(DOC), 'manuscript': str(PRODUCTION), 'manuscript_sha256': sha(PRODUCTION.read_bytes()),
        'research_runtime': str(ROOT / 'ARM9_RESEARCH_ONLY.bin'), 'research_runtime_sha256': sha(target),
        'native_runtime_proof': str(ROOT / 'native_runtime_verification.json'),
        'native_font_proof': str(ROOT / 'native_font_proof.json'),
        'native_scope_cases_per_current_and_prototype': 40056, 'modal_output_equivalence_cases': 3668,
        'old_quantity_cases': 77, 'new_duration_byte_cases': 256, 'status_contract_cases': 140,
        'native_layout_cases': 525, 'complete_font_planes_visually_reviewed': 26,
        'status': '12-source-prose-and-native-format-reviewed-registered-integration-and-actual-scenes-pending',
        'unchanged_integrated_candidate': deepcopy(ledger['current_integrated_candidate']),
        'remaining_gates': ['Source-locked COMMON repack retaining all unselected strings/opaque payloads and cache bounds',
                            'Registered combined ROM,manifest and exact clean-input patch',
                            'Actual revised companion offer/discount/duration and Rename scenes,entry/exit and startup regressions'],
        'no_completed_entry_credit': True, 'full_goal_complete': False}
    ledger['refit_dialogue_v833'] = entry
    ledger['research_checkpoints'].append({'id': 'V833-bounded-Refit-runtime-and-native-fonts', **entry})
    ledger['active_source_prose_drafts']['manuscripts'] = [
        'work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json', str(PRODUCTION)]
    ledger['active_source_prose_drafts']['status'] = 'three-older-context-unmapped-and12-Refit-integration-actual-scenes-pending'
    ledger['refit_dialogue_v832']['superseded_native_format_review'] = str(PRODUCTION)
    for finding in ledger['findings']:
        if finding['id'] == 'COMMON1256-1267-Refit-source-voice-units-and-prose':
            finding.update(status=entry['status'], native_format_review=str(ROOT / 'native_font_proof.json'))
    ledger['latest_runtime_research_before_V833'] = deepcopy(ledger.get('latest_runtime_research'))
    ledger['latest_runtime_research'] = entry
    ledger['latest_checkpoint'] = (
        'V833 verifies bounded formatting for12 Refit dialogue drafts without a new ROM. '
        'Lossless exact-member table compaction174->176 bytes is funded by the ceremony filter14->12 while its ITCM wrapper remains128;gate164,quantity104,sections/BSS/cache and123040 staged bytes stay fixed. '
        'Both current/prototype40,056 selector/ABI cases,all3668 complete modal outputs,77 earlier quantity cases,all256 new duration values,140 status contracts and eight-caller reference closure pass. '
        'All525 native quantity/printf/paragraph cases and26 independent full glyph planes pass;four sheets are visually reviewed with no wrapping findings. '
        'A v2 manuscript now has all individual native-format gates approved,including1 day/plural days. '
        'Registered COMMON/ROM/patch integration and actual revised helper/discount/duration/Rename samples remain. Current V831 is unchanged;634 completed,649 source/prose reviewed,15 reviewed drafts pending,not the full remaining scope. '
        'All remaining shared/route/player prose,raw coverage and separate graphics/all18 plaques remain open;goal active.')
    save(LEDGER, ledger)
    DOC.write_text('''# V833: bounded Refit dialogue runtime and native layouts

The12 source-reviewed Refit dialogue drafts now have complete controlled native
formatting coverage. The v2 manuscript has all five individual editorial gates;
it is not yet integrated into a registered ROM or claimed gameplay-verified.

## Current source and owned footprints

Source is combined V831 ARM9 SHA256
278028874ab612693246fc816f5a44d420648ab0c6992009702b443baa0d9be7.
The actual latest table is the ceremony-era174-byte table, superseding the
older Inn142/144-byte capacity note from V832. No earlier runtime is restored.

New exact memberships are direct parent02054014 IDs1263-1267 and queued
parent02053DB8 table02118680 only. A10-bit low key/6-bit run-length codec with
a universal384 bias encodes every old and new member exactly. Relative
coordinate/status comparisons retain the same normalized IDs. The table grows
174->176 inside the original allocation, funded by moving one normalization
instruction from the ceremony filter14->12 into its existing128-byte wrapper.
Selecting its wrap function directly preserves all previous outputs and keeps
the wrapper128 bytes;the gate remains164 and quantity helper104. Original384
source-owned data/code bytes, sections, BSS, caches and123040 staged bytes do
not grow. All declared patches reverse to the exact source ARM9.

The compact quantity helper remains private to eight proven BL callers: the
earlier six prices and one day caller plus original refit return02017B90. Only
that BL is added to the external reference census. Its bit classification is
valid only for these exact source-locked callers;it is not a public LR-to-unit
API. Earlier full-width numbers/gold coin/coins/day/days stay exact. New refit
durations0-255 preserve the original numeric buffer and choose1 day/plural days.

## Evidence

-40,056 native exact parent/ID/queued-pointer/stride/ABI cases for both current
 and prototype,with every prior member retained and only the declared additions.
-All3668 complete modal outputs and wrong-parent/edge controls equal V831.
-77 earlier quantity cases and256 new duration-byte values pass native outputs,
 original128-byte numeric-buffer bounds,write contracts and saved-register ABI.
-All140 complete status phrase/memory/ABI cases pass after index relocation.
-Private-reference census across resident sections,overlays and ARM7 preserves
 every earlier incoming reference and finds only the declared eighth numeric BL.
-All525 native number/unit,printf and exact-consumer paragraph cases preserve
 every word,guard and width. They include all256 duration values,percentage
 width/format controls and all ten static paragraphs.
-26 complete native228x64 glyph planes match independent font masks,cover all12
 records,generated geometries and decimal glyphs. Four sheets were opened and
 visually reviewed:complete leading/trailing letters,consistent alignment,no
 clipping,no single-word tails or weak-line-end findings. Large percentage
 examples are deliberate bounds controls,not possible game discounts promised
 by the translation. These previews are not actual gameplay screenshots.

The rejected initial encoding misrouted842 and is archived. A cached scratch
branch target in the baseline numeric probe required fresh machines when switching
to the bare-number getter. Bank-extent and guard-coordinate probe assumptions
were corrected. Longer glyph paints required the established2M instruction
allowance. Failed/incomplete probes are retained and receive no completion credit.

## Remaining work

Source-locked COMMON repack;registered combined build/manifest;exact clean-input
patch;actual revised companion offer,discount,duration and Rename scenes;normal
entry/exit/startup regression. V831 remains current and no ROM was modified or
promoted.634 completed entries and649 source/prose reviews remain;15 reviewed
drafts await work. Those are not all remaining shared/route/player prose. The
raw-source revisit and separate graphics/all18-plaque audit remain unfinished.
''', encoding='utf-8')
    paragraph = '\n\n## V833: Refit dialogue bounded runtime and native fonts\n\n' + ledger['latest_checkpoint'] + ' See [V833 evidence](refit_dialogue_v833_runtime.md).\n'
    for path in ('docs/translation_progress.md', 'docs/editorial_review_goal.md', 'docs/todo.md'):
        with Path(path).open('a', encoding='utf-8') as handle:
            handle.write(paragraph)
    sources = [Path(__file__), Path(runtime.__file__), PRODUCTION, DOC, LEDGER,
               Path('scripts/verify_refit_runtime_v833.py'), Path('scripts/probe_refit_dialogue_layout_v833.py'),
               *map(Path, ('docs/translation_progress.md', 'docs/editorial_review_goal.md', 'docs/todo.md')),
               *ROOT.glob('*.json'), *ROOT.glob('*.png'), *ROOT.glob('*.bin'),
               *ROOT.glob('*_scope/*.json'), *ROOT.glob('native_font_previews/*.png')]
    save(ROOT / 'source_program_manifest.json', {str(p): sha(p.read_bytes()) for p in sources})
    sources.append(ROOT / 'source_program_manifest.json')
    copies = []
    for source in sources:
        target_path = ARCHIVE / source.absolute().relative_to(Path.cwd())
        target_path.parent.mkdir(parents=True, exist_ok=True)
        copy2(source, target_path)
        assert sha(source.read_bytes()) == sha(target_path.read_bytes())
        copies.append({'source': str(source), 'archive': str(target_path), 'sha256': sha(target_path.read_bytes())})
    save(ROOT / 'archive_manifest.json', {'archive': str(ARCHIVE), 'files': copies, 'all_copies_hash_verified': True,
                                         'native_previews_not_guide_promoted': True,
                                         'previous_goal_turn_classification': 'progress:V832 source/prose/native context and actual Rename exploration',
                                         'this_goal_turn_classification': 'progress:bounded runtime,full inherited scope/modal/unit/status preservation,and12-paragraph native font approval'})
    copy2(ROOT / 'archive_manifest.json', ARCHIVE / 'archive_manifest.json')
    print('V833 recorded:12 native-format-approved drafts;634 completed unchanged;V831 current;E archive verified;goal active.', flush=True)


if __name__ == '__main__':
    main()
