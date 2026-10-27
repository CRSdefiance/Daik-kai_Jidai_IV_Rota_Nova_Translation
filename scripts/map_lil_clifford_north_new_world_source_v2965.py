"""Map six complete Clifford/northern aftermath andNew World exchanges;zero review credit."""
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

ROOT=Path('work/analysis/lil_Clifford_North_New_World_source_v2965');BASE=0x02000000
HISTORY=Path('work/analysis/lil_after_London_inventory_v1913/all336_states_and_original_London_town_eligibility.json')
SPEAKERS={1: 'Hodram', 2: 'Lil Argot', 3: 'Maria', 4: 'Janus Pasar', 6: 'Julio Erneco', 7: 'Christina;historical native catalog Cristina Erneco', 9: 'Camille', 10: 'Xien Yan', 11: 'Jam Jack Ludwyan', 13: 'Cesare;historical native catalog Cesare Tony', 18: 'Charles Jean Rochefort', 22: 'Samwell;historical native catalog Samwell ダ Khan', 27: 'Aziza Nurennahar', 42: 'Vasquez Maldonado;historical native catalog Vasquez デ Maldonado', 28: 'James Clifford', 43: 'Diogo Escante;historical native catalog Diogo デ Escante', 12: 'Yukihisa;historical native catalog Yukihisa Genjo Shiraki', 14: 'Emilio;historical native catalog legacy full-width Ferog', 15: 'Angelo Puccini', 16: 'Gerhard Ardelknatts', 17: 'Al Ferid Shin;native catalog legacy full-width F', 19: 'Carlo Sinat', 20: 'Fernando Dias', 21: 'Ian Dukov', 23: 'Manuel Almeida', 26: 'Julian Lopes', 40: 'Antony Kuhn;historical catalog legacy full-width Fong', 56: 'Georg;Kuhn envoy,historical native catalog partly Japanese surname', 92: 'Barkeep;original class92', 151: 'Generic crew reporter;original Retainer actor151', 254: 'Original FE modal presenter;speaker identified from source prose,not actor254'}
if __name__=='__main__':
    assert not ROOT.exists();ledgerpath=Path('translations/editorial_review_current_v1.json');ledger=read(ledgerpath);candidate=ledger['current_integrated_candidate']
    priorpath=Path('work/analysis/editorial_handoff_verification_v2963b/verified_handoff.json');assert sha(ledgerpath.read_bytes())==read(priorpath)['ledger_sha256']
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
        for number in [67,68,69,149,150,151]:
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
    assert [len(p['records']) for p in packets]==[11,19,14,21,22,56] and len(choice_rows)==0 and len(allrows)==143
    for index,row in enumerate(allrows):row.update(previous_storage_speech=allrows[index-1]['id'] if index else None,next_storage_speech=allrows[index+1]['id'] if index+1<len(allrows) else None,storage_order_not_branch_reachability=True)
    ROOT.mkdir(parents=True)
    save(ROOT/'complete143_clean_current_native_context.json',dict(format='dk4-editorial-source-context-packet-v1',source_ROM='work/clean.nds',source_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),current_ROM=candidate['path'],current_ROM_sha256=candidate['sha256'],current_ARM9_sha256=sha(arm),source_SC2_sha256=sha(clean.read_file('/data/SC2.DK4')),current_SC2_sha256=sha(current.read_file('/data/SC2.DK4')),original_EV2_sha256=sha(ev),
        actual_historical_snapshot=historical['snapshot'],actual_historical_snapshot_sha256=sha(raw),historical_snapshot_ROM=historical['candidate'],historical_snapshot_is_London_not_selected_Clifford_North_New_World_scenes=True,source_exact_spans=[dict(start=a,end=b,sha256=sha(arm[a:b])) for a,b in spans],registered_name_catalog_call_bindings=call_bindings,registered_name_catalog_config=str(name_config),registered_name_catalog_config_sha256=sha(name_config.read_bytes()),speaker_catalog=names,blocks=packets,records=allrows,typed_choice_records=choice_rows,
        total_editorial_objects=143,speech_objects=143,progressive_speeches=140,system_FE_panels=3,typed_choice_labels=0,
        scope='Six complete Lil exchangesSC2B67/B68/B69/B149/B150/B151:Clifford downfall/subordination letters andseparate Proof returns,worldwide trade/homeward suggestion,bamboo puzzle andmap discovery,Clifford NewWorld strategy request,andMaldonado private worries/publictavern confrontation. All143speeches comprise140ordinary andthree originalFEbodies;no typed choices. Original453commands/180relative sites/45predicates andEV2dependencies mapped. Exactclean/currentreferences andfullpreambles remain sourcebound,including0Dordinaryactor13Cesare. Preliminaryhistorical macroprobes staydistinct fromcurrentFE-null dispatch/fonts/actualselectedgameplay. Cataloglegacyglyphs remain evidencewithoutnewname/UI/rank/relationship edits. Completecontext/gloss/prose/native/reference/representative/release reviewstillrequired;zeroeditorialcredit. Fullgoalactive.',
        prior_state_inventory=str(HISTORY),prior_state_inventory_sha256=sha(HISTORY.read_bytes()),source_universe='work/analysis/editorial_source_universe_v2701c/source_universe_inventory.json',source_prose_credit_added=0,completion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    assert sum(len(b['all_clean_native_commands']) for b in packets)==453
    keys={(r['file_path'],r['id']) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['record_keys']}
    assert not keys & {(r['file_path'],r['id']) for r in allrows+choice_rows}
    assert sum(r['kind']=='system-FE' for r in allrows)==3
    print('Six complete Clifford/north/NewWorld exchanges:143speeches,140progressive/3FE,no choices,453commands,286historical macrocontexts. Zeroeditorialcredit.')
