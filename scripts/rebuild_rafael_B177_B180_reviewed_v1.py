"""Rebuild the four exact tutorial blocks with full native control and inverse guards."""
from pathlib import Path

from dk4tool.dialogue.reviewed_choice_object_v2 import compile_choices as strict_choices, labels
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.check_rafael_B177_B180_two_choice_display_v2 import LEGACY_CURRENT, compile_choices as legacy_choices
from scripts.source_locked_derivation_v5118 import checked_text

ROOT = Path('work/analysis')
DOC = Path('translations/rafael_B177_B180_formatting_manuscript_v2.json')
PLAN = ROOT / 'Rafael_B177_B180_automatic_layout_v8_20261105/automatic_plans.json'
NATIVE = ROOT / 'Rafael_B177_B180_offline_review_v1_20261105/compiled_native_pages.json'
PACKET = ROOT / 'Rafael_B177_B180_current1424_20261105/current_effective.json'
MENU = ROOT / 'Rafael_B177_B180_native_menus_v2_20261105/complete_choice_objects.json'
INPUTS = ROOT / 'Rafael_B177_B180_storage_inputs_v1_20261105'
TEMPLATE = Path('scripts/rebuild_rafael_B141_B160_reviewed_v1.py')


def compile_bound_choices(source, prior, rows, *, require_formatting=True):
    first = rows[0]
    if prior == LEGACY_CURRENT:
        assert first['block'] == 177 and first['source_command_offset'] == 2278
        assert first['current_choice_object_hex'] == LEGACY_CURRENT.hex()
        target = legacy_choices(source, prior, rows, require_formatting=require_formatting)
        assert labels(target) == [b'Yes', b'No']
        return target
    return strict_choices(source, prior, rows, require_formatting=require_formatting)


def prepare():
    assert not INPUTS.exists()
    doc, plan, native, packet, menu = map(load, [DOC, PLAN, NATIVE, PACKET, MENU])
    assert doc['blocks'] == [177, 178, 179, 180] == [g['block'] for g in packet['groups']]
    assert packet['runtime'] == native['runtime'] == doc['runtime']
    assert native['manuscript_sha256'] == plan['manuscript_sha256'] == sha(DOC.read_bytes())
    assert native['plan_sha256'] == sha(PLAN.read_bytes())
    assert native['all_final_186_body_pages_directly_viewed'] and native['all_16_reviewed_caption_style_planes_directly_viewed']
    assert len(doc['records']) == 183 and len(native['records']) == 175 and native['pages'] == 186
    assert all(c['word'] != 0x4100 for g in packet['groups'] for k in ('all_source_commands','all_current_commands') for c in g[k])
    typed = {r['id']: r for r in doc['records'] if r['kind'] == 'typed-choice-label'}
    bound = []
    for obj in menu['objects']:
        receipt_path = Path(obj['receipt'])
        receipt = load(receipt_path)
        assert sha(receipt_path.read_bytes()) == obj['receipt_sha256']
        assert receipt['runtime'] == doc['runtime'] and receipt['source_index_andcount_preserved']
        rows = [typed[key] for key in obj['record_ids']]
        assert load(receipt['manuscript'])['records'] == rows
        source, current = [bytes.fromhex(rows[0][key]) for key in ('source_choice_object_hex','current_choice_object_hex')]
        target = compile_bound_choices(source, current, rows, require_formatting=False)
        assert target.hex() == receipt['native_choice_object_hex']
        assert target == Path(obj['compiled_path']).read_bytes() and sha(target) == obj['compiled_sha256']
        bound.append(dict(block=obj['block'], source_command_offset=obj['source_command_offset'],
            target_object_hex=target.hex(), record_IDs=obj['record_ids'], versions=receipt['versions'],
            native_proof=str(receipt_path), native_proof_sha256=obj['receipt_sha256']))
    assert len(bound) == 4 and len(typed) == 8
    shared = dict(manuscript=str(DOC), manuscript_sha256=sha(DOC.read_bytes()),
        runtime=doc['runtime'], plan=str(PLAN), plan_sha256=sha(PLAN.read_bytes()),
        actual_gameplay=False, new_credit=0)
    INPUTS.mkdir()
    save(INPUTS/'menu.json', {**shared, 'offline_visual_approved':True, 'direct_view_pending':False,
        'menus':bound, 'source_caption_proof':str(MENU), 'source_caption_proof_sha256':sha(MENU.read_bytes())})
    save(INPUTS/'styles.json', {**shared, 'objects':[], 'complete_clean_current_census_proves_no4100_objects':True})


from scripts.rebuild_rafael_B141_B160_reviewed_v1 import source as previous

source = checked_text(previous, {
    'from dk4tool.dialogue.reviewed_choice_object_v2 import compile_choices': '',
    'value=compile_choices(source,prior,rows,require_formatting=False)':
        'value=compile_bound_choices(source,prior,rows,require_formatting=False)',
    "len(doc['records'])==557": "len(doc['records'])==183",
    "==len(native['records'])==549": "==len(native['records'])==175",
    '==(549,0,8)': '==(175,0,8)',
    'len(changed)==20': 'len(changed)==4',
    'speech_count=549': 'speech_count=175',
    'total_rendered_speech_count=549': 'total_rendered_speech_count=175',
    'ordinary_speeches=549': 'ordinary_speeches=175',
    'changed_blocks=20': 'changed_blocks=4',
    'Rafael B141-B160 complete557-object source-bound reconstruction': 'Rafael B177-B180 complete183-object source-bound reconstruction',
})
if __name__=='__main__':
    import sys
    if sys.argv[1:] == ['--prepare']:
        prepare()
    else:
        exec(compile(source,__file__+'::same-complete-rebuild-183-scope-exact-legacy-current-slot','exec'),globals())
