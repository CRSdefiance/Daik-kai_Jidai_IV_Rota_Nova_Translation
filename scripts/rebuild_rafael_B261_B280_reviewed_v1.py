"""Rebuild the 135 reviewed Rafael objects under the existing scene contract."""
from pathlib import Path
import sys

from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_rafael_B261_B280_display_v1 import DELTA, JACOB, MENU_PATHS, NATIVE, PLAN, STYLES
from scripts.finish_rafael_B261_B280_native_pages_v1 import MANUSCRIPT, ROOT, SHEETS, digest
from scripts.plan_rafael_B261_B280_v1 import CURRENT
from scripts.rebuild_rafael_B241_B260_reviewed_v1 import REGISTRY, TEMPLATE, source as previous
from scripts.source_locked_derivation_v5118 import checked_text


INPUTS = ROOT / 'stored_rebuild_inputs_v1'
MENU = INPUTS / 'menu.json'
COMPOUNDS = INPUTS / 'styles.json'
VISUAL = INPUTS / 'visual_review.json'


def prepare():
    assert not INPUTS.exists()
    doc, plan, native, styles = map(load, (MANUSCRIPT, PLAN, NATIVE, STYLES))
    runtime = doc['runtime']
    assert runtime == styles['runtime'] == native['runtime']
    assert native['plan_sha256'] == digest(PLAN)
    old_plan = Path(styles['plan'])
    assert styles['plan_sha256'] == digest(old_plan)
    old = {row['id']: row for row in load(old_plan)['records']}
    new = {row['id']: row for row in plan['records']}
    styled = [ident for obj in styles['objects'] for ident in obj['physical_record_IDs']]
    assert len(set(styled)) == len(styled) == 16 and all(old[ident] == new[ident] for ident in styled)
    common = dict(manuscript=str(MANUSCRIPT), manuscript_sha256=digest(MANUSCRIPT),
                  plan=str(PLAN), plan_sha256=digest(PLAN), runtime=runtime, new_credit=0)
    menus, previews = [], []
    for offset, word, path in zip((270, 1664), (0x2200, 0x2100), MENU_PATHS, strict=True):
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
        menus.append(dict(block=261, source_command_offset=offset, source_word=word,
                          target_object_hex=target, record_IDs=[row['id'] for row in rows],
                          native_receipt=str(path), native_receipt_sha256=digest(path)))
    previews.extend([*load(SHEETS/'sheet_index.json')['sheets'], *load(DELTA)['sheets'], load(JACOB)['review_sheet']])
    assert len(previews) == 10 and all(digest(row['path']) == row['sha256'] for row in previews)
    INPUTS.mkdir()
    save(MENU, {**common, 'menus': menus, 'offline_visual_approved': True, 'direct_view_pending': False})
    save(COMPOUNDS, {**styles, **common, 'unchanged_style_plan_source': str(old_plan),
         'unchanged_style_plan_source_sha256': digest(old_plan), 'all16_style_plan_records_exact': True})
    save(VISUAL, {**common, 'native_sha256': digest(NATIVE), 'body_pages': 131, 'typed_choice_captions': 5,
         'source_staged_progressive_pages': 0, 'all_final_body_caption_and_name_sheets_directly_viewed': True,
         'name_sheets_scope': 'Jacob only. Plett relocation pending.', 'sheets': previews})


source = checked_text(previous, {
    "len(doc['records'])==292": "len(doc['records'])==135",
    "==len(native['records'])==286": "==len(native['records'])==130",
    '==(272,14,6)': '==(114,16,5)',
    'else:assert block==244 and not records and not compound and current==clean':
        "else:raise AssertionError(f'Expected a changed block for reviewed block {block}')",
    'len(changed)==18': 'len(changed)==20',
    'unchanged_control_only_blocks=[244],speech_count=272': 'unchanged_control_only_blocks=[],speech_count=114',
    'style_physical_speech_count=14,total_rendered_speech_count=286,typed_choice_count=6,compound_objects=5':
        'style_physical_speech_count=16,total_rendered_speech_count=130,typed_choice_count=5,compound_objects=4',
    'ordinary_speeches=272,style_alternatives=14,menu_labels=6,changed_blocks=18':
        'ordinary_speeches=114,style_alternatives=16,menu_labels=5,changed_blocks=20',
    'Rafael B241–B260 complete source-bound reconstruction': 'Rafael B261–B280 complete source-bound reconstruction',
    "==(294,6,2)": "==(131,5,0)",
    "assert args.packet==CURRENT and args.menu==OUT/'menu.json' and args.styles==OUT/'styles.json'":
        "assert args.packet==CURRENT and args.menu==MENU and args.styles==COMPOUNDS",
    "release['all_eight_registered_final_stages_preserved']":
        "release['all_preceding_eight_stages_and_exclusive_field_preserved']",
})


if __name__ == '__main__':
    if sys.argv[1:] == ['--prepare']:
        prepare()
    else:
        FINAL_NATIVE = NATIVE
        exec(compile(source, __file__ + '::same-native-scene-rebuild-exact-135-object-scope', 'exec'), globals())
