"""Bind Hodram_B46's original picture181 descriptor and clean/current Red Dye identity; no inventory or full-resource claim."""
import inspect,struct
from pathlib import Path
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.generic_speaker_label_data_v1 import BASE,POOL,cstring
from scripts.papal_trade_route_native_context_v7626 import RouteCurrentContext
from scripts.prove_lil_B145_picture_controls_v3587 import picture
from scripts.verify_village_wrap_v608 import read,save
from scripts.source_locked_derivation_v5118 import checked_text
ROOT=Path('work/analysis/Hodram_B46_pigment_v8190b')
SOURCE=Path('work/analysis/Hodram_B46_clean_context_v8179/complete_clean_SC1_B46_EV1_andcoverage_before_current_English.json')
GLOSS=Path('work/analysis/Hodram_B137_B45_B46_clean_gloss_v8183/28_first_clean_glosses_six_identities_explicit_prerequisite_graph_before_current_English.json')
INPUT=Path('work/analysis/current_V8172_Hodram_native_v8187/current_native_input.json')
CATALOG=Path('translations/all_item_names_arm9_v1.json')
if __name__=='__main__':
    assert not ROOT.exists();source,gloss,inp,cat=map(read,[SOURCE,GLOSS,INPUT,CATALOG])
    assert gloss['source_packets']['46']['sha256']==sha(SOURCE.read_bytes()) and gloss['source_only_no_current_body_orname_comparison_no_localized_manuscript']
    current,clean=[NdsImage.open(p) for p in [inp['current_ROM'],'work/clean.nds']]
    assert sha(Path(inp['current_ROM']).read_bytes())==inp['current_ROM_sha256']
    arm,ja=[im.read_file('/__arm9__.bin') for im in [current,clean]]
    g=source['groups'][0];block=bytes.fromhex(g['clean_block_hex']);c=next(c for c in g['commands'] if c['word']==0x4800)
    assert c['offset']==140 and c['whole_command_hex']=='0048b5a8' and c['native_extent']==4
    spans=[(0x29FFC,0x2A0F8),(0x28A64,0x28A8C),(0x28E8C,0x28F0C),(0x4A930,0x4AA74)]
    assert all(arm[a:b]==ja[a:b] for a,b in spans)
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')
    picture_adapter=checked_text(inspect.getsource(picture),{'assert word in [0x4821,0x4822,0x4823,0x4700]':'assert word==0x4800'});env=dict(picture.__globals__);exec(compile(picture_adapter,__file__+'::original-exact-source4800','exec'),env)
    native=ctx.execute(env['picture'],block,c);ctx.machines.pop();assert not ctx.machines
    request=native['original_picture_boundary_calls'][0]
    assert request['descriptor']==[0,181,1,5] and request['layout']==[0,0,0] and request['resource_body_unexecuted']
    at=0x11E210+181*24;metadata=ja[at:at+24];ptr=struct.unpack_from('<I',metadata)[0];jp=cstring(ja,ptr-BASE)
    assert jp[:-1].decode('cp932')=='紅色の顔料'
    registered=next(r for r in cat['records'] if r['offset']==at and r['id'].startswith('DK4_ITEM_POINTER_'))
    assert ja[at:at+4].hex()==registered['source_hex'].lower() and registered['english']=='Red Dye'
    cp=struct.unpack_from('<I',arm,at)[0];payload=bytes(MainCodeFile(arm,BASE).sections[3].data[:-48]);assert len(payload)==123264
    value=cstring(payload,cp-POOL) if POOL<=cp<POOL+len(payload) else cstring(arm,cp-BASE)
    assert value==b'Red Dye\0' and arm[at+4:at+24]==metadata[4:]
    instructions=[dict(address=i.address,mnemonic=i.mnemonic,operands=i.op_str) for i in Cs(CS_ARCH_ARM,CS_MODE_ARM).disasm(ja[0x28E8C:0x28F0C],BASE+0x28E8C)]
    assert any(i['address']==BASE+0x28EB4 and i['operands']=='r0, #3' for i in instructions)
    assert any(i['address']==BASE+0x28EE0 and i['operands']=='r1, #0xda' for i in instructions)
    assert any(i['address']==BASE+0x28EF8 and i['mnemonic']=='bl' and i['operands']=='#0x204a930' for i in instructions)
    save(ROOT/'original4800_descriptor181_clean_current_Red_Dye_andbounded_consumer_path.json',dict(
        source_packet=str(SOURCE),source_packet_sha256=sha(SOURCE.read_bytes()),source_gloss=str(GLOSS),source_gloss_sha256=sha(GLOSS.read_bytes()),
        current_ROM=inp['current_ROM'],current_ROM_sha256=inp['current_ROM_sha256'],native_picture_case=native,
        fresh_picture_cases=1,clean_native_picture_case_not_reexecuted_exact_code_bytes_bound=True,
        original_descriptor_category0_index181_andlayout0_0_0=request,
        clean_current_consumer_code_spans=[dict(start=a,end=b,sha256=sha(arm[a:b])) for a,b in spans],
        original_category0_consumer_bounds0_to217_passes_index_to4A930=True,clean_category_dispatch_instructions=instructions,
        item_ID=181,metadata_field=at,clean_metadata_hex=metadata.hex(),current_metadata_hex=arm[at:at+24].hex(),
        source_name_pointer=ptr,source_name_offset=ptr-BASE,source_terminated_hex=jp.hex(),source_Japanese=jp[:-1].decode('cp932'),
        current_name_pointer=cp,current_terminated_hex=value.hex(),current_English='Red Dye',registered_item_record_ID=registered['id'],
        registered_item_batch=str(CATALOG),registered_item_batch_sha256=sha(CATALOG.read_bytes()),
        source_picture_index_anditem181_metadata_concordant_unchanged_original_category0_consumer_bound=True,
        native_descriptor_boundary_only_full_resource_body_inventory_award_card_bounds_andnatural_activation_not_claimed=True,
        original_A000_00a0ffff0100b530_preserved_not_independently_interpreted_as_inventory_award=True,
        no_new_item_asset_localization_or_duplicate_item_credit=True,current_Hodram_B46_English_dialogue_body_still_unread=True,
        source_owned_picture_adapter=picture_adapter,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,GLOSS,INPUT,CATALOG,Path(__file__)]},new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('Hodram_B46 original4800:descriptor[0,181,1,5]/layout[0,0,0];clean紅色の顔料/currentRedDye exact. Original category0/index bounds/call path bound;resource/inventory effect/card/actual scene unclaimed.')
