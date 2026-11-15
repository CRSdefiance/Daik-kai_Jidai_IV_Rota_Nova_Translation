"""Freeze trusted B49 adapters andderive independent complete source/stored body andtwo-name oracles."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Hodram_B49_native_tools_v8432')
SOURCE=Path('work/analysis/Hodram_B49_source_display_v8386b/source_display.json')
CONTROLS=Path('work/analysis/Hodram_B49_source_controls_v8384/source_controls.json')
MENU=Path('work/analysis/Hodram_B49_menu_v8400/menu_provider_and_planes.json')

NAME_BLOCK='''    # Recompute both scoped default-name planes through the original style11
    # caller;the full-name Joakim field andall207/custom-name scope remain explicit.
    declared=models['name_planes'];require(len(declared)==2 and declared==source['reused_original_scoped_style11_planes'],'two exact scoped source-bound nameplanes')
    names={}
    for name in declared:
        actor=name['actor_ID'];raw=bytes.fromhex(name['input_hex'])
        require((actor,name['text'],raw) in [(1,'Hodram Bergstrom',b'Hodram Bergstrom'),(2,'Lil Argot',b'Lil Argot')],'source-qualified scoped default identity')
        caller=FunctionType(style.style_source_proof.__code__,{**style.style_source_proof.__globals__,'ARM9':sha(arm)},argdefs=style.style_source_proof.__defaults__)
        raster=FunctionType(style.native_name_raster.__code__,{**style.native_name_raster.__globals__,'style_source_proof':caller},argdefs=style.native_name_raster.__defaults__)
        plane,events,usedfont=raster(arm,raw);emitted,flushes=original_name_events(events,raw)
        require(usedfont==font and plane==pixels(arm,font,events) and emitted==codes(raw),'independent complete current style11 name glyphs')
        require(plane==Path(name['native_plane']).read_bytes() and sha(plane)==name['native_plane_sha256'] and events==name['native_glyph_events'] and flushes==name['source_owned_final_zero_ink_flushes'],'complete scoped nameplane/events/flushes')
        require(all(e['style']==11 and e['y']==0 and 0<=e['x'] and e['x']+6<=216 for e in events) and max(e['x']+6 for e in events)==name['original_pair_flush_width'],'current complete scoped name bounds')
        names[actor]=dict(actor_ID=actor,text=name['text'],plane=plane,events=events,width=name['original_pair_flush_width'])
    require(set(names)=={1,2},'both unique source identities')
    return dict(bodies=computed,names=names,
        summary=dict(native_body_pages_recomputed=28,progressive_pages=26,original_FE_pages=2,scoped_style11_nameplanes_recomputed=2,complete_native_models=summaries,
            name_plane_sha256={str(k):sha(v['plane']) for k,v in names.items()},FE_original_index15_ink14_CP932_shadow_not_old_normalized1=True,all_first_internal_final_glyphs_bounds_consumption_andindependent_planes_exact=True,
            original_current_font_oracle_inverse_binding=oracle,new_emulator_runs=0))
'''

if __name__=='__main__':
    assert not ROOT.exists();guard=Path('dk4tool/patch/hodram_B49_native_guards_v1.py');assert not guard.exists()
    adapters={
        'pages':(str(SOURCE),'source_owned_target_page_adapter'),
        'dispatch':(str(SOURCE),'source_owned_dispatch_adapters'),
        'macro_body':(str(SOURCE),'source_owned_macro_body_adapter'),
        'progressive_macro':(str(SOURCE),'source_owned_progressive_adapter'),
        'FE_macro':(str(SOURCE),'source_owned_FE_adapter'),
        'seeded_end':(str(CONTROLS),'source_owned_seeded_end_adapter'),
        'picture':(str(CONTROLS),'source_owned_picture_adapter'),
        'menu_VM':(str(MENU),'source_owned_VM_adapter'),
        'menu_painter':(str(MENU),'source_owned_painter_adapter'),
    }
    trusted={str(p):sha(p.read_bytes()) for p in [SOURCE,CONTROLS,MENU]}
    code='''"""Exact trusted B49 source adapter bindings survive release-dependency challenge tests."""
import json
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.hodram_B49_profile_v2 import contract
ADAPTERS=ADAPTER_VALUES
TRUSTED=TRUSTED_VALUES

def trusted_adapter(name,declared):
    if name not in ADAPTERS:raise ValueError('B49 native adapter:unknown source consumer')
    text,key=ADAPTERS[name];path=Path(text);raw=path.read_bytes();digest=sha(raw);frozen=contract()
    if digest!=TRUSTED[text] or (str(path.resolve()) in frozen['dependencies'] and frozen['dependencies'][str(path.resolve())]!=digest):
        raise ValueError('B49 native adapter:exact trusted source artifact required:'+name)
    expected=json.loads(raw)[key]
    if declared!=expected:raise ValueError('B49 native adapter:exact trusted source-owned adapter required:'+name)
    return expected
'''.replace('ADAPTER_VALUES',repr(adapters)).replace('TRUSTED_VALUES',repr(trusted))
    compile(code,str(guard),'exec');guard.write_text(code,encoding='utf8')
    old=Path('dk4tool/patch/hodram_outcomes_native_evidence_v4.py').read_text('utf8');start=old.index('    # Recompute the nameplane')
    result=derive('dk4tool/patch/hodram_outcomes_native_evidence_v4.py','dk4tool/patch/hodram_B49_native_evidence_v1.py',{
        'hodram_outcomes_native_guards_v3':'hodram_B49_native_guards_v1',
        "source['ARM9_sha256']==stored['ARM9_sha256']==models['ARM9_sha256']==sha(arm)":"source['ARM9_sha256']==data['pages']['ARM9_sha256']==models['ARM9_sha256']==sha(arm)",
        "source['font_sha256']==stored['font_sha256']==models['font_sha256']==sha(font)":"source['font_sha256']==data['pages']['font_sha256']==models['font_sha256']==sha(font)",
        "len(rows)==6 and {r['source_selector'] for r in rows}=={2,254}":"len(rows)==14 and {r['source_selector'] for r in rows}=={1,2,254}",
        'six source-qualified mixed-consumer records':'fourteen source-qualified mixed-consumer records',
        "source['source_owned_target_page_adapter']==stored['source_owned_target_page_adapter']":"source['source_owned_target_page_adapter']",
        "len(declared)==6 and len({r['id'] for r in declared})==6":"len(declared)==14 and len({r['id'] for r in declared})==14",
        'expanded_body=body,source_selector=2)':'expanded_body=body,source_selector=raw[0])',
        old[start:]:NAME_BLOCK,
    })
    ROOT.mkdir(parents=True);save(ROOT/'derivation.json',dict(derivation=result,trusted_adapter_module=str(guard),trusted_adapter_module_sha256=sha(guard.read_bytes()),exact_source_artifact_hashes=trusted,existing_frozen_source_hashes_still_required=True,late_menu_adapter_explicitly_hash_pinned_in_module=True,all_original_font_oracle_native_instruction_ABI_canary_complete_glyph_andbounds_guards_preserved=True,new_credit=0,full_goal_complete=False))
