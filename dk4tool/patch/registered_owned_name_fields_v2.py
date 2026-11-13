"""Registered fixed-slot name fields after all immutable existing release stages."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.owned_name_fields_v2 import plan_arm9_name_fields
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load

def plan_release(image,config_path):
    config=load(config_path)
    def require(ok,message):
        if not ok:raise ValueError('Registered name fields: '+message)
    require(config['format']=='dk4-registered-owned-name-fields-v2','registered field schema')
    for path,digest in config['dependencies'].items():require(sha(Path(path).read_bytes())==digest,'changed dependency: '+path)
    require(sha(bytes(image.rom.save()))==config['parent_ROM_sha256'],'exact complete predecessor')
    clean_path=Path(config['clean_ROM']);require(sha(clean_path.read_bytes())==config['clean_ROM_sha256'],'clean Japanese input')
    doc,proposal,native,actual=[load(config[k]) for k in ['manuscript','proposal','native','actual']]
    validate_natural_dialogue_batch(doc)
    require(native['offline_visual_approved'] and not native['direct_view_pending'] and native['proposal_sha256']==sha(Path(config['proposal']).read_bytes()),'reviewed exact native proposal')
    require(len(doc['records'])==len(proposal['fields'])==len(config['actual_policy']),'whole reviewed field membership')
    versions={v['version']:v['names']['rows'] for v in native['versions']}
    changes=[]
    for row,field,policy in zip(doc['records'],proposal['fields'],config['actual_policy'],strict=True):
        require(row['owned_field']==field and policy['actor']==field['actor'],'individual source andfield binding')
        proposed={r['consumer']:r['text'] for r in versions['proposed'] if r['actor_ID']==field['actor']}
        current={r['consumer']:r['text'] for r in versions['current'] if r['actor_ID']==field['actor']}
        require(row['english']==proposed['full-catalogue']==policy['full_name'],'reviewed complete full-name spelling')
        if policy['kind']=='changed-progressive-name':
            found=[r for r in actual['name_headers'] if r['label']==proposed['progressive-nameplate'] and r[policy['complete_header_key']]]
            require(len(found)>=policy['minimum_headers']>0,'complete actual changed progressive name')
        elif policy['kind']=='unchanged-progressive-middle-component':
            require(field['column']==8 and current['progressive-nameplate']==proposed['progressive-nameplate'] and row['full_catalogue_UI_unvisited'] and actual['Samwell_full_catalogue_UI_unvisited'],'honest distinct full-name-only offline coverage')
        else:raise ValueError('Unqualified name consumer policy')
        changes.append(f'ACTOR{field["actor"]}_NAME_COLUMN{field["column"]}_LOCALIZED')
    arm,proof=plan_arm9_name_fields(image.read_file('/__arm9__.bin'),proposal,NdsImage.open(clean_path).read_file('/__arm9__.bin'))
    require(proof==native['name_data_plan'] and sha(arm)==config['target_ARM9_sha256'],'frozen native inverse andtarget')
    require(arm==Path(native['proposed_ARM9']).read_bytes(),'exact tested name data')
    return arm,dict(**proof,changed_records=changes,registered_source_reviewed_metadata_only=True,new_credit=0,final_ROM_sha256=config['target_ROM_sha256'])
