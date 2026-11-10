"""Apply the frozen28-byte name proposal after the final tutorial wrap, with exact inverses."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.owned_name_fields_v2 import plan_arm9_name_fields
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/Hodram_B0_B41_clean_20261107');OUT=ROOT/'mixed_research_v2'

def main():
    assert not OUT.exists()
    rebuilt_path=ROOT/'stored_reconstruction_v3/reconstruction.json';rebuilt=load(rebuilt_path)
    name_path=ROOT/'name_field_checks_v1/native_name_fields_verification.json';native=load(name_path)
    proposal_path=ROOT/'name_field_inputs_v1/owned_fields_proposal.json';proposal=load(proposal_path)
    parent=NdsImage.open(rebuilt['parent']);story=NdsImage.open(rebuilt['research_ROM'])
    assert digest(rebuilt['parent'])==rebuilt['parent_sha256'] and digest(rebuilt['research_ROM'])==rebuilt['research_ROM_sha256']
    old=story.read_file('/__arm9__.bin');assert old==parent.read_file('/__arm9__.bin')
    arm,proof=plan_arm9_name_fields(old,proposal,NdsImage.open('work/clean.nds').read_file('/__arm9__.bin'))
    assert proof==native['name_data_plan'] and arm==Path(native['proposed_ARM9']).read_bytes() and proof['changed_bytes']==28
    story.replace_file('/__arm9__.bin',arm)
    assert [p for _,p,data in parent.iter_files() if story.read_file(p)!=data]==['/data/SC1.DK4']
    assert [p for p,data in parent.iter_components() if story.read_file(p)!=data]==['/__arm9__.bin']
    output=bytes(story.rom.save());story.replace_file('/__arm9__.bin',old)
    assert bytes(story.rom.save())==Path(rebuilt['research_ROM']).read_bytes()
    story.replace_file('/data/SC1.DK4',parent.read_file('/data/SC1.DK4'))
    assert bytes(story.rom.save())==Path(rebuilt['parent']).read_bytes()
    OUT.mkdir();rom=OUT/'reviewed_SC1_and_three_surnames_RESEARCH_ONLY.nds';rom.write_bytes(output)
    reference=dict(research_ROM=str(rom),research_ROM_sha256=digest(rom),
        story_only_research_ROM=rebuilt['research_ROM'],story_only_research_ROM_sha256=rebuilt['research_ROM_sha256'],
        parent=rebuilt['parent'],parent_sha256=rebuilt['parent_sha256'],target_ARM9_sha256=sha(arm),name_data_plan=proof,
        exact_story_only_inverse=True,complete_registered_parent_inverse_exact=True,
        corrected_header_observation='name_headers_pixels_v1/focused_actual_pixels.json',
        header_fixture_ARM9_andselected_commands_exact_to_this_target=True,
        no_registered_release_orpromotion=True,new_credit=0,
        evidence={str(p):digest(p) for p in [rebuilt_path,name_path,proposal_path,ROOT/'name_headers_pixels_v1/focused_actual_pixels.json',Path(__file__)]})
    save(OUT/'research_reference.json',reference)
    print(dict(final_mixed_research_SHA256=digest(rom),whole_parent_inverse=True,owned_name_bytes=28))

if __name__=='__main__':main()
