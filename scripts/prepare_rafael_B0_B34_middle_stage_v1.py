"""Freeze the separately reviewed exclusive middle fields for cumulative release."""
from pathlib import Path
from dk4tool.patch.rafael_middle_fields_release_v1 import plan_release
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.plan_rafael_B0_B34_v1 import ROOT
from scripts.prepare_rafael_B0_B34_registered_v1 import CLEAN

CONFIG=Path('translations/rafael_B0_B34_middle_fields_release_v1.json')
QUALIFICATION=ROOT/'registered_preparation_v1/middle_fields_qualification.json'

def main():
    assert not CONFIG.exists() and not QUALIFICATION.exists()
    ref=load(ROOT/'rebuilt_with_names_v1/research_reference.json')
    native=ROOT/'owned_middle_fields_visual_v1.json'
    proposal=ROOT/'owned_middle_fields_v1/proposal.json'
    manuscript=Path('translations/rafael_B0_B34_owned_middle_fields_final_v1.json')
    actual=ROOT/'research_final_v1/actual_review.json'
    paths=[native,proposal,manuscript,actual,Path(__file__),
        Path('dk4tool/patch/rafael_middle_fields_release_v1.py'),
        Path('dk4tool/patch/registered_owned_name_fields_v2.py'),
        Path('dk4tool/patch/owned_name_fields_v2.py')]
    assert digest(ref['story_only_research_ROM'])==ref['story_only_research_ROM_sha256']
    assert digest(ref['research_ROM'])==ref['research_ROM_sha256']
    config=dict(format='dk4-registered-owned-name-fields-v2',clean_ROM=str(CLEAN),
        clean_ROM_sha256=digest(CLEAN),parent_ROM_sha256=ref['story_only_research_ROM_sha256'],
        target_ROM_sha256=ref['research_ROM_sha256'],
        target_ARM9_sha256=load(native)['name_data_plan']['target_ARM9_sha256'],
        manuscript=str(manuscript),proposal=str(proposal),native=str(native),actual=str(actual),
        actual_policy=[dict(actor=actor,kind='unchanged-progressive-middle-component',full_name=name)
            for actor,name in [(30,'Dinis de Albuquerque'),(40,'Antony von Kuhn'),(59,'Garcia de Oviedo')]],
        dependencies={str(p):digest(p) for p in paths},new_credit=0)
    draft=QUALIFICATION.with_name('middle_fields_candidate_config.json')
    save(draft,config)
    image=NdsImage.open(ref['story_only_research_ROM'])
    old=image.read_file('/__arm9__.bin')
    arm,proof=plan_release(image,draft)
    assert proof['changed_bytes']==9 and proof['complete_parent_inverse_exact']
    image.replace_file('/__arm9__.bin',arm)
    assert bytes(image.rom.save())==Path(ref['research_ROM']).read_bytes()
    image.replace_file('/__arm9__.bin',old)
    assert bytes(image.rom.save())==Path(ref['story_only_research_ROM']).read_bytes()
    save(CONFIG,config)
    save(QUALIFICATION,dict(config=str(CONFIG),config_sha256=digest(CONFIG),
        story_only_ROM_sha256=config['parent_ROM_sha256'],target_ROM_sha256=config['target_ROM_sha256'],
        target_ARM9_sha256=config['target_ARM9_sha256'],proof=proof,
        exact_combined_research_target_and_story_only_inverse=True,new_credit=0))
    print('Qualified three full-name fields: nine owned bytes; exact combined target and inverse.')

if __name__=='__main__':main()
