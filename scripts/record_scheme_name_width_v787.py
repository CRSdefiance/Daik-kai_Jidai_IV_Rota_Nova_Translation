"""Record the shared scheme-name width repair as native research,not a release."""

import shutil
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.native_machine_scoped_v764 import machine
from scripts.prepare_product_pitches_v747 import native_layout
from scripts.research_scheme_name_width_v787 import ROOT, PRIOR, CURRENT, WIDTH
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/scheme_name_width_v787_research.md')
LEDGER = Path('translations/editorial_review_current_v1.json')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V787 Shared letter-name width research')
SUMMARY = (
    'V787 identifies the shared scheme-name width method as an original10-cell Japanese maximum. '
    'A source-guarded single-instruction research repair reports24 cells for the23-character '
    'English maximum plus its four-bit paired blank cell. Six native geometry cases,40 original '
    'single-line row renders,ten whole8MiB/ABI getter cases and all six ordinary selector entry '
    'edges pass;four external callers and two wrappers use automatic width. All ten names retain '
    'complete native glyphs;old width crops six proposed names and earlier Forge Papers. '
    'An initial dialogue-wrap probe error is separated from an odd-pitch first-glyph sensitivity. '
    'All3668 COMMON mappings and repaired676/677 remain exact. Full SDK window/GPU playback, '
    'remaining consumers/diplomacy eligibility,production prose integration and exact patch remain. '
    'V783 current;417 complete,496 source/prose,79 drafts;full editorial/graphics goals unfinished.'
)


