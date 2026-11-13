"""Draft the optional coda, Charlotte's letter and the B166 departure from clean Japanese."""
import inspect

from scripts import seal_clean_independent_drafts_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

CONTEXT = {166: (
    "Eirene looks forward to new research and the crew shifts from teasing to preparing the expedition. Charlotte's "
    "letter arrives in careful but halting Portuguese, with a pronunciation aid and a separate Japanese reading for "
    "the player. Preserve both versions and the crew's responses to the letter's effort. Rafael's embarrassment gives "
    "way to a first destination and his familiar call to the crew. Keep 'Muint' as written by Charlotte. The phonetic "
    "hints are a draft English guide to the source's intended sound and require display qualification."
)}

DATA = {166: {
    658: ("Eirene imagines finding new research material in uncharted waters.", "Uncharted waters... I might find something new to study out there."),
    680: ("A companion pleads with Claudio to keep the flirting off the ship and threatens to make trouble otherwise.", "Just do me a favor and keep the flirting off the ship, or I'll raise hell."),
    683: ("Claudio sputters and tells the teaser not to talk nonsense.", "D-don't talk nonsense!"),
    695: ("A companion happily expects even more scenes worth watching.", "Oh, wow! Sounds like there'll be even more we can't afford to miss!"),
    714: ("A companion notes that Eirene looks happy and wonders if she should return to London.", "Eirene looks so happy... Maybe I should go back to London..."),
    723: ("An older companion urges them to begin expedition preparations right away now that it is decided.", "If that's settled, we'd best get the expedition ready."),
    726: ("Rafael says there is no need to rush and suggests they all rest because they are probably tired.", "We don't have to rush. I'm sure you're all tired. We can get some rest first."),
    731: ("Claudio warns Rafael that an expedition from another country could beat them to it.", "What are you talking about? If we drag our feet, another country's expedition will get there first!"),
    742: ("A companion dislikes that prospect and absolutely refuses to lose to somebody else.", "Now that won't do. I'll be damned if I'm losing to anybody."),
    756: ("A companion agrees that whoever moves first wins a contest.", "You bet. In a race, first one there wins."),
    770: ("Eirene laughs, remembers something and asks Rafael if he knows what it is.", "Heh heh... Oh, that's right. FI, do you know what this is?"),
    774: ("Rafael wonders if it is a letter.", "...What is it? A letter?"),
    779: ("Eirene confirms it and asks him to read it.", "That's right. Here, go ahead and read it."),
    782: ("Rafael wonders who sent it, pauses, then reacts in surprise.", "Who's it from, I wonder? ...Oh!"),
    787: ("The original FE letter opens with Rafael's given-name substitution.", "FI"),
    791: ("Charlotte attempts to thank Rafael for everything in Portuguese. Retain her original spelling and the separate phonetic gloss.", "Muint obrigada por tudo. (MWEEN-too oh-bree-GAH-dah por TOO-doo.)"),
    794: ("Charlotte's second line is halting Portuguese again, with a separate pronunciation gloss and her signature.", "Muint bem obrigada. (MWEEN-too beng oh-bree-GAH-dah.) Charlotte Miller"),
    797: ("The separate player reading uses Rafael's given name and Charlotte's signature and says she is very well. Its thanks are heartfelt.", "FI, thank you so much for everything. I'm doing very well, thank you. Charlotte Miller"),
    807: ("A companion hesitantly comments on the letter's halting wording.", "How should I put it... It's a little awkwardly written."),
    818: ("Another companion concedes that the meaning is clear despite the phrasing.", "Hmm... Well, you can tell what she means."),
    832: ("A companion calls the critic a fool for saying something so pointless.", "You idiot! Keep those stupid comments to yourself!"),
    846: ("A companion says Charlotte put her heart into the letter and calls the criticism terribly rude.", "She put her heart into that letter! How rude can you get?"),
    860: ("A companion drawls that the others fail to understand how a woman feels.", "How can you be this clueless about how a woman feels?"),
    869: ("Janus says Charlotte seems to have studied Portuguese and done her best to write the letter.", "It looks like Charlotte studied Portuguese and did her best to write this."),
    873: ("Rafael pauses and softly says Charlotte's name.", "...Charlotte..."),
    877: ("Claudio chuckles and declares their first destination settled.", "Heh. Guess that settles where we're going first!"),
    880: ("Rafael is startled and starts to object hesitantly.", "Huh?! B-but..."),
    884: ("Claudio teases Rafael for blushing and tells him to hurry up and get ready.", "Aw, look at him blush. Come on, get ready!"),
    887: ("Julio says nobody objects and that exploring the New World first is a good option.", "Nobody has any objections. The New World seems a fine place to start exploring."),
    891: ("Rafael responds to Julio by name, trailing off with feeling.", "Julio..."),
    899: ("Janus addresses Rafael as admiral and asks him to give the order as usual.", "That's right, Admiral. Give us the order, just like always."),
    902: ("Rafael pauses, then agrees with conviction.", "...All right!"),
    908: ("Rafael calls everyone to get under way in the closing FE placement.", "All right, everyone! Let's go!"),
    912: ("The crew gives a single loud affirmative cheer in the closing FE placement.", "Aye!"),
}}

source = checked_text(inspect.getsource(previous.seal), {
    "        b=group['block'];assert {int(r['id'].split('_R')[-1]) for r in group['records']}==set(data[b])":
        """        b=group['block']
        full=group['records']
        selected=full[102:]
        assert len(full)==136 and len(selected)==34
        assert selected[0]['source_reference']['record_index']==658
        assert selected[-1]['source_reference']['record_index']==912
        assert {r['source_reference']['record_index'] for r in selected}==set(data[b])""",
    "        for source in group['records']:": "        for source in selected:",
    "complete_blocks=list(data),source_contexts=contexts":
        "complete_blocks=[],source_contexts=contexts,complete_exchange_scope='B166 expedition and Charlotte letter through closing crew response, R0658–R0912'",
    "across{len(data)} completeblocks": "for the final B166 exchanges",
})
env = dict(previous.seal.__globals__)
exec(compile(source, __file__ + '::exact-ending-exchange-scope', 'exec'), env)

if __name__ == '__main__':
    env['seal']('work/analysis/Rafael_B161_B180_clean_20261105', 'B166_charlotte_letter_clean_drafts_v1.json', DATA, CONTEXT, {}, __file__, 34)
