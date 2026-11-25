"""Register all Palace prose after the complete V792 inherited release stack."""

from copy import deepcopy
from pathlib import Path

from dk4tool.patch import palace_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=owned.ROOT
CONFIG=Path('translations/palace_editorial_release_v1.json')
MANUSCRIPT=Path('translations/palace_editorial_manuscript_v3.json')
DRAFT=Path('translations/palace_editorial_manuscript_v2.json')


def main():
    assert not CONFIG.exists() and not MANUSCRIPT.exists()
    production=deepcopy(read(DRAFT));native=read(ROOT/'production_layout.json')
    assert native['manuscript_sha256']==sha(DRAFT.read_bytes()) and native['native_layouts']==323
    for row in production['records']:
        assert all(row['review'][g] for g in ('source','context','localization','naturalness'))
        assert not row['review']['formatting']
        row['review']['formatting']=True
        row['status']='source-native-production-reviewed;experimental-actual-revised-playback-pending'
        row['context']+=' V797 verifies the stored paragraph through the original trampoline and exact parent dispatcher. Native complete copies and fonts pass;actual revised playback remains required.'
    production.update({'reviewed_research_manuscript':str(DRAFT),'reviewed_research_manuscript_sha256':sha(DRAFT.read_bytes()),
        'status':'registered-experimental-actual-gameplay-pending','whole_batch_completion_credit':False})
    save(MANUSCRIPT,production)
    rom=NdsImage.open('out/all_routes_combined_v792_candidate.nds')
    c,a,proof=owned.plan(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),production['records'])
    assert c==(ROOT/'COMMON_RESEARCH_ONLY.bin').read_bytes() and a==(ROOT/'COMBINED_ARM9_RESEARCH_ONLY.bin').read_bytes()
    registry=read('translations/release_stack.json');assert 'all-routes-unified-v797' not in registry['profiles']
    assert len(registry['accepted_layers'])==114
    inherited=deepcopy(registry['profiles']['all-routes-unified-v792'])
    frozen={}
    for value in inherited.values():
        if isinstance(value,str) and value.endswith('.json') and Path(value).exists():
            cfg=read(value);frozen[value]=sha(Path(value).read_bytes())
            for p,h in cfg.get('dependencies',{}).items():assert sha(Path(p).read_bytes())==h,p;frozen[p]=h
    save(ROOT/'frozen_prior_dependencies.json',frozen)
    save(ROOT/'release_stack_before_v797.json',registry)
    files=[Path(p) for p in ('dk4tool/patch/palace_editorial.py','dk4tool/patch/palace_editorial_runtime.py',
        'dk4tool/patch/item_diplomacy_runtime.py','dk4tool/patch/arrival_notices_editorial.py',
        'dk4tool/script/common_message_table.py','scripts/prepare_item_common_v788.py',
        'scripts/prepare_recruitment_common_v772.py','scripts/context_palace_v795.py',
        'scripts/prepare_palace_v797.py','scripts/verify_palace_runtime_v796.py','scripts/verify_palace_copies_v797.py',
        'scripts/native_call_abi_v764.py','scripts/native_machine_scoped_v764.py',str(DRAFT))]
    files += [ROOT/p for p in ('production_layout.json','prospective_common_repack.json')]
    files += [Path('work/analysis/palace_editorial_v795/native_context.json'),
        Path('work/analysis/palace_editorial_v795/prototype_layout/visual_review.json')]
    files += [Path('work/analysis/palace_runtime_v796')/p for p in ('bounded_compaction.json','scope_proof.json','status_contracts.json')]
    first,last=proof['repacked_block_range']
    files += [ROOT/f'native_copies/native_copies_block_{b:02d}.json' for b in range(first,last+1)]
    save(CONFIG,{'format':'dk4-palace-editorial-v1','source_common_sha256':owned.SOURCE_COMMON,
        'source_arm9_sha256':owned.SOURCE_ARM,'target_common_sha256':sha(c),'target_arm9_sha256':sha(a),
        'directory_sha256':proof['directory_sha256'],'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'dependencies':{str(p):sha(p.read_bytes()) for p in files}})
    assert owned.apply_release(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),CONFIG)[:2]==(c,a)
    registry['profiles']['all-routes-unified-v797']={**inherited,'palace_editorial':str(CONFIG),'status':'experimental',
        'description':'Full V792 stack plus31 source-reviewed Palace paragraphs and exact scoped existing-allocation formatting. Actual revised Palace gameplay pending.'}
    save('translations/release_stack.json',registry)
    assert all(sha(Path(p).read_bytes())==h for p,h in frozen.items())
    print('V797 registered;all earlier profiles,114 accepted layers and frozen dependencies preserved.',flush=True)


if __name__=='__main__':main()
