"""Review 23 scoped names; reuse clean proofs and bind both current getters freshly."""
import inspect
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_hodram_B211_B230_contextual_v1 import OUT as PROSE
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.prove_lil_B167_names_v4124b import names
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_hodram_B221_B230_contextual_v1 import CURRENT
from scripts.source_locked_derivation_v5118 import checked_text
from dk4tool.rom.nds import NdsImage

PRIOR=Path('work/analysis/Hodram_B211_B230_clean_20261104/native_identity_checkpoint_v1.json')
NATIVE=Path('work/Hodram_B211_B230_resume_20261106/scoped_names_current_v1.json')
OUT=Path('translations/hodram_B211_B230_scoped_names_review_v1.json')
REASONS={
1:'Retain user-approved Hodram and Joakim with Bergstrom. The source has all three components; progressive and full-name consumers intentionally differ. His restrained military voice does not create a new rank.',
4:'Retain established Janus Pasar for the clean ジェナス・パサー. His signed practical letter and its announcements identify the same companion; correct the older Gennas/Pasa dialogue spellings to these forms.',
7:'Retain established Cristina Erneco for クリスティナ・エルネコ. Her pirate-sword interest, swan encounter and Charm result belong to the same character. The older Christina dialogue spelling is corrected; the shared surname alone establishes no new kinship.',
11:'Retain Jam Ludwyan and full Jam Jack Ludwyan, preserving all clean components. His separate blunt comment on Yukihisa\'s prose does not identify him with the runtime-selected companion.',
12:'Retain Yukihisa Shiraki and full Yukihisa Genjo Shiraki, using the approved complete surname. The letter\'s signature uses the same native identity rather than the older Hakuki Gensho rendering of its kanji.',
13:'Retain Cesare Tony, the established readable rendering of the clean personal name. His explanation of Ian\'s historical interest adds no new nationality or biographical label.',
14:'Retain Emilio Ferog with its accepted ASCII initial. The eager food-loving weapon request needs a youthful voice, not an invented age, child relationship or new personal name.',
16:'Retain Gerhard Adernkatz, preserving the source identity in his martial-history stories and reflective questions. Formal diction does not justify adding an unspoken title to his name.',
17:'Retain Al Shin and full Al Ferid Shin. The source supplies those components; Al\'s weapon rumor and Saladin account require no invented Lord title or extra relationship.',
21:'Retain Ian Dukov, matching the clean イアン・ドゥーコフ and the two native consumers. All nine full-width I defects occur in dialogue text, not in these already-consistent nameplate fields.',
23:'Retain Manuel Almeida, the source-bound reflective companion. His devotional objection and square conversation remain his own; speaking about religion does not turn an occupation into his name.',
25:'Retain Yifa Sol, the established readable phonetic form of イファ・ソル. Her reference to a teacher does not supply a new name, family relation or formal rank.',
26:'Retain Julian Lopes, the established form of ユリアン・ロペス. His separate flirtations with Lucia and Safia establish no relationship status or connection to other characters with similar names.',
82:'Retain Shopkeeper for 広場の店主 in the sword-seeking woman\'s interruption. The regional male metadata is not a surname or a new player-facing biography.',
85:'Retain Shopkeeper for 広場の店主 in the Crusades exchange. Keep the role label; do not turn Islamic-region metadata into a personal name, nationality claim or religious title.',
92:'Retain Barkeep for 酒場の親父. The familiar source father-like address is occupational here and does not establish kinship with Hodram.',
149:'Retain Guildmaster for ギルドの元締め. The source explicitly supplies the guild role even though this exchange concerns his favorite novel; Chinese metadata is not a surname.',
151:'Retain Sailor on the progressive nameplate and Retainer in the full-name consumer. The clean native progressive role and separate 配下 catalogue field have different established functions. Playing a losing combatant opposite the boy creates no new rank, age or relationship.',
162:'Retain Boy for 男の子. His Charles Martel proclamation is explicit pretend hero-play, not a reason to rename the real speaker Charles Martel or infer who the other participant is.',
169:'Retain Alluring Woman for 妖艶な女. Vivienne is her spoken self-identification in this exchange; a shared generic speaker slot should not become a newly invented universally named actor. Indian metadata adds no biography to the legend.',
170:'Retain Mysterious Old Man for 謎の老人. The source explicitly supplies both mystery and age. His pirate recollection and prophetic family tradition do not justify a more specific identity or a kinship label for the listener.',
197:'Retain Safia for サフィア. Basra is separate source location metadata, not a family name; her covered hair and Julian\'s flirtation do not establish religion or relationship status beyond the spoken source.',
199:'Retain Lucia for ルシア. Malacca is separate location metadata, not a surname; her gift teasing does not establish a marriage or an existing romance.',
}

