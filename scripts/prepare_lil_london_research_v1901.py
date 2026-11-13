"""Unregistered V1875-derived B26 test image,never a production parent."""
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_London_research_v1901')
PARENT=Path('out/all_routes_combined_v1875_candidate.nds')
ROM=ROOT/'lil_London_V1875_derived_RESEARCH_ONLY.nds'

if __name__=='__main__':
    assert not ROOT.exists()
    path=Path('work/analysis/lil_London_relocation_v1899/nested_source_relocation_research.json')
    plan=read(path)
    assert plan['all262_nested_commands_111_complete_preambles_and_92_typed_spans_preserved']
    assert plan['all460_relocated_native_skip_cases_match_original_mapping']
    assert read('work/analysis/lil_London_FE_parity_v1900/all3_final_FE_parity_native_planes.json')['all3_complete_padded_targets_one_native_page_and_pixel_exact']
    assert sha(PARENT.read_bytes())==plan['candidate_sha256']=='872f4047dd3c9ee335dc7e6dbff5e96af668c67b07e145f29422db71c0871d97'
    parent,image=NdsImage.open(PARENT),NdsImage.open(PARENT)
    container=IlnkContainer.parse(parent.read_file('/data/SC2.DK4'))
    target=Path(plan['research_block']).read_bytes()
    assert sha(target)==plan['research_block_sha256'] and len(target)==7120
    container.blocks[26]=target
    image.replace_file('/data/SC2.DK4',container.to_bytes())
    ROOT.mkdir(parents=True)
    image.save(ROM)
    result=NdsImage.open(ROM)
    assert [p for _,p,data in parent.iter_files() if result.read_file(p)!=data]==['/data/SC2.DK4']
    for p,data in parent.iter_components():assert result.read_file(p)==data,p
    before,after=(IlnkContainer.parse(v.read_file('/data/SC2.DK4')).blocks for v in (parent,result))
    assert len(before)==len(after)==336
    assert [n for n,(a,b) in enumerate(zip(before,after,strict=True)) if a!=b]==[26]
    save(ROOT/'research_image_receipt.json',dict(parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),
        research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),ARM9_sha256=sha(result.read_file('/__arm9__.bin')),
        SC2_sha256=sha(result.read_file('/data/SC2.DK4')),COMMON_sha256=sha(result.read_file('/COMMON/MESFILE.DK4')),
        only_changed_file='/data/SC2.DK4',only_changed_block=26,block_growth_bytes=864,
        all335_other_SC2_blocks_every_other_file_and_native_component_exact=True,
        registered_candidate=False,not_for_user_handoff_or_new_parent=True,
        reference_approval_and_revised_actual_scene_pending=True,
        source_relocation_plan=str(path),source_relocation_plan_sha256=sha(path.read_bytes()),
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    (ROOT/'RESEARCH_ONLY.txt').write_text('Unregistered V1875-derived London test image. Only SC2B26 changes. Not a release orconstruction parent. Revised gameplay andcomplete reference approval pending.\n',encoding='utf-8')
    print(dict(research_ROM_sha256=sha(ROM.read_bytes()),only_changed_block=26,growth=864,registered=False))
