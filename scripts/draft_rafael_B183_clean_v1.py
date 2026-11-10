"""Draft the visitation and morning follow-up from complete clean Japanese."""
from scripts.seal_clean_independent_drafts_v1 import seal


CONTEXT = {183: (
    "Sanghyeon addresses Rafael with formal courtesy. He and Yifa trained under the same teacher, and he was her senior. "
    "His formal connection to her was severed after she left, but they grew up like siblings and he worries about her. "
    "Rafael is unsure whether this was a dream. Yifa senses Sanghyeon and explains that he used his arts to visit. "
    "Rafael relays the advice and reminds Yifa she also owes the crew her share of the work."
)}
DATA = {183: {
    10: ("The visitor’s first call reaches Rafael only as a respectful address.", "...Sir..."),
    14: ("Rafael does not respond.", "..."),
    19: ("The visitor uses FI with a respectful honorific.", "...FI, sir..."),
    23: ("Rafael stirs in confusion.", "...Hm?"),
    28: ("The stranger apologizes for approaching so suddenly and says he means no harm.", "Forgive me for approaching you so suddenly. I mean no harm."),
    31: ("He gives a formal greeting and introduces himself as Sanghyeon, Yifa’s senior under the same teacher.", "It is an honor to meet you. My name is Sanghyeon. Yifa and I trained under the same teacher. I was her senior."),
    35: ("He learned that Rafael would take Yifa in and came to speak with him briefly.", "I heard that you had agreed to take Yifa in. I came to have a word with you, if I may."),
    39: ("Rafael starts to ask about the visitor’s connection to Yifa.", "You're Yifa's...?"),
    44: ("Sanghyeon is ashamed and blames his own shortcomings in guiding Yifa for her unrestrained behavior.", "It pains me to admit this, but Yifa grew up with so little restraint because I failed to guide her properly."),
    47: ("She left the mountain without permission to avoid training, then left the country. He says this is unacceptable.", "She came down from the mountain without our teacher's permission to get out of training. Then she left the country. That cannot be excused."),
    51: ("Yifa likely does not know that people from their unnamed country are forbidden to leave it.", "She probably has no idea, but the people of our country are forbidden to go abroad."),
    55: ("Rafael asks whether Sanghyeon came to take Yifa back.", "Did you come to take Yifa back?"),
    59: ("Sanghyeon cannot take her back. Breaking the prohibition is a grave offense and she has been expelled from their training school.", "Even if I wanted to, I could not. Breaking that law is a grave offense. Yifa has been expelled from our school."),
    62: ("His formal connection to her has already been severed.", "I no longer have any formal ties to her..."),
    65: ("Despite that, they grew up together like a real brother and sister.", "But we grew up together, as close as any brother and sister."),
    68: ("He is anxious that the inexperienced Yifa may behave badly in front of others.", "She still has so much to learn. I cannot help worrying that she will do something improper in front of others."),
    72: ("He knows it is presumptuous to ask, but requests that Rafael guide Yifa so she does not stray from the right path.", "I know I am asking a great deal. Please guide Yifa and help her stay on the right path."),
    75: ("If possible, he asks Rafael to tell Yifa to keep training off the mountain and follow her teacher’s instructions.", "And if you can... Tell her to keep up her training, even away from the mountain, and remember what our teacher taught her."),
    78: ("He closes by asking Rafael to look after Yifa.", "Please take good care of Yifa."),
    81: ("Rafael wonders whether it was a dream because it felt unusually real.", "Was that... a dream? It felt awfully real for a dream..."),
    85: ("Yifa calls an exuberant good morning and starts urging Rafael to leave before stopping.", "Good morning! Hey, let's get going alrea..."),
    88: ("Yifa reacts in sudden wordless surprise.", "!!!"),
    92: ("Rafael asks what is wrong.", "What's wrong?"),
    97: ("Yifa senses the presence of her senior fellow student.", "I can feel him. The senior I trained with!"),
    101: ("Rafael echoes the relationship and asks if the person is Sanghyeon.", "Your senior? Wait, is his name Sanghyeon?"),
    105: ("Yifa asks how Rafael knows and where Sanghyeon is.", "How do you know that?! Where is he?"),
    109: ("Rafael says a man appeared in his dream and introduced himself as Yifa’s senior fellow student, named Sanghyeon.", "Well, a man showed up in my dream just now. He said you trained together and he was your senior. His name was Sanghyeon."),
    113: ("Yifa repeats that it was a dream.", "A dream?"),
    117: ("Yifa softly addresses Sanghyeon with familial warmth.", "...Sanghyeon..."),
    121: ("Yifa realizes he could not leave the mountain in person, so he came to see them by using his art.", "I get it... He couldn't leave the mountain, so he used his arts to come see me."),
    125: ("Rafael is surprised that the encounter could be part of her arts.", "His arts? Y-you can do that with them, too?"),
    129: ("Rafael passes on the instruction to obey her teacher off the mountain and tells her Sanghyeon was worried.", "He said to follow your teacher's instructions even away from the mountain. He was really worried about you."),
    134: ("Yifa laughs warmly that Sanghyeon will always be a worrier.", "Oh, Sanghyeon... Hee hee. He'll always be such a worrier."),
    138: ("Rafael pauses and asks what is the matter.", "...What's wrong?"),
    142: ("Yifa vows to work hard at training because she doesn’t want to disappoint Sanghyeon.", "I'm gonna train hard! I don't want to let Sanghyeon down!"),
    146: ("Rafael says training is fine but she must do shipboard work too.", "Hold on. Training's fine, but we need you to do your share of the work aboard, too."),
    150: ("Yifa cheerfully assures Rafael he can count on her.", "Don't worry! You can count on me!"),
}}
if __name__ == '__main__':
    seal('work/analysis/Rafael_B181_B200_clean_20261105', 'B183_clean_drafts_v1.json', DATA, CONTEXT, {}, __file__, 37)
