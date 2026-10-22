"""Reuse the frozen full-glyph/state checker with the explicit Athens fixture."""

import argparse
from pathlib import Path
from types import FunctionType

from dk4tool.patch.grand_race_menu_release import sha
from scripts import verify_ceremony_families_gameplay_v815 as original
from scripts.native_ceremony_athens_fixture_v816 import set_condition
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/ceremony_Athens_v816')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--spec', type=Path, required=True)
    args = parser.parse_args(); spec = read(args.spec)
    ROOT.mkdir(parents=True, exist_ok=True)
    previous = read('work/analysis/ceremony_access_v810/site_chant_gameplay_verification_v815.json')
    source = Path(original.__file__)
    assert sha(source.read_bytes()) == previous['producer_sha256']
    def Athens_condition(arm, raw, request):
        assert request['mode'] == 'ceremony-family'
        return set_condition(arm, raw, {**request, 'mode': 'ceremony-Athens'})

    loader = FunctionType(original.load.__code__, {**original.__dict__, 'set_condition': Athens_condition})
    verifier = FunctionType(original.verify.__code__, {**original.__dict__,
        'load': loader, 'ROOT': ROOT, '__file__': str(Path(__file__).resolve())})
    verifier(spec)
    temporary = ROOT/(spec['name']+'_gameplay_verification_v815.json')
    proof = read(temporary)
    proof.update(source_checker=str(source), source_checker_sha256=sha(source.read_bytes()),
        original_full_glyph_outside_body_state_time_and_return_checks_unchanged=True,
        only_declared_fixture_function_and_request_mode_rebound=True,
        Athens_fixture_sha256=sha(Path('scripts/native_ceremony_athens_fixture_v816.py').read_bytes()),
        scenario_specification=str(args.spec), scenario_specification_sha256=sha(args.spec.read_bytes()))
    save(ROOT/(spec['name']+'_gameplay_verification_v816.json'), proof)


if __name__ == '__main__':
    main()
