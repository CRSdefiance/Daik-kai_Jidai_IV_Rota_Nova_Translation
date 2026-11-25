"""Current whole pipelines and native fonts for real names/captured-cap controls."""
from pathlib import Path
from PIL import Image,ImageDraw
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.search_reports_native_consumers_v1662 import assigned_role
from scripts.ship_loss_surrender_native_plan_v1444 import compiled
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.probe_common_single_cache_v862 import Loader
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/ship_loss_fonts_v2690')
DOC=Path('translations/ship_loss_contextual_editorial_manuscript_v1.json')
BASE=0x02000000

if __name__=='__main__':
    assert not ROOT.exists()
    ctx=CurrentContext(DOC,'out/all_routes_combined_v1807_candidate.nds',ROOT)
    doc=read(DOC);context=read(doc['native_context_proof']);font=ctx.rom.read_file('/GRP/KANJI.FNT')
    goldenpath=Path('work/analysis/ship_loss_surrender_fonts_v1448/native_font_research.json');golden=read(goldenpath)
    assert len(golden['cases'])==624 and golden['findings']==[]
    old={(r['message_ID'],r['name_hex']):r for r in golden['cases']}
    names={}
    for n in context['original_live_name_getters']:
        names.setdefault(n['name_hex'],dict(name=n['name'],hex=n['name_hex'],kind='current-historical-model-native-name-getter',actual_getter=n))
    for r in golden['cases']:
        names.setdefault(r['name_hex'],dict(name=r['name'],hex=r['name_hex'],kind='captured-cap-CPU-input-not-keyboard-reachability'))
    for value in ['100% Chance','%s%o%09d']:
        names.setdefault(value.encode().hex(),dict(name=value,hex=value.encode().hex(),kind='inserted-percent-data-within18bytes-CPU-only'))
    assert len(names)==31 and all(0<len(bytes.fromhex(n))<=18 for n in names)
    longest_real=max(context['original_live_name_getters'],key=lambda n:len(bytes.fromhex(n['name_hex'])))['name_hex']
    extras={(2076,('F'+'A'*17).encode().hex()),(2078,('長崎丸'*3).encode('cp932').hex()),(2078,b'Santa Maria'.hex()),(2078,b"F's Hope".hex()),(2099,'ＦＡＬＣＯＮ'.encode('cp932').hex()),(2099,b'%s%o%09d'.hex())}
    cases=[];samples=[];fixtures=[];all_matches=0
    for row in doc['records']:
        n=row['message_id'];table=next(t for t in context['voice_tables'] if n in t['members'])
        choice=next((c for c in table['all207_original_actor_choices'] if c['message_ID']==n and c['actor_ID']==context['logical_First_Mate_actor_ID']),None)
        if choice is None:choice=next(c for c in table['all207_original_actor_choices'] if c['message_ID']==n and c['actor_ID']!=1)
        if True: # All three original consumers are role1.
            if choice['actor_ID']==context['logical_First_Mate_actor_ID']:raw,fixture=ctx.raw,dict(no_roster_fixture=True,actual_logical_actor_ID=choice['actor_ID'])
            else:raw,fixture=assigned_role(ctx.arm,ctx.raw,1,choice['actor_ID'],choice['actor_object'])
            speaker=1
        fixtures.append(dict(message_ID=n,original_actor_choice=choice,CPU_only_fixture=fixture))
        text=compiled(row);assert text==ctx.entries[n].text
        for hx,name in names.items():
            argument=bytes.fromhex(hx);pipeline=ctx.speak(table['entry'],speaker,table['table'],argument,raw=raw)
            cpu=ctx.machines[-1][0];owner=int.from_bytes(ctx.arm[0x552A0:0x552A4],'little')
            loaded=bytes(cpu.mem_read(owner+0x2030,512)).split(b'\0')[0]
            assert loaded==text and pipeline['input_hex']==text.replace(b'%s',argument,1).hex()
            assert pipeline['parent']==table['parent'] and pipeline['selector']==table['table']
            formatted=bytes.fromhex(pipeline['formatted_hex']);lines=[v.strip().decode('cp932') for v in formatted.split(b'\n')]
            assert ' '.join(lines)==text.replace(b'%s',argument,1).decode('cp932').strip()
            assert 1<=len(lines)<=4 and all(0<len(line.encode('cp932'))<=35 for line in lines)
            weak=[i for i,line in enumerate(lines[:-1]) if line.split()[-1].strip('.,!?;:').lower() in {'a','an','the','to','of','with','for','from','on','in','as','at'}]
            orphan=len(lines)>1 and len(lines[-1].split())==1
            complete_name_row=len(lines)>1 and lines[-1]==argument.decode('cp932')+'!' and text.endswith(b'%s!')
            assert not weak and (not orphan or complete_name_row),(n,name,lines)
            disposition=('The final row is exactly the complete original runtime proper name plus the source exclamation. It is an intact named object following the complete captured/taken-over predicate;no name byte or English predicate/title is stranded.' if complete_name_row else None)
            # The whole original pipeline has already verified actor preservation.
            # Release each copied CPU after recording its bounded loader output.
            ctx.machines.pop()
            events=[];pixels=bytes(ctx.raster(ctx.arm,formatted,0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000,glyph_events=events))
            assert pixels==bytes(independent_font(ctx.arm,font,lines))
            for y,line in enumerate(lines):
                rowevents=[e for e in events if e['y']==y*16]
                assert all(e['code']==32 and e['x']==0 for e in rowevents if e['x']<6)
                actual=[e for e in rowevents if e['x']>=6];pos=0;x=6
                for j,char in enumerate(line):
                    encoded=char.encode('cp932');code=int.from_bytes(encoded,'big')
                    if code!=32 and actual[pos]['code']==32 and actual[pos]['x']==x:
                        assert len(encoded)==2 or (y>0 and j==0);pos+=1
                    assert actual[pos]['code']==code and (actual[pos]['x'],actual[pos]['y'])==(x,y*16)
                    pos+=1;x+=6*len(encoded)
                assert x<=228 and all(e['code']==32 for e in actual[pos:])
            reference=old.get((n,hx))
            if reference:
                assert formatted.hex()==reference['native_pipeline']['formatted_hex'] and lines==reference['lines'] and sha(pixels)==reference['whole_native_font_plane_sha256'];all_matches+=1
            case=dict(message_ID=n,name_case=name,compiled_hex=text.hex(),loaded_template_hex=loaded.hex(),formatted_hex=formatted.hex(),lines=lines,
                native_pipeline=pipeline,complete_native_and_independent_plane_equal=True,complete_ordered_glyphs_margins_blank_paper_and_bounds_pass=True,
                full_palette_font_plane_sha256=sha(pixels),matches_prior_full_native_case=bool(reference),
                weak_line_end_indices=weak,single_word_final_row=orphan,complete_atomic_runtime_name_on_final_row=complete_name_row,final_runtime_name_row_justification=disposition)
            if hx==longest_real or (n,hx) in extras:
                p=ROOT/f'ID{n}_name{hx}_complete_native.png';Image.frombytes('L',(228,64),bytes(0 if v else 255 for v in pixels)).save(p)
                case.update(preview=str(p),preview_sha256=sha(p.read_bytes()),complete_glyph_events=events);samples.append(case)
            cases.append(case)
        print(f'ID{n}:31whole current pipelines/full native planes pass.',flush=True)
    assert len(cases)==744 and all_matches==624 and len(samples)==30 and not ctx.machines
    copies=[Loader(ctx.arm,ctx.common).copy(n,ctx.entries[n].text,mode) for mode in ['cold','warm'] for n in [*range(2074,2082),*range(2090,2106)]]
    assert len(copies)==48
    loader=Loader(ctx.arm,ctx.common);boundary=[]
    for n in [2099,2099,2100,2100,2099,2099,2105,2105]:boundary.append(loader.copy(n,ctx.entries[n].text,'sequence'))
    assert all(b['reads']==0 for b in boundary[1::2]) and all(b['reads']>0 for b in boundary[::2])
    sheets=[]
    for start in range(0,len(samples),10):
        group=samples[start:start+10];sheet=Image.new('RGB',(936,152*((len(group)+1)//2)),'#263238');draw=ImageDraw.Draw(sheet)
        for i,c in enumerate(group):
            x,y=i%2*468,i//2*152;label=f'ID{c["message_ID"]}: '+c['name_case']['name'];draw.text((x+5,y+3),label,fill='white')
            sheet.paste(Image.open(c['preview']).resize((456,128),Image.Resampling.NEAREST),(x+5,y+22))
        p=ROOT/f'native_review_sheet{start//10+1}.png';sheet.save(p);sheets.append(dict(path=str(p),sha256=sha(p.read_bytes())))
    save(ROOT/'native_font_and_pipeline_proof.json',dict(candidate=str(ctx.rompath),candidate_sha256=sha(ctx.rompath.read_bytes()),ARM9_sha256=sha(ctx.arm),COMMON_sha256=sha(ctx.common),
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),cases=cases,full_native_font_and_original_pipeline_cases=744,
        all624_previous_native_cases_equal_current_full_palette_planes=True,additional_current_names_or_percent_cases=120,
        names=list(names.values()),original_speaker_fixtures=fixtures,complete_atomic_name_final_row_cases=sum(c['complete_atomic_runtime_name_on_final_row'] for c in cases),all48_current_cold_warm_copies=copies,COMMON22_23_boundary_cache_sequence=boundary,
        all_executed_pipeline_instructions_current_exact_and_actor_models_unchanged=True,
        ASCII_lengths1to18_macro_like_names_fullwidth_CJK_apostrophes_and_inserted_percent_data_preserved=True,
        captured_byte_capacity_not_all_keyboard_pages_or_legacy_name_reachability=True,
        findings=[],review_sheets=sheets,visual_review_pending=True,
        current_context_plan=str(ctx.proof_path),current_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        original_native_proof=str(goldenpath),original_native_proof_sha256=sha(goldenpath.read_bytes()),
        no_actual_selected_capture_surrender_new_emulator_run_or_completion_credit=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('744current original pipelines/full native planes,624old full-palette matches,48copies and8boundary switches pass.30samples on3sheets await visual review. No selected capture/surrender event claim.')
