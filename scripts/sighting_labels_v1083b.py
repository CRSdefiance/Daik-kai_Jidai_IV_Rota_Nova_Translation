"""Two source-owned equal-allocation labels;no code,pointer or section growth."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read

FIELDS=((0x14511C,'至近距離'.encode('cp932')+b'\0',b'vicinity\0'),
        (0x15E0A4,'武装Latina'.encode('cp932').ljust(16,b'\0'),b'Armed Latina\0'.ljust(16,b'\0')))


def apply(arm):
    proof=read('work/analysis/sighting_runtime_v1076/native_runtime_verification.json')
    assert sha(arm)==proof['research_ARM9_sha256']
    target=bytearray(arm);fields=[]
    for at,old,new in FIELDS:
        assert len(old)==len(new) and arm[at:at+len(old)]==old
        assert b'\0' in new and not any(new[new.index(0)+1:])
        target[at:at+len(new)]=new
        fields.append({'offset':at,'allocation_bytes':len(old),'source_hex':old.hex(),'target_hex':new.hex()})
    result=bytes(target);restore=bytearray(result)
    for at,old,new in FIELDS:restore[at:at+len(old)]=old
    assert bytes(restore)==arm and len(arm)==len(result)
    return result,{'source_ARM9_sha256':sha(arm),'research_ARM9_sha256':sha(result),'fields':fields,
        'all_instructions_pointers_sections_and_other_bytes_exact':True,'no_pool_or_staged_payload_growth':True}
