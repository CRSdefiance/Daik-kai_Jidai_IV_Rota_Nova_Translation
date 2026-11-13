"""Research-only story plus owned name metadata; registered release still required."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.owned_name_glyph_v1 import plan_arm9_name_glyph
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Hodram_B81_B89_name_research_20261101')
REBUILT=Path('work/analysis/Hodram_B81_B89_rebuild_20261101/reconstruction.json')
NAME=Path('work/analysis/Emilio_name_glyph_native_20261101/native_name_glyph_verification_reviewed.json')
if __name__=='__main__':
    assert not ROOT.exists();rebuilt,name=map(load,[REBUILT,NAME]);assert name['offline_visual_approved']
    path=Path(rebuilt['research_ROM']);assert sha(path.read_bytes())==rebuilt['research_ROM_sha256']
    image=NdsImage.open(path);old=image.read_file('/__arm9__.bin')
    target,proof=plan_arm9_name_glyph(old,load(name['proposal']))
    assert sha(target)==name['name_data_plan']['target_ARM9_sha256']
    revised=deepcopy(image);revised.replace_file('/__arm9__.bin',target)
    assert all(revised.read_file(p)==v for _,p,v in image.iter_files())
    assert [p for p,v in image.iter_components() if revised.read_file(p)!=v]==['/__arm9__.bin']
    restored=deepcopy(revised);restored.replace_file('/__arm9__.bin',old)
    assert bytes(restored.rom.save())==bytes(image.rom.save())
    ROOT.mkdir(parents=True);out=ROOT/'story_andname_RESEARCH_ONLY.nds';out.write_bytes(bytes(revised.rom.save()))
    reference={**rebuilt,'story_reconstruction':str(REBUILT),'story_reconstruction_sha256':sha(REBUILT.read_bytes()),
        'research_ROM':str(out),'research_ROM_sha256':sha(out.read_bytes()),
        'story_only_research_ROM':str(path),'story_only_research_ROM_sha256':sha(path.read_bytes()),
        'name_native_proof':str(NAME),'name_native_proof_sha256':sha(NAME.read_bytes()),'owned_name_metadata_plan':proof,
        'all_other_files_components_exact':False,'only_source_qualified_owned_name_slot_additionally_changed':True,
        'whole_story_only_parent_inverse_exact':True,'not_a_registered_release_orhandoff':True,'new_credit':0}
    save(ROOT/'research_reference.json',reference)
    print(dict(research_ROM=str(out),sha256=sha(out.read_bytes()),ARM9_sha256=sha(target),registered=False,new_credit=0))
