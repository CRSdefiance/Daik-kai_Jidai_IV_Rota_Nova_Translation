"""Exact B210 source/name/control/native-page contract; no global formatter or runtime changes."""
import json
from pathlib import Path
from dataclasses import replace
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
CONTRACT=Path('translations/lil_B210_native_contract_v1.json')
CONTRACT_SHA='97ccdda7a9dec308626d1e25965725dc09bc7e1702e902e86a2641d176be61c0'
ARM9_SHA='4f4e41d26a0b24610a38a9da03dc549e4afec82121a1c72f35665104bb7ea351'
def contract():
    raw=CONTRACT.read_bytes()
    if sha(raw)!=CONTRACT_SHA:raise ValueError('B210 frozen native contract changed')
    d=json.loads(raw)
    for p,digest in d['dependencies'].items():
        if sha(Path(p).read_bytes())!=digest:raise ValueError('B210 native dependency changed:'+p)
    if len(d['record_bindings'])!=10 or d['physical_native_rows_per_page']!=4 or d['complete_native_pages']!=10:raise ValueError('Complete B21010-object/single-page contract required')
    return d
def expected_profile(record_id):
    d=contract()
    if record_id not in d['record_bindings']:raise ValueError('Unreviewed B210 record')
    r=d['record_bindings'][record_id];base=get_dialogue_profile('lil-opening-editorial-native-v1')
    return replace(base,name='lil-B210-source-bound-v1:'+record_id,max_lines=r['maximum_total_rows'],leading_speaker_bytes=frozenset({r['source_selector']}),metrics_source=base.metrics_source+';exact B210 record '+record_id+'. Native viewport216x64,6px ASCII/16px pitch,original guards/pair phase. Every exact paragraph uses one original four-row page. All ten source preambles,static voices and source-matched progressive names remain bound;no runtime/font change.')
def profile_for(arm,source_block,record_id):
    d=contract()
    if sha(arm)!=ARM9_SHA or sha(source_block) not in d['source_block_hashes']:raise ValueError('Exact B210 clean/current source block and V6488 runtime required')
    return expected_profile(record_id)
