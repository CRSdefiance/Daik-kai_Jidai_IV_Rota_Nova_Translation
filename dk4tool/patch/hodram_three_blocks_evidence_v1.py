"""Independently recompute native masks and saved whole-exchange observations before commit."""
import struct
from pathlib import Path
from types import FunctionType
from PIL import Image
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.research_lil_B209_native_pages_v6461 import pages as original_pages
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels as original_pixels
from scripts.prove_lil_B208_name_planes_v6405 import codes,original_name_events
from scripts import lil_B207_name_style_v6354d as style

ARM9='12ebaf3f3ce558e731c4c972ae90696392a351426cf147fbf3bd830dd1d82d1b'
PAGE_ADAPTER='50ad653583e9e808d4141de08033715f52410e27bab98ba335b6b7d8b023e059'
PATH='/data/SC1.DK4'
VERSIONS=('clean_Japanese','revised_English')
COLORS=((0,8,0),(98,97,98),(197,198,197))

def check_evidence(data,rows,parent,reference,result,load,require):
    from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
    inventory,_,_=scoped_inventory();models=data['native_models'];stored=data['native_stored'];names=data['native_names']
    arm,font=parent.read_file('/__arm9__.bin'),parent.read_file('/GRP/KANJI.FNT')
    require(sha(arm)==ARM9==models['ARM9_sha256']==names['ARM9_sha256'] and sha(font)==models['font_sha256'],'exact current native code/font')
    require(reference.read_file('/__arm9__.bin')==arm and reference.read_file('/GRP/KANJI.FNT')==font,'reference retains exact current code/font')
    adapter=models['source_owned_exact_target_page_adapter']
    require(sha(adapter.encode())==PAGE_ADAPTER and adapter==stored['source_owned_target_page_adapter'],'source-locked native page adapter')
    pixels=FunctionType(original_pixels.__code__,{**original_pixels.__globals__,'CURRENT_ARM9':ARM9},argdefs=original_pixels.__defaults__)
    env={**original_pages.__globals__,'expected_pixels':pixels,'codes':codes};exec(compile(adapter,__file__+'::exact-original-native-pages','exec'),env)
    wanted={r['id'] for r in rows};bodyplanes={};bodymasks={}
    require(set(models['native_models'])==set(VERSIONS) and len(wanted)==28,'both complete native body sets')
    for version in VERSIONS:
        listed=models['native_models'][version];require(len(listed)==28 and {r['id'] for r in listed}==wanted,'unique source-qualified native models')
        for row in rows:
            m=next(r for r in listed if r['id']==row['id']);st=next(r for r in stored['records'] if r['id']==row['id'])
            raw=bytes.fromhex(row['source_hex'] if version=='clean_Japanese' else row['final_stored_hex']);text=raw[1:]
            require(raw[0]==row['source_selector']==m['source_selector'] and m['input_hex']==raw.hex() and m['block']==row['block'],'literal source-qualified native input:'+row['id'])
            require(not any(t in text for t in [b'FI',b'FA',b'FO',b'%']),'zero source substitutions remain zero')
            fresh=env['pages'](arm,font,text)
            require(len(fresh['pages'])==len(m['pages'])==1 and m['total_bytes']==fresh['total_bytes']==len(text) and m['complete_consumed_bytes']==fresh['complete_consumed_bytes']==len(text),'complete single-page native consumption')
            page,declared=fresh['pages'][0],m['pages'][0];plane=bytes.fromhex(page['native_plane_hex']);saved=Path(declared['native_plane']).read_bytes()
            require(plane==saved and sha(plane)==declared['native_plane_sha256'],'every recomputed native body pixel:'+row['id'])
            for field in ['page','start','end','consumed_hex','events','first_visible_origin','native_independent_plane_equal','all_bitmap_header_input_canaries_exact']:
                require(page[field]==declared[field],'native glyph/consumption/bounds metadata:'+row['id']+':'+field)
            require([e['code'] for e in page['events'] if e['code']!=32]==[c for c in codes(text) if c not in [32,10]],'all first/internal/final glyphs in source order')
            if version=='revised_English':
                require(st['file_path']==PATH and st['block']==row['block'] and st['source_selector']==row['source_selector'],'stored source-qualified identity')
                require(st['source_reference']==row['source_reference'] and st['predecessor_reference']==row['current_reference'] and st['target_reference']==row['integrated_reference_pending'],'complete stored source/current/final references')
                require(st['compiled_hex']==row['compiled_hex'] and st['stored_hex']==row['final_stored_hex'] and st['expanded_stored_hex']==text.hex(),'complete compiler/stored literal input')
                before=bytes.fromhex(row['current_hex']);compiled=bytes.fromhex(row['compiled_hex']);pad=len(before)%2!=len(compiled)%2
                require(st['compiler_owned_parity_space']==pad and raw==compiled+(b' ' if pad else b''),'compiler-only parity space')
                sp=st['complete_native_stored_proof'];require(len(sp['pages'])==1 and sp['pages'][0]['events']==page['events'] and sp['complete_consumed_bytes']==len(text),'stored native event/consumption binding')
            black={(i%216,i//216) for i,b in enumerate(plane) if b==1};gray={(i%216,i//216) for i,b in enumerate(plane) if b==15}
            cp=pixels(arm,font,[e for e in page['events'] if e['kind']=='cp932']);cpgray={(i%216,i//216) for i,b in enumerate(cp) if b==15}&gray
            bodyplanes[version,row['id']]=plane;bodymasks[version,row['id']]={COLORS[0]:black,COLORS[1]:gray-cpgray,COLORS[2]:cpgray}
    caller=FunctionType(style.style_source_proof.__code__,{**style.style_source_proof.__globals__,'ARM9':ARM9},argdefs=style.style_source_proof.__defaults__)
    raster=FunctionType(style.native_name_raster.__code__,{**style.native_name_raster.__globals__,'style_source_proof':caller},argdefs=style.native_name_raster.__defaults__)
    nameinks={};nameby={n['actor_ID']:n for n in models['name_planes']};approved={r['actor_ID']:r['name'] for r in data['names']['records']}
    require(set(nameby)==set(approved)=={1,2,9,16,18,113} and names['name_planes']==models['name_planes'],'six exact current name consumers')
    for actor,n in nameby.items():
        require(n['text']==approved[actor] and n['input_hex']==n['text'].encode('cp932').hex(),'complete reviewed name input')
        plane,events,usedfont=raster(arm,bytes.fromhex(n['input_hex']));emitted,flushes=original_name_events(events,bytes.fromhex(n['input_hex']))
        require(usedfont==font and plane==pixels(arm,font,events)==Path(n['native_plane']).read_bytes() and sha(plane)==n['native_plane_sha256'],'independent complete native name pixels')
        require(events==n['native_glyph_events'] and emitted==codes(bytes.fromhex(n['input_hex'])) and flushes==n['source_owned_final_zero_ink_flushes'],'complete name glyph order andfinal flush')
        require(n['original_pair_flush_width']==max(e['x']+6 for e in events) and all(e['style']==11 and e['y']==0 and 0<=e['x'] and e['x']+6<=216 for e in events),'original name geometry/style')
        nameinks[actor]={(i%216,i//216) for i,b in enumerate(plane) if b}
    clean=NdsImage.open('work/clean.nds');parentbank=IlnkContainer.parse(parent.read_file(PATH)).blocks
    sourcebanks={'clean_Japanese':IlnkContainer.parse(clean.read_file(PATH)).blocks,'revised_English':IlnkContainer.parse(reference.read_file(PATH)).blocks}
    opening=parentbank[42];initializers,initialtexts=inventory(arm,opening);first=initialtexts[0]['offset'];prelude=opening[8:first]
    require(first==42 and len(prelude)==34 and len([c for c in initializers if c['offset']<first])==8,'eight original Hodram opening initializers')
    fixtures=data['fixtures']['fixtures'];require(len(fixtures)==6,'six complete whole-exchange fixtures')
    complete=0;bodyholds=0;nameholds=0;groups_out=[];frames=0
    for number in [137,45,46]:
        actual=data[f'actual_B{number}'];require(not actual['unresolved'] and len(actual['groups'])==2,'both actual groups withno unresolved observations')
        for group,version in zip(actual['groups'],VERSIONS,strict=True):
            fixture=group['fixture'];require(group['version']==fixture['version']==version and group['block']==fixture['source_block']==number,'exact scene scope')
            require(fixture==next(f for f in fixtures if f['source_block']==number and f['version']==version),'exact complete fixture declaration')
            source=sourcebanks[version][number];end=8+struct.unpack_from('<H',source,4)[0]
            logical=bytearray(opening[:8]+prelude+source[8:end]);struct.pack_into('<H',logical,4,len(logical)-8);block=bytes(logical)+bytes(-len(logical)%4)
            require(block.hex()==fixture['fixture_block_hex'] and sha(block)==fixture['fixture_block_sha256'] and len(block)==fixture['fixture_stored_bytes'],'complete original exchange fixture bytes')
            require(fixture['route']==1 and fixture['fixture_block']==42 and fixture['constant_shift_bytes']==34 and fixture['original_opening_prelude_hex']==prelude.hex(),'exact original initializer/constant-shift context')
            fi=NdsImage.open(fixture['research_ROM']);require(sha(Path(fixture['research_ROM']).read_bytes())==fixture['research_ROM_sha256'],'whole actual fixture ROM')
            checkbank=list(parentbank);checkbank[42]=block;require(fi.read_file(PATH)==IlnkContainer(checkbank).to_bytes(),'only original opening block replaced')
            require(all(fi.read_file(p)==v for p,v in parent.iter_components()) and all(p==PATH or fi.read_file(p)==v for _,p,v in parent.iter_files()),'all unowned fixture files/components exact')
            parsed,texts=inventory(arm,block);require(parsed==fixture['all_fixture_commands'],'native parsed complete fixture commands')
            expected={c['offset']:c for c in parsed};objects={r['fixture_command_offset']:r for r in fixture['all_original_exchange_commands']};records={r['fixture_command_offset']:r for r in fixture['original_text_records']}
            selectedrows=[r for r in rows if r['block']==number];require(len(texts)==len(records)==len(selectedrows),'all source speeches in whole fixture')
            base=Path(f'work/analysis/Hodram_scene_runs_v8280/route1_B{number}_{version}');terminal=load(base/'terminal.json');plan=load(base/'run_plan.json')
            report,trace=load(group['capture_report']),load(group['observer']);framecount={137:24001,45:10001,46:16001}[number]
            require(terminal['terminal'] and terminal['report']==group['capture_report'] and terminal['observer']==group['observer'] and group['actual_frames']==report['frames']==terminal['frames']==plan['frames']==framecount,'terminal capture scope')
            require(sha(Path(group['capture_report']).read_bytes())==terminal['report_sha256'] and sha(Path(group['observer']).read_bytes())==terminal['observer_sha256'],'report/observer integrity')
            require(report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded') and not report['callback_errors'] and not report['goal_complete'] and not report['hardware_device_verification'],'coldboot andexplicit hardware/route limits')
            require(not any(v for k,v in report.items() if k.startswith('synthetic_')) and report['ROM_sha256']==fixture['research_ROM_sha256'],'no forced state inputs')
            schedule=load(plan['inputs']);ordinary=load('work/analysis/hodram_opening_context_v2018/ordinary_Hodram_NewGame_inputs.json')
            require(schedule==ordinary+[dict(start=f,duration=5,buttons=['A']) for f in range(4000,framecount-480,240)] and report['scripted_input_schedule']==schedule,'original unretimed ordinary input schedule')
            require(not trace['errors'] and not trace['mismatches'] and trace['all_host_slots_restored_and_core_file_exact'],'readonly observer/core restoration')
            banks={r:IlnkContainer.parse(fi.read_file(f'/data/SC{r}.DK4')).blocks for r in range(4)};photos={}
            for photo in report['frames_captured']:
                require(sha(Path(photo['path']).read_bytes())==photo['PNG_sha256'],'actual PNG integrity');pic=Image.open(photo['path']).convert('RGB');require(pic.size==(256,384),'original full framebuffer bounds')
                rgb=pic.crop((16,296,232,360)).get_flattened_data();photos[photo['frame']]=(photo,pic,{c:{(i%216,i//216) for i,v in enumerate(rgb) if v==c} for c in COLORS})
            pairs=[];speeches=[];following=[];lastnext=None;normal=None
            for index,row in enumerate(trace['rows']):
                resident=row['source'];require(row['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'] and resident['classification']=='original_SC_cache','observed readonly original cache')
                payload=banks[resident['route']][resident['block']];require(resident['whole_resident_payload_exact_ROM'] and resident['actual_sha256']==resident['registered_sha256']==sha(payload),'whole resident original cache identity')
                require(sha(Path(resident['actual_payload_file']).read_bytes())==sha(payload),'whole resident payload bytes')
                if row['kind']!='after_command':continue
                if normal or (resident['route'],resident['block'])!=(1,42):
                    following.append(dict(frame=row['frame'],route=resident['route'],block=resident['block'],offset=resident['instruction_offset'],word=resident['first_word'],native_result=row['result_words']));continue
                entry=trace['rows'][row['entry_row']];at=entry['source']['instruction_offset'];command=expected[at];word=command['word']
                require(entry['kind']=='before_command' and resident['instruction_offset']==at and resident['first_word']==word,'complete original command entry/return association')
                for seen in [entry,row]:
                    s=seen['source'];require((s['route'],s['block'])==(1,42) and s['actual_sha256']==sha(block) and s['payload_bytes']==len(block) and s['instruction_pointer']==s['payload_address']+at,'complete original fixture payload/PC binding')
                if lastnext is not None:require(at==lastnext,'original next-command/control-flow boundary')
                if word in [0x100,0x200,0x300,0x400]:
                    span=struct.unpack_from('<H',block,at+2)[0];prev=entry['mode'];taken=word==0x100 or word==0x200 and prev==0 or word==0x300 and prev==1 or word==0x400 and prev==2
                    require(row['decoded_length']==4+(span if taken else 0),'observed original relative decision')
                else:require(row['decoded_length']==command['native_extent'],'complete original native command extent')
                lastnext=at+row['decoded_length'];obj=objects.get(at)
                pair=dict(fixture_offset=at,canonical_source_offset=None if obj is None else obj['canonical_clean_offset'],source_command_ordinal=None if obj is None else obj['source_command_ordinal'],word=word,
                    start=entry['frame'],returned=row['frame'],duration=row['frame']-entry['frame'],entry_row=row['entry_row'],return_row=index,decoded_length=row['decoded_length'],observed_previous_result=entry['mode'],
                    native_result=row['result_words'],before_RNG=entry['original_RNG_seed'],after_RNG=row['original_RNG_seed'],UI_before=entry['native_UI_request_words'],UI_after=row['native_UI_request_words'])
                pairs.append(pair)
                if word==0:
                    require(row['decoded_length']==4 and row['result_words']==[0,pairs[-2]['native_result'][1]],'complete normal end retains value word');normal=dict(frame=row['frame'],native_result=row['result_words'],complete_four_byte_end=True)
                if at not in records:continue
                rec=records[at];actor=rec['source_selector'];ident=rec['id'];source_row=next(r for r in selectedrows if r['id']==ident)
                require(actor==source_row['source_selector'] and rec['source_reference']==source_row['source_reference'],'observed source-qualified static actor')
                holds=[];nh=[];partial=[];ink=nameinks[actor];n=nameby[actor];required=bodymasks[version,ident]
                for f,(photo,pic,foundmasks) in photos.items():
                    if not entry['frame']+20<f<row['frame']-4:continue
                    found={(x-16,y-276) for y in range(276,289) for x in range(14,18+n['original_pair_flush_width']) if pic.getpixel((x,y))==COLORS[1]};nameok=found==ink
                    if nameok:nh.append(dict(frame=f,capture=photo['path'],sha256=photo['PNG_sha256']))
                    diffs={str(c):len(foundmasks[c]^required[c]) for c in COLORS}
                    if any(diffs.values()) or not nameok:
                        partial.append(dict(frame=f,body_differences=diffs,name_missing=len(ink-found),name_extra=len(found-ink),not_counted_as_complete=True));continue
                    holds.append(dict(frame=f,capture=photo['path'],sha256=photo['PNG_sha256'],native_page=1,all_black_ASCII_CP932_gray_first_internal_final_glyphs_andname_exact=True,actual_name=n['text']))
                require(holds and nh,'actual complete native body/name hold:'+ident)
                speeches.append(dict(id=ident,source_selector=actor,name=n['text'],start=entry['frame'],returned=row['frame'],pages=1,complete_holds=holds,nameholds=nh,partial_ortransition_samples=partial,selected_capture=holds[-1]))
                observation=next(o for o in source_row['actual_display_observations'] if o['version']==version)
                require(observation['speech']==speeches[-1],'per-record approved actual body/header association:'+ident)
            require(pairs==group['command_pairs'] and speeches==group['speeches'] and following==group['following_original_cache_commands'],'every recomputed selected/following command andspeech observation')
            require(normal==group['normal_return'] and normal is not None and not group['unknown_sources'] and not group['unvisited_conditional_text_IDs'],'all28 selected source speeches andnormal returns')
            complete+=len(speeches);bodyholds+=sum(len(s['complete_holds']) for s in speeches);nameholds+=sum(len(s['nameholds']) for s in speeches);frames+=framecount
            groups_out.append(dict(block=number,version=version,speeches=len(speeches),complete_body_holds=sum(len(s['complete_holds']) for s in speeches),normal_return=normal))
    require((complete,bodyholds,nameholds,frames)==(56,262,262,100006),'all56 source/revised pages/262body-name holds/100006frames')
    return dict(native_paragraphs_recomputed=56,native_names_recomputed=6,actual_speech_observations=complete,complete_body_holds=bodyholds,complete_name_holds=nameholds,actual_frames=frames,groups=groups_out,
        no_new_emulator_runs=True,fixture_scope_not_natural_optional_activation_fullroute_orhardware=True)
