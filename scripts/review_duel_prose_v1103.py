"""Review33 source-mapped duel alternatives;formatting and release remain pending."""
from collections import Counter
from dataclasses import asdict
from pathlib import Path
from shutil import copy2
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.patch.sighting_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/duel_prose_v1103')
MANUSCRIPT=Path('translations/duel_editorial_manuscript_v1.json')
ARCHIVE=Path('E:/Rota Nova translations/Editorial review/V1103 Duel source and prose review')
TEXT={
1931:("So you're %s! Let's settle this with a duel!",'Recognizes the named opponent and proposes settling the encounter by single combat.'),
1932:("So you're %s! Face me in a fair duel!",'Recognizes the named opponent and demands an honorable,fair duel.'),
1933:("Ah, you're %s! Let's duel!",'Exclaims on recognizing the opponent and challenges them to a duel.'),
1934:("So, you're %s! Let's settle this with a duel!",'Recognizes the opponent and confidently proposes resolving the matter by a duel.'),
1935:("Well, if it isn't %s! Fight me one on one!",'Roughly greets the recognized opponent and demands a one-on-one fight.'),
1936:("You must be %s! We'll settle this with a duel!",'An older-voiced duelist recognizes the opponent and proposes settling the encounter by single combat.'),
1937:("You're %s! Let's duel!",'Excitedly recognizes the opponent and demands a duel with the speaker.'),
1938:("...You're %s! We shall settle this with a duel!",'Pauses,recognizes the opponent,and formally proposes settling the matter through a duel.'),
1939:("Interesting. I accept your challenge!",'Finds the challenge interesting and formally accepts it.'),
1940:("Interesting. I'll take you on!",'Finds the challenge interesting and accepts it.'),
1941:("All right! I'll take you on!",'Enthusiastically agrees to face the challenger.'),
1942:("Bring it on! I accept your challenge!",'Confidently welcomes and accepts the challenge.'),
1943:("This'll be fun! I'll take you on!",'Roughly expresses amusement and accepts the challenge.'),
1944:("All right! Let's do this!",'Enthusiastically resolves to take on the challenge.'),
1945:("Next time won't be so easy!",'Warns that the next encounter will not go the same way.'),
1946:("You won't get away next time!",'Threatens not to let the opponent get away next time.'),
1947:("You're not getting away next time!",'Roughly threatens not to let the opponent escape next time.'),
1948:("Grr... Next time, you're dead!",'Growls in frustration and threatens the opponents life in their next encounter.'),
1949:("I'll get you next time!",'Personally promises to beat the opponent next time,in a youthful voice.'),
1950:("Damn you! Things will be different next time!",'Curses the opponent and warns that next time will not go this way;does not specify a guaranteed victory.'),
1951:("%s, please get to safety! Everyone, give them cover!",'Politely urges the named defeated person to escape and orders everyone to provide cover.'),
1952:("%s, get out of here! We'll all cover you!",'Urgently tells the named person to escape and promises collective cover.'),
1953:("%s, get away now! Everyone, give them cover!",'Urgently tells the named person to escape and orders everyone to provide cover.'),
1954:("%s, get out of here! Come on, lads, cover them!",'Urges the named person to escape and roughly orders the men to provide cover.'),
1955:("%s, get to safety! Everyone, cover them!",'An older-voiced companion tells the named person to escape and orders everyone to cover them.'),
1956:("%s, run! We'll all protect you!",'Urgently urges the named person to flee and reassures them that everyone will protect them.'),
1973:("Admiral, please get to safety! Everyone, give them cover!",'Politely urges the admiral to escape and orders everyone to provide cover.'),
1974:("Admiral, get to safety! We'll cover you!",'Urges the admiral to escape while promising covering support.'),
1975:("Admiral, please get to safety! Everyone, cover them!",'Politely urges the admiral to escape and calls on everyone to provide cover.'),
1976:("Admiral, get out of here! Lads, cover them!",'Urges the admiral to escape and roughly orders the men to provide cover.'),
1977:("Admiral, get clear! Everyone, give them cover!",'An older-voiced companion commands the admiral to escape and calls on everyone to provide cover.'),
1978:("Admiral, run! Everyone, cover them!",'Urgently tells the admiral to escape and orders everyone to provide cover.'),
1979:("Admiral, we'll cover you! Get to safety now!",'Tells the admiral to entrust covering support to the speaker and urgently escape.')}


