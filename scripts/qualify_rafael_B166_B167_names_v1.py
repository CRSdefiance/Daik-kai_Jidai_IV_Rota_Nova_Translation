"""Bind complete B166–B167 exchanges to their exact native public and catalogue names."""
from pathlib import Path
import struct

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.prove_lil_B167_names_v4124b import names as original_names
from scripts.qualify_rafael351_item_and_UI_terms_v1 import string
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime

A = Path('work/analysis')
CURRENT = A / 'Rafael_B166_B167_current1674_20261105/current_effective.json'
IDENTITY = CURRENT.with_name('names_and_terms_v1.json')
NAMES = Path('translations/rafael_B166_B167_scoped_names_review_v1.json')
ADAPTER = A / 'Rafael_B61_B80_new_name_bindings_20261104/names.json'
MACROS = A / 'Rafael557_macros_inputs_v1_20261105/qualified_identity_andmacros.json'
PREVIOUS_NAMES = [
    A / 'Rafael_B161_B165_current1607_20261105/names_and_terms_v1.json',
    A / 'Rafael557_names_terms_v1_20261105/names_terms_andconsumer_dependency_qualification.json',
]
HELP = Path('translations/help_early23_contextual_final_review_v1.json')
PRIOR_REVIEW = Path('translations/rafael_B161_B165_integrated_final_review_v1.json')
REASONS = {
    0: 'Keep the user-approved public name and the separate given, surname and full-name forms in the audience.',
    4: 'Keep the established Janus Pasar while his courtesy, aside and attempts to deflect embarrassment shape his voice.',
    5: 'Keep Claudio Manaus as the public name and Clau as the familiar spoken nickname in the source.',
    6: 'Keep Julio Erneco and his distinct older register in the expedition and alternative recruitment advice.',
    7: 'Keep Cristina Erneco in both the eavesdropping and Charlotte-letter responses.',
    8: 'Keep the default Arcadius Eudoxios and full catalogue name as table forms. Eirene names herself in this scene, which requires its own native alias check.',
    11: 'Keep Jam Ludwyan on the nameplate and preserve Jack in the separate catalogue name.',
    13: 'Keep Cesare Tony across his nervous reaction to the court and his hesitant criticism of the letter.',
    14: 'Keep Emilio Ferog, whose aside about food and audible chewing make him identifiable without an added role.',
    15: 'Keep Angelo Puccini for the competitive interruption and emphatic defense of Charlotte.',
    17: 'Keep Al Shin on the nameplate and restore the spoken Al Ferid Shin, exactly matching the distinct full catalogue form.',
    18: 'Keep Charles Rochefort on the nameplate and preserve Jean in the distinct catalogue form.',
    19: 'Keep Carlo Sinat on his conditional warning without borrowing a role from a different listener.',
    20: 'Keep Fernando Dias in his status aside and comments among the listeners.',
    21: 'Keep Ian Dukov even where the Japanese gives him only a silent conditional reaction.',
    22: 'Keep Samwell Khan as the public form and the separate catalogue da. His reactions provide no reason to expand the nameplate.',
    23: 'Keep Manuel Almeida on the alternative listener line and avoid assigning a role from outside the scene.',
    25: 'Keep the established Yifa Sol in her optional excited aside.',
    26: 'Keep Julian Lopes in the conditional response to Charlotte’s letter.',
    27: 'Keep Aziza Nurennahar for her version of the teasing remark, distinct from Cristina’s branch.',
    115: 'Keep Port Worker as the clean departure-office role without turning the familiar Japanese label into kinship or a private name.',
    120: 'Keep Guard in the palace entrance scene. The clean fields give a role and no personal rank.',
    125: 'Keep King, whose formal speech identifies Portugal without naming the ruler.',
    148: 'Keep Guildmaster as the source guild leadership role. His status as Al’s employer belongs in the exchange.',
}
EXTERNAL = {30: 'Dinis Albuquerque', 80: 'Charlotte Miller'}


def digest(path):
    return sha(Path(path).read_bytes())


