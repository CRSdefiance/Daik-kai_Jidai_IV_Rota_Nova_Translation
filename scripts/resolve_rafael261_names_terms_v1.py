"""Resolve32 linguistic holds against clean/current getters and registered native text data."""
import struct
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.main_pool_cache_visibility import BASE
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Rafael261_names_terms_20261105')
OLD=Path('translations/rafael_B85_B100_contextual_prose_review_v1.json')
NEW=Path('translations/rafael_B85_B100_contextual_editorial_manuscript_v2.json')
NAMES=Path('translations/rafael_B85_B100_scoped_names_androles_v1.json')
P330=Path('work/analysis/Rafael_B81_B84_formatting_20261105/scoped_names_macro_andconsumer_dependency_qualification_v1.json')
FRESH=[Path('work/analysis')/folder/'names.json' for folder in [
    'Rafael_B85_B100_new_name_bindings_20261105','Rafael_B85_B100_three_changed_dependency_name_bindings_20261105']]
META=Path('work/analysis/Rafael_B85_B100_clean_drafts_20261105/20_scoped_name_metadata_andpending_bindings.json')
REASONS={
0:'Retain user-approved Rafael Castor. Both source components and the qualified captain0 substitutions agree.',
4:'Retain Janus Pasar for the clean phonetic components and established public identity. His polite conversational voice adds no rank.',
5:'Retain Claudio Manaus. The explicit familiar shortening Clau is preserved where the source uses it; it does not replace the full nameplate.',
6:'Retain Julio Erneco. Neither these exchanges nor familiar forms of address create a family relationship with Rafael or Charles.',
7:'Retain Cristina Erneco, consistent with the reviewed source identity and the preceding recruitment/rescue exchanges.',
12:'Retain Yukihisa Shiraki in the ordinary nameplate and Yukihisa Genjo Shiraki in the explicit full introduction. Both original getters establish the distinct middle-name scope.',
13:'Retain Cesare Tony, already individually justified in the Lil223 name review. The phonetic pair is readable and has no established identity/readability defect. Do not invent a nationality or claim an independently verified Latin surname.',
14:'Retain Emilio Ferog. His simple, food-focused speech is distinct from broken English or a newly invented nickname.',
15:'Retain Angelo Puccini. The source Italian exclamation and teasing belong in his dialogue, without adding a nationality to the label.',
16:'Retain Gerhard Adernkatz. His source admiral status is separate from his ordinary name, and his personal sword recollection uses first person.',
18:'Retain Charles Rochefort in the nameplate and Charles Jean Rochefort in the full catalogue. Preserve the source middle-name ordering without imposing it on every spoken reference.',
20:'Retain Fernando Dias. The source reward notices explicitly name Fernando; those names must not become an ambiguous His.',
26:'Retain Julian Lopes for the clean phonetic components and existing native identity. His romantic rivalry is his own interpretation, not an established relationship.',
41:'Retain Sojin Kurushima. His emphatic spoken Kurushima self-reference matches the source surname, without adding a shogun or other rank.',
108:'Retain Trader for the original trading-house role. Familiar older-man language is not Father, and unused Native metadata is not part of the returned public name.',
109:'Retain Shipwright for the source shipyard man. Charles’s older-man greeting does not make them relatives; unused European metadata is not displayed.',
114:'Retain Port Worker for the source port role. The familiar older-brother form is not literal kinship or a new official rank.',
151:'Retain Sailor: both original and current progressive getters return the public 水夫/Sailor role. The separate catalogue 配下/Retainer metadata is not the visible dialogue label.',
152:'Retain Sailor for the former sailor in the miracle encounter: the clean public getter explicitly returns 水夫. Do not substitute the unused Retainer field or invent an employer.',
158:'Retain Sailor for Kurushima’s subordinate because the clean public getter explicitly returns 水夫. The boss relationship is in the conversation; it does not justify replacing the source public role with raw Retainer metadata.',
}

def terminated(raw,at):
    assert 0<=at<len(raw)
    return raw[at:raw.index(0,at)+1]

