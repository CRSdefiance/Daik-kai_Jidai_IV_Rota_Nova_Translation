"""Validate complete mixed-consumer outcomes in memory, then commit exactly one whole NDS object."""
import json
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_outcomes_builder_guard_v2 import checked_dependency
from dk4tool.dialogue.hodram_outcomes_profile_v3 import validate_runtime,validate_approved_batch,profile_for
from dk4tool.dialogue.hodram_outcomes_layout_v3 import encode_relocatable_dialogue,audit_relocatable_dialogue_record
from dk4tool.dialogue.hodram_outcomes_names_v3 import validate_scoped_names
from dk4tool.patch.hodram_outcome_references_v1 import reconstruct_and_bind,serializable_groups
from dk4tool.patch.hodram_outcomes_native_evidence_v4 import check_native_models
from dk4tool.patch.hodram_outcomes_actual_evidence_v2 import check_actual
from dk4tool.patch.hodram_outcomes_comparison_v1 import check_comparisons
from dk4tool.patch.hodram_outcomes_FE_evidence_v2 import check_FE_geometry
from dk4tool.patch.hodram_outcomes_controls_v3 import check_controls,check_loaders_and_census
from scripts.Hodram_outcomes_release_paths_v8347 import PARENT,ROM,DOC,NAMES,MAP,SEAL,proofs,observed_scope

CONFIG='translations/hodram_outcomes_editorial_release_v3.json'
PATH='/data/SC1.DK4'
CANONICAL=Path('out/raphael_natural_v2_accepted_base.nds')

def load(path):return json.loads(Path(path).read_bytes())
def require(ok,message):
    if not ok:raise ValueError('Hodram outcomes atomic contract: '+message)
def check_dependencies(conf):
    for path,digest in conf['dependencies'].items():require(checked_dependency(Path(path),digest),'dependency:'+path)
def commit_image(image,rom):image.rom=rom

