"""Verify registered exact-slot COMMON changes,native copies andclean-input patch."""
from copy import deepcopy
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.patch import reinforcement_faction_prose as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import make_xdelta,apply_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.probe_common_single_cache_v862 import Loader
from scripts.reinforcement_sniping_layout_v1024 import compiled
from scripts.probe_reinforcement_sniping_layout_v1030 import native_layout,TABLES
from scripts.verify_arrival_native_v792 import prepared
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/reinforcement_faction_release_v1805')
ROM=Path('out/all_routes_combined_v1807_candidate.nds')
OLD=Path('out/all_routes_combined_v1775_candidate.nds')

if __name__=='__main__':
    output=ROOT/'registered_release_verification.json';assert not output.exists()
    manifest,prior=(read(p.with_suffix('.manifest.json'))for p in(ROM,OLD));digest=sha(ROM.read_bytes())
    assert manifest['profile']=='all-routes-unified-v1807'and manifest['candidate_sha256']==digest
    assert manifest['base_sha256']=='3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    registry=read('translations/release_stack.json');assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    restored=deepcopy(registry);profile=restored['profiles'].pop(manifest['profile']);assert restored==read(ROOT/'registry_before_raw.json')
    assert profile['reinforcement_faction_prose']==owned.CONFIG
    old_profile=deepcopy(registry['profiles']['all-routes-unified-v1775']);new_profile=deepcopy(profile)
    for p in(old_profile,new_profile):p.pop('description',None);p.pop('note',None)
    new_profile.pop('reinforcement_faction_prose');assert new_profile==old_profile
    config=read(owned.CONFIG);normal=lambda s:str(s).replace('\\','/')
    assert [normal(s)for s in manifest['batches']]==[normal(s)for s in prior['batches']]+[normal(config['manuscript'])]
    assert len(manifest['batches'])==477 and len(registry['accepted_layers'])==114 and all(manifest['checks'].values())
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    old,new=map(NdsImage.open,(OLD,ROM));arm=new.read_file('/__arm9__.bin');common=new.read_file(owned.PATH)
    assert[p for _,p,data in old.iter_files()if new.read_file(p)!=data]==[owned.PATH]
    for p,data in old.iter_components():assert new.read_file(p)==data,p
    assert len(MainCodeFile(arm,0x02000000).sections[3].data)-48==123040
    baseline=NdsImage.open(manifest['base_rom']);stage=owned.apply_release(old,baseline)
    assert old.read_file(owned.PATH)==common
    final_stage=manifest['relocations'][owned.PATH]['reinforcement_faction_prose']
    assert final_stage['proof']==stage and final_stage['release_config_sha256']==sha(Path(owned.CONFIG).read_bytes())
    rows=owned.entries(common,arm,config['directory_sha256']);doc=read(config['manuscript'])
    assert all(rows[r['message_id']].text==compiled(r)for r in doc['records'])
    loader=Loader(arm,common);selected=[0,602,676,677,*range(1910,1932),3667];copies=[]
    for mode in('warm','cold'):
        for n in selected:copies.append({**loader.copy(n,rows[n].text,mode),'mode':mode})
    loader.reset();sequence=[]
    for n in(0,1911,1912,602,1916,1911,1930,676,677,1911,3667,1916):
        sequence.append(loader.copy(n,rows[n].text,'sequence'))
    proof=read('work/analysis/reinforcement_faction_prose_v1802/six_paragraphs120_complete_native_cases.json')
    cpu=prepared(arm);native=[]
    for case in proof['all120_cases']:
        n=case['message_ID'];value,lines=native_layout(cpu,rows[n].text,n,bytes.fromhex(case['argument_case']['hex']),TABLES['reinforcement'])
        assert value.hex()==case['formatted_hex']and lines==case['lines']
        native.append({'message_ID':n,'faction_hex':case['argument_case']['hex'],'exact_new_paragraph_current_native_layout':True})
    clean=Path('work/clean.nds');clean_sha=sha(clean.read_bytes());patch=ROM.with_suffix('.xdelta');result=ROOT/'patch_reconstruction_RESEARCH_ONLY.nds'
    assert not patch.exists()and not result.exists()
    make_xdelta(clean,ROM,patch);apply_xdelta(clean,patch,result)
    assert result.read_bytes()==ROM.read_bytes()and sha(clean.read_bytes())==clean_sha
    builder=Path('scripts/build_integrated_release.py').read_bytes();addition=(ROOT/'builder_added_optional_stage.bin').read_bytes()
    assert builder.count(addition)==1 and builder.replace(addition,b'',1)==(ROOT/'builder_before.py').read_bytes()
    save(output,{'candidate':str(ROM),'candidate_sha256':digest,'profile':manifest['profile'],
        'manifest':str(ROM.with_suffix('.manifest.json')),'manifest_sha256':sha(ROM.with_suffix('.manifest.json').read_bytes()),
        'canonical_base':manifest['base_rom'],'canonical_base_sha256':manifest['base_sha256'],
        'all477_batches114_accepted_layers_and_previous_profiles_preserved':True,'only_COMMON1911_through1916_changed_from_V1775':True,
        'all3668_native_offsets_copy_spans_and41_block_lengths_exact':True,'all3662_other_strings_and_unowned_native_bytes_exact':True,
        'every_other_ROM_file_component_ARM9_font_graphic_story_and123040_staged_bytes_exact':True,
        'stage':stage,'native_complete_copy_cases':copies,'native_cache_sequence_cases':sequence,
        'actual_native_cold_warm_complete_copy_NUL_guard_and_ABI_checks_pass':True,
        'native_file_open_read_are_host_contracts_not_actual_gameplay_IO':True,'all120_new_current_native_layout_cases':native,
        'COMMON_sha256':sha(common),'ARM9_sha256':sha(arm),'SC2_sha256':sha(new.read_file('/data/SC2.DK4')),
        'patch':str(patch),'patch_sha256':sha(patch.read_bytes()),'clean_input_sha256':clean_sha,
        'exact_patch_reconstruction':str(result),'whole_reconstruction_byte_exact':True,
        'startup_and_new_six_paragraph_gameplay_samples_still_pending':True,'no_completed_editorial_credit':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print({'registered_ROM_SHA256':digest,'patch_SHA256':sha(patch.read_bytes()),'native_copy_cases':len(copies),
        'cache_sequence_cases':len(sequence),'new_layout_cases':len(native),'full_goal_complete':False},flush=True)
