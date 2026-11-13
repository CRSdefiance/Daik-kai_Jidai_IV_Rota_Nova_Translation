"""Approve57 private-scope native bodies/two typed labels; revised actual pending."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.lil_speyer_profile import profile_for
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/lil_Speyer_font_approval_v1937')
OLD = Path('translations/lil_speyer_encounter_editorial_manuscript_v1.json')
NEW = Path('translations/lil_speyer_encounter_editorial_manuscript_v2.json')
OLD_CHOICES = Path('translations/lil_speyer_choices_editorial_draft_v1.json')
NEW_CHOICES = Path('translations/lil_speyer_choices_editorial_draft_v2.json')
FONT = Path('work/analysis/lil_Speyer_fonts_v1922/all57_native_macros_and_complete_font_planes.json')
CHOICE_FONT = Path('work/analysis/lil_Speyer_choice_v1927/original_choice_decoder_VM_geometry_and_native_pixels.json')
CONTROL = Path('work/analysis/lil_Speyer_controls_v1936/source_bound_B25_B128_progressive_control_contract.json')

if __name__ == '__main__':
    assert not ROOT.exists() and not NEW.exists() and not NEW_CHOICES.exists()
    doc,menu,font,choice,control = map(read,(OLD,OLD_CHOICES,FONT,CHOICE_FONT,CONTROL))
    assert font['manuscript_sha256']==sha(OLD.read_bytes()) and choice['manuscript_sha256']==sha(OLD_CHOICES.read_bytes())
    assert not font['failures'] and len(font['cases'])==57 and font['native_macro_calls']==456
    assert choice['six_original_VM_selection_and_cancel_cases_pass'] and choice['eight_complete_native_style_label_planes_pass']
    image = NdsImage.open(font['candidate'])
    arm = image.read_file('/__arm9__.bin')
    blocks = IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    fonts = {r['id']:r for r in font['cases']}
    profiles = {n:profile_for(arm,blocks[n])for n in(25,128)}
    base = get_dialogue_profile('lil-opening-editorial-native-v1')
    assert not any(p in base.leading_speaker_bytes for p in (29,151,152,254))
    negative = []
    for label,callback in (
        ('wrong-runtime',lambda:profile_for(bytes([arm[0]^1])+arm[1:],blocks[128])),
        ('unrelated-London-block',lambda:profile_for(arm,blocks[26])),
        ('mutated-source-block',lambda:profile_for(arm,blocks[128][:-1]+bytes([blocks[128][-1]^1]))),
        ('unsupported-FE-control',lambda:encode_relocatable_dialogue(b'\xfeHello','{SPEAKER:FE}Hello',profiles[128])),
        ('mismatched-source-speaker',lambda:encode_relocatable_dialogue(b'\x1dHello','{SPEAKER:98}Hello',profiles[128])),
        ('unmapped-control-99',lambda:encode_relocatable_dialogue(b'\x99Hello','{SPEAKER:99}Hello',profiles[128])),
    ):
        try:callback()
        except ValueError as error:negative.append(dict(case=label,error=str(error)))
        else:raise AssertionError('Invalid source/control case accepted:'+label)
    revised = deepcopy(doc)
    warnings = []
    for row in revised['records']:
        old_english = row['english']
        english = old_english.removesuffix('{PAD}')
        result = encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),english,profiles[row['block']])
        case = fonts[row['id']]
        assert result.encoded.hex()==case['encoded_hex']
        assert all(d.code=='line-break-count'for d in result.diagnostics)
        if result.diagnostics:
            row['qa_waivers']=['line-break-count']
            row['qa_waiver_reason']=('Only the count of physical source line breaks differs. Full-exchange review finds no deliberate pause to preserve; automatic English wrapping preserves complete native/independent glyphs, bounds and one216x64 page. No other warning is waived.')
            warnings.append(row['id'])
        row.update(english=english,native_display_consumer='original_progressive_54020',
            native_control_proof=str(CONTROL),native_font_proof_case=row['id'])
        if row['source_presentation_prefix_hex']=='98':
            row.update(actual_visible_nameplate='Sailor',native_catalog_full_name='Retainer',
                native_catalog_identity_not_substituted_for_actual_display_name=True)
        row['review']['formatting']=True
    assert len(warnings)==23
    revised.update(predecessor_manuscript=str(OLD),predecessor_manuscript_sha256=sha(OLD.read_bytes()),
        encoder='dialogue-relocatable-v1',required_runtime_ARM9_sha256=sha(arm),formatting_review_pending=False,
        native_control_proof=str(CONTROL),native_font_proof=str(ROOT/'all57_complete_native_font_and_macro_reconciliation.json'),
        native_font_all8_review_sheets_viewed=True,actual_revised_gameplay_and_registered_release_pending=True,
        status='source-context-prose-native-reviewed;revised-actual-and-release-pending')
    revised_menu = deepcopy(menu)
    for row in revised_menu['records']:
        row['review']['formatting']=True
        row['native_choice_font_and_VM_proof']=str(CHOICE_FONT)
        row['actual_two_label_menu_viewed']=True
        row['individual_choice_selected_in_original_test']=row['option_index']==0
    revised_menu.update(predecessor_manuscript=str(OLD_CHOICES),predecessor_manuscript_sha256=sha(OLD_CHOICES.read_bytes()),
        required_runtime_ARM9_sha256=sha(arm),formatting_review_pending=False,
        native_choice_font_and_VM_proof=str(CHOICE_FONT),native_choice_review_sheet_viewed=True,
        status='two-labels-source-native-reviewed;revised-menu-and-release-pending')
    validate_natural_dialogue_batch(revised)
    validate_natural_dialogue_batch(revised_menu)
    ROOT.mkdir(parents=True)
    save(NEW,revised)
    save(NEW_CHOICES,revised_menu)
    proof = deepcopy(font)
    proof.update(manuscript=str(NEW),manuscript_sha256=sha(NEW.read_bytes()),
        source_native_font_proof=str(FONT),source_native_font_proof_sha256=sha(FONT.read_bytes()),
        source_manuscript=str(OLD),source_manuscript_sha256=sha(OLD.read_bytes()),
        native_control_proof=str(CONTROL),native_control_proof_sha256=sha(CONTROL.read_bytes()),
        all57_encoded_outputs_reproduced_with_source_bound_private_profile=True,
        all8_native_review_sheets_actually_viewed=True,visual_review_pending=False,
        six_invalid_scope_control_cases_rejected=negative,only23_physical_line_count_warnings_narrowly_waived=warnings,
        original_scoped_57_progressive_paragraphs_and456_macro_cases_complete=True,
        revised_actual_display_and_registered_release_still_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()))
    for sheet in proof['review_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    assert sha(Path(choice['visual_review_sheet']).read_bytes())==choice['visual_review_sheet_sha256']
    save(ROOT/'all57_complete_native_font_and_macro_reconciliation.json',proof)
    save(ROOT/'approval_receipt.json',dict(manuscript=str(NEW),manuscript_sha256=sha(NEW.read_bytes()),
        choices=str(NEW_CHOICES),choices_sha256=sha(NEW_CHOICES.read_bytes()),
        private_profile='dk4tool/dialogue/lil_speyer_profile.py',private_profile_sha256=sha(Path('dk4tool/dialogue/lil_speyer_profile.py').read_bytes()),
        all57_complete_native_planes456_macro_cases=True,two_choice_labels_six_VM_cases_eight_planes=True,
        all8_native_sheets_and_choice_sheet_actually_viewed=True,negative_cases=negative,
        source_physical_line_count_warnings_narrowly_waived=23,no_prose_body_changes=True,
        no_global_profile_ROM_orcompletion_changes=True,full_goal_complete=False))
    print(dict(native_speeches=57,macro_cases=456,typed_labels=2,scope_control_negatives=len(negative),
        narrowly_waived_physical_line_counts=23,revised_actual_and_release_pending=True))
