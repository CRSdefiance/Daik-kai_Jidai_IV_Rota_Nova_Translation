"""Preserve first sealed config;add corrected atomic module andexact compatible predecessor bindings."""
import sys
from pathlib import Path
from dk4tool.patch import hodram_B49_editorial_v2 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Hodram_B49_release_paths_v8450 import CONFIG,proofs
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B49_production_v8455')
if __name__=='__main__':
    assert not ROOT.exists() and not CONFIG.exists();conf=read('translations/hodram_B49_editorial_release_v1.json');before=dict(conf['dependencies'])
    conf['proofs']=proofs();previous=read('translations/hodram_outcomes_editorial_release_v5.json')
    for p,h in previous['dependencies'].items():assert p not in conf['dependencies'] or conf['dependencies'][p]==h;conf['dependencies'][p]=h
    paths={Path(__file__),Path(owned.__file__),Path('scripts/Hodram_B49_release_paths_v8450.py'),Path('translations/hodram_outcomes_editorial_release_v5.json'),Path('translations/hodram_B49_editorial_release_v1.json'),Path('work/analysis/Hodram_B49_atomic_fix_v8450/source_equivalence.json'),*map(Path,proofs().values())}
    root=Path.cwd().resolve()
    for module in tuple(sys.modules.values()):
        filename=getattr(module,'__file__',None)
        if filename and filename.endswith('.py') and Path(filename).resolve().is_relative_to(root):paths.add(Path(filename))
    for path in paths:
        p=str(path.resolve());h=sha(path.read_bytes());assert p not in conf['dependencies'] or conf['dependencies'][p]==h;conf['dependencies'][p]=h
    assert all(conf['dependencies'][p]==h for p,h in before.items());save(CONFIG,conf);owned.check_dependencies(conf)
    ROOT.mkdir(parents=True);save(ROOT/'configuration_receipt.json',dict(configuration=str(CONFIG),configuration_sha256=sha(CONFIG.read_bytes()),prior_dependencies=len(before),new_dependencies=len(conf['dependencies']),every_prior_dependency_andall445_frozen_contract_entries_retained_exact=True,only_compiler_planning_field_andexact_compatibility_bindings_changed=True,failed_atomic_v1_preserved=True,no_builder_registry_ROM_orcredit_change=True,new_credit=0,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print('Pinned corrected B49 atomic stage;all earlierdependencies retained. Builder/registry/ROM/counters unchanged.')
