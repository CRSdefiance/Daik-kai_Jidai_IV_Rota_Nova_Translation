"""Replay the staged Ceuta lessons with the recorded ordinary navigation inputs."""

from inspect import getsource
from types import FunctionType, SimpleNamespace

from scripts import audit_rafael_ceuta_arrival_20261119 as baseline
from scripts import observe_rafael_ceuta_arrival_20261119 as original
from scripts import review_rafael_ceuta_contract_routes_20261119 as staged
from scripts.source_locked_derivation_v5118 import checked_text

ROOT = staged.STAGED / 'ordinary_replay'
CAPTURE = ROOT / 'capture'
JOURNAL = ROOT / 'navigation.jsonl'


def capture():
    prior = staged.base.load(baseline.OUTPUT)
    assert staged.base.digest(original.JOURNAL) == prior['evidence'][str(original.JOURNAL)]
    adapter = checked_text(getsource(original.main), {
        "    assert base.digest(active.ROM) == release['candidate_sha256'] == prefix['ROM_sha256']":
            "    assert base.digest(active.ROM) == release['candidate_sha256']\n"
            "    assert release['predecessor_sha256'] == prefix['ROM_sha256'] == prior['candidate_sha256']",
        '    JOURNAL.touch(exist_ok=False)':
            "    assert not JOURNAL.exists()\n    JOURNAL.write_bytes(original.JOURNAL.read_bytes())",
    })
    scope = vars(original) | dict(ROOT=ROOT,CAPTURE=CAPTURE,JOURNAL=JOURNAL,prior=prior,original=original,
        active=SimpleNamespace(ROM=staged.ROM,RELEASE=staged.PROOF),__file__=__file__)
    scope['make_observer'] = FunctionType(original.make_observer.__code__,scope)
    exec(compile(adapter,__file__+'::ordinary-replay','exec'),scope)
    scope['main']()


if __name__ == '__main__':
    capture()
