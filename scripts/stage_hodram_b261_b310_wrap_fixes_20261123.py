"""Stage the remaining Hodram wrap revisions from the rebound B261–B310 packet."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import pair_hodram_b261_b310_wrap_fixes_20261123 as bound
from scripts import register_hodram_b221_b260_wrap_fixes_20261123 as registered
from scripts import stage_hodram_b221_b260_wrap_fixes_20261123 as prior
from scripts.source_locked_derivation_v5118 import checked_text


base, native, paired = prior.base, prior.native, prior.paired
BATCH = Path(".codex-release-work/hodram_b261_b310_wrap_fixes_20261123/release")
ROOT = BATCH / "staged"
REVIEW, PREFLIGHT = BATCH / "contextual_review.json", BATCH / "native_preflight.json"
ROM = ROOT / "Hodram_B261_B310_Wraps_STAGED.nds"
PROOF, NATIVE = ROOT / "stored_proof.json", ROOT / "native_display.json"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
FE_PROOF = ROOT / "unchanged_FE_pages.json"
MANUSCRIPT = paired.OUTPUT.with_name("b261_b310_working_review.md")
ARCHIVE = prior.ARCHIVE
review = SimpleNamespace(REVIEW=REVIEW, PREFLIGHT=PREFLIGHT)
parent = registered
PROTECTION = {
    (266, 6): ["I need you to bring someone in.", "I know I can count on you."],
    (274, 76): ["They say the king enshrined there", "has to give you his blessing",
                "before you can claim the treasure.", "It's worth a try, I'd say."],
    (279, 5): ["Hmm... What am I going to do?", "Looks like I'll have to ask you..."],
    (279, 15): ["he's been prowling", "the Mediterranean.", "I'm counting on you.", "Here's your advance."],
    (281, 12): ["I'd better stop Hernan.", "He's prowling the Mediterranean."],
    (282, 19): ["The Arab pirate is Iscal Yasar.", "He's beaten fleet after fleet.",
                "You're our last hope.", "I'm counting on you."],
    (283, 64): ["Those very Proofs of Conquest.", "all over the world."],
    (286, 5): ["At last, Mr. FA!", "I've been looking for you.", "I need you to stop a gang."],
    (286, 43): ["He won't be easy to catch...", "All right. I'll take the job."],
    (287, 69): ["You've shown what you can do.", "I'd like to ask a favor.", "I need you to find some ruins."],
    (287, 84): ["You mean I'm the strongest warrior?"],
    (291, 49): ["It looks quite deep...", "But it's our only way forward."],
    (291, 152): ["Hmm... We'll only hurt more people.", "Close combat!"],
    (294, 75): ["come in as we did", "and died here..."],
    (297, 251): ["We'll need timber to make charcoal."],
    (298, 176): ["in the Indian Ocean", "should sell it."],
    (305, 27): ["Golden? Oh, that temple!", "It's a fair way off..."],
    (309, 178): ["Form up! Break through together!"],
}

scope = prior.scope | globals()
proposal_source = checked_text(prior.proposal_source, {"len(rows) == 29": "len(rows) == 18"})
exec(compile(proposal_source, __file__ + "::manuscript", "exec"), scope)
source = checked_text(prior.source, {
    '    candidate = packet["candidate_sha256"]':
        '    bound.main()\n'
        '    binding = base.load(bound.OUTPUT)\n'
        '    candidate = binding["candidate_sha256"]',
    '    packet = packet | {"groups":[g for g in packet["groups"] if 221 <= g["block"] <= 260]}':
        '    packet = packet | {"groups":[g | {"current_archive_sha256":binding["installed_archive_sha256"]}'
        ' for g in packet["groups"] if 261 <= g["block"] <= 310]}',
    'block in (226, 238, 239, 252) and selector == 208': 'block in (291, 294, 309) and selector in (208, 211, 214, 215, 216, 218)',
    'block in (224, 243, 251, 252)': 'block in (291, 294, 309)',
    'len(records) == 310 and len(captions) == 11 and len(styles) == 37 and len(groups) == 22':
        'len(records) == 183 and len(captions) == 7 and len(styles) == 115 and len(groups) == 14',
    'sum(row["kind"] == "system" for row in records) == 16': 'sum(row["kind"] == "system" for row in records) == 15',
    '{"retention":281, "prose":29}': '{"retention":165, "prose":14, "wrap_only":4}',
    'len(leads) == 29': 'len(leads) == 17',
    'source_packet_sha256=base.digest(paired.OUTPUT),':
        'source_packet_sha256=base.digest(paired.OUTPUT), exact_rebinding_sha256=base.digest(bound.OUTPUT),',
})
exec(compile(source, __file__ + "::contextual-review", "exec"), scope)
inherited_run = FunctionType(prior.run.__code__, scope)
preflight_source = checked_text(getsource(scope["native_review"].preflight), {
    'tokens=[t for t in ("FO","FI") if t.encode("ascii") in body]':
        'assert row["route"] == 1\n        tokens=[t for t in ("FO","FI","FA") if t.encode("ascii") in body]',
    '"FI":default_first[row["route"]]}': '"FI":default_first[row["route"]],"FA":"Bergstrom"}',
    '"FI":"W"*16}': '"FI":"W"*16,"FA":"W"*16}',
})
preflight_scope = scope["native_review"].preflight.__globals__ | dict(
    REVIEW=REVIEW, PREFLIGHT=PREFLIGHT, ROOT=BATCH, parent=parent)
exec(compile(preflight_source, __file__ + "::surname-layout-preflight", "exec"), preflight_scope)


def run(action):
    if action == "preflight":
        preflight_scope["preflight"]()
    else:
        inherited_run(action)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("review", "preflight", "stage", "native_display", "patch", "startup"))
    run(cli.parse_args().action)
