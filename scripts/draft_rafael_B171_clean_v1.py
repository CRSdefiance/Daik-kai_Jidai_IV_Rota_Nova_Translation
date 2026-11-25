"""Draft Cristina’s complete flamenco exchange from clean Japanese."""
from scripts.seal_clean_independent_drafts_v1 import seal


CONTEXT = {171: (
    "Rafael, Claudio and Cristina have been drinking when lively music starts. Cristina excuses herself to dance, "
    "two patrons cheer, and Rafael and Claudio react. Claudio’s teasing gives way to a genuine apology and recognition "
    "of Cristina as a crewmate in her own right. The two numbered patron labels, joint cheer and applause are four "
    "distinct source modal panels. Keep their header/body placements for native qualification."
)}

DATA = {171: {
    5: ("Rafael exhales and says they have had quite a bit to drink.", "Whew. We really did have a lot to drink."),
    10: ("Claudio boasts that a man of the sea should hold his liquor and points out that Cristina seems unfazed.", "What are you talking about? A man of the sea has to hold his liquor. Look at Cristina. She’s doing just fine."),
    13: ("Rafael points out Cristina is not a man and tells Clau he has had too much.", "Cristina isn't a man, Clau... You've had too much to drink."),
    17: ("Cristina agrees she too has had a lot, then notices the music.", "I've had quite a bit myself. Oh..."),
    22: ("Rafael notices passionate music starting up.", "Listen. That music's got some fire to it."),
    27: ("Claudio agrees it makes him want to dance.", "Yeah, it makes you wanna get up and dance."),
    31: ("Cristina recognizes the tune and politely excuses herself.", "This tune... Excuse me a moment."),
    34: ("Rafael starts to call after Cristina.", "Oh, Cristina..."),
    39: ("Claudio calls out and asks if Cristina is going to the privy.", "Hey, Cristina! Going to the privy?"),
    44: ("The source heading identifies Patron 1. He is impressed by the young woman.", "Patron 1: Look at her go!"),
    47: ("The source heading identifies Patron 2. He admires her looks and how well she dances.", "Patron 2: Yeah! She's beautiful, and can she dance!"),
    52: ("Rafael is impressed by Cristina’s performance.", "Cristina, that was amazing."),
    57: ("Claudio is taken aback by the performance.", "Well... That was a surprise."),
    61: ("The two source headings stand together over three increasingly drawn-out Bravo cheers.", "Patron 1 and Patron 2: Bravo, bravo, bravooo!"),
    64: ("The crowd’s applause is presented as a separate sound-effect panel.", "Applause!"),
    68: ("Cristina says she could not help dancing because she likes this tune.", "I couldn't help myself... I love this tune."),
    71: ("Rafael reiterates his praise and says Cristina looked genuinely impressive.", "...That was incredible. You looked amazing out there, Cristina."),
    76: ("Cristina thanks Rafael and admits she is embarrassed by the praise.", "Thank you. You're making me blush."),
    80: ("Claudio uses a teasingly formal title and observes that the swordswoman likes flamenco too.", "So our fine swordswoman likes flamenco, too."),
    84: ("Cristina falls silent after Claudio’s comment.", "..."),
    88: ("Rafael calls out Clau and objects to his rude tone.", "Clau! What's with that tone? That's rude!"),
    92: ("Claudio says he meant no insult. He had thought Cristina was a dull woman who only practiced swordsmanship.", "I wasn't taking a shot at you. I figured all you ever did was practice with your sword. I thought you were boring."),
    95: ("Cristina is surprised by the admission.", "What?"),
    99: ("Claudio apologizes after admitting he misjudged her.", "I'm sorry..."),
    103: ("Claudio says he likes Cristina and will now recognize her as a companion in her own right beyond being the old man’s granddaughter.", "You're all right. I used to think of you as the old man's granddaughter. From here on out, you're one of us."),
}}


if __name__ == '__main__':
    seal('work/analysis/Rafael_B161_B180_clean_20261105', 'B171_clean_drafts_v1.json', DATA, CONTEXT, {}, __file__, 25)
