"""Disposable full-stack research image;never a registered candidate or parent."""
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_opening_research_v1704')
PARENT=Path('out/all_routes_combined_v1676_candidate.nds')
ROM=ROOT/'lil_opening_V1676_derived_RESEARCH_ONLY.nds'


if __name__=='__main__':
    assert not ROOT.exists()
    evidence=read('work/analysis/lil_opening_relocation_v1701/parity_and_native_command_research.json')
    assert sha(PARENT.read_bytes())==evidence['ROM_sha256']=='337edf22ab6ee96536aadb15fb461652149b157e8d9bd1ef60db998f97608510'
    parent=NdsImage.open(PARENT);image=NdsImage.open(PARENT)
    container=IlnkContainer.parse(parent.read_file('/data/SC2.DK4'))
    block=Path('work/analysis/lil_opening_relocation_v1701/block22_RESEARCH_ONLY.bin').read_bytes()
    assert sha(block)==evidence['research_block_sha256'] and len(block)==3292
    container.blocks[22]=block;target=container.to_bytes()
    assert len(target)-len(parent.read_file('/data/SC2.DK4'))==292
    image.replace_file('/data/SC2.DK4',target)
    ROOT.mkdir(parents=True);image.save(ROM)
    result=NdsImage.open(ROM)
    before={p:b for _,p,b in parent.iter_files()};after={p:b for _,p,b in result.iter_files()}
    assert set(before)==set(after) and [p for p in before if before[p]!=after[p]]==['/data/SC2.DK4']
    assert dict(parent.iter_components())==dict(result.iter_components())
    old=IlnkContainer.parse(before['/data/SC2.DK4']).blocks
    new=IlnkContainer.parse(after['/data/SC2.DK4']).blocks
    assert len(old)==len(new) and [n for n,(a,b) in enumerate(zip(old,new,strict=True)) if a!=b]==[22]
    save(ROOT/'research_image_receipt.json',{'parent':str(PARENT),'parent_sha256':sha(PARENT.read_bytes()),
        'research_ROM':str(ROM),'research_ROM_sha256':sha(ROM.read_bytes()),'SC2_sha256':sha(target),
        'ARM9_sha256':sha(result.read_file('/__arm9__.bin')),'only_changed_file':'/data/SC2.DK4','only_changed_block':22,
        'whole_unchanged_SC2_blocks':len(old)-1,'all_other_files_ARM9_ARM7_routes_art_fonts_and_runtime_exact':True,
        'block_growth_bytes':292,'registered_candidate':False,'not_for_user_handoff_or_new_parent':True,
        'external_reference_map_incomplete_research_testing_only':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    (ROOT/'RESEARCH_ONLY.txt').write_text('Unregistered V1676-derived opening probe. Only SC2 B22 changes. Not a release,parent,or user handoff. External-reference mapping and full revised scene tests are unfinished.\n',encoding='utf-8')
    print({'research_ROM':str(ROM),'sha256':sha(ROM.read_bytes()),'changed_files':['/data/SC2.DK4'],'changed_blocks':[22],'registered':False})
