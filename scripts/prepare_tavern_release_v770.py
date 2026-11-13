"""Register complete32-entry Tavern continuation after all native copy gates."""

import ast
import importlib
from copy import deepcopy
from pathlib import Path

from dk4tool.patch import tavern_continuation_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script import common_message_table as parser
from scripts.review_tavern_continuation_v768 import MANUSCRIPT as DRAFT
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/tavern_release_v770')
RESEARCH=Path('work/analysis/tavern_runtime_v769')
MANUSCRIPT=Path('translations/tavern_continuation_editorial_manuscript_v3.json')
CONFIG=Path('translations/tavern_continuation_editorial_release_v1.json')
CURRENT=Path('out/all_routes_combined_v767_candidate.nds')


def main():
    assert not CONFIG.exists() and not MANUSCRIPT.exists()
    ROOT.mkdir(parents=True,exist_ok=True)
    repack=read(RESEARCH/'prospective_common_repack.json')
    copies=[read(RESEARCH/'native_copies'/f'native_copies_block_{k:02d}.json') for k in range(41)]
    assert sum(len(r['cases']) for r in copies)==7336
    assert {(r['message_id'],r['cold_cache']) for report in copies for r in report['cases']}=={(n,cold) for n in range(3668) for cold in(False,True)}
    assert all(report['COMMON_sha256']==repack['target_COMMON_sha256'] and report['ARM9_sha256']==repack['target_ARM9_sha256'] for report in copies)
    assert all(r['complete_native_copy']['entire_native_span_including_post_NUL_payload_exact'] for report in copies for r in report['cases'])
    native=read(RESEARCH/'full_output_verification.json')
    assert native['manuscript_sha256']==sha(DRAFT.read_bytes()) and native['new32_complete_scoped_outputs']==14282
    assert not native['immutable_storage_writes']
    assert read(RESEARCH/'runtime_verification.json')['paired_dispatch_cases']==55284
    assert len(read(RESEARCH/'earlier_outputs.json')['all1124_Yard_outputs'])==1124
    parser_path=Path(parser.__file__);text=parser_path.read_text(encoding='utf-8')
    digest=repack['directory_sha256'];assert digest not in text
    (ROOT/'common_message_table_before_v770.py').write_text(text,encoding='utf-8')
    marker='RELOCATED_DIRECTORY_HASHES = frozenset({\n';assert text.count(marker)==1
    parser_path.write_text(text.replace(marker,marker+f'    # V770: exact2151 selections164-2314;32 Tavern continuation entries.\n    "{digest}",\n',1),encoding='utf-8')
    importlib.reload(parser)
    doc=deepcopy(read(DRAFT))
    for r in doc['records']:
        assert not r['review']['formatting'];r['review']['formatting']=True
        r['status']='source-context-native-layout-and-copy-reviewed-actual-gameplay-pending'
    doc['status']='native-and-copy-reviewed-registered-experimental-actual-gameplay-pending'
    doc['prior_manuscript_sha256']=sha(DRAFT.read_bytes())
    doc['native_runtime_proof']=str(RESEARCH/'full_output_verification.json')
    doc['native_copy_proof']=str(RESEARCH/'native_copies')
    save(MANUSCRIPT,doc)
    rom=NdsImage.open(CURRENT)
    c,a,proof=owned.transform(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),doc)
    assert c==(RESEARCH/'COMMON_RESEARCH_ONLY.bin').read_bytes()
    assert a==(RESEARCH/'COMBINED_ARM9_RESEARCH_ONLY.bin').read_bytes()
    save(ROOT/'native_integration.json',{'source_ROM_sha256':sha(CURRENT.read_bytes()),
        'target_COMMON_sha256':sha(c),'target_ARM9_sha256':sha(a),'proof':proof,
        'all7336_whole_native_copy_spans_pass':True,'actual_gameplay_pending':True})
    registry_path=Path('translations/release_stack.json');registry=read(registry_path)
    assert 'all-routes-unified-v770' not in registry['profiles']
    save(ROOT/'release_stack_before_v770.json',registry)
    profile=deepcopy(registry['profiles']['all-routes-unified-v767']);replays=[]
    for key in('market_stock_editorial_v2','market_contract_editorial','shipyard_editorial','port_services_editorial','tavern_conversations_editorial'):
        previous=Path(profile[key]);config=read(previous)
        matches=[p for p in config['dependencies'] if Path(p).name==parser_path.name];assert len(matches)==1
        config['dependencies'][matches[0]]=sha(parser_path.read_bytes())
        for path,h in config['dependencies'].items():assert sha(Path(path).read_bytes())==h,path
        target=Path('translations')/f'{key}_replay_for_v770.json';assert not target.exists()
        save(target,config);profile[key]=str(target)
        replays.append({'original':str(previous),'original_sha256':sha(previous.read_bytes()),'explicit_replay':str(target),
            'only_updated_dependency':matches[0],'target_common_sha256':config['target_common_sha256'],'target_arm9_sha256':config['target_arm9_sha256']})
    save(ROOT/'explicit_parser_replays.json',{'five_original_configs_preserved':replays,'one_new_exact_directory_digest':digest})
    dependencies=[Path(p) for p in('dk4tool/patch/tavern_continuation_editorial.py','dk4tool/patch/tavern_continuation_runtime.py',
        'scripts/review_tavern_continuation_v768.py','dk4tool/script/common_message_table.py',
        'scripts/tavern_continuation_runtime_v769.py','scripts/verify_tavern_ownership_v769.py',
        'scripts/verify_tavern_runtime_v769.py','scripts/verify_tavern_outputs_v769.py','scripts/verify_tavern_earlier_v769.py',
        'scripts/prepare_tavern_common_research_v769.py','scripts/verify_tavern_copies_v769.py')]
    dependencies+=[RESEARCH/name for name in('owned_runtime_plan.json','runtime_verification.json','full_output_verification.json',
        'earlier_outputs.json','prospective_common_repack.json','provider_verification.json','dispatch_matrix.json')]
    dependencies+=[RESEARCH/'native_copies'/f'native_copies_block_{k:02d}.json' for k in range(41)]
    dependencies+=[ROOT/'native_integration.json',ROOT/'explicit_parser_replays.json',ROOT/'common_message_table_before_v770.py']
    for path in dependencies:
        if path.suffix=='.py':ast.parse(path.read_text(encoding='utf-8'),filename=str(path))
    save(CONFIG,{'format':'dk4-tavern-continuation-editorial-v1',
        'source_common_sha256':sha(rom.read_file('/COMMON/MESFILE.DK4')),'source_arm9_sha256':sha(rom.read_file('/__arm9__.bin')),
        'target_common_sha256':sha(c),'target_arm9_sha256':sha(a),
        'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'dependencies':{str(path):sha(path.read_bytes()) for path in dependencies}})
    profile.update({'tavern_continuation_editorial':str(CONFIG),'status':'experimental',
        'description':'Complete V767 plus32 source-reviewed Tavern cost/round/treasure/fleet replies;full private region phrases and corrected player-vocative target. Full native/ownership/copy gates pass;actual scenes pending.'})
    registry['profiles']['all-routes-unified-v770']=profile;save(registry_path,registry)
    print('V770 full profile registered;five frozen configurations replay unchanged outputs with the exact new parser digest. Actual gameplay pending.',flush=True)


if __name__=='__main__':main()
