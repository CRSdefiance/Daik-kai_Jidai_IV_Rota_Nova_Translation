"""Unregistered full-stack B24 test image;never a release orconstruction parent."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B24_research_v1829')
PARENT=Path('out/all_routes_combined_v1807_candidate.nds')
ROM=ROOT/'lil_B24_V1807_derived_RESEARCH_ONLY.nds'

if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    plan=read('work/analysis/lil_B24_relocation_v1828/parity_and17_native_command_research.json')
    assert sha(PARENT.read_bytes())==plan['candidate_sha256']=='4851f3c54fba3d4b745a8990002687b943b842e836044ab54285a13ec7648fdc'
    parent=NdsImage.open(PARENT);image=NdsImage.open(PARENT)
    container=IlnkContainer.parse(parent.read_file('/data/SC2.DK4'))
    block=Path('work/analysis/lil_B24_relocation_v1828/block24_RESEARCH_ONLY.bin').read_bytes()
    assert sha(block)==plan['target_block_sha256']and len(block)==992
    container.blocks[24]=block;image.replace_file('/data/SC2.DK4',container.to_bytes());image.save(ROM)
    result=NdsImage.open(ROM)
    assert[p for _,p,data in parent.iter_files()if result.read_file(p)!=data]==['/data/SC2.DK4']
    for p,data in parent.iter_components():assert result.read_file(p)==data
    old,new=(IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks for im in(parent,result))
    assert len(old)==len(new)==336 and[n for n,(a,b)in enumerate(zip(old,new,strict=True))if a!=b]==[24]
    save(ROOT/'research_image_receipt.json',{'parent':str(PARENT),'parent_sha256':sha(PARENT.read_bytes()),
        'research_ROM':str(ROM),'research_ROM_sha256':sha(ROM.read_bytes()),'ARM9_sha256':sha(result.read_file('/__arm9__.bin')),
        'SC2_sha256':sha(result.read_file('/data/SC2.DK4')),'COMMON_sha256':sha(result.read_file('/COMMON/MESFILE.DK4')),
        'only_changed_file':'/data/SC2.DK4','only_changed_block':24,'block_growth_bytes':136,
        'all335_other_SC2_blocks_every_other_file_andall_native_components_exact':True,
        'registered_candidate':False,'not_for_user_handoff_or_new_parent':True,'reference_map_andfull_actual_scene_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    (ROOT/'RESEARCH_ONLY.txt').write_text('Unregistered V1807-derived B24 test image. Only SC2B24 changes. Not a release,construction parent,oruser handoff. Reference approval andactual scene pending.\n',encoding='utf-8')
    print({'research_ROM_sha256':sha(ROM.read_bytes()),'only_changed_block':24,'growth':136,'registered':False},flush=True)
