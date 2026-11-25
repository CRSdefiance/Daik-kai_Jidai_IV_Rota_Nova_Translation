"""Registered, fixed-size name metadata after the unchanged code-only bounds layer."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.owned_name_glyph_v1 import plan_arm9_name_glyph
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts.audit_story_glyph_consistency import load

def plan_release(image,config_path):
    config=load(config_path)
    if config['format']!='dk4-registered-owned-name-glyph-v1':raise ValueError('Registered owned-name format required')
    for path,digest in config['dependencies'].items():
        if sha(Path(path).read_bytes())!=digest:raise ValueError('Changed name dependency: '+path)
    if sha(bytes(image.rom.save()))!=config['parent_ROM_sha256']:raise ValueError('Exact complete post-bounds predecessor required')
    doc=load(config['manuscript']);validate_natural_dialogue_batch(doc)
    if len(doc['records'])!=1 or doc['records'][0]['id']!='actor14_surname_normal_F' or doc['records'][0]['english']!='Emilio Ferog':
        raise ValueError('Exact source-reviewed name identity required')
    proposal=load(config['proposal']);native=load(config['native']);actual=load(config['actual'])
    if not native['offline_visual_approved'] or native['proposal_sha256']!=sha(Path(config['proposal']).read_bytes()):raise ValueError('Exact reviewed name native binding required')
    if len(actual['name_headers'])!=7 or not all(r['complete_name_ink_andblank_guards_exact'] and r['label']=='Emilio Ferog' for r in actual['name_headers']):
        raise ValueError('Complete actual name headers required')
    arm,proof=plan_arm9_name_glyph(image.read_file('/__arm9__.bin'),proposal)
    if proof!=native['name_data_plan'] or sha(arm)!=config['target_ARM9_sha256']:raise ValueError('Frozen name data inverse andtarget required')
    return arm,dict(**proof,changed_records=['ACTOR14_SURNAME_NORMAL_ASCII_F'],
        registered_source_reviewed_metadata_only=True,actual_name_headers=7,new_credit=0,
        final_ROM_sha256=config['target_ROM_sha256'])
