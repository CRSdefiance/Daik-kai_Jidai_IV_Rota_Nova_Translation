"""Relocate both market printf literals out of the live town-capture instruction."""
import struct
from ndspy.code import MainCodeFile
from dk4tool.patch.grand_race_menu_release import sha

BASE=0x02000000
OLD_FORMAT=0x01FFC6A0
CAPTURE=0x01FFC6AC
NEW_FORMAT=0x01FFD000
FIELDS=(0xC3EF8,0xC4074)
FORMAT=b'%s\n  %s %d%%\0'
PAYLOAD=FORMAT+bytes(-len(FORMAT)%4)
CURRENT_ARM9='12e986d9625937d2d4141f7093e07fc16a474a129ee08a1043702952ac53f78d'

def transform(source):
    if sha(source)!=CURRENT_ARM9:raise ValueError('Exact registered Maria301 ARM9 required')
    code=MainCodeFile(source,BASE)
    if bytes(code.save())!=source:raise ValueError('Source native-section serialization is not exact')
    if len(code.sections)!=5 or code.sections[4].ramAddress!=0x01FFC000 or len(code.sections[4].data)!=0x1000:
        raise ValueError('Exact five-section current autoload geometry required')
    before=[(s.ramAddress,bytes(s.data),s.bssSize) for s in code.sections]
    old=bytes(code.sections[4].data)
    if old[0x6A0:0x6AC]!=FORMAT[:-1] or old[0x6AC:0x6B0]!=bytes.fromhex('0c209fe5'):
        raise ValueError('Expected complete format prefix and live town-capture opcode required')
    if NEW_FORMAT+len(PAYLOAD)>BASE:raise ValueError('Data must stay inside original ITCM mapping')
    for s in code.sections:
        if not (s.ramAddress+len(s.data)+s.bssSize<=NEW_FORMAT or NEW_FORMAT+len(PAYLOAD)<=s.ramAddress):
            raise ValueError('New declared literal allocation overlaps a current section orBSS')
    pointer_changes=[]
    for field in FIELDS:
        if struct.unpack_from('<I',source,field)[0]!=OLD_FORMAT:raise ValueError('Original market format pointer changed')
        pointer_changes.append(dict(offset=field,before_hex=source[field:field+4].hex(),after_hex=struct.pack('<I',NEW_FORMAT).hex()))
        struct.pack_into('<I',code.sections[0].data,field,NEW_FORMAT)
    code.sections.append(MainCodeFile.Section(PAYLOAD,NEW_FORMAT,0))
    target=bytes(code.save());parsed=MainCodeFile(target,BASE)
    if len(parsed.sections)!=6:raise ValueError('Declared new literal section missing')
    for index,(address,data,bss) in enumerate(before):
        section=parsed.sections[index]
        if section.ramAddress!=address or section.bssSize!=bss:raise ValueError('Existing section geometry changed')
        restored=bytearray(section.data)
        if index==0:
            for field in FIELDS:restored[field:field+4]=source[field:field+4]
            settings=code.codeSettingsOffs
            restored[settings:settings+12]=before[0][1][settings:settings+12]
        if bytes(restored)!=data:raise ValueError('Unowned existing section bytes changed')
    added=parsed.sections[5]
    if (added.ramAddress,bytes(added.data),added.bssSize)!=(NEW_FORMAT,PAYLOAD,0):raise ValueError('New read-only literal allocation differs')
    # Restore the two pointers and remove the declared data section to prove the
    # complete prior serialized ARM9, including its original autoload table.
    for field in FIELDS:struct.pack_into('<I',parsed.sections[0].data,field,OLD_FORMAT)
    parsed.sections.pop()
    if bytes(parsed.save())!=source:raise ValueError('Whole predecessor ARM9 inverse failed')
    return target,dict(source_ARM9_sha256=sha(source),target_ARM9_sha256=sha(target),pointer_changes=pointer_changes,
        declared_readonly_literal_section=dict(address=NEW_FORMAT,bytes=len(PAYLOAD),hex=PAYLOAD.hex(),bss=0),
        old_town_capture_instruction_andall_existing_ITCM_bytes_preserved=True,
        existing_geometry_andall_code_fonts_trade_logic_unchanged_except_two_literal_pointers=True,
        whole_serialized_parent_inverse_exact=True,no_editorial_credit=True)
