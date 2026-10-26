"""Complete connected Mediterranean and West/East African exchanges, including source predecessors."""
import struct
from pathlib import Path
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC,UC_ARM_REG_R0
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_lessons_v1717 import inventory
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Goods_Mediterranean_source_v2820');BASE=0x02000000
HISTORY=Path('work/analysis/lil_after_London_inventory_v1913/all336_states_and_original_London_town_eligibility.json')
SPEAKERS={2:'Lil Argot',4:'Janus Pasar',6:'Julio Erneco',9:'Camille',13:'Cesare Tony',16:'Gerhard Ardelknatts',17:'Al Ferid Shin;native catalog legacy full-width F',20:'Fernando Dias',76:'Mikhail Volk Letzel',151:'Generic crew reporter;original Retainer actor151',171:'Research student;original actor171'}
if __name__=='__main__':
    assert not ROOT.exists();ledgerpath=Path('translations/editorial_review_current_v1.json');ledger=read(ledgerpath);candidate=ledger['current_integrated_candidate']
    priorpath=Path('work/analysis/editorial_handoff_verification_v2819/verified_handoff.json');assert sha(ledgerpath.read_bytes())==read(priorpath)['ledger_sha256']
    current=NdsImage.open(candidate['path']);clean=NdsImage.open('work/clean.nds');historical=read(HISTORY);history=NdsImage.open(historical['candidate'])
    arm,original=current.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin');oldarm=history.read_file('/__arm9__.bin')
    raw=Path(historical['snapshot']).read_bytes();assert sha(raw)==historical['snapshot_sha256'] and sha(Path(historical['candidate']).read_bytes())==historical['candidate_sha256']
    spans=[(0x24274,0x242C8),(0x242CC,0x24310),(0x24314,0x24330),(0x24334,0x243A0),(0x2A1D8,0x2A530),(0x23840,0x23A28)]
    for a,b in spans:assert arm[a:b]==original[a:b]==oldarm[a:b]==raw[a:b]
    name_stage=read(Path(candidate['path']).with_suffix('.manifest.json'))['relocations']['/__arm9__.bin']['reviewed_name_integration']
    name_config=Path(name_stage['release_config']);assert sha(name_config.read_bytes())==name_stage['release_config_sha256']
    call_bindings=[]
    for at in [0x242C8,0x24310,0x24330]:
        assert arm[at:at+4]==oldarm[at:at+4]==raw[at:at+4] and arm[at:at+4]!=original[at:at+4]
        call_bindings.append(dict(address=BASE+at,clean_original_hex=original[at:at+4].hex(),registered_hex=arm[at:at+4].hex(),owner_module='dk4tool.patch.confirmed_name_message_catalog',preserved_existing_name_catalog_tailcall=True))
    ev=clean.read_file('/data/EV2.DK4');assert current.read_file('/data/EV2.DK4')==history.read_file('/data/EV2.DK4')==ev
    jp=IlnkContainer.parse(clean.read_file('/data/SC2.DK4')).blocks;en=IlnkContainer.parse(current.read_file('/data/SC2.DK4')).blocks
    cpu,get=get_machine(oldarm,raw);actors,captain=get(0xCB184),get(0x7F244);assert captain==get(0x2E58C)==2
    hook=cpu.hook_add(UC_HOOK_CODE,lambda c,a,z,d:c.reg_write(UC_ARM_REG_PC,0x027E0000),begin=BASE+0x242CC,end=BASE+0x242CC)
    packets=[];allrows=[];choice_rows=[];names={}
    try:
        for number in [41,43,44,45,46]:
            source,target=jp[number],en[number];commands,speeches=inventory(original,source);now,spoken=inventory(arm,target)
            shape=lambda rs:[(r['offset'],r['word'],r['native_extent'],r['ancestor_0100_offsets']) for r in rs]
            assert shape(commands)==shape(now)
            rows=[]
            for sequence,(a,b) in enumerate(zip(speeches,spoken,strict=True)):
                ja,at=a['offset']+5,b['offset']+5;source_bytes=source[ja:source.index(b'\0',ja)];value=target[at:target.index(b'\0',at)]
                prefix=source_bytes[0];assert prefix in SPEAKERS and value[0]==prefix
                assert source[ja-5:ja+1]==target[at-5:at+1]==bytes.fromhex('0040ffff00')+bytes([prefix])
                actor_ID=None if prefix==254 else get(0x2434C,prefix);assert prefix==254 or actor_ID==prefix
                actor=actors+0x19E4 if actor_ID in [None,2] else actors+4+32*actor_ID
                if actor_ID is not None:
                    namecpu,nameget=get_machine(oldarm,raw);vt=struct.unpack('<I',namecpu.mem_read(actor,4))[0];fn=struct.unpack('<I',namecpu.mem_read(vt+8,4))[0];ptr=nameget(fn-BASE,actor)
                    names[str(prefix)]=dict(original_actor_ID=actor_ID,original_selector=0x0202434C,editorial_speaker=SPEAKERS[prefix],historical_native_catalog_name=bytes(namecpu.mem_read(ptr,80)).split(b'\0')[0].decode('cp932'),catalog_getter=fn,
                        catalog_style_or_legacy_name_glyphs_not_edited=True)
                expanded=[]
                for label,text in [('clean-Japanese',source_bytes[1:]),('current-English',value[1:])]:
                    cpu.mem_write(0x02660000-16,b'\xA5'*2080);cpu.mem_write(0x02660000,text+b'\0');guard=bytes(cpu.mem_read(0x02660000-16,2080))
                    cpu.mem_write(0x02662000-16,b'\xA5'*4128);call(cpu,0x242C8,(0x02662000,0x02660000,actor),instruction_limit=400000)
                    result=bytes(cpu.mem_read(0x02662000,4096)).split(b'\0')[0]
                    assert bytes(cpu.mem_read(BASE,0x400000))==raw and bytes(cpu.mem_read(0x02660000-16,2080))==guard
                    assert bytes(cpu.mem_read(0x02662000-16,16))==b'\xA5'*16 and bytes(cpu.mem_read(0x02662000+len(result)+1,4095-len(result)))==b'\xA5'*(4095-len(result))
                    expanded.append(dict(version=label,input_hex=text.hex(),output_hex=result.hex(),output_text=result.decode('cp932'),original_macro_ABI_entire4MiB_input_output_guards_exact=True,
                        historical_original_macro_probe_not_current_whole_pipeline_or_display=True,FE_uses_captain_for_macro_probe_not_a_FE_presenter_claim=prefix==254))
                ident=f'DK4_MES_B{number}_R{source[:ja].count(bytes([0])):04d}'
                row=dict(id=ident,file_path='/data/SC2.DK4',block=number,source_record_index=source[:ja].count(bytes([0])),current_record_index=target[:at].count(bytes([0])),source_reference=dict(offset=ja,bytes=len(source_bytes),header_offset=ja-5),current_reference=dict(offset=at,bytes=len(value),header_offset=at-5),source_hex=source_bytes.hex(),current_hex=value.hex(),
                    source_Japanese=source_bytes[1:].decode('cp932'),current_English=value[1:].decode('cp932'),source_complete_preamble_hex=source[ja-5:ja+1].hex(),source_presentation_prefix_hex=f'{prefix:02x}',speaker=SPEAKERS[prefix],original_actor_ID=actor_ID,
                    kind='system-FE' if prefix==254 else 'progressive',native_command_extent=a['native_extent'],ancestor_0100_offsets=a['ancestor_0100_offsets'],spoken_sequence_index=sequence,original_macro_probes=expanded,source_prose_or_completion_credit_added=0)
                rows.append(row);allrows.append(row)
            choices=[]
            for a,b in zip(commands,now,strict=True):
                if a['word']!=0x2100:continue
                versions=[]
                for label,block,command in [('clean',source,a),('current',target,b)]:
                    value=block[command['offset']:command['offset']+command['native_extent']];uc=machine(arm);STREAM,OBJECT=0x02660000,0x02662000
                    uc.mem_write(STREAM-16,b'\xA5'*(len(value)+32));uc.mem_write(STREAM,value);uc.mem_write(OBJECT-16,b'\xA5'*64);uc.mem_write(OBJECT,struct.pack('<3I',0,0,STREAM));before=bytes(uc.mem_read(OBJECT-16,64))
                    call(uc,0x2A3B8,(OBJECT,));assert uc.reg_read(UC_ARM_REG_R0)==2;labels=[]
                    for option in [0,1]:
                        relative=6+struct.unpack_from('<H',value,2+2*option)[0];call(uc,0x2A30C,(OBJECT,option));pointer=uc.reg_read(UC_ARM_REG_R0);assert pointer==STREAM+relative
                        text=bytes(uc.mem_read(pointer,len(value)-relative)).split(b'\0')[0];assert text
                        labels.append(dict(option_index=option,relative_offset=relative,offset=command['offset']+relative,hex=text.hex(),text=text.decode('cp932')))
                    assert bytes(uc.mem_read(OBJECT-16,64))==before and bytes(uc.mem_read(STREAM,len(value)))==value
                    assert bytes(uc.mem_read(STREAM-16,16))==bytes(uc.mem_read(STREAM+len(value),16))==b'\xA5'*16
                    versions.append(dict(version=label,command_offset=command['offset'],command_hex=value.hex(),labels=labels,original_count_pointer_ABI_input_output_guards_exact=True))
                for original_label,current_label in zip(versions[0]['labels'],versions[1]['labels'],strict=True):
                    option=original_label['option_index'];ident=f'DK4_CHOICE_B{number}_C{a["offset"]}_O{option}'
                    choice_rows.append(dict(id=ident,file_path='/data/SC2.DK4',block=number,command_offset=a['offset'],option_index=option,source_reference=dict(offset=original_label['offset'],bytes=len(bytes.fromhex(original_label['hex']))),current_reference=dict(offset=current_label['offset'],bytes=len(bytes.fromhex(current_label['hex']))),
                        source_hex=original_label['hex'],current_hex=current_label['hex'],source_Japanese=original_label['text'],current_English=current_label['text'],source_legacy_NUL_ID=f'DK4_MES_B{number}_R{source[:original_label["offset"]].count(bytes([0])):04d}',kind='typed-choice-label',speaker='Lil Argot;player-selected reply',source_prose_or_completion_credit_added=0))
                choices.append(dict(source_command=a,current_command=b,original_native_label_decoders=versions))
            packets.append(dict(block=number,clean_block_sha256=sha(source),current_block_sha256=sha(target),source_bytes=len(source),current_bytes=len(target),all_clean_native_commands=commands,all_current_native_commands=now,source_current_native_command_shape_exact=True,records=rows,choices=choices,
                original_event_source=historical['all336_original_events'][number],historical_completion_or_dependency_state_not_current_eligibility=True))
    finally:cpu.hook_del(hook)
    assert [len(p['records']) for p in packets]==[15,21,16,25,13] and len(choice_rows)==0 and len(allrows)==90
    for index,row in enumerate(allrows):row.update(previous_storage_speech=allrows[index-1]['id'] if index else None,next_storage_speech=allrows[index+1]['id'] if index+1<len(allrows) else None,storage_order_not_branch_reachability=True)
    empty_jp,empty_en=inventory(original,jp[42]),inventory(arm,en[42]);assert not empty_jp[1] and not empty_en[1] and not any(c['word']==0x2100 for c in empty_jp[0]) and jp[42]==en[42]
    terminology={}
    for path,key in [('translations/city_help_manuscript_v1.json','HELP_TOPIC_194'),('translations/item_interface_manuscript_v1.json','ITEM_CATEGORY_00'),('translations/town_trade_port_contextual_editorial_manuscript_v3.json','COMMON_MESSAGE_654')]:
        data=read(path);row=next(r for r in data['records'] if r['id']==key);terminology[key]=dict(path=path,sha256=sha(Path(path).read_bytes()),record=row)
    ROOT.mkdir(parents=True)
    save(ROOT/'source_item_terminology_and_empty_B42_context.json',dict(terminology=terminology,selected_dialogue_term='source item',selected_trade_location_term='Market',inventory_Local_Product_category_reconciliation_lead_uncredited=True,empty_B42=dict(clean_current_sha256=sha(jp[42]),bytes=len(jp[42]),clean_commands=empty_jp[0],current_commands=empty_en[0],speech_objects=0,choice_objects=0),not_editorial_orcompletion_credit=True,full_goal_complete=False))
    save(ROOT/'complete90_clean_current_native_context.json',dict(format='dk4-editorial-source-context-packet-v1',source_ROM='work/clean.nds',source_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),current_ROM=candidate['path'],current_ROM_sha256=candidate['sha256'],current_ARM9_sha256=sha(arm),source_SC2_sha256=sha(clean.read_file('/data/SC2.DK4')),current_SC2_sha256=sha(current.read_file('/data/SC2.DK4')),original_EV2_sha256=sha(ev),
        actual_historical_snapshot=historical['snapshot'],actual_historical_snapshot_sha256=sha(raw),historical_snapshot_ROM=historical['candidate'],historical_snapshot_is_London_not_selected_Goods_Mediterranean_scenes=True,source_exact_spans=[dict(start=a,end=b,sha256=sha(arm[a:b])) for a,b in spans],registered_name_catalog_call_bindings=call_bindings,registered_name_catalog_config=str(name_config),registered_name_catalog_config_sha256=sha(name_config.read_bytes()),speaker_catalog=names,blocks=packets,records=allrows,typed_choice_records=choice_rows,
        total_editorial_objects=90,progressive_speeches=90,system_FE_panels=0,typed_choice_labels=0,
        scope='Five complete original exchanges:SC2B41polderofficecompletion/fundingpromise,B43source-item/new-specialtyexplanation,B44Mediterraneanreturnplans andCamilleinitiative alternatives,B45Hayreddindownfall/subordination/crew/mapvariants,andB46Pashadownfall/subordination/treasurevariants. Event41requires40and44requires43. SourceB42has no4000speech or2100choice andis separatelyboundedtechnicalcontext,notneweditorialcredit. All90ordinaryspeech objects includeallstoredalternatives;thereare noFEpanels orchoiceobjects. Complete0040ffff00plusprefix bindsoriginalselectors2/4/6/9/13/16/17/20/76/151/171;source4Cis executableMikhailstate,notgenerallystrippedASCII-L. Nativecatalogstrings arehistoricalgetter evidence,notnewobservednameplates orauthoritytorename people. Selfreferencewiseolderfellow andmerchantoyaji do notinventkinship. Generic151andResearchStudent171do notimplynewranks oruniquereusedNPCidentities. All273nativecommands are mapped,including128relative sites and32original8000/8100predicates. Source/current shapes andEV2are exact;threeregisterednamecatalog tailcalls remainowned. All180historical macrocontexts preserveABI/whole4MiB/input-outputguards incopiedLondonstate;no currentfont/GPU/sceneactivation isclaimed. B43原産物means specialty-producing sourceitems,distinct fromordinaryraw-materialcommodities;followcurrenthelpSourceItems andMarket usage. Theitem-only LocalProduct category isretainedas separatelylogged terminology-reconciliation lead,notnewcompletioncredit. Do notaddthehelp-onlyfive-specialtylimit intoaspeechthatdoesnotstateit. Preservewhobrings/surrendersanitem,playerchoice,regionsuitability/multiplepotentialtowns,otherfactionsabilitytotrade,andmarketshare/opportunitycost reasoning withoutinventingliteralexclusiveitemownership. B44specifiesAfricaandIndia,notAsia;explicitMediterraneandestinations andalternativereturn/challenge proposals remainseparate. Mikhailselfpraise,Fernandoconfidence/insight,Gerhardmeasuredassessment andLil/Camillepublic-privatevoices staydistinct. Poldergift is400000currencygold,surprisedstudentremainsfirstperson,andfurtherinvestment/fundraisingisfutureintent,notearnedprogress. Hayreddin/Pashafactiondestruction andsubordination variants do notmeanallindividualsdied;rumor,appearances,qualifiedstrengthcomparison anduncertaintyabouttreasure/armor stayqualified. CrewcredittoLil leadership andGerhardrespect/personalappeal arenotextratitularranks ornewromance. Lil manly-face observations areprivate anddo notprove a relationship. SourceFI/FOmacrosandallcompletepreambles remainexact. WiderKuhninvitation/backstory arcs remainopenafterthesefivecompleteexchanges. Allfreshsource/prose,currentnativeformatting,references,representative andregisteredreleasegates remainrequired.',
        prior_state_inventory=str(HISTORY),prior_state_inventory_sha256=sha(HISTORY.read_bytes()),source_universe='work/analysis/editorial_source_universe_v2701c/source_universe_inventory.json',source_prose_credit_added=0,completion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    assert packets[0]['original_event_source']['must_be_completed']==[40] and packets[2]['original_event_source']['must_be_completed']==[43]
    assert sum(len(b['all_clean_native_commands']) for b in packets)==273
    print('Five complete polder/source-item/Mediterranean exchanges:90progressive speeches,273commands,180historical macrocontexts;noFEorchoices. Zeroeditorialcredit.')
