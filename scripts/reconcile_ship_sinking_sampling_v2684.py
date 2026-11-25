"""Fresh full-palette binding of named-target/direct and role1 representative holds."""
import struct
from pathlib import Path
from PIL import Image,ImageDraw
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_dialogue_palette_v628 import PALETTE,resident,captured_rgb
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT=Path('work/analysis/ship_sinking_sampling_v2684');BASE=0x02000000
DOC=Path('translations/ship_sinking_contextual_editorial_manuscript_v1.json')

if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True);doc=read(DOC)
    originals=[('named-target',Path('work/analysis/enemy_capture_history_v2597b/historical_enemy_capture_current_binding.json'),2082,0x02117B00,0x53F0C),
        ('role1',Path('work/analysis/aftermath_defeat_history_v2551b/historical_aftermath_defeat_current_binding.json'),2138,0x02117F00,0x53D44)]
    holds=[];controls=[];contexts=[];selected=[];evidence={str(DOC):sha(DOC.read_bytes()),'docs/editorial_testing_scope_v1870.md':sha(Path('docs/editorial_testing_scope_v1870.md').read_bytes())}
    for label,hp,n,table,entry in originals:
        old=read(hp);evidence[str(hp)]=sha(hp.read_bytes());chosen=[h for h in old['historical_holds'] if h['message_ID']==n]
        assert len(chosen)==2
        first=chosen[0];contextpath=ROOT/(label+'_historical_source.json');save(contextpath,dict(actual_snapshot=first['RAM'],actual_snapshot_sha256=first['RAM_sha256']))
        inputpath=ROOT/(label+'_current_context_input.json');save(inputpath,dict(current_ROM=doc['current_ROM'],current_ROM_sha256=doc['current_ROM_sha256'],
            current_ARM9_sha256=doc['current_ARM9_sha256'],current_COMMON_sha256=doc['current_COMMON_sha256'],native_context_proof=str(contextpath)))
        ctx=CurrentContext(inputpath,old['historical_candidate'],ROOT/label)
        cpu,get,_=ctx.machine(ctx.arm,ctx.common,ctx.raw,ctx.plan);fleet=get(0xCB1A8)
        if label=='named-target':
            attacker=get(0x36C70,fleet+4+132+12);target=get(0x36C70,fleet+4+5*132+12)
            actor=get(0x55DC4,attacker,8);assert get(0x7EE08,actor)==18
            vt=struct.unpack('<I',cpu.mem_read(target,4))[0];method=struct.unpack('<I',cpu.mem_read(vt+4,4))[0];ptr=get(method-BASE,target)
            argument=bytes(cpu.mem_read(ptr,64)).split(b'\0')[0];assert argument==b'Hanse Cog'
            assert [get(0x5543C,target),get(0x55444,target)]==[30,0]
            source_control=dict(source_actor_ID=18,original_actor_getter_argument=8,native_name_getter=method,target_name_hex=argument.hex(),target_Hull_Crew=[30,0],not_a_sinking=True)
        else:
            actor,argument=1,None;assert get(0x82478,fleet+0x2090,1)==18
            source_control=dict(source_role=1,source_actor_ID=18,not_a_sinking=True)
        pipeline=ctx.speak(entry,actor,table,argument)
        formatted=bytes.fromhex(pipeline['formatted_hex']);lines=[p.strip().decode('cp932') for p in formatted.split(b'\n')]
        pixels=bytes(ctx.raster(ctx.arm,formatted,0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000))
        assert pixels==bytes(independent_font(ctx.arm,ctx.rom.read_file('/GRP/KANJI.FNT'),lines))
        palette=struct.unpack('<16H',resident(ctx.arm,PALETTE,32));colors={1:captured_rgb(palette[15]),15:captured_rgb(palette[14])}
        assert colors=={1:(0,8,0),15:(197,198,197)}
        def match(im,plane=pixels):
            for index,color in colors.items():
                expected={(16+i%228,296+i//228) for i,p in enumerate(plane) if p==index}
                actual={(x,y) for y in range(294,366) for x in range(16,244) if im.getpixel((x,y))==color}
                assert expected==actual
        for h in chosen:
            path=Path(h['capture']);assert sha(path.read_bytes())==h['capture_sha256'] and sha(Path(h['RAM']).read_bytes())==h['RAM_sha256']
            image=Image.open(path).convert('RGB');match(image)
            holds.append(dict(message_ID=n,frame=h['frame'],capture=str(path),capture_sha256=h['capture_sha256'],
                current_complete_native_ink_gray_shadow_and_blank_masks_equal=True,lines=lines,source_control=source_control,
                historical_other_family_not_a_sinking_or_current_visit=True))
            evidence[str(path)]=h['capture_sha256']
        original=Image.open(first['capture']).convert('RGB')
        def rejects(im,plane=pixels):
            try:match(im,plane)
            except AssertionError:return True
            return False
        for title,box in [('erase-first-visible-letter',(22,296,28,312)),('erase-final-punctuation',(22+6*(len(lines[-1])-1),296+16*(len(lines)-1),28+6*(len(lines[-1])-1),312+16*(len(lines)-1)))]:
            bad=original.copy();bad.paste('white',box);assert rejects(bad);controls.append(dict(family=label,case=title,rejected=True))
        for title,color in [('stray-ink',colors[1]),('stray-gray-shadow',colors[15])]:
            bad=original.copy();bad.putpixel((17,360),color);assert rejects(bad);controls.append(dict(family=label,case=title,rejected=True))
        if label=='named-target':
            wrong=ctx.speak(entry,actor,table,b'Vestaros');wronglines=[v.strip().decode('cp932') for v in bytes.fromhex(wrong['formatted_hex']).split(b'\n')]
            wrongpixels=bytes(independent_font(ctx.arm,ctx.rom.read_file('/GRP/KANJI.FNT'),wronglines));assert rejects(original,wrongpixels)
            controls.append(dict(family=label,case='wrong-name-through-current-original-pipeline',rejected=True))
        selected.extend([dict(**holds[-2],label=label+' historical hold;not sinking'),dict(capture=old['scoped_historical_cancellation_and_battle_transitions_freshly_rechecked'][-1]['capture'],capture_sha256=old['scoped_historical_cancellation_and_battle_transitions_freshly_rechecked'][-1]['capture_sha256'],label=label+' historical normal return')])
        contexts.append(dict(family=label,pipeline=pipeline,current_context_plan=str(ctx.proof_path),current_context_plan_sha256=sha(ctx.proof_path.read_bytes()),source_control=source_control))
        oldarm=NdsImage.open(old['historical_candidate']).read_file('/__arm9__.bin');clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
        for a,b in [(0x53D44,0x54058),(0x54058,0x54144),(0x54164,0x54240),(0x55DC4,0x55E6C),(0x72660,0x72BD8),(0x753F0,0x75560)]:assert ctx.arm[a:b]==oldarm[a:b]==clean[a:b]
    for s in selected:assert sha(Path(s['capture']).read_bytes())==s['capture_sha256']
    sheet=Image.new('RGB',(512,820),'#263238');draw=ImageDraw.Draw(sheet)
    for i,s in enumerate(selected):
        x,y=i%2*256,i//2*410;draw.text((x+2,y+3),s['label'][:39],fill='white');sheet.paste(Image.open(s['capture']).convert('RGB'),(x,y+24))
    sp=ROOT/'historical_representative_not_sinking.png';sheet.save(sp)
    save(ROOT/'representative_control_and_rgb_reconciliation.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],
        evidence=evidence,current_source_contexts=contexts,historical_holds=holds,negative_controls=controls,
        historical_actual_IDs=[2082,2138],actual_sinking_IDs=[],new_emulator_runs=0,
        all_four_historical_complete_native_ink_shadow_and_blank_masks_equal=True,
        original_named_target_getter_and_actor_selection_and_role1_control_shared=True,
        original_constructor_return_status_and_projectile_code_clean_current_historical_exact=True,
        previous_gunnery_pilots_without_notice_still_no_sinking_credit=True,
        policy_resolution='The16unchanged reports use established kind0 member/direct-actor portrait controls and one original ship-name substitution. Every current whole pipeline and complete native font is checked for31name cases,including current live names,all1-18ASCII byte lengths,macro-like,CJK/fullwidth andinserted percent data. Two source families keep their distinct active/Hull/side predicates and source-selected actor/name providers. Existing named-target capture2082 proves the same55DC4/direct/name path andnormal dismissal/return;role1defeat2138 supplies the member panel/return sample. Current full-palette RGB/blank masks freshly bind those4historical holds,with9corruptions rejected. These samples do not prove a sinking. Unchanged constructor/return/event code plus current exhaustive native tests leave no new translation-specific display/control risk requiring an individual sinking visit under the user representative policy. No result,Hull,crew,RNG,message or outcome is forged;no new emulator run or earned qualification is claimed.',
        no_open_translation_specific_display_or_control_finding=True,
        review_sheet=str(sp),review_sheet_sha256=sha(sp.read_bytes()),visual_review_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('4historical named-target/role1holds freshly match current full RGB ink/shadow/blank masks;9corruptions reject. Shared sources/normal returns reconcile sink16under representative policy;no actual sinking claim.')
