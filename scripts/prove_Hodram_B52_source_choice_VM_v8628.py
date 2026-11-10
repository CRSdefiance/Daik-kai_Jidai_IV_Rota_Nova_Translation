"""Bind original B52 choice width/geometry/returns and source-qualified response paths."""
import inspect,struct
from pathlib import Path
from types import SimpleNamespace
from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.main_pool_cache_visibility import BASE,POOL
from dk4tool.patch.grand_race_menu_release import sha
from scripts import verify_ship_advice_choice_centering_20261022 as original
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B52_source_choice_VM_v8628')
GLOSS=Path('work/analysis/Hodram_B52_clean_gloss_v8617/three_first_clean_glosses_two_choice_labels_anddistinct_terminal_risks.json')
CONTROL=Path('work/analysis/Hodram_B52_source_controls_v8620/source_controls.json')
GETTERS=Path('work/analysis/Hodram_B52_choice_source_v8627/source_choice_getters.json')
INPUT=Path('work/analysis/current_V8609_Hodram_native_v8612/current_native_input.json')
FORWARD=Path('work/analysis/Hodram_B51_result_flow_v8558c/result_flow.json')

if __name__=='__main__':
    assert not ROOT.exists();gloss,controls,getters,inp,forward=map(read,[GLOSS,CONTROL,GETTERS,INPUT,FORWARD])
    assert gloss['current_English_dialogue_bodies_andchoice_labels_still_unconsulted'] and controls['current_B52_English_dialogue_bodies_still_unconsulted']
    image=NdsImage.open(inp['current_ROM']);arm=image.read_file('/__arm9__.bin');clean=NdsImage.open('work/clean.nds')
    assert sha(Path(inp['current_ROM']).read_bytes())==inp['current_ROM_sha256'] and sha(arm)==inp['current_ARM9_sha256']=='12ebaf3f3ce558e731c4c972ae90696392a351426cf147fbf3bd830dd1d82d1b'
    assert image.read_file('/__arm9__.bin')==NdsImage.open(controls['candidate']).read_file('/__arm9__.bin')
    assert getters['command']==gloss['source_typed_choice']['command'] and getters['all_two_source_labels_two_versions_two_even_alignments_exact']
    sections=MainCodeFile(arm,BASE).sections;payload=bytes(sections[3].data[:-48]);assert len(payload)==123264
    owned=[*sections,SimpleNamespace(ramAddress=POOL,data=payload)];executed=set()
    def machine(current_arm):
        assert current_arm==arm;cpu=original.machine(current_arm)
        def exact(u,pc,size,unused):
            owners=[s for s in owned if s.ramAddress<=pc and pc+size<=s.ramAddress+len(s.data)]
            assert len(owners)==1,hex(pc)
            section=owners[0];at=pc-section.ramAddress
            assert bytes(u.mem_read(pc,size))==bytes(section.data[at:at+size]),hex(pc)
            executed.add(pc)
        cpu.hook_add(UC_HOOK_CODE,exact);return cpu
    vm_adapter=checked_text(inspect.getsource(original.choice_vm),{
        'def choice_vm(arm, object_bytes):':'def choice_vm(arm, object_bytes, alignment):',
        "    cpu.mem_write(text - 16, b'\\xA5' * 96)":"    assert alignment in [0,2];text+=alignment\n    cpu.mem_write(text - 16, b'\\xA5' * 96)",
        'p.decode() for p in labels':"p.decode('cp932') for p in labels",
        "'VM_state': state,":"'VM_state': state, 'VM_selection_word': selection,",
    })
    env={**original.__dict__,'machine':machine};exec(compile(vm_adapter,__file__+'::exact-source-provider','exec'),env)
    command=gloss['source_typed_choice']['command'];raw=bytes.fromhex(command['whole_command_hex'])
    expected=[r['source_Japanese'] for r in gloss['source_typed_choice']['labels']]
    assert len(raw)==36 and command['offset']==68
    cases=[]
    for alignment in [0,2]:
        result=env['choice_vm'](arm,raw,alignment)
        assert result['labels']==expected
        assert [(c['modal_selection'],c['VM_state']) for c in result['VM_cases']]==[(0,2),(1,2),(-1,0)]
        assert [c['VM_selection_word'] for c in result['VM_cases'][:2]]==[0,1]
        assert all(c['next_command_delta']==36 and c['original_dispatch_ABI_and_guards_pass'] for c in result['VM_cases'])
        cases.append(dict(alignment=alignment,native_VM=result))
    assert cases[0]['native_VM']==cases[1]['native_VM']
    assert arm[0x24048:0x24118]==clean.read_file('/__arm9__.bin')[0x24048:0x24118]
    assert forward['original_caller_instruction_span']['sha256']==sha(arm[0x24048:0x24118])
    assert len(forward['caller_fragment_cases'])==50 and all(c['all_six_return_words_preserved'] and c['next_parser_r3']==(c['result'][1] if c['result'][0]==2 else c['previous_structural_value']) for c in forward['caller_fragment_cases'])
    group=gloss['groups'][0];commands={c['offset']:c for c in group['commands']};branches={c['offset']:c for c in controls['source_relative_cases']}
    paths=[]
    for selected in [0,1]:
        at=68+len(raw);visited=[8,68];speeches=[8]
        while True:
            visited.append(at);command=commands[at]
            if command['word']==0:break
            if at in branches:
                at=next(c['next_offset'] for c in branches[at]['cases'] if c['previous_result_structural_argument']==selected)
            else:
                if command['word']==0x4000:speeches.append(at)
                at+=command['native_extent']
            assert len(visited)<20
        assert (speeches,at)==(([8,112],166) if selected==0 else ([8,178],224))
        ends=[c for c in controls['distinct_seeded_ends'] if c['source_offset']==at]
        assert len(ends)==25 and all(c['native_result'][0]==selected for c in ends)
        paths.append(dict(modal_selection_argument=selected,original_menu_result_kind=2,forwarded_selection_argument=selected,source_command_offsets=visited,source_speech_headers=speeches,source_terminal_offset=at,source_terminal_hex=command['whole_command_hex'],terminal_native_result_kind=selected,structural_composition_not_actual_controller_choice_orwhole_scene=True))
    ROOT.mkdir(parents=True);save(ROOT/'source_menu_provider_andresponse_paths.json',dict(candidate=inp['current_ROM'],candidate_sha256=inp['current_ROM_sha256'],ARM9_sha256=sha(arm),source_gloss=str(GLOSS),source_gloss_sha256=sha(GLOSS.read_bytes()),source_controls=str(CONTROL),source_controls_sha256=sha(CONTROL.read_bytes()),source_getters=str(GETTERS),source_getters_sha256=sha(GETTERS.read_bytes()),source_choice=gloss['source_typed_choice'],even_alignment_provider_cases=cases,bridged_modal_return_cases=6,source_width_units=cases[0]['native_VM']['native_width_units'],source_menu_rectangle=cases[0]['native_VM']['native_menu_rectangle'],structural_response_paths=paths,caller_fragment_reused_from=str(FORWARD),caller_fragment_reused_sha256=sha(FORWARD.read_bytes()),reused_original_kind2_value_forwarding_kind3_carry_cases=50,full_original_caller_code_current_andclean_identical=True,source_owned_VM_adapter=vm_adapter,all_executed_instructions_exact_current_sections_and123264_payload=True,executed_instruction_addresses=len(executed),modal_loop_bridged_not_actual_input_oractivation=True,cancel_kind0_does_not_claim_a_followup_path=True,complete_Japanese_menu_glyphs_backing_highlight_controller_dismissal_andactual_branch_visits_pending=True,current_B52_English_dialogue_andchoice_bodies_still_unconsulted=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [GLOSS,CONTROL,GETTERS,INPUT,FORWARD,Path(original.__file__),Path(__file__)]}))
    print('B52 source menu: two exact providers/six bridged returns, original 0/1 forwarding composes withdrawal/normal166 versus reckless-boldness/flagged224; cancel distinct. No actual controller/path or menu-glyph claim.')
