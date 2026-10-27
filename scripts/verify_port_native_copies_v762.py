"""Run the frozen ARM946 full-copy verifier on the V762 research components."""

from pathlib import Path

import scripts.verify_shipyard_native_copies_v760 as verifier


if __name__ == '__main__':
    verifier.ROOT = Path('work/analysis/port_services_v762')
    verifier.main()
