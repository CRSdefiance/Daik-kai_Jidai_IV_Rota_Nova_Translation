"""Derive the one additive B51 registration, with full builder and registry inverse."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B51_registration_tools_v8608');assert not root.exists()
    source=Path('scripts/register_Hodram_B50_v8542.py').read_text(encoding='utf-8')
    a=source.index('    profile.update(');b=source.index('    updated=',a)
    profile="""    profile.update(status='experimental',hodram_outcomes_editorial='translations/hodram_outcomes_editorial_release_v7.json',hodram_B49_editorial='translations/hodram_B49_editorial_release_v5.json',hodram_B50_editorial='translations/hodram_B50_editorial_release_v2.json',hodram_B51_editorial=str(CONFIG),
        description='Complete V8543 plus clean-Japanese whole-exchange Hodram SC1B51: five speeches, four revisions and one justified retention.',
        note='Natural-dialogue-v2 en-US. Restore gruff southern Mediterranean warning, complete Hodram clarification, unnamed bad-news description and well-meant self-preservation advice; preserve conditional Charles echo and unresolved private Gerhard suspicion. No invented identity, rulership, rank, gender, kinship, crime or supernatural fact. Scoped Hodram/Joakim, Gerhard Adernkatz, Charles/Jean and Port Worker names retained; no all207-name credit. All20commands/5fullpreambles/8relatives/2queries/4opaquecontrols/fullend/tails and325loads/650modes/326actions/shippedcallers bound. Original216px width/five English singlepages/complete characters/two line-count infos/zero warnings orwaivers. Two initialized actual entry fixtures20002frames/eight pageoccurrences/56completeholds show four speeches perlanguage; CharlesR32 remains offline-tested and unvisited. Normalends4736/4734 carry[0,0];two shortduration differences,13timing/length rows differ;no sampled boundaryPRNG/UIrequest differences,finalseeds differ,3of89laterRGBpairs differ. Five sampled components/wholeactors/captain1 match;rawcalendar uninterpreted. No naturalactivation,original location,earned inventory,customnames,fullroute,hardware,everyframe causality,futurePRNGoutcomes orbroadsimulation claim. Frozenpolicy322 rejections,17atomicsemanticfailures,3genuinewrongmemory failures,25changedbuilder rejections;two atomiclifecycle reports equal/onewholeNDScommit each. Compatible predecessors reproduce entireV8543 exactly retaining535/675/756prior dependencies. Fullfourstory/earlierdialogue/sharedtown-shop/random/Help/remainingprose/207names/retrospectivewrap goalactive. Graphics/laterolder-recordtechnicalaudit separate;preserveallROMs/drafts/failures/main4701. No promotion,separatepackage,pruning,commit orpush.')
"""
    result=derive('scripts/register_Hodram_B50_v8542.py','scripts/register_Hodram_B51_v8608.py',{
        source[a:b]:profile,
        'hodram_B50_editorial_v1':'hodram_B51_editorial_v1',
        'from dk4tool.patch.hodram_outcomes_builder_guard_v6 import BUILDER,STAGE_V5,STAGE_B49_V2,STAGE_V6,STAGE_B49_V3,STAGE_B50,validate_builder_bytes':'from dk4tool.patch.hodram_outcomes_builder_guard_v7 import BUILDER,STAGE_V6,STAGE_B49_V3,STAGE_B50,STAGE_V7,STAGE_B49_V4,STAGE_B50_V2,STAGE_B51,validate_builder_bytes',
        'scripts.Hodram_B50_release_paths_v8537':'scripts.Hodram_B51_release_paths_v8595',
        'Hodram_B50_registration_v8542':'Hodram_B51_registration_v8608',
        'Hodram_B50_atomic_binding_v8541':'Hodram_B51_atomic_binding_v8606',
        'Hodram_B50_builder_validation_v8535':'Hodram_B51_builder_validation_v8596',
        'editorial_handoff_verification_v8533':'editorial_handoff_verification_v8601',
        "PROFILE='all-routes-unified-v8543'":"PROFILE='all-routes-unified-v8609'",
        "binding['all16_actually_changed_semantic_precommit_cases_rejected_without_mutation']":"binding['all17_actually_changed_semantic_precommit_cases_rejected_without_mutation'] and binding['all3_genuine_wrong_memory_inputs_rejected_withall_guards_active'] and binding['lifecycle_reports_value_equal']",
        "len(read(PARENT.with_suffix('.manifest.json'))['batches'])==643":"len(read(PARENT.with_suffix('.manifest.json'))['batches'])==644",
        '{STAGE_V5:STAGE_V6,STAGE_B49_V2:STAGE_B49_V3+STAGE_B50}':'{STAGE_V6:STAGE_V7,STAGE_B49_V3:STAGE_B49_V4,STAGE_B50:STAGE_B50_V2+STAGE_B51}',
        "inverse=after.replace(STAGE_B50.encode(),b'',1).replace(STAGE_V6.encode(),STAGE_V5.encode(),1).replace(STAGE_B49_V3.encode(),STAGE_B49_V2.encode(),1)":"inverse=after.replace(STAGE_B51.encode(),b'',1).replace(STAGE_V7.encode(),STAGE_V6.encode(),1).replace(STAGE_B49_V4.encode(),STAGE_B49_V3.encode(),1).replace(STAGE_B50_V2.encode(),STAGE_B50.encode(),1)",
        "validate_builder_bytes(after,digest)['B50_additive_stage_present']":"validate_builder_bytes(after,digest)['B51_additive_stage_present']",
        "registry['profiles']['all-routes-unified-v8475']":"registry['profiles']['all-routes-unified-v8543']",
        'build_integrated_release_v8542.tmp':'build_integrated_release_v8608.tmp',
        "parent_profile='all-routes-unified-v8475'":"parent_profile='all-routes-unified-v8543'",
        'expected_manifest_batches=644':'expected_manifest_batches=645',
        'Register B50 cumulatively after complete V8475':'Register B51 cumulatively after complete V8543',
        'Registered experimental V8543 aftercompleteV8475;expected644batches':'Registered experimental V8609 aftercompleteV8543;expected645batches',
    })
    build=derive('scripts/build_Hodram_B50_v8543.py','scripts/build_Hodram_B51_v8609.py',{
        'Hodram_B50_build_v8543':'Hodram_B51_build_v8609',
        'all_routes_combined_v8543_candidate':'all_routes_combined_v8609_candidate',
        'Hodram_B50_registration_v8542':'Hodram_B51_registration_v8608',
        'all-routes-unified-v8543':'all-routes-unified-v8609'})
    root.mkdir(parents=True);save(root/'derivation.json',dict(registration=result,sole_registered_builder_wrapper=build,exact_prior_builder_registry_inverse_andall_accepted_main4701_guards_preserved=True,no_live_registration_build_ROM_orcredit_yet=True,new_credit=0,full_goal_complete=False))
