"""Register complete arrival prose as one stage after the full V788 stack."""

from copy import deepcopy
from pathlib import Path

from dk4tool.patch import arrival_notices_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=owned.ROOT
CONFIG=Path('translations/arrival_notices_editorial_release_v1.json')
MANUSCRIPT=Path('translations/arrival_notices_editorial_manuscript_v3.json')
DRAFT=Path('translations/arrival_notices_editorial_manuscript_v2.json')


def main():
    assert not CONFIG.exists() and not MANUSCRIPT.exists()
    draft=read(DRAFT);native=read(ROOT/'native_verification.json')
    assert native['manuscript_sha256']==sha(DRAFT.read_bytes()) and len(native['layouts'])==49
    production=deepcopy(draft)
    for row in production['records']:
        assert all(row['review'][g] for g in ('source','context','localization','naturalness')) and not row['review']['formatting']
        row['review']['formatting']=True
        row['status']='source-native-reviewed-registered-experimental-actual-revised-GPU-pending'
        row['context']+=' V792 original modal consumer and printf are bound to native faction/number getters. Complete native layouts/fonts/copies pass;actual revised GPU playback remains required.'
    production.update({'reviewed_research_manuscript':str(DRAFT),'reviewed_research_manuscript_sha256':sha(DRAFT.read_bytes()),
        'status':'registered-experimental-actual-gameplay-pending','whole_batch_completion_credit':False})
    save(MANUSCRIPT,production)
    rom=NdsImage.open('out/all_routes_combined_v788_candidate.nds')
    c,a,proof=owned.plan(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),production['records'])
    assert c==(ROOT/'COMMON_RESEARCH_ONLY.bin').read_bytes() and a==(ROOT/'ARM9_RESEARCH_ONLY.bin').read_bytes()
    registry=read('translations/release_stack.json');assert 'all-routes-unified-v792' not in registry['profiles']
    assert len(registry['accepted_layers'])==114
    inherited=deepcopy(registry['profiles']['all-routes-unified-v788'])
    frozen={}
    for value in inherited.values():
        if isinstance(value,str) and value.endswith('.json') and Path(value).exists():
            cfg=read(value);frozen[value]=sha(Path(value).read_bytes())
            for p,h in cfg.get('dependencies',{}).items():assert sha(Path(p).read_bytes())==h,p;frozen[p]=h
    save(ROOT/'frozen_prior_dependencies.json',frozen)
    save(ROOT/'release_stack_before_v792.json',registry)
    files=[Path(p) for p in ('dk4tool/patch/arrival_notices_editorial.py','dk4tool/patch/captain_prompt_wrap.py',
        'dk4tool/patch/item_diplomacy_editorial.py','dk4tool/script/common_message_table.py',
        'scripts/prepare_item_common_v788.py','scripts/prepare_recruitment_common_v772.py',
        'scripts/verify_arrival_native_v792.py','scripts/verify_arrival_consumer_v792.py','scripts/verify_arrival_copies_v792.py',
        'scripts/native_call_abi_v764.py','scripts/native_machine_scoped_v764.py',str(DRAFT))]
    files += [ROOT/p for p in ('native_verification.json','consumer_proof.json','visual_review.json','prospective_repack.json')]
    files += [ROOT/f'native_copies/native_copies_block_{b:02d}.json' for b in range(6)]
    save(CONFIG,{'format':'dk4-arrival-notices-editorial-v1','source_common_sha256':owned.SOURCE_COMMON,
        'source_arm9_sha256':owned.SOURCE_ARM,'target_common_sha256':sha(c),'target_arm9_sha256':sha(a),
        'directory_sha256':proof['directory_sha256'],'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'dependencies':{str(p):sha(p.read_bytes()) for p in files}})
    assert owned.apply_release(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),CONFIG)[:2]==(c,a)
    profile=deepcopy(inherited)
    profile.update({'arrival_notices_editorial':str(CONFIG),'status':'experimental',
        'description':'Full V788 stack plus three independent complete courier-status paragraphs and scoped existing-allocation modal balancing. Actual revised arrival playback pending.'})
    registry['profiles']['all-routes-unified-v792']=profile
    save('translations/release_stack.json',registry)
    assert all(sha(Path(p).read_bytes())==h for p,h in frozen.items())
    print('V792 registered;all inherited dependencies and profiles retained.Production playback pending.',flush=True)


if __name__=='__main__':main()
