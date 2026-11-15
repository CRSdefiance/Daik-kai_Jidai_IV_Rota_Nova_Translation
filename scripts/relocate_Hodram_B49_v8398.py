"""Sparse research reconstruction of the complete B49 exchange, including its typed menu."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.Hodram_outcomes_registered_route_context_v8380 import RouteCurrentContext
from scripts.prove_Maria_story_branches_v7741 import native_skip
from scripts.prove_lil_B212_controls_v6603b import compile_menu
from scripts.prove_lil_B212_consumers_v6595 import choice_getters
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B49_relocation_v8398')
CURRENT=Path('work/analysis/Hodram_B49_choice_binding_v8387b/current_with_choices.json')
DOC=Path('translations/hodram_B49_editorial_manuscript_v2.json')
NATIVE=Path('work/analysis/Hodram_B49_native_review_v8397/native_body_review.json')
CONTROL=Path('work/analysis/Hodram_B49_source_controls_v8384/source_controls.json')
INPUT=Path('work/analysis/current_V8377_Hodram_native_v8380/current_native_input.json')

if __name__=='__main__':
    assert not ROOT.exists()
    packet,doc,native,control,inp=map(read,[CURRENT,DOC,NATIVE,CONTROL,INPUT])
    assert native['manuscript_sha256']==sha(DOC.read_bytes()) and native['reviewed_body_pages']==14
    assert len(doc['records'])==14 and len(doc['typed_choice_records'])==2
    assert all(not r['review']['formatting'] for r in doc['records']+doc['typed_choice_records'])
    assert inp['current_ROM_sha256']==doc['current_ROM_sha256']==packet['current_ROM_sha256']
    image=NdsImage.open(doc['current_ROM'])
    assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']
    archive=image.read_file('/data/SC1.DK4');arm=image.read_file('/__arm9__.bin')
    assert sha(archive)==packet['current_archive_sha256']==doc['current_archive_sha256']
    container=IlnkContainer.parse(archive);assert len(container.blocks)==325
    g=packet['groups'][0];assert len(packet['groups'])==1 and g['block']==49
    old=container.blocks[49];clean=bytes.fromhex(g['clean_block_hex'])
    oldend=g['current_logical_end'];cleanend=8+struct.unpack_from('<H',clean,4)[0]
    assert sha(old)==g['current_block_sha256'] and sha(clean)==g['clean_block_sha256']
    assert old==bytes.fromhex(g['current_block_hex']) and oldend==cleanend==984
    assert old[oldend:]==clean[cleanend:]==b'' and old[:8]==clean[:8]
    inventory,walker,fn=scoped_inventory()
    before,speeches=inventory(arm,old)
    assert before==g['all_current_commands'] and len(before)==36 and len(speeches)==14
    assert inventory(arm,clean)[0]==g['all_source_commands']==control['all_original_source_commands']
    patches=[];texts=[]
    for row in doc['records']:
        at=row['current_reference']['offset'];ja=row['source_reference']['offset']
        previous=bytes.fromhex(row['current_hex']);source=bytes.fromhex(row['source_hex'])
        value=bytes.fromhex(row['compiled_hex']);preamble=row['source_complete_preamble_hex']
        assert old[at:at+len(previous)+1]==previous+b'\0' and clean[ja:ja+len(source)+1]==source+b'\0'
        assert old[at-5:at+1].hex()==clean[ja-5:ja+1].hex()==preamble
        assert at==ja and len(previous)==len(source) and value[0]==previous[0]==source[0]==row['source_selector']
        assert value[0] in [1,2,254] and value[1:] and b'\0' not in value[1:]
        assert old[:at].count(b'\0')==row['current_record_index']
        assert clean[:ja].count(b'\0')==row['source_record_index']
        for macro in [b'FI',b'FA',b'FO']:assert source[1:].count(macro)==value[1:].count(macro)==0
        pad=len(value)%2!=len(previous)%2;stored=value+(b' ' if pad else b'')
        assert len(stored)%2==len(previous)%2
        patches.append(dict(id=row['id'],start=at,end=at+len(previous),old=previous,source=source,value=stored))
        texts.append(dict(id=row['id'],file_path=row['file_path'],block=49,source_reference=row['source_reference'],current_reference=row['current_reference'],source_selector=row['source_selector'],source_complete_preamble_hex=preamble,old_offset=at,old_length=len(previous),old_hex=previous.hex(),compiled_hex=value.hex(),new_length=len(stored),target_hex=stored.hex(),parity_space_added=pad))
    menu=packet['typed_choices'][0];oldmenu=menu['current_command'];jamenu=menu['source_command']
    choices=doc['typed_choice_records'];assert [r['option_index'] for r in choices]==[0,1]
    labels=[r['english'].encode('ascii') for r in choices];typed=compile_menu(0x2100,labels)
    at=oldmenu['offset'];previous=bytes.fromhex(oldmenu['whole_command_hex']);source=bytes.fromhex(jamenu['whole_command_hex'])
    assert at==jamenu['offset']==574 and len(previous)==len(source)==26 and len(typed)==22
    assert old[at:at+26]==previous and clean[at:at+26]==source
    patches.append(dict(id='B49-complete-native-menu',start=at,end=at+26,old=previous,source=source,value=typed))
    patches.sort(key=lambda p:p['start']);assert len(patches)==15 and all(a['end']<=b['start'] for a,b in zip(patches,patches[1:]))
    def mapped(at):
        delta=0
        for p in patches:
            if at<p['start']:break
            assert not p['start']<at<p['end'],'Interior reference in replaced body/menu'
            if at==p['start']:return at+delta
            delta+=len(p['value'])-len(p['old'])
        return at+delta
    chunks=[];last=0
    for p in patches:chunks.extend([old[last:p['start']],p['value']]);last=p['end']
    chunks.append(old[last:oldend]);logical=bytearray(b''.join(chunks))
    assert len(logical)==mapped(oldend)<0x2400
    fixups=[]
    boundaries={c['offset'] for c in before}|{oldend}
    for edge in control['operands_requiring_adjustment_when_resizing']:
        assert edge['block']==49 and edge['offset'] in boundaries and edge['matched_skip_target'] in boundaries
        assert old[edge['offset']:edge['offset']+4].hex()==edge['source_operand_hex']
        assert old[edge['offset']:edge['offset']+4]==clean[edge['offset']:edge['offset']+4]
        start=mapped(edge['offset']);finish=mapped(edge['matched_skip_target']);span=finish-start-4
        assert 0<=span<=0xffff and span%2==0 and struct.unpack_from('<H',logical,start)[0]==edge['word']
        struct.pack_into('<H',logical,start+2,span)
        fixups.append(dict(**edge,new_offset=start,new_unmatched_next=start+4,new_matched_skip_target=finish,target_span=span))
    assert len(fixups)==8
    struct.pack_into('<H',logical,4,len(logical)-8);target=bytes(logical)+bytes(-len(logical)%4)
    after,finalspeeches=inventory(arm,target);assert len(after)==36 and len(finalspeeches)==14
    maps=[]
    for previous,new in zip(before,after,strict=True):
        a,z=previous['offset'],new['offset'];word=previous['word']
        assert z==mapped(a) and new['word']==word
        assert new['native_extent']==mapped(a+previous['native_extent'])-z
        assert new['ancestor_0100_offsets']==[mapped(x) for x in previous['ancestor_0100_offsets']]
        br,nr=bytes.fromhex(previous['whole_command_hex']),bytes.fromhex(new['whole_command_hex'])
        if word==0x4000:assert br[:6]==nr[:6]
        elif word in [0x100,0x200,0x300,0x400]:assert br[:2]==nr[:2]
        elif word==0x2100:assert br==bytes.fromhex(oldmenu['whole_command_hex']) and nr==typed
        else:assert br==nr
        maps.append(dict(word=word,old_offset=a,new_offset=z,old_extent=previous['native_extent'],new_extent=new['native_extent'],source_0100_ancestors=previous['ancestor_0100_offsets'],target_0100_ancestors=new['ancestor_0100_offsets']))
    assert after[-1]['word']==0 and after[-1]['native_extent']==4 and after[-1]['offset']+4==len(logical)
    for row in texts:
        at=mapped(row['old_offset']);row.update(new_offset=at,new_record_index=target[:at].count(b'\0'))
        assert target[at:at+row['new_length']+1]==bytes.fromhex(row['target_hex'])+b'\0'
        assert target[at-5:at+1].hex()==row['source_complete_preamble_hex']
    mc=dict(word=0x2100,count=2,old_offset=oldmenu['offset'],old_length=26,new_offset=mapped(oldmenu['offset']),new_length=22,old_hex=oldmenu['whole_command_hex'],clean_hex=jamenu['whole_command_hex'],target_hex=typed.hex(),labels=[r['english'] for r in choices],record_IDs=[r['id'] for r in choices],label_references=[])
    for row in choices:
        i=row['option_index'];field=mc['new_offset']+2+2*i;base=mc['new_offset']+6
        relative=struct.unpack_from('<H',target,field)[0];at=base+relative;value=row['english'].encode('ascii')
        assert target[at:at+len(value)+1]==value+b'\0'
        for data,key,ref in [(old,'current_hex',row['current_reference']),(clean,'source_hex',row['source_reference'])]:
            raw=bytes.fromhex(row[key]);assert data[ref['offset']:ref['offset']+len(raw)+1]==raw+b'\0' and data[:ref['offset']].count(b'\0')==ref['record_index']
        mc['label_references'].append(dict(id=row['id'],option_index=i,source_reference=row['source_reference'],old_reference=row['current_reference'],new_offset=at,new_length=len(value),new_record_index=target[:at].count(b'\0'),relative_table_field=field,relative_base=base,relative_offset=relative,target_hex=value.hex()))
    for source_version,original in [(False,old),(True,clean)]:
        inverse=bytearray(target[:len(logical)]);inverse[:8]=original[:8]
        for fix in fixups:struct.pack_into('<H',inverse,fix['new_offset']+2,fix['source_span'])
        for patch in reversed(patches):
            at=mapped(patch['start']);inverse[at:at+len(patch['value'])]=patch['source'] if source_version else patch['old']
        end=8+struct.unpack_from('<H',original,4)[0]
        assert bytes(inverse)+original[end:]==original,'Complete clean/current block inverse'
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')
    byoffset={c['offset']:c for c in after};finalboundaries=set(byoffset)|{len(logical)};skipcases=[]
    for fix in fixups:
        result=ctx.execute(native_skip,target,byoffset[fix['new_offset']]);ctx.machines.pop()
        assert all(c['next_offset'] in finalboundaries and c['next_offset']==(fix['new_matched_skip_target'] if c['taken'] else fix['new_unmatched_next']) for c in result['cases'])
        skipcases.append(result)
    getters=choice_getters(arm,byoffset[mc['new_offset']])
    assert len(getters)==2 and all(c['count']==2 and [bytes.fromhex(r['hex']) for r in c['labels']]==labels for c in getters)
    assert not ctx.machines
    bp=ROOT/'SC1_B49_RESEARCH_ONLY.bin';bp.write_bytes(target)
    blocks=list(container.blocks);blocks[49]=target;newarchive=IlnkContainer(blocks).to_bytes();parsed=IlnkContainer.parse(newarchive)
    assert len(parsed.blocks)==325 and [i for i,(a,b) in enumerate(zip(container.blocks,parsed.blocks,strict=True)) if a!=b]==[49]
    inverse=list(parsed.blocks);inverse[49]=old;assert IlnkContainer(inverse).to_bytes()==archive
    ap=ROOT/'SC1_B49_RESEARCH_ONLY.DK4';ap.write_bytes(newarchive)
    group=dict(block=49,file_path='/data/SC1.DK4',source_block_sha256=sha(old),clean_block_sha256=sha(clean),target_block=str(bp),target_block_sha256=sha(target),source_header_hex=old[:8].hex(),target_header_hex=target[:8].hex(),source_bytes=len(old),source_logical_end=oldend,source_tail_bytes=len(old)-oldend,target_bytes=len(target),target_logical_end=len(logical),target_tail_bytes=len(target)-len(logical),text_records=texts,choice_commands=[mc],relative_fixups=fixups,relocated_skip_cases=skipcases,command_map=maps,all_current_commands=before,all_target_commands=after,source_current_andclean_block_inverse_exact=True)
    save(ROOT/'reconstruction.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),source_packet=str(CURRENT),source_packet_sha256=sha(CURRENT.read_bytes()),file_path='/data/SC1.DK4',source_archive_sha256=sha(archive),target_archive=str(ap),target_archive_sha256=sha(newarchive),groups=[group],other324_blocks_byte_exact=True,complete_predecessor_archive_inverse_exact=True,complete_clean_source_block_inverse_exact=True,source_relative_sites=8,relocated_native_skip_cases=sum(len(r['cases']) for r in skipcases),relocated_menu_getters=getters,all36_commands14_six_byte_preambles8_relatives1_query2_choices4_picture_hide_boundaries7_opaque_effects_andfull_terminal_preserved=True,source_FE_panels=1,source_macro_counts=dict(FI=0,FA=0,FO=0),parity_space_records=[r['id'] for r in texts if r['parity_space_added']],native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),research_archives_only_no_ROM_registration_orcredit=True,stored_fonts_choice_UI_actual_policy_atomic_andregistered_release_pending=True,evidence={str(p):sha(p.read_bytes()) for p in [CURRENT,DOC,NATIVE,CONTROL,INPUT,Path(__file__),Path(compile_menu.__code__.co_filename),Path(choice_getters.__code__.co_filename)]},new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('B49 reconstructed:14 speeches+2 choices,36 commands,8 relocated branches/40 cases;324 other blocks exact;both whole block inverses andparent archive exact. Parity tails:',sum(r['parity_space_added'] for r in texts),'No ROM/credit.')
