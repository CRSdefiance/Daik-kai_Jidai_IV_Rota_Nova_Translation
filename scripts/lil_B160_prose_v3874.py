"""Whole-exchange decisions: missing ship, sleepy banter, eyewitness and search plan."""
REVISIONS={
5:("Admiral! This is terrible! The ship... It's gone!",'Restore the alarm and broken repetition before the missing-ship report. The singular ship remains singular; no flagship or entire fleet is invented.'),
8:("Gone...? Are you sure you're not mixing it up with the ship next to it?",'Restore the neighboring-ship explanation as Lil\'s doubtful question, rather than reducing it to an unspecified wrong ship.'),
11:("That's a pretty bad joke this early in the morning...",'Restore a complete spoken complaint and explicit morning context. Camille has not stated that he personally just woke up.'),
23:("Oh, come on! I need my beauty sleep!",'Localize Angelo\'s vain sleep-and-skin complaint with the natural beauty-sleep idiom. Preserve the sleepy comic setup for his later wide-awake reaction.'),
32:("I-it's true! The ship's gone!",'Restore Lil\'s startled hesitation and confirmation after the source transition, without suggesting literal magic.'),
46:("It wasn't me! I don't eat things that look that bad! Honest!",'Restore Emilio\'s defensive first-person rule about unappetizing food. The older claim that ships taste awful implies unsupported prior knowledge; the source speaks only about appearance.'),
50:("I'm kidding. Wait... This is no time for jokes! What's going on?!",'Restore Lil\'s self-correction from the Emilio joke back to alarm. Keep all four turns inside their shared optional branch.'),
61:("W-what should we do?!",'Restore the Sailor\'s anxious stammer while keeping the short appeal spontaneous.'),
83:("Hey! Admiral!",'Render the Port Worker\'s call for attention and source rank directly. Remove Wait, which can imply an unspoken departure or demand to stop.'),
87:("This is terrible! I saw a lanky young man tinkering with the ship all by himself early this morning...",'Restore the alarm, eyewitness attribution, lanky young appearance, solitary activity and early-morning timing. No identity, motive or authorized inspection is established.'),
110:("We're in a bind... What should we do, {MACRO:FI}?",'Restore Camille\'s troubled assessment before asking the captain. Preserve the logical FI substitution and the independent core exchange.'),
113:("I never thought he'd set sail! He was alone, so I assumed he was just checking the ship or something.",'Restore the witness\'s mistaken assumption and explicit failure to expect a departure. The inspection remains his guess; the line works without Angelo\'s optional challenge.'),
117:("That's true... You wouldn't expect him to set sail all by himself.",'Restore Lil\'s sympathetic agreement and the specific surprise at a solitary departure. Do not assert that sailing alone is universally impossible.'),
121:("Let's start by asking around town and looking for the ship thief.",'Restore Camille\'s connected proposal to gather information and search. Keep the ship reference and first step without inventing a known destination or recovery.')
}
RETAIN_NOTES={
29:'No joke! Come to the harbor now! naturally carries the Sailor\'s insistence that the report is real and his immediate summons to the port facility. The urgency needs no new office name or duration.',
43:'Did Emilio eat it? is a natural absurd hypothetical in Lil\'s optional food joke. The preceding missing-ship confirmation makes it clear what it refers to; it does not establish an eaten ship.',
54:'The ellipsis accurately preserves Emilio\'s silence after Lil catches herself joking. Adding an explanation or guilt would invent an unspoken reaction.',
73:'Mamma mia! Wide awake now! preserves Angelo\'s source cultural exclamation and natural comic reversal of his sleepy complaint. Its spoken fragment suits his sudden alarm.',
79:'What\'s going on? is a complete natural puzzled question and keeps Camille\'s core response coherent with either optional branch absent.',
91:'Then he sailed off! naturally completes the Port Worker\'s eyewitness report with the source alarm. It supplies no unsupported identity or motive.',
103:'Why didn\'t you stop him? naturally conveys Angelo\'s incredulous reproach as a question. It does not establish that the worker could have stopped the departure.',
132:'Mamma mia! What rotten luck! naturally preserves Angelo\'s source exasperation and repeated cultural expression as the comic closing tag, with no new blame or biography.'
}
