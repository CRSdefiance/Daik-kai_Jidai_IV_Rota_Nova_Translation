"""Reconcile the current Refit formatter and owned layout before checking the four panels."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/check_reviewed_deck_native_andallocation.py').read_text(encoding='utf-8'),{
    'Shared_Deck_native_andallocation_20261104':'Shared_Deck_native_andallocation_v2_20261104',
    'from dk4tool.patch.deck_explanation_release import format_paragraph':'from dk4tool.dialogue.refit_help import compile_paragraph',
    'from scripts.execute_scene_caption_raster import execute':'from scripts.current_refit_caption_native_v1 import execute',
    "format_paragraph(rows[owner['source_owner_offset']]['english'].removesuffix('{PAD}')).encode('cp932')+b'\\0'":
        "compile_paragraph(rows[owner['source_owner_offset']]['english'].removesuffix('{PAD}'))[0]",
    'len(proposed)==544':'len(proposed)==540',
    "    ROOT.mkdir();sheet=Image.new('RGB',(672,656),'white');draw=ImageDraw.Draw(sheet);cases=[]\n    dims=geometry(ctx.arm);assert dims['dimensions']==[168,84]":
    """    assert all(o['proposed_offset_without_allocation_approval']==o['current_offset'] for o in current)
    proposed_arm=bytearray(ctx.arm);proposed_arm[start:end]=proposed
    inverse=bytearray(proposed_arm);inverse[start:end]=ctx.arm[start:end]
    assert bytes(inverse)==ctx.arm
    layout_path=Path('work/analysis/refit_help_v712/native_layout_proof.json');layout=load(layout_path)
    layout_arm_path=Path('work/analysis/refit_help_v712/target_ARM9.bin');layout_arm=layout_arm_path.read_bytes()
    assert all(ctx.arm[a:b]==layout_arm[a:b] for a,b in layout['layout']['owned_spans'])
    dims=dict(dimensions=[168,108],current_refit_layout_exact_native_proof_reuse=True,
        native_layout_proof=str(layout_path),native_layout_proof_sha256=sha(layout_path.read_bytes()),
        native_layout_ARM9=str(layout_arm_path),native_layout_ARM9_sha256=sha(layout_arm),no_historical_RAM_overlay=True)
    ROOT.mkdir();proposed_path=ROOT/'proposed_ARM9_RESEARCH_ONLY.bin';proposed_path.write_bytes(proposed_arm)
    sheet=Image.new('RGB',(672,1040),'white');draw=ImageDraw.Draw(sheet);cases=[]""",
    "english=row['english'].removesuffix('{PAD}');formatted=format_paragraph(english)\n        if row['decision']=='retention':assert formatted==row['current_stored_text']":
        "english=row['english'].removesuffix('{PAD}');compiled,lines=compile_paragraph(english);formatted=compiled[:-1].decode('ascii')",
    'surface_size=(168,84)':'surface_size=(168,108)',
    "e['y']+12<=36":"e['y']+12<=60",
    'index*164':'index*260',
    'pic.crop((0,0,168,36)).resize((672,144)':'pic.crop((0,0,168,60)).resize((672,240)',
    'proposed_needed_bytes=544,allocation_shortfall_bytes=4':'proposed_needed_bytes=540,allocation_shortfall_bytes=0',
    'three_retained_panels_current_wraps_exact=True':'three_good_wordings_preserved_with_fresh_current_consumer_wraps=True,\n        all31_pointers_andallocations_unchanged=True,current_source_owned_storage_bounds_pass=True,\n        proposed_ARM9=str(proposed_path),proposed_ARM9_sha256=sha(proposed_arm),complete_parent_target_inverse_exact=True',
    'source_owned_storage_solution_andconnected_target_consumers_andactual_gameplay_pending=True':'connected_target_consumers_andactual_gameplay_pending=True',
    "Four native Deck panels/eight mode cases pass;current accepted pool540/proposed544:four-byte allocation issue remains,no ROM changed.":
        'Four current Refit panels/eight native modes pass;validated formatter fits540 source bytes withall31 pointer/allocation positions unchanged;no ROM changed.',
})
exec(compile(source,__file__+'::same-panel-checks-with-qualified-current-Refit-layout-and-formatter','exec'),globals())
