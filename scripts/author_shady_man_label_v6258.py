"""Bind the full eight-exchange editorial decision to one exclusively owned primary string."""
import struct
from copy import deepcopy
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.shady_man_label_data_v1 import BASE,POOL,TABLE,SOURCE,cstring,transform
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/shady_man_label_author_v6258');DOC=Path('translations/shady_man_label_manuscript_v1.json')
PARENT=Path('out/all_routes_combined_v6220_candidate.nds');PROPOSAL=Path('translations/earring_speaker_names_editorial_proposal_v1.json')
if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists()
    proposal=read(PROPOSAL);prior=read('work/analysis/editorial_handoff_verification_v6256/verified_handoff.json')
    assert sha(PARENT.read_bytes())==proposal['current_ROM_sha256']==prior['candidate_sha256']
    assert proposal['all_eight_direct_seller_source_exchanges_read_as_complete_exchanges'] and proposal['complete_seller_context_speeches_read']==195
    selected=next(r for r in proposal['records'] if r['actor_ID']==173)
    assert selected['proposed_progressive_nameplate']==selected['proposed_full_catalogue_name']=='Shady Man'
    image,clean=NdsImage.open(PARENT),NdsImage.open('work/clean.nds');arm,original=image.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin')
    assert sha(arm)==SOURCE
    payload=bytes(MainCodeFile(arm,BASE).sections[3].data[:-48]);assert len(payload)==123264 and arm.count(payload)==1
    raw_at=arm.index(payload);ident=173;field=TABLE+ident*32;parts=[]
    for delta in [0,4,8]:
        p=struct.unpack_from('<I',original,field+delta)[0]
        if p:
            raw=cstring(original,p-BASE);parts.append(dict(pointer_field=field+delta,pointer=p,storage_offset=p-BASE,terminated_hex=raw.hex(),Japanese=raw[:-1].decode('cp932')))
        else:parts.append(dict(pointer_field=field+delta,null=True))
    assert parts[0]['Japanese']=='怪しい人' and parts[1]['Japanese']=='アラブ水夫' and parts[2]['null']
    pointer=struct.unpack_from('<I',arm,field)[0];at=pointer-POOL;old=cstring(payload,at);assert old==b'Suspicious Person\0'
    row=dict(id='ACTOR_173_PRIMARY_SPEAKER_LABEL',actor_ID=ident,source_Japanese='怪しい人',source_meaning=selected['source_primary_meaning'],
        source_reference=dict(source_file='/__arm9__.bin',pointer_field=field,pointer=parts[0]['pointer'],terminated_hex=parts[0]['terminated_hex']),
        all_three_source_name_fields=parts,current_English='Suspicious Person',
        current_reference=dict(source_file='/__arm9__.bin',pointer_field=field,runtime_pointer=pointer,staged_payload_offset=at,file_offset=raw_at+at,terminated_hex=old.hex()),
        english='Shady Man',speaker='Anonymous recurring seller,actor173',
        context='Eight complete clean Japanese seller exchanges:SC0B208/B218,SC1B200/B210,SC2B196/B206,SC3B169/B179.195 complete speeches include112 actor173 speeches. Four haggling scenes and four legendary ceramic-earring pitches establish the dubious qualifier. Every earring ending explicitly saysあの男. Unused secondaryアラブ水夫 is metadata,not a displayed occupation/nationality.',
        localization_note=selected['localization_note'],editorial_decision='revise',target_locale='en-US',review=deepcopy(selected['review']),
        target_native_getter_substitution_glyph_display_and_registered_release_pending=True,new_dialogue_completion_credit=0,new_name_completion_credit=0)
    target,plan=transform(arm,original,[row]);ROOT.mkdir(parents=True);binary=ROOT/'one_label_ARM9_RESEARCH_ONLY.bin';binary.write_bytes(target)
    evidence={str(p):sha(p.read_bytes()) for p in [PROPOSAL,Path('work/analysis/earring_seller_Cristina_names_v6241/four_route_seller_full_exchanges_and_explicit_Cristina_spelling_census.json'),Path('dk4tool/patch/shady_man_label_data_v1.py'),Path(__file__)]}
    save(DOC,dict(format='dk4-shady-man-label-localization-manuscript-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',records=[row],current_ROM=str(PARENT),current_ROM_sha256=sha(PARENT.read_bytes()),source_ROM='work/clean.nds',source_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),current_ARM9_sha256=sha(arm),clean_ARM9_sha256=sha(original),current_COMMON_sha256=sha(image.read_file('/COMMON/MESFILE.DK4')),target_ARM9=str(binary),target_ARM9_sha256=sha(target),data_plan=plan,whole_context_evidence=evidence,source_context_localization_naturalness_approved_native_format_and_release_pending=True,source_naming_metadata_and_all_previous_manuscripts_preserved=True,all207_name_review_scope_remains_open=True,no_duplicate_story_dialogue_credit=True,new_name_completion_credit=0,full_goal_complete=False))
    save(ROOT/'one_source_owned_label_draft_and_exact_data_plan.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),plan=plan,evidence=evidence,new_ROMs=0,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('Shady Man exact owned primary prefix prepared. All621 pointers,secondary/middle fields,5 sections and other bytes exact;native/display/release pending.')
