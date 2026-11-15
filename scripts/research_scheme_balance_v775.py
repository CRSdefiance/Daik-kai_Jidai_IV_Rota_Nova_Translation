"""In-memory formatting research only; scratch storage is not ROM ownership."""

import inspect
import re
import struct
from pathlib import Path

from keystone import Ks,KS_ARCH_ARM,KS_MODE_THUMB

from dk4tool.patch import shipyard_editorial as original
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_tavern_continuation_layout_v768 import format_case
from scripts.review_tavern_schemes_v774 import MANUSCRIPT
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/tavern_schemes_layout_v775')
SCRATCH=0x02478000


def program():
    source=inspect.getsource(original.assemble)
    pattern=r"    balance = bytes\(kt.asm\(f'''(.*?)''', BALANCE\)\[0\]\)"
    matched=re.findall(pattern,source,re.S)
    assert len(matched)==1
    assembly=matched[0].replace('{{','{').replace('}}','}')
    marker='line_end:\n'
    assert assembly.count(marker)==1
    assembly=assembly.replace(marker,marker+'ldr r0,extra_word\ncmp r7,r0\nbeq failed\n')
    assembly+='\n.align 2\nextra_word: .word 0x66726f6d\n'
    return bytes(Ks(KS_ARCH_ARM,KS_MODE_THUMB).asm(assembly,SCRATCH)[0]),assembly


def install(u,arm):
    code,assembly=program()
    # Only the source-owned literal wrapper's exact helper literal is selected.
    lo,hi=original.LITERAL,0x02147C20
    source=arm[lo-original.BASE:hi-original.BASE]
    needle=struct.pack('<I',original.BALANCE|1)
    assert source.count(needle)==1
    pointer=lo+source.index(needle)
    assert bytes(u.mem_read(pointer,4))==needle
    u.mem_write(SCRATCH,code)
    u.mem_write(pointer,struct.pack('<I',SCRATCH|1))
    return {'scratch_address':SCRATCH,'bytes':len(code),'code_hex':code.hex(),
        'literal_helper_pointer':pointer,'source_module_sha256':sha(Path(original.__file__).read_bytes()),
        'assembly_sha256':sha(assembly.encode()),'only_in_memory_research_not_production_storage_approval':True}


def main():
    arm=NdsImage.open('out/all_routes_combined_v773_candidate.nds').read_file('/__arm9__.bin')
    rows={r['message_id']:r for r in read(MANUSCRIPT)['records']}
    findings=read(ROOT/'layout_findings.json')
    results=[]
    for i,case in enumerate(findings):
        if i%64==0:
            u=machine(arm)
            receipt=install(u,arm)
        result=format_case(u,rows[case['id']],tuple(bytes.fromhex(s) for s in case['source_values_hex']))
        results.append({'before':case,'after':result})
    save(ROOT/'from_word_research.json',{'original_findings_count':len(findings),
        'remaining_findings':sum(bool(r['after']['findings']) for r in results),
        'receipt':receipt,'cases':results,'no_ROM_changed':True,
        'producer_sha256':sha(Path(__file__).read_bytes())})
    print('Adding from to the native weak-word check leaves',sum(bool(r['after']['findings']) for r in results),'of',len(findings),'warnings.',flush=True)


if __name__=='__main__':main()