def plan_release(image,baseline,config=CONFIG):
    conf=load(config);check_dependencies(conf)
    require(conf['format']=='dk4-Hodram-outcomes-editorial-release-v1' and conf['manuscripts']==[str(DOC)] and conf['proofs']==proofs(),'exact complete source-qualified configuration')
    require((conf['reference_map'],conf['reference_approval'],conf['parent_ROM'],conf['reference_ROM'],conf['canonical_ROM'])==(str(MAP),str(SEAL),str(PARENT),str(ROM),str(CANONICAL)),'exact sealed parent/reference/canonical paths')
    require(sha(baseline.source.read_bytes())==sha(CANONICAL.read_bytes())==conf['canonical_ROM_sha256']=='3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe','canonical baseline identity')
    require(conf['clean_ROM']=='work/clean.nds' and sha(Path(conf['clean_ROM']).read_bytes())==conf['clean_ROM_sha256']=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d','exact clean Japanese input')
    require(sha(PARENT.read_bytes())==conf['parent_ROM_sha256']==sha(bytes(image.rom.save())) and sha(ROM.read_bytes())==conf['reference_ROM_sha256'],'whole predecessor/reference identities')
    require({p:sha(v) for _,p,v in image.iter_files()}==conf['predecessor_file_hashes'] and {p:sha(v) for p,v in image.iter_components()}==conf['predecessor_component_hashes'],'every predecessor file/component')
    frozen=validate_runtime(image);doc=load(DOC);validate_approved_batch(doc)
    data={k:load(p) for k,p in conf['proofs'].items()};mapping,seal=load(MAP),load(SEAL)
    require(data['native_contract']==frozen and data['names']==frozen['name_review_binding'],'frozen complete native andscoped-name approvals');validate_scoped_names(data['names'])
    require(mapping['file_path']==PATH and mapping['external_references_complete'] and mapping['all15commands6sixbyte_preambles_zero_relatives_one_FE_one_FI_source_current_target_bound'] and mapping['every_clean_source_block_predecessor_archive_andwhole_ROM_inverse_exact'],'complete source/current/final reference flags')
    require(mapping['new_credit']==seal['new_credit']==0 and not mapping['full_goal_complete'] and not seal['full_goal_complete'],'no premature completion credit orfull-goal claim')
    require(seal['manuscript_sha256']==sha(DOC.read_bytes()) and seal['name_review_sha256']==sha(NAMES.read_bytes()) and seal['reference_map_sha256']==sha(MAP.read_bytes()),'sealed reviewed manuscript/name/map lineage')
    require(mapping['source_ROM_sha256']==seal['parent_sha256']==conf['parent_ROM_sha256'] and seal['research_ROM_sha256']==conf['reference_ROM_sha256'] and seal['independent_entire_ROM_equal_tested_reference'],'sealed full parent/reference equality')
    require(data['reference']['parent_sha256']==conf['parent_ROM_sha256'] and data['reference']['research_ROM_sha256']==conf['reference_ROM_sha256'],'pinned reference receipt')
    policy=data['policy_validation'];require(policy['positive_count']==len(policy['positives'])==6 and policy['negative_count']==len(policy['negatives'])==357 and all(n['rejected'] for n in policy['negatives']) and policy['all_changed_inputs_verified_distinct'] and policy['all_rejections_match_expected_guard'],'six policy positives/357 actual-changing expected rejections')
    source=data['current'];arm=image.read_file('/__arm9__.bin');archive=image.read_file(PATH)
    require(doc['current_ROM_sha256']==source['current_ROM_sha256']==conf['parent_ROM_sha256'] and doc['current_archive_sha256']==source['current_archive_sha256']==mapping['source_archive_sha256']==sha(archive),'exact source-qualified previous archive')
    require(doc['current_ARM9_sha256']==source['current_ARM9_sha256']==sha(arm) and doc['current_COMMON_sha256']==source['current_COMMON_sha256']==sha(image.read_file('/COMMON/MESFILE.DK4')),'current runtime/shared names dependency')
    dependency=frozen['explicit_registered_Gerhard_dependency'];require(dependency==conf['required_registered_Gerhard_dependency'] and dependency['candidate_sha256']==conf['parent_ROM_sha256'] and dependency['ARM9_sha256']==sha(arm),'explicit registered Adernkatz parent dependency')
    require(sha(Path(dependency['correction']).read_bytes())==dependency['correction_sha256'],'registered surname correction configuration')
    require(conf['archives']==[dict(file_path=PATH,source_sha256=sha(archive),target_sha256=mapping['target_archive_sha256'])] and conf['components']==[],'only one owned SC1 archive,no new name orcode mutation')
    bank=IlnkContainer.parse(archive).blocks
    for row,positive in zip(doc['records'],policy['positives'],strict=True):
        ident=row['id'];raw=bytes.fromhex(row['source_hex']);consumer=frozen['record_bindings'][ident]['consumer'];p=profile_for(arm,bank[row['block']],ident,PATH,consumer)
        encoded=encode_relocatable_dialogue(raw,row['planned_English_markup'],p);qa=audit_relocatable_dialogue_record(raw,row['planned_English_markup'],p)
        require(encoded.encoded.hex()==row['compiled_hex']==frozen['record_bindings'][ident]['compiled_hex']==positive['compiled_hex'] and positive['id']==ident and positive['consumer']==consumer,'independent complete mixed-consumer compiler output:'+ident)
        require(qa==positive['qa'] and qa['native_page_count']==1 and not qa['qa_waivers'],'all original QA/single-page bounds andzero waivers:'+ident)
    clean=NdsImage.open(conf['clean_ROM']);result=reconstruct_and_bind(image,clean,doc,data['relocation'],source)
    require(serializable_groups(result)==mapping['groups'] and sha(result['target_archive'])==mapping['target_archive_sha256'],'every independent native reference/header/tail/inverse map')
    refs=[]
    for group in result['groups']:
        for r in group['text_records']:
            row=next(x for x in doc['records'] if x['id']==r['id'])
            refs.append(dict(id=r['id'],file_path=PATH,block=group['block'],source_reference=row['source_reference'],current_reference=row['current_reference'],target_reference=dict(file_path=PATH,block=group['block'],offset=r['new_offset'],bytes=r['new_length'],header_offset=r['new_offset']-5,record_index=r['new_record_index'],target_block_sha256=group['target_block_sha256']),source_hex=row['source_hex'],current_hex=row['current_hex'],compiled_hex=row['compiled_hex'],stored_hex=r['target_hex'],consumer=frozen['record_bindings'][r['id']]['consumer']))
    require(refs==mapping['records'],'all six exact source/current/final records andconsumers')
    reference=NdsImage.open(ROM);native=check_native_models(data,doc['records'],image,load,require)
    controls=check_controls(data,doc['records'],image,reference,result,native,load,require);entries=check_loaders_and_census(data,image,reference,result,load,require)
    actual=check_actual(data,doc['records'],image,clean,result,native,load,require);FE=check_FE_geometry(data,image,native,load,require);comparison=check_comparisons(data,image,load,require);scope=observed_scope(data)
    require(scope==mapping['observed_scope']==seal['observed_scope'],'all recomputed timing/RNG/UI/component/calendar/RGB andfixture scope limits')
    approval=data['display'];require(approval['all_six_five_perrecord_review_gates_true'] and approval['actual_complete_body_header_orFE_absent_header_holds']==actual['complete_actual_holds']==100 and approval['six_source_and_six_revised_actual_single_pages'] and approval['original_FE_two_paint_snapshots_four_actual_VRAM_palette_RGB_holds_bound'],'scoped actual body/name/FE display approval')
    require(approval['later_difference_characterization']=='B48 frame4870 differs in the A prompt;5410 and7030 in menu highlight;9550through10001 in lower-screen sailing clouds. All script-boundary seeds match,but final B48 seeds differ. This is measured scope,not a causal explanation orfuture-outcome equivalence.' and approval['full_measured_command_UI_duration_native_components_actor_captain_rawcalendar_PRNG_andRGB_scope']==data['comparison']['groups'],'all approved measured later differences andcomparison scope')
    require(approval['six_fullruns_orfour_whole_scene_plus_two_focused_counts']==dict(whole_scene_runs=4,whole_scene_frames=40004,focused_boundary_runs=2,focused_boundary_frames=8002,total_actual_frames=48006),'four whole scene andtwo focused FE run scope')
    planned=deepcopy(image);planned.replace_file(PATH,result['target_archive']);validate_runtime(planned)
    require(bytes(planned.rom.save())==ROM.read_bytes(),'whole planned ROM equals approved tested reference')
    require([p for _,p,v in image.iter_files() if planned.read_file(p)!=v]==[PATH] and all(planned.read_file(p)==v for p,v in image.iter_components()),'only owned SC1 file changes;all code/fonts/graphics/names components exact')
    restored=deepcopy(planned);restored.replace_file(PATH,archive);require(bytes(restored.rom.save())==PARENT.read_bytes(),'every complete predecessor ROM byte inverses')
    changes=[dict(id=r['id'],file_path=PATH,block=r['block'],kind=r['consumer'],old_offset=r['current_reference']['offset'],new_offset=r['target_reference']['offset']) for r in refs]
    return planned.rom,dict(manuscripts=conf['manuscripts'],reference_map=conf['reference_map'],changed_records=changes,files=[dict(file_path=PATH,source_sha256=sha(archive),target_sha256=sha(result['target_archive']),changed_records=changes)],one_complete_NDS_object_commit_after_all_gates=True,all15commands6preambles_two_full_ends_andall_clean_parent_inverses_exact=True,explicit_registered_Adernkatz_dependency_preserved=True,native_summary=native['summary'],native_controls=controls,native_entries=entries,native_actual=actual,original_FE=FE,comparison=comparison,actual_scope=scope,editorial_completion_credit_pending_registered_release=True,full_goal_complete=False)

def apply_release(image,baseline,config=CONFIG):
    try:planned,report=plan_release(image,baseline,config)
    except (KeyError,TypeError,IndexError,AssertionError,StopIteration) as exc:
        raise ValueError('Hodram outcomes atomic contract: invalid orcontradictory evidence schema: '+str(exc)) from exc
    commit_image(image,planned)
    return report
