"""Plan the complete source-qualified Hodram edit in memory; commit one NDS object after all checks."""
import json
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.hodram_three_blocks_profile_v1 import contract,profile_for,validate_runtime,validate_approved_batch
from dk4tool.dialogue.hodram_three_blocks_layout_v1 import encode_relocatable_dialogue,audit_relocatable_dialogue_record
from dk4tool.patch.hodram_three_blocks_references_v1 import reconstruct_and_bind,serializable_groups
from dk4tool.patch.hodram_three_blocks_controls_v2 import check_controls,check_loaders_and_census
from dk4tool.patch.hodram_three_blocks_evidence_v1 import check_evidence
from dk4tool.patch.hodram_three_blocks_comparison_v1 import check_comparisons
from scripts.Hodram_three_blocks_release_paths_v8290 import PARENT,ROM,DOC,NAMES,MAP,SEAL,proofs,observed_scope

CONFIG='translations/hodram_three_blocks_editorial_release_v2.json'
PATH='/data/SC1.DK4'
CANONICAL=Path('out/raphael_natural_v2_accepted_base.nds')

def load(path):return json.loads(Path(path).read_bytes())

def require(ok,message):
    if not ok:raise ValueError('Hodram atomic editorial contract: '+message)

def check_dependencies(conf):
    for path,digest in conf['dependencies'].items():require(sha(Path(path).read_bytes())==digest,'dependency:'+path)

def commit_image(image,rom):image.rom=rom

