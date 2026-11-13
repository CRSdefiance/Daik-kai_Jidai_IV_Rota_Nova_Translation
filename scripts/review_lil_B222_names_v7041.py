"""Retain the two source-bound names contextually and measure exact current style11 planes."""
from copy import deepcopy
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from scripts.square_shopkeeper_exact_native_context_v7020 import CurrentContext
from scripts.square_shopkeeper_name_style_v7020 import native_name_raster,style_source_proof
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels
from scripts.generic_name_macro_owned_v5886b import expand
from scripts.prove_lil_B208_name_planes_v6405 import codes,original_name_events
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B222_name_planes_v7041')
CONSUMER=Path('work/analysis/lil_B222_consumers_v7038/sixteen_effective_bodies32_dispatches_two_actors_four_name_consumers.json')
SOURCE=Path('work/analysis/lil_B222_source_v7037/sixteen_clean_current_sunset_Noritsune_exchange_source_references.json')
INPUT=Path('work/analysis/current_V7029_native_v7033/current_native_input.json')
STOCKHOLM=Path('work/analysis/lil_Stockholm_source_v1848b/all51_clean_current_native_source_context.json')
DOC=Path('translations/lil_B222_speaker_name_review_v1.json')
if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists();consumer,source,stockholm=map(read,[CONSUMER,SOURCE,STOCKHOLM])
    assert consumer['candidate_sha256']==source['current_ROM_sha256']==read(INPUT)['current_ROM_sha256']
    original=consumer['native_four_distinct_name_consumers'];got={(r['actor_ID'],r['consumer']):r['text'] for r in original['rows']}
    assert got=={(2,'progressive-nameplate'):'Lil Argot',(2,'full-catalogue'):'Lil Argot',(16,'progressive-nameplate'):'Gerhard Ardelknatts',(16,'full-catalogue'):'Gerhard Ardelknatts'}
    source_names={r['actor_ID']:r['fields'] for r in consumer['source_name_fields']}
    assert [f.get('Japanese') for f in source_names[2]]==['リル','アーゴット',None]
    assert [f.get('Japanese') for f in source_names[16]]==['ゲルハルト','アーデルンカッツ',None]
    context_rows=[r for r in stockholm['records'] if r['id'] in ['DK4_MES_B27_R0091','DK4_MES_B27_R0094']]
    assert len(context_rows)==2 and 'ゲルハルト・アーデルンカッツ' in context_rows[0]['Japanese'] and 'アーデルンカッツ提督' in context_rows[1]['Japanese']
    ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')
    literals=['Lil','Argot','Lil Argot','Gerhard','Ardelknatts','Gerhard Ardelknatts'];cases=[];planes=[]
    for ident in [2,16]:
        for word in literals:
            result=ctx.execute(expand,word.encode('ascii'),ident);ctx.machines.pop()
            assert all(c['output_hex']==word.encode('ascii').hex() for c in result['cases'])
            cases.append(dict(actor_ID=ident,literal=word,native=result))
    assert not ctx.machines;sheet=Image.new('RGB',(900,1092),'#263238');draw=ImageDraw.Draw(sheet)
    for index,word in enumerate(literals):
        raw=word.encode('ascii');pixels,events,font=native_name_raster(ctx.arm,raw);assert pixels==expected_pixels(ctx.arm,font,events)
        visible,flushes=original_name_events(events,raw);assert visible==codes(raw) and all(e['kind']=='ascii' and e['y']==0 and 0<=e['x'] and e['x']+6<=216 for e in events)
        plane=ROOT/f'name{index+1}.bin';plane.write_bytes(pixels)
        preview=ROOT/f'name{index+1}.png';im=Image.new('RGB',(216,64));im.putdata([(65,53,42) if p else (250,245,223) for p in pixels]);im.save(preview)
        y=index*182;draw.text((4,y+4),word+';complete current original style11',fill='white');sheet.paste(im.crop((0,0,216,16)).resize((864,64),Image.Resampling.NEAREST),(4,y+28))
        planes.append(dict(text=word,native_plane=str(plane),native_plane_sha256=sha(pixels),preview=str(preview),preview_sha256=sha(preview.read_bytes()),events=events,
            source_owned_zero_ink_flushes=flushes,original_pair_flush_width=max(e['x']+6 for e in events),complete_leading_internal_final_glyphs_in_one_original_row=True))
    sp=ROOT/'six_complete_name_component_planes.png';sheet.save(sp)
    records=[]
    for ident,word,reason in [
        (2,'Lil Argot','Retain the user-established Lil Argot identity fromリル/アーゴット. Both original consumers return that complete pair. The direct Gerhard address does not change Lil\'s name,title,kinship or identity.'),
        (16,'Gerhard Ardelknatts','Retain Gerhard forゲルハルト and the established localized family-name form Ardelknatts tied toアーデルンカッツ. The complete earlier Stockholm source self-introduction names the same given/family pair,and the current spoken Gerhard agrees with both original full-name consumers. This reflective story gives no reason to invent a new surname,nickname,title or identity. Preserve the full family component rather than truncating it;no claim is made that the fictional surname is a conventional national name or that an original Latin artwork spelling was inspected here.')]:
        records.append(dict(id=f'ACTOR_{ident:03d}_B222_CONTEXTUAL_NAME_RETENTION',actor_ID=ident,english=word,editorial_decision='retain-wording',
            source_fields=deepcopy(source_names[ident]),current_original_consumers=[r for r in original['rows'] if r['actor_ID']==ident],
            source_meaning='The original given/family-name pair;the third field is null in both clean and current data.',
            context=source['whole_exchange_context_notes'],localization_note=reason,fresh_retained_wording_justification=reason,
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            formatting_reason='Four original getters and six component/returned literal planes with48 alignment cases pass;actual B222 headers and final English native display remain pending.',
            new_name_or_dialogue_credit=0))
    evidence={str(p):sha(p.read_bytes()) for p in [CONSUMER,SOURCE,INPUT,STOCKHOLM,Path(__file__),Path('docs/glossary.md'),Path('translations/character_name_localization_policy_v1.json'),
        Path('scripts/square_shopkeeper_exact_native_context_v7020.py'),Path('scripts/square_shopkeeper_name_style_v7020.py'),Path('scripts/square_shopkeeper_font_oracles_v7020.py')]}
    save(ROOT/'two_actors_four_getters_six_name_component_planes48_alignments.json',dict(candidate=source['current_ROM'],candidate_sha256=source['current_ROM_sha256'],
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),native_four_distinct_name_consumers=original,name_planes=planes,native_literal_cases=cases,
        name_literal_alignment_count=48,complete_name_component_plane_count=6,source_owned_style11_caller=style_source_proof(ctx.arm),
        Stockholm_name_identity_source_only_no_reopening_or_duplicate51_record_credit=[dict(id=r['id'],source_reference=r['source_reference'],Japanese=r['Japanese']) for r in context_rows],
        actual_B222_headers_and_complete_English_display_pending=True,full_catalogue_UI_unvisited=True,no_name_asset_change_or_global207_approval=True,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),review_sheet=str(sp),review_sheet_sha256=sha(sp.read_bytes()),
        visual_review_pending=True,evidence=evidence,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    save(DOC,dict(format='dk4-contextual-speaker-name-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',records=records,
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),native_name_proof=str(ROOT/'two_actors_four_getters_six_name_component_planes48_alignments.json'),
        native_name_proof_sha256=sha((ROOT/'two_actors_four_getters_six_name_component_planes48_alignments.json').read_bytes()),
        no_name_asset_or_duplicate_source_credit=True,full207_name_role_alias_review_and_full_catalogue_UI_remain_open=True,full_goal_complete=False))
    print('Lil Argot/Gerhard Ardelknatts contextually retained;four getters,six complete planes/48 alignments pass. Actual headers and formatting approval pending.',flush=True)
