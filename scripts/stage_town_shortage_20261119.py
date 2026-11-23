"""Widen the two original compact city-condition surfaces to eight letters."""

from struct import pack_into, unpack_from

from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R4, UC_ARM_REG_R6, UC_ARM_REG_R8, UC_ARM_REG_R10, UC_ARM_REG_PC, UC_ARM_REG_SP

from dk4tool.dialogue.review import REQUIRED_REVIEW_GATES, validate_natural_dialogue_batch
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.city_status_labels import NAMES, TABLE
from scripts import checkpoint_pending_shared_native_20261115 as census
from scripts import register_town_summary_20261119 as parent
from scripts import replay_town_shortage_20261119 as replay
from scripts.probe_button_prompt_native import BASE, STACK, call, machine

base, native = parent.base, parent.native
ARM, COMMON, CLEAN, PENDING = (getattr(parent.stage,key) for key in ('ARM','COMMON','CLEAN','PENDING'))
ROOT = replay.ROOT/'staged_v2'
ROM, PROOF = ROOT/'Town_Shortage_STAGED.nds', ROOT/'staged.json'
BODY = 0x02460020
SHORTAGE = 'Shortage'
SOURCE_WIDTH, WIDTH, HEIGHT = 36, 48, 12
TOWN_ROW = 0x11A694
TRADE_FRAME_WORD = 0xBB3A4
TRADE_FRAME, OBJECT_OFFSET = 0x25A8, 0x14
NEW_BITMAP_BYTES = WIDTH*HEIGHT//2
PATCHES = {
    TOWN_ROW+12: (24,120),
    TOWN_ROW+20: (SOURCE_WIDTH, WIDTH),
    0xC1AB0: (0xE3A00009, 0xE3A0000C),
    0xC1ADC: (0xE3A00024, 0xE3A00030),
    0x11AE9C: (100,112),
    0xC205C: (0xAD4,TRADE_FRAME-OBJECT_OFFSET),
    TRADE_FRAME_WORD: (TRADE_FRAME,TRADE_FRAME+NEW_BITMAP_BYTES),
}


def trade_entry(rom):
    targets = {0x020C0FE4,0x020C4680,0x020BB238}
    return [(name,address,target,kind) for name,start,data in census.components(rom.rom)
            for address,target,kind in census.branch_hits(data,start,targets)]


def read_string(arm,address):
    start = address-BASE
    return arm[start:arm.index(0,start,start+64)]


def transform(clean,current):
    assert unpack_from('<7i',current,TOWN_ROW) == (-1,68,62,24,12,SOURCE_WIDTH,HEIGHT)
    assert unpack_from('<4I',current,0x11AE94) == (64,166,100,178)
    assert current[0xBB238:0xBB244] == clean[0xBB238:0xBB244] == bytes.fromhex('f0412de960c19fe50cd04de0')
    assert current[0xBB398:TRADE_FRAME_WORD] == clean[0xBB398:TRADE_FRAME_WORD]
    expected_calls = [(0xBB2C4,0x020C0FE4),(0xBB290,0x020C4680)]
    assert all(census.branch_hits(current[site:site+4],BASE+site,{target}) == [(BASE+site,target,'arm_bl')] for site,target in expected_calls)
    image = bytearray(current)
    for index,(before,after) in PATCHES.items():
        assert unpack_from('<I',current,index) == unpack_from('<I',clean,index) == (before,)
        pack_into('<I',image,index,after)

    rows = parent.stage.rectangles(image)
    assert parent.stage.validate_rectangles(rows) == 16
    assert unpack_from('<4I',image,0x11AE94) == (64,166,112,178)
    trade_dest = (64,166,112,178)
    label_and_goods = [(16,166,52,178),(140,168,176,180),(144,126,216,162),(64,150,100,162)]
    for x,y,ex,ey in label_and_goods:
        assert trade_dest[2] <= x or ex <= trade_dest[0] or trade_dest[3] <= y or ey <= trade_dest[1]
    assert TRADE_FRAME % 8 == NEW_BITMAP_BYTES % 8 == 0
    assert TRADE_FRAME-OBJECT_OFFSET+NEW_BITMAP_BYTES == unpack_from('<I',image,TRADE_FRAME_WORD)[0]-OBJECT_OFFSET
    inverse = bytearray(image)
    for index,(before,_) in PATCHES.items():
        pack_into('<I',inverse,index,before)
    assert bytes(inverse) == current

    records = []
    phrases = [read_string(clean,ptr).decode('cp932') for ptr in unpack_from('<13I',clean,TABLE)]
    assert phrases[-1] == '通常'
    source_ptr = unpack_from('<I',clean,0xB6420)[0]
    ptr = unpack_from('<I',current,0xB6420)[0]
    assert read_string(clean,source_ptr).decode('cp932') == '品不足'
    assert read_string(current,ptr) == SHORTAGE.encode('ascii')
    source_ref = dict(offset=source_ptr-BASE,length=len(read_string(clean,source_ptr)),pointer_field=0xB6420)
    current_ref = dict(offset=ptr-BASE,length=8,pointer_fields=[0xB6420,0xB171C],
        Town_Summary_descriptor=TOWN_ROW, Trade_descriptor=0x11AE94)
    records.append(dict(id='CITY_COMPACT_SHORTAGE',file_path=ARM,speaker='City status field',clean_Japanese='品不足',
        source_meaning='Goods are in short supply. The narrow display groups the seven shortage types under this status.',
        context='Town Summary and Market Trade display the current settlement condition next to the Status heading.',
        previous_English=SHORTAGE,english=SHORTAGE,decision='revision',wording_changed=False,display_changed=True,
        localization_note='The generic noun matches the original compact description and contrasts clearly with Normal. Restore the last two letters.',
        source_reference=source_ref,current_reference=current_ref,staged_reference=current_ref,
        source_hex=read_string(clean,source_ptr).hex(),current_hex=read_string(current,ptr).hex(),
        review=dict.fromkeys(REQUIRED_REVIEW_GATES,True)))
    return bytes(image),records,phrases


