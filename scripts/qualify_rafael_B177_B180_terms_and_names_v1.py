"""Bind the four exchanges to exact current public names, rooms and equipment terms."""
from pathlib import Path
import struct
from dk4tool.patch.crew_role_labels import FIELD,ORIGINAL,ENGLISH
from dk4tool.patch.main_pool_cache_visibility import BASE
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.common_single_cache_v861 import entries as current_entries
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.qualify_rafael351_item_and_UI_terms_v1 import string
from scripts.prove_lil_B167_names_v4124b import names as original_names

A=Path('work/analysis')
CURRENT=A/'Rafael_B177_B180_current1424_20261105/current_effective.json'
OUT=CURRENT.with_name('names_and_terms_v1.json')
PRIOR=A/'Rafael261_names_terms_20261105/names_macros_andconsumer_dependency_qualification_v1.json'
ADAPTER=A/'Rafael_B61_B80_new_name_bindings_20261104/names.json'
ROOMS=A/'HELP_active_skill_labels_20261105/active_terms_binding_v2.json'
ROLES=A/'Shared_HELP_T103_T132_clean_20261104/native_roles_rooms_andskills_v1.json'
REFIT=Path('translations/refit_contextual_final_review_v1.json')
NAMES=Path('translations/rafael_B177_B180_scoped_names_review_v1.json')
CURRENT_COMMON_DIRECTORY='80d007e6b0f0a7eb60ec8d51d25211302371b763a3f49eea666044d49064cc3e'
REASONS={
    0:('Rafael Castor','Keep Rafael Castor in the header and preserve FI in direct address. His invitations do not assign a new rank or duty.'),
    4:('Janus Pasar','Keep Janus Pasar. His curiosity about fittings and explanation of the coin game express his expertise without a new title.'),
    5:('Claudio Manaus','Keep Claudio Manaus as the public name and Clau when the clean exchange uses his nickname.'),
    13:('Cesare Tony','Keep the approved Cesare Tony in both introductions and the header. Former ownership of the Elysion and a request to sail again do not imply a military rank.'),
    20:('Fernando Dias','Keep Fernando Dias. The last introduction says both names; his insight and luck are his own claims, not a new title.'),
    23:('Manuel Almeida','Keep Manuel Almeida in the header. His spoken introduction says Manuel only; the nameplate is no reason to add his surname to the speech.'),
    109:('Shipwright','Keep Shipwright for the existing role. The lesson establishes expertise without giving the instructor a new rank or proper name.'),
    164:('Man','Keep the established public Man label. The quarrel establishes a couple breaking up, not marriage or another status.'),
    165:('Woman','Keep the established public Woman label. Her line makes a choice to stop seeing him without inventing marriage or family.'),
}

