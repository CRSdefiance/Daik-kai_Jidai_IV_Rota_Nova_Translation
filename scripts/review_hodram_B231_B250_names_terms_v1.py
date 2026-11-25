"""Bind scoped current names and terms; reuse unchanged source-name ABI and static fields."""
import inspect
import struct
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.audit_native_given_name_table import string
from scripts.bind_hodram_B191_B210_identities import cstring
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.prove_lil_B167_names_v4124b import names
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_hodram_B231_B250_contextual_v1 import CURRENT,OUT as PROSE
from scripts.prepare_hodram_B231_B250_scope_v1 import ROOT
from scripts.source_locked_derivation_v5118 import checked_text
from dk4tool.rom.nds import NdsImage
from dk4tool.script.arm9_profiles import WORLD_CITY_ENTRIES

NATIVE=ROOT/'scoped_names_current_v1.json'
REVIEW=Path('translations/hodram_B231_B250_scoped_names_review_v1.json')
TERMS=ROOT/'scoped_terms_v1.json'
ROLES=ROOT/'role_bindings_v1.json'
REASONS={
1:'Retain approved Hodram and Joakim with Bergstrom. The public name and full name intentionally differ. His officer’s voice does not add a rank to the label.',
4:'Retain Janus Pasar for ジェナス・パサー. Correct Gennas in the injured-hand dialogue to the same established identity.',
6:'Retain Julio Erneco for フリオ・エルネコ. His old-fashioned familiar voice does not justify elder as a self-name or a family relationship.',
11:'Retain Jam Ludwyan and full Jam Jack Ludwyan for the three source components. His full letter signature should not become Ludwayer.',
13:'Retain established readable Cesare Tony for チェザーレ・トーニ. His formal rant supplies no additional officer title or new biographical claim.',
18:'Retain Charles Rochefort and full Charles Jean Rochefort. The letter signature preserves the source middle component; do not append a noble particle or rank.',
19:'Retain Carlo Sinat for カルロ・シナート. The speaker’s medical interest and the earlier papal-trade scene identify the same companion, without a newly invented title.',
20:'Retain Fernando Dias, including the accepted complete ASCII initial and source given/surname forms. His boast is his own speech, not this man.',
22:'Retain Samwell Khan and full Samwell da Khan. The clean middle component is preserved in its established full-name consumer; his eager voice adds no age or relationship.',
23:'Retain Manuel Almeida. The practical art/tool joke does not justify naming him a sculptor, priest or new-ranked official.',
113:'Retain Port Worker for the familiar occupational 出港所の兄貴. The helpful stranger is not a brother, father or unproven senior harbor officer.',
139:'Retain Priest for 神父. Father in direct address is conventional clerical language, with no biological relationship implied. European metadata is not a surname.',
147:'Retain Guildmaster for ギルドの元締め. The survey commission uses the explicit guild role; regional metadata supplies no personal name.',
151:'Retain Sailor in the progressive consumer and Retainer in the full-name consumer. This is the unchanged unassigned-role fallback for selector208 at startup, not a new roster assignment or actual conditional participant.',
186:'Retain the accepted repaired Francisca spelling for フランシスカ. The stolen birthday gift explicitly establishes her father, while Stockholm remains location metadata rather than a surname.',
188:'Retain Margrete as a readable rendering of マルグレーテ in the gold-river rumor. Hamburg metadata does not create a surname or new biography.',
193:'Retain Myrine for ミュリネー across the local-ruins exchange. It is the established readable name; Athens is separate location metadata, not an added surname or historical identity.',
195:'Retain Nelly for ネリー in the pyramids invitation. Alexandria remains location metadata, and her friendly advice establishes no new relationship.',
196:'Retain Hatra for ハトラ in the pleasant-weather and Solomon-treasury exchange. Sofala remains location metadata; do not substitute a geographic biography for her name.'}

