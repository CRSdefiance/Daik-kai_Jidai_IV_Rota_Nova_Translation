"""Register the complete reviewed family with exact native proof dependencies."""

import importlib
from copy import deepcopy
from pathlib import Path

from dk4tool.patch import recruitment_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script import common_message_table as parser
from scripts.context_tavern_recruitment_v771 import CURRENT
from scripts.review_tavern_recruitment_v771 import MANUSCRIPT as DRAFT
from scripts.verify_recruitment_consumers_v773 import ROOT
from scripts.verify_village_wrap_v608 import read,save

RESEARCH=Path('work/analysis/recruitment_owned_v772')
MANUSCRIPT=Path('translations/recruitment_editorial_manuscript_v3.json')
CONFIG=Path('translations/recruitment_editorial_release_v1.json')


def main():
    assert not CONFIG.exists() and not MANUSCRIPT.exists()
    ROOT.mkdir(parents=True,exist_ok=True)
    repack=read(RESEARCH/'prospective_common_repack.json')
    copies=[read(RESEARCH/f'native_copies/native_copies_block_{k:02d}.json') for k in range(41)]
    assert {(r['message_id'],r['cold_cache']) for report in copies for r in report['cases']}=={(n,cold) for n in range(3668) for cold in(False,True)}
    assert all(r['COMMON_sha256']==repack['target_COMMON_sha256'] and r['ARM9_sha256']==repack['target_ARM9_sha256'] for r in copies)
    assert all(r['complete_native_copy']['entire_native_span_including_post_NUL_payload_exact'] for report in copies for r in report['cases'])
    assert read(RESEARCH/'native_layout/verification.json')['manuscript_sha256']==sha(DRAFT.read_bytes())
    assert read(RESEARCH/'native_layout/identical_to_reviewed_v771.json')['all3423_complete_case_records_exact']
    assert read(RESEARCH/'dispatch_adapter.json')['paired_scope_and_register_contracts']==128644
    assert read(RESEARCH/'typed_status_contracts.json')['count']==140
    assert read(RESEARCH/'quantity_equivalence.json')['count']==84
    assert read(ROOT/'consumer_routing.json')['original_source_callers_select_nonnull_portrait_core_for_this_family']
    parser_path=Path(parser.__file__);text=parser_path.read_text(encoding='utf-8');digest=repack['directory_sha256']
    assert digest not in text
    (ROOT/'common_message_table_before_v773.py').write_text(text,encoding='utf-8')
    marker='RELOCATED_DIRECTORY_HASHES = frozenset({\n';assert text.count(marker)==1
    parser_path.write_text(text.replace(marker,marker+f'    # V773: exact2151 selections164-2314;25 recruitment/condition entries.\n    "{digest}",\n',1),encoding='utf-8')
    importlib.reload(parser)
    doc=deepcopy(read(DRAFT))
    for row in doc['records']:
        assert not row['review']['formatting'];row['review']['formatting']=True
        row['status']='source-context-native-font-runtime-copy-reviewed-actual-scenes-pending'
    doc['status']='registered-experimental-native-and-copy-reviewed-actual-scenes-pending'
    doc['consumer_routing_proof']=str(ROOT/'consumer_routing.json')
    doc['prior_manuscript_sha256']=sha(DRAFT.read_bytes())
    doc['native_runtime_proof']=str(RESEARCH/'owned_runtime_plan.json')
    save(MANUSCRIPT,doc)
    rom=NdsImage.open(CURRENT);c,a,proof=owned.transform(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),doc)
    assert c==(RESEARCH/'COMMON_RESEARCH_ONLY.bin').read_bytes() and a==(RESEARCH/'COMBINED_ARM9_RESEARCH_ONLY.bin').read_bytes()
    save(ROOT/'native_integration.json',{'source_ROM_sha256':sha(CURRENT.read_bytes()),'target_COMMON_sha256':sha(c),
        'target_ARM9_sha256':sha(a),'proof':proof,'actual_scenes_pending':True})
    registry_path=Path('translations/release_stack.json');registry=read(registry_path)
    assert 'all-routes-unified-v773' not in registry['profiles']
    save(ROOT/'release_stack_before_v773.json',registry)
    profile=deepcopy(registry['profiles']['all-routes-unified-v770']);replays=[]
    for key in('market_stock_editorial_v2','market_contract_editorial','shipyard_editorial','port_services_editorial',
            'tavern_conversations_editorial','tavern_continuation_editorial'):
        original=Path(profile[key]);config=read(original)
        matches=[p for p in config['dependencies'] if Path(p).name==parser_path.name];assert len(matches)==1
        config['dependencies'][matches[0]]=sha(parser_path.read_bytes())
        for p,h in config['dependencies'].items():assert sha(Path(p).read_bytes())==h,p
        target=Path('translations')/f'{key}_replay_for_v773.json';assert not target.exists()
        save(target,config);profile[key]=str(target)
        replays.append({'original':str(original),'original_sha256':sha(original.read_bytes()),'explicit_replay':str(target),
            'only_updated_dependency':matches[0],'target_common_sha256':config['target_common_sha256'],'target_arm9_sha256':config['target_arm9_sha256']})
    save(ROOT/'explicit_parser_replays.json',{'six_frozen_configs_preserved':replays,'one_new_exact_digest':digest})
    paths=[Path(p) for p in('dk4tool/patch/recruitment_editorial.py','dk4tool/patch/recruitment_editorial_runtime.py',
        'dk4tool/patch/recruitment_quantity_runtime.py','dk4tool/patch/tavern_continuation_editorial.py',
        'dk4tool/script/common_message_table.py','scripts/recruitment_owned_runtime_v772.py','scripts/recruitment_quantity_v772.py',
        'scripts/verify_recruitment_owned_v772.py','scripts/verify_recruitment_storage_v772.py',
        'scripts/probe_recruitment_owned_layout_v772.py','scripts/prepare_recruitment_common_v772.py',
        'scripts/verify_recruitment_copies_v772.py','scripts/verify_recruitment_consumers_v773.py')]
    paths += [RESEARCH/p for p in('owned_runtime_plan.json','storage_reference_census.json','quantity_caller_closure.json',
        'quantity_equivalence.json','typed_status_contracts.json','dispatch_adapter.json','dispatch_matrix.json',
        'Thumb_ISA_audit.json','prospective_common_repack.json','native_layout/verification.json',
        'native_layout/identical_to_reviewed_v771.json')]
    paths += [RESEARCH/f'native_copies/native_copies_block_{k:02d}.json' for k in range(41)]
    paths += [ROOT/p for p in('native_integration.json','explicit_parser_replays.json','common_message_table_before_v773.py','consumer_routing.json')]
    save(CONFIG,{'format':'dk4-recruitment-editorial-v1','source_common_sha256':sha(rom.read_file('/COMMON/MESFILE.DK4')),
        'source_arm9_sha256':sha(rom.read_file('/__arm9__.bin')),'target_common_sha256':sha(c),'target_arm9_sha256':sha(a),
        'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'dependencies':{str(p):sha(p.read_bytes()) for p in paths}})
    profile.update({'recruitment_editorial':str(CONFIG),'status':'experimental',
        'description':'Complete V770 plus25 source-reviewed recruitment/condition replies;owned no-growth dispatch,faithful full condition phrases,exact quantities. Actual scenes pending.'})
    registry['profiles']['all-routes-unified-v773']=profile;save(registry_path,registry)
    print('V773 registered with six explicit frozen-output parser replays;actual scenes remain pending.',flush=True)


if __name__=='__main__':main()
