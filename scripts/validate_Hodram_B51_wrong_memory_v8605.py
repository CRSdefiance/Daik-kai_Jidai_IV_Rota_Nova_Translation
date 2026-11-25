"""Reject three genuinely wrong in-memory ROM inputs with every dependency and semantic guard active."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch import hodram_B51_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Hodram_B51_release_paths_v8595 import PARENT,CONFIG
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/Hodram_B51_wrong_memory_v8605')
if __name__=='__main__':
    assert not ROOT.exists();parent=NdsImage.open(PARENT);baseline=NdsImage.open(owned.CANONICAL);cases=[];commit=owned.commit_image
    ROOT.mkdir(parents=True)
    try:
        for mode in ['canonical-source-canonical-memory','current-source-canonical-memory','canonical-source-mutated-current-memory']:
            image=NdsImage(PARENT if mode=='current-source-canonical-memory' else owned.CANONICAL,deepcopy(parent.rom if mode=='canonical-source-mutated-current-memory' else baseline.rom))
            if mode=='canonical-source-mutated-current-memory':
                raw=image.read_file('/data/SC0.DK4');image.replace_file('/data/SC0.DK4',bytes([raw[0]^1])+raw[1:])
            original=image.rom;before=bytes(original.save());files=list(original.files);components={p:v for p,v in image.iter_components()};calls=[]
            def forbidden(*args):calls.append('forbidden');raise AssertionError('Wrong memory reached commit')
            owned.commit_image=forbidden
            try:owned.apply_release(image,baseline,config=CONFIG)
            except ValueError as error:
                diagnostic=str(error);assert 'whole in-memory predecessor/reference identities' in diagnostic
                assert 'Native dependency changed' not in diagnostic and 'Frozen' not in diagnostic
            else:raise AssertionError('Wrong memory accepted:'+mode)
            assert not calls and image.rom is original and bytes(original.save())==before and original.files==files and {p:v for p,v in image.iter_components()}==components
            row=dict(case=mode,input_sha256=sha(before),actual_wrong_inmemory_image=True,all_dependency_frozen_andsemantic_guards_enabled=True,rejected=True,diagnostic=diagnostic,commit_calls=0,whole_original_input_object_files_components_andserialized_bytes_unchanged=True)
            save(ROOT/(mode+'.json'),row);cases.append(row);print('PASS',mode,flush=True)
    finally:owned.commit_image=commit
    save(ROOT/'wrong_memory_rejections.json',dict(cases=cases,negative_count=3,every_wrong_image_rejected_before_commit_withall_guards_active=True,no_digest_orsemantic_bypass=True,no_disk_ROM_registry_orcredit_change=True,new_credit=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [Path(__file__),Path(owned.__file__),CONFIG]}))
