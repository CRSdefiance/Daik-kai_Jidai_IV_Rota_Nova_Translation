"""Review flagged wraps in Hodram's early confrontations and recruitment exchanges."""

import argparse
from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import register_rafael_final_wraps_20261114 as parent
from scripts import stage_rafael_crew_wraps_20261114 as template
from scripts.source_locked_derivation_v5118 import checked_text


base, sha, prior = template.base, template.sha, template.prior
ARM, CLEAN, IlnkContainer = template.ARM, template.CLEAN, template.IlnkContainer
FILE = '/data/SC1.DK4'
ROOT = Path('work/hodram_opening_wraps_20261114_v1')
CAPTURE = ROOT / 'hodram_startup/capture_report.json'
RUNTIME = ROOT / 'hodram_native_context.json'
REVIEW = parent.TRIAGE.with_name('hodram_opening_wraps_context_v1.json')
PROOF = ROOT / 'stored_and_native.json'
DEFAULTS = {'FI': 'Hodram', 'FA': 'Bergstrom', 'FO': 'Bergstrom Fleet'}


DECISIONS = {
    (3, 47): ('Gerhard', "It seems a woman leads them...",
        'Gerhard observes that a woman appears to lead the pirates.',
        'Keep his hesitation after Hodram identifies them. Hodram immediately treats them as any other pirates.',
        ('a woman leads them...',)),
    (5, 5): ('Hodram', "Heave to! You're Julian Vermeer, aren't you?",
        'Hodram orders the ship to stop and asks if this is Julian Vermeer.',
        'Use a terse order and direct identification before the man’s drunken challenge.',
        ("You're Julian Vermeer, aren't you?",)),
    (5, 14): ('Julian Vermeer', "Glug, glug... Ahh! Hah! What's my country got to do with making money? Cross me and you'll regret it!",
        'Julian drinks, scoffs at talk of his homeland and making money, and threatens anyone who interferes.',
        'Keep the same drunken contempt as the parallel Rafael encounter. It answers Hodram’s charge of betrayal for money.',
        ("What's my country", 'got to do with making money?', "Cross me and you'll regret it!")),
    (17, 146): ('Dandy', "So you heard. Nobody follows her now.",
        'The pirate realizes the crew’s complaints were overheard and says nobody will follow Aziza anymore.',
        'Keep the abrupt dismissal after Hodram asks whether they simply want Aziza gone.',
        ('Nobody follows her now.',)),
    (17, 160): ('Dandy', "Fine. We ain't letting her go for free.",
        'The pirate refuses to hand Aziza over without payment.',
        'Keep the pirate’s rough voice and opportunistic price demand before Al objects.',
        ("ain't letting her go for free.",)),
    (17, 229): ('Aziza', "So when I found out you had his sword, I had to have it. I thought...",
        'Aziza says she was determined to get the sword when she learned they had it, then hesitates.',
        'Echo the same grief and unfinished thought as the Rafael encounter. She explains what the sword meant after Hodram waits.',
        ('you had his sword,', 'I had to have it.', 'I thought...')),
    (17, 269): ('Yukihisa', "Serving a savior is a worthy path.",
        'Yukihisa says devoting oneself to a benefactor is one way to live.',
        'Keep the dignified approval after Aziza says she owes Hodram her life and promises to work hard.',
        ('is a worthy path.',)),
    (29, 19): ('Manuel', "Wh-what?! They just opened fire!",
        'Manuel is startled when the other ship opens fire without warning.',
        'Keep the stammer and identify gunfire before Gerhard wonders if it was a mistake.',
        ('They just opened fire!',)),
    (33, 8): ('Diogo', "Maldonado's dealt with. English pirates still cause trouble.",
        'Diogo says Maldonado has been dealt with, while English pirates continue to cause trouble.',
        'Preserve the contrast with the unresolved threat before Diogo proposes extending their agreement.',
        ("Maldonado's dealt with.", 'English pirates', 'still cause trouble.')),
    (34, 18): ('Fernando', "Hah! You poor fool. I bet you'll lose!",
        'Fernando mocks his opponent’s misplaced confidence and says he would bet on the opponent losing.',
        'Keep the insult and the definite challenge in answer to the opponent’s laughter.',
        ('You poor fool.', "I bet you'll lose!")),
    (39, 46): ('Aziza', "Who knew a ship like that existed...",
        'Aziza marvels that such a ship exists.',
        'Keep her genuine astonishment after Hodram names the type of ship.',
        ('a ship like that existed...',)),
    (44, 21): ('Lil', None,
        'Lil demands to know if Hodram is listening and says she is talking to him.',
        'Keep her clipped challenge after his silence. Put her second sentence together before he finally answers.',
        ("I'm talking to you!",)),
    (44, 84): ('Camille', "Um, I-I'm sorry... Please don't take offense. I know that's a lot to ask.",
        'Camille stammers an apology, asks them not to take offense, then admits that may be impossible.',
        'Keep the nervous stammer and self-correction after Lil’s threat. Camille trails off and says goodbye next.',
        ("Um, I-I'm sorry...", "Please don't take offense.", "I know that's a lot to ask.")),
    (54, 14): ('Port Worker', "So I see. Do your best, then. Heh heh.",
        'The speaker acknowledges that Hodram is new, tells him to do his best, and snickers.',
        'Keep the faintly mocking encouragement and laugh that leave Hodram puzzled.',
        ('Do your best, then.', 'Heh heh.')),
    (58, 172): ('Hodram', "I may be no different from them...",
        'Hodram concedes that he might be much the same as the Westerners he has just criticized.',
        'Keep the introspection and uncertainty, leaving Sera’s halting disagreement as the next beat.',
        ('I may be no different from them...',)),
    (58, 239): ('Manuel', "An icy isle far to the northwest... Iceland, perhaps?",
        'Manuel hears of a distant icy island to the northwest and wonders whether it is Iceland.',
        'Keep the direction and make Iceland a deduction. It follows the clue about the demon king’s weapon.',
        ('An icy isle far to the northwest...', 'Iceland, perhaps?')),
    (63, 45): ('Hodram', "Nagarpur, was it? What are you playing at?",
        'Hodram addresses Nagarpur dismissively and challenges what he is trying to do.',
        'Keep the pointed question following the crew’s indignation. Nagarpur answers with an offer of more money.',
        ('Nagarpur, was it?', 'What are you playing at?')),
    (65, 71): ('Hodram', "The world's finest navy is my goal. I couldn't ask for better parting words.",
        'Hodram says Sera’s parting words could not be more fitting for someone who aims to build the world’s best navy.',
        'Keep the private ambition and sincere farewell after Sera predicts he will rule the seas.',
        ("the world's finest navy", "couldn't ask for better", 'parting words.')),
    (67, 84): ('Hodram', "I'm not sure what you mean. Who are you, anyway?",
        'Hodram says he does not follow what the woman means, then asks who she is.',
        'Keep his shift from puzzlement to a frank question before Maria gives her full name.',
        ("I'm not sure what you mean.", 'Who are you, anyway?')),
    (69, 19): ('Lil', "No. I nearly doubted Maria. So glad you came back.",
        'Lil rejects Camille’s reassurance, says she almost doubted Maria, and is relieved Camille returned.',
        'Keep the apology’s emotional progression and distinguish Maria from the person Lil is addressing.',
        ('I nearly doubted Maria.', 'So glad you came back.')),
    (72, 91): ('Hodram', "I'd like to know if that's confidence or a bluff. For now I have no quarrel with you. No need to get so worked up.",
        'Hodram wonders whether Maria is confident or bluffing, says he has no present quarrel with her and tells her to calm down.',
        'Keep the measured provocation followed by a temporary assurance. He goes on to accept her proposal on its merits.',
        ('confidence or a bluff.', 'For now I have no quarrel with you.', 'No need to get so worked up.')),
    (72, 121): ('Hodram', "'So agreeable. So easy to handle.' Isn't that what you're thinking? Just wait for the good news.",
        'Hodram voices what he imagines Maria is thinking about his compliance and tells her to expect good news.',
        'Keep the sarcastic quotation and tag together, following Maria’s remark about his sarcasm.',
        ('So easy to handle.', "Isn't that what you're thinking?", 'Just wait for the good news.')),
    (77, 12): ('Gerhard', "Admiral, His Majesty requests that we take the field.",
        'Gerhard reports that a request to go into battle has arrived from the king.',
        'Preserve the request and the royal source. Hodram asks what it says after the crew’s report.',
        ('His Majesty requests', 'we take the field.')),
    (79, 49): ('Barbarossa', "Heh. Bad luck for you. If you cross them, be ready to die.",
        'Barbarossa calls it bad luck and warns Hodram that opposing the Ottomans could cost his life.',
        'Keep his grim amusement and the risk. Hodram asks about Barbarossa’s alliance with the empire next.',
        ('Bad luck for you.', 'If you cross them,', 'be ready to die.')),
    (79, 90): ('Barbarossa', "If you lose, do it with some dignity.",
        'Barbarossa warns Hodram not to lose in a disgraceful manner.',
        'Keep the sardonic farewell after he gives Hodram the token he despises.',
        ('do it with some dignity.',)),
    (80, 80): ('Hodram', "I still have work to do. Too dangerous. Go home.",
        'Hodram has work left to do, says it is dangerous, and orders Sera home.',
        'Keep the terse orders in answer to her intention to board. She refuses to give up.',
        ('I still have work to do.', 'Too dangerous.', 'Go home.')),
    (81, 43): ('Hodram', "It's been a while. So you're in charge of building the town.",
        'Hodram greets someone he knows and realizes that person is directing the building of the town.',
        'Keep the recognition and the responsibility. The following voices discuss taking a rest and the town’s slow progress.',
        ("It's been a while.", "you're in charge", 'building the town.')),
    (81, 51): ('Hodram', "Yes. We'll rest here tonight.",
        'Hodram agrees to spend the night resting in town.',
        'Use a brief decision before Gerhard comments on how little has been built.',
        ("We'll rest here tonight.",)),
    (84, 165): ('Hodram', "Settled, then. Your name? I'm {MACRO:FI} {MACRO:FA}.",
        'Hodram considers it settled, asks the recruit’s name and gives his own first and last names.',
        'Keep the sequence and both name substitutions. He welcomes Emilio after the reply.',
        ('Your name?', "I'm {MACRO:FI} {MACRO:FA}.")),
    (85, 105): ('Cristina', "I think Mom and Dad want me to quit swinging a sword and settle down. It drives me crazy.",
        'Cristina thinks her parents want her to give up swinging a sword and settle down, and she resents it.',
        'Keep her clipped exasperation and both parental expectations. Julio takes it as characteristic of Harald.',
        ('Mom and Dad', 'quit swinging a sword', 'and settle down.', 'It drives me crazy.')),
    (86, 37): ('Cristina', "I'm not back for good! We just stopped in London. I'll be off again soon!",
        'Cristina denies having returned home to stay, says they happened to stop in London and will leave again soon.',
        'Keep her impatient insistence. She follows it by saying she did not come back for him.',
        ("I'm not back for good!", 'We just stopped in London.', "I'll be off again soon!")),
    (87, 17): ('Hodram', "Looking to enlist? If you've got the skills, I'll consider it.",
        'Hodram asks if the applicant is volunteering to join and says he might consider it if the applicant is competent.',
        'Keep his matter-of-fact recruitment language before the applicant describes his abilities.',
        ('Looking to enlist?', "If you've got the skills,", "I'll consider it.")),
    (87, 20): ('Janus', "Yes. I like machinery. I'm good with ships, and I can fix them, too.",
        'Janus likes machinery and is good at handling ships and repairing them.',
        'Keep both practical skills as the answer to Hodram’s qualification, before they discuss terms.',
        ('I like machinery.', "I'm good with ships,", 'I can fix them, too.')),
    (88, 89): ('Sailor', "Oh? Want a fight? Boss, they bumped into us, and now they want a fight!",
        'The sailor challenges them and tells his boss they caused the collision and are now picking a fight.',
        'Keep his account as an accusation. The other crew has just charged them with causing the same collision.',
        ('Want a fight?', 'Boss, they bumped into us,', 'and now they want a fight!')),
    (88, 93): ('Kurushima', "Heaven might forgive you. Kurushima won't! Get 'em!",
        'Kurushima says even if heaven forgives them, he will not, and orders his men to attack.',
        'Keep the theatrical name-drop and swift order to his crew.',
        ('Heaven might forgive you.', "Kurushima won't!", "Get 'em!")),
    (91, 31): ('Fernando', None,
        'Fernando says the other man has no right to speak to their admiral like that.',
        'Keep his indignant wording before the man challenges him again. The brief lead leaves the insult and the reference to his admiral together.',
        ('that to our admiral!',)),
    (91, 69): ('Sailor', "A Miracle Bullet Charm. They say it works miracles.",
        'The sailor identifies the bullet pendant said to bring about miracles.',
        'Keep the item name and attribute the claim. Hodram is surprised the man would give it to him.',
        ('A Miracle Bullet Charm.', 'They say it works miracles.')),
    (92, 44): ('Trader', "Sure. You raved about our tomatoes.",
        'The trader says it is fine because they praised the tomatoes he sells.',
        'Keep the house’s tomatoes and cordial reason for the gift before Hodram thanks him.',
        ('raved about our tomatoes.',)),
}


