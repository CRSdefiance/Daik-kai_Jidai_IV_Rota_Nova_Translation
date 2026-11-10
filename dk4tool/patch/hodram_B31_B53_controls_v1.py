"""Independent original controls in the exact own-V8704 captain1 context."""
import struct
from pathlib import Path
from tempfile import TemporaryDirectory
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.hodram_B31_B53_profile_v1 import contract
from dk4tool.patch.hodram_B31_B53_native_guards_v1 import trusted_adapter,TRUSTED
from scripts.Hodram_B52_registered_route_context_v8707 import RouteCurrentContext
from scripts import prove_lil_shrines_temples_controls_v3168c as inherited
from scripts.prove_lil_B234_entry_v7576 import native_entry
from scripts.prove_Maria_story_branches_v7741 import native_skip
from scripts.prove_lil_B139_B140_conditionals_v3461c import probe
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts.prove_Hodram_B51_result_flow_v8558c import forward
from scripts.research_wedding_command_v676 import walk
SOURCE=Path('work/analysis/Hodram_B31_B53_source_controls_v8718/source_controls.json')
FLOW=Path('work/analysis/Hodram_B51_result_flow_v8558c/result_flow.json')
FLOW_SCRIPT=Path('scripts/prove_Hodram_B51_result_flow_v8558c.py')
INPUT=Path('work/analysis/current_V8704_Hodram_native_v8707/current_native_input.json')
MAP=Path('work/analysis/Hodram_B31_B53_relocation_v8728/reconstruction.json')

