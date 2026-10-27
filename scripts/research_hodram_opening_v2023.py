"""Three-block171-command research relocation,24 sites and360 native cases."""
from pathlib import Path
import struct
import textwrap
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.census_native_storylines_v1995 import complete_walk
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from scripts.verify_name_catalog_glyphs_v278 import raster,expected_pixels
from scripts.verify_village_wrap_v608 import read,save
from scripts import probe_hodram_opening_FE_v2022 as fe_helper

ROOT=Path('work/analysis/hodram_opening_relocation_v2023')
PARENT=Path('out/all_routes_combined_v2013_candidate.nds')
ROM=ROOT/'hodram_opening_V2013_derived_RESEARCH_ONLY.nds'
SOURCE=Path('work/analysis/hodram_opening_source_v2017b/all73_clean_current_opening_and_Lil_encounter_source.json')
DOC=Path('translations/hodram_opening_contextual_editorial_manuscript_v1.json')
FONT=Path('work/analysis/hodram_opening_fonts_v2021/all67_progressive_native_macros_and_complete_font_planes.json')
FE=Path('work/analysis/hodram_opening_FE_v2022/all6_separate_FE_native_planes_and48_macro_calls.json')
OWNER,STREAM,RESULT,LENGTH=0x02650000,0x02660000,0x02668000,0x02668100

