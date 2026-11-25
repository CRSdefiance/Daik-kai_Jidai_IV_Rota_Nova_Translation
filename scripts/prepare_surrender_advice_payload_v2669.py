"""One prose change;repack only its existing COMMON block with exact copy guards."""
import struct
from pathlib import Path
from copy import deepcopy
from ndspy.code import MainCodeFile
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.script.common_message_table import DIRECTORY_OFFSET,TABLE_OFFSET
from scripts.current_common_native_context_v2620b import CurrentContext
from scripts.battle_aftermath_native_plan_v1255 import compiled
from scripts.probe_common_single_cache_v862 import Loader
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/surrender_advice_payload_v2669')
DOC=Path('translations/aftermath_remaining_contextual_editorial_manuscript_v1.json')
BASE=0x02000000

if __name__=='__main__':
    assert not ROOT.exists()
    ctx=CurrentContext(DOC,'out/all_routes_combined_v1807_candidate.nds',ROOT/'source_context')
    doc=read(DOC);row=next(r for r in doc['records'] if r['message_id']==2029)
    assert doc['revised_IDs']==[2029] and row['english']=='You cannot win! I suggest you surrender at once!'
    container=IlnkContainer.parse(ctx.common);blocks=list(container.blocks);before=ctx.entries
    selected=2029;block=before[selected].block;assert block==22
    members=[r.message_id for r in before if r.block==block];assert members==list(range(1977,2100))
    arm=bytearray(ctx.arm);body=bytearray();patches=[]
    def put(at,value):
        old=bytes(arm[at:at+len(value)])
        if old!=value:
            patches.append(dict(address=BASE+at,offset=at,source_hex=old.hex(),target_hex=value.hex()))
            arm[at:at+len(value)]=value
    for n in members:
        r=before[n];payload=blocks[block][r.block_offset:r.copy_end]
        assert payload.startswith(r.text+b'\0')
        if n==selected:payload=compiled(row)+b'\0'
        put(TABLE_OFFSET+2*n,struct.pack('<H',len(body)));body.extend(payload)
    assert len(body)==5392 and len(body)<8192
    put(DIRECTORY_OFFSET+4*block,struct.pack('<HH',members[0],len(body)))
    blocks[block]=bytes(body);newcommon=IlnkContainer(blocks).to_bytes();newarm=bytes(arm)
    directory=sha(newarm[DIRECTORY_OFFSET:TABLE_OFFSET]);after=owned_entries(newcommon,newarm,directory)
    assert len(after)==len(before)==3668
    for old,new in zip(before,after,strict=True):
        assert new.text==(compiled(row) if old.message_id==selected else old.text)
        if old.message_id!=selected:
            assert container.blocks[old.block][old.block_offset:old.copy_end]==blocks[new.block][new.block_offset:new.copy_end]
    assert all(a==b for i,(a,b) in enumerate(zip(container.blocks,blocks,strict=True)) if i!=block)
    restored=bytearray(newarm)
    for p in patches:
        at=p['offset'];restored[at:at+len(bytes.fromhex(p['source_hex']))]=bytes.fromhex(p['source_hex'])
    assert bytes(restored)==ctx.arm and cache_plan(newarm)==cache_plan(ctx.arm)
    oldsections,newsections=[MainCodeFile(a,BASE).sections for a in [ctx.arm,newarm]]
    assert [(s.ramAddress,len(s.data),s.bssSize) for s in oldsections]==[(s.ramAddress,len(s.data),s.bssSize) for s in newsections]
    assert all(a.data==b.data for a,b in zip(oldsections[1:],newsections[1:],strict=True))
    assert len(newsections[3].data)-48==123040
    armpath=ROOT/'ARM9_METADATA_RESEARCH_ONLY.bin';commonpath=ROOT/'COMMON_RESEARCH_ONLY.DK4'
    armpath.write_bytes(newarm);commonpath.write_bytes(newcommon)
    plan=deepcopy(ctx.plan)
    for p in plan['patches']:
        at=p['address']-BASE
        if 0<=at and at+len(bytes.fromhex(p['target_hex']))<=len(newarm):
            p['target_hex']=newarm[at:at+len(bytes.fromhex(p['target_hex']))].hex()
    ctx.arm,ctx.common,ctx.entries,ctx.plan=newarm,newcommon,after,plan
    context=read(doc['native_context_proof']);table=next(t for t in context['voice_tables'] if t['table']==0x021177E0)
    rep=next(c for c in table['all207_original_actor_choices'] if c['message_ID']==2029 and c['actor_ID']!=1)
    pipeline=ctx.speak(0x53F0C,rep['actor_object'],0x021177E0,None)
    owner=int.from_bytes(newarm[0x552A0:0x552A4],'little')
    loaded=bytes(ctx.machines[-1][0].mem_read(owner+0x2030,512)).split(b'\0')[0]
    assert loaded==compiled(row) and pipeline['input_hex']==loaded.hex()
    fonts=read('work/analysis/aftermath_remaining_fonts_v2668/native_layout_and_font_research.json')
    targetfont=next(c for c in fonts['complete_native_planes'] if c['message_ID']==selected)
    assert pipeline['formatted_hex']==targetfont['formatted_hex']
    copies=[Loader(newarm,newcommon).copy(n,after[n].text,mode) for mode in ['cold','warm'] for n in members]
    assert len(copies)==246
    save(ROOT/'payload_plan.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        source_ROM=doc['current_ROM'],source_ROM_sha256=doc['current_ROM_sha256'],source_ARM9_sha256=doc['current_ARM9_sha256'],source_COMMON_sha256=doc['current_COMMON_sha256'],
        target_ARM9=str(armpath),target_ARM9_sha256=sha(newarm),target_COMMON=str(commonpath),target_COMMON_sha256=sha(newcommon),
        source_directory_sha256=sha(ctx.rom.read_file('/__arm9__.bin')[DIRECTORY_OFFSET:TABLE_OFFSET]),directory_sha256=directory,
        actual_changed_message_IDs=[selected],changed_block=block,old_block_bytes=5378,new_block_bytes=len(body),
        old_native_copy_bytes=before[selected].copy_end-before[selected].block_offset,new_native_copy_bytes=after[selected].copy_end-after[selected].block_offset,
        unchanged_compiled_strings_and_exact_native_copies=3667,all40_other_COMMON_blocks_exact=True,
        all_ARM9_changes_are_declared_directory_or_offset_metadata=patches,
        all_other_ARM9_bytes_restore_exact=True,code_font_geometry_sections_BSS_cache_and_staged123040_unchanged=True,
        new2029_complete_source_selected_direct_actor_loader_printf_macro_wrap_pipeline=pipeline,
        new2029_loaded_template_hex=loaded.hex(),original_direct_actor=rep,
        bounded_research_context_plan=plan,source_context_plan=str(ctx.proof_path),source_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        native_cold_warm_copies_all123_repacked_records=copies,
        future_stage_must_run_after_full_registered_V2284_stack=True,
        registered_profile_ROM_clean_patch_and_startup_still_pending=True,
        no_playable_ROM_created_or_promoted=True,no_emulator_or_gameplay_outcome_claim=True,completion_credit_added=0,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('One-line research payload passes:COMMON22 +14bytes,3667other exact copies/40blocks preserved,metadata-only ARM9;new2029source-selected loader pipeline and246native copies pass. No playable ROM.')
