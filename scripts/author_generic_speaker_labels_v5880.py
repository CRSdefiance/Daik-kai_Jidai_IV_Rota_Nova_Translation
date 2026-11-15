"""Bind three whole-context label revisions to exact clean/current primary fields."""
import struct
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.generic_speaker_label_data_v1 import BASE,POOL,TABLE,SOURCE,EXPECTED,cstring,transform
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/generic_speaker_labels_author_v5880')
DOC=Path('translations/generic_speaker_labels_manuscript_v1.json')
PARENT=Path('out/all_routes_combined_v5872_candidate.nds')
PAIR=Path('work/analysis/couple_context_review_v5775/five_whole_source_contexts_paired_label_draft_and_B199_name_fields.json')
ANON=Path('work/analysis/lil_B200_comparison_v5838/complete_clean_context_source_scene_names_role_label_and_terms.json')
if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists();pair,anon=read(PAIR),read(ANON);prior=read('work/analysis/editorial_handoff_verification_v5878/verified_handoff.json')
    assert sha(PARENT.read_bytes())==prior['candidate_sha256']
    assert pair['manual_review_scope']==dict(complete_representative_exchanges=5,complete_representative_speeches=212,distinct_role_utterances=27,all581_manually_reread=False)
    assert len(anon['source_role_exact_cross_route_copies'])==4 and anon['explicit_not_a_doctor_denial_preserved']
    image,clean=NdsImage.open(PARENT),NdsImage.open('work/clean.nds');arm,original=image.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin')
    assert sha(arm)==SOURCE;payload=bytes(MainCodeFile(arm,BASE).sections[3].data[:-48]);assert arm.count(payload)==1;raw_at=arm.index(payload)
    rows=[]
    for ident in [164,165,172]:
        japanese,current,english=EXPECTED[ident];field=TABLE+ident*32;parts=[]
        for delta in [0,4,8]:
            p=struct.unpack_from('<I',original,field+delta)[0]
            if p:
                raw=cstring(original,p-BASE);parts.append(dict(pointer_field=field+delta,pointer=p,storage_offset=p-BASE,terminated_hex=raw.hex(),Japanese=raw[:-1].decode('cp932')))
            else:parts.append(dict(pointer_field=field+delta,null=True))
        assert parts[0]['Japanese']==japanese;pointer=struct.unpack_from('<I',arm,field)[0];at=pointer-POOL;old=cstring(payload,at)
        assert old==current.encode()+b'\0'
        if ident in [164,165]:
            earlier=next(r for r in pair['paired_nameplate_decisions'] if r['actor_ID']==ident);assert earlier['proposed_English']==english
            note=earlier['rationale']+' Preserve gender and anonymity. This revises the label only;all relationship-bearing dialogue and the earlier literal-label rationale remain intact.'
            context='Five complete representative source exchanges: Ian tavern observers,Fernando\'s distant breakup,tea purchase request,cold/fur conversation and Mikhail conversation without the woman\'s partner.212 representative speeches/27 distinct role utterances;do not claim all581 surrounding route speeches manually read.'
            meaning='Unnamed '+('male' if ident==164 else 'female')+' member of the source couple role. The label identifies the speaker;marriage,age and a permanent relationship form are not established.'
        else:
            earlier=anon['actor172_label_localization_draft'];assert earlier['proposed']==english
            note=earlier['reason']+' Preserve source secondary アフリカ水夫 as metadata without silently promoting it to the displayed label. The full exchange denies that Carlo is a doctor.'
            context=anon['complete_exchange_progression']+' All four directly found route copies contain the same complete19 speeches and native commands;only SC3 header byte2 differs.'
            meaning='Anonymous person found collapsed at the port,then conscious and conversing at an inn. The source trigger is explained in the exchange;the label must remain natural during recovery.'
        rows.append(dict(id=f'ACTOR_{ident:03d}_PRIMARY_SPEAKER_LABEL',actor_ID=ident,source_Japanese=japanese,source_meaning=meaning,
            source_reference=dict(source_file='/__arm9__.bin',pointer_field=field,pointer=parts[0]['pointer'],terminated_hex=parts[0]['terminated_hex']),
            all_three_source_name_fields=parts,current_English=current,
            current_reference=dict(source_file='/__arm9__.bin',pointer_field=field,runtime_pointer=pointer,staged_payload_offset=at,file_offset=raw_at+at,terminated_hex=old.hex()),
            english=english,speaker='Anonymous speaker label',context=context,localization_note=note,editorial_decision='revise',target_locale='en-US',
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            target_native_getter_substitution_glyph_display_and_registered_release_pending=True,new_dialogue_completion_credit=0,new_name_completion_credit=0))
    target,plan=transform(arm,original,rows);ROOT.mkdir(parents=True);binary=ROOT/'three_label_ARM9_RESEARCH_ONLY.bin';binary.write_bytes(target)
    evidence={str(p):sha(p.read_bytes()) for p in [PAIR,ANON,Path('scripts/review_couple_context_v5775.py'),Path('scripts/compare_lil_B200_exchange_v5838.py'),Path('dk4tool/patch/generic_speaker_label_data_v1.py'),Path(__file__)]}
    save(DOC,dict(format='dk4-generic-speaker-label-localization-manuscript-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',records=rows,
        current_ROM=str(PARENT),current_ROM_sha256=sha(PARENT.read_bytes()),source_ROM='work/clean.nds',source_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),
        current_ARM9_sha256=sha(arm),clean_ARM9_sha256=sha(original),current_COMMON_sha256=sha(image.read_file('/COMMON/MESFILE.DK4')),
        target_ARM9=str(binary),target_ARM9_sha256=sha(target),data_plan=plan,whole_context_evidence=evidence,
        source_context_localization_naturalness_approved_native_format_and_release_pending=True,
        source_naming_metadata_and_all_previous_manuscripts_preserved=True,all207_name_review_scope_remains_open=True,
        no_duplicate_story_dialogue_credit=True,new_name_completion_credit=0,full_goal_complete=False))
    save(ROOT/'three_source_owned_label_drafts_and_exact_data_plan.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        target_ARM9=str(binary),target_ARM9_sha256=sha(target),plan=plan,evidence=evidence,new_ROMs=0,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('Three source-owned label drafts:Man/Woman/Stranger. Only owned string prefixes change;621 pointer fields and all code,allocation,wrapper and other name metadata remain exact. Native/display/release pending;no credit.')
