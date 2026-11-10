"""Validate independent complete B49 references/whole inverse and every saved loader/caller case."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_B49_references_v1 import reconstruct_and_bind
from dk4tool.patch.hodram_B49_loaders_v1 import check_loaders_and_census
from scripts.validate_Hodram_B49_native_v8433 import require
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B49_independent_refs_v8443')
PROOFS={
 'relocation':'work/analysis/Hodram_B49_relocation_v8398/reconstruction.json',
 'current':'work/analysis/Hodram_B49_choice_binding_v8387b/current_with_choices.json',
 'source_controls':'work/analysis/Hodram_B49_source_controls_v8384/source_controls.json',
 'loaders':'work/analysis/Hodram_B49_loaders_v8404/325_whole_native_loads_cache_hits650_initial_parent_modes.json',
 'callers':'work/analysis/Hodram_B49_references_v8405b/references.json',
}
if __name__=='__main__':
    assert not ROOT.exists();doc=read('translations/hodram_B49_editorial_manuscript_v4.json');data={k:read(p) for k,p in PROOFS.items()}
    parent=NdsImage.open(doc['current_ROM']);reference=NdsImage.open(doc['reference_ROM']);clean=NdsImage.open('work/clean.nds')
    result=reconstruct_and_bind(parent,clean,reference,doc,data,require);loaders=check_loaders_and_census(data,parent,reference,result,read,require)
    canonical=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');canonical.rom=parent.rom
    second=reconstruct_and_bind(canonical,clean,reference,doc,data,require)
    require(second['target_archive']==result['target_archive'],'canonical source/current in-memory image lifecycle produces identical archive')
    ROOT.mkdir(parents=True);save(ROOT/'independent_references.json',dict(references=result['summary'],loaders=loaders,canonical_source_withfull_current_ROM_positive=True,no_new_emulator_orloader_producer_replay=True,no_ROM_orcompletion_credit_change=True,new_credit=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [Path(__file__),Path('dk4tool/patch/hodram_B49_references_v1.py'),Path('dk4tool/patch/hodram_B49_loaders_v1.py'),*map(Path,PROOFS.values())]}))
    print('Independent B49:16source/current/final references,whole clean/current inverses/all324unownedblocks/allunownedfiles,325wholeloads/650parentmodes/326actions/fresh shippedcensus pass. Canonical.source+current.rom passes.No replay orcredit.')
