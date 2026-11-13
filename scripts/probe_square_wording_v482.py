"""Unshipped Square wording trials in its actual unwrapped 12-pixel contract."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import POOL
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, call, machine


def main():
    path = Path('out/all_routes_combined_v474_candidate.nds')
    arm = NdsImage.open(path).read_file('/__arm9__.bin')
    assert sha(arm) == 'c425bd54d4158a342f38a3950a02160d264eb645bd946cabf84dbe24aeaea2ce'
    font = GameAsciiFont.from_arm9(arm)
    # Decode the current Square-specific paint BL rather than hardcode a stale helper.
    branch = struct.unpack_from('<I', arm, 0x5FDC4)[0]
    assert branch >> 24 == 0xEB
    delta = branch & 0xFFFFFF
    if delta & 0x800000:
        delta -= 0x1000000
    entry = 0x5FDC4 + 8 + delta * 4
    rows = []
    for text in ('Delic. Shop', 'Delicacy Shop', 'Fiber Shop', 'Textile Shop', 'Jewelry Shop'):
        u = machine(arm)
        u.mem_write(POOL,bytes(MainCodeFile(arm,0x02000000).sections[3].data[:-48]))
        header,view,ctx,string = 0x02450000,0x02453000,0x02454000,0x02455000
        original = struct.pack('<5I',4,16,12,0x02452000-header,20)
        u.mem_write(header-16,b'\xA5'*(20+384+32))
        u.mem_write(header,original+bytes(384))
        call(u,0xD3D80,(view,))
        u.mem_write(STACK,struct.pack('<4I',64,12,0,0))
        call(u,0xD3AFC,(view,header,0,0))
        u.mem_write(struct.unpack_from('<I',arm,0xD5088)[0]+4,struct.pack('<2I',6,12))
        call(u,0xD5160,(ctx,view,1))
        u.mem_write(string,text.encode('ascii')+b'\0')
        call(u,entry,(ctx,string))
        assert u.reg_read(UC_ARM_REG_R0)-string == len(text)
        assert bytes(u.mem_read(header,20)) == original
        assert bytes(u.mem_read(header-16,16)) == bytes(u.mem_read(header+404,16)) == b'\xA5'*16
        raw = bytes(u.mem_read(header+20,384))
        indices = [n for b in raw for n in (b&15,b>>4)]
        actual = {(i%64,i//64) for i,v in enumerate(indices) if v}
        expected = {(n*5+x,y)for n,c in enumerate(text)for y in range(11)for x in range(6)if font.decode(c).getpixel((x,y))}
        rows.append({'text':text,'complete_native_ink':actual==expected,'expected_ink':len(expected),
                     'actual_ink':len(actual),'missing_pixels':sorted(expected-actual),'unexpected_pixels':sorted(actual-expected)})
    assert rows[0]['complete_native_ink'] and rows[2]['complete_native_ink'] and rows[3]['complete_native_ink'] and rows[4]['complete_native_ink']
    assert not rows[1]['complete_native_ink'] and len(rows[1]['missing_pixels']) == 11
    proof = {'candidate':str(path),'candidate_sha256':sha(path.read_bytes()),'native_Square_paint_entry':entry+0x02000000,
             'caption_contract':{'width':64,'height':12,'glyph_tracking':-1,'unwrapped':True},'trials':rows,
             'ROM_changed':False,'replacement_wording_shipped':False,
             'scope':'Isolated native caption contract; replacement wording has no actual GPU or integration credit.'}
    output = Path('work/analysis/istanbul_square_v482/wording_trial.json')
    output.write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8')
    print('Current labels exact; Delicacy Shop expansion loses11 ink pixels. No wording shipped.')


if __name__ == '__main__':
    main()
