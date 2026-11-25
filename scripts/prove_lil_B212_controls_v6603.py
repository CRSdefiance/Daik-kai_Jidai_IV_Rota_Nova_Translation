"""Bind source menu returns, all four exchange paths, opaque effects and every end."""
import inspect,struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import checked_text
from scripts import verify_ship_advice_choice_centering_20261022 as prior
from scripts.research_wedding_command_v676 import walk
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B212_controls_v6603');SOURCE=Path('work/analysis/lil_B212_source_v6594b/all14_clean_current_complete_exchange_with_two_three_choices.json');BRANCH=Path('work/analysis/lil_B212_branches_v6596/original_relative_skip_operand_proof.json');DOC=Path('translations/lil_B212_editorial_manuscript_v1.json')
def compile_menu(word,values):
    count={0x2100:2,0x2200:3}[word];assert len(values)==count;offsets=[];chunks=[];cursor=0
    for value in values:
        assert value and value.strip()==value and all(32<=v<127 for v in value);offsets.append(cursor);chunk=value+b'\0';chunk+=bytes(-len(chunk)%2);chunks.append(chunk);cursor+=len(chunk)
    return struct.pack('<'+'H'*(count+1),word,*offsets)+b''.join(chunks)
if __name__=='__main__':
    assert not ROOT.exists();packet,branch,doc=map(read,[SOURCE,BRANCH,DOC]);assert branch['source_context_sha256']==sha(SOURCE.read_bytes()) and len(branch['cases'])==100;g=packet['blocks'][0];images=[NdsImage.open(p) for p in ['work/clean.nds',packet['current_ROM']]];arms=[i.read_file('/__arm9__.bin') for i in images];blocks=[IlnkContainer.parse(i.read_file('/data/SC2.DK4')).blocks[212] for i in images]
    spans=[(0x2A1D8,0x2A414),(0x51FC0,0x52030),(0x52E40,0x52F50),(0x24048,0x24118)]
    assert all(arms[0][a:b]==arms[1][a:b] for a,b in spans)
    adapter=checked_text(inspect.getsource(prior.choice_vm),{'def choice_vm(arm, object_bytes):':'def choice_vm(arm, object_bytes, option_count):','assert cpu.reg_read(UC_ARM_REG_R0) == 2':'assert cpu.reg_read(UC_ARM_REG_R0) == option_count','for index in (0, 1):':'for index in range(option_count):','for selected in (0, 1, -1):':'for selected in [*range(option_count),-1]:','(rect, provider, maximum, 2)':'(rect, provider, maximum, option_count)','pointer, 32':'pointer, len(object_bytes)','96':'VM_GUARD_BYTES','p.decode()':"p.decode('cp932')"});env={**prior.__dict__,'VM_GUARD_BYTES':256};exec(compile(adapter,__file__+'::source-option-count-bound','exec'),env);menus=[]
    for menu in g['choices']:
        word=menu['word'];count={0x2100:2,0x2200:3}[word];rows=sorted([r for r in doc['records'] if r.get('command_offset')==menu['command_offset']],key=lambda r:r['option_index']);values=[r['english'].encode('ascii') for r in rows];target=compile_menu(word,values);versions=[]
        for version,arm,value in [('clean',arms[0],bytes.fromhex(menu['source_command']['whole_command_hex'])),('current',arms[1],bytes.fromhex(menu['current_command']['whole_command_hex'])),('reviewed-research',arms[1],target)]:
            assert len(value)+32<=256;proof=env['choice_vm'](arm,value,count);assert [c['modal_selection'] for c in proof['VM_cases']]==[*range(count),-1] and [c['VM_state'] for c in proof['VM_cases']]==[2]*count+[0] and all(c['next_command_delta']==len(value) and c['original_dispatch_ABI_and_guards_pass'] for c in proof['VM_cases']);versions.append(dict(version=version,object_hex=value.hex(),**proof))
        assert versions[-1]['labels']==[v.decode('ascii') for v in values];menus.append(dict(command_offset=menu['command_offset'],word=word,count=count,target_object_hex=target.hex(),versions=versions))
    commands={c['offset']:c for c in g['all_clean_native_commands']};texts={r['source_reference']['header_offset']:r for r in packet['records']};paths=[]
    for familiar,favorite in [(1,None),(0,0),(0,1),(0,2)]:
        cursor,last=8,0;visited=[];spoken=[];selections=[];effects=[]
        while True:
            assert cursor in commands and cursor not in visited;command=commands[cursor];word=command['word'];visited.append(cursor)
            if word==0:break
            if word in [0x100,0x200,0x300,0x400]:
                case=[r for r in branch['cases'] if r['version']=='current' and r['offset']==cursor and r['last_choice_or_result']==last];assert len(case)==1;cursor=case[0]['original_next_command_offset'];continue
            if word==0x4000:spoken.append(texts[cursor]['source_record_index'])
            elif word in [0x2100,0x2200]:
                last=familiar if word==0x2100 else favorite;assert last is not None;selections.append(dict(offset=cursor,selection=last))
            else:assert word==0xA000;effects.append(cursor)
            cursor+=command['native_extent']
        paths.append(dict(familiarity_option=familiar,favorite_general_option=favorite,native_command_offsets=visited,spoken_source_record_indices=spoken,modeled_selections=selections,source_effect_offsets=effects,source_end_offset=cursor,last_choice_result=last,native_relative_cases_and_menu_return_contract_model_not_actual_UI_or_full_VM=True))
    assert [(p['spoken_source_record_indices'],p['source_end_offset'],p['source_effect_offsets']) for p in paths]==[([5,22],152,[]),([5,32,51,54,58,62],664,[656]),([5,32,72],878,[870]),([5,32,78],878,[870])]
    leaves=[c for c in commands.values() if c['word'] in [0xA000,0]];assert [(c['offset'],c['word']) for c in leaves]==[(152,0),(656,0xA000),(664,0),(870,0xA000),(878,0)];effects=[];ends=[]
    for c in leaves:
        if c['word']==0:
            for version,arm,block in zip(['clean','current'],arms,blocks,strict=True):
                for previous in [0,1,2,3,0xFFFFFFFF]:ends.append(dict(version=version,**end_case(arm,block,c['offset'],previous)))
        else:
            value=bytes.fromhex(c['whole_command_hex']);isolated=b'CS\0\1'+struct.pack('<H',len(value))+bytes(2)+value;pair=[]
            for version,arm in zip(['clean','current'],arms,strict=True):
                result=walk(arm,isolated);assert result['error'] is None and result['stopped_offset']==result['logical_end']==len(isolated) and len(result['rows'])==1 and result['rows'][0]['word']==0xA000 and result['rows'][0]['native_extent']==8;pair.append(dict(version=version,**result))
            assert pair[0]['rows']==pair[1]['rows'] and pair[0]['opaque_effect_bridges']==pair[1]['opaque_effect_bridges'];effects.append(dict(source_offset=c['offset'],source_hex=value.hex(),cases=pair,opaque_effect_bodies_bridged_not_quest_item_stats_or_world_semantics=True))
    assert len(effects)==2 and len(ends)==30;ROOT.mkdir(parents=True)
    save(ROOT/'two_three_choices21_return_cases_four_paths_two_effect_pairs_and30_guarded_ends.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),menus=menus,native_selection_cancel_cases=21,source_owned_choice_VM_adapter=adapter,all_five_source_choice_identities_indices_and_selected_returns_bound=True,cancel_returns_state0_not_a_fourth_general_or_No_response=True,modeled_complete_exchange_paths=paths,No_path_ends152_before_favorite_menu=True,Zhao_path_ends664_with_effect656=True,Guan_and_Zhuge_paths_end878_with_effect870=True,source_A000_structural_pairs=effects,guarded_source_current_end_cases=ends,source884_logical882_tail2_three_original_end_sites_preserved=True,source_bound_native_code_spans=[dict(start=a,end=b,sha256=sha(arms[1][a:b])) for a,b in spans],native_menu_geometry_computed_by_original_constructor_from_complete_labels=True,modal_input_loop_bridged_not_actual_selection_or_full_VM=True,actual_scene_transitions_and_full_opaque_effects_unproved=True,complete_font_planes_backing_and_prose_formatting_still_pending=True,no_ROM_ledger_or_completion_change=True,new_emulator_runs=0,new_review_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,BRANCH,DOC,Path(prior.__file__),Path(__file__)]},full_goal_complete=False));print(dict(menu_return_cases=21,paths=[(p['familiarity_option'],p['favorite_general_option'],p['source_end_offset']) for p in paths],opaque_effect_pairs=2,guarded_end_cases=30,credit=0))
