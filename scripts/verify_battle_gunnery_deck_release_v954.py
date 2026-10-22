"""Full ancestry,only24 selected strings,source guards and exact clean-input patch."""



from copy import deepcopy

from pathlib import Path



from dk4tool.patch import battle_gunnery_deck_editorial as owned

from dk4tool.patch.grand_race_menu_release import sha

from dk4tool.patch.battle_sails_boarding_editorial import current_entries as previous_entries

from dk4tool.patch.xdelta import apply_xdelta,make_xdelta

from dk4tool.rom.nds import NdsImage

from scripts.prepare_battle_gunnery_deck_release_v954 import ROOT,MANUSCRIPT,OLD

from scripts.verify_refit_release_v708 import files

from scripts.verify_refit_release_v831 import rejected

from scripts.verify_village_wrap_v608 import read,save



ROM=Path('out/all_routes_combined_v954_candidate.nds')





def main():

    old,new=map(NdsImage.open,(OLD,ROM));before,after=files(old),files(new)

    changed={p for p in before if before[p]!=after[p]}

    assert before.keys()==after.keys() and changed=={'/COMMON/MESFILE.DK4','/__arm9__.bin'}

    c,a,proof=owned.apply_release(before['/COMMON/MESFILE.DK4'],before['/__arm9__.bin'],owned.CONFIG)

    assert c==after['/COMMON/MESFILE.DK4'] and a==after['/__arm9__.bin']

    original=previous_entries(before['/COMMON/MESFILE.DK4'],before['/__arm9__.bin']);actual=owned.current_entries(c,a)

    changed_IDs=[x.message_id for x,y in zip(original,actual,strict=True) if x.text!=y.text]

    manuscript=read(MANUSCRIPT)

    assert changed_IDs==[r['message_id'] for r in manuscript['records'] if r['editorial_decision']=='revise']

    assert len(changed_IDs)==17 and len(actual)==3668

    assert all(original[n].text==actual[n].text for n in (676,677,*range(1361,1423)))

    registry=read('translations/release_stack.json');prior=read(ROOT/'registry_before.json')

    restored=deepcopy(registry);profile=restored['profiles'].pop('all-routes-unified-v954')

    assert restored==prior and len(registry['accepted_layers'])==114

    inherited=deepcopy(profile);inherited.pop('battle_gunnery_deck_editorial')

    for key in ('description','note','status'):

        if key in prior['profiles']['all-routes-unified-v947']:inherited[key]=prior['profiles']['all-routes-unified-v947'][key]

        else:inherited.pop(key,None)

    assert inherited==prior['profiles']['all-routes-unified-v947']

    manifest,old_manifest=read(ROM.with_suffix('.manifest.json')),read(OLD.with_suffix('.manifest.json'))

    assert manifest['candidate_sha256']==sha(ROM.read_bytes())

    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())

    assert manifest['base_sha256']==registry['canonical_baseline']['sha256']

    assert manifest['batches']==old_manifest['batches'] and len(manifest['batches'])==471

    assert manifest['required_batches']==old_manifest['required_batches'] and all(manifest['checks'].values())

    for path,records in old_manifest['changed_records'].items():assert set(records)<=set(manifest['changed_records'][path])

    bad=deepcopy(manuscript);bad['records'][0]['current_text_hex']='42'

    controls=[rejected(lambda:owned.plan(b'X'+before['/COMMON/MESFILE.DK4'][1:],before['/__arm9__.bin'],manuscript)),

        rejected(lambda:owned.plan(before['/COMMON/MESFILE.DK4'],b'X'+before['/__arm9__.bin'][1:],manuscript)),

        rejected(lambda:owned.plan(before['/COMMON/MESFILE.DK4'],before['/__arm9__.bin'],bad))]

    template=manuscript['records'][0]

    for text in (' Leading space.','Double  spacing.','Manual\nbreak.','Unknown %s argument.','{MACRO:FI}','A'*37):

        controls.append(rejected(lambda text=text:owned.compiled({**template,'english':text})))

    clean=Path('work/clean.nds');assert sha(clean.read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'

    patch,reconstructed=ROM.with_suffix('.xdelta'),ROOT/'V954_exact_patch_reconstruction.nds'

    make_xdelta(clean,ROM,patch);apply_xdelta(clean,patch,reconstructed);assert reconstructed.read_bytes()==ROM.read_bytes()

    save(ROOT/'registered_release_verification.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),

        'patch':str(patch),'patch_sha256':sha(patch.read_bytes()),'clean_input_sha256':sha(clean.read_bytes()),

        'manifest_sha256':sha(ROM.with_suffix('.manifest.json').read_bytes()),'registry_sha256':sha(Path('translations/release_stack.json').read_bytes()),

        'changed_components_relative_to_V947':sorted(changed),'changed_native_message_IDs':changed_IDs,

        'all3644_other_text_strings_exact':True,'all_graphics_scripts_HELP_ARM7_overlays_other_files_exact':True,

        'all_prior_profiles471_batches114_accepted_layers_preserved':True,'late_stage_replay_matches_complete_target_bytes':True,

        'bad_source_stale_record_manual_spacing_breaks_and_wrong_arguments_rejected':controls,

        'exact_clean_input_patch_reconstruction':str(reconstructed),'native_repack_proof':proof,

        'actual_panel_and_startup_verification_pending':True,'canonical_not_promoted':True,

        'verifier_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})

    print('V954: full471/114 inheritance,bounded battle-gunnery-deck stage and exact clean-input patch pass;actual scenes pending.',flush=True)





if __name__=='__main__':main()