get_source = checked_text(getsource(template.get_exchanges), {
    'extras = {6096, 7436} if block == 84 else set()': 'extras = set()',
})
compile_source = checked_text(getsource(template.compile_rows), {'Original Rafael exchange': 'Original Hodram exchange'})
initial_names = template.previous
bind_source = checked_text(getsource(initial_names.bind_runtime), {'actual_captain_getter=0': 'actual_captain_getter=1', 'captain=0': 'captain=1'})
expand_source = checked_text(getsource(initial_names.macro.expand), {'captain==2': 'captain==1'})
env = template.compile_rows.__globals__ | globals() | {'previous': initial_names}
for source in (get_source, compile_source):
    exec(compile(source, __file__ + '::original-Hodram-exchange', 'exec'), env)
get_exchanges, compile_rows = env['get_exchanges'], env['compile_rows']
env = initial_names.bind_runtime.__globals__ | globals()
exec(compile(bind_source, __file__ + '::original-Hodram-context', 'exec'), env)
bind_runtime = env['bind_runtime']

native_env = vars(initial_names.macro).copy()
exec(compile(expand_source, __file__ + '::original-Hodram-name-consumer', 'exec'), native_env)
native = FunctionType(template.native.__code__, template.native.__globals__ | {
    'expand_source': lambda: native_env['expand'],
    'expand_bytes': FunctionType(template.expand_bytes.__code__, vars(template) | globals()),
}, argdefs=template.native.__defaults__)
expand_bytes = FunctionType(template.expand_bytes.__code__, vars(template) | globals())
expanded = FunctionType(template.expanded.__code__, vars(template) | globals())
contract_source = checked_text(getsource(template.contract), {
    "macro_ascii_lengths={'FI':6,'FA':6,'FO':10}, macro_widths={'FI':36,'FA':36,'FO':60}":
        "macro_ascii_lengths={'FI':6,'FA':9,'FO':15}, macro_widths={'FI':36,'FA':54,'FO':90}",
})
env = vars(template) | globals() | {'previous': initial_names}
exec(compile(contract_source, __file__ + '::measured-Hodram-name-widths', 'exec'), env)
contract = env['contract']
compile_rows.__globals__['contract'] = contract
main = FunctionType(template.main.__code__, vars(template) | globals())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preview', action='store_true')
    main(parser.parse_args().preview)
