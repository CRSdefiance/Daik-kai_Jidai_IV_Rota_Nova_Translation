"""Ten-block research image and 220 complete final stored paragraph proofs."""
from pathlib import Path
from types import FunctionType
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.verify_lil_B111_B119_fonts_v3234c import expand as expand_progressive
from scripts.verify_lil_B111_B119_FE_v3231 import expand as expand_FE
from scripts.lil_kuhn_china_FE_painter_v2909 import make_painter
from scripts.verify_name_catalog_glyphs_v278 import raster as original_raster, expected_pixels
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/lil_B111_B119_research_v3240b')
PARENT=Path('out/all_routes_combined_v3204_candidate.nds')
ROM=ROOT/'lil_B111_B119_V3204_derived_RESEARCH_ONLY.nds'
PLAN=Path('work/analysis/lil_B111_B119_relocation_v3239b/nested_source_relocation_research.json')
FONT=Path('work/analysis/lil_B111_B119_font_approval_v3236/all150_native_macro_font_reconciliation.json')

if __name__=='__main__':
    assert not ROOT.exists()
    plan,font=map(read,[PLAN,FONT])
    assert plan['all116speech_34aliased_alternatives_no_choices_and64_relative_operands_preserved']
    assert plan['all320_relocated_native_skip_cases_match_original_target_mapping']
    assert sha(PARENT.read_bytes())==plan['candidate_sha256']==font['candidate_sha256']
    parent,image=NdsImage.open(PARENT),NdsImage.open(PARENT)
    arm=image.read_file('/__arm9__.bin');container=IlnkContainer.parse(parent.read_file('/data/SC2.DK4'))
    fonts={r['id']:r for r in font['cases']}
    assert sha(parent.read_file('/data/SC2.DK4'))==plan['source_SC2_sha256']
    source=read(plan['source_context'])
    ROOT.mkdir(parents=True)
    ctx=CurrentContext('work/analysis/lil_B111_B119_fonts_v3234c/current_native_input.json',
        source['historical_snapshot_ROM'],ROOT/'current_native_context')
    class FontROM:
        @staticmethod
        def open(path):
            assert str(path)=='work/clean.nds'
            return image
    raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':FontROM},
        argdefs=original_raster.__defaults__)
    raster.__kwdefaults__=original_raster.__kwdefaults__
    paint_FE,FE_calibration=make_painter(image)
    parity=[];macro_calls=0
    for block in plan['blocks']:
        n=block['block'];assert n in range(111,120) and sha(container.blocks[n])==block['source_block_sha256']
        target=Path(block['research_block']).read_bytes()
        assert sha(target)==block['research_block_sha256'] and block['inverse_restoration_recovers_every_original_logical_byte']
        inputs=[(r,False) for r in block['text_records']]
        inputs.extend((r,True) for c in block['actor_style_commands'] for r in c['alternative_records'])
        for row,isvoice in inputs:
            stored=bytes.fromhex(row['target_hex']);case=fonts[row['id']]
            compiled=bytes.fromhex(case['encoded_hex'])
            if isvoice:
                assert stored==compiled[1:] and compiled[0] in [208,209,214,215,220] and row['actual_virtual_prefix_excluded_from_stored_body']
                value=compiled[:1]+stored;pad=False
            else:
                pad=row['parity_space_added']
                assert stored==compiled+(b' ' if pad else b'') and len(stored)%2==row['old_length']%2
                value=stored
            at=row['new_offset']
            assert target[at:at+len(stored)]==stored and target[at+len(stored)]==0
            isfe=value[0]==254
            assert value[0] in [2,4,9,14,19,20,104,137,163,170,179,198,207,208,209,214,215,220,254]
            pipeline=ctx.execute(expand_FE,value[1:]) if isfe else ctx.execute(expand_progressive,value[1:],value[0])
            expanded=bytes.fromhex(pipeline['cases'][0]['output_hex'])
            if isfe:
                paper=paint_FE(expanded);pixels=paper['logical'];events=paper['events']
                assert sha(pixels)==case['native_plane_sha256']
                assert sha(paper['physical'])==case['whole_physical228x64_plane_sha256']
                assert paper['complete_return_input_object_canaries_and_native_independent_plane_equal']
                assert all(0<=e['y']<=36 and e['x']<=228 for e in events if e['code']==32)
            else:
                pixels,events,fontmetrics=raster(arm,expanded)
                assert pixels==expected_pixels(arm,fontmetrics,events) and sha(pixels)==case['whole_native_plane_sha256']
                assert all(0<=e['y']<=48 and e['x']<=216 for e in events if e['code']==32)
                assert all(0<=e['x']<=210 and 0<=e['y']<=48 for e in events if e['code']!=32)
            assert len(pipeline['cases'])==4;macro_calls+=4;ctx.machines.pop()
            parity.append(dict(id=row['id'],consumer='FE-paper' if isfe else 'progressive',
                actual_virtual_actor_style_prefix_not_stored=isvoice,parity_space_added=pad,stored_target_hex=stored.hex(),
                target_hex=value.hex(),current_final_target_macro_alignment_cases=pipeline,
                complete_final_target_native_plane_equals_reviewed_plane=True,native_plane_sha256=sha(pixels),
                complete_native_glyph_events=events,tail_padding_consumed_without_blank_page_or_lost_glyph=True))
        container.blocks[n]=target
    assert len(parity)==150 and macro_calls==600 and not ctx.machines
    data=container.to_bytes()
    assert sha(data)==plan['target_SC2_sha256']==sha(Path(plan['target_SC2']).read_bytes())
    image.replace_file('/data/SC2.DK4',data);image.save(ROM);result=NdsImage.open(ROM)
    assert [p for _,p,data in parent.iter_files() if result.read_file(p)!=data]==['/data/SC2.DK4']
    for path,data in parent.iter_components():assert result.read_file(path)==data,path
    before,after=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks for im in [parent,result]]
    assert len(before)==len(after)==336
    assert [n for n,(a,b) in enumerate(zip(before,after,strict=True)) if a!=b]==list(range(111,120))
    save(ROOT/'research_image_receipt.json',dict(parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),
        research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),ARM9_sha256=sha(arm),
        SC2_sha256=sha(result.read_file('/data/SC2.DK4')),COMMON_sha256=sha(result.read_file('/COMMON/MESFILE.DK4')),
        only_changed_file='/data/SC2.DK4',only_changed_blocks=list(range(111,120)),
        block_growth_bytes={str(n):len(after[n])-len(before[n]) for n in range(111,120)},
        all327_other_SC2_blocks_every_other_file_and_native_component_exact=True,
        all150_final_targets_complete_native_planes_equal_reviewed_planes=True,
        current_final_padded_macro_alignment_cases=600,final_target_parity_cases=parity,
        padded_tail_creates_no_extra_page_or_lost_boundary_glyph=True,
        all34_actual_virtual_prefixes_excluded_from_physical_alternative_body=True,
        current_FE_typed_painter='scripts/lil_kuhn_china_FE_painter_v2909.py',
        current_FE_typed_painter_sha256=sha(Path('scripts/lil_kuhn_china_FE_painter_v2909.py').read_bytes()),
        current_FE_calibration=FE_calibration,current_macro_context_plan=str(ctx.proof_path),
        current_macro_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        registered_candidate=False,not_for_user_handoff_or_new_parent=True,
        source_relocation_plan=str(PLAN),source_relocation_plan_sha256=sha(PLAN.read_bytes()),
        native_font_proof=str(FONT),native_font_proof_sha256=sha(FONT.read_bytes()),
        all1_FE_final_plane_and4_macro_alignments_bound=True,
        all149_progressive_final_planes_and596_macro_alignments_bound=True,
        predicates_typed_dispatch_external_reference_loader_sampling_and_registered_release_pending=True,
        actual_selected_B111_B119_IDs=[],new_emulator_runs=0,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    (ROOT/'RESEARCH_ONLY.txt').write_text(
        'Unregistered V3204-derived nine-block source-reference test image. Not a release or construction parent. Preserve this ROM. All other files/components remain exact;registered integration must rebuild the entire canonical cumulative stack.\n',encoding='utf-8')
    print('Research image:nine selectedSC2blocks only;327otherblocks/allotherfiles/components exact.150final nativeplanes/600macro cases pass;not a release ornewparent.')
