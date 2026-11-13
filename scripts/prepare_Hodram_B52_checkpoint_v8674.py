"""Record the independent native-menu/actual-RGB production check without new credit."""
import ast
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__ == '__main__':
    source_path = Path('scripts/checkpoint_Hodram_B52_v8670.py')
    source = source_path.read_text(encoding='utf-8')
    nodes = {n.targets[0].id: n for n in ast.parse(source).body if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name)}
    proofs = ast.literal_eval(nodes['PROOFS'].value)
    proofs['production_menu'] = 'work/analysis/Hodram_B52_menu_production_v8672/menu_production_validation.json'
    summary = ast.literal_eval(nodes['SUMMARY'].value)
    summary = summary.replace('Remaining required work:source-bound production menu/control-flow/loaders-census/references/actual/comparison readers', 'Remaining required work:source-bound production control-flow/loaders-census/references/actual/comparison readers')
    summary += '\n\nProductionmenu8672 now independently checks six original provider alignments/eighteen bridged0/1/-1returns across complete cleanJapanese/currentpadded/reviewed typedobjects. Exact originalinstructionowners/full123264payload/count/order/width84to72/rectangles/consumption/ABI agree. The independent font oracle checks all12existing capturedmenus/24completeJapanese-Englishcaptions,constructor-based coordinates,first/internal/finalglyphs/blankguards/selectedorunselectedbackgrounds/highlights andthe originalblink-off. Twelve genuinelychanged adapter/table/rectangle/returnkind/caption/selection/scope inputs reject withfrozen guardsactive. No emulatorcapture orpreviousproducer replay;no ROMorcredit. Nativebackingbounds remainoffline;actualowner/RAM/VRAM/palette/backingbyteidentity andcancelavailability remainunclaimed. These results supersede only the earlier production-menu-pending clause;the full remainingobjective remains.'
    next_text = ast.literal_eval(nodes['NEXT'].value)
    next_text = next_text.replace('Continue from verifiedV8671', 'Continue from verifiedV8675')
    next_text = next_text.replace('production reconstruction8666 passes26 andnativeproduction8667 passes10.', 'production reconstruction8666 passes26,nativeproduction8667 passes10 andproductionmenu8672 passes12. Its6nativealignments/18bridgedreturns/12existingRGBmenus/24captions pass;noadditionalgameplay.')
    next_text = next_text.replace('Next complete independentproduction menu evidence,source-controlled', 'Next complete source-controlled')
    changes = {
        ast.get_source_segment(source, nodes['PROOFS']): 'PROOFS = ' + repr(proofs),
        ast.get_source_segment(source, nodes['SUMMARY']): 'SUMMARY = ' + repr(summary),
        ast.get_source_segment(source, nodes['NEXT']): 'NEXT = ' + repr(next_text),
        'checkpoint_v8670': 'checkpoint_v8674', 'verification_v8671': 'verification_v8675',
        'verification_v8661/verified_handoff.json': 'verification_v8671/verified_handoff.json',
        'review_pending_integration_v8670': 'review_pending_integration_v8674',
        'unfinished_editorial_scope_v8670': 'unfinished_editorial_scope_v8674',
        'return prior,data': """menu=data['production_menu'];summary=menu['summary']
    assert menu['negative_count']==12 and menu['all_changed_inputs_rejected_with_frozen_guards_active']
    assert [summary[k] for k in ['native_provider_alignments','bridged_modal_returns','actual_menu_samples','actual_caption_checks']]==[6,18,12,24]
    assert summary['offline_backing_bounds_separate_no_live_owner_RAM_VRAM_palette_orbacking_identity_claim']
    for path,digest in menu['evidence'].items():assert sha(Path(path).read_bytes())==digest
    return prior,data""",
        'frozen_policy243_rejections_andindependent_reconstruction26_native10_verified=True': 'frozen_policy243_rejections_andindependent_reconstruction26_native10_verified=True,production_menu6_alignments18_bridgedreturns12_existing_RGB24_captions12_rejections_verified=True',
        'V8670': 'V8674', 'V8671': 'V8675',
    }
    root = Path('work/analysis/Hodram_B52_checkpoint_tools_v8674')
    assert not root.exists()
    receipt = derive(source_path, 'scripts/checkpoint_Hodram_B52_v8674.py', changes)
    root.mkdir(parents=True)
    save(root / 'derivation.json', receipt)
