"""Reuse exact current identity proofs andbind actual item/role/city data without edits."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.main_pool_cache_visibility import BASE
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.qualify_rafael351_item_and_UI_terms_v1 import string

ROOT=Path('work/analysis/Rafael557_names_terms_v1_20261105')
CURRENT=Path('work/analysis/Rafael_B141_B160_current867_20261105/current_effective.json')
PRIOR=Path('work/analysis/Rafael351_identity_note_alignment_v1_20261105/qualified_names_roles_andparticle_findings.json')
FRESH=Path('work/analysis/Rafael557_fresh_names_v2_20261105/names.json')
FERNAN=Path('work/analysis/Rafael867_extended_release_verified_v3_20261105/own_Fernan_name_getter_verification.json')
CLEAN_NAMES=Path('work/analysis/Rafael_B61_B80_new_name_bindings_20261104/names.json')
ITEMS=Path('translations/all_item_names_arm9_v1.json')
REASONS={
0:'Retain approved Rafael Castor. FU ishis dynamic full name,notpermission tohardcode thedefault name.',
4:'Retain Janus Pasar andhis explanatory voice;do not infer a newprofessional title fromhis artifact knowledge.',
5:'Retain Claudio Manaus andthe source Clau nickname;his bluntness,teasing andloyalty do not establish an unspoken relationship.',
6:'Retain Julio Erneco. His familiar kiddo address toRafael isnot kinship;the national-loyalty exchange explicitly identifies him asSpanish.',
7:'Retain Cristina Erneco fromthe exact source/current getters. Historic profile notes saying Charlie mustnot override the actual actor7 identity.',
8:'Retain public Arcadius Eudoxios andthe private Eirene component. The reveal establishes a woman using a male alias;do not globallyrename the public actor.',
19:'Retain Carlo Sinat withoutinventing a scholarly rank forthe alternate map reaction.',
25:'Retain approved Yifa Sol. Resolve provisional Ihwa toYifa inbody prose;the bamboo exchange addsno newbiography.',
30:'Retain public Dinis Albuquerque. Fullcatalogue デ stillneeds the separate source-qualified de pointer correction.',
35:'Retain Fernan Silveira andthe already corrected ASCII F. His naval title andpartnership are explicit inthe palace/tutorial exchange.',
37:'Retain Abraham Uddin publicly andAbraham Ibn Uddin infull. Company-leader address mustnot invent a specific naval promotion.',
39:'Retain Duarte Pereira andfull Duarte Lopes de Pereira. The source explicitly gives governor andadmiral titles;his divided loyalties mustnot beflattened into simple villainy.',
42:'Retain Vasquez Maldonado andfull Vasquez de Maldonado. Preserve the overheard rivalry withoutinventing the unfinished plan.',
54:'Retain Ibn Niyadi. Guiding the party doesnot justify replacing his proper name withan invented servant orrelative label.',
60:'Retain Juan Blanco. He isone ofEscante’s people inthis exchange;do not invent an additional officer rank.',
75:'Retain Hans Letzel. Doctor isexplicit inthe source address;old-man forms elsewhere are not a family relationship.',
92:'Retain Barkeep for酒場の親父. His local account doesnot establish a family tie,ethnicity ormilitary title.',
120:'Retain Guard for衛兵. The palace setting supports the role withoutinventing nobility ora personal name.',
142:'Retain Innkeeper for宿屋のおばさん. Rafael’s address isnot proof that she ishis aunt;keep the response asdirect gratitude.',
151:'Retain public Sailor;do not expose unused full-catalogue Retainer metadata asan ordinary dialogue label.',
}


def main():
    assert not ROOT.exists()
    current,prior,fresh,fern,oldclean=map(load,[CURRENT,PRIOR,FRESH,FERNAN,CLEAN_NAMES])
    ctx=RegisteredRuntime(current['runtime']['release_proof'],current['runtime']['startup_proof'],captain=0)
    assert current['runtime']==fresh['runtime']==fern['runtime']==ctx.receipt()
    previous=RegisteredRuntime(prior['runtime']['release_proof'],prior['runtime']['startup_proof'],captain=0)
    assert ctx.arm==previous.arm and ctx.common==previous.common
    assert ctx.actor_root==previous.actor_root and ctx.actor_bytes==previous.actor_bytes
    assert ctx.image.read_file('/GRP/KANJI.FNT')==previous.image.read_file('/GRP/KANJI.FNT')
    clean=NdsImage.open('work/clean.nds');jp=clean.read_file('/__arm9__.bin')
    assert sha(jp)==oldclean['clean_ARM9_sha256']==fresh['clean_ARM9_sha256']
    actors=sorted({r['source_selector'] for g in current['groups'] for r in g['records'] if r['source_selector']<207})
    assert actors==sorted(REASONS) and len(actors)==20
    a,b=[struct.unpack_from('<I',arm,0xCDAC0)[0]-BASE for arm in [jp,ctx.arm]]
    bindings=[];names=[]
    for actor in actors:
        fields=[]
        for column in [0,4,8]:
            sa,ca=a+32*actor+column,b+32*actor+column
            sp,cp=struct.unpack_from('<I',jp,sa)[0],struct.unpack_from('<I',ctx.arm,ca)[0]
            s=string(jp,sp) if sp else dict(pointer=0,hex='',text='')
            c=string(ctx.raw,cp) if cp else dict(pointer=0,hex='',text='')
            fields.append(dict(column=column,source=dict(field_offset=sa,**s),current=dict(field_offset=ca,**c)))
        if actor in fresh['actors']:
            source_forms=[r for r in fresh['clean_names']['rows'] if r['actor_ID']==actor]
            forms=[r for r in fresh['current_names']['rows'] if r['actor_ID']==actor]
            proof=FRESH;mode='fresh exact own-current native name/voice consumers'
        elif actor==35:
            source_forms=[r for r in oldclean['clean_names']['rows'] if r['actor_ID']==35]
            forms=fern['own_name_consumers']['rows'];assert all(r['actor_ID']==35 for r in forms)
            assert fern['original_progressive_andfull_catalogue_getters_read_corrected_normal_F_from_own_snapshot']
            proof=FERNAN;mode='existing exact current Fernan getters plus unchanged clean-source getter evidence'
        else:
            item=next(r for r in prior['name_bindings'] if r['actor_ID']==actor)
            assert fields==item['source_andcurrent_fields']
            source_forms,forms=item['clean_consumers'],item['current_consumers']
            proof=PRIOR;mode='exact ARM9/COMMON/font/complete actor-array/individual-field reuse'
        assert len(forms)==2 and {r['consumer'] for r in forms}=={'progressive-nameplate','full-catalogue'}
        public=next(r for r in forms if r['consumer']=='progressive-nameplate');assert public['text'].isascii()
        bindings.append(dict(actor_ID=actor,source_andcurrent_fields=fields,current_consumers=forms,clean_consumers=source_forms,
            native_proof=str(proof),native_proof_sha256=sha(proof.read_bytes()),qualification=mode))
        names.append(dict(id=f'ACTOR{actor}_RAFAEL141_160_NAME',actor_ID=actor,kind='progressive-nameplate',
            english=public['text'],speaker=public['text'],source_meaning='Source-defined proper name orpublic role fromexact fields/native consumers.',
            context='Complete SC0 B141–B160 exchanges;private aliases do not globallyreplace public labels.',
            decision='retention',finding=REASONS[actor],retention_reason=REASONS[actor],localization_note=REASONS[actor],
            source_reference=dict(actor_ID=actor,fields=[f['source'] for f in fields]),
            current_reference=dict(actor_ID=actor,consumer='progressive-nameplate',text_hex=public['text_hex'],native_proof=str(proof)),
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),new_credit=0))
    def field(offset):
        sp,cp=[struct.unpack_from('<I',arm,offset)[0] for arm in [jp,ctx.arm]]
        return dict(pointer_field_offset=offset,source=string(jp,sp),current=string(ctx.raw,cp),current_field_hex=ctx.arm[offset:offset+4].hex())
    wanted={'紅色の顔料','古びた羊皮紙','謎の石版上部','謎の石版下部','枯れないハスの葉','クシャナ朝の大皿',
        '古代王国の貨幣','乳液の入った壺','儀式用の小刀','太陽紋の鞘','唐代の竹細工','竹細工の組立絵図'}
    items=[]
    for registered in load(ITEMS)['records']:
        if 'english' not in registered:continue
        row=field(registered['offset'])
        if row['source']['text'] not in wanted:continue
        assert row['current']['text']==registered['english']
        row['registered_item_record']=registered['id'];items.append(row)
    assert {r['source']['text'] for r in items}==wanted and len(items)==12
    from dk4tool.patch.crew_role_labels import FIELD,ORIGINAL,ENGLISH
    table=struct.unpack_from('<I',ctx.arm,FIELD)[0];assert table==ENGLISH
    role_pointer=struct.unpack_from('<I',ctx.raw,table-BASE+4)[0]
    source_pointer=struct.unpack_from('<I',jp,ORIGINAL-BASE+4)[0]
    role=dict(index=1,source=string(jp,source_pointer),current=string(ctx.raw,role_pointer),
        source_pointer_field_offset=ORIGINAL-BASE+4,current_table_literal_offset=FIELD,current_table_literal_hex=ctx.arm[FIELD:FIELD+4].hex())
    assert role['source']['text']=='副官' and role['current']['text'].rstrip()=='First Mate'
    city=field(1192580);assert city['source']['text']=='サン＝ジョルジェ' and city['current']['text']=='Sao Jorge'
    ROOT.mkdir(parents=True)
    name_path=Path('translations/rafael_B141_B160_scoped_names_review_v1.json');assert not name_path.exists()
    save(name_path,dict(format='dk4-scoped-name-contextual-review-v2',translation_policy='natural-dialogue-v2',target_locale='en-US',
        encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],records=names,
        public_name_retentions=20,public_name_changes=0,all_name_formatting_gates_pending=True,
        global207_andfull_catalogue_UI_review_still_open=True,two_catalogue_de_fixes_still_pending=True,new_credit=0,guide_photos=False))
    save(ROOT/'names_terms_andconsumer_dependency_qualification.json',dict(runtime=ctx.receipt(),actors=actors,
        name_bindings=bindings,fresh_actors=fresh['actors'],exact_reused_actors=sorted(set(actors)-set(fresh['actors'])),
        exact_ARM9_COMMON_font_actor_array_andindividual_reused_fields=True,
        scoped_names=str(name_path),scoped_names_sha256=sha(name_path.read_bytes()),items=items,first_mate=role,Sao_Jorge=city,
        Eirene_is_private_native_middle_component_not_a_global_public_rename=True,Yifa_replaces_provisional_Ihwa=True,
        no_new_native_name_execution_for_reused_entries=True,no_native_display_orfont_plane_approval=True,
        no_ROM_RAM_registry_orprose_writes=True,new_credit=0,guide_photos=False,
        evidence={str(p):sha(p.read_bytes()) for p in [CURRENT,PRIOR,FRESH,FERNAN,CLEAN_NAMES,ITEMS,Path(__file__)]}))
    print('Bound20 scoped names:10 fresh/10 exactreuses,12 items,First Mate andSao Jorge. No name data changes,formatting orcredit.')
    for r in items:print(r['source']['text'],'=>',r['current']['text'])


if __name__=='__main__':main()