def main():
    assert not IDENTITY.exists() and not NAMES.exists()
    current = load(CURRENT)
    rt = current['runtime']
    ctx = RegisteredRuntime(rt['release_proof'], rt['startup_proof'], captain=0)
    assert ctx.receipt() == rt
    font = ctx.image.read_file('/GRP/KANJI.FNT')
    actors = {r['source_selector'] for g in current['groups'] for r in g['records']} - {254}
    assert actors == REASONS.keys()
    prior = {}
    for p in PREVIOUS_NAMES:
        proof = load(p)
        old = RegisteredRuntime(proof['runtime']['release_proof'], proof['runtime']['startup_proof'], captain=0)
        assert (ctx.arm,ctx.common,ctx.actor_root,ctx.actor_bytes) == (old.arm,old.common,old.actor_root,old.actor_bytes)
        assert old.image.read_file('/GRP/KANJI.FNT') == font
        for row in proof['name_bindings']:
            prior[row['actor_ID']] = row
    macros = load(MACROS)
    assert macros['macro_ascii_lengths'] == dict(FI=6,FA=6,FO=10,FU=13)
    mr = macros['runtime']
    old = RegisteredRuntime(mr['release_proof'],mr['startup_proof'],captain=0)
    assert (ctx.arm,ctx.common,ctx.actor_root,ctx.actor_bytes) == (old.arm,old.common,old.actor_root,old.actor_bytes)
    assert old.image.read_file('/GRP/KANJI.FNT') == font
    jp = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    source_root,target_root = (struct.unpack_from('<I', x,0xCDAC0)[0]-BASE for x in (jp,ctx.arm))

    fresh = sorted((actors | EXTERNAL.keys()) - prior.keys())
    adapter = load(ADAPTER)
    env = {**original_names.__globals__, 'ACTORS':fresh}
    exec(compile(adapter['source_owned_current_adapter'], __file__ + '::same-original-getters', 'exec'), env)
    result = ctx.execute(env['names'])
    assert len(result['rows']) == 2*len(fresh)
    bindings, names, terms = [], [], []
    for actor in sorted(actors | EXTERNAL.keys()):
        fields = []
        for column in (0,4,8):
            sa,ca = source_root+32*actor+column,target_root+32*actor+column
            def field(data, table, at):
                pointer = struct.unpack_from('<I',table,at)[0]
                return dict(field_offset=at,**(string(data,pointer) if pointer else dict(pointer=0,hex='',text='')))
            fields.append(dict(column=column,source=field(jp,jp,sa),current=field(ctx.raw,ctx.arm,ca)))
        if actor in fresh:
            forms = [r for r in result['rows'] if r['actor_ID'] == actor]
        else:
            assert fields == prior[actor]['source_andcurrent_fields']
            forms = prior[actor]['current_consumers']
        by_consumer = {r['consumer']:r for r in forms}
        assert set(by_consumer) == {'progressive-nameplate','full-catalogue'}
        for form in forms:
            raw = bytes.fromhex(form['text_hex'])
            assert raw.decode('cp932') == form['text']
            if not raw.isascii():
                assert actor == 30 and form['consumer'] == 'full-catalogue'
                assert form['text'] == 'Dinis デ Albuquerque' and raw.hex() == '44696e697320836620416c627571756572717565'
        public = by_consumer['progressive-nameplate']
        if actor in EXTERNAL:
            assert public['text'] == EXTERNAL[actor]
            terms.append(dict(actor_ID=actor,text=public['text'],fields=fields,current_consumers=forms))
            continue
        bindings.append(dict(actor_ID=actor,source_andcurrent_fields=fields,current_consumers=forms,fresh=actor in fresh))
        reason = REASONS[actor]
        names.append(dict(id=f'ACTOR{actor}_RAFAEL166_167_NAME',actor_ID=actor,kind='progressive-nameplate',
            english=public['text'],speaker=public['text'],source_meaning='Public character name or role in the clean actor fields.',
            context='Public speaker labels and separate catalogue fields for Rafael SC0 B166–B167.',
            decision='retention',retention_reason=reason,finding=reason,localization_note=reason,
            source_reference=dict(actor_ID=actor,fields=[f['source'] for f in fields]),
            current_reference=dict(actor_ID=actor,consumer='progressive-nameplate',text_hex=public['text_hex']),
            contextual_alias_check_pending=actor==8,
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),new_credit=0))
    al = next(r for r in bindings if r['actor_ID']==17)
    assert {r['text'] for r in al['current_consumers']} == {'Al Shin','Al Ferid Shin'}
    alias = next(r for r in bindings if r['actor_ID']==8)
    assert alias['source_andcurrent_fields'][2]['source']['text']=='エイレネ'
    assert alias['source_andcurrent_fields'][2]['current']['text']=='Eirene'
    proof = next(r for r in load(HELP)['records'] if r.get('heading')=='Proof of Conquest')
    assert all(proof['review'].values())
    reviewed = load(PRIOR_REVIEW)['records']
    estado = next(r for r in reviewed if 'Estado' in r['english'])
    assert all(estado['review'].values())
    evidence = {str(p):digest(p) for p in [CURRENT,ADAPTER,MACROS,*PREVIOUS_NAMES,HELP,PRIOR_REVIEW,Path(__file__)]}
    save(NAMES,dict(format='dk4-scoped-name-contextual-review-v2',translation_policy='natural-dialogue-v2',
        target_locale='en-US',encoder='dialogue-relocatable-v1',records=names,
        review_gates=['source','context','localization','naturalness','formatting'],all_name_formatting_gates_pending=True,
        runtime=rt,new_credit=0,no_global_name_table_changes=True,evidence=evidence))
    save(IDENTITY,dict(runtime=rt,actors=sorted(actors),name_bindings=bindings,fresh_actors=fresh,
        exact_reused_actors=sorted((actors|EXTERNAL.keys())-set(fresh)),external_term_name_bindings=terms,
        exact_unchanged_actor0_macro_dependencies=True,macro_ascii_lengths=macros['macro_ascii_lengths'],
        Proof_of_Conquest_help_record=proof['id'],approved_Estado_story_record=estado['id'],
        prior_actor30_catalogue_de_defect_preserved_separate_from_spoken_name=True,
        current_boot_actor8_default_does_not_prove_in_scene_alias=True,scoped_names=str(NAMES),
        scoped_names_sha256=digest(NAMES),no_new_visual_gameplay_orcatalogue_UI_claim=True,new_credit=0,evidence=evidence))
    print(f'{len(names)} scoped name/role decisions and two mentioned names bound, {len(fresh)} fresh getter pairs.')


if __name__ == '__main__':
    main()
