"""Registered source-bound escape portrait formatter correction."""
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from scripts.escape_direct_runtime_v1183b import apply
from scripts.verify_village_wrap_v608 import read

CONFIG='translations/escape_direct_formatting_release_v1.json'


def current_entries(common,arm):
    from dk4tool.patch.duel_editorial import current_entries as parent_entries
    config=read(CONFIG)
    assert sha(arm)==config['target_arm9_sha256']
    path=Path(config['runtime_plan'])
    assert sha(path.read_bytes())==config['dependencies'][str(path)]
    restored=bytearray(arm)
    for row in read(path)['patches']:
        at=row['address']-0x02000000;target=bytes.fromhex(row['target_hex'])
        assert arm[at:at+len(target)]==target
        restored[at:at+len(target)]=bytes.fromhex(row['source_hex'])
    assert sha(restored)==config['source_arm9_sha256']
    return parent_entries(common,bytes(restored))


def apply_release(arm,path):
    config=read(path)
    assert config['format']=='dk4-escape-direct-formatting-v1'
    assert sha(arm)==config['source_arm9_sha256']
    for name,digest in config['dependencies'].items():
        assert sha(Path(name).read_bytes())==digest,name
    doc=read(config['manuscript'])
    assert doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US'
    assert len(doc['records'])==33 and all(all(row['review'].values()) for row in doc['records'])
    fonts,pipeline=read(config['font_proof']),read(config['source_pipeline_proof'])
    assert len(fonts['cases'])==1417 and len(pipeline['all13_direct_pipeline_cases'])==13
    result,plan=apply(arm)
    assert sha(result)==config['target_arm9_sha256']==fonts['ARM9_sha256']==pipeline['ARM9_sha256']
    old,new=[MainCodeFile(v,0x02000000) for v in (arm,result)]
    shape=lambda c:[(s.ramAddress,len(s.data),s.bssSize) for s in c.sections]
    assert shape(old)==shape(new) and cache_plan(arm)==cache_plan(result)
    assert all(old.sections[i].data==new.sections[i].data for i in (1,2,3,4))
    assert len(new.sections[3].data)-48==123040
    return result,{**plan,'source_bound_direct_pipeline_cases':13,'complete_native_font_cases':1417,
        'release_config':str(path),'release_config_sha256':sha(Path(path).read_bytes()),
        'natural_dialogue_v2_prose_source_glosses_and_all33_compiled_texts_unchanged':True,
        'gameplay_and_editorial_completion_require_separate_evidence':True}
