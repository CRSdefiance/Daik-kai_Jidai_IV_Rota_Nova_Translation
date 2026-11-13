"""Exercise independent native-menu and existing actual RGB evidence checks."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_B52_menu_evidence_v1 import check_menu_actual
from dk4tool.dialogue.hodram_B52_profile_v1 import validate_approved_batch, validate_runtime
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/Hodram_B52_menu_production_v8672')
DOC = Path('translations/hodram_B52_editorial_manuscript_v6.json')
PATHS = dict(menu_provider='work/analysis/Hodram_B52_menu_v8636/menu_provider_and_planes.json',
    source_menu_VM='work/analysis/Hodram_B52_source_choice_VM_v8628b/source_menu_provider_andresponse_paths.json',
    menu_actual='work/analysis/Hodram_B52_actual_menu_RGB_v8654/actual_menu_RGB_glyph_geometry_highlight.json',
    withdrawal='work/analysis/Hodram_B52_actual_v8651/B52/paired_actual_dialogue_headers_flow_returns.json',
    opposition='work/analysis/Hodram_B52_opposition_actual_v8653/B52/paired_actual_dialogue_headers_flow_returns.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    doc = read(DOC)
    parent = NdsImage.open(doc['current_ROM'])
    validate_approved_batch(doc)
    validate_runtime(parent)
    data = {k: read(p) for k, p in PATHS.items()}

    def require(value, message):
        if not value:
            raise ValueError('B52 production menu:' + message)

    result = check_menu_actual(data, doc, parent, read, require)
    assert (result['native_provider_alignments'], result['bridged_modal_returns'], result['actual_menu_samples'], result['actual_caption_checks']) == (6, 18, 12, 24)
    negatives = []

    def reject(label, mutate):
        changed = deepcopy(data)
        mutate(changed)
        assert changed != data
        try:
            check_menu_actual(changed, doc, parent, read, require)
        except ValueError as error:
            assert 'Native dependency changed' not in str(error)
            negatives.append(dict(label=label, actual_changed_input=True, rejected=True, diagnostic=str(error)))
        else:
            raise AssertionError('Changed menu evidence accepted:' + label)

    reject('untrusted-native-adapter', lambda d: d['menu_provider'].__setitem__('source_owned_VM_adapter', d['menu_provider']['source_owned_VM_adapter'] + '\n'))
    reject('source-label-object', lambda d: d['source_menu_VM']['source_choice']['command'].__setitem__('whole_command_hex', d['source_menu_VM']['source_choice']['command']['whole_command_hex'] + '0000'))
    reject('current-label-object', lambda d: d['menu_provider']['versions'][0].__setitem__('object_hex', d['menu_provider']['versions'][0]['object_hex'] + '0000'))
    reject('reviewed-label-object', lambda d: d['menu_provider']['versions'][1].__setitem__('object_hex', d['menu_provider']['versions'][1]['object_hex'] + '0000'))
    reject('native-rectangle', lambda d: d['menu_provider']['versions'][1]['cases'][0]['native_VM']['native_menu_rectangle'].__setitem__(0, 70))
    reject('modal-return-kind', lambda d: d['source_menu_VM']['even_alignment_provider_cases'][0]['native_VM']['VM_cases'][0].__setitem__('VM_state', 0))
    reject('missing-actual-case', lambda d: d['menu_actual']['groups'].pop())
    reject('actual-caption-leading-cell', lambda d: d['menu_actual']['groups'][0]['samples'][0]['labels'][0]['caption_origin'].__setitem__(0, 80))
    reject('actual-caption-final-mask', lambda d: d['menu_actual']['groups'][0]['samples'][0]['labels'][1].__setitem__('independent_font_mask_sha256', '0' * 64))
    reject('actual-highlight', lambda d: d['menu_actual']['groups'][0]['samples'][0]['labels'][0].__setitem__('highlight_visible', False))
    reject('source-choice-order', lambda d: d['menu_actual']['groups'][0].__setitem__('labels', list(reversed(d['menu_actual']['groups'][0]['labels']))))
    reject('live-backing-overclaim', lambda d: d['menu_actual'].__setitem__('no_new_owner_pointer_RAM_VRAM_palette_orunowned_backing_byte_identity_claim', False))
    assert len(negatives) == 12
    ROOT.mkdir(parents=True)
    save(ROOT / 'menu_production_validation.json', dict(summary=result, negative_cases=negatives, negative_count=12,
         original_Japanese_current_padded_andreviewed_menu_native_results_independently_checked=True,
         all12_existing_actual_RGB_samples_and24captions_independently_checked=True,
         no_native_backing_to_live_RAM_VRAM_palette_owner_identity_upgrade=True,
         all_changed_inputs_rejected_with_frozen_guards_active=True,
         no_previous_producer_oractual_emulator_replay_no_ROM_orcredit=True, full_goal_complete=False,
         evidence={str(p): sha(Path(p).read_bytes()) for p in [DOC, *PATHS.values(), __file__, 'dk4tool/patch/hodram_B52_menu_evidence_v1.py']}))
    print('B52 production menu:6 original provider alignments/18 bridged returns,12 existing actual RGB menus/24 complete captions;12 semantic rejections. Visible/offline backing limits preserved; no new gameplay or credit.')
