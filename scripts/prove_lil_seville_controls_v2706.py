"""Source-bound ordinary actor/FE dispatch and unchanged representative rules."""
import struct
from pathlib import Path
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_PC,UC_ARM_REG_LR
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.native_call_abi_v764 import call
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Seville_controls_v2706');BASE=0x02000000;TEXT=0x02660000
PACKET=Path('work/analysis/lil_Seville_source_v2704b/complete20_clean_current_native_context.json')
if __name__=='__main__':
    assert not ROOT.exists();packet=read(PACKET);current=NdsImage.open(packet['current_ROM']);historical=NdsImage.open(packet['historical_snapshot_ROM']);clean=NdsImage.open('work/clean.nds')
    arm=historical.read_file('/__arm9__.bin');now=current.read_file('/__arm9__.bin');original=clean.read_file('/__arm9__.bin');raw=Path(packet['actual_historical_snapshot']).read_bytes();assert sha(raw)==packet['actual_historical_snapshot_sha256']
    spans=[(0x2425C,0x242C8),(0x242CC,0x24310),(0x24314,0x24330),(0x24334,0x243A0),(0x54020,0x54060),(0x5473C,0x54804)]
    for a,b in spans:assert arm[a:b]==now[a:b]==original[a:b]==raw[a:b]
    cpu,get=get_machine(arm,raw);actors,captain=get(0xCB184),get(0x7F244);assert captain==2;selectors={n:get(0x2434C,n) for n in [2,4,16,20,31,254]}
    assert selectors=={2:2,4:4,16:16,20:20,31:31,254:208} and bytes(cpu.mem_read(BASE,0x400000))==raw
    cases=[]
    for row in packet['records']:
        prefix=int(row['source_presentation_prefix_hex'],16);expected_actor=None if prefix==254 else actors+0x19E4 if prefix==2 else actors+4+32*prefix
        for version,field in [('clean-Japanese','source_hex'),('current-English','current_hex')]:
            cpu,get=get_machine(arm,raw);value=bytes.fromhex(row[field]);body=value[1:];assert value[0]==prefix;cpu.mem_write(TEXT-16,b'\xA5'*2080);cpu.mem_write(TEXT,body+b'\0');guard=bytes(cpu.mem_read(TEXT-16,2080));seen=[]
            def boundary(u,pc,size,unused):
                if pc==BASE+0x940B0:
                    seen.append(dict(boundary=pc,kind='unexecuted-UI-preparation940B0',return_value_ignored_by_original_caller=True))
                else:
                    first,second=u.reg_read(UC_ARM_REG_R0),u.reg_read(UC_ARM_REG_R1);pointer=first if pc!=BASE+0x54020 else second
                    text=bytes(u.mem_read(pointer,2048)).split(b'\0')[0]
                    seen.append(dict(boundary=pc,kind='unexecuted-native-panel-body',actor_object=first if pc==BASE+0x54020 else None,text_hex=text.hex()))
                u.reg_write(UC_ARM_REG_R0,0);u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))
            hooks=[cpu.hook_add(UC_HOOK_CODE,boundary,begin=pc,end=pc) for pc in [BASE+0x940B0,BASE+0x54020,BASE+0x5473C,BASE+0x53AC4]]
            try:call(cpu,0x2425C,(prefix,TEXT),instruction_limit=500000)
            finally:
                for hook in hooks:cpu.hook_del(hook)
            assert len(seen)==2 and seen[0]['boundary']==BASE+0x940B0
            actual=seen[1];expected_presenter=BASE+(0x5473C if prefix==254 else 0x54020)
            assert actual['boundary']==expected_presenter and actual['actor_object']==expected_actor
            expected=next(p for p in row['original_macro_probes'] if p['version']==version)['output_hex'];assert actual['text_hex']==expected
            assert bytes(cpu.mem_read(BASE,0x400000))==raw and bytes(cpu.mem_read(TEXT-16,2080))==guard
            cases.append(dict(id=row['id'],version=version,prefix=prefix,selector_result=None if prefix==254 else selectors[prefix],native_presenter=actual,whole4MiB_and_input_guards_and_full_saved_register_ABI_exact=True,UI_boundaries=seen,
                source_dispatch_fragment_executed_with_historical_registered_name_wrapper=True,current_and_clean_dispatch_spans_exact_except_three_registered_name_calls=True,not_current_whole_display_or_live_Seville_activation=True))
    assert len(cases)==36 and sum(c['prefix']==254 for c in cases)==2 and all(c['native_presenter']['boundary']!=BASE+0x53AC4 for c in cases)
    refs=[Path('work/analysis/lil_Hamburg_controls_v1953b/source_bound_B74_presenter_and_control_contract.json'),Path('work/analysis/lil_London_controls_v1893b/source_bound_B26_presenter_and_control_contract.json'),Path('work/analysis/lil_Speyer_choice_v1927/original_choice_decoder_VM_geometry_and_native_pixels.json')]
    proofs=[read(p) for p in refs]
    assert proofs[0]['FE_uses_original_separate_consumer_and_null_actor_macro_caller'] and proofs[0]['three_FE_actual_anonymous_portrait_free_paper_panels_viewed']
    assert proofs[1]['progressive_presenter']==BASE+0x54020 and proofs[1]['FE_modal_presenter']==BASE+0x5473C
    ROOT.mkdir(parents=True)
    save(ROOT/'source_bound_B28_B29_presenter_and_control_contract.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],ARM9_sha256=sha(now),source_context=str(PACKET),source_context_sha256=sha(PACKET.read_bytes()),
        exact_complete_preambles=[dict(id=r['id'],preamble_hex=r['source_complete_preamble_hex'],kind=r['kind']) for r in packet['records']],all18_complete_preambles_bound=True,ordinary_native_actor_selectors={str(k):v for k,v in selectors.items() if k!=254},
        ordinary_selector_on_FE_would_return208_but_original_dispatch_selects_FE_first=True,FE_modal_presenter=BASE+0x5473C,progressive_presenter=BASE+0x54020,all36_source_current_text_contexts_dispatch_to_correct_actor_or_FE=cases,
        original_native_dispatch_and_return_ABI_preserved_under_explicit_unexecuted_UI_boundaries=True,unexecuted_UI_boundaries=[BASE+0x940B0,BASE+0x54020,BASE+0x5473C],all_five_ordinary_actor_models_and_all4MiB_unchanged=True,
        current_clean_historical_exact_spans=[dict(start=a,end=b,sha256=sha(now[a:b])) for a,b in spans],
        existing_Lil_progressive_FE_and_typed_choice_rules_references={str(p):sha(p.read_bytes()) for p in refs},
        actual_Janus4_Valdes31_or_selected_Seville_IDs=[],new_emulator_runs=0,
        scope='Original ordinary selector2/4/16/20/31and shared54020presenter are source-bound;FEis dispatched before fallback208and uses5473Cwithnull macro actor. Existing Lil actual progressive/FE/menu samples establish the reusable panel rules. Janus/Valdes individual portraits andnameplates are not claimed observed. Thirty-six historical copied-state native dispatcher/macro/caller-return cases preserve all4MiB,inputs andsaved-register ABI. UIpreparation940B0andpanel bodies are explicit unexecuted boundaries,not claimed pixel or gameplay tests. Current native body/font/choice planes,branch relocation,representative reconciliation andregistered integration still require separate proofs. No global profile orruntime is changed.',
        no_ROM_profile_prose_orcompletion_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('18complete preambles/36native dispatch contexts pass;actor2/4/16/20/31andFEseparate;whole4MiB/ABI/guards exact. UIbodies remain explicit boundaries;no Seville activation orcompletion claim.')
