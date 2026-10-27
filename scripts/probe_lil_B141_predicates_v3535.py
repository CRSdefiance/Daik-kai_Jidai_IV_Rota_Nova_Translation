"""Run the three source predicates without forcing funds or predicate results."""
import inspect
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.prove_lil_B139_B140_conditionals_v3461c import probe
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B141_predicates_v3535')
SOURCE=Path('work/analysis/lil_B141_source_v3532b/all14_clean_current_complete_context.json')
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);group=packet['blocks'][0];image=NdsImage.open(packet['current_ROM']);block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[141]
    ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B141_voices_v3533/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context');cases=[]
    for c in group['all_current_native_commands']:
        if c['word']!=0x8000:continue
        result=ctx.execute(probe,block,c);ctx.machines.pop();cases.append(result)
    assert len(cases)==3 and not ctx.machines and all(not c['original_event_completion_calls'] for c in cases)
    save(ROOT/'three_unforced_current_native_predicate_results.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),cases=cases,portable_source_owned_predicate_adapter=inspect.getsource(probe),historical_London_snapshot_not_B141_eligibility=True,no_money_roster_event_RNG_or_result_fixture=True,predicate_semantics_and_funding_boundaries_still_require_binding=True,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),no_ROM_registry_ledger_review_or_completion_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print([(c['source_command_hex'],c['native_result']) for c in cases])