def selectors(arm, phrases):
    u = machine(arm)
    results = []
    initial = bytearray(0x80)
    for value in range(256):
        initial[0x6A] = value
        u.mem_write(BODY,bytes(initial))
        call(u,0xB2D58,(BODY,))
        full = read_string(arm,u.reg_read(UC_ARM_REG_R0)).decode('ascii')
        assert full == (NAMES[value] if value < 13 else 'Normal')
        compact = SHORTAGE if len(full) >= 8 else full
        call(u,0xB16D8,(BODY,BODY+0x100,BODY+0x104))
        pointer,length = unpack_from('<2I',u.mem_read(BODY+0x100,8))
        assert length == len(compact) and read_string(arm,pointer).decode('ascii') == compact
        for start,end,register,output in ((0x020B61EC,0x020B6204,UC_ARM_REG_R8,UC_ARM_REG_R4),
                                          (0x0208D858,0x0208D870,UC_ARM_REG_R10,UC_ARM_REG_R6)):
            u.reg_write(UC_ARM_REG_SP,STACK)
            u.reg_write(register,BODY)
            u.emu_start(start,end,count=300)
            assert u.reg_read(UC_ARM_REG_PC) == end
            assert read_string(arm,u.reg_read(output)).decode('ascii') == compact
        assert bytes(u.mem_read(BODY,len(initial))) == initial
        if value < 13:
            results.append(dict(status=value,source_Japanese=phrases[value],full=full,compact=compact,pixels=6*len(compact)))
    font = GameAsciiFont.from_arm9(arm)
    for row in results:
        caption = row['compact']
        rectangles = [font.decode(char).getbbox() for char in caption]
        assert all(rect for rect in rectangles) and row['pixels'] <= WIDTH
        assert all(6*i+rect[2] <= WIDTH and 1+rect[3] <= HEIGHT for i,rect in enumerate(rectangles))
    return results


def main():
    assert not ROOT.exists()
    previous,ledger = map(base.load,(parent.RELEASE,base.LEDGER))
    assert base.digest(parent.ROM) == previous['candidate_sha256'] == ledger['current_integrated_candidate']['sha256']
    assert base.digest(base.REGISTRY) == previous['registry_sha256']
    assert base.digest(CLEAN) == previous['clean_input_sha256']
    clean,parent_image = map(base.NdsImage.open,(CLEAN,parent.ROM))
    entry_points = trade_entry(clean)
    assert entry_points == trade_entry(parent_image) == [('ARM9 section 0',site,target,'arm_bl') for site,target in
        ((0x020BA40C,0x020BB238),(0x020BB290,0x020C4680),(0x020BB2C4,0x020C0FE4))]
    arm = parent_image.read_file(ARM)
    target,records,phrases = transform(clean.read_file(ARM),arm)
    choices = selectors(target,phrases)
    parent.stage.verify_runtime(target,previous)
    parent_image.replace_file(ARM,target)
    binary = bytes(parent_image.rom.save())
    parent_image.replace_file(ARM,arm)
    assert bytes(parent_image.rom.save()) == parent.ROM.read_bytes()
    review = dict(translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',
        review_gates=sorted(REQUIRED_REVIEW_GATES),candidate_sha256=native.digest(binary),records=records)
    validate_natural_dialogue_batch(review)
    ROOT.mkdir(parents=True)
    ROM.write_bytes(binary)
    base.save(PROOF,review|dict(parent_sha256=previous['candidate_sha256'],clean_input_sha256=previous['clean_input_sha256'],
        target_ARM9_sha256=native.digest(target),entire_parent_inverse=True,exact_entry_paths=entry_points,
        atlas_bound=[228,72],atlas_rectangles=16,native_status_domain=256,native_statuses=choices,
        original_trade_stack_bytes=TRADE_FRAME,added_trade_stack_bytes=NEW_BITMAP_BYTES,
        source_proofs={str(p):base.digest(p) for p in (parent.RELEASE, CLEAN)}))
    print('Town Summary and Trade now reserve the eight original-size glyph cells needed by Shortage.')


if __name__ == '__main__':
    main()
