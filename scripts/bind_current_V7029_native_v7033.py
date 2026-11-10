"""Bind the registered current filename to its byte-identical own target boot, without replay."""
from pathlib import Path
from scripts.square_shopkeeper_exact_native_context_v7020 import CurrentContext
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/current_V7029_native_v7033')
if __name__=='__main__':
    assert not ROOT.exists();release=read('work/analysis/square_shopkeeper_release_v7030/registered_release_verification.json')
    start=read('work/analysis/square_shopkeeper_startup_v7033/registered_current_startup_and_town_verification.json')
    proof=read('work/analysis/square_shopkeeper_names_v7021/all_name_field_voice_dynamic_macro_and_complete_native_label_consumers.json')
    previous=Path(proof['versions'][1]['current_native_input']);d=read(previous)
    assert sha(Path(release['candidate']).read_bytes())==release['candidate_sha256']==start['candidate_sha256']==d['current_ROM_sha256']
    assert Path(release['candidate']).read_bytes()==Path(d['current_ROM']).read_bytes()
    assert start['actual_target_NewGame7019_reused_by_exact_whole_ROM_hash'] and start['all_five_actor_captain_and_current_payload_controls_pass']
    d.update(historical_exact_target_input=str(previous),historical_exact_target_input_sha256=sha(previous.read_bytes()),current_ROM=release['candidate'],
        current_ROM_sha256=release['candidate_sha256'],registered_profile=release['profile'],exact_whole_ROM_target_boot_alias_not_a_historical_RAM_overlay=True)
    ROOT.mkdir(parents=True);inp=ROOT/'current_native_input.json';save(inp,d)
    ctx=CurrentContext(inp,'unused-no-historical-ROM',ROOT/'current_context');assert not ctx.machines
    save(ROOT/'registered_current_native_input_binding.json',dict(input=str(inp),input_sha256=sha(inp.read_bytes()),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
        ARM9_sha256=d['current_ARM9_sha256'],COMMON_sha256=d['current_COMMON_sha256'],native_context_proof=d['native_context_proof'],
        native_context_proof_sha256=sha(Path(d['native_context_proof']).read_bytes()),context_plan=str(ctx.proof_path),context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        full_current_ROM_equals_own_research_boot_ROM=True,no_old_ROM_or_RAM_overlay_or_relaxed_runtime_instruction_guard=True,
        all123264_payload_bytes_COMMON_directory_actual_captain_and_exact2b6_hash_checks_pass=True,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('Current V7029 input bound to its exact whole-ROM own target boot;strict2b6/payload/directory/instruction guards preserved.No replay or overlay.',flush=True)
