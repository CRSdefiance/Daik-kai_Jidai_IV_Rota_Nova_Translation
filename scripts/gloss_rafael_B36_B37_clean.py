"""Record both complete pirate exchanges from clean Japanese before current English."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Rafael_early_story_B36_B41_B51_B60_clean_20261104')
DECISIONS={
36:dict(context='A lookout reports a possible enemy fleet. The young companions worry, while Julio recognizes the Algiers pirates and then Barbarossa Hayreddin. Julio explains their strength and reported Ottoman involvement. Claudio summarizes the regional predicament; surviving the immediate encounter takes priority. Janus lines are conditional companion inserts, not a separate conversation.',notes=[
    'Hayreddin 一家 denotes his organization here; do not invent biological family relationships.',
    'Ottoman involvement is reported as hearsay. Claudio’s entrance/far-end/boss remark is his interpretation, not an added independent account of a formal chain of command.',
    'Pirate terminology describes this named in-game force; preserve the North African/Algiers setting without adding an ethnicity or religion.'],meanings=[
    'The lookout calls to the admiral: vessels that appear to be enemies have been sighted.',
    'Janus wonders what that fleet could be.',
    'Claudio asks whether they are pirates.',
    'Rafael hopes this does not turn into trouble.',
    'Janus says that if they are pirates, a fight will be unavoidable.',
    'Julio recognizes the Algiers pirates and wonders uneasily whether that particular man is among them.',
    'Rafael asks about the Algiers pirates.',
    'Julio explains that this is the name for the men who use the North African coast as a base and raid around Algiers.',
    'Janus reacts: they really are pirates.',
    'Claudio complains that they are being tested right away.',
    'Julio confirms the feared identification: Barbarossa Hayreddin.',
    'Rafael asks whether he is powerful.',
    'Julio says Hayreddin’s organization stands far above even the other Algiers pirates: immensely powerful and merciless.',
    'Claudio reacts in alarm and asks whether Julio is serious.',
    'Julio adds that the Ottoman Turks, currently the strongest power in the Mediterranean, are apparently also involved in the pirates’ activities.',
    'Claudio pictures these pirates at the entrance to the Mediterranean and their boss at its distant end.',
    'Julio says that to trade in the Mediterranean, they first have to find some way of dealing with Hayreddin, who controls Gibraltar.',
    'Janus sighs that they have a difficult road ahead.',
    'Julio brings them back to the immediate problem: somehow getting through the present situation.',
    'Claudio asks how they are supposed to get through it.',
]),
37:dict(context='Rafael tries the enemy-of-my-enemy argument to survive Hayreddin’s arrival. Julio recommends confidence; Rafael’s grand declaration draws applause from his own crew and threats from Salid. Hayreddin’s amusement allows Rafael to bluff about future strength. Hayreddin grants passage but restricts trading, offers conditional help against Spain within his waters, and warns against encroaching on his territory. Rafael’s fear catches up with him after the pirates leave. Janus inserts depend on companion state.',notes=[
    'Use native-bound identities for Hayreddin, Salid and the generic crews before English approval; spellings in these source glosses are provisional leads.',
    'Keep FI (given name), FO (company/fleet name) and FU (full name) distinct. The FU declaration must not be silently reduced to a given name.',
    'Hayreddin grants transit, not unrestricted Mediterranean trade. His reinforcements are neither guaranteed nor available outside his own waters.',
    'The warning against two great powers and the prohibition on touching Hayreddin’s territory remain separate conditions.',
    'Preserve Rafael’s earnest bluff, Claudio’s brash objections, Janus’s tact and Julio’s reassurance. Do not invent mentorship, kinship or a formal alliance.'],meanings=[
    'Janus asks Admiral FI what they should do.',
    'Rafael asks Julio about his understanding that the Algiers pirates and Spain are on bad terms.',
    'Julio explains that they chiefly target Spanish ships and will probably soon clash with Admiral Valdes, commander of the royal navy.',
    'Rafael recalls reports that Spanish pressure has lately made trade difficult for Portuguese fleets.',
    'Rafael hopes their common enemy can give them a way out, invoking the idea that an enemy’s enemy is a friend.',
    'Claudio calls him naive and reminds him that these are pirates.',
    'Janus remarks uneasily that this looks bad.',
    'Hayreddin challenges them about what they are doing in the southern Mediterranean.',
    'Claudio reacts that they have been spotted.',
    'Janus wonders how they can get out of this.',
    'Julio has heard that Hayreddin values pride; looking ready to flee might only make them prey. He recommends facing him confidently.',
    'Rafael repeats the idea of acting confidently, steels himself and clears his throat.',
    'Rafael begins a grand declaration: they are Portuguese voyagers traveling the world under the banner of defeating Spain and restoring Portugal.',
    'Rafael announces their organization’s name, FO.',
    'Rafael declares that he is Admiral FU, using the full-name substitution.',
    'Julio praises the impressive declaration.',
    'Their crew cheers and applauds.',
    'Salid calls Rafael an idiot and threatens to kill them all.',
    'Rafael thinks the attempt has failed and they are about to be killed.',
    'Hayreddin tells Salid to wait.',
    'Hayreddin asks whether they really said they meant to defeat Spain.',
    'Rafael stammers that they did.',
    'Hayreddin laughs at the entertaining prospect of them making an enemy of the Invincible Armada.',
    'Claudio protests, asking what is so funny.',
    'Hayreddin warns Claudio to watch his mouth.',
    'Janus checks Clau and urges him to leave this to FI; he then encourages their leader to show what he can do.',
    'Claudio grumbles, relents and tells FI to do his best.',
    'Rafael decides to take a chance and try.',
    'Salid taunts them about their vanished bravado: if they mean to beat the Armada, they ought at least to be prepared to stand against the pirates.',
    'Rafael stammers that this is exactly right.',
    'Hayreddin notes the bold claim but warns that attempting it in their present condition would get them killed.',
    'Rafael agrees emphatically that now is not the time.',
    'Salid demands what he means.',
    'Hayreddin laughs and asks when the right time will be.',
    'Rafael says they will gain experience, train and acquire the strength to face Hayreddin on equal terms.',
    'Salid laughs that no one is so softhearted as to stand by while someone else rises to power.',
    'Rafael provokes them: are the Algiers pirates more cowardly than their reputation, afraid they could not beat his fleet once it grows strong?',
    'Salid reacts angrily to the challenge.',
    'Rafael asks to be allowed to travel freely through these waters and vows eventually to defeat the Spanish Armada.',
    'Salid angrily accuses him of getting far too carried away.',
    'Hayreddin recalls that Rafael introduced himself as FI.',
    'Hayreddin laughs and calls the youngster very entertaining.',
    'Salid protests to his admiral.',
    'Hayreddin accepts: they should explore and trade until their strength lives up to their words, and he will take them on when they are ready.',
    'Salid protests directly to Admiral Hayreddin.',
    'Hayreddin asks whether Salid seriously expects him to take such fledglings as real opponents now.',
    'Salid falters and denies that was his intention.',
    'Hayreddin dismisses the objection, saying an occasional game like this may be entertaining.',
    'Salid submits and says he understands.',
    'Hayreddin grants them passage through the Mediterranean, but tells them to conduct their trade in other seas.',
    'Rafael reacts in dismay to the restriction.',
    'Hayreddin asks whether their present fleet could handle angering both Valdes of Spain and the Ottoman Turks; neither great power is as lenient as he is.',
    'If they aspire to Mediterranean supremacy, Hayreddin tells them to make their name elsewhere first; unnecessary trouble here irritates him.',
    'Hayreddin pauses as he thinks of another condition or offer.',
    'Rafael nervously asks what it is.',
    'Hayreddin offers that if Spanish ships attack them, his fleet will reinforce them, but only within his own waters.',
    'Rafael is astonished and asks whether he means it.',
    'Hayreddin cautions that help cannot be guaranteed, since he too is a busy man.',
    'Rafael gratefully accepts.',
    'Hayreddin warns that any encroachment on his organization’s territory will be treated as a challenge to him and answered without mercy.',
    'Rafael hurriedly agrees to that condition.',
    'Hayreddin starts an unfinished thought about what Rafael might be able to do.',
    'Hayreddin dismisses the unfinished thought, tells them to grow strong enough to entertain him and stresses that they must keep their promises.',
    'Rafael says he understands and gives his word.',
    'Hayreddin accepts and orders his people to withdraw.',
    'The pirate crew answers his order affirmatively.',
    'Claudio praises FI’s effective bluff and says he did well.',
    'Janus observes that he secured a remarkable promise.',
    'Rafael sighs in relief, admits he surprised himself and says he is only now beginning to feel frightened.',
    'Claudio laughs that Rafael may be the sort who performs best under pressure.',
    'Julio praises what Rafael did.',
    'Rafael thanks everyone, but says that now he has made those claims he will have to work hard and become stronger.',
]),
}

if __name__=='__main__':
    output=ROOT/'B36_B37_92_clean_meanings_v1.json'
    assert not output.exists()
    source=ROOT/'clean_source_packet.json'
    packet=load(source)
    rows=[]
    for group in packet['groups']:
        if group['block'] not in DECISIONS:continue
        review=DECISIONS[group['block']]
        assert len(group['records'])==len(review['meanings'])
        for row,meaning in zip(group['records'],review['meanings'],strict=True):
            assert bytes.fromhex(row['source_hex'])[1:].decode('cp932')==row['source_Japanese']
            rows.append(dict(**row,source_meaning=meaning,exchange_context=review['context'],
                source_macros_complete={m:row['source_Japanese'].count(m) for m in ['FI','FA','FO','FU']},
                source_context_notes=review['notes'],native_identity_andEnglish_localization_andformatting_pending=True,new_credit=0))
    assert len(rows)==92 and sum(r['source_macros_complete']['FU'] for r in rows)==1
    save(output,dict(source=str(source),source_sha256=sha(source.read_bytes()),blocks=[36,37],records=rows,
        source_meanings_saved=92,all_complete_exchanges_reread=True,current_orhistorical_English_dialogue_not_consulted=True,
        FU_full_name_requires_separate_native_binding=True,no_new_completion_credit=True,new_credit=0,guide_photos=False,
        producer_sha256=sha(Path(__file__).read_bytes())))
    print('92 clean source meanings saved for complete B36/B37 exchanges;FU retained as distinct full-name macro.')
