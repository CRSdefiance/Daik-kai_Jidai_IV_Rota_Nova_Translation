"""Expand two Square menu captions through the existing full category decoder."""

from hashlib import sha256
from pathlib import Path
from struct import pack, unpack_from

from ndspy.code import MainCodeFile

from dk4tool.patch.category_dialogue_lookup import BASE, GETTER, INNER, OUTER, TABLE
from dk4tool.patch.main_pool_cache_visibility import POOL, cache_plan, target
from dk4tool.patch.square_caption_cells import assemble
from scripts import register_fleet_sighting_alerts_20261115 as parent
from scripts.prepare_all_routes_promotion_20261111 import verify_runtime
from scripts.verify_release_baseline import files


base = parent.base
ARM, CLEAN = parent.stage.ARM, parent.stage.CLEAN
ROOT = Path('work/square_shop_captions_20261115_v1')
ROM, STORED = ROOT / 'Square_Shop_Captions_RESEARCH_ONLY.nds', ROOT / 'staged.json'
FORMAT_SLOT = 0x14463C
CAPTIONS = (
    ('食料品', 'Food', 'Basic foods and staples, including grain, fish and cheese.'),
    ('調味料', 'Cond.', 'Sugar, honey, salt and cooking oils. The compact abbreviation keeps this separate from Spices; Seasonings Shop exceeds the current caption width.'),
    ('珍味', 'Delicacy', 'Special foods such as caviar, shark fins and nuts. Delicacy fits at full width and distinguishes them from staples.'),
    ('香辛料', 'Spices', 'Pepper, cloves, saffron and other spices. The familiar category name distinguishes them from the separate cooking seasonings.'),
    ('嗜好品', 'Treats', 'Specialty indulgences such as coffee, tea, cocoa and tobacco. The category covers goods bought for enjoyment.'),
    ('酒類', 'Liquor', 'Alcoholic goods including wine, spirits and sake. Liquor Shop is a familiar umbrella name for an alcohol retailer.'),
    ('貴金属', 'Metals', 'Gold, silver and platinum. The compact term is distinct from Ore Shop, and Precious Metals Shop exceeds the caption width.'),
    ('工芸品', 'Crafts', 'Manufactured wares including glass, china, lacquerware and inlaid ware. Crafts signals the worked products.'),
    ('繊維', 'Fiber', 'Fiber and woven goods such as wool, silk and their cloth. The existing compact label identifies the broad trade family; Textile Shop remains a clearer wording lead.'),
    ('贅沢品', 'Luxury', 'Luxury wares such as carpets, art and fine furs. The qualifier is already idiomatic before Shop.'),
    ('香料', 'Scents', 'Aromatic products such as musk, frankincense and ambergris. Scents covers the trade ingredients without implying they are finished perfumes.'),
    ('装飾品', 'Jewelry', 'Decorative materials such as jade, ivory and coral. Jewelry distinguishes ornamental wares from the separate stock gemstones.'),
    ('宝石', 'Gems', 'Pearls, diamonds and other precious stones. Gems clearly identifies the gem trade.'),
    ('薬', 'Med', 'Medicinal trade goods such as ginseng, quinine and cordyceps. Medicine spells out the category and fits in the original cell.'),
    ('染料', 'Dyes', 'Dye goods including indigo and cochineal. The category stays recognizable as a shop label.'),
    ('武器', 'Arms', 'Arms and equipment including guns, cannon, blades and armor. Arms is concise and suits the period setting.'),
    ('鉱石', 'Ore', 'Unprocessed mineral goods such as iron, copper and tin ore. Ore distinguishes the shop from Metals.'),
    ('雑貨', 'Goods', 'Miscellaneous supplies such as timber, leather and wax. Sundries identifies the miscellaneous category and avoids the generic Goods Shop.'),
)
EXPANSIONS = {13: 'Medicine', 17: 'Sundries'}


def transform(source):
    code = MainCodeFile(source, BASE)
    outer = code.sections[4]
    inner = code.sections[3]
    outer_offset = OUTER - outer.ramAddress
    inner_offset = INNER - POOL
    assert target(source, 0x5FDA8) == OUTER
    # This is the full-pointer branch of the registered category decoder.
    decode_full = 0x02151754
    assert source[decode_full - BASE:decode_full - BASE + 8] == bytes.fromhex('ff04c10306058002')
    assert source[TABLE:TABLE + 18 * 4] == bytes(code.sections[0].data[TABLE:TABLE + 18 * 4])
    assert source[FORMAT_SLOT:FORMAT_SLOT + 8] == b'%s Shop\0'
    for ident, word in EXPANSIONS.items():
        packed, = unpack_from('<I', source, TABLE + 4 * ident)
        at = (packed & 0xFFFFFF) + 0x01800000 - BASE
        assert source[at:at + len(word) + 1] == word.encode('ascii') + b'\0'

    # An inverted membership bit gives Z=1 for the four full names. For an
    # index above 17 the comparison leaves Z=0, so the old fallback gets it.
    # The full path preserves Z across two loads and enters the old decoder
    # immediately after its caller check. Everything else uses its normal entry.
    mask = 0xFFFFFFFF ^ sum(1 << i for i in (2, 11, *EXPANSIONS))
    new_outer = assemble(f'''
        cmp r0, #17
        ldrls r1, mask
        movls r1, r1, lsr r0
        tstls r1, #1
        beq {INNER}
        b {GETTER}
        mask: .word {mask}
    ''', OUTER)
    new_inner = assemble(f'''
        ldr r1, table
        ldr r1, [r1, r0, lsl #2]
        b {decode_full}
        table: .word {BASE + TABLE}
    ''', INNER)
    changes = (
        (4, outer_offset, OUTER, '10402de90040a0e1092603eb020054e300009f05107b0eea60c3ff01', new_outer),
        (3, inner_offset, INNER, '0b0054e300009f051080bde820af3902', new_inner),
    )
    owned = []
    for section, offset, address, old_hex, new in changes:
        data = code.sections[section].data
        old = bytes.fromhex(old_hex)
        assert len(old) == len(new) and bytes(data[offset:offset + len(old)]) == old
        data[offset:offset + len(new)] = new
        owned.append(dict(section=section, offset=offset, runtime_address=address,
                          before=old_hex, after=new.hex()))
    result = bytes(code.save())
    assert cache_plan(result) == cache_plan(source)
    for section, offset, _, old_hex, new in changes:
        code.sections[section].data[offset:offset + len(new)] = bytes.fromhex(old_hex)
    assert bytes(code.save()) == source
    return result, owned


def main():
    assert not ROM.exists() and not STORED.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    assert base.digest(parent.ROM) == release['candidate_sha256']
    assert base.digest(CLEAN) == release['clean_input_sha256']
    image = base.NdsImage.open(parent.ROM)
    before = files(image)
    assert sha256(before[ARM]).hexdigest() == release['target_ARM9_sha256']
    arm, owned = transform(before[ARM])
    verify_runtime(arm, release)
    image.replace_file(ARM, arm)
    after = files(image)
    assert before.keys() == after.keys() and {name for name in before if before[name] != after[name]} == {ARM}
    ROOT.mkdir(parents=True, exist_ok=True)
    image.save(ROM)
    image.replace_file(ARM, before[ARM])
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    base.save(STORED, dict(candidate_sha256=base.digest(ROM), previous_sha256=release['candidate_sha256'],
        target_ARM9_sha256=sha256(arm).hexdigest(), owned=owned, whole_parent_inverse=True))
    print('Staged two Square-only caption expansions with exact ARM9 and whole-parent inverses.')


if __name__ == '__main__':
    main()
