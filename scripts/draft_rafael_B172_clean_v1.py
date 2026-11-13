"""Draft Samwell’s complete market and cooking audition from clean Japanese."""
from scripts.seal_clean_independent_drafts_v1 import seal


CONTEXT = {172: (
    "Rafael’s group is surprised by a cow in the road before a market vendor asks to join them. Samwell boasts of skills, "
    "admits he has no experience, then insists on a cooking audition. The food overturns Claudio’s skepticism, and "
    "Samwell undercuts his own proverb about concealed talent by congratulating himself. Leave the unnamed dish unnamed."
)}

DATA = {172: {
    6: ("Rafael reacts with delight at the unfamiliar sight.", "Wow! Look at that!"),
    11: ("Claudio is startled to find a cow lying in the middle of the road.", "What in the world?! There's a cow lying right in the middle of the road!"),
    14: ("Julio says it is nothing like their own country.", "Quite different from back home, isn't it?"),
    19: ("Samwell cheerfully calls out to customers and praises everything he is selling.", "Come on over! See anything you like? It's all good stuff!"),
    22: ("Samwell notices unusual customers and eagerly asks if they are travelers.", "Well, here's a face I don't see every day. Hey, you folks are travelers, right?"),
    25: ("Samwell wants them to take him along. He is tired of seeing elephants and wants to visit other countries.", "Perfect! Take me with you. I'm tired of looking at elephants. I want to see other countries. How about it?"),
    28: ("Rafael is startled by the sudden request, confirms they are sailors and asks whether Samwell has any special skills.", "H-huh? That's a little sudden. We are sailors, yes, but... What can you do?"),
    33: ("Samwell proudly says he is a good cook and asks if that would be handy at sea.", "Ahem! I'm a great cook. That comes in handy at sea, doesn't it?"),
    36: ("Rafael considers it but says someone aboard can already cook.", "Hmm. Cooking... We do already have someone who can cook."),
    40: ("Samwell says he is good with his hands and guesses he could build ships or perhaps make maps.", "I'm handy, too. I bet I could build ships. Might even be able to make maps."),
    44: ("Samwell boasts that he learns quickly and has good instincts, affirming his own assessment.", "I'm a fast learner. I've got good instincts, you know. Yep, I do."),
    48: ("Claudio cuts through the bragging and asks whether he has any experience.", "All right, all right. Have you actually done any of that?"),
    51: ("Samwell cheerfully admits he has no experience at all.", "None whatsoever!"),
    55: ("Claudio is bewildered by the admission.", "Huh?!"),
    59: ("Julio is amazed Samwell can boast so much with no experience.", "You talk a big game for someone who's never done it."),
    62: ("Samwell asks what is strange about it, says he is young and quick to adapt, then brags about his instincts again.", "What's so strange about that? I'm young. Give me a chance and I'll get the hang of it. I told you I've got good instincts. Ahem!"),
    65: ("Rafael sees no problem and says he likes Samwell.", "I don't see why not. I like him."),
    69: ("Claudio asks whether an admiral should make a decision so casually.", "Hey, hold on. You're the admiral. Shouldn't you think this through?"),
    73: ("Samwell unexpectedly agrees that Rafael is being too casual.", "He's right. You're taking this a little too lightly."),
    76: ("Rafael is baffled because Samwell just asked to be hired.", "Wait, what? Weren't you just asking me to hire you?"),
    81: ("Samwell says yes but insists Rafael appreciate how good he is first.", "Sure. But you've got to see how good I am first."),
    85: ("Rafael asks what Samwell proposes.", "So what do you want to do?"),
    90: ("Samwell asks to be tested.", "Give me a test!"),
    94: ("Rafael asks what kind of test he means.", "What kind of test?"),
    99: ("Samwell will make one dish and proposes passing if everyone says it tastes good.", "I'll make you one dish. If everyone says it tastes good, I pass. How's that?"),
    103: ("Rafael agrees and tells him to go ahead.", "All right. Let's see what you can make."),
    110: ("Samwell presents the food after the wait.", "Thanks for waiting. Here you go!"),
    114: ("Claudio finds the dish odd and asks if it is something disgusting while already chewing.", "What's this? It looks downright weird. This isn't something awful, is it? (Munch, munch.)"),
    118: ("Claudio pauses, stammers, then draws out how good it tastes and repeats the judgment.", "...Th-this is goooood! This is really good!"),
    121: ("Rafael agrees it tastes good.", "You're right. It's delicious."),
    126: ("Julio agrees and notes appearances can be deceiving.", "Oh, that is good. Hmm. You can't judge a person by appearances."),
    129: ("Samwell puffs himself up and invokes the proverb that a talented hawk hides its claws.", "Ahem! They say the truly talented don't show off, you know."),
    133: ("Claudio deadpans that Samwell should not be saying that about himself.", "...You're not supposed to say that about yourself."),
    137: ("Rafael asks whether everyone is now happy for Samwell to join them.", "So we're all agreed? He can join us?"),
    141: ("Samwell cheers, gives his full name and greets the group.", "I did it! I'm Samwell da Khan. Glad to meet you!"),
}}


if __name__ == '__main__':
    seal('work/analysis/Rafael_B161_B180_clean_20261105', 'B172_clean_drafts_v1.json', DATA, CONTEXT, {}, __file__, 35)
