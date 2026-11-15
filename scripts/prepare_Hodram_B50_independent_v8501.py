"""Derive independent command-atom reconstruction for the complete twelve-command B50 program."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Hodram_B50_independent_tools_v8501')
if __name__=='__main__':
    assert not ROOT.exists();result=derive('scripts/verify_Hodram_B49_reconstruction_v8402.py','scripts/verify_Hodram_B50_reconstruction_v8501.py',{
        'Hodram_B49_independent_v8402':'Hodram_B50_independent_v8501','Hodram_B49_relocation_v8398':'Hodram_B50_relocation_v8495','translations/hodram_B49_editorial_manuscript_v2.json':'translations/hodram_B50_editorial_manuscript_v2.json',
        'work/analysis/Hodram_B49_choice_binding_v8387b/current_with_choices.json':'work/analysis/Hodram_B50_current_v8488/current_effective.json',
        'blocks[49]':'blocks[50]','len(commands)==36 and len(speeches)==14':'len(commands)==12 and len(speeches)==3','len(fixups)==8':'len(fixups)==0',
        '36 disjoint command atoms;0100 contributes only its four-byte header while nested commands contribute their own atoms':'12 disjoint command atoms;all three six-byte preambles andnine nontext controls/fullterminal are independently reconstructed',
        'Independent36-command-atom reconstruction equals sparse block/archive;8 offsets recomputed;clean/current block andwhole parent archive recover exactly.No ROM/credit.':'Independent12-command-atom B50 reconstruction equals sparseblock/archive;zero relatives;wholeclean/current blocks andparent archive recoverexactly.NoROM/credit.',
    })
    ROOT.mkdir(parents=True);save(ROOT/'derivation.json',dict(derivation=result,all_native_numeric_constants_andmultiplicity_preserved=True,all_original_disjoint_atom_preamble_extent_parity_tail_andinverse_checks_preserved=True,no_ROM_orcredit=True,new_credit=0,full_goal_complete=False))
