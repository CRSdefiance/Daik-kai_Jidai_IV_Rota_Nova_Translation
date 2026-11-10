"""Preserve stopped V1; adapt menu packet aliases without changing any reader guard."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B52_atomic_tools_v8693');assert not root.exists()
    receipts=[]
    receipts.append(derive('scripts/Hodram_B52_release_paths_v8688.py','scripts/Hodram_B52_release_paths_v8693.py',{
        'Hodram_B52_release_seal_v8689':'Hodram_B52_release_seal_v8693',
        'translations/hodram_B52_editorial_release_v1.json':'translations/hodram_B52_editorial_release_v2.json',
    }))
    receipts.append(derive('dk4tool/patch/hodram_B52_editorial_v1.py','dk4tool/patch/hodram_B52_editorial_v2.py',{
        'Hodram_B52_release_paths_v8688':'Hodram_B52_release_paths_v8693',
        'menu=check_menu_actual(data,doc,image,load,require)':"menu=check_menu_actual({**data,'withdrawal':data['actual'],'opposition':data['opposition_actual']},doc,image,load,require)",
    }))
    receipts.append(derive('scripts/seal_Hodram_B52_release_v8689.py','scripts/seal_Hodram_B52_release_v8693.py',{
        'hodram_B52_editorial_v1':'hodram_B52_editorial_v2','Hodram_B52_release_paths_v8688':'Hodram_B52_release_paths_v8693',
        "previous=read(configurations[-1])":"previous=read('translations/hodram_B52_editorial_release_v1.json')",
        'paths={DOC,NAMES,SEAL,':'paths={DOC,NAMES,SEAL,Path(\'translations/hodram_B52_editorial_release_v1.json\'),',
        'prior_B51_dependency_count':'prior_complete_release_dependency_count',
    }))
    for source,target,root_old,root_new in [
        ('validate_Hodram_B52_atomic_v8690','validate_Hodram_B52_atomic_v8690b','Hodram_B52_atomic_positive_v8690','Hodram_B52_atomic_positive_v8690b'),
        ('validate_Hodram_B52_wrong_memory_v8691','validate_Hodram_B52_wrong_memory_v8691b','Hodram_B52_wrong_memory_v8691','Hodram_B52_wrong_memory_v8691b')]:
        receipts.append(derive('scripts/'+source+'.py','scripts/'+target+'.py',{
            'hodram_B52_editorial_v1':'hodram_B52_editorial_v2','Hodram_B52_release_paths_v8688':'Hodram_B52_release_paths_v8693',root_old:root_new,
        }))
    root.mkdir(parents=True)
    save(root/'derivations.json',dict(derivations=receipts,
         original_failure='Stage supplied actual/opposition_actual; menu reader uses withdrawal/opposition. Add only these two aliases at the menu-reader call. All frozen native/editorial/production guards remain unchanged.',
         stopped_stage_V1_originalseal8689_configV1_positive8690_andwrong_memory8691_preserved=True,
         successor_retains_every_original993_dependency_andall855_predecessor471_native_entries=True,
         no_old_reader_producer_oractual_capture_replay=True))
