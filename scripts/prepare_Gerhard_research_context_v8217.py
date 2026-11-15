"""Prepare own research-ROM startup and strict target context; never borrow the parent snapshot."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Gerhard_research_context_tools_v8217')
REFERENCE=Path('work/analysis/Gerhard_reference_v8215/research_image_receipt.json')
if __name__=='__main__':
    assert not ROOT.exists();reference=read(REFERENCE)
    capture=derive('scripts/capture_Lil_Gerhard_current_v8197.py','scripts/capture_Gerhard_research_v8217.py',{
        'Lil_Gerhard_context_runs_v8197':'Gerhard_research_context_runs_v8217',
        "verified=Path('work/analysis/Rafael_B50_release_v8173/registered_release_verification.json');v=read(verified);rom=Path(v['candidate']);manifest=read(rom.with_suffix('.manifest.json'))\n    assert manifest['profile']=='all-routes-unified-v8172' and sha(rom.read_bytes())==manifest['candidate_sha256']==v['candidate_sha256']":
        "reference=Path('work/analysis/Gerhard_reference_v8215/research_image_receipt.json');ref=read(reference);rom=Path(ref['research_ROM']);v=dict(candidate_sha256=ref['research_ROM_sha256']);manifest=dict(profile='Gerhard-Adernkatz-RESEARCH-ONLY')\n    assert not ref['registered_candidate'] and sha(rom.read_bytes())==v['candidate_sha256']",
        'Lil_Gerhard_route{route}_v8197_V8172':'Gerhard_research_route{route}_v8217_reference8215',
        'current_registered_ROM_only_no_ROM_or_RAM_or_savestate_fixture=True':'exact_research_ROM_only_no_RAM_or_savestate_fixture=True,registered_candidate=False,research_reference=str(reference),research_reference_sha256=sha(reference.read_bytes())',
        'Capture own-current Lil New Game through original ordinary inputs;not optional Stockholm/Hamburg activation.':'Capture own unregistered research-ROM Lil NewGame with original ordinary inputs;no optional event activation.',
        "scope['route_identity']+' own-current NewGame capture terminal;actual captain/payload/EV/native binding pending.'":"scope['route_identity']+' own research-ROM NewGame terminal;actual captain/payload/native binding pending;not registered oroptional scene.'",
    })
    context=derive('scripts/Lil_current_route_context_v8198.py','scripts/Gerhard_research_route_context_v8218.py',{
        '2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a':reference['research_ARM9_sha256'],
        'sections=MainCodeFile(self.arm,BASE).sections;payload=bytes(sections[3].data[:-48])':
        """reference=read('work/analysis/Gerhard_reference_v8215/research_image_receipt.json')
        assert not reference['registered_candidate'] and self.doc['current_ROM']==reference['research_ROM'] and self.doc['current_ROM_sha256']==reference['research_ROM_sha256']
        parent=Path(reference['parent']);assert sha(parent.read_bytes())==reference['parent_sha256']
        oldarm=NdsImage.open(parent).read_file('/__arm9__.bin');slot=reference['only_changed_name_span'];at=slot['offset']
        assert slot['bytes']==12 and len(self.arm)==len(oldarm) and self.arm[at:at+12].hex()==slot['target_hex']
        restored=bytearray(self.arm);restored[at:at+12]=bytes.fromhex(slot['current_hex']);assert bytes(restored)==oldarm
        assert self.arm[at+12:at+20]==oldarm[at+12:at+20]==b'Blades\\0\\0'
        sections=MainCodeFile(self.arm,BASE).sections;payload=bytes(sections[3].data[:-48])""",
        'original_current123264_deployed_payload_exact=True,patches=[],no_initialized_RAM_overlay=True,':
        'original_current123264_deployed_payload_exact=True,patches=[],no_initialized_RAM_overlay=True,\n            research_reference=reference,exact12byte_name_change_andfull_ARM9_inverse_bound=True,registered_candidate=False,',
        'Bound native CPU research to a real snapshot from the exact current ROM.':'Bind native CPU research to its own exact unregistered name-correction ROM snapshot.',
    })
    binding=derive('scripts/bind_Lil_Gerhard_current_v8198.py','scripts/bind_Gerhard_research_v8218.py',{
        'scripts.Lil_current_route_context_v8198':'scripts.Gerhard_research_route_context_v8218',
        'Lil_Gerhard_current_binding_v8198':'Gerhard_research_binding_v8218',
        'Lil_Gerhard_context_runs_v8197/route2':'Gerhard_research_context_runs_v8217/route2',
        'current_V8172_Lil_native_v8198':'Gerhard_reference8215_own_native_v8218',
        "release=read('work/analysis/Rafael_B50_release_v8173/registered_release_verification.json')\n    assert sha(Path(plan['candidate']).read_bytes())==release['candidate_sha256']==plan['candidate_sha256'] and plan['profile']=='all-routes-unified-v8172'\n    assert sha(arm)==release['ARM9_sha256'] and sha(common)==release['COMMON_sha256']":
        "reference=read('work/analysis/Gerhard_reference_v8215/research_image_receipt.json');release=read('work/analysis/Rafael_B50_release_v8173/registered_release_verification.json')\n    assert not reference['registered_candidate'] and sha(Path(plan['candidate']).read_bytes())==reference['research_ROM_sha256']==plan['candidate_sha256'] and plan['profile']=='Gerhard-Adernkatz-RESEARCH-ONLY'\n    assert sha(arm)==reference['research_ARM9_sha256'] and sha(common)==release['COMMON_sha256']",
        'own_registered_capture_context.json':'own_research_capture_context.json',
        "registered_profile=plan['profile']":"research_profile=plan['profile'],registered_candidate=False",
        'V8172 Lil frame':'Research8215 Lil frame',
        'own_Lil_current_context.png':'own_Gerhard_research_context.png',
        'own_Lil_startup_andstrict_captain2_context.json':'own_research_startup_andstrict_captain2_context.json',
        'all_strict2b6_COMMON_directory_and123264_payload_guards_pass=True':'all_strict_targetARM9_inverse_COMMON_directory_and123264_payload_guards_pass=True,registered_candidate=False',
        'Bind exact own-current Lil captain2 snapshot without a historical RAM overlay.':'Bind exact own research-ROM captain2 snapshot without borrowing parent RAM.',
        'Own V8172 Lil captain2 andstrict current123264-byte context pass;startup sheet view pending.No optional scene activated.':'Own research8215 captain2 andstrict target inverse/current123264 context pass;startup view pending.No optional scene orregistered release.',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivations.json',dict(derivations=[capture,context,binding],
        exact_research_ARM9_guard=reference['research_ARM9_sha256'],all_parent_bytes_outside_owned12_inverse_bound=True,
        no_native_instruction_address_orpool_extent_changed=True,own_research_capture_required_no_parent_RAM_overlay=True,
        registered_current_V8172_andmainV4701_unchanged=True,new_credit=0,full_goal_complete=False))
    print('Prepared own research capture /strict exact-target ARM9 inverse context /binder;all existing native guards preserved.')
