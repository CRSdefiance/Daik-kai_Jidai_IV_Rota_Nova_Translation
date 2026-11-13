"""Preserve rejectedV3409 andregister aseparate hook for the validated compiler."""
import os
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.patch import lil_B137_editorial_v2 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B137_registration_v3415')
OLDREG=Path('work/analysis/lil_B137_registration_v3408b')
PROFILE='all-routes-unified-v3416'
if __name__=='__main__':
    assert not ROOT.exists();rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py');raw,code=rp.read_bytes(),builder.read_bytes();registry=read(rp);conf=read(owned.CONFIG);oldreceipt=read(OLDREG/'registration_receipt.json');failed=read('work/analysis/lil_B137_build_v3409/build_terminal.json')
    assert failed['terminal'] and failed['returncode']==1 and not failed['candidate_exists'] and not Path(failed['candidate']).exists() and PROFILE not in registry['profiles']
    assert sha(rp.read_bytes())==oldreceipt['release_stack_sha256'] and sha(code)==oldreceipt['builder_sha256'] and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492' and len(registry['accepted_layers'])==114
    assert sha(Path(owned.__file__).read_bytes())==conf['dependencies'][str(Path(owned.__file__))] and sha(Path(owned.CONFIG).read_bytes())==oldreceipt['config_sha256']
    assert conf==read(OLDREG/'positive_config.json') and len(read(OLDREG/'negative_cases.json')['cases'])==28 and read(OLDREG/'negative_cases.json')['all_rejected_before_mutation']
    image=NdsImage.open('out/all_routes_combined_v3372_candidate.nds');proof=owned.apply_release(image,NdsImage.open('out/raphael_natural_v2_accepted_base.nds'));assert len(proof['changed_records'])==48 and image.read_file('/data/SC2.DK4')==Path('work/analysis/lil_B137_relocation_v3401b/SC2_RESEARCH_ONLY.DK4').read_bytes()
    oldstage=(OLDREG/'builder_added_optional_stage.bin').read_bytes();assert code.count(oldstage)==1 and b'from dk4tool.patch.lil_B137_editorial_v1 import' in oldstage
    stage=oldstage.replace(b"profile_config.get('lil_B137_editorial')",b"profile_config.get('lil_B137_editorial_v2')").replace(b'from dk4tool.patch.lil_B137_editorial_v1 import',b'from dk4tool.patch.lil_B137_editorial_v2 import').replace(b"['lil_B137_editorial']",b"['lil_B137_editorial_v2']")
    assert stage!=oldstage and b"profile_config.get('lil_B137_editorial_v2')" not in code
    anchor=b'    # Lexically valid "% o"';assert code.count(anchor)==1;after=code.replace(anchor,stage+anchor);compile(after,str(builder),'exec')
    profile=deepcopy(registry['profiles']['all-routes-unified-v3372']);assert 'lil_B137_editorial' not in profile
    profile.update(lil_B137_editorial_v2=owned.CONFIG,description='Complete V3372 cumulative stack plus48 B137 contextual reviews through the validated v2 compiler.',note='V3409 build rejected before candidate creation because its hook importedv1;the failed profile/stage/proofs remain preserved. This separate optionalv2 hook matches the positively reconstructed compiler and28negative tests.48speech/22revisions/26retentions;117commands/48spans/240skips/12predicates,48nativeplanes/384logical-compiled/192finalmacrocases,sixviewed/hash-exact sheets. Registeredbuild/exactcleanpatch/freshstartup pending. Experimental;no promotion;preserveeveryROM/translation.')
    ROOT.mkdir(parents=True);(ROOT/'registry_before_raw.json').write_bytes(raw);(ROOT/'builder_before.py').write_bytes(code);(ROOT/'builder_added_optional_stage.bin').write_bytes(stage);save(ROOT/'positive_reconstruction.json',proof);copy2(OLDREG/'negative_cases.json',ROOT/'negative_cases.json')
    registry['profiles'][PROFILE]=profile;pending=rp.with_name('release_stack_v3415_pending.json');assert not pending.exists();save(pending,registry);assert rp.read_bytes()==raw and builder.read_bytes()==code;builder.write_bytes(after);os.replace(pending,rp)
    restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE);assert restored==read(ROOT/'registry_before_raw.json') and builder.read_bytes().replace(stage,b'',1)==code and builder.read_bytes().count(oldstage)==1
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v3372',stage_key='lil_B137_editorial_v2',config=owned.CONFIG,config_sha256=sha(Path(owned.CONFIG).read_bytes()),compiler=str(Path(owned.__file__)),compiler_sha256=sha(Path(owned.__file__).read_bytes()),negative_cases=28,negative_tests_reused_by_exact_validated_compiler_and_config_hash=True,reused_negative_proof=str(OLDREG/'negative_cases.json'),reused_negative_proof_sha256=sha((OLDREG/'negative_cases.json').read_bytes()),positive_reconstruction=str(ROOT/'positive_reconstruction.json'),failed_profile='all-routes-unified-v3409',failed_build='work/analysis/lil_B137_build_v3409/build_terminal.json',failed_profile_and_old_hook_preserved_exactly=True,all114accepted_layers_previous_profiles_and_V1492_promotion_unchanged=True,only_one_optional_stage_and_one_experimental_profile_added=True,release_stack_sha256=sha(rp.read_bytes()),builder_sha256=sha(builder.read_bytes()),no_ROM_created_or_promoted=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('RegisteredV3416 through separatev2 hook;rejectedV3409/profile/stage preserved. Positive48-source reconstruction passes;28negatives reused byexact compiler/config hash. No ROMcreated.')
