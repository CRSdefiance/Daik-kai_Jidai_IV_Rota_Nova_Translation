"""Bind the five Rafael exchanges to current native names and established terms."""
from pathlib import Path
import struct

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.prove_lil_B167_names_v4124b import names as original_names
from scripts.qualify_rafael351_item_and_UI_terms_v1 import string
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime

A=Path('work/analysis')
CURRENT=A/'Rafael_B161_B165_current1607_20261105/current_effective.json'
PRIOR=A/'Rafael557_names_terms_v1_20261105/names_terms_andconsumer_dependency_qualification.json'
MACROS=A/'Rafael261_names_terms_20261105/names_macros_andconsumer_dependency_qualification_v1.json'
ADAPTER=A/'Rafael_B61_B80_new_name_bindings_20261104/names.json'
ITEMS=Path('translations/all_item_names_arm9_v1.json')
STORY=Path('translations/rafael557_integrated_final_review_v1.json')
HELP=Path('translations/help_early23_contextual_final_review_v1.json')
OUT=CURRENT.with_name('names_and_terms_v1.json')
NAMES=Path('translations/rafael_B161_B165_scoped_names_review_v1.json')
REASONS={
    0:('Rafael Castor','Retain the user-approved full name in the header. The audience preserves separate surname and given-name substitutions.'),
    4:('Janus Pasar','Keep Janus Pasar as the public name while his careful map reading supplies the scene’s more precise register.'),
    5:('Claudio Manaus','Keep Claudio Manaus in the header. The ball lesson establishes mentoring and banter without family or a new rank.'),
    8:('Arcadius Eudoxios','Keep the public Arcadius name in his exchange with Claudio. The earlier private revelation does not change this scene’s address.'),
    120:('Guard','Keep the established role across the admission and royal-audience commands. His courtesy supplies no name or rank.'),
    125:('King','Keep the source role label. The audience establishes Portugal in prose and gives no personal name.'),
    132:('Priest','Retain the established public ritual role for the presentation of the relic. The dialogue supplies no personal name or denomination.'),
    163:('Boy','Keep the ordinary source role label. The child addresses Claudio familiarly while learning how to throw a ball.'),
}