def plan_release(image,baseline,config=CONFIG):
    conf=load(config);check_dependencies(conf)
    require(conf['format']=='dk4-Hodram-three-blocks-editorial-release-v1' and conf['manuscripts']==[str(DOC)] and conf['proofs']==proofs(),'exact complete source-qualified configuration')
    require((conf['reference_map'],conf['reference_approval'],conf['parent_ROM'],conf['reference_ROM'],conf['canonical_ROM'])==(str(MAP),str(SEAL),str(PARENT),str(ROM),str(CANONICAL)),'exact sealed parent/reference/canonical paths')
    require(sha(baseline.source.read_bytes())==sha(CANONICAL.read_bytes())==conf['canonical_ROM_sha256']=='3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe','canonical baseline identity')
    require(conf['clean_ROM']=='work/clean.nds' and sha(Path(conf['clean_ROM']).read_bytes())==conf['clean_ROM_sha256']=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d','exact clean Japanese input')
    require(sha(PARENT.read_bytes())==conf['parent_ROM_sha256']==sha(bytes(image.rom.save())) and sha(ROM.read_bytes())==conf['reference_ROM_sha256'],'whole predecessor/reference identities')
    require({p:sha(v) for _,p,v in image.iter_files()}==conf['predecessor_file_hashes'] and {p:sha(v) for p,v in image.iter_components()}==conf['predecessor_component_hashes'],'every predecessor file/component')
    frozen=validate_runtime(image);doc=load(conf['manuscripts'][0]);validate_approved_batch(doc)
    data={k:load(p) for k,p in conf['proofs'].items()};mapping,seal=load(conf['reference_map']),load(conf['reference_approval'])
    require(data['native_contract']==frozen and data['names']==frozen['name_review_binding'],'frozen complete native andscoped-name approvals')
    require(mapping['file_path']==PATH and mapping['external_references_complete'] and mapping['all60commands28sixbyte_preambles8relatives_source_current_target_bound'] and mapping['every_clean_source_block_predecessor_archive_andwhole_ROM_inverse_exact'],'complete source/current/final reference flags')
    require(mapping['new_credit']==seal['new_credit']==0 and not mapping['full_goal_complete'] and not seal['full_goal_complete'],'no premature completion credit orfull-goal claim')
    require(seal['manuscript_sha256']==sha(DOC.read_bytes()) and seal['name_review_sha256']==sha(NAMES.read_bytes()) and seal['reference_map_sha256']==sha(MAP.read_bytes()),'sealed reviewed manuscript/name/map lineage')
    require(mapping['source_ROM_sha256']==seal['parent_sha256']==conf['parent_ROM_sha256'] and seal['research_ROM_sha256']==conf['reference_ROM_sha256'] and seal['independent_entire_ROM_equal_tested_reference'],'sealed full parent/reference equality')
    require(data['reference']['parent_sha256']==conf['parent_ROM_sha256'] and data['reference']['research_ROM_sha256']==conf['reference_ROM_sha256'],'pinned reference receipt')
    policy=data['policy_validation'];require(policy['positive_count']==len(policy['positives'])==28 and policy['negative_count']==len(policy['negatives'])==579 and all(n['rejected'] for n in policy['negatives']) and policy['all_changed_inputs_verified_distinct'],'28policy positives/579actual-changing expected rejections')
    source=data['current'];arm=image.read_file('/__arm9__.bin');archive=image.read_file(PATH)
    require(doc['current_ROM_sha256']==source['current_ROM_sha256']==conf['parent_ROM_sha256'] and doc['current_archive_sha256']==source['current_archive_sha256']==mapping['source_archive_sha256']==sha(archive),'exact source-qualified previous archive')
    require(doc['current_ARM9_sha256']==source['current_ARM9_sha256']==sha(arm) and doc['current_COMMON_sha256']==source['current_COMMON_sha256']==sha(image.read_file('/COMMON/MESFILE.DK4')),'current runtime/shared names dependency')
    dependency=frozen['explicit_registered_Gerhard_dependency'];require(dependency==conf['required_registered_Gerhard_dependency'] and dependency['candidate_sha256']==conf['parent_ROM_sha256'] and dependency['ARM9_sha256']==sha(arm),'explicit registered Adernkatz parent dependency')
    require(sha(Path(dependency['correction']).read_bytes())==dependency['correction_sha256'],'registered surname correction configuration')
    require(conf['archives']==[dict(file_path=PATH,source_sha256=sha(archive),target_sha256=mapping['target_archive_sha256'])] and conf['components']==[],'only one owned SC1 archive,no new name orcode mutation')
    bank=IlnkContainer.parse(archive).blocks
    for row,positive in zip(doc['records'],policy['positives'],strict=True):
        ident=row['id'];raw=bytes.fromhex(row['source_hex']);p=profile_for(arm,bank[row['block']],ident,PATH,'progressive')
        encoded=encode_relocatable_dialogue(raw,row['planned_English_markup'],p);qa=audit_relocatable_dialogue_record(raw,row['planned_English_markup'],p)
        require(encoded.encoded.hex()==row['compiled_hex']==frozen['record_bindings'][ident]['compiled_hex']==positive['compiled_hex'] and positive['id']==ident,'independent complete compiler output:'+ident)
        require(qa['issues']==row['all_original_QA_issues'] and qa==positive['qa'] and qa['native_page_count']==1,'all original QA andexact ordinary wrap allowances:'+ident)
        require(qa['qa_waivers']==row['qa_waivers'] and qa['qa_waiver_scope']==row['qa_waiver_scope'],'only exact source/prose-bound warning scopes:'+ident)
    result=reconstruct_and_bind(image,NdsImage.open(conf['clean_ROM']),doc,data['relocation'],source)
    require(serializable_groups(result)==mapping['groups'] and sha(result['target_archive'])==mapping['target_archive_sha256'],'every independent native reference/relative/header/tail/inverse map')
    refs=[]
    for group in result['groups']:
        for r in group['text_records']:
            row=next(x for x in doc['records'] if x['id']==r['id'])
            refs.append(dict(id=r['id'],file_path=PATH,block=group['block'],source_reference=row['source_reference'],current_reference=row['current_reference'],
                target_reference=dict(file_path=PATH,block=group['block'],offset=r['new_offset'],bytes=r['new_length'],header_offset=r['new_offset']-5,record_index=r['new_record_index'],target_block_sha256=group['target_block_sha256']),
                source_hex=row['source_hex'],previous_hex=row['current_hex'],compiled_hex=row['compiled_hex'],stored_hex=r['target_hex'],source_complete_preamble_hex=row['source_complete_preamble_hex'],source_selector=row['source_selector'],
                editorial_decision=row['decision'],retention_reason=row['retention_reason'],review=row['review']))
    require(refs==mapping['records'],'all28 exact source/current/final records andindividual reasons')
    reference=NdsImage.open(ROM);controls=check_controls(data,doc['records'],image,reference,result,load,require)
    entries=check_loaders_and_census(data,image,reference,result,load,require)
    actual=check_evidence(data,doc['records'],image,reference,result,load,require)
    comparison=check_comparisons(data,image,load,require);scope=observed_scope(data)
    require(scope==mapping['observed_scope']==seal['observed_scope'],'all recomputed timing/RNG/UI/component/calendar/RGB andfixture scope limits')
    approval=data['display_approval'];require(approval['all28_five_per_record_gates_true'] and approval['actual_complete_speech_observations_both_versions']==actual['actual_speech_observations'] and approval['actual_complete_body_andname_holds_both_versions']==actual['complete_body_holds'],'scoped actual display approval')
    require(approval['B137_fixture_later_captain0_andparty0_not_normal_Hodram_route_continuity'] and approval['initialized_opening_not_original_event_activation_location_eligibility_orall_attainable_effect_paths'] and approval['no_every_frame_causality_future_outcome_broad_simulation_fullroute_orhardware_claim'],'mandatory actual fixture/simulation scope limits')
    planned=deepcopy(image);planned.replace_file(PATH,result['target_archive']);validate_runtime(planned)
    require(bytes(planned.rom.save())==ROM.read_bytes(),'whole planned ROM equals approved tested reference')
    require([p for _,p,v in image.iter_files() if planned.read_file(p)!=v]==[PATH] and all(planned.read_file(p)==v for p,v in image.iter_components()),'only owned SC1 file changes;all code/fonts/graphics/names components exact')
    restored=deepcopy(planned);restored.replace_file(PATH,archive);require(bytes(restored.rom.save())==PARENT.read_bytes(),'every complete predecessor ROM byte inverses')
    changes=[dict(id=r['id'],file_path=PATH,block=r['block'],kind='progressive',old_offset=r['current_reference']['offset'],new_offset=r['target_reference']['offset']) for r in refs]
    return planned.rom,dict(manuscripts=conf['manuscripts'],reference_map=conf['reference_map'],changed_records=changes,
        files=[dict(file_path=PATH,source_sha256=sha(archive),target_sha256=sha(result['target_archive']),changed_records=changes)],
        one_complete_NDS_object_commit_after_all_gates=True,all60commands28preambles8relatives_three_clean_source_andfull_parent_inverses_exact=True,
        explicit_registered_Adernkatz_dependency_preserved=True,native_controls=controls,native_entries=entries,native_actual=actual,comparison=comparison,actual_scope=scope,
        editorial_completion_credit_pending_registered_release=True,full_goal_complete=False)

def apply_release(image,baseline,config=CONFIG):
    try:planned,report=plan_release(image,baseline,config)
    except (KeyError,TypeError,IndexError,AssertionError,StopIteration) as exc:
        raise ValueError('Hodram atomic editorial contract: invalid orcontradictory evidence schema: '+str(exc)) from exc
    commit_image(image,planned)
    return report
