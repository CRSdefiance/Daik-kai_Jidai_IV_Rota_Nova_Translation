"""Check original dispatch and complete post-substitution Tavern word rasters."""

import json
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.probe_button_prompt_native import STACK, call, machine
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_repair_wait_native_v474 import scope
from scripts.verify_tavern_addresses_v413 import wrap

OUT = Path('work/analysis/tavern_family_v508')


def main():
    rom = NdsImage.open('out/all_routes_combined_v502_candidate.nds')
    old = rom.read_file('/__arm9__.bin')
    arm = (OUT/'target_arm9.bin').read_bytes()
    entries = common_message_entries((OUT/'target_common.bin').read_bytes(),arm,clean=False)
    dispatch = []
    for parent in (0x02054014,0x02054044):
        changed = []
        for number in range(3668):
            a,b = scope(old,parent,number),scope(arm,parent,number)
            if parent == 0x02054014 and 822 <= number <= 869:
                assert a[0] == 0x01FF9EDC and b[0] == 0x01FFCF78
                changed.append(number)
            else:
                # r3 is dispatch scratch and is overwritten before use in the
                # active formatter. Compare the actual selected code path.
                assert a[0] == b[0],(parent,number,a,b)
        dispatch.append({'parent':parent,'all3668_dispatches_compared':True,'newly_wrapped_messages':changed})
    u = machine(arm)
    dest,fmt = STACK+0x1000,STACK+0x2000
    args = [STACK+0x2200+i*0x100 for i in range(6)]
    cases,failures = [],[]
    for number in range(820,874):
        template = entries[number].text.rstrip()
        for long in (False,True):
            value = b'Lisbon' if not long else b'Black Glacier Sword'
            if number == 827:
                value = b'Hodram' if not long else b'Camille'
            if 852 <= number <= 858:
                value = b'12345'
            values = [value]*6
            if number == 843:
                # Clean843 has one item and four location/direction parts,
                # not five item names. These are explicitly supplied layout
                # contracts; this does not prove the native argument provider.
                values = [b'Pocket Watch' if not long else b'Black Glacier Sword',
                          b'north',b'52' if not long else b'90',
                          b'east' if not long else b'west',b'5' if not long else b'180',b'']
            for pointer,argument in zip(args,values):
                u.mem_write(pointer,argument+b'\0')
            u.mem_write(fmt,template+b'\0')
            u.mem_write(STACK,struct.pack('<4I',*args[2:]))
            u.mem_write(dest-16,b'\xA5'*544)
            call(u,0xD7720,(dest,fmt,args[0],args[1]))
            expanded = template
            for argument in values:
                expanded = expanded.replace(b'%s',argument,1)
            assert bytes(u.mem_read(dest,len(expanded)+1)) == expanded+b'\0'
            assert bytes(u.mem_read(dest-16,16)) == b'\xA5'*16
            assert bytes(u.mem_read(dest+len(expanded)+1,527-len(expanded))) == b'\xA5'*(527-len(expanded))
            formatted = wrap(arm,expanded,0x02054014,number)
            assert b' '.join(formatted.split()) == b' '.join(expanded.split()),(number,expanded,formatted)
            events = []
            pixels = raster(arm,formatted,0x01FFCE40-0x02000000,size=(228,160),instruction_limit=1000000,glyph_events=events)
            visible = [e for e in events if e['code'] not in (32,10)]
            expected = [c for c in expanded if c not in (32,10)]
            chars_match = [e['code'] for e in visible] == expected
            words_match = True
            offset = 0
            for word in expanded.split():
                group = visible[offset:offset+len(word)]
                words_match &= len(group) == len(word) and len({e['y'] for e in group}) == 1
                offset += len(word)
            row = {'message':number,'long_argument':long,'expanded':expanded.decode(),
                   'supplied_arguments':[v.decode()for v in values],
                   'formatted':formatted.decode(),'all_visible_characters_in_order':chars_match,
                   'every_word_on_one_row':words_match,'ink_pixels':sum(bool(p)for p in pixels)}
            cases.append(row)
            if not(chars_match and words_match):
                failures.append(row)
    proof = {'target_arm9_sha256':sha(arm),'dispatch':dispatch,'cases':cases,
             'argument_values_are_layout_contracts_not_native_provider_verification':True,
             'original_four_row_and236_byte_limits_preserved':True,
             'failures':failures,'production_ROM_modified':False,'full_goal_complete':False}
    (OUT/'native_proof.json').write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'cases':len(cases),'failures':failures},indent=2))
    assert not failures,'Tavern family does not yet preserve every complete word/glyph.'


if __name__ == '__main__':
    main()
