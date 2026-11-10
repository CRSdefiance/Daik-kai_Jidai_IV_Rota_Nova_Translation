"""Compose a reviewed story research image and independently checked fixed-slot names."""
import argparse
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.owned_name_fields_v2 import plan_arm9_name_fields
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for arg in ['reconstruction','names','out']:parser.add_argument('--'+arg,type=Path,required=True)
    args=parser.parse_args();assert not args.out.exists()
    rebuilt,name=map(load,[args.reconstruction,args.names]);assert name['offline_visual_approved'] and not name['direct_view_pending']
    path=Path(rebuilt['research_ROM']);assert sha(path.read_bytes())==rebuilt['research_ROM_sha256']
    image=NdsImage.open(path);old=image.read_file('/__arm9__.bin')
    proposal_path=Path(name['proposal']);assert sha(proposal_path.read_bytes())==name['proposal_sha256']
    target,proof=plan_arm9_name_fields(old,load(proposal_path),NdsImage.open('work/clean.nds').read_file('/__arm9__.bin'))
    assert proof==name['name_data_plan'] and target==Path(name['proposed_ARM9']).read_bytes()
    revised=deepcopy(image);revised.replace_file('/__arm9__.bin',target)
    assert all(revised.read_file(p)==v for _,p,v in image.iter_files())
    assert [p for p,v in image.iter_components() if revised.read_file(p)!=v]==['/__arm9__.bin']
    restored=deepcopy(revised);restored.replace_file('/__arm9__.bin',old)
    assert bytes(restored.rom.save())==bytes(image.rom.save())
    args.out.mkdir(parents=True);out=args.out/'story_andnames_RESEARCH_ONLY.nds';out.write_bytes(bytes(revised.rom.save()))
    reference={**rebuilt,'story_reconstruction':str(args.reconstruction),'story_reconstruction_sha256':sha(args.reconstruction.read_bytes()),
        'research_ROM':str(out),'research_ROM_sha256':sha(out.read_bytes()),
        'story_only_research_ROM':str(path),'story_only_research_ROM_sha256':sha(path.read_bytes()),
        'name_native_proof':str(args.names),'name_native_proof_sha256':sha(args.names.read_bytes()),'owned_name_metadata_plan':proof,
        'all_other_files_components_exact':False,'only_source_qualified_owned_name_fields_additionally_changed':True,
        'whole_story_only_parent_inverse_exact':True,'not_a_registered_release_orhandoff':True,'new_credit':0}
    save(args.out/'research_reference.json',reference)
    print(dict(research_ROM=str(out),sha256=sha(out.read_bytes()),ARM9_sha256=sha(target),registered=False,new_credit=0))

if __name__=='__main__':main()
