"""Rebuild the complete reviewed Rafael B301–B320 objects for stored checks."""
from pathlib import Path
import sys

from scripts import rebuild_rafael_B281_B300_reviewed_v1 as previous
from scripts.audit_story_glyph_consistency import load, save
from scripts.check_rafael_B301_B320_name_planes_v1 import RETAINED
from scripts.refine_rafael_B301_B320_plan_v1 import MANUSCRIPT, ROOT, digest
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_rafael_B301_B320_flow_delta_v1 import FINAL_SHEETS
from scripts.verify_rafael_B301_B320_visual_delta_v1 import FINAL as FINAL_NATIVE, PLAN, SHEETS
from scripts.write_rafael_B301_B320_contextual_v1 import CURRENT


REGISTRY, TEMPLATE = previous.REGISTRY, previous.TEMPLATE
STYLES = ROOT / 'compiled_styles_v3/compiled_style_objects.json'
BINARY = ROOT / 'native_binary_menus_v1/complete_choice_objects.json'
TERNARY = ROOT / 'native_ternary_menu_v1/menu_provider_and_planes.json'
INPUTS = ROOT / 'stored_rebuild_inputs_v1'
MENU = INPUTS / 'menu.json'
COMPOUNDS = INPUTS / 'styles.json'
VISUAL = INPUTS / 'visual_review.json'


def prepare():
    assert not INPUTS.exists()
    doc, native, styles, binary, ternary, names = map(load, (MANUSCRIPT, FINAL_NATIVE, STYLES, BINARY, TERNARY, RETAINED))
    runtime = doc['runtime']
    assert all(proof['runtime'] == runtime for proof in (native, styles, ternary, names))
    assert native['plan_sha256'] == styles['plan_sha256'] == digest(PLAN)
    assert native['manuscript_sha256'] == styles['manuscript_sha256'] == digest(MANUSCRIPT)
    assert (len(styles['objects']), styles['physical_alternatives'], styles['native_target_slot_cases']) == (19, 145, 152)
    assert binary['all_checks_pass'] and binary['physical_caption_records'] == 8
    assert ternary['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
    ternary_object, = ternary['menus']
    proofs = [(o['block'], o['source_command_offset'], 0x2100, Path(o['receipt']), o['receipt_sha256'])
              for o in binary['objects']]
    proofs.append((312, ternary_object['source_command_offset'], 0x2200, TERNARY, digest(TERNARY)))
    menus, previews = [], []
    for block, offset, word, path, checksum in sorted(proofs):
        assert digest(path) == checksum
        proof = load(path)
        assert proof['runtime'] == runtime and proof['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
        rows = [row for row in doc['records'] if row['kind'] == 'typed-choice-label'
                and (row['block'], row['source_command_offset'], row['source_word']) == (block, offset, word)]
        sub = Path(proof['manuscript'])
        assert digest(sub) == proof['manuscript_sha256']
        for a, b in zip(rows, load(sub)['records'], strict=True):
            assert all(a[key] == b[key] for key in ('id', 'english', 'source_reference', 'current_reference'))
        target = proof['native_choice_object_hex'] if word == 0x2100 else ternary_object['target_object_hex']
        assert bytes.fromhex(target)[:2] == word.to_bytes(2, 'little')
        previews.extend([proof['review_sheet']] if word == 0x2100 else proof['review_sheets'])
        menus.append(dict(block=block, source_command_offset=offset, source_word=word, target_object_hex=target,
                          record_IDs=[row['id'] for row in rows], native_receipt=str(path), native_receipt_sha256=checksum))
    assert sum(len(o['record_IDs']) for o in menus) == 11 and len(menus) == 5
    prior, fresh = map(load, (FINAL_SHEETS/'sheet_index.json', SHEETS/'sheet_index.json'))
    assert prior['pages'] == native['pages'] == 444 and fresh['pages'] == 38
    previews.extend([*prior['sheets'], *fresh['sheets'], *names['review_sheets']])
    assert len(previews) == 28 and all(digest(row['path']) == row['sha256'] for row in previews)
    common = dict(manuscript=str(MANUSCRIPT), manuscript_sha256=digest(MANUSCRIPT),
                  plan=str(PLAN), plan_sha256=digest(PLAN), runtime=runtime, new_credit=0)
    INPUTS.mkdir()
    save(MENU, {**common, 'menus': menus, 'offline_visual_approved': True, 'direct_view_pending': False})
    save(COMPOUNDS, {**styles, **common})
    save(VISUAL, {**common, 'native_sha256': digest(FINAL_NATIVE), 'body_pages': 444, 'typed_choice_captions': 11,
         'source_staged_progressive_pages': 0, 'all_final_body_caption_and_name_sheets_directly_viewed': True,
         'name_sheets_scope': 'All 19 scoped actor and role labels with 18 distinct strings.', 'sheets': previews})


source = checked_text(previous.source, {
    "len(doc['records'])==245": "len(doc['records'])==453",
    "==len(native['records'])==240": "==len(native['records'])==442",
    '==(164,76,5)': '==(297,145,11)',
    'unchanged_control_only_blocks=[],speech_count=164': 'unchanged_control_only_blocks=[],speech_count=297',
    'style_physical_speech_count=76,total_rendered_speech_count=240,typed_choice_count=5,compound_objects=13':
        'style_physical_speech_count=145,total_rendered_speech_count=442,typed_choice_count=11,compound_objects=24',
    'ordinary_speeches=164,style_alternatives=76,menu_labels=5,changed_blocks=20':
        'ordinary_speeches=297,style_alternatives=145,menu_labels=11,changed_blocks=20',
    'Rafael B281–B300 complete source-bound reconstruction': 'Rafael B301–B320 complete source-bound reconstruction',
    "==(248,5,0)": "==(444,11,0)",
    "release['all_nine_registered_final_stages_preserved'] and release['owned_Plett_Jacob_surnames_verified']":
        "release['all_predecessor_stage_dependencies_preserved'] and release['owned_Zaganos_surname_verified']",
})


if __name__ == '__main__':
    if sys.argv[1:] == ['--prepare']:
        prepare()
    else:
        exec(compile(source, __file__ + '::same-native-scene-rebuild-exact-453-object-scope', 'exec'), globals())
