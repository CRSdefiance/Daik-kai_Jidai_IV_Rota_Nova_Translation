"""Independently rebuild both complete outcome scripts by native commands; no ROM/credit."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Hodram_registered_route_context_v8303 import RouteCurrentContext
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_outcome_relocation_v8326')
DOC=Path('translations/hodram_B47_B48_editorial_manuscript_v2.json')
CURRENT=Path('work/analysis/Hodram_B47_B48_current_v8317c/six_exact_source_current_effective_refs_after_whole_clean_gloss_andnative_source_view.json')
CONTROL=Path('work/analysis/Hodram_B47_B48_source_controls_v8314/two_EV1_entries15_commands6_preambles7_opaque_effect_pairs50_complete_seeded_ends.json')
VIEW=Path('work/analysis/Hodram_B47_B48_native_review_v8325/six_native_pages_directly_viewed_no_warning_waivers.json')
INPUT=Path('work/analysis/current_V8300_Hodram_native_v8303/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();doc,current,control,view,inp=map(read,[DOC,CURRENT,CONTROL,VIEW,INPUT])
    assert view['manuscript_sha256']==sha(DOC.read_bytes()) and view['all_six_complete_bodies_visually_read'] and not view['original_warnings'] and len(view['original_infos'])==6
    assert len(doc['records'])==6 and doc['current_ROM_sha256']==current['current_ROM_sha256']==inp['current_ROM_sha256'] and control['source_relative_sites']==control['source_raw_predicates']==0
    image=NdsImage.open(doc['current_ROM']);assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']
    arm=image.read_file('/__arm9__.bin');archive=image.read_file('/data/SC1.DK4');container=IlnkContainer.parse(archive);assert len(container.blocks)==325 and sha(archive)==doc['current_archive_sha256']
    inventory,walker,inventory_source=scoped_inventory();env=dict(end_case.__globals__);exec(compile(control['source_owned_seeded_end_adapter'],__file__+'::unchanged-complete-normal-end-carry','exec'),env)
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');blocks=list(container.blocks);groups=[]
    for spec in current['groups']:
        number=spec['block'];old=container.blocks[number];clean=bytes.fromhex(spec['clean_block_hex']);assert old==bytes.fromhex(spec['current_block_hex']) and number in [47,48]
        commands,speeches=inventory(arm,old);assert commands==spec['all_current_commands'] and len(speeches)==3
        sourcecommands=spec['all_source_commands'];assert len(commands)==len(sourcecommands) and all(c['word'] not in [0x100,0x200,0x300,0x400,0x8000,0x8100,0x2100,0x4100] for c in commands)
        chunks=[];texts=[];maps=[];offset=8
        for source,before in zip(sourcecommands,commands,strict=True):
            assert source['word']==before['word'];raw=bytes.fromhex(before['whole_command_hex']);source_raw=bytes.fromhex(source['whole_command_hex']);new=raw
            if before['word']==0x4000:
                row=next(r for r in doc['records'] if r['block']==number and r['current_reference']['header_offset']==before['offset'])
                prior=bytes.fromhex(row['current_hex']);compiled=bytes.fromhex(row['compiled_hex']);assert raw[5:5+len(prior)+1]==prior+b'\0' and raw[:6].hex()==row['source_complete_preamble_hex']
                assert compiled[0]==prior[0]==row['source_selector'] and row['source_selector'] in [2,254] and b'\0' not in compiled[1:]
                pad=len(compiled)%2!=len(prior)%2;stored=compiled+(b' ' if pad else b'');assert len(stored)%2==len(prior)%2
                assert stored[1:].count(b'FI')==bytes.fromhex(row['source_hex'])[1:].count(b'FI') and not any(m in stored[1:] for m in [b'FA',b'FO',b'%'])
                new=raw[:5]+stored+b'\0'+raw[5+len(prior)+1:];assert len(new)%2==0 and new[:6]==raw[:6]==source_raw[:6]
                texts.append(dict(id=row['id'],file_path=doc['file_path'],block=number,source_selector=row['source_selector'],source_complete_preamble_hex=row['source_complete_preamble_hex'],source_reference=row['source_reference'],current_reference=row['current_reference'],
                    old_offset=before['offset']+5,old_length=len(prior),old_hex=prior.hex(),compiled_hex=compiled.hex(),target_hex=stored.hex(),new_length=len(stored),new_offset=offset+5,parity_space_added=pad))
            else:assert raw==source_raw
            chunks.append(new);maps.append(dict(word=before['word'],clean_offset=source['offset'],old_offset=before['offset'],new_offset=offset,clean_extent=source['native_extent'],old_extent=before['native_extent'],new_extent=len(new),clean_0100_ancestors=source['ancestor_0100_offsets'],source_0100_ancestors=before['ancestor_0100_offsets'],target_0100_ancestors=[]));offset+=len(new)
        logical=bytearray(old[:8]+b''.join(chunks));struct.pack_into('<H',logical,4,len(logical)-8);target=bytes(logical)+bytes(-len(logical)%4);assert len(logical)==offset and len(target)<0x2400
        final,finalspeeches=inventory(arm,target);assert len(final)==len(commands) and len(finalspeeches)==3 and final[-1]['word']==0 and final[-1]['native_extent']==4 and final[-1]['offset']+4==len(logical)
        for c,m,chunk in zip(final,maps,chunks,strict=True):
            assert c['offset']==m['new_offset'] and c['word']==m['word'] and c['native_extent']==len(chunk) and bytes.fromhex(c['whole_command_hex'])==chunk and c['ancestor_0100_offsets']==[]
        for text in texts:
            at=text['new_offset'];stored=bytes.fromhex(text['target_hex']);text['new_record_index']=target[:at].count(b'\0');assert target[at:at+len(stored)+1]==stored+b'\0' and target[at-5:at+1].hex()==text['source_complete_preamble_hex']
        def inverse(source_version):
            original=clean if source_version else old;original_commands=sourcecommands if source_version else commands;body=[]
            for original_command,final_command in zip(original_commands,final,strict=True):
                raw=bytes.fromhex(final_command['whole_command_hex']);body.append(bytes.fromhex(original_command['whole_command_hex']) if final_command['word']==0x4000 else raw)
            end=8+int.from_bytes(original[4:6],'little');return original[:8]+b''.join(body)+original[end:]
        assert inverse(False)==old and inverse(True)==clean
        end=final[-1];ends=[env['end_case'](arm,target,end['offset'],p,v) for p in [0,1,2,3,0xFFFFFFFF] for v in [0,1,2,3,0xFFFFFFFF]]
        assert len(ends)==25 and all(c['native_extent']==4 and c['native_result'][0]==0 and c['native_result'][1]==c['initial_value_word'] for c in ends)
        path=ROOT/f'SC1_block{number}_RESEARCH_ONLY.bin';path.write_bytes(target);blocks[number]=target
        groups.append(dict(block=number,file_path=doc['file_path'],source_block_sha256=sha(old),clean_block_sha256=sha(clean),target_block=str(path),target_block_sha256=sha(target),
            source_header_hex=old[:8].hex(),target_header_hex=target[:8].hex(),source_bytes=len(old),source_logical_end=spec['current_logical_end'],source_tail_bytes=spec['current_tail_bytes'],target_bytes=len(target),target_logical_end=len(logical),target_tail_bytes=len(target)-len(logical),
            text_records=texts,relative_fixups=[],relocated_skip_cases=[],command_map=maps,all_source_commands=sourcecommands,all_current_commands=commands,all_target_commands=final,target_seeded_normal_ends=ends,
            source_current_andclean_block_inverse_exact=True,all_original_controls_sixbyte_preambles_full_ends_andseparate_tails_preserved=True,external_references_complete=False))
        print('RELOCATION',number,len(old),'->',len(target),'parity',sum(t['parity_space_added'] for t in texts),flush=True)
    targetarchive=IlnkContainer(blocks).to_bytes();parsed=IlnkContainer.parse(targetarchive);assert [i for i,(a,b) in enumerate(zip(container.blocks,parsed.blocks,strict=True)) if a!=b]==[47,48]
    restored=list(parsed.blocks)
    for group in groups:restored[group['block']]=container.blocks[group['block']]
    assert IlnkContainer(restored).to_bytes()==archive and not ctx.machines
    output=ROOT/'SC1_B47_B48_RESEARCH_ONLY.DK4';output.write_bytes(targetarchive)
    save(ROOT/'two_blocks6_speeches15_commands_full_source_parent_inverses.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],file_path=doc['file_path'],manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),source_archive_sha256=sha(archive),target_archive=str(output),target_archive_sha256=sha(targetarchive),groups=groups,
        only_blocks47_48_changed_all323_others_exact=True,all_full_predecessor_archive_andtwo_clean_source_block_inverses_exact=True,source_relative_sites=0,fresh_target_seeded_normal_end_cases=50,all15_commands6_complete_preambles_FE_FI_full_terminals_andtails_preserved=True,
        no_interior_orrelative_entry_assumed_from_linear_code=True,research_archive_only_no_ROM_orregistered_credit=True,external_references_complete=False,stored_fonts_final_dispatch_effect_semantics_loaders_census_actual_policy_atomic_andregistered_release_pending=True,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),inventory_walker=walker,inventory_function=inventory_source,new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [DOC,CURRENT,CONTROL,VIEW,INPUT,Path(__file__)]}))
