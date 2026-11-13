"""Exact six-block research image andall143 final padded native targets."""
from pathlib import Path
from types import FunctionType
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.verify_lil_clifford_north_new_world_fonts_v2985 import expand as expand_progressive
from scripts.verify_lil_clifford_north_new_world_FE_v2980 import expand as expand_FE
from scripts.lil_kuhn_china_FE_painter_v2909 import make_painter
from scripts.verify_name_catalog_glyphs_v278 import raster as original_raster,expected_pixels
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Clifford_North_New_World_research_v2990');PARENT=Path('out/all_routes_combined_v2958_candidate.nds')
ROM=ROOT/'lil_Clifford_North_New_World_V2958_derived_RESEARCH_ONLY.nds'
PLAN=Path('work/analysis/lil_Clifford_North_New_World_relocation_v2989/nested_source_relocation_research.json')
FONT=Path('work/analysis/lil_Clifford_North_New_World_font_approval_v2986/all143_native_macro_font_reconciliation.json')
if __name__=='__main__':
    assert not ROOT.exists();plan,font=map(read,[PLAN,FONT]);assert plan['all143_texts_and180_relative_operands_preserved'] and plan['all900_relocated_native_skip_cases_match_original_target_mapping']
    assert sha(PARENT.read_bytes())==plan['candidate_sha256']==font['candidate_sha256'];parent,image=NdsImage.open(PARENT),NdsImage.open(PARENT);arm=image.read_file('/__arm9__.bin');container=IlnkContainer.parse(parent.read_file('/data/SC2.DK4'))
    assert sha(parent.read_file('/data/SC2.DK4'))==plan['source_SC2_sha256'];fe=read('work/analysis/lil_Clifford_North_New_World_FE_v2980/current_FE_macro_font_and_typed_paper_proof.json');fonts={r['id']:r for r in font['cases']+fe['cases']};source=read('work/analysis/lil_Clifford_North_New_World_source_v2965/complete143_clean_current_native_context.json')
    ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_Clifford_North_New_World_fonts_v2985/current_native_input.json',source['historical_snapshot_ROM'],ROOT/'current_native_context')
    class FontROM:
        @staticmethod
        def open(path):assert str(path)=='work/clean.nds';return image
    raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':FontROM},argdefs=original_raster.__defaults__);raster.__kwdefaults__=original_raster.__kwdefaults__
    paint_FE,FE_calibration=make_painter(image)
    parity=[];macro_calls=0
    for block in plan['blocks']:
        n=block['block'];assert n in [67,68,69,149,150,151] and sha(container.blocks[n])==block['source_block_sha256'];target=Path(block['research_block']).read_bytes();assert sha(target)==block['research_block_sha256'] and block['inverse_restoration_recovers_every_original_logical_byte']
        for row in block['text_records']:
            value=bytes.fromhex(row['target_hex']);case=fonts[row['id']];compiled=bytes.fromhex(case['encoded_hex']);assert value==compiled+(b' ' if row['parity_space_added'] else b'') and len(value)%2==row['old_length']%2
            isfe=value[0]==254
            assert value[0] in [2,9,11,12,13,14,16,17,18,20,21,22,27,28,42,92,151,254]
            pipeline=ctx.execute(expand_FE,value[1:]) if isfe else ctx.execute(expand_progressive,value[1:],value[0]);expanded=bytes.fromhex(pipeline['cases'][0]['output_hex'])
            if isfe:
                target_paper=paint_FE(expanded);pixels=target_paper['logical'];events=target_paper['events']
                assert sha(pixels)==case['native_plane_sha256'] and sha(target_paper['physical'])==case['whole_physical228x64_plane_sha256']
                assert target_paper['complete_return_input_object_canaries_and_native_independent_plane_equal']
                assert all(0<=e['y']<=36 and e['x']<=228 for e in events if e['code']==32)
            else:
                pixels,events,kanji=raster(arm,expanded)
                assert pixels==expected_pixels(arm,kanji,events) and sha(pixels)==case['whole_native_plane_sha256']
                assert all(0<=e['y']<=48 and e['x']<=216 for e in events if e['code']==32) and all(0<=e['x']<=210 and 0<=e['y']<=48 for e in events if e['code']!=32)
            assert len(pipeline['cases'])==4;macro_calls+=4;ctx.machines.pop()
            parity.append(dict(id=row['id'],consumer='FE-paper' if isfe else 'progressive',parity_space_added=row['parity_space_added'],target_hex=value.hex(),current_final_target_macro_alignment_cases=pipeline,
                complete_final_target_native_plane_equals_reviewed_plane=True,native_plane_sha256=sha(pixels),complete_native_glyph_events=events,tail_padding_consumed_without_blank_page_or_lost_glyph=True))
        container.blocks[n]=target
    assert len(parity)==143 and macro_calls==572 and not ctx.machines
    data=container.to_bytes();assert sha(data)==plan['target_SC2_sha256']==sha(Path(plan['target_SC2']).read_bytes());image.replace_file('/data/SC2.DK4',data);image.save(ROM);result=NdsImage.open(ROM)
    assert [p for _,p,data in parent.iter_files() if result.read_file(p)!=data]==['/data/SC2.DK4']
    for path,data in parent.iter_components():assert result.read_file(path)==data,path
    before,after=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks for im in [parent,result]];assert len(before)==len(after)==336 and [n for n,(a,b) in enumerate(zip(before,after,strict=True)) if a!=b]==[67,68,69,149,150,151]
    save(ROOT/'research_image_receipt.json',dict(parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),ARM9_sha256=sha(arm),SC2_sha256=sha(result.read_file('/data/SC2.DK4')),COMMON_sha256=sha(result.read_file('/COMMON/MESFILE.DK4')),
        only_changed_file='/data/SC2.DK4',only_changed_blocks=[67,68,69,149,150,151],block_growth_bytes={str(n):len(after[n])-len(before[n]) for n in [67,68,69,149,150,151]},all330_other_SC2_blocks_every_other_file_and_native_component_exact=True,
        all143_final_targets_complete_native_planes_equal_reviewed_planes=True,current_final_padded_macro_alignment_cases=572,final_target_parity_cases=parity,padded_tail_creates_no_extra_page_or_lost_boundary_glyph=True,
        current_FE_typed_painter='scripts/lil_kuhn_china_FE_painter_v2909.py',current_FE_typed_painter_sha256=sha(Path('scripts/lil_kuhn_china_FE_painter_v2909.py').read_bytes()),current_FE_calibration=FE_calibration,current_macro_context_plan=str(ctx.proof_path),current_macro_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        registered_candidate=False,not_for_user_handoff_or_new_parent=True,source_relocation_plan=str(PLAN),source_relocation_plan_sha256=sha(PLAN.read_bytes()),native_font_proof=str(FONT),native_font_proof_sha256=sha(FONT.read_bytes()),
        all3_FE_final_padded_planes_and12_macro_alignments_bound=True,all140_ordinary_final_padded_planes_and560_macro_alignments_bound=True,external_reference_loader_representative_and_registered_release_pending=True,actual_selected_Clifford_North_New_World_IDs=[],new_emulator_runs=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    (ROOT/'RESEARCH_ONLY.txt').write_text('Unregistered V2958-derived Clifford/north/NewWorld six-block source-reference test image. Not a release or construction parent. Preserve this ROM. All other files/components remain exact;registered integration must rebuild the entire canonical cumulative stack.\n',encoding='utf-8')
    print('Research image:only six selectedSC2blocks change;330otherblocks/allotherfiles/components exact.143final nativeplanes/572macro cases pass;not a registeredrelease ornewparent.')