def main():
    assert not OUT.exists() and not NAMES.exists()
    current,prior,macros,adapter=map(load,[CURRENT,PRIOR,MACROS,ADAPTER])
    rt=current['runtime']
    ctx=RegisteredRuntime(rt['release_proof'],rt['startup_proof'],captain=0)
    assert ctx.receipt()==rt
    font=ctx.image.read_file('/GRP/KANJI.FNT')
    for earlier in (prior,macros):
        old=RegisteredRuntime(earlier['runtime']['release_proof'],earlier['runtime']['startup_proof'],captain=0)
        assert (ctx.arm,ctx.common,ctx.actor_root,ctx.actor_bytes)==(old.arm,old.common,old.actor_root,old.actor_bytes)
        assert old.image.read_file('/GRP/KANJI.FNT')==font
    assert macros['complete_ARM9_COMMON_font_andactor0_macro_dependencies_qualified']
    assert macros['macro_ascii_lengths']==dict(FI=6,FA=6,FO=10)
    assert sha(Path(macros['same_Rafael_default_macro_proof']).read_bytes())==macros['same_Rafael_default_macro_proof_sha256']
    assert {r['source_selector'] for g in current['groups'] for r in g['records']}=={*REASONS,254}
    clean=NdsImage.open('work/clean.nds')
    jp=clean.read_file('/__arm9__.bin')
    old_names={r['actor_ID']:r for r in prior['name_bindings']}
    fresh=sorted(set(REASONS)-old_names.keys())
    assert fresh==[125,132,163]
    env={**original_names.__globals__,'ACTORS':fresh}
    exec(compile(adapter['source_owned_current_adapter'],__file__+'::same-own-native-getters','exec'),env)
    result=ctx.execute(env['names'])
    assert len(result['rows'])==6
    a,b=[struct.unpack_from('<I',arm,0xCDAC0)[0]-BASE for arm in [jp,ctx.arm]]
    names,bindings=[],[]
    for actor,(expected,reason) in REASONS.items():
        fields=[]
        for column in (0,4,8):
            source_at,current_at=a+32*actor+column,b+32*actor+column
            source=struct.unpack_from('<I',jp,source_at)[0]
            target=struct.unpack_from('<I',ctx.arm,current_at)[0]
            read=lambda data,ptr: string(data,ptr) if ptr else dict(pointer=0,hex='',text='')
            fields.append(dict(column=column,source=dict(field_offset=source_at,**read(jp,source)),
                current=dict(field_offset=current_at,**read(ctx.raw,target))))
        if actor in fresh:
            forms=[r for r in result['rows'] if r['actor_ID']==actor]
        else:
            assert fields==old_names[actor]['source_andcurrent_fields']
            forms=old_names[actor]['current_consumers']
        assert {r['consumer'] for r in forms}=={'progressive-nameplate','full-catalogue'}
        by_consumer={'progressive-nameplate':expected,'full-catalogue':expected}
        if actor==8:
            by_consumer['full-catalogue']='Arcadius Eirene Eudoxios'
        assert all(r['text']==by_consumer[r['consumer']]==bytes.fromhex(r['text_hex']).decode('ascii') for r in forms)
        bindings.append(dict(actor_ID=actor,source_andcurrent_fields=fields,current_consumers=forms,fresh=actor in fresh))
        names.append(dict(id=f'ACTOR{actor}_RAFAEL161_165_NAME',actor_ID=actor,kind='progressive-nameplate',
            english=expected,speaker=expected,source_meaning='Public name or role from the clean actor fields.',
            context='Public speaker label for the complete Rafael SC0 B161–B165 exchanges.',
            decision='retention',retention_reason=reason,finding=reason,localization_note=reason,
            source_reference=dict(actor_ID=actor,fields=[f['source'] for f in fields]),
            current_reference=dict(actor_ID=actor,consumer='progressive-nameplate',text_hex=forms[0]['text_hex']),
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),new_credit=0))
    items=[]
    for offset,source,english in [(1176184,'模様入りの布','Patterned Cloth'),(1176352,'真鍮のランプ','Brass Lamp')]:
        r=next(r for r in load(ITEMS)['records'] if r['offset']==offset)
        sp,cp=[struct.unpack_from('<I',arm,offset)[0] for arm in [jp,ctx.arm]]
        sj,ce=string(jp,sp),string(ctx.raw,cp)
        assert sj['text']==source and ce['text']==r['english']==english
        items.append(dict(id=r['id'],offset=offset,source=sj,current=ce))
    story={r['id']:r for r in load(STORY)['records']}
    terms=[]
    for key,phrase in [('DK4_MES_B141_R0073','Hayreddin'),('DK4_MES_B141_R0107',"Pasha's forces"),
        ('DK4_MES_B150_R0118','seven Proofs'),('DK4_MES_B152_R0050','The Estado')]:
        row=story[key]
        assert phrase in row['editorial_logical_English'] and all(row['review'].values())
        terms.append(dict(id=key,phrase=phrase,source_reference=row['source_reference'],registered_reference=row['planned_integrated_reference']))
    proof=next(r for r in load(HELP)['records'] if r.get('heading')=='Proof of Conquest')
    assert all(proof['review'].values())
    evidence={str(p):sha(p.read_bytes()) for p in [CURRENT,PRIOR,MACROS,ADAPTER,ITEMS,STORY,HELP,Path(__file__)]}
    save(NAMES,dict(format='dk4-scoped-name-contextual-review-v2',translation_policy='natural-dialogue-v2',
        target_locale='en-US',encoder='dialogue-relocatable-v1',records=names,
        review_gates=['source','context','localization','naturalness','formatting'],all_name_formatting_gates_pending=True,
        runtime=rt,new_credit=0,no_global_name_table_changes=True,evidence=evidence))
    save(OUT,dict(runtime=rt,actors=sorted(REASONS),name_bindings=bindings,fresh_actors=fresh,
        exact_reused_actors=sorted(set(REASONS)-set(fresh)),items=items,approved_story_terms=terms,
        Proof_of_Conquest_help_record=proof['id'],scoped_names=str(NAMES),scoped_names_sha256=sha(NAMES.read_bytes()),
        **{key:macros[key] for key in ['complete_ARM9_COMMON_font_andactor0_macro_dependencies_qualified',
            'same_Rafael_default_macro_proof','same_Rafael_default_macro_proof_sha256','macro_ascii_lengths']},
        no_new_visual_gameplay_orcatalogue_UI_claim=True,new_credit=0,evidence=evidence))
    print('Eight public labels bound, five exact name reuses and three fresh getter pairs. Two item fields and five term references verified.')

if __name__=='__main__':
    main()
