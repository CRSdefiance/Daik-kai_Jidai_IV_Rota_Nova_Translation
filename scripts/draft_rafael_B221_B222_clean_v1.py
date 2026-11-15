"""Seal the Muramasa letter and red sword rumor from clean Japanese."""
from pathlib import Path
import re

from scripts.audit_story_glyph_consistency import load, save
from scripts.seal_clean_independent_drafts_v1 import seal
from dk4tool.patch.grand_race_menu_release import sha


ROOT=Path('work/analysis/Rafael_B221_B240_clean_20261106')
CONTEXT={
    221:"The crew announces a letter, with alternate voices before and after the reading. Yukihisa writes formally about a cursed Muramasa blade said to be hidden by enemies of the Tokugawa. Jam and the alternate speakers find the letter hard to read. Rafael thinks the search is worth trying. The final author signature is separate and indented in the clean text.",
    222:"A crewmate tells Rafael a rumor about a sharp red-tinged sword a lord sealed without using. He calls the lord cowardly. Rafael is intrigued and asks where it is. The crewmate never learned the location and suggests looking when they have a chance. Keep the reported history and the speaker's guesses distinct.",
}
DATA={
    221:{
        27:("Yukihisa has heard of the legendary Muramasa, a cursed sword believed to spell ill fortune for Tokugawa, Japan's ruler. There is an effort to eradicate the famous blades.",
            "Word has reached me of the legendary Muramasa, a cursed blade. It is said to bring ill fortune to Tokugawa, the ruler of Japan. There are efforts afoot to rid the world of these renowned swords."),
        30:("A clan with a grudge against Tokugawa seems to have hidden one of the blades somewhere in East Asia. Yukihisa sends word for now.",
            "A clan that bears Tokugawa a grudge appears to have hidden one of the blades somewhere in East Asia. I thought you should have word of it."),
        33:("Yukihisa is sure this is the object he has long sought. He signs the letter with his full name on a separate indented row.",
            "I have no doubt it is the very blade I have sought all these years. Yukihisa Genjo Shiraki"),
        65:("Jam calls the writing needlessly complicated and says it is typical of Yukihisa.",
            "He sure makes it a chore to read. That's Yukihisa for you."),
        71:("Rafael is impressed and says the blade is worth looking for.",
            "Huh! This sounds worth looking for."),
    },
    222:{
        5:("The crew member calls the admiral's attention to an interesting lead.","Admiral, listen to this! I heard something you might want to know."),
        8:("He heard a local lord obtained an exceptionally sharp sword.","Word is a lord around here got hold of an incredibly sharp sword."),
        11:("Rafael reacts with enthusiasm.","Oh, nice!"),
        16:("They say the blade is faintly red and looks as if it has drunk the blood of many people.","They say the blade's got a red tint. Looks like it's had its fill of blood."),
        20:("Rafael considers the red sword.","A red sword, huh..."),
        25:("Apparently the lord found it unsettling and sealed it away somewhere without ever using it. The speaker guesses the lord was a coward.","The lord said it gave him the creeps, so he sealed it away somewhere without ever using it. Must've been a real coward."),
        28:("Rafael thinks such a fine sword is going to waste.","But it's a fine sword, right? Seems like a waste to me."),
        32:("The crew member calls the lord a fool and asks what he thought a sword was for.","What a fool. What did he think a sword was for?"),
        36:("Rafael acknowledges the sword has a story to it and asks where the lord hid it.","It does sound like there's a story behind it. Where do you think he hid it?"),
        40:("The crew member did not hear where it was hidden and suggests looking when they have a chance.","Couldn't find out where, but let's look for it if we get the chance."),
    },
}
ANNOUNCE={
    0:("Announce the letter in an attentive tone.","Admiral, a letter came in from Yukihisa."),
    42:("Give the admiral the news in formal language.","Admiral, we have received a letter from Yukihisa."),
    84:("Announce the letter conversationally. This body serves two style slots.","Admiral, there's a letter from Yukihisa."),
    122:("Politely inform the admiral that Yukihisa sent a letter.","Admiral, a letter for you from Yukihisa."),
    168:("Announce the letter in a crewman's casual voice.","Admiral, you've got a letter from Yukihisa."),
    206:("An older voice calls the admiral's attention to the letter.","Admiral, here's a letter from Yukihisa."),
    244:("A youthful voice calls out about the letter.","Admiral! Yukihisa sent you a letter!"),
}
REACTION={
    0:("The reader finds the writing difficult and typical of Yukihisa.","It's a tough read, isn't it? That's Yukihisa for you."),
    38:("The reader formally remarks on the difficult writing and its author.","It's a rather difficult letter. Quite typical of Yukihisa."),
    70:("The reader makes a friendly observation about the difficulty and style.","It's hard to read, huh? Just like Yukihisa."),
    106:("The reader politely remarks on the writing and recognizes Yukihisa's style.","It's a hard letter to read, isn't it? It sounds just like Yukihisa."),
    144:("The crewman finds the writing awfully complicated and typical of Yukihisa.","He sure doesn't make it easy to read. That's Yukihisa, all right."),
    188:("An older voice remarks on the difficult wording and recognizes the author.","That's a tricky bit of writing. Just what you'd expect from Yukihisa."),
    226:("The young reader cannot make out what the letter says. No Yukihisa comparison here.","It's so hard! I can't tell what it says."),
    270:("The reader finds the letter difficult and emphatically recognizes the style.","That's a rather difficult letter. Yes, that's Yukihisa through and through."),
}


def main():
    speech=ROOT/'B221_B222_clean_speech_drafts_v1.json'
    styles=ROOT/'clean_style_objects.json'
    out=ROOT/'B221_B222_clean_drafts_v1.json'
    assert not out.exists()
    seal(ROOT,speech.name,DATA,CONTEXT,{},__file__,15)
    ordinary,objects=map(load,(speech,styles))
    rows=[]
    for r in objects['records']:
        if r['block']!=221:
            continue
        prefix,command,offset=r['id'].rsplit('_',2)
        assert prefix=='SC0_B221_STYLE' and int(command) in (8,702)
        meaning,draft=(ANNOUNCE if int(command)==8 else REACTION)[int(offset)]
        assert not re.search(rb'F[A-Z]',bytes.fromhex(r['source_hex']))
        rows.append({**r,'source_meaning':meaning,'independent_English':draft,'context':CONTEXT[221],
            'speaker':'Runtime-selected crew voice. Exact identity binding pending.',
            'review':dict(source=False,context=False,localization=False,naturalness=False,formatting=False),
            'current_English_comparison_pending':True,'complete_native_style_binding_andformatting_pending':True,
            'native_literal_token_counts':{},'new_credit':0})
    assert len(rows)==len(ANNOUNCE)+len(REACTION)==15
    assert sum(len(r['source_style_indices']) for r in rows)==16
    records=ordinary['records']+rows
    assert len(records)==len({r['id'] for r in records})==30
    save(out,{**ordinary,'records':records,'records_count':30,'physical_style_alternatives':15,
        'source_style_alias_slots':16,'signature_layout_pending':'DK4_MES_B221_R0033',
        'evidence':{**ordinary['evidence'],**{str(p):sha(p.read_bytes()) for p in (speech,styles)}}})
    print('Sealed 30 clean-only drafts across the complete letter and sword-rumor exchanges.')


if __name__=='__main__':
    main()

