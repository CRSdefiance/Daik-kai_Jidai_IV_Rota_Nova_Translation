"""Rebuild all reviewed Rafael B281–B300 commands for stored and emulator checks."""
from pathlib import Path
import sys

from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_rafael_B281_B300_display_v1 import DELTA_SHEETS, MENUS, NAME, STYLES
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.plan_rafael_B281_B300_v1 import CURRENT, FORMATTING, ROOT
from scripts.rebuild_rafael_B261_B280_reviewed_v1 import REGISTRY, TEMPLATE, source as previous
from scripts.refine_rafael_B281_B300_visual_v1 import FIRST_SHEETS
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_rafael_B281_B300_visual_delta_v1 import FINAL as FINAL_NATIVE, PLAN


INPUTS = ROOT / 'stored_rebuild_inputs_v1'
MENU = INPUTS / 'menu.json'
COMPOUNDS = INPUTS / 'styles.json'
VISUAL = INPUTS / 'visual_review.json'


def prepare():
    assert not INPUTS.exists()
    doc, plan, native, styles = map(load, (FORMATTING, PLAN, FINAL_NATIVE, STYLES))
    runtime = doc['runtime']
    assert runtime == styles['runtime'] == native['runtime']
    assert native['plan_sha256'] == styles['plan_sha256'] == digest(PLAN)
    assert styles['manuscript_sha256'] == digest(FORMATTING)
    assert (len(styles['objects']), styles['physical_alternatives'], styles['native_target_slot_cases']) == (11, 76, 88)
    common = dict(manuscript=str(FORMATTING), manuscript_sha256=digest(FORMATTING),
                  plan=str(PLAN), plan_sha256=digest(PLAN), runtime=runtime, new_credit=0)
    menus, previews = [], []
    for offset, word, path in zip((884, 1906), (0x2200, 0x2100), MENUS, strict=True):
        proof = load(path)
        assert proof['runtime'] == runtime and proof['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
        rows = [row for row in doc['records'] if row['kind'] == 'typed-choice-label' and row['source_command_offset'] == offset]
        sub = Path(proof['manuscript'])
        assert digest(sub) == proof['manuscript_sha256']
        for a, b in zip(rows, load(sub)['records'], strict=True):
            assert all(a[key] == b[key] for key in ('id', 'english', 'source_reference', 'current_reference'))
        if word == 0x2200:
            assert len(proof['menus']) == 1 and proof['menus'][0]['source_command_offset'] == offset
            target = proof['menus'][0]['target_object_hex']
            previews.extend(proof['review_sheets'])
        else:
            target = proof['native_choice_object_hex']
            previews.append(proof['review_sheet'])
        assert bytes.fromhex(target)[:2] == word.to_bytes(2, 'little')
        menus.append(dict(block=293, source_command_offset=offset, source_word=word,
                          target_object_hex=target, record_IDs=[row['id'] for row in rows],
                          native_receipt=str(path), native_receipt_sha256=digest(path)))
    previews.extend([*load(FIRST_SHEETS)['sheets'], *load(DELTA_SHEETS)['sheets'], load(NAME)['review_sheet']])
    assert len(previews) == 16 and all(digest(row['path']) == row['sha256'] for row in previews)
    assert len(plan['records']) == 240
    INPUTS.mkdir()
    save(MENU, {**common, 'menus': menus, 'offline_visual_approved': True, 'direct_view_pending': False})
    save(COMPOUNDS, {**styles, **common})
    save(VISUAL, {**common, 'native_sha256': digest(FINAL_NATIVE), 'body_pages': 248, 'typed_choice_captions': 5,
         'source_staged_progressive_pages': 0, 'all_final_body_caption_and_name_sheets_directly_viewed': True,
         'name_sheets_scope': 'Zaganos Bey in both native name consumers.', 'sheets': previews})


source = checked_text(previous, {
    "len(doc['records'])==135": "len(doc['records'])==245",
    "==len(native['records'])==130": "==len(native['records'])==240",
    '==(114,16,5)': '==(164,76,5)',
    'unchanged_control_only_blocks=[],speech_count=114': 'unchanged_control_only_blocks=[],speech_count=164',
    'style_physical_speech_count=16,total_rendered_speech_count=130,typed_choice_count=5,compound_objects=4':
        'style_physical_speech_count=76,total_rendered_speech_count=240,typed_choice_count=5,compound_objects=13',
    'ordinary_speeches=114,style_alternatives=16,menu_labels=5,changed_blocks=20':
        'ordinary_speeches=164,style_alternatives=76,menu_labels=5,changed_blocks=20',
    'Rafael B261–B280 complete source-bound reconstruction': 'Rafael B281–B300 complete source-bound reconstruction',
    "==(131,5,0)": "==(248,5,0)",
    "release['all_preceding_eight_stages_and_exclusive_field_preserved']":
        "release['all_nine_registered_final_stages_preserved'] and release['owned_Plett_Jacob_surnames_verified']",
})


if __name__ == '__main__':
    if sys.argv[1:] == ['--prepare']:
        prepare()
    else:
        exec(compile(source, __file__ + '::same-native-scene-rebuild-exact-245-object-scope', 'exec'), globals())
