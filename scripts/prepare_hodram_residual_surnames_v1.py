"""Qualify three source-reviewed surname spans after the exact final SC1 transaction."""
from pathlib import Path
from dk4tool.patch.registered_owned_name_fields_v2 import plan_release
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.prepare_hodram_residual_registered_v2 import ROOT,OUT,CLEAN

CONFIG=Path('translations/hodram_residual_surnames_release_v1.json')
QUALIFICATION=OUT/'surname_fields_qualification.json'

def main():
    assert not CONFIG.exists() and not QUALIFICATION.exists()
    refpath=ROOT/'mixed_research_v2/research_reference.json';ref=load(refpath)
    native=ROOT/'research_final_v1/owned_surnames_native_approved.json'
    proposal=ROOT/'name_field_inputs_v1/owned_fields_proposal.json'
    manuscript=Path('translations/hodram_B0_B41_owned_surnames_final_v1.json')
    actual=ROOT/'gameplay_review_v1.json'
    paths=[refpath,native,proposal,manuscript,actual,Path(__file__),
        Path('dk4tool/patch/registered_owned_name_fields_v2.py'),Path('dk4tool/patch/owned_name_fields_v2.py')]
    assert digest(ref['story_only_research_ROM'])==ref['story_only_research_ROM_sha256']
    assert digest(ref['research_ROM'])==ref['research_ROM_sha256']
    conf=dict(format='dk4-registered-owned-name-fields-v2',clean_ROM=str(CLEAN),clean_ROM_sha256=digest(CLEAN),
        parent_ROM_sha256=ref['story_only_research_ROM_sha256'],target_ROM_sha256=ref['research_ROM_sha256'],
        target_ARM9_sha256=load(native)['name_data_plan']['target_ARM9_sha256'],
        manuscript=str(manuscript),proposal=str(proposal),native=str(native),actual=str(actual),
        actual_policy=[dict(actor=actor,kind='changed-progressive-name',full_name=name,
            complete_header_key='complete_name_glyphs_andblank_guards_exact',minimum_headers=1)
            for actor,name in [(55,'David Flahven'),(56,'Georg Salzgitter'),(57,'Nagayoshi Kamuro')]],
        dependencies={str(p):digest(p) for p in paths},new_credit=0)
    draft=OUT/'surname_fields_candidate_config.json';save(draft,conf)
    image=NdsImage.open(ref['story_only_research_ROM']);old=image.read_file('/__arm9__.bin')
    arm,proof=plan_release(image,draft)
    assert proof['changed_bytes']==28 and proof['complete_parent_inverse_exact']
    image.replace_file('/__arm9__.bin',arm);assert bytes(image.rom.save())==Path(ref['research_ROM']).read_bytes()
    image.replace_file('/__arm9__.bin',old);assert bytes(image.rom.save())==Path(ref['story_only_research_ROM']).read_bytes()
    save(CONFIG,conf)
    save(QUALIFICATION,dict(config=str(CONFIG),config_sha256=digest(CONFIG),story_only_ROM_sha256=conf['parent_ROM_sha256'],
        target_ROM_sha256=conf['target_ROM_sha256'],target_ARM9_sha256=conf['target_ARM9_sha256'],proof=proof,
        exact_combined_research_target_and_story_only_inverse=True,new_credit=0))
    print('Qualified three complete observed surnames:28 owned bytes; exact mixed target andwhole story-only inverse.')

if __name__=='__main__':main()
