"""Replay the Lisbon stock boundary on the verified Ceuta candidate."""

from inspect import getsource
from types import FunctionType, SimpleNamespace

from scripts import observe_lisbon_extra_stock_20261124 as stock
from scripts import register_ceuta_contract_refusal_20261124 as current
from scripts.stage_cartridge_title_20261123 import digest, reference, write


ROOT = stock.ROOT.with_name("editorial_20261124_lisbon_stock_quota")
CONTROLLER = ROOT / "controller.jsonl"
OPENING = stock.ACTIONS[:4]


def main():
    # Keep the earlier fixture and ordinary input prefix. Only the candidate,
    # capture path and subsequent controller commands change.
    previous = SimpleNamespace(**(vars(stock.prior) | {"current": current}))
    scope = vars(stock) | dict(prior=previous, ROOT=ROOT, CONTROLLER=CONTROLLER, ACTIONS=OPENING, __file__=__file__)
    scope["finance_prerequisite"] = FunctionType(stock.finance_prerequisite.__code__, scope)
    FunctionType(stock.main.__code__, scope)()
    write(ROOT / "stock_quota_runner.json", dict(
        source=reference(__file__), reused_launcher=reference(stock.__file__), controller=reference(CONTROLLER),
        fixture_function_sha256=stock.sha256(getsource(stock.finance_prerequisite).encode()).hexdigest(),
        candidate=reference(current.RELEASE), rom_sha256=digest(current.ROM)))


if __name__ == "__main__":
    main()
