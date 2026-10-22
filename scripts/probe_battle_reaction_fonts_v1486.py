"""All32 original actor pipelines and full native/independent glyph planes."""
from copy import deepcopy
from pathlib import Path
from types import FunctionType
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.battle_reaction_native_plan_v1484 import compiled
from scripts.probe_battle_aftermath_fonts_v1256 import consumer
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_reaction_fonts_v1486')
PLAN=Path('work/analysis/battle_reaction_payload_v1484/native_payload_plan.json')
DOC=Path('translations/battle_reactions_editorial_manuscript_v1.json')

def main():
    assert not ROOT.exists()
    plan,doc=read(PLAN),read(DOC);assert sha(DOC.read_bytes())==plan['manuscript_sha256']
    context=read(doc['source_context']);assert sha(Path(doc['source_context']).read_bytes())==doc['source_context_sha256']
    raw=Path(context['snapshot']['path']).read_bytes();assert sha(raw)==context['snapshot']['sha256']
    arm,common=Path(plan['target_ARM9']).read_bytes(),Path(plan['target_COMMON']).read_bytes()
    assert sha(arm)==plan['target_ARM9_sha256'] and sha(common)==plan['target_COMMON_sha256']
    entries=owned_entries(common,arm,plan['directory_sha256']);current=NdsImage.open(doc['current_ROM'])
    class CurrentFont:
        @staticmethod
        def open(path):
            assert path=='out/all_routes_combined_v255_candidate.nds'
            return current
    raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':CurrentFont},argdefs=original_raster.__defaults__)
    source={r['message_ID']:r for f in context['families'] for r in f['all8_original_actor_speech_contract_probes']}
    ROOT.mkdir(parents=True);cases=[];findings=[]
    for row in doc['records']:
        n=row['message_id'];representative=source[n];value=compiled(row);assert entries[n].text==value
        native=consumer(arm,common,raw,plan,0x53F0C,representative['actor_object'],row['source_table'])
        assert native['input_hex']==value.hex() and native['parent']==row['original_native_parent']
        assert native['selector']==row['source_table'] and native['selector_offset']==row['selector_stack_offset']
        formatted=bytes.fromhex(native['formatted_hex']);lines=[v.strip().decode('ascii') for v in formatted.split(b'\n')]
        assert ' '.join(lines)==row['english'] and 1<=len(lines)<=4
        assert all(0<len(v)<=35 and '  ' not in v for v in lines)
        events=[];pixels=raster(arm,formatted,0x01FFCE40-0x02000000,size=(228,64),instruction_limit=2000000,glyph_events=events)
        assert pixels==independent_font(arm,current.read_file('/GRP/KANJI.FNT'),lines)
        for index,line in enumerate(lines):
            actual=[e for e in events if e['y']==16*index and e['x']>=6 and e['x']<6+6*len(line)]
            assert [e['code'] for e in actual]==list(line.encode('ascii'))
            assert [e['x'] for e in actual]==[6+6*i for i in range(len(line))]
            assert actual[0]['x']==6 and actual[-1]['x']+6<=228
        issues=[]
        if len(lines)>1 and len(lines[-1].split())==1:issues.append('isolated-final-word')
        weak=[i for i,line in enumerate(lines[:-1]) if line.split()[-1].strip('.,!?;:').lower() in {'a','an','the','to','of','with','for','from','on','in','as','at','and','or'}]
        if weak:issues.append('weak-line-ending')
        path=ROOT/f'ID{n}_complete_native.png'
        Image.frombytes('L',(228,64),bytes(0 if p else 255 for p in pixels)).save(path)
        case={'message_ID':n,'source_family':row['source_family'],'source_voice':row['source_voice'],
            'existing_actor_ID':representative['existing_actor_ID'],'actor_object':representative['actor_object'],
            'compiled_hex':value.hex(),'native_pipeline':native,'lines':lines,'findings':issues,'weak_line_end_indices':weak,
            'full228x64_native_and_independent_font_exact':True,'complete_ordered_glyph_events':events,
            'complete_first_final_letters_uniform6px_margins_bounds_and_blank_paper_pass':True,
            'whole_native_font_plane_sha256':sha(bytes(pixels)),'preview':str(path),'preview_sha256':sha(path.read_bytes()),
            'CPU_existing_actor_probe_no_role_identity_RNG_health_or_emulator_change':True}
        cases.append(case)
        if issues:findings.append({k:case[k] for k in ['message_ID','lines','findings']})
    invalid=[];baseline=doc['records'][0]
    for label,field,value in [('leading-space','english',' '+baseline['english']),('trailing-space','english',baseline['english']+' '),
        ('internal-gap','english','A  battle!'),('LF','english','A\nbattle!'),('NUL','english','A\0battle!'),
        ('invented-printf','english','A battle with %s!'),('literal-percent','english','100% ready!'),
        ('layout-markup','english','A battle! {LB}'),('empty','english',''),('non-ASCII','english','A battle\u2014yes!'),
        ('unreviewed-long-contract','english','A'*160),('wrong-ID','message_id',2146),
        ('invented-argument-count','native_argument_count',1),('invented-macro','source_native_macros',['IC'])]:
        row=deepcopy(baseline);row[field]=value
        try:compiled(row)
        except (ValueError,AssertionError):invalid.append(label)
        else:raise AssertionError(label)
    sheets=[]
    for start in [0,16]:
        sheet=Image.new('RGB',(936,1216),'#263238');draw=ImageDraw.Draw(sheet)
        for j,case in enumerate(cases[start:start+16]):
            x,y=j%2*468,j//2*152
            draw.text((x+5,y+3),f'ID{case["message_ID"]} voice{case["source_voice"]}',fill='white')
            with Image.open(case['preview']) as preview:sheet.paste(preview.resize((456,128),Image.Resampling.NEAREST),(x+5,y+22))
        path=ROOT/f'reactions_{start:02d}_native_review.png';sheet.save(path)
        sheets.append({'path':str(path),'sha256':sha(path.read_bytes())})
    save(ROOT/'native_font_research.json',{'manuscript':str(DOC),'manuscript_sha256':sha(DOC.read_bytes()),
        'plan':str(PLAN),'plan_sha256':sha(PLAN.read_bytes()),'ARM9_sha256':sha(arm),'COMMON_sha256':sha(common),
        'cases':cases,'findings':findings,'invalid_compiler_inputs_rejected':invalid,
        'all32_original_actor_selection_printf_macro_wrap_and_full_glyph_planes_verified':True,
        'all824_existing_actor_choices':sum([f['all206_existing_actor_choices'] for f in context['families']],[]),
        'sheets_for_visual_review':sheets,'visual_review_layout_refinement_copies_registered_release_and_original_events_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('32 full original actor/font planes and14 compiler rejections pass;layout findings:',findings)

if __name__=='__main__':main()
