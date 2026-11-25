"""Allow only independently measured RNG data changes; preserve every native constant."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B227_seal_repair_v7317b')
if __name__=='__main__':
    assert not ROOT.exists()
    old="    r=derive('scripts/seal_lil_B226_references_v7269.py','scripts/seal_lil_B227_references_v7317.py',changes);ROOT.mkdir(parents=True);save(ROOT/'source_locked_reference_seal.json',r)"
    new="""    source=Path('scripts/seal_lil_B226_references_v7269.py').read_text('utf8')
    for key in changes:assert key in source,key
    planned=re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m.group(0)],source);compile(planned,'B227-measured-seal','exec')
    oldproof=Path('work/analysis/lil_B226_later_v7266/following_final_components_and_measured_timing_RNG_RGB_limits.json');newproof=Path('work/analysis/lil_B227_later_v7314/following_final_components_and_measured_timing_RNG_RGB_limits.json');oldseeds=read(oldproof)['final_PRNG_seeds'];newseeds=read(newproof)['final_PRNG_seeds']
    before,after=native_numbers(source),native_numbers(planned)
    assert before-after==Counter(oldseeds) and after-before==Counter(newseeds)
    r=derive('scripts/seal_lil_B226_references_v7269.py','scripts/seal_lil_B227_references_v7317.py',changes)
    assert Path('scripts/seal_lil_B227_references_v7317.py').read_text('utf8')==planned
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_reference_seal.json',dict(tool=r,only_changed_high_integer_data_are_independently_measured_final_PRNG_seeds=True,old_measured_seeds=oldseeds,new_measured_seeds=newseeds,all_other_native_high_integer_values_andmultiplicity_exact=True,evidence={str(p):sha(p.read_bytes()) for p in [oldproof,newproof]},original_overbroad_numeric_preflight_failure_preserved=True))"""
    r=derive('scripts/prepare_lil_B227_seal_v7317.py','scripts/prepare_lil_B227_seal_v7317b.py',{'from scripts.source_locked_derivation_v5118 import derive':"import re\nfrom collections import Counter\nfrom scripts.source_locked_derivation_v5118 import native_numbers\nfrom scripts.prepare_lil_B156_layout_v3705 import derive\nfrom scripts.verify_village_wrap_v608 import read\nfrom dk4tool.patch.grand_race_menu_release import sha",'lil_B227_seal_tools_v7317':'lil_B227_seal_tools_v7317b',old:new})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_measured_seed_only_repair.json',r)
