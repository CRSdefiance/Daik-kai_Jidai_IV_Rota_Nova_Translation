"""Current34 pipelines/copies and712 real-name/proposed native layout cases."""
import inspect
from pathlib import Path
from PIL import Image,ImageDraw
from scripts.current_common_native_context_v2620b import CurrentContext
from scripts.probe_reinforcement_sniping_layout_v1030 import native_layout
from scripts.verify_arrival_native_v792 import prepared
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.search_reports_native_consumers_v1662 import assigned_role
from scripts.probe_common_single_cache_v862 import Loader
from scripts.battle_aftermath_native_plan_v1255 import compiled
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/aftermath_remaining_fonts_v2668')
DOC=Path('translations/aftermath_remaining_contextual_editorial_manuscript_v1.json')
BASE=0x02000000

def layout_variant(parent):
    code=inspect.getsource(native_layout)
    if parent!=0x02053DB8:
        code=code.replace('0x02053DB8',hex(parent))
        code=code.replace("struct.pack('<I',n)","struct.pack('<I',table)")
        needle="struct.pack('<I',table))\n    call"
        assert code.count(needle)==1
        code=code.replace(needle,"struct.pack('<I',0))\n    call")
    env=dict(native_layout.__globals__);exec(compile(code,__file__,'exec'),env)
    return env['native_layout'],sha(code.encode())

