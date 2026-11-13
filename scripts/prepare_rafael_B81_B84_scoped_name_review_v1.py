"""Retain16 individually source-bound names/roles and localize matching spoken references consistently."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

PROOF=Path('work/analysis/Rafael_B81_B84_formatting_20261105/scoped_names_macro_andconsumer_dependency_qualification_v1.json')
OUTPUT=Path('translations/rafael_B81_B84_scoped_names_androles_v1.json')
REASONS={
0:'Keep approved Rafael and established Castor;the native two-consumer name matches both clean components and captain0 substitutions.',
4:'Keep established Janus Pasar for the clean phonetic personal-name components;his everyday familiar voice gives no reason to invent a title or biography.',
5:'Keep native Claudio Manaus. Correct Manous in the scoped spoken introduction;the surname spelling must agree across the two actual name getters and body prose.',
6:'Keep Julio Erneco for フリオ/エルネコ,including the explicit grandfather relationship in these exchanges. Do not replace the clean surname with Ernesto.',
7:'Keep native Cristina Erneco and use Cristina consistently in these scoped bodies instead of their older Christina spelling. This does not declare every other route consumer reviewed.',
14:'Keep Emilio Ferog for the clean two-part name and restore the spoken surname that the earlier introduction omitted. Preserve his simple food-focused characterization.',
15:'Keep established Angelo Puccini,matching both clean name components;the full given/surname label is natural and needs no additional rank.',
16:'Keep established Gerhard Adernkatz,matching the source admiral and both native getters. Use the source first person in his speeches;the name does not authorize repeated this old man self-references.',
79:'Keep native Mivor Genz for the clean ミヴォール/ゲンツ components. Correct inconsistent spoken Gentz to Genz;do not infer a nationality or an external Latin spelling from that consistency choice.',
82:'Keep Shopkeeper as the natural occupational label for 広場の店主 in this town encounter. The square setting supplies its location;unused European-man metadata need not become a visible label.',
95:'Keep Patron for 酒場の客,a customer reacting to the bullfight in the complete town exchange. It denotes the source role without inventing a personal identity.',
104:'Keep Trader for 交易所の親父,an older trade-house proprietor. The familiar Japanese older-man wording establishes no father/son relationship.',
113:'Keep Port Worker for 出港所の兄貴. The role is clear in the port context;the familiar older-brother address is not literal kinship.',
147:'Keep Guildmaster for ギルドの元締め,the source guild head. The occupational authority is supported by the clean label;no unrelated noble/military rank is added.',
162:'Keep Boy for explicit 男の子 andthe source-labeled rescued child. The three FE Boy: bodies are separate null-actor presentations;this ordinary nameplate does not replace their source control.',
167:'Keep Lady for 貴婦人,a polite generic label for the woman in the rescue exchange. The clean label supports this social description;do not turn it into a named title or invent further family ties.',
}

if __name__=='__main__':
    assert not OUTPUT.exists();proof=load(PROOF);rows=[]
    for name in proof['name_bindings']:
        actor=name['actor_ID'];fields=name['source_andcurrent_fields'];text=name['current_consumers'][0]['text']
        rows.append(dict(id=f'ACTOR_{actor}_SCOPED_RAF81_84',actor_ID=actor,english=text,
            source_reference=dict(file_path='/__arm9__.bin',actor_ID=actor,fields=[dict(column=f['column'],field_offset=f['source_field'],pointer=f['source_pointer'],hex=f['source_hex']) for f in fields]),
            current_reference=dict(file_path='/__arm9__.bin',actor_ID=actor,fields=[dict(column=f['column'],field_offset=f['current_field'],pointer=f['current_pointer'],hex=f['current_hex']) for f in fields]),
            clean_components=[bytes.fromhex(f['source_hex']).decode('cp932') for f in fields],
            decision='retention',finding=REASONS[actor],retention_reason=REASONS[actor],
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            native_getter_proof=str(PROOF),native_getter_proof_sha256=sha(PROOF.read_bytes()),
            no_new_integrated_name_credit=True,new_credit=0))
    assert len(rows)==16 and {r['actor_ID'] for r in rows}==set(REASONS)
    save(OUTPUT,dict(format='dk4-scoped-name-contextual-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        records=rows,scope='Complete Rafael B81-B84 exchanges;individual natural name/role retentions with corresponding body consistency repairs.',
        new_global_name_field_changes=0,scoped_progressive_planes_pending=True,actual_headers_andfull_catalogue_UI_unvisited=True,
        full_207_name_review_still_open=True,new_credit=0,guide_photos=False,
        evidence={str(p):sha(p.read_bytes()) for p in [PROOF,Path(__file__)]}))
    print('Reviewed16 scoped names/roles asindividual retentions;body consistency repairs remain in330 batch. Fresh/matching style11 planes pending.')
