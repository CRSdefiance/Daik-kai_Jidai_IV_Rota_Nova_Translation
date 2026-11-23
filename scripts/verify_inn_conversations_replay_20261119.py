"""Match the Inn transitions to the immediate predecessor under identical inputs."""

from inspect import getsource

from scripts import replay_inn_conversations_20261119 as game
from scripts.source_locked_derivation_v5118 import checked_text


def verify():
    base,stage = game.base,game.stage
    root = stage.ROOT/"istanbul_predecessor"
    prior_path = root/"capture/capture_report.json"
    trace_path = root/"requests.json"
    prior,trace,terminal = map(base.load,(prior_path,trace_path,root/"terminal.json"))
    schedule,_,end,_,donor = game.schedule("istanbul")
    assert prior["ROM_sha256"]==terminal["ROM_sha256"]==base.digest(stage.parent.ROM)
    assert prior["frames"]==terminal["completed_frames"]==end
    assert prior["scripted_input_schedule"]==schedule and prior["cold_boot"] and not prior["savestate_loaded"]
    assert not prior["callback_errors"] and not any(v for k,v in prior.items() if k.startswith("synthetic_"))
    assert prior["battery_save_preloaded"]["source_sha256"]==donor["source_sha256"]
    assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["errors"] and not trace["mismatches"]
    current = base.load(game.CAPTURE/"requests.json")
    assert current["source_requests"]==trace["source_requests"]
    source = checked_text(getsource(game.verify),{
        "history = base.load(source)": "history = prior",
        "(*paths,source,PLAN)": "(*paths,source,PLAN,prior_path,trace_path,Path(__file__))",
    })
    scope = vars(game)|dict(prior=prior,prior_path=prior_path,trace_path=trace_path,__file__=__file__)
    exec(compile(source,__file__+"::current_predecessor","exec"),scope)
    scope["verify"]()


if __name__=="__main__":
    verify()
