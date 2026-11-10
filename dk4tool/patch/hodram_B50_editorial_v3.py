"""Validate the complete reviewed B50 exchange, then commit exactly one whole NDS object."""
import json
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_outcomes_builder_guard_v8 import checked_dependency
from dk4tool.dialogue.hodram_B50_profile_v2 import validate_runtime,validate_approved_batch,profile_for
from dk4tool.dialogue.hodram_B50_layout_v2 import encode_relocatable_dialogue,audit_relocatable_dialogue_record
from dk4tool.dialogue.hodram_B50_names_v2 import validate_scoped_names
from dk4tool.patch.hodram_B50_references_v1 import reconstruct_and_bind
from dk4tool.patch.hodram_B50_native_evidence_v1 import check_native_models
from dk4tool.patch.hodram_B50_actual_evidence_v1 import check_actual
from dk4tool.patch.hodram_B50_FE_evidence_v1 import check_FE_geometry
from dk4tool.patch.hodram_B50_comparison_v1 import check_comparisons
from dk4tool.patch.hodram_B50_controls_v1 import check_controls
from dk4tool.patch.hodram_B50_loaders_v1 import check_loaders_and_census
from scripts.Hodram_B50_release_paths_v8537 import PARENT,ROM,DOC,NAMES,SEAL,CONFIG,proofs,observed_scope

PATH='/data/SC1.DK4'
CANONICAL=Path('out/raphael_natural_v2_accepted_base.nds')
def load(path):return json.loads(Path(path).read_bytes())
def require(ok,message):
    if not ok:raise ValueError('Hodram B50 atomic contract: '+message)
def check_dependencies(conf):
    for path,digest in conf['dependencies'].items():require(checked_dependency(Path(path),digest),'dependency:'+path)
def commit_image(image,rom):image.rom=rom

