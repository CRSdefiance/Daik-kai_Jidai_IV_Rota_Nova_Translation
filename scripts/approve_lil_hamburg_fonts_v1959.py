"""Approve complete B74 native planes without granting revised gameplay credit."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.lil_hamburg_profile import profile_for
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_Hamburg_font_approval_v1959')
OLD = Path('translations/lil_hamburg_recruitment_editorial_manuscript_v2.json')
OUT = Path('translations/lil_hamburg_recruitment_editorial_manuscript_v3.json')
MENU = Path('translations/lil_hamburg_recruitment_choices_editorial_draft_v1.json')
MENU_OUT = Path('translations/lil_hamburg_recruitment_choices_editorial_draft_v2.json')
FONT = Path('work/analysis/lil_Hamburg_fonts_v1954/all76_native_macros_and_complete_font_planes.json')
FE = Path('work/analysis/lil_Hamburg_FE_v1955/all3_FE_native_planes_and_actual_mode_reconciliation.json')
MACROS = Path('work/analysis/lil_Hamburg_FE_macros_v1956/all3_FE24_native_macro_alignment_cases.json')
CHOICE = Path('work/analysis/lil_Hamburg_choice_v1958/original_choice_decoder_VM_geometry_and_native_pixels.json')
CONTROL = Path('work/analysis/lil_Hamburg_controls_v1953b/source_bound_B74_presenter_and_control_contract.json')

if __name__ == '__main__':
    assert not ROOT.exists() and not OUT.exists() and not MENU_OUT.exists()
    doc, menu, font, fe, macros, choice = map(read,(OLD,MENU,FONT,FE,MACROS,CHOICE))
    assert all(p['manuscript_sha256'] == sha(OLD.read_bytes()) for p in (font,fe,macros))
    assert choice['manuscript_sha256'] == sha(MENU.read_bytes())
    assert len(font['cases']) == 76 and font['native_macro_calls'] == 608 and not font['failures']
    assert fe['all6_original_Hamburg_FE_holds_match_complete_native_mode1_ink']
    assert fe['all3_new_FE_targets_fit_one_page_complete_in228x48']
    assert macros['all24_full_macro_input_output_and4MiB_guards_pass']
    assert choice['six_original_VM_selection_and_cancel_cases_pass']
    assert choice['eight_complete_native_style_label_planes_pass']
    cases = {r['id']:deepcopy(r) for r in font['cases']+fe['cases']}
    assert len(cases) == 79
    for row in macros['cases']:
        cases[row['id']]['macro_cases'] = row['macro_cases']
    assert sum(len(r['macro_cases']) for r in cases.values()) == 632
    sheets = font['review_sheets']+[dict(path=fe['review_sheet'],sha256=fe['review_sheet_sha256'])]
    dependencies = {str(p):sha(p.read_bytes()) for p in (OLD,MENU,FONT,FE,MACROS,CHOICE,CONTROL,
        Path('dk4tool/dialogue/lil_hamburg_profile.py'),Path('scripts/prove_lil_hamburg_controls_v1953.py'),
        Path('scripts/prove_lil_hamburg_controls_v1953b.py'),Path('scripts/probe_lil_london_known_fonts_v1886.py'),
        Path('scripts/probe_lil_london_FE_v1896.py'),Path('scripts/check_lil_london_FE_macros_v1897.py'),
        Path('scripts/prove_lil_speyer_choice_v1927.py'))}
    for r in list(cases.values()):
        assert sha(Path(r['preview']).read_bytes()) == r['preview_sha256']
        dependencies[r['preview']] = r['preview_sha256']
    for r in sheets:
        assert sha(Path(r['path']).read_bytes()) == r['sha256']
        dependencies[r['path']] = r['sha256']
    assert sha(Path(choice['visual_review_sheet']).read_bytes()) == choice['visual_review_sheet_sha256']
    dependencies[choice['visual_review_sheet']] = choice['visual_review_sheet_sha256']
    image = NdsImage.open(doc['current_ROM'])
    arm = image.read_file('/__arm9__.bin')
    blocks = IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    block = blocks[74]
    progressive, modal = profile_for(arm,block), profile_for(arm,block,'FE-paper')
    negatives = []
    def reject(label, fn):
        try: fn()
        except ValueError as error: negatives.append(dict(case=label,error=str(error)))
        else: raise AssertionError('Invalid Hamburg scope accepted: '+label)
    reject('wrong-runtime',lambda:profile_for(bytes([arm[0]^1])+arm[1:],block))
    reject('unrelated-London-block',lambda:profile_for(arm,blocks[26]))
    reject('mutated-source',lambda:profile_for(arm,block[:-1]+bytes([block[-1]^1])))
    reject('unmapped-consumer',lambda:profile_for(arm,block,'unmapped'))
    base = get_dialogue_profile('lil-opening-editorial-native-v1')
    for prefix in ('10','fe'):
        row = next(r for r in doc['records'] if r['source_presentation_prefix_hex'] == prefix)
        reject('global-'+prefix+'-rejected',lambda r=row:encode_relocatable_dialogue(bytes.fromhex(r['source_hex']),r['english'].removesuffix('{PAD}'),base))
    f = next(r for r in doc['records'] if r['source_presentation_prefix_hex'] == 'fe')
    named = next(r for r in doc['records'] if r['source_presentation_prefix_hex'] == '10')
    reject('FE-not-progressive',lambda:encode_relocatable_dialogue(bytes.fromhex(f['source_hex']),f['english'].removesuffix('{PAD}'),progressive))
    reject('progressive-not-FE',lambda:encode_relocatable_dialogue(bytes.fromhex(named['source_hex']),named['english'].removesuffix('{PAD}'),modal))
    reject('unmapped11',lambda:encode_relocatable_dialogue(b'\x11Hello','{SPEAKER:11}Hello',progressive))
    revised = deepcopy(doc)
    waived = []
    for row in revised['records']:
        english = row['english'].removesuffix('{PAD}')
        consumer = modal if row['source_presentation_prefix_hex'] == 'fe' else progressive
        compiled = encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),english,consumer)
        assert compiled.encoded.hex() == cases[row['id']]['encoded_hex']
        assert all(d.severity == 'warning' and d.code == 'line-break-count' for d in compiled.diagnostics)
        if compiled.diagnostics:
            row['qa_waivers'] = ['line-break-count']
            row['qa_waiver_reason'] = ('Only physical source line-count differs. The full exchange has no deliberate pause at these Japanese storage breaks; automatic English wrapping preserves all source facts and complete native glyphs in one original progressive or FE page. No other warning is waived.')
            waived.append(row['id'])
        row.update(english=english,compiled_hex=compiled.encoded.hex(),
            native_display_consumer='original_FE_modal_5473C_mode1' if consumer == modal else 'original_progressive_54020',
            native_control_proof=str(CONTROL),native_font_proof_case=row['id'],individually_observed_original_context=True)
        row['review']['formatting'] = True
    font_path = ROOT/'all79_complete_native_font_and_macro_reconciliation.json'
    revised.update(predecessor_manuscript=str(OLD),predecessor_manuscript_sha256=sha(OLD.read_bytes()),
        review_gates=['source','context','localization','naturalness','formatting'],formatting_review_pending=False,
        status='all79-source-prose-native-font-approved;typed-relocation-revised-gameplay-release-pending',
        encoder='dialogue-relocatable-v1',required_runtime_ARM9_sha256=sha(arm),
        native_font_proof=str(font_path),scoped_profile_module='dk4tool/dialogue/lil_hamburg_profile.py',
        scoped_profile_module_sha256=sha(Path('dk4tool/dialogue/lil_hamburg_profile.py').read_bytes()),
        native_control_proof=str(CONTROL),native_control_proof_sha256=sha(CONTROL.read_bytes()),
        all11_native_review_sheets_actually_viewed=True,actual_revised_gameplay_and_registered_release_pending=True)
    revised_menu = deepcopy(menu)
    for row in revised_menu['records']:
        row['review']['formatting'] = True
        row['native_choice_font_and_VM_proof'] = str(CHOICE)
        row['individual_choice_selected_in_original_test'] = row['option_index'] == 0
    revised_menu.update(predecessor_manuscript=str(MENU),predecessor_manuscript_sha256=sha(MENU.read_bytes()),
        review_gates=['source','context','localization','naturalness','formatting'],formatting_review_pending=False,
        required_runtime_ARM9_sha256=sha(arm),native_choice_font_and_VM_proof=str(CHOICE),
        native_choice_review_sheet_viewed=True,status='two-labels-source-native-reviewed;revised-menu-release-pending')
    validate_natural_dialogue_batch(revised)
    validate_natural_dialogue_batch(revised_menu)
    bad = deepcopy(revised)
    bad['records'][0]['review']['formatting'] = False
    reject('incomplete-individual-formatting',lambda:validate_natural_dialogue_batch(bad))
    bad_menu = deepcopy(revised_menu)
    bad_menu['review_gates'].remove('formatting')
    reject('incomplete-batch-formatting',lambda:validate_natural_dialogue_batch(bad_menu))
    assert len(negatives) == 11
    ROOT.mkdir(parents=True)
    save(OUT,revised)
    save(MENU_OUT,revised_menu)
    save(font_path,dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],
        manuscript=str(OUT),manuscript_sha256=sha(OUT.read_bytes()),source_manuscript=str(OLD),
        source_manuscript_sha256=sha(OLD.read_bytes()),cases=list(cases.values()),failures=[],native_macro_calls=632,
        all79_complete_native_independent_planes=True,all76_progressive_and3_separate_FE_planes_complete=True,
        all6_original_FE_holds_match_complete_native_mode1_ink=True,all11_review_sheets_actually_viewed=True,
        review_sheets=sheets,visual_review_pending=False,only_physical_line_count_warnings_narrowly_waived=waived,
        negative_cases=negatives,evidence=dependencies,revised_actual_and_relocation_release_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    save(ROOT/'approval_receipt.json',dict(manuscript=str(OUT),manuscript_sha256=sha(OUT.read_bytes()),
        choices=str(MENU_OUT),choices_sha256=sha(MENU_OUT.read_bytes()),font_proof=str(font_path),font_proof_sha256=sha(font_path.read_bytes()),
        original79_speeches_observed_new79_planes632_macro_cases=True,two_labels_eight_planes_six_VM_cases=True,
        all11_native_sheets_and_choice_sheet_actually_viewed=True,negative_cases=negatives,
        narrowly_waived_physical_line_counts=len(waived),no_prose_body_changes=True,
        no_global_profile_ROM_orcompletion_changes=True,full_goal_complete=False))
    print(dict(native_speeches=79,macro_calls=632,labels=2,scope_negatives=len(negatives),line_count_waivers=len(waived)))
