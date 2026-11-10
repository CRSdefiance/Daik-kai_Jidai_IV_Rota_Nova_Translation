"""Derive independent B50 native body/name readers and immutable original adapter guards."""
import ast
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Hodram_B50_native_tools_v8519')
SOURCE=Path('work/analysis/Hodram_B50_source_display_v8487/source_display.json')
CONTROLS=Path('work/analysis/Hodram_B50_source_controls_v8486/source_controls.json')
if __name__=='__main__':
    assert not ROOT.exists();oldpath=Path('dk4tool/patch/hodram_B49_native_guards_v1.py');text=oldpath.read_text(encoding='utf-8')
    assignments={n.targets[0].id:ast.get_source_segment(text,n.value) for n in ast.parse(text).body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name)}
    adapters={
        'pages':(str(SOURCE),'source_owned_target_page_adapter'),
        'dispatch':(str(SOURCE),'source_owned_dispatch_adapters'),
        'macro_body':(str(SOURCE),'source_owned_macro_body_adapter'),
        'progressive_macro':(str(SOURCE),'source_owned_progressive_adapter'),
        'FE_macro':(str(SOURCE),'source_owned_FE_adapter'),
        'seeded_end':(str(CONTROLS),'source_owned_seeded_end_adapter'),
        'picture':(str(CONTROLS),'source_owned_picture_adapter'),
    }
    trusted={str(p):sha(p.read_bytes()) for p in [SOURCE,CONTROLS]}
    for p,key in adapters.values():assert key in read(p)
    tools=[derive(str(oldpath),'dk4tool/patch/hodram_B50_native_guards_v1.py',{
        assignments['ADAPTERS']:repr(adapters),assignments['TRUSTED']:repr(trusted),
        'hodram_B49_profile_v2':'hodram_B50_profile_v2','B49':'B50',
    })]
    tools.append(derive('dk4tool/patch/hodram_B49_native_evidence_v1.py','dk4tool/patch/hodram_B50_native_evidence_v1.py',{
        'hodram_B49_native_guards_v1':'hodram_B50_native_guards_v1',
        "len(rows)==14 and {r['source_selector'] for r in rows}=={1,2,254}":"len(rows)==3 and {r['source_selector'] for r in rows}=={2,254}",
        'fourteen source-qualified mixed-consumer records':'three source-qualified mixed-consumer records',
        "len(declared)==14 and len({r['id'] for r in declared})==14":"len(declared)==3 and len({r['id'] for r in declared})==3",
        "len(declared)==2 and declared==source['reused_original_scoped_style11_planes']":"len(declared)==1 and declared==[source['reused_original_Lil_style11_plane']]",
        'two exact scoped source-bound nameplanes':'one exact scoped source-bound Lil nameplane',
        "[(1,'Hodram Bergstrom',b'Hodram Bergstrom'),(2,'Lil Argot',b'Lil Argot')]":"[(2,'Lil Argot',b'Lil Argot')]",
        "set(names)=={1,2},'both unique source identities'":"set(names)=={2},'one unique scoped source identity'",
        'native_body_pages_recomputed=28,progressive_pages=26,original_FE_pages=2,scoped_style11_nameplanes_recomputed=2':'native_body_pages_recomputed=6,progressive_pages=4,original_FE_pages=2,scoped_style11_nameplanes_recomputed=1',
        'Recompute both scoped default-name planes':'Recompute the scoped Lil default-name plane',
        'caller;the full-name Joakim field andall207/custom-name scope remain explicit.':'caller;all207/custom-name scope remains open.',
    }))
    tools.append(derive('scripts/validate_Hodram_B49_native_v8433.py','scripts/validate_Hodram_B50_native_v8520.py',{
        'hodram_B49_native_evidence_v1':'hodram_B50_native_evidence_v1',
        'Hodram_B49_independent_native_v8433':'Hodram_B50_independent_native_v8520',
        'Hodram_B49_source_display_v8386b':'Hodram_B50_source_display_v8487',
        'Hodram_B49_stored_v8399':'Hodram_B50_stored_v8496',
        'Hodram_B49_models_v8408':'Hodram_B50_models_v8506',
        'Hodram_B49_pages_v8395':'Hodram_B50_pages_v8492b',
        'translations/hodram_B49_editorial_manuscript_v4.json':'translations/hodram_B50_editorial_manuscript_v5.json',
        "summary['native_body_pages_recomputed']==28 and summary['scoped_style11_nameplanes_recomputed']==2":"summary['native_body_pages_recomputed']==6 and summary['scoped_style11_nameplanes_recomputed']==1",
        "len(result['bodies']['revised_English'])==14 and set(result['names'])=={1,2}":"len(result['bodies']['revised_English'])==3 and set(result['names'])=={2}",
        'dk4tool/patch/hodram_B49_native_evidence_v1.py':'dk4tool/patch/hodram_B50_native_evidence_v1.py',
        'dk4tool/patch/hodram_B49_native_guards_v1.py':'dk4tool/patch/hodram_B50_native_guards_v1.py',
        'B49 independent native:':'B50 independent native:',
        'Independent B49 native:28 complete source/stored pages,26progressive/twoFE,two original style11names.':'Independent B50 native:6 complete source/stored pages,4progressive/twoFE,one original style11name.',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'derivations.json',dict(tools=tools,trusted_adapter_artifact_hashes=trusted,all_native_high_integer_constants_andmultiplicity_preserved=True,all_original_font_oracle_native_instruction_ABI_canary_complete_glyph_andbounds_guards_preserved=True,no_actual_emulator_orproducer_replay=True,new_credit=0,full_goal_complete=False))
