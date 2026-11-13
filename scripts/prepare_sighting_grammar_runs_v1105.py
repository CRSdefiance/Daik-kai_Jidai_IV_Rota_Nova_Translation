"""Create versioned startup and original compass-scene replays for V1105."""
from pathlib import Path


def main():
    target=Path('scripts/run_sighting_grammar_startup_v1105.py');assert not target.exists()
    body=Path('scripts/run_sighting_startup_v1086.py').read_text(encoding='utf-8')
    body=body.replace('work/analysis/sighting_release_v1085','work/analysis/sighting_grammar_release_v1104').replace(
        'out/all_routes_combined_v1086_candidate.nds','out/all_routes_combined_v1105_candidate.nds').replace(
        'out/all_routes_combined_v1034_candidate.nds','out/all_routes_combined_v1086_candidate.nds').replace(
        'sighting_v1086_','sighting_grammar_v1105_').replace(
        'reinforcement_sniping_v1034_newgame','sighting_v1086_newgame').replace(
        'reinforcement_sniping_v1034_title','sighting_v1086_title').replace(
        'whole256x384_RGB_exact_to_V1034','whole256x384_RGB_exact_to_V1086').replace(
        'V1034_reference','V1086_reference').replace('V1086:','V1105:').replace('match V1034','match V1086')
    target.write_text(body,encoding='utf-8')
    target=Path('scripts/run_sighting_grammar_gameplay_v1106.py');assert not target.exists()
    body=Path('scripts/run_sighting_gameplay_v1094.py').read_text(encoding='utf-8')
    body=body.replace('out/all_routes_combined_v1086_candidate.nds','out/all_routes_combined_v1105_candidate.nds').replace(
        'sighting_gameplay_v1094_','sighting_grammar_gameplay_v1106_').replace(
        'sighting_v1094_1086_','sighting_grammar_v1106_1105_').replace(
        'scripts.native_sighting_context_v1087b','scripts.native_sighting_grammar_fixture_v1106').replace(
        'scripts/native_sighting_context_v1087b.py','scripts/native_sighting_grammar_fixture_v1106.py')
    target.write_text(body,encoding='utf-8')
    target=Path('scripts/verify_sighting_grammar_gameplay_v1106.py');assert not target.exists()
    body=Path('scripts/verify_sighting_compass_v1094b.py').read_text(encoding='utf-8')
    body=body.replace('work/analysis/sighting_compass_v1094b','work/analysis/sighting_grammar_actual_v1106').replace(
        'sighting_v1094_1086_compassReady8','sighting_grammar_v1106_1105_compassReady8').replace(
        'out/all_routes_combined_v1086_candidate.nds','out/all_routes_combined_v1105_candidate.nds').replace(
        'scripts.native_sighting_context_v1087b','scripts.native_sighting_grammar_fixture_v1106').replace(
        'sighting_gameplay_v1094_compassReady8','sighting_grammar_gameplay_v1106_compassReady8').replace(
        'translations/sighting_editorial_manuscript_v7.json','translations/sighting_editorial_manuscript_v9.json').replace(
        'from dk4tool.patch.sighting_editorial import current_entries','from dk4tool.patch.sighting_grammar_editorial import current_entries').replace(
        'one exact17-byte fixture and normal battle entry pass','one exact17-byte fixture and normal sea return pass')
    target.write_text(body,encoding='utf-8')
    print('Created versioned startup,compass replay,and identity-bound actual verifier;all prior producers preserved.')


if __name__=='__main__':main()