if __name__=='__main__':
    assert not ROOT.exists()
    ctx=CurrentContext(DOC,'out/all_routes_combined_v1807_candidate.nds',ROOT)
    doc=read(DOC);context=read(doc['native_context_proof']);font=ctx.rom.read_file('/GRP/KANJI.FNT')
    goldenpath=Path('work/analysis/battle_aftermath_fonts_v1260/native_font_proof.json');golden=read(goldenpath)
    old={(c['message_id'],c['name_case']['town_index'] if c['name_case'] and c['name_case']['kind']=='source-native-town' else None):c for c in golden['cases'] if c['name_case'] is None or c['name_case']['kind']=='source-native-town'}
    layouts={parent:layout_variant(parent) for parent in [0x02053DB8,0x02053F40,0x02054014]}
    rows={r['message_id']:r for r in doc['records']};cases=[];samples=[];pipelines=[];findings=[]
    names=context['all114_current_native_town_names_and_two_original_exchange_paths']
    longest=max(names,key=lambda r:len(bytes.fromhex(r['name_hex'])))
    cpu=prepared(ctx.arm)
    for n,row in rows.items():
        if n==2192:
            entry,parent,key,actor=0x53FE4,0x02054014,2192,names[0]['town_speaker_object']
            choice=dict(actor_object=actor,actor_ID=names[0]['town_speaker_actor_ID']);raw=ctx.raw;fixture=None
        else:
            table=next(t for t in context['voice_tables'] if n in t['members'])
            choice=next(c for c in table['all207_original_actor_choices'] if c['message_ID']==n and c['actor_ID']!=1)
            key=table['table']
            if 2000<=n<=2010:
                entry,parent,actor=0x53D44,0x02053DB8,1
                if choice['actor_ID']==16:raw,fixture=ctx.raw,None
                else:raw,fixture=assigned_role(ctx.arm,ctx.raw,1,choice['actor_ID'],choice['actor_object'])
            else:entry,parent,actor,raw,fixture=0x53F0C,0x02053F40,choice['actor_object'],ctx.raw,None
        arg=bytes.fromhex(longest['name_hex']) if row['native_argument_count'] else None
        native=ctx.speak(entry,actor,key,arg,raw=raw)
        deployed=ctx.entries[n].text
        assert native['input_hex']==(deployed.replace(b'%s',arg,1) if arg else deployed).hex()
        assert native['parent']==parent
        pipelines.append(dict(message_ID=n,entry=entry,parent=parent,selector=key,original_actor=choice,CPU_only_fixture=fixture,
            current_deployed_pipeline=native,proposed_revision_loaded=(n!=2029),
            current2029_still_old_wording=(n==2029)))
        value=compiled(row);layout,_=layouts[parent]
        if n!=2029:assert value==deployed
        else:assert value!=deployed
        variants=names if row['native_argument_count'] else [None]
        for name in variants:
            argument=bytes.fromhex(name['name_hex']) if name else None
            formatted,lines=layout(cpu,value,n,argument,key)
            assert ' '.join(lines)==value.replace(b'%s',argument,1).decode('cp932').strip() if argument else ' '.join(lines)==row['english']
            orphan=len(lines)>1 and len(lines[-1].split())==1
            weak=[i for i,line in enumerate(lines[:-1]) if line.split()[-1].strip('.,!?;:').lower() in {'a','an','the','to','of','with','for','from','on','in','as','at'}]
            assert not orphan and not weak,(n,name,lines)
            pixels=bytes(independent_font(ctx.arm,font,lines))
            previous=old[(n,name['town_index'] if name else None)]
            if n!=2029:
                assert formatted.hex()==previous['native_formatted_hex'] and lines==previous['lines']
                path=Path(previous['preview']);assert sha(path.read_bytes())==previous['preview_sha256']
                assert bytes(bool(p) for p in pixels)==bytes(v==0 for v in Image.open(path).convert('L').tobytes())
            case=dict(message_ID=n,town_index=name['town_index'] if name else None,
                town_name=name['name'] if name else None,town_hex=name['name_hex'] if name else None,
                compiled_hex=value.hex(),formatted_hex=formatted.hex(),lines=lines,
                font_plane_sha256=sha(pixels),current_native_printf_wrap_ABI_and_guards_pass=True,
                complete_current_independent_plane_equals_historical_native=(n!=2029),
                proposed_input_not_current_COMMON=(n==2029),no_orphan_or_weak_line_end=True)
            if name is None or name['town_index']==longest['town_index']:
                events=[];fresh=bytes(ctx.raster(ctx.arm,formatted,0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000,glyph_events=events))
                assert fresh==pixels
                for y,line in enumerate(lines):
                    glyphs=[e for e in events if e['y']==y*16 and e['x']>=6]
                    pos=0;x=6
                    for j,char in enumerate(line):
                        if ord(char)!=32 and glyphs[pos]['code']==32 and glyphs[pos]['x']==x:
                            assert y>0 and j==0;pos+=1
                        assert glyphs[pos]['code']==ord(char) and (glyphs[pos]['x'],glyphs[pos]['y'])==(x,y*16)
                        pos+=1;x+=6
                    assert x<=228 and all(e['code']==32 for e in glyphs[pos:])
                preview=ROOT/f'ID{n}_complete_native.png';Image.frombytes('L',(228,64),bytes(0 if p else 255 for p in fresh)).save(preview)
                case.update(complete_native_font_and_ordered_glyphs_pass=True,ordered_glyph_events=events,
                    preview=str(preview),preview_sha256=sha(preview.read_bytes()))
                samples.append(case)
                if n!=2029:assert native['formatted_hex']==formatted.hex()
            cases.append(case)
        print(f'ID{n}: {len(variants)}layout cases;native plane and deployed pipeline pass'+(';2029proposal is isolated input only' if n==2029 else ''),flush=True)
    assert len(cases)==712 and len(samples)==34 and len(pipelines)==34
    copies=[Loader(ctx.arm,ctx.common).copy(n,ctx.entries[n].text,mode) for mode in ['cold','warm'] for n in rows]
    assert len(copies)==68
    sheets=[]
    for start in range(0,len(samples),10):
        group=samples[start:start+10];sheet=Image.new('RGB',(936,152*((len(group)+1)//2)),'#263238');draw=ImageDraw.Draw(sheet)
        for i,c in enumerate(group):
            x,y=i%2*468,i//2*152;label=f'ID{c["message_ID"]}: '+('PROPOSED tone revision' if c['proposed_input_not_current_COMMON'] else 'current retained paragraph')
            draw.text((x+5,y+3),label,fill='white');sheet.paste(Image.open(c['preview']).resize((456,128),Image.Resampling.NEAREST),(x+5,y+22))
        path=ROOT/f'native_review_sheet{start//10+1}.png';sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes())))
    save(ROOT/'native_layout_and_font_research.json',dict(candidate=str(ctx.rompath),candidate_sha256=sha(ctx.rompath.read_bytes()),
        ARM9_sha256=sha(ctx.arm),COMMON_sha256=sha(ctx.common),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        cases=cases,complete_native_planes=samples,current_deployed_original_pipelines=pipelines,current_deployed_cold_warm_copies=copies,
        all114_real_town_names_for_each_of6_templates=684,static_or_proposed_cases=28,
        current_deployed_2029_remains_old_wording=True,proposed2029_not_loaded_or_copied_from_a_research_or_playable_COMMON=True,
        proposed2029_native_formatter_and_complete_font_pass=True,proposed_revision_release_payload_copy_and_startup_checks_pending=True,
        no_historical_synthetic_name_waivers_transferred=True,findings=findings,review_sheets=sheets,visual_review_pending=True,
        source_frame_layout_adapters={str(p):v[1] for p,v in layouts.items()},
        current_pipeline_plan=str(ctx.proof_path),current_pipeline_plan_sha256=sha(ctx.proof_path.read_bytes()),
        golden_native_proof=str(goldenpath),golden_native_proof_sha256=sha(goldenpath.read_bytes()),
        no_new_emulator_run_ROM_build_or_completion_credit=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('712native layouts,34complete planes,34deployed pipelines and68deployed copies pass. Proposed2029still requires registered payload/release/native-copy verification. Visual review pending.')
