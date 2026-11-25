"""Resolve241 prose holds with scoped native identities, role0 and actual item pointers."""
import struct
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.main_pool_cache_visibility import BASE
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime

OLD=Path('translations/rafael_B101_B120_contextual_prose_review_v1.json')
NEW=Path('translations/rafael_B101_B120_contextual_editorial_manuscript_v2.json')
NAMES=Path('translations/rafael_B101_B120_scoped_names_androles_v1.json')
CURRENT=Path('work/analysis/Rafael_B101_B120_current678_20261105/current_effective.json')
FRESH=Path('work/analysis/Rafael241_new_name_bindings_20261105/names.json')
DYNAMIC=FRESH.with_name('dynamic207.json')
PRIOR=Path('work/analysis/Rafael261_names_terms_20261105/names_macros_andconsumer_dependency_qualification_v1.json')
OUT=Path('work/analysis/Rafael241_names_terms_20261105')
REASONS={
0:'Retain approved Rafael Castor andthe captain0 identity; no new family orrank is inferred.',
4:'Retain Janus Pasar, consistent withthe original phonetic components andhis established scholarly voice.',
5:'Retain Claudio Manaus; preserve the explicit Clau nickname inRafael\'s direct praise without replacing his full public name.',
6:'Retain Julio Erneco. Here the clean dialogue explicitly identifies Cristina ashis granddaughter; this doesnot make himRafael\'s grandfather.',
8:'Retain Arcadius Eudoxios andthe distinct full-catalogue middle component Eirene. No new gender,identity revelation orbiography is inferred fromthe name.',
12:'Retain Yukihisa Shiraki; his formal blade admiration doesnot require aninvented warrior title.',
14:'Retain Emilio Ferog andhis simple,enthusiastic food-focused voice.',
22:'Retain Samwell Khan andfull-catalogue Samwell da Khan. The established readable phonetic adaptation hasno concrete identity/readability defect; the casual rumor enthusiast isnot renamed tofit a presumed nationality.',
75:'Retain Hans Letzel, the actual current public spelling matching the source ハンス・レッツェル. Do not silently import anolder Retzel prose spelling oradd a rank tohis endorsement.',
135:'Retain Priest for祭主, the ritual/temple officiant. The generic public label doesnot make hima Christian priest; his temple dialogue supplies the setting.',
137:'Retain Senior Monk for高僧. Seniority isexplicit inthis source role rather thanan invented relationship orofficial court rank.',
139:'Retain Priest for神父 inthese church conversations; unused European metadata isnot part ofthe public label.',
151:'Retain Sailor, the original andcurrent progressive public getter result. Do not expose unused Retainer/nationality catalogue metadata ashis dialogue header.',
160:'Retain Villager for村民. The speaker\'s own religious history belongs inthe conversation,not aninvented sect orregional label.',
177:'Retain Sect Leader for教祖 inthis self-proclaimed religious group. The pompous research-society title belongs inthe speech; no outside church office isadded.',
178:'Retain Follower for信徒. A collective cheer canuse the source public singular role without inventing a named cult member.',
188:'Retain Margrete forマルグレーテ, the source-defined named informant. Hamburg isunused secondary metadata,not a surname ornew spoken description.',
191:'Retain Donna forドナ, the source-defined named informant. Seville isunused regional metadata,not a surname orrelationship label.'
}


def string(raw,pointer):
    if not pointer:return b''
    at=pointer-BASE
    assert 0<=at<len(raw)
    return raw[at:raw.index(0,at)]


