"""Seal261 clean-only source meanings/independent drafts before exposing older story English."""
import struct
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.reviewed_choice_object_v2 import labels,count_and_base
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.prepare_rafael_B81_B84_formatting_v1 import string
from translations.rafael_B85_B100_clean_draft_data_v1 import DRAFTS as original
from translations.rafael_B85_B100_clean_draft_data_v2 import DRAFTS,CHOICES

SOURCE=Path('work/analysis/Rafael_B81_B100_clean_20261105/clean_source_packet.json')
ROOT=Path('work/analysis/Rafael_B85_B100_clean_drafts_20261105')
CONTEXT={
85:'Complete conditional return to Gerhard after the first recruitment attempt. A sailor proposes another visit;Rafael goes alone andshows he haslearned. Gerhard admits thatRafael’s words haveweighed onhim,andagrees. The separate refusal choice defers the visit. Do notread both choices aschronological actions orclaim a natural branch activation.',
86:'Complete Charles recruitment fromthe Caribbean tavern explosion through the shipwright’s eager handoff,the factory meeting andCharles’s scientific monologue. Julio suggests rum;Cesare panics andcalculates benefits;Claudio isblunt andJanus reins himin. The shipwright wants Charles elsewhere buttries tosoundhelpful. Charles’s familiar older-man address isnot kinship. His self-absorbed enthusiasm interrupts the actual recruitment question;Rafael finallyextracts ananswer.',
87:'Complete first Zipang encounter:Claudio criticizes hairstyles,Julio counsels respect,thenKurushima’s gang stages abumping extortion. The source’s hostile foreigner address belongs tothe gang,not thenarrator. Yukihisa intervenes,uses theback ofhisblade,apologizes andasks tosailaway. Preserve his restrained formal voice,explicit desire totesthimself asa man,andJapanese given/middle/family introduction without adding rank. Keep the Sun imagery andJulio’s source perspective.',
88:'Complete Silla crown discovery andJulian encounter,including both alternative choices. The party overheard Julian andMeihua inHangzhou andfound thecrown first. One branch givesit tohim undera hastily asserted helping motive;Rafael lateraccepts thesacrifice andClaudio calls himasofttouch. The other saysRafael wants togivethegift himself;Julian infers aromantic rivalry andhurriesoff. This inference isJulian’s,not narrator-confirmed love ornewrelationship.',
90:'Complete Janus daydream andRafael’s promise:Janus admires thevariety ofMediterranean countries,ports andships,andwouldliketo trade there withhisown fleet. Rafael promises thatregion whenhe entrusts himwitharegional fleet;thetiming remains unspecified. Retain thewarm encouragement andJanus’s polite eagerness without inventing animmediate assignment.',
91:'Complete miracle-belief question withalternative outcomes. The man first challenges acaptain’s dependability,Fernando objects,andtheman reveals hiswish togive a miracle-associated bullet pendant toabelieving captain. Hehas asked onehundred people,not onehundredships,andis physically unable to sail. Preserve hisuncertain history:do notinvent hisinjury,cause ofdisability orpersonal shipwreck. Luck andSpirit reward panels aredistinct branches,not cumulative rewards. Refusal dialogue isseparate.',
92:'Complete tomato conversation:Emilio keeps eating andpraising tomatoes,Rafael responds andprivately notes hisappetite,anda trader gives at omato seedling becauseofthepraise. The source says thetrader handles/sells tomatoes,not thathegrows them. Preserve repeated chewing andthe final deadpan thought;do notturn theseedling intoseeds or fruit.',
93:'Complete banana theft,fruitless chase andfood distraction. Three physical FE animal-like cries remain distinct fromordinary nameplated dialogue. Emilio prioritizes hisstolen banana;Rafael notices unfamiliar seeds asapotential discovery,thendistracts himwiththelocal foodspecialty atRafael’s expense. The source doesnot establish anidentified animal speaker oraglobal first botanical discovery.',
95:'Complete Gerhard lost-sword reminiscence. A place recalls hisKatzbalger lost fighting pirates;itsplainappearance belied excellenthandling andlongattachment. Hisfisherman/cheap-sale account isconjecture,notprovenhistory. Rafael offers hopeful reassurance thatsomeone values it;Gerhard’s comfort remains conditional. Preserve nostalgia without inventing recovery orownership transfer.',
97:'Complete runaway-ninja clothing rumor andAngelo/Yukihisa quarrel,including theexplanation ofnukenin andninja. Angelo doesnotknow eitherterm atfirst;Yukihisa explains stealth,exposure/death anddangerous defection. Keep death’s source phrasing without inventing whoexecutes whom. Angelo’s teasing clashes withYukihisa’s formality;Rafael stops both,theyapologize,andreturn tothearmor rumor. Cultural terms,sourceItalian exclamation anddistinct voices remain;native item-name binding ispending.',
100:'Complete amber conversation betweenCharles andtheportworker. Charles’s scientific explanation andenthusiasm contrast withtheworker’s bewilderment,whichprompts arumor aboutanamber-shining place onanoffshore island. Preserve treesap,thebee andthousands-of-years source timescale;do notsubstitute modern geological ages orclaim therumorisconfirmed. Familiar address doesnotmake thembrothers.',
}

