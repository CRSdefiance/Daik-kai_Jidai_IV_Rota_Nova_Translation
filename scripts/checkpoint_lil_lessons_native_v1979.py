"""Bind59 unchanged lesson targets andfour labels; review one new native plane."""
from copy import deepcopy
from dataclasses import replace
import os
from pathlib import Path
from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_lessons_native_checkpoint_v1979')
DOC = Path('translations/lil_lessons_editorial_manuscript_v6.json')
MENU = Path('translations/lil_lesson_choices_editorial_draft_v3.json')
OLD = Path('translations/lil_lessons_final_review_v1.json')
OLD_FONT = Path('work/analysis/lil_Deck_label_approval_v1758/all60_current_native_font_reconciliation.json')
OLD_FE = Path('work/analysis/lil_Deck_label_approval_v1758/all9_current_FE_reconciliation.json')
NEW_FONT = Path('work/analysis/lil_Lookout_affiliation_fonts_v1978/one_changed_native_macros_and_complete_font_plane.json')
LEDGER = Path('translations/editorial_review_current_v1.json')
HANDOFF = Path('docs/editorial_handoff_current.md')
CHANGED = 'DK4_MES_B23_R0142'

if __name__ == '__main__':
    assert not ROOT.exists()
    doc, menu, old, old_font, old_fe, new_font = map(read,(DOC,MENU,OLD,OLD_FONT,OLD_FE,NEW_FONT))
    assert sha(DOC.read_bytes()) == new_font['manuscript_sha256']
    assert len(new_font['cases']) == 1 and new_font['cases'][0]['id'] == CHANGED
    assert not new_font['failures'] and new_font['native_macro_calls'] == 8
    new_case = new_font['cases'][0]
    assert new_case['whole_native_independent_font_plane_exact']
    assert new_case['all_glyphs_complete_in_order_unique_cells_within216x64']
    assert new_case['all_continuation_visible_origins_equal_first_row_zero']
    assert not new_case['diagnostics']
    assert sha(Path(new_case['preview']).read_bytes()) == new_case['preview_sha256']
    for sheet in new_font['review_sheets']:
        assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
    im, previous = map(NdsImage.open,(doc['current_ROM'],old['candidate']))
    arm = im.read_file('/__arm9__.bin')
    assert arm == previous.read_file('/__arm9__.bin')
    blocks, before = (IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks for image in (im,previous))
    assert all(blocks[n] == before[n] for n in (120,23))
    assert sha(arm) == old_font['ARM9_sha256'] == new_font['ARM9_sha256']
    for path,expected in old['proofs'].items(): assert sha(Path(path).read_bytes()) == expected,path
    assert old_fe['all9_reviewed_FE_full_actual_context_native_planes_pass']
    assert old_fe['all9_complete_targets_fit_one_native_page_inside228x48']
    old_cases = {r['id']:r for r in old_font['cases']}
    fe_cases = {r['id']:r for r in old_fe['reviewed_cases']}
    assert len(old_cases) == 60 and len(fe_cases) == 9
    old_rows = {r['id']:r for r in old['records']}
    base = get_dialogue_profile('lil-opening-editorial-native-v1')
    # This local FE planning isolate is source-bound to the two already proven
    # exact blocks/runtime above. Complete display is inherited from the separate
    # mode1 paper proof, never from this conservative paragraph planner.
    fe_profile = replace(base,name='source-bound-unchanged-lessons-FE-planning-only',leading_speaker_bytes=frozenset({254}))
    cases, inherited = [], []
    for row in doc['records']:
        source = bytes.fromhex(row['source_hex'])
        current = bytes.fromhex(row['current_text_hex'])
        at = row['current_reference']['offset']
        assert blocks[row['block']][at:at+len(current)] == current
        english = row['english'].removesuffix('{PAD}')
        profile = fe_profile if source[:1] == b'\xfe' else base
        encoded = encode_relocatable_dialogue(source,english,profile).encoded
        if row['id'] == CHANGED:
            assert encoded.hex() == new_case['encoded_hex']
            cases.append({**deepcopy(new_case),'consumer':'original_progressive_54020',
                'new_native_and_independent_plane_and8_alignment_calls':True,'new_review_sheet_actually_viewed':True})
            continue
        assert english == old_rows[row['id']]['english']
        assert encoded.hex() == old_cases[row['id']]['encoded_hex']
        assert current in (encoded,encoded+b' ')
        if source[:1] == b'\xfe':
            case = fe_cases[row['id']]
            assert case['target_hex'] == current.hex()
            assert case['one_native_page_consumes_complete_target']
            assert case['complete_first_last_letters_full_native_independent_plane_bounds_and_input_guards']
            assert sha(Path(case['logical_228x48_plane']).read_bytes()) == case['logical_plane_sha256']
            assert sha(Path(case['display_preview']).read_bytes()) == case['display_preview_sha256']
            case = {**deepcopy(case),'encoded_hex':encoded.hex(),'consumer':'original_FE_modal_5473C_mode1',
                'complete_mode1_native_plane_inherited_from_exact_unchanged_target':True}
        else:
            case = deepcopy(old_cases[row['id']])
            assert case['whole_native_and_independent_font_plane_exact']
            assert case['complete_printable_glyph_order_unique_cells_and_bounds_verified']
            assert sha(Path(case['preview']).read_bytes()) == case['preview_sha256']
        case.update(unchanged_exact_target_inherited_without_repeated_native_run=True,source_proof=str(OLD_FE if source[:1] == b'\xfe' else OLD_FONT))
        cases.append(case)
        inherited.append(row['id'])
    assert len(cases) == 60 and len(inherited) == 59
    assert sum(r['consumer'] == 'original_FE_modal_5473C_mode1' for r in cases) == 9
    assert sum(r['source_presentation_prefix_hex'] != 'fe' and r['id'] != CHANGED for r in doc['records']) == 50
    old_menu_path = Path(old['manuscripts'][1])
    old_menu = read(old_menu_path)
    for key in ('native_label_pointer_proof','original_choice_UI_proof','visual_review'):
        assert sha(Path(old_menu[key]).read_bytes()) == old_menu[key+'_sha256']
    assert len(menu['records']) == 4
    for row in menu['records']:
        prior = old_rows[row['id']]
        assert row['english'] == prior['english']
        assert row['current_reference'] == prior['current_reference']
        assert row['current_text_hex'] == prior['current_text_hex']
    ROOT.mkdir(parents=True)
    combined = ROOT/'all60_source_bound_native_font_inheritance.json'
    save(combined,dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),candidate=doc['current_ROM'],
        candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(arm),cases=cases,
        new_native_planes=1,new_macro_alignment_calls=8,new_plane_visual_review_complete=True,
        inherited_unchanged_progressive_planes=50,inherited_unchanged_separate_FE_mode1_planes=9,
        inherited_typed_choice_labels=4,no_repeated_equivalent_gameplay_or59_native_runs=True,
        exact_current_clean_source_packet=doc['source_context'],exact_source_packet_sha256=doc['source_context_sha256'],
        full_typed_reference_map_revised_sample_registered_integration_and_parity_still_pending=True,
        per_record_batch_formatting_gates_not_yet_promoted=True,
        evidence={str(p):sha(p.read_bytes()) for p in (DOC,MENU,OLD,OLD_FONT,OLD_FE,NEW_FONT,old_menu_path)},
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    raw = LEDGER.read_bytes()
    ledger = read(LEDGER)
    fresh = ledger['contextual_story_natural_dialogue_pass_v1871']
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release']) == (428,364,64)
    (ROOT/'ledger_before.json').write_bytes(raw)
    (ROOT/'handoff_before.md').write_bytes(HANDOFF.read_bytes())
    family = next(u for u in ledger['coverage_units'] if u['id'] == 'Lil-sailing-crew64-contextual-v1977')
    family.update(focused_native_font_proof=str(combined),focused_native_font_proof_sha256=sha(combined.read_bytes()),
        changed_Lookout_native_plane_and8_macro_cases_pass=True,unchanged59_targets_source_bound_font_inheritance_verified=True,
        four_labels_source_bound_native_UI_inheritance_verified=True,
        status='fresh-contextual-source-prose-and-focused-native-reviewed;typed-reference-parity-revised-integration-pending')
    fresh['pending_historical_reconciliations'][-1].update(focused_native_font_proof=str(combined),
        changed_native_plane_viewed=True,typed_reference_parity_revised_release_pending=True)
    ledger['next_route_scene_editorial_packet'] = dict(file_path='/data/SC2.DK4',blocks=[120,23],
        source_context=doc['source_context'],manuscript=str(DOC),choices=str(MENU),focused_native_font_proof=str(combined),
        current_parent=doc['current_ROM'],current_parent_sha256=doc['current_ROM_sha256'],changed_ID=CHANGED,
        next='Map current-source B23 native commands/relative spans around the one revised Lookout paragraph; prove parity pixels andall opaque bytes/inverse restoration. Use a focused revised Lookout/return sample with original controls,then registered successor andclean patch/startup. B120,59other targets andfourlabels are unchanged andsource-bound.',
        full_goal_complete=False)
    summary = ('V1979 lesson64 fresh revision native checkpoint:changed Lookout affiliation paragraph passes one complete216x64 native/independent plane and8 guarded macro/alignment calls;sheet viewed. '
        '50unchanged progressive targets,nineunchanged FE228x48 mode1 targets andfourtyped labels inherit exact source-bound proofs without repeated native/gameplay runs. '
        'Typed current-source B23relocation/relative spans,finalparity,revised representative display/return andregistered integration remainpending;draft formatting gates remainfalse. '
        'Fresh428reread/364integrated/64pending;historical1831 andsource/prose1947 unchanged. CurrentregisteredV1971/clean patch unchanged. '
        '116COMMON,broader all-routes/shared/town/random/playerprose,1467historical records needingreconciliation,graphics/all18plaques andlaterolder-record technical re-audit stayopen;fullgoalactive.')
    ledger['latest_checkpoint'] = summary
    ledger['research_checkpoints'].append(dict(id='V1979-lessons-focused-native',proof=str(ROOT/'checkpoint_receipt.json'),
        completed_entries_added=0,source_prose_reviews_added=0,new_native_planes=1,inherited_targets=59,full_goal_complete=False))
    pending = LEDGER.with_name('editorial_review_current_v1979_pending.json')
    assert not pending.exists() and LEDGER.read_bytes() == raw
    save(pending,ledger)
    os.replace(pending,LEDGER)
    text = HANDOFF.read_text(encoding='utf-8').replace('# Current editorial handoff - V1977','# Current editorial handoff - V1979',1)
    text = text.replace('No active reviewed-incomplete route drafts.116 COMMON andall broader story/shared/town/random/player prose remain.',
        '64-entry fresh historical lesson reconciliation remainsactive;global completion counts arehistorical.116 COMMON andall broader story/shared/town/random/player prose remain.')
    anchor = '## Active unit: earlier sailing/crew64 fresh contextual pass - V1977'
    chapter = ('## Current focused native checkpoint - V1979\n\n'+summary+'\n\n'
        f'- Proof:{combined.as_posix()};changedpreview:work/analysis/lil_Lookout_affiliation_fonts_v1978/DK4_MES_B23_R0142.png. Fullthree-row paragraph,first/last letters,allinternal glyphs,bounds,macro alignment guards andzero diagnostics pass.\n'
        '- ExistingFE proof usesreviewed_cases/target_hex(includingcompiler-owned trailing parity),not the progressive cases table. Allninecomplete FElogicalplanes/displaypreviews verified byhash andsource target bytes. Do notcollapse native548A8internal draw label into a progressive consumer;theouterconsumer is5473Cmode1.\n'
        '- Usecurrent V1971 B23asinput,withcleanrecord142/currentrecord141 distinct. Onechangedparagraph requires a newtypedmap;theoldB23map describes a different sourceversion. Focused revisedLookout sample canreuse original crew-final coldboot/input/16-byte Bruges fixture;no event/branch overrides. Newbatch/sourceproofs stayfrozen;emit successors.\n'
        '- Alltest/build jobs terminal. Frozenfailed opening1976 assumedwholeCOMMONequality;1976b provesonlysixlaterreinforcementmessage changes1911-1916,unchanged3668offset/copyspans andallother3662strings. No further source/control fault remainsfromthat assertion.\n\n')
    HANDOFF.write_text(text.replace(anchor,chapter+anchor),encoding='utf-8')
    Path('docs/lil_lessons_v1979_native_checkpoint.md').write_text('# V1979 lesson native checkpoint\n\n'+summary+'\n\nProof: '+combined.as_posix()+'\n',encoding='utf-8')
    for name in ('translation_progress.md','todo.md','editorial_review_goal.md'):
        with (Path('docs')/name).open('a',encoding='utf-8') as stream: stream.write('\n\n## V1979 lesson focused native checkpoint\n\n'+summary+'\n')
    save(ROOT/'checkpoint_receipt.json',dict(proof=str(combined),proof_sha256=sha(combined.read_bytes()),
        changed_native_planes=1,changed_macro_calls=8,inherited_unchanged_speech_targets=59,inherited_unchanged_labels=4,
        fresh_reread=428,fresh_integrated=364,fresh_pending=64,historical_completed=1831,registered_ROM_unchanged=True,
        ledger_sha256=sha(LEDGER.read_bytes()),handoff_sha256=sha(HANDOFF.read_bytes()),
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(changed_native_plane=1,new_macro_calls=8,inherited_progressive=50,inherited_FE=9,inherited_labels=4,
        typed_reference_revised_registered_integration_pending=True,full_goal_remains_active=True))
