"""Reuse the calibrated planner with source-owned virtual style prefixes and actor0."""
import inspect
import linecache
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts import plan_editorial_scene_prose_v9 as previous
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.audit_story_glyph_consistency import load
from dk4tool.patch.grand_race_menu_release import sha

def qualify_source(doc):
    clean=NdsImage.open('work/clean.nds')
    archive=IlnkContainer.parse(clean.read_file(doc['file_path']))
    zeros=set();bindings=[]
    for row in doc['records']:
        if row['kind']=='typed-choice-label':continue
        ref=row['source_reference'];block=archive.blocks[row['block']]
        raw=bytes.fromhex(row['source_hex'])
        assert block[ref['offset']:ref['offset']+len(raw)]==raw
        if row.get('native_object_kind')=='4100-style-alternative':
            header=bytes.fromhex(row['source_header_hex']);at=ref['command_offset']
            assert len(header)==20 and header[:2]==b'\0A' and block[at:at+20]==header
            assert header[19]==row['source_selector'] and header[18]==0
            offsets=struct.unpack_from('<8H',header,2)
            assert all(at+20+offsets[i]==ref['offset'] for i in row['source_style_indices'])
            assert block[ref['offset']+len(raw)]==0 and b'\0' not in raw
            bindings.append(dict(id=row['id'],source_reference=ref,source_header_hex=header.hex(),source_body_hex=raw.hex(),
                formatter_only_virtual_source_hex=(bytes([header[19]])+raw).hex(),prefix_not_stored_in_alternative=True))
        elif row['source_selector']==0:
            header=bytes.fromhex(row['source_complete_preamble_hex'])
            assert row['block']==126 and header.hex()=='0040ffff0000'
            assert block[ref['header_offset']:ref['header_offset']+6]==header
            assert raw[0]==0 and b'\0' not in raw[1:] and block[ref['offset']+len(raw)]==0
            zeros.add(raw)
            bindings.append(dict(id=row['id'],source_reference=ref,complete_source_preamble_hex=header.hex(),
                source_body_with_real_selector_hex=raw.hex(),actual_source_frame={13:4320,21:4800,29:5280,38:5760,49:6480}[row['source_record_index']]))
    assert len(zeros)==5 and len(bindings)==53
    return zeros,bindings

def formatting_source(row):
    raw=bytes.fromhex(row['source_hex'])
    if row.get('native_object_kind')=='4100-style-alternative':
        assert row['virtual_formatter_prefix_is_not_part_of_stored_alternative_text']
        return (bytes([row['source_selector']])+raw).hex()
    return raw.hex()

# The generated function is inspectable through v9's retained linecache.
source=checked_text(inspect.getsource(previous.main),{
    '    doc=load(args.manuscript)':
        '    doc=load(args.manuscript)\n    bound_zero_bodies,source_bindings=qualify_source(doc)',
    "'source_bound_existing_literal':source_bound_existing_literal,'page_cut_penalty':page_cut_penalty}":
        "'source_bound_existing_literal':source_bound_existing_literal,'page_cut_penalty':page_cut_penalty,'BOUND_ZERO_SOURCE_BODIES':bound_zero_bodies}",
    "            planning={**row,'english':row['planned_English_markup']}":
        "            planning={**row,'english':row['planned_English_markup'],'source_hex':formatting_source(row)}",
    '        records=rows,failures=failures,source_owned_planner=adapter,':
        '        records=rows,failures=failures,source_owned_planner=adapter,formatter_source_bindings=source_bindings,real_actor0_source_bound_not_terminator=True,virtual_style_prefixes_not_stored=True,',
})
env={**previous.main.__globals__,'__file__':__file__,'qualify_source':qualify_source,'formatting_source':formatting_source}
filename=__file__+'::same-planner-source-bound-prefix-inputs'
linecache.cache[filename]=(len(source),None,source.splitlines(keepends=True),filename)
exec(compile(source,filename,'exec'),env)
main=env['main']
if __name__=='__main__':main()
