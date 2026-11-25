"""Read the complete London rescue exchange before consulting any old English."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

SOURCE=Path('work/analysis/Hodram_B81_B90_clean_20261101/clean_source_packet.json')
OUT=SOURCE.with_name('B86_clean_meanings_before_English.json')
MEANINGS=[
(5,'Actor7 enjoys returning to London and says nothing compares with the air of home.'),
(8,'Hodram tells her to take her time resting now that she is back in her hometown.'),
(12,'She thanks him and says she will walk around the port, which she has always enjoyed.'),
(16,'Hodram says the rest of them will be resting at the inn.'),
(19,'She finds that nothing has changed and enjoys the familiar surroundings.'),
(22,'The suitor loudly celebrates the reunion as a miracle of love and calls クリスティナ with extravagant elongated syllables; this is his interpretation.'),
(26,'She recognizes the danger of being spotted by him and reacts in alarm.'),
(30,'He tearfully says he knew his love would reach her and trails off emotionally.'),
(34,'She tells him not to cry because everyone is watching.'),
(37,'She insists that she has not returned permanently: the fleet is only stopping in London and she will soon travel again.'),
(40,'He reacts with a confused sound.'),
(44,'She emphatically repeats that she did not come back for him.'),
(47,'She states emphatically that she is not considering marrying him at all.'),
(51,'He laments the rejection and asks what she dislikes about him.'),
(54,'She explains that she is not thinking of marriage yet and asks him to give up; preserve her agency and refusal.'),
(58,'He finally says he understands and will give up, then laments the end of his love.'),
(62,'She sighs with relief that he will stop pursuing her.'),
(66,'She reacts abruptly to something nearby.'),
(70,'He sighs and then also notices something.'),
(74,'A woman screams for her little boy.'),
(78,'Actor7 asks what happened.'),
(83,'The mother says her boy fell into the sea and begs someone to save him. This expressly establishes her relationship to this child.'),
(87,'Actor7 tells the mother to wait and says she will rescue him.'),
(91,'She encourages the child to hold on and says help is coming now.'),
(95,'The suitor cries クリスティナ in alarm.'),
(100,'She reassures the child that she has reached him and he is safe. お姉ちゃん is a comforting self-reference to a stranger, not proof she is his sister.'),
(103,'An anonymous FE message visibly labels the speaker as a boy, who cries that he is frightened.'),
(106,'She reassures him again that he is safe.'),
(110,'She tells the boy not to cling to her neck because she cannot breathe. Her repeated お姉ちゃん does not establish kinship.'),
(113,'The FE boy voice repeats that he is frightened.'),
(116,'She realizes that if this continues, she will drown along with the child.'),
(119,'The FE boy voice cries out in fear again.'),
(122,'She struggles and says she cannot keep going and will drown.'),
(126,'The mother screams for someone to help.'),
(132,'The suitor asks whether nobody else is there to help.'),
(136,'He fears for クリスティナ but hesitates because of the sea and water.'),
(139,'He repeats his fear of the sea; the explicit greater-than comparison puts that fear above クリスティナ at this first stage of the joke.'),
(142,'He struggles against his hesitation and gives a loud resolving cry.'),
(145,'He repeats the fear, but the explicit less-than comparison now puts クリスティナ above the fear. Preserve the reversal, not two identical hesitation lines.'),
(148,'He repeatedly calls her name as he resolves to act.'),
(151,'He shouts an elongated クリスティーナ with emphatic punctuation; verify the same identity despite the lengthened pronunciation.'),
(155,'He announces his own launch as ミヴォール in theatrical elongated delivery.'),
(159,'He calls クリスティナ and says he is coming to help now. The clean body begins with a line break; preserve its intent through reviewed formatting, not an automatic authored leading blank.'),
(165,'She coughs awake, sees ミヴォール, and asks where she is and what happened.'),
(169,'He joyfully recognizes that his beloved has regained consciousness; affection is his voiced perspective.'),
(172,'She recalls drowning and immediately asks whether the boy is safe.'),
(176,'He confirms that the boy is safe and reports that the lady thanked them.'),
(180,'She concludes someone rescued them and wants to find and thank the person who saved her life.'),
(184,'He hesitantly indicates that her rescuer is right here.'),
(187,'She reacts in surprise.'),
(191,'He finally says he was the one who rescued her.'),
(194,'She objects in disbelief that he was afraid of water, trailing off.'),
(198,'He acknowledges that fear but says his thoughts changed when he felt he had to save クリスティナ; the sentence remains unfinished.'),
(202,'He says he somehow swam after all and can hardly believe it himself. Do not invent prior swimming lessons or a permanent cure.'),
(205,'She still finds it hard to believe that he did this.'),
(208,'She abruptly says she must get to the inn.'),
(212,'He asks whether she is all right.'),
(216,'She says she can go on her own.'),
(220,'He takes his leave, trailing off.'),
(225,'The boy recognizes the woman who tried to save him and calls her お姉ちゃん familiarly, without making her his sister.'),
(229,'She asks whether the child is all right.'),
(233,'He says he is fine, thanks her, and asks where the man who rescued them is. お兄ちゃん is familiar address to that rescuer, not a claim of brotherhood.'),
(237,'The mother sincerely thanks her and asks about the man who had been with her.'),
(240,'She asks whether he really jumped into the sea.'),
(244,'The mother confirms that he jumped in while shouting strangely.'),
(247,'The mother infers that he must love クリスティナ very much; keep this as her assessment, not proof of reciprocal love or consent to marriage.'),
(250,'She quietly realizes that his account was true.'),
(254,'The mother offers an unnamed token of thanks and asks her to accept it.'),
(259,'She awkwardly thanks the mother for the gift.'),
(263,'The mother takes her leave and thanks her again.'),
(266,'The boy says goodbye using the same familiar お姉ちゃん address.'),
(272,'Back with the group, she concludes her account with that is what happened.'),
(276,'Hodram is impressed that ミヴォール rose to the occasion.'),
(279,'She says she still has trouble believing it.'),
(283,'Hodram notices the man arriving just as they are discussing him and invokes the speak-of-someone idiom.'),
(287,'She notices ミヴォール and calls his name hesitantly.'),
(291,'He answers by calling クリスティナ softly.'),
(295,'She admits she did not thank him properly, thanks him now, and shyly says he looked admirable or dashing then.'),
(299,'He reacts with extravagant surprise.'),
(303,'He excitedly asks if she really thinks he looked dashing and says he is extremely happy.'),
(307,'She warns him that he is misunderstanding something; her compliment is not consent to the engagement.'),
(311,'He says he does not care, is simply delighted, and calls her name theatrically.'),
(315,'She tells him to stop being noisy and urges the fleet to leave because he is becoming a nuisance.'),
(319,'He promises to wait for her indefinitely.'),
(322,'Hodram chuckles that they make a good pair. Keep his teasing observation distinct from a confirmed romance or marriage.'),
]

if __name__=='__main__':
    assert not OUT.exists();packet=load(SOURCE)
    group=next(g for g in packet['groups'] if g['block']==86)
    meanings=dict(MEANINGS);assert len(meanings)==len(group['records'])==85
    rows=[]
    for source in group['records']:
        row=deepcopy(source)
        row.update(source_meaning_gloss=meanings.pop(source['source_reference']['record_index']),
            meaning_read_in_complete_clean_exchange=True,earlier_English_unconsulted=True,
            localization_andfive_gate_approval_pending=True)
        rows.append(row)
    assert not meanings
    save(OUT,dict(source_packet=str(SOURCE),source_packet_sha256=sha(SOURCE.read_bytes()),records=rows,
        meanings=85,blocks=[86],source_only_no_English_comparison_orlocalization=True,
        exact_individual_source_references_retained=True,
        whole_exchange_notes=['Refusal, attempted child rescue, fear versus devotion, unexpected courage, confirmation, thanks, comic overreaction and final teasing form one arc.',
            'The boy and his mother are relatives; neither rescuer is established as his sibling.',
            'Preserve visible FE boy labels and the reversed greater/less-than joke; no invented condition cure, courtship acceptance or wedding.'],
        new_credit=0,producer_sha256=sha(Path(__file__).read_bytes())))
    print('85 complete London rescue meanings saved before earlier English;no new credit.')
