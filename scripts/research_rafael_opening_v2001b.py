"""Successor derives every intended current skip target from clean command order.

V2001 stopped before writing any artifact: its boundary gate exposed the second
inherited stale operand,0300 at6446. Keep both producers unchanged as evidence.
"""
from pathlib import Path

SOURCE=Path('scripts/research_rafael_opening_v2001.py')

if __name__=='__main__':
    text=SOURCE.read_text(encoding='utf-8')
    old="    command_by_offset={r['offset']:r for r in commands}"
    new="""    command_by_offset={r['offset']:r for r in commands}
    clean_commands=read('work/analysis/native_storyline_census_v1995/SC0_block044_clean_native.json')['commands']
    assert len(clean_commands)==len(commands)==182
    assert [(r['word'],len(r['ancestor_0100_offsets']))for r in clean_commands]==[(r['word'],len(r['ancestor_0100_offsets']))for r in commands]
    clean_to_current={a['offset']:b['offset']for a,b in zip(clean_commands,commands,strict=True)}
    intended_spans={}
    for original,now in zip(clean_commands,commands,strict=True):
        if original['word']not in(0x100,0x200,0x300,0x400):continue
        clean_span=struct.unpack_from('<H',bytes.fromhex(original['whole_command_hex']),2)[0]
        clean_target=original['offset']+4+clean_span
        assert clean_target in clean_to_current
        current_target=clean_to_current[clean_target]
        intended_spans[now['offset']]=current_target-now['offset']-4
        struct.pack_into('<H',normalized,now['offset']+2,intended_spans[now['offset']])
    assert intended_spans=={6442:4,6446:158,6604:76,6680:0}
    assert [i for i,(a,b)in enumerate(zip(source,normalized,strict=True))if a!=b]==[6448,6606]
    assert not complete_walk(arm,bytes(normalized))['errors']"""
    assert text.count(old)==1;text=text.replace(old,new)
    text=text.replace("intended_span=struct.unpack_from('<H',normalized,at+2)[0]", "intended_span=intended_spans[at]")
    text=text.replace("sum(e['inherited_stale_span_explicitly_repaired']for e in edges)==1", "sum(e['inherited_stale_span_explicitly_repaired']for e in edges)==2")
    text=text.replace('rafael_opening_relocation_v2001','rafael_opening_relocation_v2001b')
    text=text.replace('explicit_inherited_stale_span_repair=True,', "explicit_two_inherited_stale_spans_repaired=True,clean_to_current_native_command_correspondence=clean_to_current,\n        classified_current_spans=intended_spans,failed_predecessor_source=str(SOURCE),\n        failed_predecessor_sha256=sha(SOURCE.read_bytes()),")
    exec(compile(text,str(SOURCE),'exec'),{'__name__':'__main__','__file__':__file__,'SOURCE':SOURCE})
