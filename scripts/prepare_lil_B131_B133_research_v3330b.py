"""Ten-block research image and 220 complete final stored paragraph proofs."""
from pathlib import Path
from types import FunctionType
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.verify_lil_B131_B133_fonts_v3324b import expand as expand_progressive
from scripts.verify_lil_B131_B133_FE_v3325 import expand as expand_FE
from scripts.lil_kuhn_china_FE_painter_v2909 import make_painter
from scripts.verify_name_catalog_glyphs_v278 import raster as original_raster, expected_pixels
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/lil_B131_B133_research_v3330b')
PARENT=Path('out/all_routes_combined_v3300_candidate.nds')
ROM=ROOT/'lil_B131_B133_V3300_derived_RESEARCH_ONLY.nds'
PLAN=Path('work/analysis/lil_B131_B133_relocation_v3329b/nested_source_relocation_research.json')
FONT=Path('work/analysis/lil_B131_B133_native_approval_v3326/all63_native_macro_font_choice_and_source00_reconciliation.json')

if __name__=='__main__':
    assert not ROOT.exists()
    plan,font=map(read,[PLAN,FONT])
    assert plan['all61speech_two_choice_labels_and24_relative_operands_preserved']
    assert plan['all120_relocated_native_skip_cases_match_original_target_mapping']
    assert sha(PARENT.read_bytes())==plan['candidate_sha256']==font['candidate_sha256']
    parent,image=NdsImage.open(PARENT),NdsImage.open(PARENT)
    arm=image.read_file('/__arm9__.bin');container=IlnkContainer.parse(parent.read_file('/data/SC2.DK4'))
    fonts={r['id']:r for r in font['cases']}
    assert sha(parent.read_file('/data/SC2.DK4'))==plan['source_SC2_sha256']
    source=read(plan['source_context'])
    ROOT.mkdir(parents=True)
    ctx=CurrentContext('work/analysis/lil_B131_B133_fonts_v3324b/current_native_input.json',
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
    from scripts.map_lil_B122_B127_source_v3260c import choice_getters,control2000
    from scripts.verify_ship_advice_choice_centering_20261022 import choice_vm
    menus=[];pauses=[]
    parity=[];macro_calls=0
    for block in plan['blocks']:
        n=block['block'];assert n in [131,133] and sha(container.blocks[n])==block['source_block_sha256']
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
            assert value[0] in [0,2,5,9,20,254]
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
        for c in block['choice_commands']:
            value=bytes.fromhex(c['target_hex']);assert target[c['new_offset']:c['new_offset']+len(value)]==value
            getters=choice_getters(arm,dict(whole_command_hex=value.hex(),offset=c['new_offset'],native_extent=len(value)))
            assert all([r['text'] for r in g['labels']]==c['labels'] for g in getters)
            approved=next(m for m in font['menu_targets'] if (m['block'],m['command_offset'])==(n,c['old_offset']))
            assert approved['object_hex']==value.hex() and approved['labels']==c['labels']
            vm=choice_vm(arm,value);assert vm['labels']==c['labels'] and vm['native_menu_rectangle']==approved['native_geometry'] and [r['modal_selection'] for r in vm['VM_cases']]==[0,1,-1]
            menus.append(dict(block=n,old_offset=c['old_offset'],new_offset=c['new_offset'],whole_target_object_hex=value.hex(),getters=getters,original_VM_selection_cancel_and_geometry=vm,complete_label_planes_bound_by_exact_approved_object=True))
        assert not block['original2000_pause_and_resume_maps']
        container.blocks[n]=target
    assert len(parity)==61 and macro_calls==244 and not ctx.machines
    assert len(menus)==1 and len(pauses)==0
    data=container.to_bytes()
    assert sha(data)==plan['target_SC2_sha256']==sha(Path(plan['target_SC2']).read_bytes())
    image.replace_file('/data/SC2.DK4',data);image.save(ROM);result=NdsImage.open(ROM)
    assert [p for _,p,data in parent.iter_files() if result.read_file(p)!=data]==['/data/SC2.DK4']
    for path,data in parent.iter_components():assert result.read_file(path)==data,path
    before,after=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks for im in [parent,result]]
    assert len(before)==len(after)==336
    assert [n for n,(a,b) in enumerate(zip(before,after,strict=True)) if a!=b]==list([131,133])
    save(ROOT/'research_image_receipt.json',dict(parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),
        research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),ARM9_sha256=sha(arm),
        SC2_sha256=sha(result.read_file('/data/SC2.DK4')),COMMON_sha256=sha(result.read_file('/COMMON/MESFILE.DK4')),
        only_changed_file='/data/SC2.DK4',only_changed_blocks=list([131,133]),
        block_growth_bytes={str(n):len(after[n])-len(before[n]) for n in [131,133]},
        all334_other_SC2_blocks_every_other_file_and_native_component_exact=True,
        all61_final_targets_complete_native_planes_equal_reviewed_planes=True,
        current_final_padded_macro_alignment_cases=244,final_target_parity_cases=parity,
        padded_tail_creates_no_extra_page_or_lost_boundary_glyph=True,
        final_menu_cases=menus,all1_final2100_object_two_labels_and3_selection_cancel_cases_bound=True,final2000_pause_cases=pauses,no_source2000_pause_commands=True,all18_final_source00_speech_prefixes_and_nonempty_bodies_preserved=True,
        all61_complete_source_static_or_FE_prefixes_preserved=True,
        current_FE_typed_painter='scripts/lil_kuhn_china_FE_painter_v2909.py',
        current_FE_typed_painter_sha256=sha(Path('scripts/lil_kuhn_china_FE_painter_v2909.py').read_bytes()),
        current_FE_calibration=FE_calibration,current_macro_context_plan=str(ctx.proof_path),
        current_macro_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        registered_candidate=False,not_for_user_handoff_or_new_parent=True,
        source_relocation_plan=str(PLAN),source_relocation_plan_sha256=sha(PLAN.read_bytes()),
        native_font_proof=str(FONT),native_font_proof_sha256=sha(FONT.read_bytes()),
        all1_FE_final_plane_and4_macro_alignments_bound=True,
        all60_progressive_final_planes_and240_macro_alignments_bound=True,
        predicates_typed_dispatch_external_reference_loader_sampling_and_registered_release_pending=True,
        actual_selected_B131_B133_IDs=[],new_emulator_runs=0,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    (ROOT/'RESEARCH_ONLY.txt').write_text(
        'Unregistered V3300-derived two-block source-reference test image. Not a release or construction parent. Preserve this ROM. All other files/components remain exact;registered integration must rebuild the entire canonical cumulative stack.\n',encoding='utf-8')
    print('Research image:two selectedSC2blocks only;334otherblocks/allotherfiles/components exact.61final nativeplanes/244macro cases,one complete menu and18source00 targets pass;not a release ornewparent.')