def main():
    assert not ROOT.exists() and not MANUSCRIPT.exists() and not ARCHIVE.exists()
    source_path=Path('work/analysis/duel_source_v1101/source_context_packet.json')
    supplement_path=Path('work/analysis/duel_source_v1102/escape_source_supplement.json')
    source,supplement=read(source_path),read(supplement_path)
    assert supplement['zero_predicate_actor_IDs']==[0,1,2,3] and supplement['original_alternate_table']==0x02117620
    assert supplement['prior_source_inventory_sha256']==sha(source_path.read_bytes())
    source_rows={r['message_ID']:r for r in source['source_and_current_neighbors']}
    source_rows.update({r['message_ID']:r for r in supplement['source_and_current_seven_additional_alternatives']})
    rom_path=Path(source['candidate']);rom=NdsImage.open(rom_path);clean_path=Path('work/clean.nds');clean=NdsImage.open(clean_path)
    assert sha(rom_path.read_bytes())==source['candidate_sha256'] and sha(clean_path.read_bytes())==source['clean_ROM_sha256']
    arm,common=rom.read_file('/__arm9__.bin'),rom.read_file('/COMMON/MESFILE.DK4')
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    en=current_entries(common,arm);records=[]
    table_rows={r['family']:r for r in source['tables']}
    for n,(english,meaning) in sorted(TEXT.items()):
        assert jp[n].text.hex()==source_rows[n]['source_hex'] and en[n].text.hex()==source_rows[n]['current_hex']
        assert english.isascii() and english==' '.join(english.split()) and not any(c in english for c in '{}\n\r\t')
        arguments=jp[n].text.count(b'%s');assert english.count('%s')==arguments and '%' not in english.replace('%s','')
        if n<1939:family='challenge';consumer='original-duel-side0-actor-text';table=table_rows[family]['address']
        elif n<1945:family='acceptance';consumer='original-duel-side1-actor-text';table=table_rows[family]['address']
        elif n<1951:family='defeated_opponent_threat';consumer='original-duel-side1-actor-text';table=table_rows[family]['address']
        elif n<1957:family='cover_for_defeated_captain';consumer='original-post-duel-companion-speech';table=table_rows[family]['address']
        else:family='cover_for_main_captain';consumer='original-post-duel-companion-speech';table=supplement['original_alternate_table']
        old=en[n].text.decode('cp932');retain=english==old
        note=('Preserve the independent original voice alternative,recognition/challenge,acceptance,warning or covering-support intent. '
            'No weapon,kinship,rank beyond the source Admiral,or actual battle outcome is added. Read aloud in the original challenge/reply/duel/post-duel flow. '
            'Ordinary prose remains one logical paragraph;native actor selection,source name bytes and renderer controls are not authored into English. ')
        if n<=1950:
            note+='The original duel consumerD458/CE898/DA28 requires its own complete layout/font/transition audit;do not inherit shared-speech formatter approval. '
        else:
            note+='Original53F0C chooses the First Mate or original alternate companion. Name-bearing1951..1956 and Admiral1973..1979 are separate native branches,not successive sentences. Do not hardcode masculine him:the main-captain branch covers Rafael,Hodram,Lil and Maria. '
        if n in (1932,1935,1937,1939,1941,1942,1943):
            note+='Replace obsolete fullwidth Latin letters in editable prose with ordinary ASCII;complete leading glyphs still require the actual native-consumer proof before release. '
        if n==1940:note+='Restore the source amusement lost by the previous bare Challenge accepted. '
        if n==1950:note+='Restore the broad next-time warning rather than inventing a specific guaranteed win. '
        if retain:note+='Retained wording is already faithful and reads naturally in this source context. '
        records.append({'id':f'COMMON_MESSAGE_{n}','message_id':n,'source_family':family,'consumer':consumer,
            'speaker':'Original selected duelist for native side0' if n<1939 else 'Original selected duelist for native side1' if n<1951 else 'Original First Mate or original source-selected alternate companion',
            'context':'Independent voice alternative selected from original table '+hex(table)+'. Original caller/HP branches and conditional name getters are documented in V1101/V1102;no eligibility result or actor identity is forced.',
            'source_table':table,'source_voice_classes_including_native_fallback':[i for i,v in enumerate(table_rows[family]['voice_IDs'] if family in table_rows else supplement['voice_IDs']) if v==n],
            'source_reference':{k:v for k,v in asdict(jp[n]).items() if k!='text'},'source_hex':jp[n].text.hex(),'source_Japanese':jp[n].text.decode('cp932'),
            'current_reference':{k:v for k,v in asdict(en[n]).items() if k!='text'},'current_text_hex':en[n].text.hex(),'current_English':old,
            'source_meaning':meaning,'english':english,'localization_note':note,'editorial_decision':'retain' if retain else 'revise',
            'native_argument_count':arguments,'native_argument_kind':'source-selected-opponent-name' if n<1939 else 'source-selected-defeated-person-compact-name' if n<1957 and n>=1951 else None,
            'source_native_macros':[],'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False}})
    decisions=Counter(r['editorial_decision'] for r in records);assert len(records)==33 and decisions=={'revise':22,'retain':11},decisions
    doc={'format':'dk4-natural-dialogue-source-manuscript-v2','translation_policy':'natural-dialogue-v2','target_locale':'en-US',
        'encoder':'dialogue-relocatable-v1','consumer_layout_profile':'duel-distinct-native-consumers-pending-calibration-v1',
        'review_gates':['source','context','localization','naturalness','formatting'],'formatting_review_pending':True,
        'status':'33-source-context-prose-reviewed;native-consumer-font-release-and-actual-pending','file_path':'/COMMON/MESFILE.DK4',
        'source_clean_ROM_sha256':sha(clean_path.read_bytes()),'current_ROM':str(rom_path),'current_ROM_sha256':sha(rom_path.read_bytes()),
        'current_COMMON_sha256':sha(common),'current_ARM9_sha256':sha(arm),'native_context_proof':str(source_path),
        'native_context_proof_sha256':sha(source_path.read_bytes()),'source_context_supplement':str(supplement_path),
        'source_context_supplement_sha256':sha(supplement_path.read_bytes()),'records':records}
    ROOT.mkdir(parents=True);save(MANUSCRIPT,doc)
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path)
    assert ledger['records_editorially_completed']==1196 and ledger['records_with_source_and_prose_pass']==1234
    assert not set(TEXT)&set(ledger['reviewed_but_incomplete_COMMON_IDs'])
    save(ROOT/'editorial_ledger_before_prose.json',ledger)
    for field in ('records_with_source_and_prose_pass','records_with_source_prose_drafts'):ledger[field]+=33
    ledger['source_prose_reviewed_counts_by_file']['/COMMON/MESFILE.DK4']+=33
    ledger['reviewed_but_incomplete_COMMON_IDs']=sorted([*ledger['reviewed_but_incomplete_COMMON_IDs'],*TEXT])
    ledger['active_source_prose_drafts']['native_message_IDs']=list(ledger['reviewed_but_incomplete_COMMON_IDs'])
    ledger['active_source_prose_drafts']['manuscripts'].append(str(MANUSCRIPT))
    ledger['active_source_prose_drafts']['status']='older3-context;shot;15-sighting-grammar-release;33-duel-native-fonts-release-actual-pending'
    ledger['duel_prose_v1103']={'native_message_IDs':sorted(TEXT),'manuscript':str(MANUSCRIPT),
        'source_context':str(source_path),'escape_source_supplement':str(supplement_path),
        'source_prose_reviews_added':33,'completed_entries_added':0,'revisions':22,'retained_wordings':11,
        'gendered_escape_pronoun_finding':'The unchanged native main-captain branch covers IDs0..3;English him is not valid for Lil/Maria. Neutral them/you retains the source.',
        'native_fonts_registered_integration_actual_and_normal_transitions_pending':True}
    summary=('V1103 source/prose-reviews33 duel challenge,acceptance,opponent threat and named/Admiral escape alternatives1931-1956/1973-1979:22 proposed revisions and11 justified retentions.1040 original voice selections and208 actor predicates bind distinct duel and shared-speech consumers. Drafts restore recognition,fair combat,amusement and the broad next-time warning;neutral cover requests work for all four captains instead of hardcoded him. Fullwidth Latin F/I becomes editable ASCII pending complete initial-glyph proof. All original substitutions,approved names,voice and branch distinctions are preserved. Native consumer calibration,fonts,registered combined exact patch and actual scenes/transitions remain pending.1196 complete,1267 source/prose;no completion credit. V1086 is last combined candidate,V997 fully scene-verified;the15 sighting grammar revisions also still need new registered integration. Full shared/routes/raw-source editorial scope and separate graphics audit remain open.')
    ledger['latest_checkpoint']=summary;ledger['research_checkpoints'].append({'id':'V1103-duel-source-prose',
        'manuscript':str(MANUSCRIPT),'source_prose_reviews_added':33,'completed_entries_added':0,
        'previous_goal_turn_classification':'progress:registered build and current photographed formatting rechecked;15 new grammar drafts fully native-reviewed;33 duel sources mapped',
        'this_goal_turn_classification':'progress:33 exact clean records reviewed;22 proposed revisions11 retentions and gender-neutral main-captain escape finding recorded',
        'full_goal_complete':False})
    assert ledger['records_with_source_and_prose_pass']==1267 and ledger['source_prose_reviewed_counts_by_file']['/COMMON/MESFILE.DK4']==1266
    save(ledger_path,ledger)
    doc_path=Path('docs/duel_v1103_source_prose_review.md')
    doc_path.write_text('# V1103: duel dialogue source and prose review\n\n'+summary+
        '\n\nOriginal table02117340 contains eight challenges;02117360 contains six acceptances with native fallback. The duel-specificD458 consumer selects its own side actor and prints through CE898/DA28. Opponent threats021174E0 remain independent of the later original53F0C companion escape notices. Original predicate7EF28 returns0 for main captain IDs0..3;they receive1973..1979 addressed to Admiral. Other IDs receive named1951..1956. Therefore cover him is an inherited English defect for Lil and Maria;neutral pronouns correct it without changing the original branch.\n\nThese are source/prose drafts,not a new playable patch. Every record retains a false formatting gate. Do not reuse the ordinary sighting formatter for duel-specific boxes until its consumer and complete font planes have been mapped. Old fullwidth F/I must not be blindly changed in a ROM. The original name getters,actor assignments,HP results,RNG and battle outcomes remain untouched.\n',encoding='utf-8')
    for filename in ('docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md'):
        with Path(filename).open('a',encoding='utf-8') as stream:stream.write('\n\n## V1103: duel source and prose review\n\n'+summary+' See [V1103 review](duel_v1103_source_prose_review.md).\n')
    ARCHIVE.mkdir(parents=True);files=[]
    for path in (Path(__file__),MANUSCRIPT,ledger_path,doc_path,source_path,supplement_path,ROOT/'editorial_ledger_before_prose.json'):
        target=ARCHIVE/path.absolute().relative_to(Path.cwd());target.parent.mkdir(parents=True,exist_ok=True);copy2(path,target)
        assert sha(path.read_bytes())==sha(target.read_bytes());files.append({'source':str(path),'archived':str(target),'sha256':sha(target.read_bytes())})
    save(ROOT/'archive_manifest.json',{'files':files,'all_hashes_verified':True,'no_ROM_or_save_changed':True,'no_completed_entry_credit':True})
    print('33 source/prose reviews:22 revisions11 retained.1267 source/prose;1196 complete unchanged. Native formatting,release and actual scenes pending.',flush=True)


if __name__=='__main__':main()