def main():
    assert not ROOT.exists();packet=load(SOURCE)
    cleanpath=Path(packet['source_ROM']);assert sha(cleanpath.read_bytes())==packet['source_ROM_sha256']
    clean=NdsImage.open(cleanpath);assert sha(clean.read_file(packet['file_path']))==packet['source_archive_sha256']
    groups=[g for g in packet['groups'] if g['block']>=85]
    assert [g['block'] for g in groups]==list(range(85,101))
    source_rows=[r for g in groups for r in g['records']]
    assert len(source_rows)==255 and sum(len(v) for v in DRAFTS.values())==255
    assert set(CONTEXT)==set(DRAFTS)
    assert all(a[0]==b[0] and a[2]==b[2] for block in original for a,b in zip(original[block],DRAFTS[block],strict=True))
    drafts={f'DK4_MES_B{block}_R{index:04d}':(meaning,english) for block,items in DRAFTS.items() for index,meaning,english in items}
    assert set(drafts)=={r['id'] for r in source_rows}
    previous=load(Path('translations/rafael_B81_B84_contextual_final_review_v1.json'))
    assert not set(drafts)&{r['id'] for r in previous['records']}
    rows=[]
    for source in source_rows:
        row=deepcopy(source);meaning,english=drafts[row['id']]
        assert not row['source_decode_error'] and meaning and english and english==english.strip() and english.isascii()
        assert not any(t in english for t in ['\n','{LB','{ALIGN','{PAD}'])
        assert '  ' not in english
        for macro in ['FI','FA','FO','FU']:
            assert english.count('{MACRO:'+macro+'}')==bytes.fromhex(row['source_hex'])[1:].count(macro.encode()),(row['id'],macro)
        row.update(source_meaning=meaning,english=english,independent_English_draft=english,context=CONTEXT[row['block']],
            kind='system-FE' if row['source_selector']==254 else 'progressive',
            review=dict(source=True,context=True,localization=False,naturalness=False,formatting=False),
            current_English_comparison_pending=True,source_meaning_anddraft_precede_old_English_comparison=True,
            native_name_term_full_preamble_andfresh_display_pending=True,new_credit=0)
        rows.append(row)
    choices=[]
    for group in groups:
        for command in group['all_source_commands']:
            if command['word'] not in [0x2100,0x2200]:continue
            block,at=group['block'],command['offset'];raw=bytes.fromhex(command['whole_command_hex'])
            values=labels(raw);count,base=count_and_base(raw)
            assert (block,at) in CHOICES and len(CHOICES[block,at])==count
            for index,(value,(meaning,english)) in enumerate(zip(values,CHOICES[block,at],strict=True)):
                offset=at+base+struct.unpack_from('<H',raw,2+index*2)[0]
                choices.append(dict(id=f'SC0_B{block}_NATIVE_CHOICE_{at}_{index}',file_path=packet['file_path'],block=block,
                    kind='typed-choice-label',source_index=index,source_command_offset=at,source_command_hex=raw.hex(),
                    source_choice_object_hex=raw.hex(),source_relative_label_offset=offset-at-base,
                    source_byte_offset=offset,source_hex=value.hex(),source_Japanese=value.decode('cp932'),
                    source_reference=dict(file_path=packet['file_path'],block=block,command_offset=at,offset=offset,
                        source_index=index,length=len(value)+1),source_meaning=meaning,english=english,
                    independent_English_draft=english,context=CONTEXT[block],speaker='Rafael/player choice',
                    review=dict(source=True,context=True,localization=False,naturalness=False,formatting=False),
                    earlier_English_unconsulted=True,current_English_comparison_pending=True,
                    native_caption_geometry_selection_anddisplay_pending=True,new_credit=0))
    assert len(choices)==6 and len({r['id'] for r in rows+choices})==261
    # Only names/role metadata is consulted here. It isnot a native getter or
    # display approval,andno earlier English story body is read bythis producer.
    native=load(Path('work/analysis/Rafael330_stored_consumer_inputs_v3_20261105/native_consumer_planes.json'))
    runtime=native['runtime'];snapshot=Path(runtime['snapshot']['path']);ram=snapshot.read_bytes()
    assert sha(ram)==runtime['snapshot']['sha256']
    current=NdsImage.open('out/all_routes_combined_sea22_fleet66_20261105_malloc_candidate.nds')
    arms=[clean.read_file('/__arm9__.bin'),current.read_file('/__arm9__.bin')]
    assert sha(arms[1])==runtime['ARM9_sha256']
    actors=sorted({r['source_selector'] for r in rows}-{254});names=[]
    for actor in actors:
        fields=[]
        for col in [0,4,8]:
            pair=[]
            for arm,buf in zip(arms,[arms[0],ram],strict=True):
                at=struct.unpack_from('<I',arm,0xCDAC0)[0]-BASE+actor*32+col
                pointer=struct.unpack_from('<I',arm,at)[0];value=string(buf,pointer)
                pair.append(dict(field_offset=at,pointer=pointer,hex=value.hex(),text=value.decode('cp932')))
            fields.append(dict(column=col,source=pair[0],current=pair[1]))
        names.append(dict(actor_ID=actor,fields=fields,metadata_only_not_native_name_orrole_approval=True))
    assert len(names)==20
    ROOT.mkdir()
    paths=[SOURCE,Path('translations/rafael_B85_B100_clean_draft_data_v1.py'),
        Path('translations/rafael_B85_B100_clean_draft_data_v2.py'),Path(__file__)]
    save(ROOT/'261_source_meanings_andindependent_drafts_v1.json',dict(format='dk4-independent-clean-source-drafts-v1',
        translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',
        file_path=packet['file_path'],blocks=list(range(85,101)),records=rows+choices,
        source_speeches=255,source_choice_labels=6,typed_choice_objects=3,complete_exchanges=11,
        control_only_blocks=[g['block'] for g in groups if not g['records']],
        clean_source_packet=str(SOURCE),clean_source_packet_sha256=sha(SOURCE.read_bytes()),
        source_ROM=packet['source_ROM'],source_ROM_sha256=packet['source_ROM_sha256'],
        source_archive_sha256=packet['source_archive_sha256'],earlier_English_story_bodies_unconsulted=True,
        only_approved_name_metadata_consulted=True,source_meanings_anddrafts_sealed_before_current_story_extraction=True,
        contextual_comparison_localization_naturalness_andall_display_gates_pending=True,
        no_completion_credit_no_registered_batch_no_ROM_output=True,new_credit=0,guide_photos=False,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in paths}))
    save(ROOT/'20_scoped_name_metadata_andpending_bindings.json',dict(actors=names,
        runtime=runtime,source_components_andcurrent_field_bytes_bound=True,
        actual_getters_headers_andglobal_name_review_not_implied=True,
        concrete_followups=[
            'Actor151 raw Retainer field alreadyhas a prior actual Sailor getter;do notuse rawfields as visible labels.',
            'Actor152 is the former sailor inB91;check actualgetter andother uses before assigning a loyalty/employment label.',
            'Actor158 isKurushima’s henchman inB87;source boss/subordinate relationship isexplicit,not a player retainer.',
            'The ethnic/geographical secondary fields ofgeneric roles arenot automatically spoken speaker labels.',
            'Bind Zipang,Meihua,Silla Gold Crown,bullet pendant,Katzbalger andRunaway Ninja garb against approved native terms.',
            'Keep Charles’s older-man address andtheportworker’s familiar younger-man address nonfamilial.',
        ],new_credit=0))
    print('Sealed255 clean-source speech meanings/drafts plus6 choices across11 complete exchanges;20 name metadata bindings. Comparisons andall display gates pending.')

if __name__=='__main__':main()
