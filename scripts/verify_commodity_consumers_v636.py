"""Repeat the full native consumer checks for the corrected oil terminology."""

from pathlib import Path

from scripts import verify_commodity_consumers_v635 as verify

if __name__ == '__main__':
    verify.ROOT = Path('work/analysis/commodity_fidelity_v636')
    verify.CONFIG = Path('translations/commodity_fidelity_v2.json')
    verify.main()
