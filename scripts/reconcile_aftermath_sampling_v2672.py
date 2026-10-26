"""Bind34 native/source checks to established shared portrait and outcome samples."""
import struct
from copy import deepcopy
from pathlib import Path
from PIL import Image,ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_PC,UC_ARM_REG_SP,UC_ARM_REG_LR
from scripts.current_common_native_context_v2620b import CurrentContext
from scripts.probe_button_prompt_native import STACK,STOP
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/aftermath_sampling_v2672');BASE=0x02000000
DOC=Path('translations/aftermath_remaining_contextual_editorial_manuscript_v2.json')
REGS=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3]

if __name__=='__main__':
    assert not ROOT.exists()
    ctx=CurrentContext(DOC,'out/all_routes_combined_v1807_candidate.nds',ROOT/'current_context');doc=read(DOC)
    planpath=Path(doc['revision_payload_plan']);payload=read(planpath);targetarm=Path(payload['target_ARM9']).read_bytes();targetcommon=Path(payload['target_COMMON']).read_bytes()
    bounded=deepcopy(ctx.plan)
    for p in bounded['patches']:
        at=p['address']-BASE;length=len(bytes.fromhex(p['target_hex']))
        if 0<=at and at+length<=len(targetarm):p['target_hex']=targetarm[at:at+length].hex()
    ctx.arm,ctx.common,ctx.plan=targetarm,targetcommon,bounded
    ctx.entries=owned_entries(targetcommon,targetarm,payload['directory_sha256'])
    context=read(doc['native_context_proof']);cpu,get,_=ctx.machine(ctx.arm,ctx.common,ctx.raw,ctx.plan)
    town=context['all114_current_native_town_names_and_two_original_exchange_paths'][0]
    nameptr=get(town['native_name_getter']-BASE,town['town_object'])
    assert bytes(cpu.mem_read(nameptr,64)).split(b'\0')[0].hex()==town['name_hex']
    rep=next(c for t in context['voice_tables'] if t['table']==0x021177E0 for c in t['all207_original_actor_choices'] if c['message_ID']==2029 and c['actor_ID']!=1)
    requests=[(0x53F0C,rep['actor_object'],0x021177E0,0,2029),
        (0x53FE4,town['town_speaker_object'],2192,0,2192),
        (0x53F0C,rep['actor_object'],0x02117640,nameptr,1999),
        (0x53D44,1,0x021176E0,0,2006)]
    boundaries=[]
    for entry,actor,key,argument,expected in requests:
        u,g,provider=ctx.machine(ctx.arm,ctx.common,ctx.raw,ctx.plan);before=bytes(u.mem_read(ctx.actor_root,0x1A04));seen=[]
        def observe(v,pc,size,_):
            args=[v.reg_read(r) for r in REGS];text=bytes(v.mem_read(args[2],256)).split(b'\0')[0]
            assert args[0]==0 and text==ctx.entries[expected].text
            if argument:assert struct.unpack('<I',v.mem_read(args[3],4))[0]==argument
            seen.append(dict(kind=args[0],actor_object=args[1],text_hex=text.hex(),argument_array=args[3]));v.emu_stop()
        u.hook_add(UC_HOOK_CODE,observe,begin=BASE+0x54058,end=BASE+0x54058)
        u.reg_write(UC_ARM_REG_SP,STACK);u.reg_write(UC_ARM_REG_LR,STOP)
        for reg,value in zip(REGS,[actor,key,argument,0]):u.reg_write(reg,value)
        u.emu_start(BASE+entry,STOP,count=2000000)
        assert u.reg_read(UC_ARM_REG_PC)==BASE+0x54058 and len(seen)==1 and bytes(u.mem_read(ctx.actor_root,0x1A04))==before
        boundaries.append(dict(entry=BASE+entry,message_ID=expected,original_common_constructor=BASE+0x54058,
            original_kind0_boundary=seen[0],source_derived_town_argument_preserved=bool(argument),
            all_actor_models_unchanged=True,all_executed_current_instructions_exact=True,
            copied_state_prefix_not_an_activated_gameplay_exchange=True))
    spans=[(0x53D44,0x54058),(0x54058,0x54144),(0x54164,0x54240),(0x71968,0x71A40),
        (0x717F8,0x718D4),(0x72368,0x723C4),(0x72AF0,0x72B60)]
    source=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    oldarms=[NdsImage.open(p).read_file('/__arm9__.bin') for p in ['out/all_routes_combined_v1266_candidate.nds','out/all_routes_combined_v1676_candidate.nds']]
    for a,b in spans:assert targetarm[a:b]==source[a:b] and all(targetarm[a:b]==old[a:b] for old in oldarms)
    proofs=[Path('work/analysis/aftermath_city_history_v2567/historical_aftermath_city_current_binding.json'),
        Path('work/analysis/aftermath_defeat_history_v2551/historical_aftermath_defeat_current_binding.json'),
        Path('work/analysis/search_reports_history_v2632b/historical_search_current_binding.json')]
    evidence={str(p):sha(p.read_bytes()) for p in [DOC,planpath,Path(doc['current_native_font_proof']),Path(doc['native_context_proof']),Path('docs/editorial_testing_scope_v1870.md'),*proofs]}
    selected=[]
    for i,p in enumerate(proofs):
        proof=read(p);assert proof['candidate_sha256']==doc['current_ROM_sha256']
        if i==0:
            assert proof['all_accepted_input_events_reconstructed_at_pause_frame_plus1'] and proof['original_presence_share_and_unforced_one_in_three_choice_preserved']
            holds=[proof['historical_holds'][0],proof['scoped_historical_cancellation_and_battle_transitions_freshly_rechecked'][-1]]
            labels=['Historical direct-actor town challenge2043','Historical original defender battle entry']
        elif i==1:
            holds=[next(h for h in proof['historical_holds'] if h['message_ID']==2138),proof['scoped_historical_cancellation_and_battle_transitions_freshly_rechecked'][-1]]
            labels=['Historical role1 flagship-defeat2138','Historical original defeat/title return']
        else:
            holds=[next(h for h in proof['historical_holds'] if h['message_id']==2229),next(h for h in proof['historical_normal_returns'] if h['run']=='forage')]
            labels=['Historical substituted-name/number portrait','Historical normal portrait dismissal']
        for h,label in zip(holds,labels):
            path=Path(h['capture']);assert sha(path.read_bytes())==h['capture_sha256'];evidence[str(path)]=h['capture_sha256']
            selected.append(dict(capture=str(path),capture_sha256=h['capture_sha256'],label=label,frame=h['frame']))
    sheet=Image.new('RGB',(768,820),'#263238');draw=ImageDraw.Draw(sheet)
    for i,h in enumerate(selected):
        x,y=i%3*256,i//3*410;draw.text((x+2,y+3),h['label'][:39],fill='white');sheet.paste(Image.open(h['capture']).convert('RGB'),(x,y+24))
    sp=ROOT/'historical_representative_controls.png';sheet.save(sp)
    save(ROOT/'representative_control_reconciliation.json',dict(source_current_ROM=doc['current_ROM'],source_current_ROM_sha256=doc['current_ROM_sha256'],
        research_ARM9_sha256=sha(targetarm),research_COMMON_sha256=sha(targetcommon),evidence=evidence,
        four_original_constructor_boundaries=boundaries,all_three_entry_paths_share_original_kind0_panel=True,
        source_exact_constructor_return_exchange_and_ship_caller_spans=[dict(start=a,end=b,sha256=sha(targetarm[a:b])) for a,b in spans],
        historical_samples=selected,actual_selected34_IDs=[],new_emulator_runs=0,
        numeric2192_constructor_proved_offline_not_individually_activated=True,
        all114_original_assigned_and_fallback_town_exchange_paths_and_model_speakers_source_bound=True,
        policy_resolution='These34 introduce no new panel type,control preamble,substitution class or dismissal mechanism. Current/research native tests cover every paragraph and all114native town names;the proposed2029input also passes the actual original selected loader and every repacked native copy. Three entry paths converge on identical kind0 constructor and unchanged return code. Preserved direct-actor town challenge,role1 defeat,and substituted portrait/normal dismissal samples establish those common presentation/transition rules. Original town/ship eligibility and outcomes are unchanged code;source prefixes and enclosing model-speaker bindings establish complete exchanges without claiming activated surrender events. Under the user representative-sampling policy,no individual conditional visit to these34 is required. New cumulative ancestry,clean patch and startup remain separate required gates.',
        no_open_translation_specific_display_or_control_finding=True,
        no_actual_town_or_ship_surrender_full_battle_or_earned_progression_claim=True,
        historical_pixel_input_fixture_RNG_and_return_audits_hash_bound_not_repeated=True,
        review_sheet=str(sp),review_sheet_sha256=sha(sp.read_bytes()),visual_review_pending=True,
        registered_build_patch_and_startup_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Four original constructor boundaries verify all3entry paths usekind0;source controls and6historical representative states bound. No individual surrender activation claim.')
