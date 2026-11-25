"""Classify six raw Thumb-ADR decodes as original COceanScene vtable words."""
import inspect
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import verify_aftermath_isa_compiler_v1257 as previous
from scripts.verify_personal_gameplay_v841 import rtti
from scripts.verify_village_wrap_v608 import read


def classify(old,new,accesses):
    outside = lambda rows:sorted(r for r in rows if not r[-1])
    rows = outside(accesses[0])
    assert rows == outside(accesses[1])
    expected = [(0x02147DCC,0x02147E60),(0x02147DD0,0x02147E94),
        (0x02147DDC,0x02147EC0),(0x02147DE0,0x02147ED4),
        (0x02147DE4,0x02147EE8),(0x02147E2C,0x02147EC0)]
    assert [(r[2],r[3]) for r in rows] == expected
    a,b,c = (r.read_file('/__arm9__.bin') for r in (old,new,NdsImage.open('work/clean.nds')))
    assert a[0x147D58:0x147E54] == b[0x147D58:0x147E54] == c[0x147D58:0x147E54]
    context = read('work/analysis/battle_aftermath_context_v1248d/source_context_and_consumer_frames.json')
    raw = Path(context['snapshot']).read_bytes()
    assert sha(raw) == context['snapshot_sha256'] and rtti(raw,0x02147D5C) == '11COceanScene'
    owners = []
    at = raw.find(struct.pack('<I',0x02147D5C))
    while at >= 0:
        if struct.unpack_from('<I',raw,at+4)[0] == 0x02147DA4 and struct.unpack_from('<I',raw,at+16)[0] == 0x02147E4C:
            owners.append(0x02000000+at)
        at = raw.find(struct.pack('<I',0x02147D5C),at+1)
    assert owners == [0x0218DB10]
    words = []
    for at,target in expected:
        value = struct.unpack_from('<I',c,at-0x02000000)[0]
        assert value & 3 == 0 and 0x02000000 <= value < 0x02100000
        assert a[value-0x02000000:value-0x02000000+8] == c[value-0x02000000:value-0x02000000+8]
        words.append({'source_data_address':at,'original_ARM_function_pointer':value,
            'secondary_vtable_slot':(at-0x02147DA4)//4,'raw_false_Thumb_ADR_target':target})
    return {'snapshot':context['snapshot'],'snapshot_sha256':sha(raw),'live_original_COceanScene':owners[0],
        'primary_secondary_tertiary_vtables':[0x02147D5C,0x02147DA4,0x02147E4C],
        'source_current_target_complete_immutable_vtable_region_sha256':sha(c[0x147D58:0x147E54]),
        'raw_ADR_decodes_are_typed_source_function_pointer_words':words,
        'unclassified_external_Thumb_ADR_leads':[]}


if __name__ == '__main__':
    source = inspect.getsource(previous.main)
    old = 'assert outside(accesses[0]) == outside(accesses[1]) == []'
    assert source.count(old) == 1
    source = source.replace(old,'classified = classify(old,new,accesses)')
    old = "'source_target_Thumb_ADR_census':accesses,'all_external_Thumb_ADR_references_absent':True,"
    assert source.count(old) == 1
    source = source.replace(old,"'source_target_Thumb_ADR_census':accesses,'typed_source_vtable_classification':classified,'all_actual_external_Thumb_ADR_references_absent':True,")
    env = {**previous.__dict__,'__file__':__file__,'classify':classify,
        'ROOT':Path('work/analysis/battle_aftermath_isa_compiler_v1257b')}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
