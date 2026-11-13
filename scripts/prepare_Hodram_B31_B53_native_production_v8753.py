"""Derive independent production glyph models and hard-bound original adapters."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B31_B53_native_tools_v8753');assert not root.exists()
    display=Path('work/analysis/Hodram_B31_B53_source_display_v8720/source_display_andbranch_paths.json')
    controls=Path('work/analysis/Hodram_B31_B53_source_controls_v8718/source_controls.json')
    guard=derive('dk4tool/patch/hodram_B51_native_guards_v1.py','dk4tool/patch/hodram_B31_B53_native_guards_v1.py',{
        'hodram_B51_profile_v1':'hodram_B31_B53_profile_v1','B51':'B31/B53',
        'work/analysis/Hodram_B51_source_display_v8556/source_display.json':display.as_posix(),
        'work/analysis/Hodram_B51_source_controls_v8555/source_controls.json':controls.as_posix(),
        'd0c3ac21329bbe11862db49e6a9cbb45a7ece9967c00f148d10adb1f991b42a8':sha(display.read_bytes()),
        '68e5e6da1254fac674062be1e342d3ac6f216b3194f00bb11c384592e49745b6':sha(controls.read_bytes()),
    })
    original="""    declared=models['name_planes'];require(len(declared)==4 and declared==[b['reused_current_original_style11_plane'] for b in source['scoped_clean_current_four_names_andreused_native_consumers']],'four exact scoped source-bound nameplanes')"""
    bound="""    declared=models['name_planes']
    binding=data['names']['records'][0]['exact_source_current_andnative_bindings']
    expected34=dict(next(p for p in binding['fresh_actor34_name_planes'] if p['text']=='Barbarossa Hayreddin'))
    expected34['original_pair_flush_width']=max(e['x']+(6 if e['kind']=='ascii' else 12) for e in expected34['native_glyph_events'])
    require(len(declared)==2 and declared==[expected34,binding['scoped_reused_actor113']['plane']],'two exact scoped source-bound progressive nameplanes')"""
    native=derive('dk4tool/patch/hodram_B51_native_evidence_v1.py','dk4tool/patch/hodram_B31_B53_native_evidence_v1.py',{
        'hodram_B51_native_guards_v1':'hodram_B31_B53_native_guards_v1',
        "len(rows)==5 and {r['source_selector'] for r in rows}=={1,16,18,113}":"len(rows)==3 and {r['source_selector'] for r in rows}=={34,113}",
        'five source-qualified progressive records':'three source-qualified progressive records',
        "len(declared)==5 and len({r['id'] for r in declared})==5":"len(declared)==3 and len({r['id'] for r in declared})==3",
        original:bound,
        "[(1,'Hodram Bergstrom',b'Hodram Bergstrom'),(16,'Gerhard Adernkatz',b'Gerhard Adernkatz'),(18,'Charles Rochefort',b'Charles Rochefort'),(113,'Port Worker',b'Port Worker')]":"[(34,'Barbarossa Hayreddin',b'Barbarossa Hayreddin'),(113,'Port Worker',b'Port Worker')]",
        "flushes==name['source_owned_final_zero_ink_flushes']":"flushes==name.get('source_owned_final_zero_ink_flushes',name.get('source_owned_zero_ink_flushes'))",
        "require(set(names)=={1,16,18,113},'four unique scoped source identities')":"require(set(names)=={34,113},'two unique scoped source identities')",
        'native_body_pages_recomputed=10,progressive_pages=10':'native_body_pages_recomputed=6,progressive_pages=6',
        'scoped_style11_nameplanes_recomputed=4':'scoped_style11_nameplanes_recomputed=2',
        'no_FE_body_orpalette_scope_in_this_five_progressive_batch':'no_FE_body_orpalette_scope_in_this_three_progressive_batch',
        'and four scoped nameplanes':'and two scoped progressive nameplanes','Recompute four scoped':'Recompute two scoped',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(native_guards=guard,native_models=native,
        all_native_high_integer_constants_andmultiplicity_preserved=True,all_original_native_ASCII_CP932_pixels_complete_codes_pagination_bounds_andfont_inverse_guards_preserved=True,
        actor34_exact_current_progressive_plane_andactor113_exact_reused_plane_bound_separately_from_fullcatalogue_UI=True,
        trusted_source_adapter_paths_andhashes_pinned_independently_of_outer_releaseconfig=True,
        no_native_oractual_probe_replayed_by_preparer_no_ROM_orcredit=True,new_credit=0,full_goal_complete=False))
