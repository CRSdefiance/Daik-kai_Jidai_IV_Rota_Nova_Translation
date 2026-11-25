"""Independently execute original menu providers andverify actual owned backing/complete visible caption/highlight pixels."""
from pathlib import Path
from types import SimpleNamespace
from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from PIL import Image
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.main_pool_cache_visibility import BASE,POOL
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.hodram_B49_choices_v2 import compile_choices
from dk4tool.patch.hodram_B49_native_guards_v1 import trusted_adapter
from scripts import verify_ship_advice_choice_centering_20261022 as original
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.trace_file_ids_v683 import mapped_read
from scripts.square_shopkeeper_font_oracles_v7020 import PROGRESSIVE_ORACLE_SOURCE
from scripts.verify_name_catalog_glyphs_v278 import expected_pixels as original_expected
from scripts.prove_lil_B208_name_planes_v6405 import codes

def check_menu_actual(data,doc,parent,clean,load,require):
    declared=data['menu_actual'];actual=data['tail_actual'];provider=data['menu_provider']
    require(not declared['unresolved'] and not actual['unresolved'],'actual menu/body proofs have no unresolved cases')
    arm,font=parent.read_file('/__arm9__.bin'),parent.read_file('/GRP/KANJI.FNT')
    sections=MainCodeFile(arm,BASE).sections;payload=bytes(sections[3].data[:-48]);require(len(payload)==123264,'exact current menu staged payload')
    owners=[*sections,SimpleNamespace(ramAddress=POOL,data=payload)];executed=set()
    def machine(value):
        require(value==arm,'exact current menu runtime');cpu=original.machine(value)
        def exact(u,pc,size,unused):
            hits=[s for s in owners if s.ramAddress<=pc and pc+size<=s.ramAddress+len(s.data)]
            require(len(hits)==1,'unique original menu instruction owner');s=hits[0];offset=pc-s.ramAddress
            require(bytes(u.mem_read(pc,size))==bytes(s.data[offset:offset+size]),'every executed original menu instruction byte');executed.add(pc)
        cpu.hook_add(UC_HOOK_CODE,exact);return cpu
    env={**original.__dict__,'machine':machine};adapter=trusted_adapter('menu_VM',provider['source_owned_VM_adapter'])
    exec(compile(adapter,__file__+'::trusted-original-menu-provider','exec'),env)
    inventory,_,_=scoped_inventory();tables={}
    for version,image in [('clean-Japanese',clean),('current-padded-English',parent)]:
        commands,_=inventory(arm,IlnkContainer.parse(image.read_file('/data/SC1.DK4')).blocks[49]);menus=[c for c in commands if c['word']==0x2100]
        require(len(menus)==1,'one original source/current menu');tables[version]=bytes.fromhex(menus[0]['whole_command_hex'])
    tables['reviewed-stored-English']=compile_choices(doc['typed_choice_records']);require(len(tables['reviewed-stored-English'])==22,'exact original-count compiled22byte menu')
    native_VM={}
    require([v['version'] for v in provider['versions']]==list(tables),'exact source/current/reviewed menu versions')
    for version,table in tables.items():
        record=next(v for v in provider['versions'] if v['version']==version);require(record['object_hex']==table.hex() and record['object_bytes']==len(table),'independent full native menu table:'+version)
        require(len(record['cases'])==2,'both even native menu alignments')
        for alignment,case in zip([0,2],record['cases'],strict=True):
            result=env['choice_vm'](arm,table,alignment)
            require(case['alignment']==alignment and case['native_VM']==result,'every native provider/rectangle/three bridged returns:'+version)
            require([(r['modal_selection'],r['VM_state']) for r in result['VM_cases']]==[(0,2),(1,2),(-1,0)],'original menu modal-result mapping')
        native_VM[version]=result
    require(native_VM['clean-Japanese']['minimum_width_units']==native_VM['reviewed-stored-English']['minimum_width_units']==10,'source andtarget native60px caption widths')
    require(declared['source_owned_independent_oracle']==PROGRESSIVE_ORACLE_SOURCE,'exact independent native CP932/ASCII font oracle')
    oe={**original_expected.__globals__,'WIDTH':256,'HEIGHT':36};exec(compile(PROGRESSIVE_ORACLE_SOURCE,__file__+'::independent-owned-caption-font','exec'),oe);oracle=oe['expected_pixels']
    results=[];off=[]
    for group in actual['groups']:
        version,choice=group['version'],group['choice'];root=Path('work/analysis/Hodram_B49_tail_runs_v8416')/f'route1_{version}_{choice}';terminal=load(root/'terminal.json');op=Path(terminal['menu_observer']);owner=load(op)
        require(sha(op.read_bytes())==terminal['menu_observer_sha256'] and not owner['errors'] and not owner['mismatches'] and owner['all_host_slots_restored_and_core_file_exact'] and owner['read_only_argument_observation_not_emulated_code_or_memory_edit'],'actual readonly original caption owner')
        report=load(group['capture_report']);photos={p['frame']:p for p in report['frames_captured']};labels=group['fixture']['original_menu_records'];width=60
        v='clean-Japanese' if version=='clean_Japanese' else 'reviewed-stored-English';vm=native_VM[v];rect=vm['native_menu_rectangle']
        require(rect[1:4:2]==[64,128] and rect[2]-rect[0]==width+32 and vm['labels']==[l['label'] for l in labels],'fresh original rectangle/complete ordered labels')
        pair=group['actual_menu_pair'];selected=0 if choice=='accept' else 1
        require(pair['native_result']==[2,selected] and group['normal_return']['native_result']==[0,selected],'actual controller selection andnormal carry')
        active=[r for r in owner['rows'] if pair['start']<=r['frame']<=pair['returned']];excluded=[r for r in owner['rows'] if r not in active]
        require(active and all(r['context_words'][3]==84 and r['text']=='All right.' and r['frame']>group['normal_return']['frame'] for r in excluded),'later identical sailing caption rows explicitly separated')
        pointers={r['backing_pointer'] for r in active};require(len(pointers)==1,'one actual B49 backing owner');pointer=next(iter(pointers));bindings=[]
        for r in active:
            i=next(l['option_index'] for l in labels if l['label_hex']==r['text_hex'])
            require(r['PC']==0x020D5340 and r['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'],'original caption PC/readonly callback')
            require(r['context_words'][3:5]==[width,12] and r['context_words'][12]==8 and r['view_words'][7:9]==[0,i*12] and r['view_words'][10:12]==[width,12],'actual caption context/view/style geometry')
            require(r['bitmap_header_words'][:3]==[4,64,36] and r['backing_bytes']==4608 and r['backing_pointer']==r['bitmap_header_address']+r['bitmap_header_words'][4],'actual typed256x36 backing descriptor/pointer')
            require(sha(Path(r['backing']).read_bytes())==r['backing_sha256'],'whole readonly owner backing capture')
            bindings.append(dict(frame=r['frame'],option_index=i,logical_view=[width,12],source_view_origin=[0,i*12],style=8))
        events=[];label_masks=[]
        for label in labels:
            raw=bytes.fromhex(label['label_hex']);i=label['option_index'];points=codes(raw);text_width=sum(6 if c<128 else 12 for c in points);x=(width-text_width)//2
            one=[dict(kind='ascii' if c<128 else 'cp932',code=c,style=8,x=x+sum(6 if v<128 else 12 for v in points[:j]),y=i*12) for j,c in enumerate(points)];events.extend(one)
            plane=oracle(arm,font,[dict(e,y=0) for e in one],canvas_height=12);mask={(j%256,j//256) for j,b in enumerate(plane) if b}
            require(all(0<=xx<width and 0<=yy<12 for xx,yy in mask),'every complete native caption glyph fits its owned view');label_masks.append(mask)
        expected=oracle(arm,font,events,canvas_height=36);owned=[y*256+x for y in range(24) for x in range(width)];owned_set=set(owned);expected_owned=bytes(expected[i] for i in owned)
        sp=Path(terminal['readonly_menu_snapshots']);require(sha(sp.read_bytes())==terminal['readonly_menu_snapshots_sha256'],'whole held menu snapshot metadata');snapshots=load(sp)
        require([s['frame'] for s in snapshots]==[4310,4370,4430],'exact original pre/post-DOWN held samples');samples=[]
        for s in snapshots:
            frame=s['frame'];require(pair['start']<frame<pair['returned'] and s['all_CPU_WRAM_DTCM_ITCM_andconfiguration_exact_before_after_readonly_export'],'held snapshot original menu interval/readonly export')
            regions={}
            for name,ref in s['files'].items():
                raw=Path(ref['path']).read_bytes();require(len(raw)==ref['bytes'] and sha(raw)==ref['sha256'],'complete held original menu region:'+name);regions[name]=raw
            packed=mapped_read(regions['WRAM'],regions['DTCM'],s['DTCM_base'],pointer,4608);pixels=bytes(v for b in packed for v in [b&15,b>>4]);actual_owned=bytes(pixels[i] for i in owned)
            require(actual_owned==expected_owned,'every actual owned caption pixel equals independent glyphs')
            unowned=sum(pixels[i]!=expected[i] for i in range(len(pixels)) if i not in owned_set)
            photo=photos[frame];require(sha(Path(photo['path']).read_bytes())==photo['PNG_sha256'],'whole actual menu PNG')
            pic=Image.open(photo['path']).convert('RGB');selection=1 if choice=='decline' and frame>4355 else 0;x=rect[0]+16;require(x==(256-width)//2,'native original horizontal caption origin');cases=[]
            for i,ink in enumerate(label_masks):
                y=192+rect[1]+16+20*i
                actual_black={(xx-x,yy-y) for yy in range(y-1,y+13) for xx in range(x-2,x+width+2) if pic.getpixel((xx,yy))==(8,8,8)}
                require(actual_black==ink,'all actual first/internal/final caption glyphs andblank guards')
                cyan={(xx,yy) for yy in range(y-4,y+16) for xx in range(x,x+width) if pic.getpixel((xx,yy))==(0,165,172)}
                positions={(xx,yy) for yy in range(y-4,y+16) for xx in range(x,x+width)}-{(x+xx,y+yy) for xx,yy in ink};visible=bool(cyan)
                require((cyan==positions and i==selection) or not cyan,'only complete original selected highlight pixels')
                color=(0,165,172) if visible else (205,198,180);require(all(pic.getpixel(p)==color for p in positions),'all native background/glyph guard pixels')
                cases.append(dict(option_index=i,label=labels[i]['label'],caption_origin=[x,y],caption_size=[width,12],full_visible_black_glyph_mask_andblank_guards_equal=True,exact_native_background_pixels_equal=True,selected_highlight_visible=visible,selected=i==selection))
            samples.append(dict(frame=frame,selected_option_index=selection,visible_selected_option_index=next((c['option_index'] for c in cases if c['selected_highlight_visible']),None),actual_owned_pixels_sha256=sha(actual_owned),independent_owned_pixels_sha256=sha(expected_owned),actual_full_physical_plane_sha256=sha(pixels),unowned_physical_differences=unowned,no_claim_that_unowned_backing_is_blank_oridentical=True,capture=photo,labels=cases))
        observed=next(g for g in declared['groups'] if (g['version'],g['choice'])==(version,choice))
        require(observed['caption_owner_bindings']==bindings and observed['samples']==samples and observed['all_owner_rows']==owner['rows'] and observed['excluded_later_nonB49_Allright_caption_rows']==excluded,'every independently recomputed owner/surface/visible label/highlight field')
        require(observed['actual_physical_backing']==[256,36] and observed['actual_caption_view']==[60,12] and observed['original_native_menu_rectangle']==rect,'complete actual owner geometry')
        seen={s['visible_selected_option_index'] for s in samples if s['visible_selected_option_index'] is not None};require(seen==({0} if choice=='accept' else {0,1}),'both logical controller selections actually highlighted')
        off.extend(dict(version=version,choice=choice,frame=s['frame'],logical_selected_option=s['selected_option_index']) for s in samples if s['visible_selected_option_index'] is None)
        results.append(dict(version=version,choice=choice,samples=len(samples),complete_visible_labels=2*len(samples),owned_caption_pixels_per_sample=len(owned),native_menu_rectangle=rect,later_nonB49_owner_rows_retained=len(excluded)))
    require(len(results)==4 and off==declared['source_highlight_off_samples']==[],'four actual menus/twelve samples/allselected sampledhighlights visible')
    return dict(original_even_alignment_providers_recomputed=6,bridged_modal_returns_recomputed=18,actual_menu_groups=results,actual_owned_backing_samples_recomputed=12,complete_visible_label_samples_recomputed=24,source_andtarget_caption_width_px=60,all_owned_backing_visible_glyphs_blankguards_native_backgrounds_highlights_andresults_independently_checked=True,no_unowned_blank_orcrosslanguage_everyframe_highlight_claim=True,executed_original_menu_instruction_addresses=len(executed),new_emulator_runs=0)
