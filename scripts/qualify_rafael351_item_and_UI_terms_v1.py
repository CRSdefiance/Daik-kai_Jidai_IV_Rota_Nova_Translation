"""Bind scoped editorial terms to clean/current data without changing any ROM."""
import struct
from pathlib import Path

from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE
from scripts.audit_story_glyph_consistency import load, save
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime

ROOT = Path('work/analysis/Rafael351_item_UI_terms_v1_20261105')
CURRENT = Path('work/analysis/Rafael_B121_B140_current678_20261105/current_effective.json')
IDENTITY = Path('work/analysis/Rafael351_identity_note_alignment_v1_20261105/qualified_names_roles_andparticle_findings.json')
ITEMS = Path('translations/all_item_names_arm9_v1.json')
BUTTONS = Path('translations/trading_button_labels_v2.json')
RADIAL = Path('translations/common_radial_obj_labels_v3.json')
HELP = Path('translations/help_shipyard_sea59_integrated_final_review_v1.json')


def string(raw, pointer):
    at = pointer - BASE
    assert 0 <= at < len(raw)
    end = raw.index(0, at)
    assert end - at < 160
    value = raw[at:end]
    return dict(pointer=pointer, hex=value.hex(), text=value.decode('cp932'))


def main():
    assert not ROOT.exists()
    current, identity = map(load, [CURRENT, IDENTITY])
    ctx = RegisteredRuntime(current['runtime']['release_proof'], current['runtime']['startup_proof'], captain=0)
    assert ctx.receipt() == current['runtime'] == identity['runtime']
    jp = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')

    def field(offset):
        sp, cp = [struct.unpack_from('<I', raw, offset)[0] for raw in [jp, ctx.arm]]
        return dict(pointer_field_offset=offset, source=string(jp, sp), current=string(ctx.raw, cp),
                    current_field_hex=ctx.arm[offset:offset+4].hex())

    item_rows = []
    registered_items = {r['offset']: r for r in load(ITEMS)['records'] if 'english' in r}
    for offset, source, english in [(1173016, 'トラロックのナイフ', 'Tlaloc Knife'),
            (1174024, '善導のステッキ', 'Guiding Staff'), (1174984, '六分儀', 'Sextant'),
            (1175440, '細雪のローブ', 'Snow-Silk Robe'), (1176304, '儀式用の小刀', 'Ceremonial Knife')]:
        row = field(offset)
        assert row['source']['text'] == source and row['current']['text'] == english == registered_items[offset]['english']
        row['registered_item_record'] = registered_items[offset]['id']
        item_rows.append(row)
    # Generic "this knife" in B126 does not identify either named knife above.
    # This binding must never be used to invent an item name in that exchange.
    buttons = []
    for offset, english in [(1160476, 'Select'), (1160532, 'Finish')]:
        r = next(r for r in load(BUTTONS)['records'] if r['offset'] == offset)
        source, actual = [raw[offset:offset+8] for raw in [jp, ctx.arm]]
        assert actual.split(b'\0')[0].decode('ascii') == r['english'] == english
        buttons.append(dict(offset=offset, source_hex=source.hex(), current_hex=actual.hex(),
            source=source.split(b'\0')[0].decode('cp932'), current=english, context=r['context'], registered_record=r['id']))

    wanted = [(1192928, 'ヴェルデ', 'Verde'), (1192580, 'サン＝ジョルジェ', 'Sao Jorge'),
        (1150404, '自動移動', 'Auto Move'), (1150500, '自動移動', 'Auto Move'),
        (1154468, '自動移動', 'Auto Move'), (1134328, '旗艦重視', 'Flagship'),
        (1149892, '水夫を集める', 'Recruit Crew'), (428576, '自動移動中', 'Auto Sail')]
    terms = []
    for offset, source, english in wanted:
        row = field(offset)
        assert row['source']['text'] == source and row['current']['text'] == english
        terms.append(row)

    source_names, current_names = [struct.unpack_from('<I', raw, 0xCDAC0)[0]-BASE for raw in [jp, ctx.arm]]
    assert source_names == current_names
    vels = field(source_names+61*32)
    assert vels['source']['text'] == 'ヴェルス' and vels['current']['text'] == 'Vels'
    vels['actor_ID'] = 61
    vels['scope'] = 'Body reference to the existing given name; no new full-name or progressive-header review credit.'

    accepted = NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    radial = load(RADIAL)
    assert next(r for r in radial['records'] if r['bank'] == 4)['text'] == 'Route Map'
    obj = ctx.image.read_file('/GRP/DSOBJ.DK4')
    assert obj == accepted.read_file('/GRP/DSOBJ.DK4')
    help_rows = [r for r in load(HELP)['records'] if r.get('heading') == 'Auto Move']
    assert help_rows and all(all(r['review'][g] for g in ['source','context','localization','naturalness','formatting']) for r in help_rows)
    arms = [r for r in load(HELP)['records'] if "town's Arms" in r.get('english','') or "town's Arms" in r.get('source_meaning','') or 'Arms rating' in r.get('english','')]
    assert arms
    ROOT.mkdir(parents=True)
    save(ROOT/'term_bindings.json', dict(runtime=ctx.receipt(), clean_ARM9_sha256=sha(jp),
        items=item_rows, buttons=buttons, pointer_terms=terms, Vels_given_name=vels,
        Route_Map=dict(registered_record=next(r['id'] for r in radial['records'] if r['bank']==4), bank=4, text='Route Map',
            resource='/GRP/DSOBJ.DK4', resource_sha256=sha(obj), exact_accepted_main_resource_reuse=True,
            shorter_ARM9_Map_heading_is_a_different_consumer=True),
        Auto_Move_HELP_reuse=[dict(id=r['id'], heading=r['heading'], english=r['english'], review=r['review']) for r in help_rows],
        Arms_reviewed_HELP_references=[dict(id=r['id'], english=r['english'], review=r['review']) for r in arms],
        source_full_half_anchor_are_sailing_states_not_new_literal_UI_caption_claim=True,
        source_India_Proof_and_generic_knife_need_no_invented_landmark_or_named_item=True,
        two_full_catalogue_particle_fixes_still_pending=True,
        no_new_native_execution_rendering_gameplay_or_original_conditional_activation=True,
        read_only_no_ROM_RAM_registry_or_current_manuscript_change=True, new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [CURRENT,IDENTITY,ITEMS,BUTTONS,RADIAL,HELP,Path(__file__)]}))
    print('Bound five item names, two trading buttons, eight menu/status/place pointers, Vels, and accepted Route Map resource. Offline data checks only; no ROM change or credit.')


if __name__ == '__main__': main()
