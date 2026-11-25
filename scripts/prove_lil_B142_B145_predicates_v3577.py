"""Bind six unforced predicates without altering memberships,funds or results."""
import inspect
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.prove_lil_B139_B140_conditionals_v3461c import probe
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B142_B145_predicates_v3577')
SOURCE=Path('work/analysis/lil_B142_B145_source_v3571/all38_clean_current_complete_context.json')
if __name__=='__main__':
    assert not ROOT.exists();source=read(SOURCE);image=NdsImage.open(source['current_ROM']);blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks;ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B142_B145_voices_v3572/current_native_input.json',source['historical_snapshot_ROM'],ROOT/'current_context');cases=[]
    for group in source['blocks']:
        for c in group['all_current_native_commands']:
            if c['word']!=0x8000:continue
            result=ctx.execute(probe,blocks[group['block']],c);ctx.machines.pop();assert not result['original_event_completion_calls'];cases.append(dict(block=group['block'],**result))
    assert len(cases)==6 and not ctx.machines
    save(ROOT/'six_source_exact_unforced_current_predicate_results.json',dict(candidate=source['current_ROM'],candidate_sha256=source['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),cases=cases,source_predicate_result_constants={c['source_command_hex']:c['native_result'][1] for c in cases},portable_source_owned_predicate_adapter=inspect.getsource(probe),all_cases_copied_London_context_not_scene_eligibility=True,no_membership_money_roster_event_RNG_or_result_fixture=True,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),new_emulator_runs=0,no_ROM_registry_ledger_review_orcompletion_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print([(c['block'],c['source_command_hex'],c['native_result'][1]) for c in cases])
