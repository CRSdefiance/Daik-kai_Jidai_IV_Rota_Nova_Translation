"""Replay the original selected raid rumor with a disclosed history input."""

from argparse import ArgumentParser
from inspect import getsource
from io import StringIO
import json
from pathlib import Path
import sys

from scripts import headless_desmume_v193 as harness
from scripts import native_condition_fixture_v520 as adapter
from scripts import native_inn_fixture_v803 as assignment
from scripts import native_inn_history_fixture_v804 as history
from scripts import replay_inn_conversations_20261119 as inn
from scripts import stage_inn_numerals_context_20261119 as stage
from scripts.source_locked_derivation_v5118 import checked_text

base = stage.base
ROOT = stage.ROOT/"raid_rumor"
ORIGINAL = Path("work/analysis/inn_history_v804/raid_won_0m_commands.jsonl")
REQUEST = dict(mode="Inn-history",event="raid",won=True,months_ago=10)


def fixture(arm,raw,request):
    assert request==REQUEST
    proof,release = map(base.load,(stage.PROOF,stage.parent.RELEASE))
    image = base.NdsImage.open(stage.parent.ROM)
    previous = image.read_file(stage.ARM)
    expected,_ = stage.previous.recompile(image,previous,release)
    assert arm==expected and stage.native.digest(arm)==proof["target_ARM9_sha256"]
    cfg = dict(target_arm9_sha256=proof["target_ARM9_sha256"])

    def checked_read(path):
        assert path=="translations/inn_editorial_release_v1.json"
        return cfg

    verify_spans = "assert all(arm[lo:hi]=="
    code = checked_text(getsource(assignment.set_condition),{verify_spans:"assert all(previous[lo:hi]=="})
    prepared = vars(assignment)|dict(read=checked_read,previous=previous)
    exec(compile(code,__file__+"::original_assignment","exec"),prepared)
    code = checked_text(getsource(history.set_condition),{
        verify_spans:"assert all(previous[lo:hi]==",
        "str(months).translate(str.maketrans('0123456789','０１２３４５６７８９')).encode('cp932')":
            "str(months).encode('ascii')",
    })
    context = vars(history)|dict(read=checked_read,previous=previous,assign=prepared["set_condition"])
    exec(compile(code,__file__+"::original_history","exec"),context)
    return context["set_condition"](arm,raw,request)


def schedule():
    commands = [json.loads(line) for line in ORIGINAL.read_text(encoding="utf-8").splitlines()]
    assert commands[0]["condition_fixture"]==(REQUEST|{"months_ago":0})
    commands[0]["condition_fixture"] = REQUEST
    return commands


def capture():
    assert not ROOT.exists()
    inputs,_,_,_,donor = inn.schedule("istanbul")
    path = stage.ROOT/"raid_reload_inputs.json"
    base.save(path,[row for row in inputs if row["start"]<=2801])
    argv = [harness.__file__,"--rom",str(stage.ROM),"--out",str(ROOT),"--battery-save",donor["source"],
        "--inputs-json",str(path),"--press-start","-1","--touchscreen","--frames","6401","--capture-every","999999",
        "--capture-at","3200","--pause-at","3200","--dump-capture-ram","--dump-pause-ram","--allow-condition-fixtures"]
    old,stdin,prior_argv = adapter.set_condition,sys.stdin,sys.argv
    try:
        adapter.set_condition = fixture
        sys.argv = argv
        sys.stdin = StringIO("".join(json.dumps(row)+"\n" for row in schedule()))
        harness.main()
    finally:
        adapter.set_condition,sys.stdin,sys.argv = old,stdin,prior_argv
    assert base.digest(donor["source"])==donor["source_sha256"]


if __name__=="__main__":
    parser = ArgumentParser(description=__doc__)
    parser.parse_args()
    capture()