def main():
    assert not any(p.exists() for p in (NATIVE,REVIEW,TERMS))
    current,prose,roles,source_fields=map(load,(CURRENT,PROSE,ROLES,ROOT/'clean_name_fields.json'))
    runtime=current['runtime'];assert runtime==roles['runtime']
    ctx=RegisteredRuntime(runtime['release_proof'],runtime['startup_proof'],captain=1)
    assert ctx.receipt()==runtime and digest('translations/release_stack.json')==ctx.release['registry_sha256']
    actors=sorted(REASONS)
    expected={r['source_selector'] for r in prose['records'] if r.get('source_selector',254)<207}
    expected|={r['resolved_actor_ID'] for r in roles['native_roles']['rows'] if r['source_selector']==208}
    assert set(actors)==expected and len(actors)==19
    adapter=checked_text(inspect.getsource(names),{'for ident in [2,4,13,23,109]:':'for ident in ACTORS:'})
    env={**names.__globals__,'ACTORS':actors};exec(compile(adapter,__file__+'::original-current-name-consumers','exec'),env)
    result=ctx.execute(env['names']);assert len(result['rows'])==38
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    source_table=struct.unpack_from('<I',clean,0xCDAC0)[0]
    table=struct.unpack_from('<I',ctx.arm,0xCDAC0)[0];assert table==source_table
    existing={r['actor_ID']:r for r in load('translations/hodram_B211_B230_scoped_names_final_v1.json')['records']}
    prior_fields={r['actor_ID']:r['fields'] for r in source_fields['records']}
    assert set(prior_fields)==set(actors)-{151}
    records=[]
    for actor in actors:
        clean_fields=[];current_fields=[]
        for column in (0,4,8):
            at=table-0x02000000+32*actor+column;pointer=struct.unpack_from('<I',clean,at)[0]
            value=string(clean,pointer)
            if not pointer:value={**value,'text':None,'hex':'','byte_length':0,'status':'source-null-component-no-text'}
            else:assert value['status']=='printable-static-string'
            field=dict(column=column,source_ARM9_field_offset=at,pointer_hex=clean[at:at+4].hex(),**value)
            if actor!=151:
                old=next(f for f in prior_fields[actor] if f['column']==column)
                assert all(field[k]==old[k] for k in ('source_ARM9_field_offset','pointer_hex','hex','text'))
            else:
                old=next(f for f in existing[151]['clean_fields'] if f['column']==column)
                assert all(field[k]==old[k] for k in ('source_ARM9_field_offset','pointer_hex','hex','text'))
            clean_fields.append(field)
            pointer=struct.unpack_from('<I',ctx.arm,at)[0];raw=cstring(ctx.raw,pointer) if pointer else b''
            assert not raw or raw.isascii()
            current_fields.append(dict(column=column,field_offset=at,pointer=pointer,field_hex=ctx.arm[at:at+4].hex(),hex=raw.hex(),text=raw.decode('ascii') if pointer else None))
        forms=[r for r in result['rows'] if r['actor_ID']==actor]
        assert len(forms)==2 and all(r['text'].isascii() and r['text_hex']==r['text'].encode().hex() for r in forms)
        contexts=[r['id'] for r in prose['records'] if r.get('source_selector')==actor or (actor==151 and r.get('source_selector')==208)]
        records.append(dict(actor_ID=actor,clean_fields=clean_fields,current_fields=current_fields,current_consumers=forms,
            approved_forms={r['consumer']:r['text'] for r in forms},english=next(r['text'] for r in forms if r['consumer']=='progressive-nameplate'),
            decision='retention',finding=REASONS[actor],localization_note=REASONS[actor],context_record_ids=contexts,
            source_reference=dict(actor_ID=actor,fields=clean_fields),current_reference=dict(actor_ID=actor,fields=current_fields),
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),new_credit=0))
    # Clean table/constructor characterization is unchanged; do not rerun its old permutations.
    save(NATIVE,dict(runtime=runtime,actors=actors,current_names=result,current_native_getters=38,
        clean_static_field_bytes_andpointers_rechecked=True,source_ordinary_name_constructor_ABI_reused_not_reexecuted=True,
        no_new_clean_getter_permutation_orcatalogue_UI_claim=True,actual_gameplay=False,new_credit=0,
        evidence={str(p):digest(p) for p in (CURRENT,PROSE,ROOT/'clean_name_fields.json',ROLES,
            Path('translations/hodram_B211_B230_scoped_names_final_v1.json'),Path('scripts/bind_clean_editorial_name_fields_v2.py'),Path(__file__))}))
    save(REVIEW,dict(translation_policy='natural-dialogue-v2',target_locale='en-US',runtime=runtime,
        records=records,scoped_actors=19,justified_retentions=19,name_revisions=0,native_rendering_andvisual_review_pending=True,
        full_catalogue_UI_unvisited=True,no_global207_name_approval=True,new_credit=0,
        evidence={str(p):digest(p) for p in (NATIVE,CURRENT,PROSE,ROOT/'clean_name_fields.json',Path(__file__))}))
    asset=Path('translations/all_item_names_arm9_v1.json');items=[]
    for index in (50,52,53,74,90,95,97,99,110,122,127):
        item=next(r for r in load(asset)['records'] if r['id']==f'DK4_ITEM_POINTER_{index:03d}')
        at=item['offset'];source=string(clean,struct.unpack_from('<I',clean,at)[0]);pointer=struct.unpack_from('<I',ctx.arm,at)[0];raw=cstring(ctx.raw,pointer)
        assert source['status']=='printable-static-string' and raw and raw.isascii()
        assert clean[at+4:at+24]==ctx.arm[at+4:at+24]
        items.append(dict(index=index,pointer_field=at,source_Japanese=source['text'],source_hex=source['hex'],
            current_pointer=pointer,current_hex=raw.hex(),current_term=raw.decode('ascii'),all_nonname_item_metadata_exact=True))
    aliases=[]
    for entry in WORLD_CITY_ENTRIES:
        if entry.japanese!='ソファラ':continue
        assert entry.suggested_english=='Sofala' and clean[entry.offset:entry.offset+entry.source_length]==entry.expected_bytes
        raw=ctx.arm[entry.offset:entry.offset+entry.slot_size]
        assert raw==b'Sofala'+bytes(entry.slot_size-6)
        aliases.append(dict(profile_ID=entry.row_id,offset=entry.offset,source_hex=entry.expected_bytes.hex(),current_span_hex=raw.hex(),current_term='Sofala'))
    assert len(aliases)==2
    terms_path=Path('guide/research/player-terminology-reference.json')
    stat=next(r for r in load(terms_path) if r['japanese']=='精神' and r['english']=='Spirit')
    save(TERMS,dict(runtime=runtime,equipment_terms=items,Sofala_aliases=aliases,permanent_attribute=stat,
        source_shortened_orunnamed_items_must_remain_so=True,
        individual_findings=[
            dict(source='アルマジロの鉄皮',current='Armadillo Hide',decision='retention-in-dialogue',reason='Use the established concise item label; the source’s iron-hard metaphor is explicit in the preceding and following dialogue. Do not introduce steel or a literal metal composition.'),
            dict(source='グプタの霊獣',current='Gupta Spirit Beast',decision='retain-spirit-beast-description',reason='Spirit beast is the established readable fantasy term in the complete magical-statue exchange. The existing English sentence already preserves Gupta origin and hearsay; prefer retaining it over a gratuitous sacred-beast replacement.'),
            dict(source='王者の像',current='King Figurehead',decision='catalogue-reference-only',reason='The church scene calls it a figurehead/statue with a regal air; do not add an item title or substitute the unrelated Demon Figurehead.'),
            dict(source='魔法の革手袋',current='Magic Leather Gloves',decision='catalogue-reference-only',reason='The worker only says gloves. Do not add magic, leather or the catalogue title to his speech.'),
            dict(source='ポセイドンの雄叫び',current="Poseidon's Roar",decision='catalogue-reference-only',reason='Charles does not identify the sound. Do not reveal a divine cause or item name in his uncertain letter.'),
            dict(source='ヘロフィロスの医学書',current="Herophilus' Medicine",decision='catalogue-reference-only',reason='Carlo describes a medical text and does not say the title. Preserve that natural description without implying a drug.')],
        geographic_andliterary_forms=dict(イギリス='Britain',インド洋='Indian Ocean',リオデジャネイロ='Rio de Janeiro',
            ヘロフィロス='Herophilus',フェイディアス='Phidias',スカーイ島='Skye',ルーイス島='Lewis',ソロモン王='King Solomon'),
        source_terms_are_localization_not_external_historical_verification=True,
        full_catalogue_item_city_UI_andglobal_item_name_review_unvisited=True,no_current_orclean_ROM_mutation=True,new_credit=0,
        evidence={str(p):digest(p) for p in (asset,terms_path,PROSE,Path('dk4tool/script/arm9_profiles.py'),Path(__file__))}))
    print('19 scoped name retentions, 38 current getters, 11 item references, two Sofala aliases and Spirit bound. Name planes remain.')

if __name__=='__main__':main()
