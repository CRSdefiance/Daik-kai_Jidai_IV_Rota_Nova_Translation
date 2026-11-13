"""Unregistered V1841-derived Stockholm test image;not a release orparent."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Stockholm_research_v1862')
PARENT=Path('out/all_routes_combined_v1841_candidate.nds')
ROM=ROOT/'lil_Stockholm_V1841_derived_RESEARCH_ONLY.nds'

if __name__=='__main__':
    assert not ROOT.exists()
    plan=read('work/analysis/lil_Stockholm_relocation_v1861/nested_source_relocation_research.json')
    assert plan['all51_texts_and24_relative_operands_preserved']and plan['all120_relocated_native_skip_cases_match_original_target_mapping']
    assert sha(PARENT.read_bytes())==plan['candidate_sha256']=='84be5d1e7382fcec09ba0846292dec418cff44533f81f843f10dd541c2cd6a28'
    spec=plan['blocks'][0];assert spec['block']==27 and len(spec['text_records'])==51 and len(spec['relative_skip_fixups'])==24
    parent=NdsImage.open(PARENT);image=NdsImage.open(PARENT);container=IlnkContainer.parse(parent.read_file('/data/SC2.DK4'))
    target=Path(spec['research_block']).read_bytes();assert sha(target)==spec['research_block_sha256']and len(target)==2972
    container.blocks[27]=target;image.replace_file('/data/SC2.DK4',container.to_bytes())
    ROOT.mkdir(parents=True);image.save(ROM);result=NdsImage.open(ROM)
    assert[p for _,p,data in parent.iter_files()if result.read_file(p)!=data]==['/data/SC2.DK4']
    for p,data in parent.iter_components():assert result.read_file(p)==data,p
    old,new=(IlnkContainer.parse(v.read_file('/data/SC2.DK4')).blocks for v in(parent,result))
    assert len(old)==len(new)==336 and[n for n,(a,b)in enumerate(zip(old,new,strict=True))if a!=b]==[27]
    save(ROOT/'research_image_receipt.json',{'parent':str(PARENT),'parent_sha256':sha(PARENT.read_bytes()),
        'research_ROM':str(ROM),'research_ROM_sha256':sha(ROM.read_bytes()),'ARM9_sha256':sha(result.read_file('/__arm9__.bin')),
        'SC2_sha256':sha(result.read_file('/data/SC2.DK4')),'COMMON_sha256':sha(result.read_file('/COMMON/MESFILE.DK4')),
        'only_changed_file':'/data/SC2.DK4','only_changed_block':27,'block_growth_bytes':280,
        'all335_other_SC2_blocks_every_other_file_and_native_component_exact':True,
        'registered_candidate':False,'not_for_user_handoff_or_new_parent':True,
        'reference_approval_and_revised_actual_scene_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    (ROOT/'RESEARCH_ONLY.txt').write_text('Unregistered V1841-derived Stockholm test image. Only SC2B27 changes. Not a release,construction parent oruser handoff. Revised gameplay andcomplete reference approval pending.\n',encoding='utf-8')
    print({'research_ROM_sha256':sha(ROM.read_bytes()),'only_changed_block':27,'growth':280,'registered':False},flush=True)