def main():
    assert not OUT.exists() and not NEW.exists() and not NAMES.exists()
    old,current,fresh,dynamic,prior=map(load,[OLD,CURRENT,FRESH,DYNAMIC,PRIOR])
    rt=current['runtime'];ctx=RegisteredRuntime(rt['release_proof'],rt['startup_proof'],captain=0)
    assert rt==ctx.receipt()==fresh['runtime']==dynamic['runtime']
    prev=RegisteredRuntime(prior['runtime']['release_proof'],prior['runtime']['startup_proof'],captain=0)
    assert ctx.arm==prev.arm and ctx.common==prev.common and ctx.actor_root==prev.actor_root and ctx.actor_bytes==prev.actor_bytes
    assert ctx.image.read_file('/GRP/KANJI.FNT')==prev.image.read_file('/GRP/KANJI.FNT')
    actors=sorted({r['source_selector'] for g in current['groups'] for r in g['records'] if r['source_selector']<207})
    assert actors==sorted(REASONS) and len(actors)==18
    assert dynamic['source_selectors']==[207] and len(dynamic['source_records'])==12
    role=dynamic['native_roles']['rows'][0]
    assert role['source_selector']==207 and role['role_index']==0 and role['resolved_actor_ID']==0
    assert dynamic['native_roles']['all_actor_role_RNG_and_unowned4MiB_exact']
    clean=NdsImage.open('work/clean.nds');jp=clean.read_file('/__arm9__.bin')
    a,b=[struct.unpack_from('<I',arm,0xCDAC0)[0]-BASE for arm in [jp,ctx.arm]]
    prior_by={r['actor_ID']:r for r in prior['name_bindings']}
    bindings=[];names=[];fresh_count=reused_count=0
    for actor in actors:
        fields=[]
        for col in [0,4,8]:
            at,source_at=b+32*actor+col,a+32*actor+col
            pointer,source_pointer=struct.unpack_from('<I',ctx.arm,at)[0],struct.unpack_from('<I',jp,source_at)[0]
            sr,cr=string(jp,source_pointer),string(ctx.raw,pointer)
            fields.append(dict(column=col,source=dict(field_offset=source_at,pointer=source_pointer,hex=sr.hex(),text=sr.decode('cp932')),
                current=dict(field_offset=at,pointer=pointer,hex=cr.hex(),text=cr.decode('cp932'))))
        if actor in fresh['actors']:
            forms=[r for r in fresh['current_names']['rows'] if r['actor_ID']==actor]
            source_forms=[r for r in fresh['clean_names']['rows'] if r['actor_ID']==actor]
            path=FRESH;qualification='Fresh clean/current intrinsic getters; current fullARM9 differs from older proofs oractor isnewly scoped.'
            fresh_count+=1
        else:
            item=prior_by[actor]
            assert fields==item['source_andcurrent_fields']
            forms=item['current_consumers'];source_forms=item.get('clean_consumers',[])
            path=PRIOR;qualification='Exact ARM9/COMMON/font/complete actor-array andfield qualification ofprior intrinsic getters.'
            reused_count+=1
        assert len(forms)==2 and {r['consumer'] for r in forms}=={'progressive-nameplate','full-catalogue'}
        public=next(r for r in forms if r['consumer']=='progressive-nameplate')
        if actor==151:assert public['text']=='Sailor'
        bindings.append(dict(actor_ID=actor,source_andcurrent_fields=fields,current_consumers=forms,clean_consumers=source_forms,
            native_proof=str(path),native_proof_sha256=sha(path.read_bytes()),qualification=qualification))
        reason=REASONS[actor]
        names.append(dict(id=f'ACTOR{actor}_RAFAEL101_120_NAME',actor_ID=actor,kind='progressive-nameplate',english=public['text'],
            speaker=public['text'],context='Complete reviewed Rafael B101–B120 exchanges; ordinary public identity only.',
            source_meaning='Source-defined personal name orpublic role fromexact source fields andnative getters.',
            decision='retention',finding=reason,retention_reason=reason,localization_note=reason,
            source_reference=dict(actor_ID=actor,fields=[r['source'] for r in fields]),
            current_reference=dict(actor_ID=actor,consumer='progressive-nameplate',text_hex=public['text_hex'],native_proof=str(path),native_proof_sha256=sha(path.read_bytes())),
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),new_credit=0))
    assert (fresh_count,reused_count)==(11,7)
    catalogue=Path('translations/all_item_names_arm9_v1.json');items=[]
    wanted={'Muramasa','Peacock Mail',"Jaguar God's Vest",'Minerva Shield',"Hestia's Pot",'Aristarchus Telescope','Rigveda'}
    for item in load(catalogue)['records']:
        if item.get('english') not in wanted:continue
        at=item['offset'];sp,cp=[struct.unpack_from('<I',buf,at)[0] for buf in [jp,ctx.arm]]
        assert jp[at:at+4].hex()==item['source_hex'].lower()
        sr,cr=string(jp,sp),string(ctx.raw,cp)
        assert cr.decode('ascii')==item['english']
        items.append(dict(id=item['id'],pointer_field=at,source_pointer=sp,source_hex=sr.hex(),Japanese=sr.decode('cp932'),
            current_pointer=cp,current_hex=cr.hex(),English=item['english'],actual_verified_own_RAM_not_assumed_flat_ARM9=True,
            no_new_item_card_gameplay_oritem_mechanic_claim=True))
    assert len(items)==7
    society=Path('translations/hodram_B111_B130_contextual_final_review_v1.json')
    society_row=next(r for r in load(society)['records'] if '古代巨石文明研究会' in r.get('source_Japanese',''))
    assert 'Ancient Megalithic Civilization Research Society' in society_row['english']
    OUT.mkdir();identity=OUT/'names_terms_roles_andconsumer_dependency_qualification_v1.json'
    save(identity,dict(runtime=rt,actors=actors,name_bindings=bindings,fresh_actors=11,qualified_reused_actors=7,
        dynamic_selectors=[207],dynamic_binding=str(DYNAMIC),dynamic_binding_sha256=sha(DYNAMIC.read_bytes()),dynamic_role0=role,
        dynamic_context_is_current_startup_not_original_conditional_scene_participation=True,no_static_actor207_table_lookup=True,
        complete_ARM9_COMMON_font_andactor0_macro_dependencies_qualified=True,
        same_Rafael_default_macro_proof=prior['same_Rafael_default_macro_proof'],same_Rafael_default_macro_proof_sha256=prior['same_Rafael_default_macro_proof_sha256'],
        macro_ascii_lengths=dict(FI=6,FA=6,FO=10),lexical_items=items,
        society_term=dict(reference=str(society),id=society_row['id'],source_reference=society_row['source_reference'],
            English='Ancient Megalithic Civilization Research Society',complete_source_name_andprevious_individual_review_agree=True),
        other_source_terms=dict(Suryavarman_II='Faithful standard readable rendering ofスールヤバルマン２世; source purpose clause doesnot prove deification.',
            Vishnu='Faithful established deity-name rendering ofヴィシュヌ; noattributes added.',
            Vedas='Renderヴェーダ consistently; Rigveda isthenative specific item title,but thedialogue doesnot explicitly name thatitem.',
            Clau='Preserve theexplicitクラウ nickname intwo alternative praise lines.',
            Cristina='Matches actor7 inqualified prior name binding; preserve Julio\'s explicitly sourced granddaughter relationship.'),
        no_new_name_data_orcomplete_global207_approval=True,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [OLD,CURRENT,FRESH,DYNAMIC,PRIOR,catalogue,society,Path('docs/glossary.md'),Path(__file__)]}))
    save(NAMES,dict(format='dk4-scoped-name-contextual-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        encoder='dialogue-relocatable-v1',records=names,public_name_records=18,individual_retentions=18,new_name_data_changes=0,
        native_binding=str(identity),native_binding_sha256=sha(identity.read_bytes()),all_scoped_name_planes_andrepresentative_actual_headers_pending=True,
        full_catalogue_UI_andglobal207_review_open=True,new_credit=0,guide_photos=False))
    doc=deepcopy(old);byactor={r['actor_ID']:r for r in names};changes=[]
    for row in doc['records']:
        before=row['english'];after=before
        for first,second in [("Minerva's Shield",'Minerva Shield'),('Tunic of the Jaguar God',"Jaguar God's Vest"),
            ('a tunic','a vest'),('the tunic','the vest'),("Aristarchus's Telescope",'Aristarchus Telescope'),
            ("Hestia's Cauldron","Hestia's Pot"),("Hestia's... Cauldron?","Hestia's... Pot?"),('a cauldron','a pot')]:
            after=after.replace(first,second)
        if row['id']=='DK4_MES_B105_R0034':after="Hestia's... Pot?"
        if after!=before:
            row.update(previous_reviewed_English=before,previous_reviewed_decision=row['decision'],english=after,decision='revision',retention_reason=None)
            row['finding']+=' Align the spoken item term withthe actual native catalogue while preserving descriptive source wording.'
            row['localization_note']=row['finding'];changes.append(dict(id=row['id'],before=before,after=after))
        if row['kind']!='typed-choice-label':
            selector=row['source_selector']
            row['speaker']=('Captain selected byruntime role0 (Rafael inverified own context)' if selector==207 else
                'Sphinx' if selector==254 and row['block']==114 else 'FE temple/Colosseum presenter' if selector==254 and row['block'] in [113,118] else
                'FE description/inscription/injury notice' if selector==254 else byactor[selector]['english'])
            row['source_record_index']=row['source_reference']['record_index']
            row['source_native_extent']=row['native_extent']
            row['planned_English_markup']='{SPEAKER:'+format(selector,'02X')+'}'+row['english']
            row['native_name_controls_andterm_binding_pending']=False
            if selector==254:
                row['source_FE_presentation_kind']=row['speaker']
                row['FE_is_not_an_ordinary_actor_nameplate']=True
                row['source_leading_blank_rows']=len(row['source_Japanese'])-len(row['source_Japanese'].lstrip('\n'))
                if row['source_leading_blank_rows']:
                    row['source_vertical_staging_not_copied_into_logical_prose']=True
                    row['fresh_FE_pagination_andmenu_transition_review_required']=True
            if selector==207:
                row['source_dynamic_speaker_binding_pending']=False
                row['native_dynamic_identity_proof']=str(DYNAMIC)
                row['no_fixed_identity_inferred_for_dynamic_selector']=True
        row['current_name_andterm_bindings_pending']=[]
        row['review'].update(localization=True)
        row['source_name_term_control_andformatting_binding_pending']=False
        row['all_fresh_display_andregistered_integration_pending']=True
    doc.update(format='dk4-natural-dialogue-v2-editorial-manuscript',pending_name_term_IDs=[],
        scoped_identity_proof=str(identity),scoped_identity_proof_sha256=sha(identity.read_bytes()),
        source_context=str(CURRENT),source_context_sha256=sha(CURRENT.read_bytes()),
        all241_individual_four_prose_gates_pass=True,four_gate_passes=241,all_fifth_formatting_gates_pending=True,
        proposed_revisions=sum(r['decision']=='revision' for r in doc['records']),justified_retentions=sum(r['decision']=='retention' for r in doc['records']),
        lexical_alignment_changes=changes,previous_prose_review=str(OLD),previous_prose_review_sha256=sha(OLD.read_bytes()))
    assert all(r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in doc['records'])
    assert len(doc['records'])==241 and all(r['english'].isascii() for r in doc['records'])
    save(NEW,doc)
    print(dict(source_objects=241,revisions=doc['proposed_revisions'],retentions=doc['justified_retentions'],four_gates=241,
        native_names=18,fresh_name_getters=11,reused_name_getters=7,dynamic_role0=role['resolved_actor_ID'],lexical_changes=len(changes),formatting_approved=0,new_credit=0))


if __name__=='__main__':main()
