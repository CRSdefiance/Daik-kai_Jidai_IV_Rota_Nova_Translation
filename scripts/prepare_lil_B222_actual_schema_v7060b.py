"""Adapt source report field names explicitly; preserve the initial failed audit and all captures."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_market_gameplay_v753 import state
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B222_actual_schema_v7060b')
SOURCE=Path('work/analysis/lil_B222_source_actual_v7044/all16_Japanese_speeches27_commands_complete_masks_headers_and_normal_return.json')
if __name__=='__main__':
    assert not ROOT.exists();d=read(SOURCE);report=read(d['report']);plan=read(Path(d['run'])/'run_plan.json');raw=Path(d['final_RAM_snapshot']['path']).read_bytes();image=NdsImage.open(d['candidate'])
    assert sha(Path(d['report']).read_bytes())==d['report_sha256'] and sha(Path(d['candidate']).read_bytes())==d['candidate_sha256']==report['ROM_sha256'] and len(raw)==4194304 and sha(raw)==d['final_RAM_snapshot']['sha256'] and d['all_jobs_terminal_and_reaped']
    assert sha(Path(plan['original_inputs']).read_bytes())==plan['inputs_sha256'] and report['scripted_input_schedule']==read(plan['original_inputs'])
    adapted=deepcopy(d);adapted.update(original_source_actual_proof=str(SOURCE),original_source_actual_proof_sha256=sha(SOURCE.read_bytes()),input_schedule_sha256=plan['inputs_sha256'],capture_report=d['report'],speech_observations=d['source_speech_observations'],final_snapshot=d['final_RAM_snapshot'],research_ROM=d['candidate'],queried_final_native_state=state(image.read_file('/__arm9__.bin'),raw),schema_adapter_only_original_command_observation_and_capture_bytes_unchanged=True,no_new_boot_or_source_coverage_claim=True)
    ROOT.mkdir(parents=True);out=ROOT/'source_report_explicit_schema_adapter.json';save(out,adapted)
    tool=derive('scripts/audit_lil_B222_English_v7060.py','scripts/audit_lil_B222_English_v7060b.py',{'English_actual_v7060':'English_actual_v7060b',str(SOURCE).replace('\\','/'):'work/analysis/lil_B222_actual_schema_v7060b/source_report_explicit_schema_adapter.json'})
    later=derive('scripts/measure_lil_B222_later_v7061.py','scripts/measure_lil_B222_later_v7061b.py',{'later_v7061':'later_v7061b','English_actual_v7060':'English_actual_v7060b'})
    save(ROOT/'preserved_failure_and_successors.json',dict(failed_audit='scripts/audit_lil_B222_English_v7060.py',failure="KeyError input_schedule_sha256:source-specific report uses run/report/source_speech_observations/final_RAM_snapshot fields.",failed_before_any_actual_audit_output_or_ROM_mutation=True,adapter=str(out),adapter_sha256=sha(out.read_bytes()),audit=tool,later=later,no_emulator_replay_or_native_address_change=True,new_credit=0,full_goal_complete=False))