def plan_release(image,baseline,config=CONFIG):
    conf=load(config);check_dependencies(conf)
    require(conf['format']=='dk4-Hodram-B50-editorial-release-v1' and conf['manuscripts']==[str(DOC)] and conf['proofs']==proofs(),'exact complete source-qualified configuration')
    require((conf['parent_ROM'],conf['reference_ROM'],conf['canonical_ROM'],conf['reference_approval'])==(str(PARENT),str(ROM),str(CANONICAL),str(SEAL)),'exact sealed parent/reference/canonical paths')
    require(sha(baseline.source.read_bytes())==sha(CANONICAL.read_bytes())==conf['canonical_ROM_sha256']=='3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe','canonical baseline identity')
    require(conf['clean_ROM']=='work/clean.nds' and sha(Path(conf['clean_ROM']).read_bytes())==conf['clean_ROM_sha256']=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d','clean Japanese identity')
    require(sha(PARENT.read_bytes())==conf['parent_ROM_sha256']==sha(bytes(image.rom.save())) and sha(ROM.read_bytes())==conf['reference_ROM_sha256'],'whole in-memory predecessor/reference identities')
    require({p:sha(v) for _,p,v in image.iter_files()}==conf['predecessor_file_hashes'] and {p:sha(v) for p,v in image.iter_components()}==conf['predecessor_component_hashes'],'every predecessor file/component')
    frozen=validate_runtime(image);doc=load(DOC);validate_approved_batch(doc);data={k:load(p) for k,p in conf['proofs'].items()};seal=load(SEAL)
    require(data['native_contract']==frozen and data['names']==frozen['name_review_binding'],'frozen native andscoped-name approvals');validate_scoped_names(data['names'])
    require(seal['manuscript_sha256']==sha(DOC.read_bytes()) and seal['name_review_sha256']==sha(NAMES.read_bytes()) and seal['parent_sha256']==conf['parent_ROM_sha256'] and seal['reference_sha256']==conf['reference_ROM_sha256'],'sealed manuscript/name/whole image lineage')
    require(doc['current_ROM_sha256']==conf['parent_ROM_sha256'] and doc['reference_ROM_sha256']==conf['reference_ROM_sha256'] and doc['source_current_final_references_complete'],'current reviewed source/final identity')
    policy=data['policy_validation'];require(len(policy['positive_speech_compilers'])==3 and policy['positive_editorial_units']==3 and policy['negative_count']==len(policy['negative_cases'])==182 and policy['every_negative_actual_input_changed_andguard_rejected'] and policy['all_frozen_dependency_guards_remained_enabled'],'3speech/nochoice positives and182meaningful policy rejections')
    dependency=conf['required_registered_stack_dependency'];slot=data['Gerhard_reference']['only_changed_name_span'];arm=image.read_file('/__arm9__.bin');at=slot['offset']
    require(dependency==seal['required_registered_stack_dependency'] and dependency['predecessor_profile']=='all-routes-unified-v8475' and dependency['predecessor_ROM_sha256']==conf['parent_ROM_sha256'] and dependency['name_span']==slot,'explicit registered V8475/Adernkatz/B49 dependency')
    require(slot['bytes']==12 and arm[at:at+12].hex()==slot['target_hex'] and arm[at+12:at+20]==b'Blades\0\0' and sha(arm)==data['Gerhard_release']['ARM9_sha256']==data['predecessor_release']['ARM9_sha256'],'complete12byte registered surname andfollowing8byte name preserved')
    for key,path in [('correction','translations/gerhard_surname_editorial_release_v2.json'),('registered_B49','translations/hodram_B49_editorial_release_v3.json'),('compatible_B49','translations/hodram_B49_editorial_release_v4.json'),('compatible_outcomes','translations/hodram_outcomes_editorial_release_v6.json')]:
        require(Path(dependency[key]).resolve()==Path(path).resolve() and sha(Path(path).read_bytes())==dependency[key+'_sha256'],'exact registered/compatible predecessor configuration:'+key)
    require(data['predecessor_release']['profile']=='all-routes-unified-v8475' and data['predecessor_release']['candidate_sha256']==conf['parent_ROM_sha256'] and data['predecessor_release']['all643_manifest_batches_and114_accepted_layers_present'],'entire registered V8475 predecessor stack')
    require(data['predecessor_compatibility']['whole_registered_V8475_ROM_byte_exact'] and data['predecessor_compatibility']['current_V8475_sha256']==conf['parent_ROM_sha256'] and data['predecessor_compatibility']['all_native_semantic_production_gates_enabled'],'compatible predecessors reproduce whole V8475')
    require(data['builder_support']['all524_prior_outcomes_dependencies_retained_exact'] and data['builder_support']['all663_prior_B49_dependencies_retained_exact'] and data['builder_validation']['negative_count']==16,'all old dependency entries andmeaningful additive-builder rejections')
    archive=image.read_file(PATH);bank=IlnkContainer.parse(archive).blocks
    for row,positive in zip(doc['records'],policy['positive_speech_compilers'],strict=True):
        ident=row['id'];raw=bytes.fromhex(row['source_hex']);consumer=frozen['record_bindings'][ident]['consumer'];profile=profile_for(arm,bank[50],ident,PATH,consumer)
        encoded=encode_relocatable_dialogue(raw,row['planned_English_markup'],profile);qa=audit_relocatable_dialogue_record(raw,row['planned_English_markup'],profile)
        require(encoded.encoded.hex()==row['compiled_hex']==frozen['record_bindings'][ident]['compiled_hex']==positive['compiled_hex'] and positive['id']==ident,'complete per-record compiler output:'+ident)
        require(qa['base_QA_issues']==frozen['record_bindings'][ident]['base_QA_issues'] and qa['native_page_count']==1 and not qa['qa_waivers'] and not any(i['severity'] in ['warning','error'] for i in qa['issues']),'native full-width bounds/pagination andunchanged QA:'+ident)
    clean=NdsImage.open(conf['clean_ROM']);reference=NdsImage.open(ROM);result=reconstruct_and_bind(image,clean,reference,doc,data,require)
    require(conf['archives']==[dict(file_path=PATH,source_sha256=sha(archive),target_sha256=sha(result['target_archive']))] and conf['components']==[],'only one owned SC1 archive,no code/nameasset changes')
    require(seal['records']==[dict(id=r['id'],source_reference=r['source_reference'],current_reference=r['current_reference'],final_reference=r['final_reference'],source_hex=r['source_hex'],current_hex=r['current_hex'],final_hex=r['final_hex']) for r in doc['records']],'three sealed exact source/current/final references')
    native=check_native_models(data,doc['records'],image,load,require)
    controls=check_controls(data,doc['records'],image,reference,result,native,load,require);loaders=check_loaders_and_census(data,image,reference,result,load,require)
    actual=check_actual(data,doc['records'],image,clean,result,native,load,require)
    FE=check_FE_geometry(data,image,native,load,require);comparison=check_comparisons(data,image,load,require)
    scope=observed_scope(data);require(scope==seal['observed_scope'] and scope['complete_page_occurrences']==6 and scope['complete_body_name_orabsent_FE_header_holds']==50,'all measured actual fixture/timing/RNG/component/calendar/RGB limits')
    approval=data['format_approval'];require(approval['all3_five_gates_true'] and approval['measured_limits']['all_three_sheets_directly_viewed'] and doc['total_actual_frames']==scope['total_actual_frames']==20002 and data['gate_metadata_approval']['manuscript_sha256']==sha(DOC.read_bytes()),'complete per-record format/native/actual approval')
    for sheet in approval['measured_limits']['directly_viewed_sheets']:require(sha(Path(sheet['path']).read_bytes())==sheet['sha256'],'directly viewed full glyph/layout evidence')
    planned=deepcopy(image);planned.replace_file(PATH,result['target_archive']);validate_runtime(planned)
    require(bytes(planned.rom.save())==ROM.read_bytes(),'whole planned ROM equals tested reference')
    require([p for _,p,v in image.iter_files() if planned.read_file(p)!=v]==[PATH] and all(planned.read_file(p)==v for p,v in image.iter_components()),'every unowned file/component exact')
    inverse=deepcopy(planned);inverse.replace_file(PATH,archive);require(bytes(inverse.rom.save())==bytes(image.rom.save()),'whole in-memory predecessor inverse')
    changes=[dict(id=r['id'],file_path=PATH,block=50,kind=frozen['record_bindings'][r['id']]['consumer'],old_offset=r['current_reference']['offset'],new_offset=r['final_reference']['offset']) for r in doc['records']]
    return planned.rom,dict(manuscripts=conf['manuscripts'],reference_approval=conf['reference_approval'],changed_records=changes,files=[dict(file_path=PATH,source_sha256=sha(archive),target_sha256=sha(result['target_archive']),changed_records=changes)],one_complete_NDS_object_commit_after_all_gates=True,all12_commands3_preambles_zero_relative_query_choice_sites_effects_ends_andtails_preserved=True,all_clean_current_archive_andwhole_ROM_inverses_exact=True,explicit_registered_V8475_Adernkatz_B49_dependency_preserved=True,native_summary=native['summary'],native_controls=controls,native_loaders=loaders,actual_summary=actual['summary'],original_FE=FE,comparison=comparison,actual_scope=scope,editorial_completion_credit_pending_registered_release=True,full_goal_complete=False)

def apply_release(image,baseline,config=CONFIG):
    try:planned,report=plan_release(image,baseline,config)
    except (KeyError,TypeError,IndexError,AssertionError,StopIteration) as exc:
        raise ValueError('Hodram B50 atomic contract: invalid orcontradictory evidence schema: '+str(exc)) from exc
    commit_image(image,planned)
    return report
