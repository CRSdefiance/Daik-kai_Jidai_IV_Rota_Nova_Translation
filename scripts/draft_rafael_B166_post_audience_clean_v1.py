"""Draft the full post-audience exchange from the clean B166 source."""
import inspect

from scripts import seal_clean_independent_drafts_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

CONTEXT = {166: (
    "Rafael comes back from the audience and catches part of Claudio and Eirene's private talk. Claudio makes light of "
    "their impending separation and Eirene presses him to say what he wants. The crew's whispered reactions give way "
    "to embarrassment when the two notice them. The change from restrained concern to teasing gives way to Rafael's "
    "own decision. Eirene acknowledges that the crew knows her identity. Rafael reveals he declined the appointment, "
    "defends Albuquerque's conduct and proposes exploring uncharted waters instead. Claudio laughs and offers his help. "
    "Preserve the Japanese FE speaker heading and alternating visual placement separately from logical prose. "
    "The crew's guesses and teasing do not establish a marriage or any undisclosed commitment."
)}

DATA = {166: {
    170: ("Rafael greets Claudio and says he is back.", "Hey, Clau. I'm back."),
    175: ("Claudio is surprised that Rafael returned so quickly.", "Huh? That was quick."),
    183: ("The source FE heading identifies Eirene. Puzzled, she addresses Claudio by name.", "...Claudio?"),
    187: ("Claudio catches himself starting to call her Arcadius and switches to Eirene.", "Oh, Arca... I mean, Eirene."),
    190: ("Under Eirene's source heading, she asks if Claudio was with the others.", "Weren't you with the others?"),
    193: ("Claudio says stiff, formal places do not suit him and lets the thought trail off.", "I'm just no good in stiff places like that, you know?"),
    196: ("Under her heading, Eirene chuckles gently and concedes he may be right.", "Heh heh... I suppose not."),
    201: ("Claudio asks what brings Eirene there and guesses that she will receive a higher scholarly rank.", "What about you? Aren't they going to make you some kind of high-ranking scholar?"),
    205: ("Under her heading, Eirene says that seems to be the case, but wonders whether accepting is right without a major research achievement.", "It seems so. I haven't made any great discoveries, though. I wonder if it's right to accept."),
    208: ("Under her heading, Eirene says higher rank means more research funding, good news for a penniless researcher.", "Still, a higher rank means more funding. That's welcome news for a penniless researcher like me."),
    211: ("Claudio's half-audible line leaves only the end of his thought about her going away.", "...you'll be gone."),
    215: ("Under her heading, Eirene asks what he said because she could not hear him.", "Hm? What was that? I couldn't hear you."),
    219: ("Claudio deflects and asks whether she is returning to Athens to do her research.", "Nothing... You're going back to Athens to do your research, right?"),
    222: ("Under her heading, Eirene says she thinks so and presses him to repeat what he just said.", "I think so. But you said something just now, didn't you? What was it?"),
    225: ("Claudio pauses in silence.", "..."),
    229: ("Claudio says he just saw her look like a scholar again and begins imagining what happens once she leaves the ship.", "Just now, you looked like a scholar again. Once you leave the ship..."),
    233: ("Claudio thinks she will go into a completely different world and is embarrassed by how unlike him the thought is.", "You'll be off to a whole different world. Ah, hell... Listen to me. Since when do I think like that?"),
    237: ("Under her heading, Eirene responds softly with Claudio's name.", "Claudio..."),
    240: ("Claudio laughs at how strange he is acting and blames first the weather, then the visit to the palace.", "Ha! I'm acting strange today. Maybe it's the weather. No, it's gotta be this palace."),
    245: ("In the staggered FE exchange Eirene addresses Claudio and asks what he wants her to do.", "Claudio... what do you want me to do?"),
    249: ("In the other FE placement Claudio blurts out a stammered response.", "Huh?! W-what do I want...?"),
    253: ("Eirene asks whether he wants her to give up her research.", "Do you want me to give up my research?"),
    257: ("Claudio says that is not what he meant and trails off.", "That's not what I meant..."),
    261: ("Eirene asks whether he wants her to stay away from Athens.", "Then you don't want me to go back to Athens?"),
    265: ("Claudio is silent in the alternating FE placement.", "..."),
    269: ("Eirene starts to suggest another possibility without naming it.", "Or..."),
    273: ("Claudio again has no answer in the alternating FE placement.", "..."),
    278: ("Janus quietly asks how things look.", "...Well?"),
    282: ("Rafael says he cannot make much out from where they are.", "I can't really tell from here..."),
    294: ("A watcher tells the others to stop pushing.", "Hey, quit pushing."),
    308: ("A watcher says he cannot see well.", "I can hardly see."),
    323: ("A watcher tells everyone they should stop, while audibly chewing.", "Come on, you guys, we shouldn't be doing this. Munch, munch."),
    337: ("A watcher cheers Claudio on at what seems to be the decisive moment.", "Go on, Clau! Now's your chance!"),
    352: ("A watcher shushes them, afraid they will be discovered.", "Shh! Keep it down! They'll hear us!"),
    359: ("Rafael almost calls her Arcadius, corrects to Eirene and reports that she nodded.", "Oh! Arcadius... I mean, Eirene just nodded..."),
    371: ("An eager watcher asks what happened.", "Hey, hey! What happened?"),
    378: ("Janus wonders if Claudio is blushing and says he has never seen him that way.", "Is Clau blushing? I've never seen him like this..."),
    381: ("A watcher mock-laments that Claudio may end up taking orders from her.", "Think she's got him wrapped around her little finger? Oh, what a sorry sight."),
    392: ("A watcher says the sight is hard to take and makes his back itch with embarrassment.", "Boy, I can hardly stand it. I'm getting itchy just watching."),
    413: ("This conditional speaker teases the complaining watcher about grinning the whole time.", "Says the one who's grinning from ear to ear."),
    422: ("An alternate watcher makes the same teasing observation in this branch.", "Says the one who's grinning from ear to ear."),
    435: ("Janus panics that the people they are watching are coming toward them.", "Oh, no! They're coming this way!"),
    440: ("An alternate watcher sounds the same alarm.", "Oh, no! They're coming this way!"),
    446: ("Rafael protests that it hurts, asks the crowd to stop pushing and cries out.", "Ow! W-wait! I said stop pushing! Whoa!"),
    452: ("Claudio recognizes Rafael and demands to know what the group is doing.", "FI! Wh-what are you all doing here?!"),
    455: ("Rafael awkwardly says he came looking for Claudio after the audience and did not mean to spy.", "Uh, well... The audience was over, so I came looking for you. I didn't mean to spy..."),
    459: ("Claudio indignantly insists they are not a spectacle.", "W-we're not putting on a show for you!"),
    471: ("A watcher cheekily says you cannot pass up a scene like that.", "Come on! You can't expect us to miss a scene like that."),
    478: ("Janus protests that he said they should stop, trailing off defensively.", "I did tell them we should stop, you know..."),
    489: ("A watcher calls everyone's behavior rude.", "Honestly, you people have no manners!"),
    504: ("Another points out that all of them ended up watching.", "You all ended up watching anyway..."),
    519: ("An optional watcher has no spoken response.", "..."),
    526: ("Eirene realizes that everybody now knows she is a woman.", "So you all know I'm a woman now."),
    529: ("Janus falters while trying to answer.", "Ah! No, I mean..."),
    533: ("Rafael says he thought it was all right to tell them by now, apologizes and doubts he could keep pretending not to know.", "I figured it was all right by now. I'm sorry... I wasn't sure I could keep pretending I didn't know."),
    538: ("Eirene reassures him, congratulates him on what she heard and jokes that she should not use his given name so casually now.", "Heh, it's all right. Oh, I heard the news. Congratulations, FI. Oh dear, I suppose I shouldn't be so familiar with you now."),
    541: ("Claudio seizes on the subject change and asks whether Rafael can afford to be killing time out here.", "R-right! Hey, FI! What are you doing standing around out here anyway?!"),
    550: ("Rafael simply asks why Claudio thinks that.", "Why?"),
    555: ("Claudio reminds him that he has supposedly just been appointed to some grand post and is expected to appear before a crowd.", "Why? You got appointed to some grand position, didn't you? Weren't they going to show you off in front of a crowd or something?"),
    559: ("Janus laughs quietly, in on the news.", "Heh heh."),
    564: ("Rafael begins an awkward answer before revealing the news.", "Well..."),
    568: ("Claudio gives a bewildered questioning reaction.", "...?"),
    572: ("Rafael tells Claudio that he turned the appointment down.", "I turned it down."),
    584: ("A companion exclaims in surprise.", "What?!"),
    591: ("Claudio repeats the news in a stammer of disbelief.", "Y-you turned it down?!"),
    595: ("Rafael explains that Admiral Albuquerque was originally commander in chief of Portugal's navy and that making a sailor like him viceroy would be strange.", "Yes. Admiral Albuquerque was commander in chief of Portugal's navy in the first place. A sailor like me, viceroy? It just doesn't seem right."),
    606: ("Claudio asks whether Rafael yielded the role to Albuquerque, accusing him of going over to Spain.", "Wait, you let Albuquerque have it?! That guy went over to Spain!"),
    610: ("Rafael argues that the officer never defected but simply gave his loyalty to the King of Spain, their sovereign at the time.", "He didn't go over to Spain. He's a military man. He was loyal to the King of Spain because that was our sovereign at the time."),
    617: ("Claudio exclaims that there are limits to being goodhearted and trails off in exasperation.", "Ah, come on! There is such a thing as being too nice! Why do you have to be so..."),
    621: ("Claudio softens and admits that this may be the very reason everyone followed Rafael.", "...Well, maybe that's exactly why we all followed you."),
    625: ("A companion gives a quiet double assent.", "Mm-hmm. Mm-hmm."),
    629: ("Rafael says that instead he offered to survey unknown waters to further develop Portugal's shipping.", "I offered to survey uncharted waters instead. It'll help Portugal build up its shipping even more."),
    633: ("Claudio laughs with approval at the idea of expedition leader instead of viceroy.", "Leader of an expedition instead of viceroy, huh? Ha ha! I like it!"),
    638: ("Claudio asks if this means Rafael will need his help after all.", "So you do need my help after all, huh?"),
    642: ("Rafael tells Claudio of course and says he is counting on him.", "Of course, Clau. I'm counting on you."),
    646: ("Claudio agrees with a boisterous assurance to leave it to him.", "You bet! Just leave it to me!"),
}}

source = checked_text(inspect.getsource(previous.seal), {
    "        b=group['block'];assert {int(r['id'].split('_R')[-1]) for r in group['records']}==set(data[b])":
        """        b=group['block']
        full=group['records']
        selected=full[26:102]
        assert len(full)==136 and len(selected)==76
        assert selected[0]['source_reference']['record_index']==170
        assert selected[-1]['source_reference']['record_index']==646
        assert full[102]['source_reference']['record_index']==658
        assert {r['source_reference']['record_index'] for r in selected}==set(data[b])""",
    "        for source in group['records']:": "        for source in selected:",
    "complete_blocks=list(data),source_contexts=contexts":
        "complete_blocks=[],source_contexts=contexts,complete_exchange_scope='B166 return from audience through Claudio joining the expedition, R0170–R0646',remaining_same_block_records=34",
    "across{len(data)} completeblocks": "for the post-audience B166 exchanges",
})
env = dict(previous.seal.__globals__)
exec(compile(source, __file__ + '::exact-post-audience-exchange-scope', 'exec'), env)

if __name__ == '__main__':
    env['seal']('work/analysis/Rafael_B161_B180_clean_20261105', 'B166_post_audience_clean_drafts_v1.json', DATA, CONTEXT, {}, __file__, 76)
