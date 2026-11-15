"""Preserve complete original loader/census guards and qualify14fresh/636exact reused parent cases."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B54_B60_loader_tools_v8841');assert not root.exists()
    module=derive('dk4tool/patch/hodram_B31_B53_loaders_v1.py','dk4tool/patch/hodram_B54_B60_loaders_v1.py',{
        'both complete B31/B53 blocks':'all seven complete B54-B60 blocks',
        "loader['archive_block_counts']=={'1':325} and ":'',
        "loader['fresh_initial_parent_modes']==650":"loader['fresh_initial_parent_modes']==14 and loader['exact_reused_initial_parent_modes']==636 and loader['total_bound_initial_parent_modes']==650 and loader['fresh_parent_blocks']==[54,55,56,57,58,59,60]",
        "    cases=modes['native_handoff_and_first_read_cases'];require":"    require(sha(Path(loader['prior_mode_proof']).read_bytes())==loader['prior_mode_proof_sha256'] and sha(Path(loader['prior_complete_loader_proof']).read_bytes())==loader['prior_complete_loader_proof_sha256'],'exact prior parent-case provenance')\n    prior_modes=load(loader['prior_mode_proof']);prior_loader=load(loader['prior_complete_loader_proof'])\n    require(prior_modes['ROM_sha256']==prior_loader['research_ROM_sha256']==sha(bytes(parent.rom.save())) and parent.read_file('/__arm9__.bin')==reference.read_file('/__arm9__.bin'),'reused cases exact registered predecessor andwhole unchanged runtime')\n    old_cases={(c['block'],c['mode']):c for c in prior_modes['native_handoff_and_first_read_cases']}\n    cases=modes['native_handoff_and_first_read_cases'];require",
        "        block=blocks[c['block']];length=":"        if c['block'] not in range(54,61):require(c==old_cases[(c['block'],c['mode'])],'every unchanged parent case exactly reused fromverified complete predecessor')\n        block=blocks[c['block']];length=",
        "for r in modes['executed_source_words']:":"for r in [*modes['executed_source_words'],*prior_modes['executed_source_words']]:",
        '[31,53]':'[54,55,56,57,58,59,60]','explicit two-block source-reference scope':'explicit seven-block source-reference scope',
        'all18 caller-selected complete command maps':'all152 caller-selected complete command maps',
        "caller['all3_speech_records']":"caller['all82_speech_records']",'all3 disjoint canonical source/current/final references':'all82 disjoint canonical source/current/final references',
        'both original blockindex entries andall nested relative targets':'seven original blockindex entries andall nested relative targets',
        "[(31,31,[52],[]),(53,53,[31],[74])]":"[(54,54,[],[]),(55,55,[],[76,129]),(56,56,[15],[]),(57,57,[128],[65]),(58,58,[],[]),(59,59,[],[]),(60,60,[142],[])]",
        'original52->31->53 connection/exclusion74,not full eligibility/location/chronology':'all seven source prerequisites andexclusions,not full eligibility/location/chronology',
        'initial_parent_modes_bound=650,original_EV1_actions_bound=326':'initial_parent_modes_bound=650,fresh_parent_cases=14,exact_reused_parent_cases=636,original_EV1_actions_bound=326',
    })
    validation=derive('scripts/validate_Hodram_B31_B53_loaders_v8761.py','scripts/validate_Hodram_B54_B60_loaders_v8842.py',{
        'hodram_B31_B53_profile_v1':'hodram_B54_B60_profile_v1','hodram_B31_B53_loaders_v1':'hodram_B54_B60_loaders_v1',
        'review_Hodram_B31_B53_actual_v8744':'review_Hodram_B54_B60_actual_v8825',
        "ROOT=Path('work/analysis/Hodram_B31_B53_loader_validation_v8761')":"PROOFS={**PROOFS,'current':'work/analysis/Hodram_B54_B60_current_v8799/current_effective.json'}\nROOT=Path('work/analysis/Hodram_B54_B60_loader_validation_v8842')",
        'translations/hodram_B31_B53_editorial_manuscript_v5.json':'translations/hodram_B54_B60_editorial_manuscript_v4.json',
        'Hodram_B31_B53_reference_validation_v8756':'Hodram_B54_B60_reference_validation_v8836',
        'dk4tool/patch/hodram_B31_B53_loaders_v1.py':'dk4tool/patch/hodram_B54_B60_loaders_v1.py',
        'B31/B53 production loaders:':'B54-B60 production loaders:','Frozen Hodram-B31-B53 contract changed':'Frozen Hodram-B54-B60 contract changed',
        'positive_entire_archive_whole_reference_ROM_all323_unownedblocks_files_components_andallinverses':'positive_entire_archive_whole_reference_ROM_all318_unownedblocks_files_components_andallinverses',
        "__setitem__('native_selected_block',53)":"__setitem__('native_selected_block',60)",
        "__setitem__('must_be_completed',[])":"__setitem__('must_be_completed',[15])",
        '    assert len(cases)==8 and':"    reject('wrong-exact-reused-parent-count',lambda d,r:d['loaders'].__setitem__('exact_reused_initial_parent_modes',635))\n    reject('wrong-prior-parent-case-proof-digest',lambda d,r:d['loaders'].__setitem__('prior_mode_proof_sha256','0'*64))\n    reject('incomplete-fresh-seven-block-set',lambda d,r:d['loaders'].__setitem__('fresh_parent_blocks',[54]))\n    assert len(cases)==11 and",
        'negative_count=8':'negative_count=11',
        'Production loader/census reader:325loads650parentmodes326actions/bothentries/fresh shippedcode scan pass;8semantic defects reject. No native-loader/capture replay,ROMcommit orcredit.':'Production loader/census reader:325loads/14fresh636exact-reused parentmodes/326actions/seven entries/fresh shippedcode scan pass;11semantic defects reject. No native-loader/capture replay,ROMcommit orcredit.',
    })
    root.mkdir(parents=True);save(root/'source_locked_loaders.json',dict(module=module,validation=validation,all_original_native_payload_IO_cache_neighbor_ABI_SP_PC_firstread_header_tail_fullinstruction_andcensus_guards_preserved=True,exact636_reuse_requires_original_wholepredecessor_complete_payloads_currentARM9_andindividual_case_equality=True,no_native_loader_producer_orcapture_replay=True,new_credit=0,full_goal_complete=False))