def main():
    assert not OUT.exists() and not NATIVE.exists()
    old,current,prose=map(load,(PRIOR,CURRENT,PROSE))
    assert len(prose['records'])==277 and prose['remaining_contextual_comparisons']==0
    actors=sorted(REASONS);assert actors==[r['actor_ID'] for r in old['records']]
    runtime=current['runtime'];ctx=RegisteredRuntime(runtime['release_proof'],runtime['startup_proof'],captain=1)
    assert ctx.receipt()==runtime
    adapter=checked_text(inspect.getsource(names),{'for ident in [2,4,13,23,109]:':'for ident in ACTORS:'})
    env={**names.__globals__,'ACTORS':actors}
    exec(compile(adapter,__file__+'::original-current-getters-own-Hodram','exec'),env)
    native=ctx.execute(env['names']);assert len(native['rows'])==46
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    checks=[];records=[]
    for prior in old['records']:
        actor=prior['actor_ID']
        for field in prior['clean_fields']:
            at=field['source_ARM9_field_offset']
            assert clean[at:at+4].hex()==field['pointer_hex']
            if field['text'] is not None:
                raw=bytes.fromhex(field['hex']);start=field['offset']
                assert clean[start:start+len(raw)+1]==raw+b'\0'
        for field in prior['current_fields']:
            at=field['field_offset'];assert ctx.arm[at:at+4].hex()==field['field_hex']
            if field['text'] is not None:
                raw=bytes.fromhex(field['hex']);start=field['pointer']-0x02000000
                assert ctx.raw[start:start+len(raw)+1]==raw+b'\0'
        forms=[r for r in native['rows'] if r['actor_ID']==actor]
        expected={r['consumer']:r['text'] for r in prior['current_consumers']}
        assert {r['consumer']:r['text'] for r in forms}==expected
        assert all(r['text'].isascii() and r['text_hex']==r['text'].encode().hex() for r in forms)
        checks.append(dict(actor_ID=actor,clean_field_bytes_andpointers_exact=True,
            current_field_bytes_pointers_andboth_getters_exact=True,source_native_proof=prior['native_proof'],
            source_native_proof_sha256=prior['native_proof_sha256']))
        records.append(dict(actor_ID=actor,clean_fields=prior['clean_fields'],current_fields=prior['current_fields'],
            current_consumers=forms,approved_forms=expected,decision='retention',finding=REASONS[actor],
            localization_note=REASONS[actor],review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            context_record_ids=prior['context_record_ids'],current_native_name_proof=str(NATIVE),new_credit=0))
    save(NATIVE,dict(runtime=runtime,actors=actors,current_names=native,dependency_checks=checks,
        clean_getter_proofs_reused_not_reexecuted=True,current_native_getters=46,
        actual_gameplay=False,new_credit=0,evidence={str(p):digest(p) for p in (PRIOR,CURRENT,PROSE,Path(__file__))}))
    save(OUT,dict(translation_policy='natural-dialogue-v2',target_locale='en-US',runtime=runtime,
        records=records,scoped_actors=23,justified_retentions=23,name_revisions=0,
        native_rendering_andvisual_review_pending=True,full_catalogue_UI_unvisited=True,
        no_global207_name_approval=True,new_credit=0,evidence={str(p):digest(p) for p in (NATIVE,PRIOR,PROSE,Path(__file__))}))
    print('Reviewed 23 scoped names: 23 justified retentions; 46 current getters exact. Name planes remain.')

if __name__=='__main__':main()