def main():
    assert not ROOT.exists() and not NEW.exists() and not NAMES.exists()
    old=load(OLD);metadata=load(META);prior=load(P330);fresh=list(map(load,FRESH))
    runtime=fresh[0]['runtime'];assert runtime==fresh[1]['runtime']
    current_path=Path(runtime['candidate']);assert sha(current_path.read_bytes())==runtime['candidate_sha256']
    current=NdsImage.open(current_path);arm=current.read_file('/__arm9__.bin')
    ram_path=Path(runtime['snapshot']['path']);ram=ram_path.read_bytes()
    assert sha(ram)==runtime['snapshot']['sha256'] and sha(arm)==runtime['ARM9_sha256']
    clean=NdsImage.open('work/clean.nds');jp=clean.read_file('/__arm9__.bin')
    assert prior['runtime']['ARM9_sha256']==runtime['ARM9_sha256'] and prior['runtime']['COMMON_sha256']==runtime['COMMON_sha256']
    earlier=NdsImage.open(prior['runtime']['candidate'])
    assert all(earlier.read_file(p)==current.read_file(p) for p in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT'])
    qualified=Path('work/analysis/Rafael330_current675_dependency_qualification_20261105.json')
    assert load(qualified)['all_relevant_Rafael330_renderer_macro_name_andSC0_input_dependencies_unchanged']
    assert load(qualified)['own_captain0_route0_actor_root_andcomplete_actor_array_exact']
    fresh_by={a:(p,d) for p,d in zip(FRESH,fresh,strict=True) for a in d['actors']}
    old_by={r['actor_ID']:r for r in prior['name_bindings']}
    names=[];bindings=[]
    for meta in metadata['actors']:
        actor=meta['actor_ID'];fields=meta['fields']
        for f in fields:
            for buf,key in [(jp,'source'),(ram,'current')]:
                at=f[key]['field_offset'];pointer=struct.unpack_from('<I',buf,at)[0]
                assert pointer==f[key]['pointer'] and terminated(buf,pointer-BASE)[:-1].hex()==f[key]['hex'] if pointer else f[key]['hex']==''
        if actor in fresh_by:
            path,proof=fresh_by[actor];assert proof['runtime']==runtime
            current_forms=[r for r in proof['current_names']['rows'] if r['actor_ID']==actor]
            source_forms=[r for r in proof['clean_names']['rows'] if r['actor_ID']==actor]
            scope='fresh clean/current intrinsic getters; no new gameplay or header pixels'
        else:
            item=old_by[actor];path=P330
            for field,previous in zip(fields,item['source_andcurrent_fields'],strict=True):
                assert field['column']==previous['column']
                assert field['source']['field_offset']==previous['source_field'] and field['source']['hex']==previous['source_hex']
                assert field['current']['field_offset']==previous['current_field'] and field['current']['hex']==previous['current_hex']
                assert field['current']['pointer']==previous['current_pointer']
            current_forms=item['current_consumers'];source_forms=[]
            scope='exact qualified current getter reuse: identical ARM9/COMMON/font, fields and complete actor model'
        assert len(current_forms)==2 and {r['consumer'] for r in current_forms}=={'progressive-nameplate','full-catalogue'}
        public=next(r for r in current_forms if r['consumer']=='progressive-nameplate')
        if actor in [151,152,158]:
            assert public['text']=='Sailor'
            if source_forms:assert next(r for r in source_forms if r['consumer']=='progressive-nameplate')['text']=='水夫'
        bindings.append(dict(actor_ID=actor,source_andcurrent_fields=fields,current_consumers=current_forms,
            clean_consumers=source_forms,native_proof=str(path),native_proof_sha256=sha(path.read_bytes()),qualification=scope))
        names.append(dict(id=f'ACTOR{actor}_RAFAEL85_100_NAME',actor_ID=actor,kind='progressive-nameplate',english=public['text'],
            speaker=public['text'],context='The complete reviewed Rafael B85–B100 exchanges; ordinary public label only.',
            source_meaning='Source-defined personal name or public occupational role from the original fields/getter.',
            localization_note=REASONS[actor],finding=REASONS[actor],decision='retention',retention_reason=REASONS[actor],
            source_reference=dict(binding=str(META),binding_sha256=sha(META.read_bytes()),actor_ID=actor,fields=[f['source'] for f in fields]),
            current_reference=dict(actor_ID=actor,native_proof=str(path),native_proof_sha256=sha(path.read_bytes()),
                text_hex=public['text_hex'],consumer='progressive-nameplate'),
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            full_catalogue_UI_andglobal207_review_not_approved=True,new_credit=0))
    assert len(names)==20 and {r['actor_ID'] for r in names}==set(REASONS)
    catalogue_path=Path('translations/all_item_names_arm9_v1.json');catalogue=load(catalogue_path);items=[]
    wanted={'Tomato Seedling','Sweeping Katzbalger','Ninja Garb','Miracle Bullet Charm','Silla Gold Crown'}
    for item in catalogue['records']:
        if item.get('english') not in wanted:continue
        at=item['offset'];source_pointer=struct.unpack_from('<I',jp,at)[0];pointer=struct.unpack_from('<I',arm,at)[0]
        assert jp[at:at+4].hex()==item['source_hex'].lower()
        source_raw=terminated(jp,source_pointer-BASE);raw=terminated(ram,pointer-BASE)
        assert raw[:-1].decode('ascii')==item['english']
        items.append(dict(id=item['id'],pointer_field=at,source_pointer=source_pointer,source_hex=source_raw.hex(),
            Japanese=source_raw[:-1].decode('cp932'),current_pointer=pointer,current_hex=raw.hex(),English=item['english'],
            current_value_from_verified_snapshot_not_assumed_flat_ARM9=True,item_getter_inventory_card_andmechanic_not_retested=True))
    assert len(items)==5
    mihwa_field=0x1224A0
    source_pointer,pointer=[struct.unpack_from('<I',a,mihwa_field)[0] for a in [jp,arm]]
    source_raw,raw=terminated(jp,source_pointer-BASE),terminated(ram,pointer-BASE)
    assert source_raw[:-1].decode('cp932')=='美華' and raw==b'Mihwa\0'
    mihwa=dict(source_field=mihwa_field,source_pointer=source_pointer,source_hex=source_raw.hex(),Japanese='美華',
        current_pointer=pointer,current_hex=raw.hex(),English='Mihwa',
        prior_observed_native_name_reference='docs/primary_town_services_v2058_checkpoint.md',
        choice='Use the established native Mihwa in story references. Do not infer nationality or a new Mandarin spelling from the Hangzhou setting.')
    zip_at=ram.find(b'Zipangu.\0');assert zip_at>=0
    reference=Path('translations/common_mystery_items_v1_native_v100_repack_v103.json')
    record=next(r for r in load(reference)['records'] if 'golden Zipangu' in r['english'])
    zipangu=dict(source_Japanese='ジパング',English='Zipangu',native_snapshot_offset=zip_at,
        current_bytes=ram[zip_at:zip_at+9].hex(),registered_reference=str(reference),registered_reference_ID=record['id'],
        choice='Use the existing registered Zipangu form consistently in this scene; this is a text-data binding, not a newly observed location label.')
    ROOT.mkdir()
    evidence=[OLD,META,P330,*FRESH,qualified,catalogue_path,reference,Path('docs/glossary.md'),
        Path('translations/lil_B223_speaker_name_review_v1.json'),Path('docs/primary_town_services_v2058_checkpoint.md'),Path(__file__)]
    identity=ROOT/'names_macros_andconsumer_dependency_qualification_v1.json'
    save(identity,dict(runtime=runtime,actors=sorted(REASONS),name_bindings=bindings,fresh_actors=12,qualified_reused_actors=8,
        full_current_getter_dependency_change_for_three_older_proofs_justified_fresh_execution=True,
        same_Rafael_default_macro_proof=prior['same_Rafael_default_macro_proof'],
        same_Rafael_default_macro_proof_sha256=prior['same_Rafael_default_macro_proof_sha256'],
        macro_ascii_lengths=dict(FI=6,FA=6,FO=10),complete_ARM9_COMMON_font_andactor0_macro_dependencies_qualified=True,
        no_new_macro_stress_execution_orordinary_nameplate_gameplay_claim=True,
        lexical_items=items,Mihwa=mihwa,Zipangu=zipangu,
        generic_Katzbalger_reference_doesnot_add_the_unspoken_Sweeping_item_epithet=True,
        Ninja_Garb_keeps_black_description_androgue_context_incomplete_exchange=True,
        new_credit=0,evidence={str(p):sha(p.read_bytes()) for p in evidence}))
    save(NAMES,dict(format='dk4-scoped-name-contextual-review-v1',translation_policy='natural-dialogue-v2',
        target_locale='en-US',encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],
        records=names,public_name_records=20,individual_retentions=20,new_name_data_changes=0,
        all20_name_planes_andrepresentative_actual_headers_pending=True,full_catalogue_UI_andglobal207_review_open=True,
        native_binding=str(identity),native_binding_sha256=sha(identity.read_bytes()),new_credit=0,guide_photos=False))
    doc=deepcopy(old);byactor={r['actor_ID']:r for r in names};changes=[]
    for row in doc['records']:
        before=row['english'];after=before.replace('Meihua','Mihwa')
        if row['id']=='DK4_MES_B87_R0005':after=after.replace('Zipang','Zipangu')
        if row['id']=='DK4_MES_B91_R0070':after="A Miracle Bullet Charm. It's said to bring miracles."
        if row['id']=='DK4_MES_B97_R0047':after="I hear it's an all-black outfit called Ninja Garb. And it's actually armor, not just clothing!"
        if row['id']=='DK4_MES_B86_R0199':after=after.replace('Claudio!','Clau!')
        if after!=before:
            previous_decision=row['decision'];row.update(english=after,decision='revision',retention_reason=None,
                previous_reviewed_English=before,previous_reviewed_decision=previous_decision)
            note=('Align the referenced name or item with its exact native lexical binding while preserving the complete Japanese exchange.'
                if row['id']!='DK4_MES_B86_R0199' else 'Preserve the explicit source nickname クラウ as the already-reviewed Clau, without changing the ordinary Claudio nameplate.')
            row['finding']=row['localization_note']=note;changes.append(dict(id=row['id'],previous=before,current=after,reason=note))
        row['review']['localization']=True;row['current_name_andterm_bindings_pending']=[]
        row['scoped_names_terms_andsource_aliases_binding']=dict(path=str(identity),sha256=sha(identity.read_bytes()))
        if row['kind']!='typed-choice-label':
            if row['source_selector']!=254:row['speaker']=byactor[row['source_selector']]['english']
            row.update(source_record_index=row['source_reference']['record_index'],current_record_index=row['current_reference']['record_index'],
                source_native_extent=row['native_extent'],planned_English_markup='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+row['english'])
            if row['source_selector']==254:row.update(source_FE_presentation_kind='stat reward notice' if row['block']==91 else 'animal-like cry',FE_is_not_an_ordinary_actor_nameplate=True)
        assert row['english'].isascii() and not row['review']['formatting']
        if row.get('source_macros'):
            assert all(row['english'].count('{MACRO:'+m+'}')==n for m,n in row['source_macros'].items())
    assert len(changes)==8 and sum(r['decision']=='revision' for r in doc['records'])==111
    assert sum(r['decision']=='retention' for r in doc['records'])==150
    doc.update(previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()),
        proposed_revisions=111,justified_retentions=150,four_gate_passes=261,pending_name_term_IDs=[],
        all261_individual_four_prose_gates_pass=True,all_fifth_formatting_gates_pending=True,
        scoped_identity_proof=str(identity),scoped_identity_proof_sha256=sha(identity.read_bytes()),
        current_comparison_packet=str(Path('work/analysis/Rafael_B85_B100_current_20261105/current_effective.json')),
        physical_speech_objects=255,ordinary_speech_objects=248,FE_speech_objects=7,typed_choice_objects=6,typed_choice_commands=3,
        resolved_name_term_binding_records=32,source_term_andalias_wording_refinements=changes,
        no_name_assets_orROM_orintegration_credit_changed=True,new_credit=0)
    save(NEW,doc);save(ROOT/'resolved32_linguistic_holds_and8_wording_refinements.json',dict(
        previous=str(OLD),current=str(NEW),current_sha256=sha(NEW.read_bytes()),resolved_holds=old['pending_name_term_IDs'],
        wording_refinements=changes,revised=111,retained=150,all261_four_prose_gates_pass=True,
        names_individually_retained=20,native_name_oritem_assets_changed=False,
        all_fresh_native_visual_stored_actual_andregistered_release_checks_pending=True,new_credit=0))
    print('Resolved32 holds:261 four-gate prose reviews(111 revisions/150 retentions),20 name retentions,12 fresh/8 reused getters. Fresh display remains.')

if __name__=='__main__':main()