def main():
    proof = read(ROOT/'native_width_verification.json')
    entries = read(ROOT/'selector_entry_closure.json')
    arm = (ROOT/'WIDTH_RESEARCH_ONLY.bin').read_bytes()
    source = (PRIOR/'NOMINAL_PROVIDER_RESEARCH_ONLY.bin').read_bytes()
    assert sha(arm) == proof['target_ARM9_sha256'] == entries['research_ARM9_sha256']
    assert sha(source) == proof['source_ARM9_sha256']
    assert proof['producer_sha256'] == sha(Path('scripts/research_scheme_name_width_v787.py').read_bytes())
    assert entries['producer_sha256'] == sha(Path('scripts/verify_scheme_selector_entries_v787.py').read_bytes())
    assert len(proof['all40_original_list_row_bitmap_cases']) == 40
    positives = [r for r in proof['all40_original_list_row_bitmap_cases'] if r['widened']]
    assert len(positives) == 20 and all(r['complete_native_row_and_independent_font_exact'] for r in positives)
    assert proof['reported_name_width_cells'] == 24 and proof['paired_blank_terminal_cell_reserved'] == 1
    assert len(proof['all6_native_geometry_cases']) == 6
    assert len(entries['four_original_external_auto_width_fragments']) == 4
    assert len(entries['two_original_forwarding_wrappers']) == 2
    assert len(entries['ten_complete_width_getter_contracts']) == 10
    for row in proof['all40_original_list_row_bitmap_cases']+[proof['odd23_cell_minimal_backing_surface_sensitivity'],
            proof['initial_dialogue_wrap_setting_was_probe_error_not_a23_cell_game_defect']]:
        assert sha(Path(row['PNG']).read_bytes()) == row['PNG_sha256']
    odd = proof['odd23_cell_minimal_backing_surface_sensitivity']
    image = Image.open(odd['PNG']).convert('L')
    font = GameAsciiFont.from_arm9(arm)
    expected = set()
    for n, char in enumerate(odd['text']):
        glyph = font.decode(char)
        expected.update((n*6+x, y) for y in range(11) for x in range(6) if glyph.getpixel((x, y)))
    actual = {(x, y) for y in range(image.height) for x in range(image.width) if image.getpixel((x, y)) < 128}
    lost, extra = sorted(expected-actual), sorted(actual-expected)
    assert len(lost) == 13 and not extra and all(x < 6 for x, y in lost)
    save(ROOT/'odd_pitch_diagnostic.json', {'input': odd, 'lost_ink_pixels': lost, 'extra_ink_pixels': extra,
        'all_lost_ink_in_first_letter_p': True, 'all23_source_bytes_consumed_despite_lost_ink': True,
        'controlled_minimal_backing_surface_not_a_captured_GPU_menu': True,
        'matches_documented_four_bit_spare_terminal_halfcell_behavior': 'docs/guild_diplomacy_v340.md',
        'single_line24_cell_rows_have_no_lost_or_extra_ink': True})
    save(ROOT/'visual_review.json', {'sheet': str(ROOT/'old_and_corrected_name_rows_3x.png'),
        'sheet_sha256': sha((ROOT/'old_and_corrected_name_rows_3x.png').read_bytes()),
        'all10_corrected_names_and_source_truncation_controls_visually_reviewed': True,
        'complete_first_and_last_letters_and_blank_terminal_cell': True,
        'left_column_is_proposed_English_in_old_width_not_historical_ROM_screenshots': True,
        'native_CPU_bitmap_evidence_not_gameplay_or_guide': True})

    restored = bytearray(arm)
    restored[WIDTH-0x02000000:WIDTH-0x02000000+4] = source[WIDTH-0x02000000:WIDTH-0x02000000+4]
    assert bytes(restored) == source
    before, after = [MainCodeFile(value, 0x02000000) for value in (source, arm)]
    assert [(s.ramAddress, len(s.data), s.bssSize) for s in before.sections] == [
        (s.ramAddress, len(s.data), s.bssSize) for s in after.sections]
    assert bytes(after.save()) == arm and cache_plan(arm) == cache_plan(source)
    rom = NdsImage.open(CURRENT)
    common, original_arm = rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin')
    a, b = [common_message_entries(common, value, clean=False) for value in (original_arm, arm)]
    assert len(a) == len(b) == 3668
    assert all((x.block, x.block_offset, x.copy_end, x.text) == (y.block, y.block_offset, y.copy_end, y.text)
               for x, y in zip(a, b))
    cpu = machine(arm)
    cpu.mem_write(0x02387A20, bytes(after.sections[3].data[:-48]))
    old_watch = read('work/analysis/dialogue_formatting_user_recheck_v782/COMMON676_677.json')
    cases = []
    for row in old_watch['entries']:
        formatted, lines = native_layout(cpu, b[row['id']].text, row['id'], ())
        assert lines == row['lines'] and formatted.hex() == row['native_formatted_hex']
        cases.append({'id': row['id'], 'lines': lines, 'native_formatted_hex': formatted.hex()})
    save(ROOT/'prose_and_geometry_preserved.json', {'one_existing_source_guarded_instruction_only': True,
        'all3668_COMMON_maps_texts_and_copy_extents_exact': True, 'repaired676_677_native_wrap': cases,
        'all_section_BSS_staged_payload_cache_startup_and_arena_geometry_exact': True,
        'source_ARM9_sha256': sha(source), 'target_ARM9_sha256': sha(arm),
        'no_ROM_or_new_actual_shop_scene_claim': True})
    protected = dict(read(PRIOR/'checkpoint.json')['protected_files_unchanged'])
    for name, expected_sha in protected.items():
        assert sha(Path(name).read_bytes()) == expected_sha, name
    cfg = read('translations/shared_dialogue_editorial_release_v2.json')
    for name, expected_sha in cfg['dependencies'].items():
        assert sha(Path(name).read_bytes()) == expected_sha, name

    DOC.write_text('''# V787: shared scheme-name width and complete native rows

## Status

This is native research for the pending item/diplomacy batch, not a new playable
ROM or production prose approval. V783 remains current. Editorial coverage stays
417 completed,496 source/prose reviewed and79 drafts. All76 pending paragraphs,
wider shared/route/prose review and the separate graphics audit remain unfinished.

## Shared formatting defect and repair

The original CScheme name-width method at0209145C returns10 cells. Its sole
reference is CScheme's vtable field0214C624. The generic selector calls this
method at0204F10C and multiplies its result by6 to size the text area. Original
Japanese scheme labels used an even byte-width bound. The current English
Forge Papers already has12 ASCII cells; the proposed full nominal names reach23.

The research repair changes one existing ARM instruction from `mov r0,#10` to
`mov r0,#24`. It keeps the return instruction and every other byte unchanged.
The24-cell bound includes the23-character maximum and its paired blank cell;
it does not shorten,scale or change the names. The four-bit SDK clears a spare
terminal halfcell for odd text,as documented in the earlier V340 source/font work.
Putting that cell inside the declared field avoids relying on undeclared backing padding.

Parent research ARM9:
`44f4e07420034aad87d837bf9b5be4066ac5bdeec5f2dea2b8141d8e5be4f6c8`.
Corrected research ARM9:
`23fb7c8ffb3055b71c1d41b41756ad1b0b0903c25e3854ca27306cdfe218d6f7`.
No section,BSS,pool,cache,startup,arena or123040-byte staged payload grows.
The getter is not shared by another class; other object types are byte-exact.

## Original native paths tested

- The source object resolver020211E4 handles encoded scheme IDs through its
  original CB130 pool. The CPU fixture changes only a source slot's type byte;
  no real letter,quest or save is created.
- The original4F500 constructor initializes the outer widget and its child.
  The tested row callback uses the correct child at outer+10 and its original
  vtable8C entry4F8D4. The default4FB38 path calls the original name getter and
  D5404 font renderer. No invented vtable or replacement glyph renderer is used.
- Six original sizing-prefix cases cover old/new widths and counts1,10,11.
  The original ten-row cap remains. Corrected outer rectangles stay within
  256×192;content width is144. The original inner-rectangle arithmetic fragment
  uses that same width. SDK window allocation is deliberately outside this proof.
- Forty complete native bitmap cases cover all ten names at heights12 and16.
  Every corrected row matches the independent font,including first/last letters
  and the empty terminal cell. Bitmap/header/view guards pass. The old60-pixel
  field truncates the six proposed names and earlier Forge Papers in these CPU tests.
- Ten width-getter cases preserve the complete8MiB memory and callee-saved ABI.

This does not establish actual GUI allocation,palette/compositing,full menu
playback,earned letters or every possible runtime control flow.

## Mode and backing-surface diagnostics

The first probe reused a dialogue test's wrap flag1. Source4FC70 creates the
list context through D5160,which initializes wrap0,and then invokes virtual8C
without changing that flag. The final tests use that exact single-line setup.
The wrong-mode result is retained separately;it is not a shipped23-cell game defect.

Separately,a controlled23-cell view backed by a tightly sized140-pixel bitmap
consumes all23 bytes but loses13 ink pixels from the first `p` of the next
bitmap row. The paired terminal clear crosses the tight pitch. The corrected
24-cell/144-pixel field preserves the entire plane. This is a native backing-
surface sensitivity test,not a claim about a captured GPU menu's allocator.
It demonstrates why byte counts alone do not prove complete leading letters.

The final comparison sheet shows proposed English in the old-width CPU field
beside the corrected native rows. Its left column is not a set of historical
ROM screenshots. All ten corrected rows are visually reviewed.

## Constructor entry scope

The clean/current census finds six original constructor edges and no additional
absolute,ARM/ADR or Thumb reference lead to these three selector entrypoints.
Four external caller fragments explicitly set width override0;two original
wrappers forward it unchanged. Thus the ordinary discovered static entries use
automatic class width. Native source fragments and stack parameters are recorded,
not merely inferred from a call graph. This is ordinary static-entry closure,
not a proof against every imaginable indirect jump or corrupted program state.

## Preservation and remaining work

Restoring the one instruction reproduces the complete V786 research ARM9.
All3668 current COMMON maps,texts and copy extents stay exact. The user's
repaired676/677 reproduce their exact native wrapping;V747 remains their actual
shop-scene reference. Existing V783 ROM/patch,canonical,clean input,donors and
frozen release dependencies remain exact. No new guide screenshot,commit or push.

Full SDK window construction and actual selector/GPU crops remain to verify in
the registered candidate. The full native initializer reached an unmodeled
allocation/copy dependency;no heap or GPU stub was introduced to claim success.
The live CPU test preserves captured storage and applies only declared guarded
deltas,instead of reloading staging data over the live snapshot.

Continue other name consumers and Guild diplomacy eligibility/argument mapping,
then production routing,COMMON reblocking/copies,registered full-stack integration,
exact clean-input patch and actual revised buy/sell/bargain/diplomacy scenes plus
startup. Then1146 onward,750–752,all routes and remaining prose. The original18
plaques,Online-body exclusion,preserved brown marks,locked character names and
older-record follow-up remain unchanged in the separate unfinished graphics audit.

## Evidence

`work/analysis/scheme_name_width_v787/native_width_verification.json` and
`selector_entry_closure.json` carry the source/code/input contracts.
`odd_pitch_diagnostic.json` records every missing ink coordinate.
`old_and_corrected_name_rows_3x.png` is the reviewed native CPU comparison.
Reproduce with research_scheme_name_width_v787.py,
verify_scheme_selector_entries_v787.py and record_scheme_name_width_v787.py.
Current evidence and producers are archived with SHA-256 receipts at
`E:/Rota Nova translations/Editorial review/V787 Shared letter-name width research`.
''', encoding='utf-8')

    ledger = read(LEDGER)
    assert ledger['records_editorially_completed'] == 417 and ledger['records_with_source_and_prose_pass'] == 496
    assert len(ledger['active_source_prose_drafts']['native_message_IDs']) == 79
    if not (ROOT/'editorial_ledger_before_v787.json').exists():
        save(ROOT/'editorial_ledger_before_v787.json', ledger)
    ledger['latest_checkpoint'] = SUMMARY
    ledger['scheme_name_width_finding'] = {'status': 'corrected-native-research;registered-ROM-and-actual-selector-pending',
        'source_width_method': WIDTH, 'old_cells': 10, 'new_cells': 24,
        'maximum_name_cells': 23, 'spare_paired_cell': 1, 'documentation': str(DOC),
        'native_proof': str(ROOT/'native_width_verification.json'),
        'ordinary_selector_entries': str(ROOT/'selector_entry_closure.json'),
        'no_editorial_completion_credit': True}
    ledger['formatting_watchlist']['latest_research_reference_proof'] = str(ROOT/'prose_and_geometry_preserved.json')
    ledger['coverage_units'][0]['next'] = (
        'Verify full scheme selector construction/actual GPU crops and remaining name consumers; '
        'finish Guild diplomacy eligibility/arguments,production dispatch/COMMON copies,registered76-entry ROM/exact patch '
        'and revised buy/sell/bargain/diplomatic plus startup scenes. Shared name-width24 repair and ordinary auto-width '
        'entry scope now native-tested. Then1146 onward,750-752,all routes/other prose;graphics audit and older-record follow-up open.')
    save(LEDGER, ledger)
    latest = read('out/editorial_review_latest.json')
    assert latest['sha256'] == sha(CURRENT.read_bytes()) and latest['profile'] == 'all-routes-unified-v783'
    latest['latest_research_checkpoint'] = str(DOC)
    save('out/editorial_review_latest.json', latest)
    for name in ('docs/known_issues.md', 'docs/todo.md', 'docs/translation_progress.md', 'docs/editorial_review_goal.md'):
        path = Path(name)
        text = path.read_text(encoding='utf-8')
        heading = '## V787: shared scheme-name width and native row bounds'
        if heading not in text:
            path.write_text(text+'\n\n'+heading+'\n\n'+SUMMARY+
                ' See [V787 research](scheme_name_width_v787_research.md).\n', encoding='utf-8')
    proofs = {str(p): sha(p.read_bytes()) for p in ROOT.glob('*.json')
              if p.name not in ('checkpoint.json', 'archive_receipt.json')}
    save(ROOT/'checkpoint.json', {'id': 'V787-shared-scheme-name-width-native-research', 'documentation': str(DOC),
        'current_candidate': latest, 'research_ARM9_sha256': sha(arm), 'proofs': proofs,
        'protected_files_unchanged': protected, 'completed_records': 417, 'source_prose_reviews': 496, 'drafts': 79,
        'previous_goal_turn_classification': 'progress:V786 native names,layouts and actual Guild context',
        'this_turn_classification': 'progress:shared width defect,complete native repair and ordinary selector entry closure',
        'new_editorial_completion_credit': 0, 'new_playable_ROM_or_patch': False,
        'full_goal_complete': False, 'graphics_audit_separate_and_unfinished': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'summary': SUMMARY})
    # Archive the authoritative current cases. Earlier unreferenced WIP PNGs
    # remain in Generated/work,not in this reviewed comparison receipt.
    sources = [p for p in ROOT.glob('*.json') if p.name != 'archive_receipt.json']
    sources += [ROOT/'WIDTH_RESEARCH_ONLY.bin', ROOT/'old_and_corrected_name_rows_3x.png']
    sources += [Path(row['PNG']) for row in proof['all40_original_list_row_bitmap_cases']]
    sources += [Path(proof[key]['PNG']) for key in ('odd23_cell_minimal_backing_surface_sensitivity',
        'initial_dialogue_wrap_setting_was_probe_error_not_a23_cell_game_defect')]
    sources += [Path('scripts/research_scheme_name_width_v787.py'), Path('scripts/verify_scheme_selector_entries_v787.py'),
        Path(__file__), DOC, LEDGER]
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    copies = []
    for src in sources:
        destination = ARCHIVE/(src.relative_to(Path.cwd()) if src.is_absolute() else src)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, destination)
        digest = sha(src.read_bytes())
        assert sha(destination.read_bytes()) == digest
        copies.append({'source': str(src), 'copy': str(destination), 'sha256': digest})
    receipt = {'archive': str(ARCHIVE), 'copies': copies, 'all_copies_SHA256_exact': True,
        'native_research_only_not_GPU_menu_or_guide': True}
    save(ROOT/'archive_receipt.json', receipt)
    save(ARCHIVE/'archive_receipt.json', receipt)
    print(f'V787 shared width research recorded and{len(copies)} artifacts archived. V783 remains current;417 complete/79 drafts;goal active.', flush=True)


if __name__ == '__main__':
    main()
