"""Rebuild the reviewed final-SC0 conversations for stored and gameplay checks."""
from pathlib import Path
import sys

from scripts import rebuild_rafael_B301_B320_reviewed_v1 as previous
from scripts.audit_story_glyph_consistency import load, save
from scripts.check_rafael_B321_B342_name_planes_v1 import RETAINED
from scripts.checkpoint_rafael_B321_B331_contextual_v1 import INPUTS as BINDINGS
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.plan_rafael_B321_B342_v1 import ROOT
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_rafael_B321_B342_visual_v1 import APPROVAL, FINAL as FINAL_NATIVE, FORMATTING, PLAN


REGISTRY, TEMPLATE = previous.REGISTRY, previous.TEMPLATE
CURRENT = BINDINGS[1]
MANUSCRIPT = FORMATTING
STYLES = ROOT / 'compiled_styles_v3/compiled_style_objects.json'
BINARY = ROOT / 'native_binary_menus_v1/complete_choice_objects.json'
TERNARY = ROOT / 'native_ternary_menus_v1/menu_provider_and_planes.json'
INPUTS = ROOT / 'stored_rebuild_inputs_v1'
MENU = INPUTS / 'menu.json'
COMPOUNDS = INPUTS / 'styles.json'
VISUAL = INPUTS / 'visual_review.json'


def prepare():
    assert not INPUTS.exists()
    doc, native, styles, binary, ternary, names, approval = map(load, (
        MANUSCRIPT, FINAL_NATIVE, STYLES, BINARY, TERNARY, RETAINED, APPROVAL))
    runtime = doc['runtime']
    assert all(proof['runtime'] == runtime for proof in (native, styles, ternary, names))
    assert native['plan_sha256'] == styles['plan_sha256'] == digest(PLAN)
    assert native['manuscript_sha256'] == styles['manuscript_sha256'] == digest(MANUSCRIPT)
    assert (len(styles['objects']), styles['physical_alternatives'], styles['native_target_slot_cases']) == (48, 298, 384)
    assert binary['all_checks_pass'] and binary['physical_caption_records'] == 10
    assert ternary['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
    ternary_objects = {(row['block'], row['source_command_offset']): row for row in ternary['menus']}
    assert len(ternary_objects) == 2
    proofs = [(row['block'], row['source_command_offset'], 0x2100, Path(row['receipt']), row['receipt_sha256'])
              for row in binary['objects']]
    proofs.extend((block, offset, 0x2200, TERNARY, digest(TERNARY)) for block, offset in ternary_objects)
    menus = []
    for block, offset, word, path, checksum in sorted(proofs):
        assert digest(path) == checksum
        proof = load(path)
        assert proof['runtime'] == runtime and proof['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
        signature = lambda row: (row['block'], row['source_command_offset'], row['source_word'])
        key = block, offset, word
        rows = [row for row in doc['records'] if row['kind'] == 'typed-choice-label' and signature(row) == key]
        subset = Path(proof['manuscript'])
        assert digest(subset) == proof['manuscript_sha256']
        reviewed = [row for row in load(subset)['records'] if signature(row) == key]
        for a, b in zip(rows, reviewed, strict=True):
            assert all(a[field] == b[field] for field in ('id', 'english', 'source_reference', 'current_reference'))
        target = (proof['native_choice_object_hex'] if word == 0x2100
                  else ternary_objects[(block, offset)]['target_object_hex'])
        assert bytes.fromhex(target)[:2] == word.to_bytes(2, 'little')
        menus.append(dict(block=block, source_command_offset=offset, source_word=word,
                          target_object_hex=target, record_IDs=[row['id'] for row in rows],
                          native_receipt=str(path), native_receipt_sha256=checksum))
    assert len(menus) == 7 and sum(len(menu['record_IDs']) for menu in menus) == 16
    assert approval['native_sha256'] == digest(FINAL_NATIVE) and approval['plan_sha256'] == digest(PLAN)
    assert approval['all_final_body_caption_and_name_sheets_directly_viewed']
    assert all(digest(row['path']) == row['sha256'] for row in approval['sheets'])
    common = dict(manuscript=str(MANUSCRIPT), manuscript_sha256=digest(MANUSCRIPT),
                  plan=str(PLAN), plan_sha256=digest(PLAN), runtime=runtime, new_credit=0)
    INPUTS.mkdir()
    save(MENU, {**common, 'menus': menus, 'offline_visual_approved': True, 'direct_view_pending': False})
    save(COMPOUNDS, {**styles, **common})
    save(VISUAL, {**common, 'native_sha256': digest(FINAL_NATIVE), 'body_pages': 552,
                  'typed_choice_captions': 16, 'source_staged_progressive_pages': 0,
                  'all_final_body_caption_and_name_sheets_directly_viewed': True,
                  'name_sheets_scope': 'All 16 scoped actors and role labels with 15 distinct progressive strings.',
                  'sheets': approval['sheets'], 'approval': str(APPROVAL), 'approval_sha256': digest(APPROVAL)})


source = checked_text(previous.source, {
    "len(doc['records'])==453": "len(doc['records'])==556",
    "==len(native['records'])==442": "==len(native['records'])==540",
    '==(297,145,11)': '==(242,298,16)',
    'unchanged_control_only_blocks=[],speech_count=297': 'unchanged_control_only_blocks=[],speech_count=242',
    'style_physical_speech_count=145,total_rendered_speech_count=442,typed_choice_count=11,compound_objects=24':
        'style_physical_speech_count=298,total_rendered_speech_count=540,typed_choice_count=16,compound_objects=55',
    'ordinary_speeches=297,style_alternatives=145,menu_labels=11,changed_blocks=20':
        'ordinary_speeches=242,style_alternatives=298,menu_labels=16,changed_blocks=22',
    'Rafael B301–B320 complete source-bound reconstruction': 'Rafael B321–B342 complete source-bound reconstruction',
    '==(444,11,0)': '==(552,16,0)',
    'len(changed)==20': 'len(changed)==22',
    "release['owned_Zaganos_surname_verified']": "release['all_other_files_components_graphics_names_andruntime_exact_to_parent']",
})


if __name__ == '__main__':
    if sys.argv[1:] == ['--prepare']:
        prepare()
    else:
        exec(compile(source, __file__ + '::same-complete-scene-rebuild-556-record-scope', 'exec'), globals())
