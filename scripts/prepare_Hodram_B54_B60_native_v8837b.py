"""Bind trusted original adapters and extend independent native evidence to167 pages/ten names."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive as original_derive,checked_text

def derive(a,b,changes):
    target=Path(b);expected=checked_text(Path(a).read_text(encoding='utf-8'),changes)
    if not target.exists():return original_derive(a,b,changes)
    assert target.read_text(encoding='utf-8')==expected
    return dict(previous=a,previous_sha256=sha(Path(a).read_bytes()),successor=b,successor_sha256=sha(target.read_bytes()),reused_exact_completed_output_of_stopped_preparer=True,native_high_integer_constants_and_multiplicity_preserved=True)

from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha

SOURCE='work/analysis/Hodram_B54_B60_source_display_v8794/82_complete_source_dispatches_alignments_pages_andmacro_binding.json'
CONTROL='work/analysis/Hodram_B54_B60_source_controls_v8791/source_controls.json'
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B54_B60_native_tools_v8837b');assert not root.exists()
    guards=derive('dk4tool/patch/hodram_B31_B53_native_guards_v1.py','dk4tool/patch/hodram_B54_B60_native_guards_v1.py',{
        'B31/B53':'B54-B60','hodram_B31_B53_profile_v1':'hodram_B54_B60_profile_v1',
        'work/analysis/Hodram_B31_B53_source_display_v8720/source_display_andbranch_paths.json':SOURCE,
        'work/analysis/Hodram_B31_B53_source_controls_v8718/source_controls.json':CONTROL,
        'd052892fa0047378b78f38ae2da882d52f8d3efa5c4e3dc5f70e69460de624ff':sha(Path(SOURCE).read_bytes()),
        '7c0145b879065b4e318785970b411699fa5963e3c9e4834b5970d4a8e7a1fcc9':sha(Path(CONTROL).read_bytes()),
    })
    old_progressive="""                result=env['pages'](arm,font,body);require(result['complete_consumed_bytes']==len(body) and len(result['pages'])==1,'complete progressive glyph consumption/page count:'+ident)
                fresh=result['pages'][0];page=record['pages'][0];plane=bytes.fromhex(fresh['native_plane_hex']);actual=Path(page['native_plane']).read_bytes()
                require(len(actual)==216*64 and actual==plane and sha(actual)==page['native_plane_sha256'],'independent complete progressive native plane:'+ident)
                for key,value in fresh.items():
                    if key!='native_plane_hex':require(page.get(key)==value,'independent progressive glyph/geometry/consumption metadata:'+ident+':'+key)
                for key,value in result.items():
                    if key!='pages':require(record.get(key)==value,'independent progressive paragraph metadata:'+ident+':'+key)
                expected=dict(pages=[dict(**{k:v for k,v in fresh.items() if k!='native_plane_hex'},native_plane_bytes=plane)],complete_consumed_bytes=len(body),expanded_body=body,source_selector=raw[0])"""
    new_progressive="""                # Cache only the pure original CPU calculation, keyed by full exact
                # runtime/font/body/adapter inputs. Every supplied model and every
                # dependency guard is checked on every invocation, including hits.
                cache_key=(arm,font,body,page_adapter)
                if cache_key not in _PAGE_CACHE:
                    _PAGE_CACHE[cache_key]=json.dumps(env['pages'](arm,font,body),sort_keys=True)
                result=json.loads(_PAGE_CACHE[cache_key])
                require(result['complete_consumed_bytes']==len(body) and len(result['pages'])==expected_pages,'complete progressive glyph consumption/page count:'+ident)
                checked_pages=[]
                for fresh,page in zip(result['pages'],record['pages'],strict=True):
                    plane=bytes.fromhex(fresh['native_plane_hex']);actual=Path(page['native_plane']).read_bytes()
                    require(len(actual)==216*64 and actual==plane and sha(actual)==page['native_plane_sha256'],'independent complete progressive native plane:'+ident)
                    for key,value in fresh.items():
                        if key!='native_plane_hex':require(page.get(key)==value,'independent progressive glyph/geometry/consumption metadata:'+ident+':'+key)
                    checked_pages.append(dict(**{k:v for k,v in fresh.items() if k!='native_plane_hex'},native_plane_bytes=plane))
                for key,value in result.items():
                    if key!='pages':require(record.get(key)==value,'independent progressive paragraph metadata:'+ident+':'+key)
                expected=dict(pages=checked_pages,complete_consumed_bytes=len(body),expanded_body=body,source_selector=raw[0])"""
    old_names="""    declared=models['name_planes'];require(len(declared)==1 and declared==[source['reused_original_Lil_style11_plane']],'one exact scoped source-bound Lil nameplane')"""
    new_names="""    declared=models['name_planes'];source_names=data['source_names'];expected_names=[]
    for item in source_names['fresh_twenty_progressive_andfull_current_getters']['rows']:
        if item['consumer']!='progressive-nameplate':continue
        plane=dict(next(p for p in source_names['native_name_planes'] if p['text']==item['text']))
        plane.update(actor_ID=item['actor_ID'],original_pair_flush_width=max(e['x']+(6 if e['kind']=='ascii' else 12) for e in plane['native_glyph_events']))
        expected_names.append(plane)
    require(len(declared)==10 and declared==expected_names,'ten exact scoped source-bound progressive nameplanes')"""
    module=derive('dk4tool/patch/hodram_B50_native_evidence_v1.py','dk4tool/patch/hodram_B54_B60_native_evidence_v1.py',{
        'scoped Lil nameplane':'ten scoped progressive nameplanes',
        'from types import FunctionType':'import json\nfrom types import FunctionType',
        'hodram_B50_native_guards_v1':'hodram_B54_B60_native_guards_v1',
        '\ndef check_native_models(':'\n_PAGE_CACHE={}\n\ndef check_native_models(',
        "len(rows)==3 and {r['source_selector'] for r in rows}=={2,254}":"len(rows)==82 and {r['source_selector'] for r in rows}=={1,20,23,24,36,84,113,114,119,141,254}",
        'three source-qualified mixed-consumer records':'82 source-qualified mixed-consumer records',
        "len(declared)==3 and len({r['id'] for r in declared})==3":"len(declared)==82 and [r['id'] for r in declared]==[r['id'] for r in rows]",
        "require(record['expanded_native_hex']==body.hex() and len(record['pages'])==1":"expected_pages=1 if version=='clean_Japanese' else row['expected_native_pages']\n            require(record['expanded_native_hex']==body.hex() and len(record['pages'])==expected_pages",
        old_progressive:new_progressive,
        'native_page_count=1,native_plane_sha256=sha(expected[\'pages\'][0][\'native_plane_bytes\'])':'native_page_count=len(expected[\'pages\']),native_plane_sha256=[sha(p[\'native_plane_bytes\']) for p in expected[\'pages\']]',
        old_names:new_names,
        "require((actor,name['text'],raw) in [(2,'Lil Argot',b'Lil Argot')],'source-qualified scoped default identity')":"binding=next((r for r in data['names']['records'] if r['actor_ID']==actor),None)\n        require(binding is not None and name['text']==binding['current_display'] and raw.hex()==binding['source_andcurrent_native_references']['current_text_hex'],'source-qualified scoped default identity')",
        "flushes==name['source_owned_final_zero_ink_flushes']":"flushes==name.get('source_owned_final_zero_ink_flushes',name.get('source_owned_zero_ink_flushes'))",
        "set(names)=={2},'one unique scoped source identity'":"set(names)=={1,20,23,24,36,84,113,114,119,141},'ten unique scoped source identities'",
        'native_body_pages_recomputed=6,progressive_pages=4,original_FE_pages=2,scoped_style11_nameplanes_recomputed=1':'native_body_pages_recomputed=167,progressive_pages=165,original_FE_pages=2,scoped_style11_nameplanes_recomputed=10',
        '    return dict(bodies=computed,names=names,':"    require(sum(len(r['pages']) for version in computed.values() for r in version.values())==167,'complete167source-andstored native pages')\n    return dict(bodies=computed,names=names,",
    })
    validation=derive('scripts/validate_Hodram_B31_B53_native_production_v8754.py','scripts/validate_Hodram_B54_B60_native_production_v8838.py',{
        'hodram_B31_B53':'hodram_B54_B60','Hodram_B31_B53_native_validation_v8754':'Hodram_B54_B60_native_validation_v8838',
        'review_Hodram_B31_B53_actual_v8744':'review_Hodram_B54_B60_actual_v8825',
        "ROOT=Path('work/analysis/Hodram_B31_B53_native_validation_v8754')":"PROOFS={**PROOFS,'source_display':'"+SOURCE+"','source_names':'work/analysis/Hodram_B54_B60_names_v8792/ten_source_identities_current_getters_voices_andplanes.json','pages':'work/analysis/Hodram_B54_B60_pages_v8804/compiled_native_pages.json'}\nROOT=Path('work/analysis/Hodram_B54_B60_native_validation_v8838')",
        'editorial_manuscript_v5.json':'editorial_manuscript_v4.json','speaker_name_review_v3.json':'speaker_name_review_v2.json',
        'B31/B53 native evidence:':'B54-B60 native evidence:','Frozen Hodram-B31-B53 contract changed':'Frozen Hodram-B54-B60 contract changed',
        "['native_body_pages_recomputed']==6":"['native_body_pages_recomputed']==167",
        "['scoped_style11_nameplanes_recomputed']==2":"['scoped_style11_nameplanes_recomputed']==10",
        "set(result['names'])=={34,113}":"set(result['names'])=={1,20,23,24,36,84,113,114,119,141}",
        'six_complete_source_andstored_native_pages_two_current_progressive_names_andall_independent_pixels_exact':'all167_complete_source_andstored_native_pages_ten_current_progressive_names_andall_independent_pixels_exact',
        'Independent production native:6complete source/stored pages+2names match;12semantic defects reject withfrozen/trusted guardsactive. No emulator/ROMcommit orcredit.':'Independent production native:167complete source/stored pages+10names match;12semantic defects reject withfrozen/trusted guardsactive. No emulator/ROMcommit orcredit.',
    })
    root.mkdir(parents=True);save(root/'source_locked_native_evidence.json',dict(guards=guards,module=module,validation=validation,all_original_independent_progressive_FE_physical_logical_glyph_palette_bounds_consumption_andname_guards_preserved=True,three_English_multipage_records_allpages_compared=True,pure_original_CPU_pages_cached_only_by_full_ARM9_font_body_andadapter_inputs_every_declared_model_anddependency_rechecked_onhits=True,new_credit=0,full_goal_complete=False))
