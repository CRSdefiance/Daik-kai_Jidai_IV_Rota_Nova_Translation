"""Bind the separate command-atom reconstruction to the complete82-record batch."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B54_B60_independent_preparation_v8810');assert not root.exists()
    result=derive('scripts/verify_Hodram_B31_B53_reconstruction_v8734.py','scripts/verify_Hodram_B54_B60_reconstruction_v8810.py',{
        'work/analysis/Hodram_B31_B53_independent_v8734':'work/analysis/Hodram_B54_B60_independent_v8810',
        'work/analysis/Hodram_B31_B53_relocation_v8728/reconstruction.json':'work/analysis/Hodram_B54_B60_relocation_v8809/reconstruction.json',
        'translations/hodram_B31_B53_editorial_manuscript_v2.json':'translations/hodram_B54_B60_editorial_manuscript_v2.json',
        'work/analysis/Hodram_B31_B53_current_v8722/current_effective.json':'work/analysis/Hodram_B54_B60_current_v8799/current_effective.json',
        "len(commands)==9":"len(commands)==len(p['all_current_commands'])",
        'len(fixups)==(4 if number==31 else 0)':"len(fixups)==len(group['relative_fixups'])",
        'if a!=b]==[31,53]':"if a!=b]==[p['block'] for p in packet['groups']]",
        'for i in [31,53]:':"for i in [p['block'] for p in packet['groups']]:",
        '18 disjoint command atoms across two complete blocks':'152 disjoint command atoms across seven complete blocks',
        'other323_blocks_exact=True':'other318_blocks_exact=True',
        'Independent18-command-atom reconstruction equals both sparse blocks/archive;4fixups recomputed;clean/current/wholearchive/wholeNDS inverses pass.No ROM/credit.':'Independent152-command-atom reconstruction equals all seven sparse blocks/archive;24fixups recomputed;clean/current/wholearchive/wholeNDS inverses pass.No ROM/credit.',
    })
    root.mkdir(parents=True);save(root/'source_locked_independent_derivation.json',dict(derivation=result,
        independent_method='Rebuild complete disjoint command atoms,not sparse speech patches;recompute every target command offset andrelative operand;then reverse complete blocks andwhole archive/ROM.',
        no_ROM_registration_orcompletion_credit=True,new_credit=0,full_goal_complete=False))
