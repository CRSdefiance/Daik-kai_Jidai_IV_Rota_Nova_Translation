"""Combine exact reviewed SC1 with three exclusive surnames and a focused header fixture."""
from copy import deepcopy
from pathlib import Path
import os
from dk4tool.patch.owned_name_fields_v2 import plan_arm9_name_fields
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/Hodram_B0_B41_clean_20261107')
OUT=ROOT/'mixed_research_v1'

def main():
    assert not OUT.exists()
    rebuilt_path=ROOT/'stored_reconstruction_v2/reconstruction.json';rebuilt=load(rebuilt_path)
    native_path=ROOT/'name_field_checks_v1/native_name_fields_verification.json';native=load(native_path)
    proposal_path=ROOT/'name_field_inputs_v1/owned_fields_proposal.json';proposal=load(proposal_path)
    assert native['proposal_sha256']==digest(proposal_path)
    image=NdsImage.open(rebuilt['research_ROM']);assert digest(rebuilt['research_ROM'])==rebuilt['research_ROM_sha256']
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');arm=image.read_file('/__arm9__.bin')
    target,proof=plan_arm9_name_fields(arm,proposal,clean)
    assert proof==native['name_data_plan'] and target==Path(native['proposed_ARM9']).read_bytes()
    assert proof['changed_bytes']==28 and proof['complete_parent_inverse_exact']
    fixture_path=ROOT/'name_header_fixtures_before_fields_v1/hodram_three_corrected_headers_fixture.json'
    fixture=load(fixture_path);source_fixture=NdsImage.open(fixture['research_ROM'])
    assert digest(fixture['research_ROM'])==fixture['research_ROM_sha256']
    assert source_fixture.read_file('/__arm9__.bin')==arm
    OUT.mkdir();outputs=[]
    for original,name in [(image,'reviewed_SC1_and_three_surnames_RESEARCH_ONLY.nds'),
                           (source_fixture,'three_corrected_headers_RESEARCH_ONLY.nds')]:
        proposed=deepcopy(original);proposed.replace_file('/__arm9__.bin',target)
        assert all(proposed.read_file(p)==data for _,p,data in original.iter_files())
        assert [p for p,data in original.iter_components() if proposed.read_file(p)!=data]==['/__arm9__.bin']
        path=OUT/name;proposed.save(path)
        reopened=NdsImage.open(path);assert reopened.read_file('/__arm9__.bin')==target
        reopened.replace_file('/__arm9__.bin',arm);assert bytes(reopened.rom.save())==bytes(original.rom.save())
        outputs.append(path)
    combined,qa=outputs
    updated=deepcopy(fixture);updated.update(research_ROM=str(qa),research_ROM_sha256=digest(qa),
        story_only_fixture=str(fixture_path),story_only_fixture_sha256=digest(fixture_path),
        qualified_name_data_proposal=str(proposal_path),qualified_name_data_proposal_sha256=digest(proposal_path),
        native_name_proof=str(native_path),native_name_proof_sha256=digest(native_path),
        only_additional_changes_three_owned_surname_spans=True,
        expected_progressive_name_data_version='proposed',
        no_savestate_battery_RAM_roster_money_RNG_eventflag_orcondition_result_override=True)
    updated['evidence'].update({str(p):digest(p) for p in [fixture_path,proposal_path,native_path,Path(__file__)]})
    save(OUT/'three_headers_fixture.json',updated)
    save(OUT/'research_reference.json',dict(research_ROM=str(combined),research_ROM_sha256=digest(combined),
        story_only_research_ROM=rebuilt['research_ROM'],story_only_research_ROM_sha256=rebuilt['research_ROM_sha256'],
        parent=rebuilt['parent'],parent_sha256=rebuilt['parent_sha256'],
        target_ARM9_sha256=sha(target),name_data_plan=proof,exact_story_only_inverse=True,
        full_registered_parent_inverse_via_original_SC1_andARM9=True,
        no_registered_release_orpromotion=True,actual_corrected_headers_pending=True,new_credit=0,
        evidence={str(p):digest(p) for p in [rebuilt_path,native_path,proposal_path,fixture_path,Path(__file__)]}))
    pins=Path('translations/rom_retention_pins.json');before=pins.read_bytes();values=load(pins)
    for path in outputs:values.append(dict(path=str(path.resolve()),reason='Preserve mixed residual research and focused surname evidence. SHA256 '+digest(path)))
    (OUT/'pins.before.json').write_bytes(before);pending=pins.with_name('rom_retention_pins.hodram_residual_mixed.pending.json')
    assert not pending.exists();save(pending,values);assert pins.read_bytes()==before;os.replace(pending,pins)
    print(dict(combined_research_SHA256=digest(combined),owned_name_bytes=proof['changed_bytes'],header_fixture_frames=fixture['frames']))

if __name__=='__main__':main()
