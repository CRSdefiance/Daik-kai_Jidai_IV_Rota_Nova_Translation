"""Keep the complete order phrase together without changing the reviewed prose."""

from pathlib import Path
from types import FunctionType

from scripts import stage_navigation_prerequisite_review_v1 as first


ROOT = Path('out/navigation_prerequisites_20261111_v2')
ROM = ROOT / first.ROM.name
PROOF = ROOT / first.PROOF.name
PHRASES = first.PHRASES | {647: ("the order from the Captain's Cabin.",)}


def main():
    compile_storage = FunctionType(first.compile_storage.__code__,
        {**first.compile_storage.__globals__, 'PHRASES': PHRASES})
    run = FunctionType(first.main.__code__, {**first.main.__globals__, '__file__': __file__,
        'ROOT': ROOT, 'ROM': ROM, 'PROOF': PROOF, 'PHRASES': PHRASES, 'compile_storage': compile_storage})
    run()


if __name__ == '__main__':
    main()