if __name__=='__main__':
    assert not OUT.exists() and not NAMES.exists()
    current,prior,rooms,roles,refit,adapter=map(load,[CURRENT,PRIOR,ROOMS,ROLES,REFIT,ADAPTER])
    rt=current['runtime'];ctx=RegisteredRuntime(rt['release_proof'],rt['startup_proof'],captain=0);assert ctx.receipt()==rt
    pt=prior['runtime'];old=RegisteredRuntime(pt['release_proof'],pt['startup_proof'],captain=0)
    assert ctx.arm==old.arm and ctx.common==old.common and ctx.actor_root==old.actor_root and ctx.actor_bytes==old.actor_bytes
    assert ctx.image.read_file('/GRP/KANJI.FNT')==old.image.read_file('/GRP/KANJI.FNT')
    clean=NdsImage.open('work/clean.nds');jp=clean.read_file('/__arm9__.bin')
    assert sha(ctx.arm)==rooms['current_ARM9_sha256']==roles['current_ARM9_sha256']
    assert sha(jp)==rooms['source_ARM9_sha256']==roles['source_ARM9_sha256']
    source_ids={r['source_selector'] for g in current['groups'] for r in g['records']}
    assert source_ids=={*REASONS,254}
    oldnames={r['actor_ID']:r for r in prior['name_bindings']}
    fresh=sorted(source_ids-set(oldnames)-{254});assert fresh==[23,164,165]
    source=adapter['source_owned_current_adapter']
    env={**original_names.__globals__,'ACTORS':fresh};exec(compile(source,__file__+'::same-own-current-name-getters', 'exec'),env)
    new=ctx.execute(env['names']);assert len(new['rows'])==6
    a,b=[struct.unpack_from('<I',arm,0xCDAC0)[0]-BASE for arm in [jp,ctx.arm]]
    bindings=[];decisions=[]
    for actor,(expected,reason) in REASONS.items():
        fields=[]
        for column in [0,4,8]:
            sa,ca=a+32*actor+column,b+32*actor+column
            sp,cp=struct.unpack_from('<I',jp,sa)[0],struct.unpack_from('<I',ctx.arm,ca)[0]
            s=string(jp,sp) if sp else dict(pointer=0,hex='',text='')
            c=string(ctx.raw,cp) if cp else dict(pointer=0,hex='',text='')
            fields.append(dict(column=column,source=dict(field_offset=sa,**s),current=dict(field_offset=ca,**c)))
        if actor in fresh:
            forms=[r for r in new['rows'] if r['actor_ID']==actor];mode='Fresh original getters on exact own Rafael snapshot.'
        else:
            assert fields==oldnames[actor]['source_andcurrent_fields']
            forms=oldnames[actor]['current_consumers'];mode='Exact prior proof reuse: actor array, fields, ARM9, COMMON and font match.'
        assert len(forms)==2 and {r['consumer'] for r in forms}=={'progressive-nameplate','full-catalogue'}
        public=next(r for r in forms if r['consumer']=='progressive-nameplate')
        assert public['text']==expected and bytes.fromhex(public['text_hex']).decode('ascii')==expected
        bindings.append(dict(actor_ID=actor,source_andcurrent_fields=fields,current_consumers=forms,qualification=mode))
        decisions.append(dict(id=f'ACTOR{actor}_RAFAEL177_180_NAME',actor_ID=actor,kind='progressive-nameplate',
            english=expected,speaker=expected,source_meaning='Exact clean name or role fields; the complete exchange determines the appropriate public label.',
            context='Rafael SC0 B177–B180, no implied new rank, relationship or global rename.',
            decision='retention',retention_reason=reason,finding=reason,localization_note=reason,
            source_reference=dict(actor_ID=actor,fields=[f['source'] for f in fields]),
            current_reference=dict(actor_ID=actor,consumer='progressive-nameplate',text_hex=public['text_hex']),
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),new_credit=0))
    wanted={'個室','娯楽室','材木室','診察室','調理室','飼育室','礼拝室','副官室','積荷倉庫','海兵詰所','武装砲台','物資倉庫'}
    room_rows=[]
    for r in rooms['active_room_references']:
        s=r['source_label'];j=s['Japanese']
        if j not in wanted:continue
        p=struct.unpack_from('<I',ctx.arm,r['pointer_field'])[0]
        assert p==r['current_pointer'] and string(ctx.raw,p)['text']==r['current_text']
        assert string(jp,BASE+s['offset'])['hex']==s['source_hex']
        assert string(ctx.arm,BASE+s['offset'])['hex']==s['current_hex']
        room_rows.append(r)
    assert {r['source_label']['Japanese'] for r in room_rows}==wanted
    assert struct.unpack_from('<I',ctx.arm,FIELD)[0]==ENGLISH
    role_rows=[]
    for i in [1,5,11,12,13,14]:
        r=roles['native_roles'][i];assert r['index']==i
        src=struct.unpack_from('<I',jp,ORIGINAL-BASE+4*i)[0]
        dst=struct.unpack_from('<I',ctx.raw,ENGLISH-BASE+4*i)[0]
        assert (src,dst)==(r['source_pointer'],r['current_pointer'])
        assert string(jp,src)['hex']==r['source_hex'] and string(ctx.raw,dst)['hex']==r['current_hex']
        role_rows.append(r)
    speech=next(r for t in rooms['active_label_tables'] for r in t['records'] if r.get('Japanese')=='説得力')
    assert speech['English']=='Speech' and struct.unpack_from('<I',ctx.arm,speech['pointer_field'])[0]==speech['current_pointer']
    assert string(ctx.raw,speech['current_pointer'])['hex']==speech['current_hex']
    entries=current_entries(ctx.common,ctx.arm,CURRENT_COMMON_DIRECTORY);terms=[]
    for n in [1268,1269,1278,1280,1282,1286,1288]:
        r=next(r for r in refit['records'] if r['message_id']==n)
        e=entries[n];assert e.text.rstrip(b'\0').hex()==r['integrated_hex'].removesuffix('00')
        terms.append(dict(id=r['id'],text=r['english'],tested_payload_hex=e.text.hex(),integrated_reference=r['integrated_reference'],
            current_reference=dict(message_id=n,block=e.block,offset=e.block_offset)))
    ev={str(p):sha(p.read_bytes()) for p in [CURRENT,PRIOR,ADAPTER,ROOMS,ROLES,REFIT,Path(__file__)]}
    save(NAMES,dict(format='dk4-scoped-name-contextual-review-v2',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',
        review_gates=['source','context','localization','naturalness','formatting'],records=decisions,all_name_formatting_gates_pending=True,
        runtime=rt,no_global_name_table_changes=True,new_credit=0,evidence=ev))
    save(OUT,dict(runtime=rt,name_bindings=bindings,fresh_actors=fresh,exact_reused_actors=sorted(set(REASONS)-set(fresh)),
        scoped_name_review=str(NAMES),scoped_name_review_sha256=sha(NAMES.read_bytes()),active_room_references=room_rows,
        active_roles=role_rows,active_Speech=speech,refit_term_references=terms,public_name_records=9,
        current_COMMON_directory_sha256=CURRENT_COMMON_DIRECTORY,
        room_scope='Mate is the compact Deck label for the First Mate office. Use the actual room labels in tutorial instructions.',
        no_new_visual_gameplay_orcatalogue_UI_claim=True,new_credit=0,evidence=ev))
    print('Nine public names bound: six exact reuses, three original getter pairs. Verified 12 room labels, six roles, Speech and seven Refit strings.')
