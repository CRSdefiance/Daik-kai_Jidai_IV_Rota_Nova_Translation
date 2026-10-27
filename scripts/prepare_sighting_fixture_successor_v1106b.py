"""Rebind the unchanged terrain helper to the exact new ROM,not a historical hash."""
from pathlib import Path


def main():
    target=Path('scripts/native_sighting_grammar_fixture_v1106b.py');assert not target.exists()
    body=Path('scripts/native_sighting_grammar_fixture_v1106.py').read_text(encoding='utf-8')
    before="    function=FunctionType(original.apply_fixture.__code__,{**original.apply_fixture.__globals__,'read':mapped_read},\n"
    after="""    current_water=FunctionType(original.water.__code__,{**original.water.__globals__,
        'ROM':Path('out/all_routes_combined_v1105_candidate.nds')},argdefs=original.water.__defaults__)
    function=FunctionType(original.apply_fixture.__code__,{**original.apply_fixture.__globals__,
        'read':mapped_read,'water':current_water},
"""
    assert body.count(before)==1;body=body.replace(before,after);target.write_text(body,encoding='utf-8')
    target=Path('scripts/run_sighting_grammar_gameplay_v1106b.py');assert not target.exists()
    body=Path('scripts/run_sighting_grammar_gameplay_v1106.py').read_text(encoding='utf-8')
    body=body.replace('sighting_grammar_gameplay_v1106_','sighting_grammar_gameplay_v1106b_').replace(
        'sighting_grammar_v1106_1105_','sighting_grammar_v1106b_1105_').replace(
        'scripts.native_sighting_grammar_fixture_v1106','scripts.native_sighting_grammar_fixture_v1106b').replace(
        'scripts/native_sighting_grammar_fixture_v1106.py','scripts/native_sighting_grammar_fixture_v1106b.py')
    target.write_text(body,encoding='utf-8')
    target=Path('scripts/verify_sighting_grammar_gameplay_v1106b.py');assert not target.exists()
    body=Path('scripts/verify_sighting_grammar_gameplay_v1106.py').read_text(encoding='utf-8')
    body=body.replace('sighting_grammar_actual_v1106','sighting_grammar_actual_v1106b').replace(
        'sighting_grammar_v1106_1105_','sighting_grammar_v1106b_1105_').replace(
        'sighting_grammar_gameplay_v1106_','sighting_grammar_gameplay_v1106b_').replace(
        'scripts.native_sighting_grammar_fixture_v1106','scripts.native_sighting_grammar_fixture_v1106b')
    target.write_text(body,encoding='utf-8')
    print('Explicit fixture/runner/verifier successors created;original terrain code and guards preserved.')


if __name__=='__main__':main()
