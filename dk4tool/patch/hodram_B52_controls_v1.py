"""Independently execute exact B52 control consumers in current captain1 context."""
import struct
from pathlib import Path
from tempfile import TemporaryDirectory
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.hodram_B52_profile_v1 import contract
from dk4tool.patch.hodram_B52_native_guards_v1 import trusted_adapter, TRUSTED
from scripts.Hodram_B51_registered_route_context_v8612 import RouteCurrentContext
from scripts import prove_lil_shrines_temples_controls_v3168c as inherited
from scripts.prove_lil_B234_entry_v7576 import native_entry
from scripts.prove_Maria_story_branches_v7741 import native_skip
from scripts.prove_lil_B139_B140_conditionals_v3461c import probe
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts.research_wedding_command_v676 import walk

SOURCE = Path('work/analysis/Hodram_B52_source_controls_v8620/source_controls.json')
FLOW = Path('work/analysis/Hodram_B51_result_flow_v8558c/result_flow.json')
FLOW_SCRIPT = Path('scripts/prove_Hodram_B51_result_flow_v8558c.py')
INPUT = Path('work/analysis/current_V8609_Hodram_native_v8612/current_native_input.json')
MAP = Path('work/analysis/Hodram_B52_relocation_v8642/reconstruction.json')

def check_controls(data, rows, parent, reference, rebuilt, native, load, require):
    mapping,current,source,display,stored,flow,menu_flow=[data[k] for k in ['relocation','current','source_controls','source_display','stored','result_flow','source_menu_VM']]
    require(sha(SOURCE.read_bytes()) == TRUSTED[SOURCE.as_posix()] and source == load(SOURCE), 'exact immutable source control artifact')
    frozen = contract()
    require(sha(FLOW.read_bytes()) == frozen['dependencies'][str(FLOW.resolve())] and flow == load(FLOW), 'exact original caller result-channel artifact')
    scriptkey = next(k for k in flow['evidence'] if Path(k).resolve() == FLOW_SCRIPT.resolve())
    require(sha(FLOW_SCRIPT.read_bytes()) == flow['evidence'][scriptkey], 'exact source-owned native caller fragment')
    require(source['current_native_input_sha256'] == sha(INPUT.read_bytes()) and stored['relocation_sha256'] == sha(MAP.read_bytes()), 'own current context and original relocation identity')
    require(sha(bytes(parent.rom.save())) == mapping['candidate_sha256'], 'whole in-memory registered predecessor')
    arm = parent.read_file('/__arm9__.bin')
    require(arm == reference.read_file('/__arm9__.bin'), 'unmodified complete runtime')
    g, block = mapping['groups'][0], rebuilt['target_block']
    require(g['block'] == 52 and len(rows) == 3 and sha(block) == g['target_block_sha256'], 'complete three-speech B52 target')
    require(len(g['all_target_commands']) == 14 and len(g['relative_fixups']) == len(g['relocated_skip_cases']) == 4, 'all fourteen commands/four relative sites')
    require(sum(len(c['cases']) for c in g['relocated_skip_cases']) == 20, 'all twenty native branch cases')
    require([r['source_selector'] for r in rows] == [113,113,113], 'three original progressive actors')
    for before, after, cm in zip(source['all_original_source_commands'], g['all_target_commands'], g['command_map'], strict=True):
        at = after['offset']
        require(before['word'] == after['word'] == cm['word'] and at == cm['new_offset'], 'source/target command association')
        require(block[at:at + after['native_extent']].hex() == after['whole_command_hex'], 'literal complete stored command bytes')
        if after['word'] == 0x4000:
            require(before['whole_command_hex'][:12] == after['whole_command_hex'][:12], 'complete original six-byte preamble')
        elif after['word']==0x2100:
            require(after['whole_command_hex']==g['choice_commands'][0]['target_hex'],'complete independently compiled typed menu')
        elif after['word'] in [0x100, 0x200, 0x300, 0x400]:
            require(before['whole_command_hex'][:4] == after['whole_command_hex'][:4], 'original relative opcode')
        else:
            require(before['whole_command_hex'] == after['whole_command_hex'], 'all original queries/opaque controls/full terminal')
    ns = {**inherited.__dict__, 'SOURCE': INPUT, 'route': 1, 'route_mask': 2, 'CATALOG_LOOKUP': {}}
    for key, field in [('dispatch', 'source_owned_dispatch_adapters'), ('macro_body', 'source_owned_macro_body_adapter')]:
        trusted_adapter(key, display[field])
    for name, text in display['source_owned_dispatch_adapters'].items():
        exec(compile(text, __file__ + '::exact-' + name, 'exec'), ns)
    exec(compile(display['source_owned_macro_body_adapter'], __file__ + '::exact-macro-body', 'exec'), ns)
    ns['CATALOG_LOOKUP'], catalogue = ns['bind_current_catalog'](parent)
    require(catalogue == stored['registered_catalogue_binding'], 'complete registered current catalogue')
    en, sk, qp, ee = dict(native_entry.__globals__), dict(native_skip.__globals__), dict(probe.__globals__), dict(end_case.__globals__)
    for label, field, env in [('entry', 'source_owned_entry_adapter', en), ('skip', 'source_owned_skip_probe', sk),
            ('query', 'source_owned_query_probe', qp), ('seeded_end', 'source_owned_seeded_end_adapter', ee)]:
        adapter = trusted_adapter(label, source[field])
        exec(compile(adapter, __file__ + '::trusted-' + label, 'exec'), env)
    with TemporaryDirectory(prefix='Hodram-B52-controls-') as temporary:
        ctx = RouteCurrentContext(INPUT, 'unused-no-historical-ROM', Path(temporary) / 'current_context')
        context_binding = load(ctx.proof_path)
        events = source['source_event_anddependency_records']
        require([e['event_ID'] for e in events] == [30,52,74] and [(e['event_ID'],e['script_block'],e['must_be_completed'],e['must_not_be_completed']) for e in source['source_event_records']]==[(52,52,[30],[74])], 'original selected event52 andits30/74 dependencies without outer eligibility claim')
        entry = ctx.execute(en['native_entry'], parent.read_file('/data/EV1.DK4'), events)
        ctx.machines.pop()
        require(entry == source['original_EV1_entry'], 'all original event getter fields and unforced completion flags')
        byoffset = {c['offset']: c for c in g['all_target_commands']}
        boundaries = set(byoffset) | {g['target_logical_end']}
        branches = []
        for fix, declared in zip(g['relative_fixups'], g['relocated_skip_cases'], strict=True):
            result = ctx.execute(sk['native_skip'], block, byoffset[fix['new_offset']])
            ctx.machines.pop()
            require(result == declared and all(c['next_offset'] in boundaries and c['next_offset'] == (fix['new_matched_skip_target'] if c['taken'] else fix['new_unmatched_next']) for c in result['cases']), 'all native relative results/extents/endpoints/ABI')
            branches.append(result)
        require(branches == stored['reused_exact_relocated_native_skip_cases'], 'stored branch evidence equals independently executed consumers')
        dispatches = []
        for ref in g['text_records']:
            raw, at = bytes.fromhex(ref['target_hex']), ref['new_offset']
            require(block[at:at + len(raw) + 1] == raw + b'\0' and ns['CATALOG_LOOKUP'].get(raw[1:]) is None, 'literal complete stored speech')
            result = ctx.execute(ns['dispatch'], raw[0], raw[1:])
            ctx.machines.pop()
            boundary = next(r for r in result['boundaries'] if r['kind'] == 'unexecuted-progressive-body')
            require(result['resolved_actor_ID'] == raw[0] and result['source_voice_class'] == {113:0}[raw[0]] and not result['FE_original_null_actor_calls'], 'original exact actor/voice/no FE')
            require(boundary['text_hex'] == native['bodies']['revised_English'][ref['id']]['expanded_body'].hex() == raw[1:].hex(), 'independently recomputed native stored text')
            dispatches.append(dict(id=ref['id'], **result))
        require(dispatches == stored['stored_dispatches'], 'all three complete original dispatch records')
        queries, opaque = [], []
        cleanarm = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
        for original, target in zip(source['all_original_source_commands'], g['all_target_commands'], strict=True):
            word = target['word']
            if word in [0x8000, 0x8100]:
                result = ctx.execute(qp['probe'], block, target)
                ctx.machines.pop()
                previous = next(q for q in source['source_raw_query_cases'] if q['word'] == word)
                require(result['native_result'] == previous['native_result'] == [2, 0, 0, 0, 0, 0] and result['source_command_hex'] == previous['source_command_hex'], 'both unforced queries and all six return words')
                queries.append(result)
            elif word not in [0,0x2100,0x4000,0x100,0x200,0x300,0x400]:
                raw = bytes.fromhex(target['whole_command_hex'])
                isolated = b'CS\0\1' + struct.pack('<H', len(raw)) + bytes(2) + raw
                pair = next(p for p in source['paired_opaque_structural_decodes'] if p['source_offset'] == original['offset'])
                versions = [dict(version=label, **walk(code, isolated)) for label, code in [('clean-decoder', cleanarm), ('current-decoder', arm)]]
                require(versions == pair['versions'], 'every paired original opaque structural decode, without effect semantics claims')
                result = walk(arm, isolated)
                opaque.append(dict(source_offset=original['offset'], target_offset=target['offset'], word=word, original_linear_decode=result))
        require(len(queries) == 0 and queries == stored['stored_queries'], 'complete relocated query ABI/scratch/input/return records')
        require(len(opaque) == 4 and opaque == stored['four_opaque_structural_decodes'], 'all four complete opaque decode records')
        terminals=[c for c in g['all_target_commands'] if c['word']==0]
        require(len(terminals)==2 and [c['whole_command_hex'] for c in terminals]==['00000000','00000080'] and terminals[-1]['offset']+4==g['target_logical_end'],'both distinct full ends before separate tail')
        endmap={c['old_offset']:c['new_offset'] for c in g['command_map'] if c['word']==0}
        require(endmap=={166:158,224:232},'exact source/current normal/flagged end maps')
        ends=[ee['end_case'](arm,block,endmap[c['source_offset']],c['previous_result'],c['initial_value_word']) for c in source['distinct_seeded_ends']]
        require(len(ends)==50 and ends==stored['distinct_seeded_ends'],'all fifty original distinct seeded ends andguard fields')
        require(sum(e['flagged_terminal'] for e in ends)==25 and all(e['native_result']==([1,0,0,0,0,0] if e['flagged_terminal'] else [0,e['initial_value_word'],0,0,0,0]) for e in ends),'normal carries value/flagged returns1clears value/all six words')
        span = flow['original_caller_span']
        require(arm[span['start']:span['end']] == cleanarm[span['start']:span['end']] and sha(arm[span['start']:span['end']]) == span['sha256'], 'original whole caller instruction span')
        require(menu_flow['caller_fragment_reused_from']==str(FLOW) and menu_flow['caller_fragment_reused_sha256']==sha(FLOW.read_bytes()) and menu_flow['reused_original_kind2_value_forwarding_kind3_carry_cases']==50,'exact source-qualified caller reuse')
        forwarded=flow['caller_fragment_cases']
        require(len(forwarded)==50 and {c['result'][0] for c in forwarded}=={2,3},'all fifty original caller cases')
        for case in forwarded:
            require(len(case['result'])==6 and case['all_six_return_words_preserved'] and case['full_unowned4MiB_actors_stream_runtime_stack_canaries_andSP_exact'],'reused caller complete six words andoriginal guards')
            require(case['next_parser_r3']==(case['result'][1] if case['result'][0]==2 else case['previous_structural_value']),'original kind2 value forwarding/kind3 carry')
        require(not ctx.machines,'no native context machine remains')
    return dict(independent_final_dispatches=3, relative_sites=4, native_relative_cases=20, raw_query_cases=0,
        original_EV1_entries=3, opaque_structural_decode_pairs=4, distinct_seeded_ends=50, exact_reused_original_result_channel_cases=50,
        original_current_native_context=context_binding, all14_commands_three_preambles_zeroqueries_typed_menu_branches_both_fullends_tail_andvalue_carries_bound=True,
        no_new_actual_scene_opaque_effect_semantics_earned_inventory_orouter_eligibility_claim=True, new_emulator_runs=0)
