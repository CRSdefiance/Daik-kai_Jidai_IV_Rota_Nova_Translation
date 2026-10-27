"""Re-run full scoped layouts with the proposed production-address runtime."""

import inspect
from pathlib import Path
from types import FunctionType

from scripts import probe_recruitment_layout_v771 as prior
from scripts import recruitment_owned_runtime_v772 as runtime
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/recruitment_owned_v772')


def main():
    env=dict(prior.__dict__)
    env.update({'runtime':runtime,'OUT':ROOT/'native_layout','CONTRACT_ROOT':ROOT,'__file__':__file__})
    env['formatter']=FunctionType(prior.formatter.__code__,env)
    source=inspect.getsource(prior.main)
    marker="contracts=read(ROOT/'typed_status_contracts.json')"
    assert source.count(marker)==1;source=source.replace(marker,"contracts=read(CONTRACT_ROOT/'typed_status_contracts.json')")
    exec(compile(source,str(Path(__file__)),'exec'),env);env['main']()
    old=read('work/analysis/tavern_recruitment_editorial_v771/native_layout_phrases_v2/matrix.json')
    new=read(ROOT/'native_layout/matrix.json')
    assert new==old
    save(ROOT/'native_layout/identical_to_reviewed_v771.json',{'all3423_complete_case_records_exact':True,
        'reference_matrix_sha256':sha(Path('work/analysis/tavern_recruitment_editorial_v771/native_layout_phrases_v2/matrix.json').read_bytes()),
        'current_matrix_sha256':sha((ROOT/'native_layout/matrix.json').read_bytes()),
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})


if __name__=='__main__':main()