def check_controls(data,rows,parent,reference,rebuilt,native,load,require):
    mapping,current,source,display,stored,flow=[data[k] for k in ['relocation','current','source_controls','source_display','stored','result_flow']]
    require(sha(SOURCE.read_bytes())==TRUSTED[SOURCE.as_posix()] and source==load(SOURCE),'exact immutable source control artifact')
    frozen=contract()
    require(sha(FLOW.read_bytes())==frozen['dependencies'][str(FLOW.resolve())] and flow==load(FLOW),'exact original separate result-channel artifact')
    key=next(k for k in flow['evidence'] if Path(k).resolve()==FLOW_SCRIPT.resolve())
    require(sha(FLOW_SCRIPT.read_bytes())==flow['evidence'][key],'exact source-owned native caller fragment')
    require(source['current_native_input_sha256']==sha(INPUT.read_bytes()) and stored['relocation_sha256']==sha(MAP.read_bytes()),'ownV8704 context andoriginal relocation identity')
    require(sha(bytes(parent.rom.save()))==mapping['candidate_sha256'],'whole in-memory registered predecessor')
    arm=parent.read_file('/__arm9__.bin');cleanarm=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    require(arm==reference.read_file('/__arm9__.bin'),'unmodified complete runtime')
    require([g['block'] for g in mapping['groups']]==[g['block'] for g in current['groups']]==[g['block'] for g in source['groups']]==[31,53] and set(rebuilt['target_blocks'])=={31,53},'complete ordered two-block scope')
    require([r['source_selector'] for r in rows]==[34,34,113],'three original progressive actors')
    for g,prior,src in zip(mapping['groups'],current['groups'],source['groups'],strict=True):
        number=g['block'];block=rebuilt['target_blocks'][number]
        require(prior['block']==src['block']==number and sha(block)==g['target_block_sha256'],'complete source-owned targetblock')
        require(len(g['all_target_commands'])==9 and len(g['relative_fixups'])==len(g['relocated_skip_cases'])==(4 if number==31 else 0),'all9commands andrelative sites')
        for before,after,cm in zip(src['all_original_source_commands'],g['all_target_commands'],g['command_map'],strict=True):
            at=after['offset'];require(before['word']==after['word']==cm['word'] and at==cm['new_offset'],'source/target command association')
            require(block[at:at+after['native_extent']].hex()==after['whole_command_hex'],'literal complete stored commandbytes')
            if after['word']==0x4000:require(before['whole_command_hex'][:12]==after['whole_command_hex'][:12],'complete original six-byte preamble')
            elif after['word'] in [0x100,0x200,0x300,0x400]:require(before['whole_command_hex'][:4]==after['whole_command_hex'][:4],'original relative opcode')
            else:require(before['whole_command_hex']==after['whole_command_hex'],'all original queries/opaquecontrols/fullterminal')
    ns={**inherited.__dict__,'SOURCE':INPUT,'route':1,'route_mask':2,'CATALOG_LOOKUP':{}}
    trusted_adapter('dispatch',display['source_owned_dispatch_adapters']);trusted_adapter('macro_body',display['source_owned_macro_body_adapter'])
    for name,text in display['source_owned_dispatch_adapters'].items():exec(compile(text,__file__+'::exact-'+name,'exec'),ns)
    exec(compile(display['source_owned_macro_body_adapter'],__file__+'::exact-macro-body','exec'),ns)
    ns['CATALOG_LOOKUP'],catalogue=ns['bind_current_catalog'](parent)
    require(catalogue==stored['registered_catalogue_binding'],'complete registered current catalogue')
    en,sk,qp,ee=dict(native_entry.__globals__),dict(native_skip.__globals__),dict(probe.__globals__),dict(end_case.__globals__)
    for label,field,env in [('entry','source_owned_entry_adapter',en),('skip','source_owned_skip_probe',sk),('query','source_owned_query_probe',qp),('seeded_end','source_owned_seeded_end_adapter',ee)]:
        adapter=trusted_adapter(label,source[field]);exec(compile(adapter,__file__+'::trusted-'+label,'exec'),env)
    dispatches=[];branches=[];queries=[];opaque=[];ends=[]
    with TemporaryDirectory(prefix='Hodram-B31-B53-controls-') as temporary:
        ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',Path(temporary)/'current_context');context_binding=load(ctx.proof_path)
        events=source['source_event_anddependency_records'];require([e['event_ID'] for e in events]==[31,52,53,74],'four original event/dependency getters')
        entry=ctx.execute(en['native_entry'],parent.read_file('/data/EV1.DK4'),events);ctx.machines.pop()
        require(entry==source['original_EV1_entry'],'original eventgetter fields andunforced completion flags')
        for g,src in zip(mapping['groups'],source['groups'],strict=True):
            number=g['block'];block=rebuilt['target_blocks'][number];byoffset={c['offset']:c for c in g['all_target_commands']};boundaries=set(byoffset)|{g['target_logical_end']}
            for fix,declared in zip(g['relative_fixups'],g['relocated_skip_cases'],strict=True):
                result=ctx.execute(sk['native_skip'],block,byoffset[fix['new_offset']]);ctx.machines.pop()
                require(result==declared and all(c['next_offset'] in boundaries and c['next_offset']==(fix['new_matched_skip_target'] if c['taken'] else fix['new_unmatched_next']) for c in result['cases']),'all native relative results/extents/endpoints/ABI')
                branches.append(dict(block=number,**result))
            for ref in g['text_records']:
                raw,at=bytes.fromhex(ref['target_hex']),ref['new_offset'];require(block[at:at+len(raw)+1]==raw+b'\0' and ns['CATALOG_LOOKUP'].get(raw[1:]) is None,'literal complete stored speech')
                result=ctx.execute(ns['dispatch'],raw[0],raw[1:]);ctx.machines.pop()
                boundary=next(r for r in result['boundaries'] if r['kind']=='unexecuted-progressive-body')
                require(result['resolved_actor_ID']==raw[0] and result['source_voice_class']=={34:1,113:0}[raw[0]] and not result['FE_original_null_actor_calls'],'original exact actor/voice/noFE')
                require(boundary['text_hex']==native['bodies']['revised_English'][ref['id']]['expanded_body'].hex()==raw[1:].hex(),'independently recomputed native stored text')
                previous=next(r for r in stored['records'] if r['id']==ref['id'])
                require(result==previous['original_dispatch'],'all complete original stored dispatch records')
                dispatches.append(dict(id=ref['id'],**result))
            for original,target in zip(src['all_original_source_commands'],g['all_target_commands'],strict=True):
                word=target['word']
                if word in [0x8000,0x8100]:
                    result=ctx.execute(qp['probe'],block,target);ctx.machines.pop();previous=src['source_raw_query_cases'][0]
                    require(result['native_result']==previous['native_result']==[2,1,0,0,0,0] and result['source_command_hex']==previous['source_command_hex'] and result['no_predicate_or_event_flag_forced'],'unforced rawquery andall six returnwords')
                    declared=next(r for r in stored['fresh_target_query_cases'] if r['block']==number)
                    require(dict(block=number,**result)==declared,'complete target query ABI/scratch/input record')
                    queries.append(dict(block=number,**result))
                elif word not in [0,0x4000,0x100,0x200,0x300,0x400]:
                    raw=bytes.fromhex(target['whole_command_hex']);isolated=b'CS\0\1'+struct.pack('<H',len(raw))+bytes(2)+raw
                    pair=next(p for p in src['paired_opaque_structural_decodes'] if p['source_offset']==original['offset'])
                    versions=[dict(version=label,**walk(code,isolated)) for label,code in [('clean-decoder',cleanarm),('current-decoder',arm)]]
                    require(versions==pair['versions'],'paired original opaque structural decode without invented effect semantics')
                    opaque.append(dict(block=number,source_offset=original['offset'],target_offset=target['offset'],word=word,versions=versions))
            terminal=g['all_target_commands'][-1]
            require(terminal['word']==0 and terminal['native_extent']==4 and terminal['offset']+4==g['target_logical_end'],'complete four-byte normalend beforeseparate tail')
            for case in src['normal_seeded_ends']:
                result=ee['end_case'](arm,block,terminal['offset'],case['previous_result'],case['initial_value_word'])
                expected={**case,'source_offset':terminal['offset']}
                require(result==expected and result['native_result']==[0,case['initial_value_word'],0,0,0,0],'normalend existing resultword independent ofinterpreterr3/all6words/guards')
                ends.append(dict(block=number,**result))
        span=flow['original_caller_span'];require(arm[span['start']:span['end']]==cleanarm[span['start']:span['end']] and sha(arm[span['start']:span['end']])==span['sha256'],'original whole caller instructionspan')
        forwarded=[]
        for case in flow['caller_fragment_cases']:
            result=ctx.execute(forward,case['result'][0],case['result'][1],case['previous_structural_value']);ctx.machines.pop()
            require(result==case,'separate resultkind2 value forwarding/kind3 interpreter carry/all6resultwords preserved');forwarded.append(result)
        require(len(forwarded)==50 and not ctx.machines,'all50original callerfragment cases complete')
    require(len(dispatches)==3 and len(branches)==4 and sum(len(r['cases']) for r in branches)==20 and len(queries)==1 and len(opaque)==8 and len(ends)==50,'complete two-block independent control coverage')
    return dict(independent_final_dispatches=3,relative_sites=4,native_relative_cases=20,raw_query_cases=1,original_EV1_entries=4,opaque_structural_decode_pairs=8,normal_seeded_ends=50,original_result_channel_cases=50,
        original_current_native_context=context_binding,all18commands3preambles_query_branches_fullends_separate_tail_andboth_resultchannels_bound=True,
        source_current_glyph_andactual_gameplay_evidence_remain_separate=True,no_new_actual_scene_opaque_effect_semantics_original_activation_oroutereligibility_claim=True,new_emulator_runs=0)
