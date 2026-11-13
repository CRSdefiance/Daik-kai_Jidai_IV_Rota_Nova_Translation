"""Probe the exact source C281 parser command without assigning a plot meaning."""
import inspect
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.papal_trade_route_native_context_v7626 import RouteCurrentContext
from scripts.prove_lil_B139_B140_conditionals_v3461c import probe
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B49_C281_v8079')
SOURCE=Path('work/analysis/Rafael_next_clean_v8073/complete_clean_SC0_B49_EV0_andcoverage_before_current_English.json')
INPUT=Path('work/analysis/current_V8066_Rafael_native_v8069/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();source,inp=map(read,[SOURCE,INPUT]);g=source['groups'][0]
    block=bytes.fromhex(g['clean_block_hex']);command=next(c for c in g['commands'] if c['word']==0xC281)
    assert command['offset']==72 and command['whole_command_hex']=='81c2' and command['native_extent']==2
    image=NdsImage.open(inp['current_ROM']);clean=NdsImage.open(source['source_ROM'])
    arm=image.read_file('/__arm9__.bin');ja=clean.read_file('/__arm9__.bin')
    assert sha(Path(inp['current_ROM']).read_bytes())==inp['current_ROM_sha256']
    assert arm[0x2A414:0x2A600]==ja[0x2A414:0x2A600]
    adapter=checked_text(inspect.getsource(probe),{'0xC200':'0xC281',"'00c2'":"'81c2'"})
    env=dict(probe.__globals__);exec(compile(adapter,__file__+'::exact-source-C281-parser','exec'),env)
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')
    result=ctx.execute(env['probe'],block,command);ctx.machines.pop()
    assert result['native_extent']==2 and result['native_result']==[3,0,0,0,0,0]
    assert result['all_unowned4MiB_actor_models_ABI_input_owner_and_output_canaries_exact'] and not ctx.machines
    save(ROOT/'exact_source_C281_native_parser_two_bytes_no_unowned_state_change.json',dict(
        candidate=inp['current_ROM'],candidate_sha256=inp['current_ROM_sha256'],source_packet=str(SOURCE),source_packet_sha256=sha(SOURCE.read_bytes()),
        exact_source_command=command,native_result=result,source_owned_parser_probe=adapter,
        current_clean_parser_span=dict(start=0x2A414,end=0x2A600,sha256=sha(arm[0x2A414:0x2A600])),
        parser_result_not_complete_24070_scene_execution_orplot_semantics=True,
        do_not_normalize_C281_toC200_orremove_opaque_control=True,
        original_C281_bytes_andnative_extent_to_preserve_through_relocation=True,
        current_English_B49_bodies_still_unread=True,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,INPUT,Path(__file__)]},new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('SourceC281 at72:original parser consumes2bytes/returns[3,0];allunowned4MiB/ABI/canaries exact. Full scene effect semantics unclaimed;preserve81c2.')
