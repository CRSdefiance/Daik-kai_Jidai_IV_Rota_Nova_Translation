"""Derive B168 complete-object relocation and distinct FE stored-byte validation."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/lil_B168_relocation_tools_v4190')

if __name__ == '__main__':
    assert not ROOT.exists()
    tools = [derive('scripts/research_lil_B167_relocation_v4139.py', 'scripts/research_lil_B168_relocation_v4190.py', {
        'Relocate B167 complete speeches and labels; preserve twelve spans and both separated ends.': 'Relocate all54 B168 speeches; preserve twelve spans, all effects and both consecutive ends.',
        'lil_B167_relocation_v4139': 'lil_B168_relocation_v4190',
        'lil_B167_editorial_manuscript_v12': 'lil_B168_editorial_manuscript_v7',
        "MENU=Path('translations/lil_B167_choice_manuscript_v2.json')": 'MENU=None',
        "doc,menu=read(DOC),read(MENU);voice={'records':[]}": "doc=read(DOC);menu={'records':[]};voice={'records':[]}",
        'all_routes_combined_v4110': 'all_routes_combined_v4160',
        'assert number==167 and len(end_maps)==2': 'assert number==168 and len(end_maps)==2',
        "assert [e['source_offset'] for e in end_maps]==[430,2172] # refusal and lecture have distinct ends": "assert [e['source_offset'] for e in end_maps]==[2906,2910] # both predecessor end words remain consecutive",
        'for r in results)==27': 'for r in results)==54',
        "sum(len(r['choice_commands']) for r in results)==1": "sum(len(r['choice_commands']) for r in results)==0",
        'for r in results)==46': 'for r in results)==82',
        '[167]': '[168]',
        'choices=str(MENU),choices_sha256=sha(MENU.read_bytes())': 'choices=None,choices_sha256=None',
        'one_original2100_object_two_source_ordered_accept_refuse_labels=True': 'no_source2100_or4100_objects=True',
        'all27speech_and12_relative_operands': 'all54speech_and12_relative_operands',
        'source_FE_system_objects=0': 'source_FE_system_objects=3',
        'two_separated_declared_refusal_and_lecture_endwords_exact': 'two_consecutive_declared_endwords_exact',
        '46commands/27speech/one2100/12spans/60targetskipcases,two distinct ends': '82commands/54speech/threeFE/12spans/60targetskipcases,two consecutive ends',
    })]
    tools.append(derive('scripts/prove_lil_B167_stored_v4140.py', 'scripts/prove_lil_B168_stored_v4191.py', {
        'all27': 'all54', 'lil_B167_stored_v4140': 'lil_B168_stored_v4191',
        'lil_B167_editorial_manuscript_v12': 'lil_B168_editorial_manuscript_v7',
        'lil_B167_relocation_v4139': 'lil_B168_relocation_v4190',
        'lil_B167_voices_v4120': 'lil_B168_voices_v4170',
        '[2,4,13,23,109]': '[2,6,9,20,76,87,165,166,254]',
        'len(cases)==27': 'len(cases)==54', 'fresh+reused==108': 'fresh+reused==216',
        'stored_targets108': 'stored_targets216', 'current_final_stored_macro_alignment_cases=108': 'current_final_stored_macro_alignment_cases=216',
        'stored_targets=27,progressive=27,FE=0': 'stored_targets=54,progressive=51,FE=3', 'macro_cases=108': 'macro_cases=216',
        'from scripts.verify_village_wrap_v608 import read,save': 'from scripts.verify_village_wrap_v608 import read,save\nfrom scripts.lil_kuhn_china_FE_painter_v2909 import make_painter',
        "if fe:\n                    targetpaint=paint(expanded)": "if fe:\n                    if paint is None:paint,calibration=make_painter(image)\n                    targetpaint=paint(expanded)",
    }))
    ROOT.mkdir(parents=True)
    save(ROOT / 'source_derivation.json', dict(tools=tools, no_ROM_registry_ledger_orcredit_change=True,
        source_scope=dict(block=168, speeches=54, progressive=51, FE=3, commands=82, relative_sites=12,
                          target_skip_cases=60, stored_macro_cases=216, clean_end_offsets=[2906,2910],
                          predecessor_end_offsets_verified=[2906,2910], predicates=3, A000=1,
                          resources=4, presentations=6, FI=7, FA=1, FO=1)))
    print('B168 relocation/stored proof successors prepared; both predecessor end offsets verified from the current command census.')
