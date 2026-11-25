"""Independent current-native source/stored glyph models and one scoped nameplane validation.

These are disposable native CPU computations, not additional emulator gameplay.
No producer script is replayed and no ROM or live game state is changed.
"""
from types import FunctionType
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Hodram_FE_font_oracles_v8315 import bind
from dk4tool.patch.hodram_B52_native_guards_v1 import trusted_adapter
from scripts.research_lil_B209_native_pages_v6461 import pages as original_pages
from scripts.prove_lil_B208_name_planes_v6405 import codes,original_name_events
from scripts import lil_B207_name_style_v6354d as style

def check_native_models(data,rows,parent,load,require):
    source,stored,models=data['source_display'],data['stored'],data['models'];arm=parent.read_file('/__arm9__.bin');font=parent.read_file('/GRP/KANJI.FNT')
    require(source['ARM9_sha256']==data['pages']['ARM9_sha256']==models['ARM9_sha256']==sha(arm),'exact current native model ARM9')
    require(source['font_sha256']==data['pages']['font_sha256']==models['font_sha256']==sha(font),'exact current native model font')
    require(len(rows)==3 and {r['source_selector'] for r in rows}=={113} and all(r['kind']=='progressive' for r in rows),'three source-qualified progressive records')
    pixels,unused_factory,oracle=bind(parent)
    page_adapter=trusted_adapter('pages',data['pages']['source_owned_target_page_adapter']);require(page_adapter==source['source_owned_target_page_adapter'],'one exact current source-owned page adapter')
    env={**original_pages.__globals__,'expected_pixels':pixels,'codes':codes};exec(compile(page_adapter,__file__+'::exact-current-independent-pages','exec'),env)
    computed={'clean_Japanese':{},'revised_English':{}};summaries=[]
    for version in computed:
        declared=models['native_models'][version];require(len(declared)==3 and len({r['id'] for r in declared})==3,'complete native model membership:'+version)
        for row in rows:
            ident=row['id'];record=next((r for r in declared if r['id']==ident),None);require(record is not None,'native model source record:'+ident)
            ref=next(r for r in stored['records'] if r['id']==ident);raw=bytes.fromhex(row['source_hex'] if version=='clean_Japanese' else ref['stored_hex']);is_FE=row['source_selector']==254
            require(raw[0]==row['source_selector'] and record['source_selector']==raw[0] and record['block']==row['block'] and record['input_hex']==raw.hex(),'native model full source/stored identity:'+ident)
            body=raw[1:].replace(b'FI',b'Hodram').replace(b'FA',b'Bergstrom').replace(b'FO',b'Bergstrom Fleet')
            require(record['expanded_native_hex']==body.hex() and len(record['pages'])==1,'complete expanded native model body/page count:'+ident)
            if is_FE:
                result=paint(body);page=record['pages'][0];plane=Path(page['native_plane']).read_bytes();physical=Path(page['physical_plane']).read_bytes()
                require(len(plane)==228*48 and len(physical)==228*64 and sha(plane)==page['native_plane_sha256'] and sha(physical)==page['physical_plane_sha256'],'complete FE plane extents/digests:'+ident)
                require(result['logical']==plane and result['physical']==physical and result['events']==page['events'],'independent original FE glyphs/logical andphysical planes:'+ident)
                require(page['page']==1 and page['start']==0 and page['end']==len(body) and result['complete_consumed_bytes']==len(body),'complete FE glyph consumption:'+ident)
                require(set(physical)<=({0,14,15} if version=='clean_Japanese' else {0,15}),'original unnormalized FE ink indices:'+ident)
                expected=dict(pages=[dict(page=1,start=0,end=len(body),events=result['events'],native_plane_bytes=plane,physical_plane_bytes=physical)],complete_consumed_bytes=len(body),expanded_body=body,source_selector=254)
            else:
                result=env['pages'](arm,font,body);require(result['complete_consumed_bytes']==len(body) and len(result['pages'])==1,'complete progressive glyph consumption/page count:'+ident)
                fresh=result['pages'][0];page=record['pages'][0];plane=bytes.fromhex(fresh['native_plane_hex']);actual=Path(page['native_plane']).read_bytes()
                require(len(actual)==216*64 and actual==plane and sha(actual)==page['native_plane_sha256'],'independent complete progressive native plane:'+ident)
                for key,value in fresh.items():
                    if key!='native_plane_hex':require(page.get(key)==value,'independent progressive glyph/geometry/consumption metadata:'+ident+':'+key)
                for key,value in result.items():
                    if key!='pages':require(record.get(key)==value,'independent progressive paragraph metadata:'+ident+':'+key)
                expected=dict(pages=[dict(**{k:v for k,v in fresh.items() if k!='native_plane_hex'},native_plane_bytes=plane)],complete_consumed_bytes=len(body),expanded_body=body,source_selector=raw[0])
            computed[version][ident]=expected
            summaries.append(dict(version=version,id=ident,source_selector=raw[0],complete_consumed_bytes=len(body),native_page_count=1,native_plane_sha256=sha(expected['pages'][0]['native_plane_bytes']),physical_plane_sha256=sha(expected['pages'][0]['physical_plane_bytes']) if is_FE else None))
    # Recompute the scoped Port Worker default-name plane through the original style11
    # caller;all207/custom-name scope remains open.
    declared=models['name_planes'];require(len(declared)==1 and declared==[b['reused_current_original_style11_plane'] for b in source['scoped_clean_current_one_name_andreused_native_consumers']],'one exact scoped source-bound nameplane')
    names={}
    for name in declared:
        actor=name['actor_ID'];raw=bytes.fromhex(name['input_hex'])
        require((actor,name['text'],raw) in [(113,'Port Worker',b'Port Worker')],'source-qualified scoped default identity')
        caller=FunctionType(style.style_source_proof.__code__,{**style.style_source_proof.__globals__,'ARM9':sha(arm)},argdefs=style.style_source_proof.__defaults__)
        raster=FunctionType(style.native_name_raster.__code__,{**style.native_name_raster.__globals__,'style_source_proof':caller},argdefs=style.native_name_raster.__defaults__)
        plane,events,usedfont=raster(arm,raw);emitted,flushes=original_name_events(events,raw)
        require(usedfont==font and plane==pixels(arm,font,events) and emitted==codes(raw),'independent complete current style11 name glyphs')
        require(plane==Path(name['native_plane']).read_bytes() and sha(plane)==name['native_plane_sha256'] and events==name['native_glyph_events'] and flushes==name['source_owned_final_zero_ink_flushes'],'complete scoped nameplane/events/flushes')
        require(all(e['style']==11 and e['y']==0 and 0<=e['x'] and e['x']+6<=216 for e in events) and max(e['x']+6 for e in events)==name['original_pair_flush_width'],'current complete scoped name bounds')
        names[actor]=dict(actor_ID=actor,text=name['text'],plane=plane,events=events,width=name['original_pair_flush_width'])
    require(set(names)=={113},'one unique scoped source identity')
    return dict(bodies=computed,names=names,
        summary=dict(native_body_pages_recomputed=6,progressive_pages=6,original_FE_pages=0,scoped_style11_nameplanes_recomputed=1,complete_native_models=summaries,
            name_plane_sha256={str(k):sha(v['plane']) for k,v in names.items()},no_FE_body_orpalette_scope_in_this_three_progressive_batch=True,all_first_internal_final_glyphs_bounds_consumption_andindependent_planes_exact=True,
            original_current_font_oracle_inverse_binding=oracle,new_emulator_runs=0))
