"""Explicit full-font successor for the V8 faction-grammar draft."""
from pathlib import Path


def main():
    target=Path('scripts/probe_sighting_fonts_v1099.py')
    assert not target.exists()
    body=Path('scripts/probe_sighting_fonts_v1075.py').read_text(encoding='utf-8')
    body=body.replace('work/analysis/sighting_fonts_v1075','work/analysis/sighting_fonts_v1099').replace(
        'work/analysis/sighting_layout_v1074/native_layout_matrix.json','work/analysis/sighting_grammar_v1098b/native_layout_matrix.json').replace(
        'out/all_routes_combined_v1034_candidate.nds','out/all_routes_combined_v1086_candidate.nds')
    before="    arm=Path(matrix['research_ARM9']).read_bytes();assert sha(arm)==matrix['research_ARM9_sha256']\n    rom=NdsImage.open(ROM);assert sha(ROM.read_bytes())==matrix['candidate_sha256']\n"
    assert body.count(before)==1
    body=body.replace(before,"    rom=NdsImage.open(ROM);assert sha(ROM.read_bytes())==matrix['candidate_sha256']\n    arm=rom.read_file('/__arm9__.bin');assert sha(arm)==matrix['ARM9_sha256']\n")
    before="    ROOT.mkdir(parents=True);(ROOT/'previews').mkdir()\n"
    assert body.count(before)==1
    body=body.replace(before,"""    for i,case in enumerate(matrix['cases']):
        if case['message_ID'] in (614,627) and case['bearing']['label']=='vicinity' and bytes.fromhex(case['faction_hex']) in (b'Li Clan',b'Hayreddin Clan',b'Bergstrom Fleet'):
            selected.add(i)
"""+before)
    body=body.replace("'research_ARM9':matrix['research_ARM9'],\n        'research_ARM9_sha256':sha(arm)",
        "'current_ROM_ARM9_sha256':sha(arm)")
    body=body.replace("'runtime_selector_ABI_regressions_registered_integration_and_actual_pending':True",
        "'unchanged_current_runtime_new_registered_prose_integration_and_actual_pending':True")
    target.write_text(body,encoding='utf-8')
    print('Created current-ROM full-font verifier;all prior producers preserved.')


if __name__=='__main__':main()