if __name__=='__main__':
    assert not ROOT.exists()
    packet,doc,font,fe=map(read,(SOURCE,DOC,FONT,FE))
    assert font['manuscript_sha256']==fe['manuscript_sha256']==sha(DOC.read_bytes())
    assert len(font['cases'])==67 and not font['failures']and len(fe['cases'])==6 and not fe['failures']
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']==font['candidate_sha256']
    image=NdsImage.open(PARENT);arm=image.read_file('/__arm9__.bin');old_file=image.read_file('/data/SC1.DK4')
    assert sha(old_file)==packet['current_SC1_sha256']
    container=IlnkContainer.parse(old_file);fonts={r['id']:r for r in font['cases']};papers={r['id']:r for r in fe['cases']}
    # Reuse the already proven separate paper renderer to test only the final
    # encoder-owned parity space as well. No progressive FE fallback is used.
    observed=read(fe_helper.OBS);captured=next(r for r in observed['rows']if r.get('complete_readonly_snapshots'))
    data=fe_helper.snapshots(captured);bitmap=struct.unpack('<25I',bytes.fromhex(captured['bitmap_100_hex']))
    descriptor=bitmap[4];header=struct.unpack_from('<5I',data['WRAM'],descriptor-0x02000000)
    helper_source=Path(fe_helper.__file__).read_text(encoding='utf-8')
    start=helper_source.index('    def render(body):');stop=helper_source.index('    try:\n        for row in doc[',start)
    helper_source=textwrap.dedent(helper_source[start:stop])
    env={**fe_helper.__dict__,'arm':arm,'data':data,'captured':captured,'ctx':captured['context'],
        'pixels_address':(descriptor+header[4])&0xffffffff,'ascii_font':fe_helper.GameAsciiFont.from_arm9(arm)}
    exec(compile(helper_source,'source_bound_FE_final_parity_v2023','exec'),env)
    render_fe=env['render'];blocks=[];cpu=machine(arm)
    for spec in packet['packets']:
        number=spec['block'];source=container.blocks[number];commands=spec['native_commands']['current']['commands']
        old_commands=spec['native_commands']['clean']['commands']
        assert [(r['offset'],r['word'],r['native_extent'],r['ancestor_0100_offsets'])for r in commands]==[(r['offset'],r['word'],r['native_extent'],r['ancestor_0100_offsets'])for r in old_commands]
        by_at={r['offset']:r for r in commands};patches=[];texts=[]
        for row in doc['records']:
            if row['block']!=number:continue
            at=row['current_reference']['header_offset'];command=by_at[at];length=command['native_extent']
            assert command['word']==0x4000 and source[at:at+6].hex()==row['source_complete_preamble_hex']
            offset=row['current_reference']['offset'];old=bytes.fromhex(row['current_text_hex'])
            assert source[offset:offset+len(old)]==old and source[offset+len(old)]==0
            modal=row['source_presentation_prefix_hex']=='fe'
            proof=papers[row['id']]if modal else fonts[row['id']]
            encoded=bytes.fromhex(proof['encoded_hex'])[1:]if modal else bytes.fromhex(proof['encoded_text_excluding_speaker_hex'])
            body=encoded+(b' 'if len(encoded)%2!=len(old[1:])%2 else b'')
            assert b'\0'not in body and len(body)%2==len(old[1:])%2
            target=source[at:at+6]+body+b'\0';target+=b'\0'*(-len(target)%2)
            if modal:
                native,physical,glyphs=render_fe(body)
                assert sha(native)==proof['native_plane_sha256']and sha(physical)==proof['physical_mask_sha256']
            else:
                expanded=body.replace(b'FI',b'Hodram').replace(b'FA',b'Bergstrom').replace(b'FO',b'Bergstrom Fleet')
                native,glyphs,font_data=raster(arm,expanded);assert native==expected_pixels(arm,font_data,glyphs)
                assert sha(native)==proof['native_font_plane_sha256']
                assert all(0<=e['x']<=210 and 0<=e['y']<=48 for e in glyphs)
            patches.append(dict(start=at,end=at+length,old=source[at:at+length],new=target))
            texts.append(dict(id=row['id'],old_command_offset=at,old_native_extent=length,source_preamble_hex=source[at:at+6].hex(),
                source_record_index=row['source_record_index'],current_source_record_index=row['record_index'],
                target_hex=target.hex(),target_text_excluding_speaker_hex=body.hex(),parity_space_added=len(body)!=len(encoded),
                separate_FE_modal=modal,final_parity_native_plane_exact=True,native_plane_sha256=sha(native)))
        patches.sort(key=lambda p:p['start']);end=8+struct.unpack_from('<H',source,4)[0]
        def mapped(offset):
            delta=0
            for p in patches:
                assert not p['start']<offset<p['end'],('unclassified interior reference',number,offset)
                if offset>=p['end']:delta+=len(p['new'])-len(p['old'])
            return offset+delta
        pieces=[];last=0
        for p in patches:pieces.extend((source[last:p['start']],p['new']));last=p['end']
        pieces.append(source[last:end]);target=bytearray(b''.join(pieces))
        assert len(target)==mapped(end)and len(target)<0x2400
        boundaries={r['offset']for r in commands}|{end};fixups=[]
        for command in commands:
            if command['word']not in(0x100,0x200,0x300,0x400):continue
            at=command['offset'];span=struct.unpack_from('<H',source,at+2)[0];old_target=at+4+span
            assert old_target in boundaries and at+4 in boundaries
            new_at,new_target=mapped(at),mapped(old_target);new_span=new_target-new_at-4
            assert new_span%2==0 and 0<=new_span<=0xffff
            struct.pack_into('<H',target,new_at+2,new_span)
            fixups.append(dict(offset=at,word=command['word'],source_span=span,source_matched_target=old_target,source_unmatched_next=at+4,
                new_offset=new_at,target_span=new_span,new_matched_target=new_target,new_unmatched_next=new_at+4))
        struct.pack_into('<H',target,4,len(target)-8);logical_end=len(target);target=bytes(target)+b'\0'*(-len(target)%4)
        walked=complete_walk(arm,target);assert not walked['errors']and len(walked['commands'])==len(commands)
        new_by_at={r['offset']:r for r in walked['commands']};mapped_commands=[]
        for command in commands:
            at=command['offset'];new_at=mapped(at);new=new_by_at[new_at]
            assert new['word']==command['word']and new['native_extent']==mapped(at+command['native_extent'])-new_at
            assert new['ancestor_0100_offsets']==[mapped(a)for a in command['ancestor_0100_offsets']]
            if command['word']==0x4000:assert source[at:at+6]==target[new_at:new_at+6]
            elif command['word']not in(0x100,0x200,0x300,0x400):assert command['whole_command_hex']==new['whole_command_hex']
            mapped_commands.append(dict(word=command['word'],old_offset=at,new_offset=new_at,old_native_extent=command['native_extent'],new_native_extent=new['native_extent'],
                source_0100_ancestors=command['ancestor_0100_offsets'],target_0100_ancestors=new['ancestor_0100_offsets']))
        for row in texts:
            row['new_command_offset']=mapped(row['old_command_offset']);row['new_offset']=row['new_command_offset']+5
            row['new_record_index']=target[:row['new_offset']].count(b'\0')
        restored=bytearray(target[:logical_end]);struct.pack_into('<H',restored,4,end-8)
        for edge in fixups:struct.pack_into('<H',restored,edge['new_offset']+2,edge['source_span'])
        for p in reversed(patches):
            at=mapped(p['start']);restored[at:at+len(p['new'])]=p['old']
        assert bytes(restored)==source[:end]
        native_cases=[]
        for label,bytes_value in(('clean',IlnkContainer.parse(NdsImage.open('work/clean.nds').read_file('/data/SC1.DK4')).blocks[number]),('current',source),('research',target)):
            cpu.mem_write(STREAM-16,b'\xa5'*(len(bytes_value)+32));cpu.mem_write(STREAM,bytes_value)
            for edge in fixups:
                at=edge['new_offset']if label=='research'else edge['offset'];span=struct.unpack_from('<H',bytes_value,at+2)[0]
                for previous in(0,1,2,3,0xffffffff):
                    cpu.mem_write(OWNER-16,b'\xa5'*64);cpu.mem_write(OWNER,struct.pack('<4I',0,STREAM+at,0,0));owner=bytes(cpu.mem_read(OWNER-16,64))
                    cpu.mem_write(RESULT-16,b'\xa5'*80);cpu.mem_write(RESULT,b'\0'*24);cpu.mem_write(LENGTH-16,b'\xa5'*36);cpu.mem_write(LENGTH,b'\0'*4)
                    call(cpu,0x2A510,(RESULT,OWNER,LENGTH,previous))
                    taken=edge['word']==0x100 or previous=={0x200:0,0x300:1,0x400:2}.get(edge['word'],-1)
                    extent=struct.unpack('<I',cpu.mem_read(LENGTH,4))[0];assert extent==4+(span if taken else 0)
                    assert bytes(cpu.mem_read(STREAM,len(bytes_value)))==bytes_value and bytes(cpu.mem_read(OWNER-16,64))==owner
                    assert bytes(cpu.mem_read(RESULT,24))==struct.pack('<6I',3,0,0,0,0,0)
                    for guard in(STREAM-16,STREAM+len(bytes_value),RESULT-16,RESULT+24,LENGTH-16,LENGTH+4):assert bytes(cpu.mem_read(guard,16))==b'\xa5'*16
                    native_cases.append(dict(version=label,offset=at,previous_result=previous,taken=taken,native_extent=extent,all_native_ABI_owner_input_and_output_guards_exact=True))
        blocks.append(dict(block=number,source_block_sha256=sha(source),target_block_sha256=sha(target),old_bytes=len(source),new_bytes=len(target),
            target_hex=target.hex(),text_records=texts,mapped_native_commands=mapped_commands,relative_skip_fixups=fixups,native_cases=native_cases,
            exact_inverse_restores_current_block=True,complete_final_parity_native_planes=True))
        container.blocks[number]=target
    assert sum(len(b['text_records'])for b in blocks)==73
    assert sum(len(b['mapped_native_commands'])for b in blocks)==171 and sum(len(b['relative_skip_fixups'])for b in blocks)==24
    assert sum(len(b['native_cases'])for b in blocks)==360
    ROOT.mkdir(parents=True);image.replace_file('/data/SC1.DK4',container.to_bytes());image.save(ROM)
    parent=NdsImage.open(PARENT);result=NdsImage.open(ROM)
    assert [p for _,p,value in parent.iter_files()if result.read_file(p)!=value]==['/data/SC1.DK4']
    assert all(result.read_file(p)==value for p,value in parent.iter_components())
    a,b=[IlnkContainer.parse(im.read_file('/data/SC1.DK4')).blocks for im in(parent,result)]
    assert len(a)==len(b)==325 and [n for n,(x,y)in enumerate(zip(a,b,strict=True))if x!=y]==[42,43,44]
    save(ROOT/'complete_three_block_typed_relocation_research.json',dict(parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),source_packet=str(SOURCE),source_packet_sha256=sha(SOURCE.read_bytes()),
        ARM9_sha256=sha(arm),source_SC1_sha256=sha(old_file),target_SC1_sha256=sha(result.read_file('/data/SC1.DK4')),blocks=blocks,
        all171_typed_commands24_relative_sites360_native_cases=True,all73_final_parity_native_planes_exact=True,
        all_three_current_blocks_restore_exactly=True,all322_other_blocks_other_files_and_components_exact=True,
        FE_final_parity_helper_source=helper_source,FE_source_helper_sha256=sha(Path(fe_helper.__file__).read_bytes()),
        loader_external_entry_actual_revised_and_registered_release_pending=True,not_a_playable_user_handoff=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(commands=171,texts=73,relative_sites=24,native_cases=360,block_sizes=[(b['block'],b['old_bytes'],b['new_bytes'])for b in blocks],research_only=True))
