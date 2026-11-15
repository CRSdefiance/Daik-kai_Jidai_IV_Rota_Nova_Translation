"""Complete B166 exchange decisions:ship-care metaphor,careful expertise andsource-specific room advice."""
REVISIONS={
5:("Is it the sail placement...? No, perhaps...","Make Manuel's absorbed opening natural spoken musing while preserving his uncertainty andunfinished reconsideration."),
8:("Hey! What do you want with this ship?","Lil challenges the stranger's purpose at her ship;want with naturally conveys business concerning it,without the predecessor's awkward request forsomething fromit."),
12:("Oh, is this your ship? A little more work would really improve her.","Preserve his recognition of the owner andtentative improvement claim in an easy conversational turn;do not invent diagnosed damage orpermission to refit."),
20:("Extra sails, perhaps... or a different basic sail type...","Keep additional sails andchanging the basic sail type as distinct alternatives in his continuing musing;the predecessor left type without a clear sail referent."),
23:("Um, excuse me...","Give Lil a natural hesitant attempt to interrupt before she loses patience;Pardon was overly formal for this brief failed interruption."),
27:("More gun batteries would make her stronger... Or perhaps a different cannon type would be better...","Correct gun decks to the reviewed gun-battery category andpreserve the second,distinct proposal to change cannon type andhis self-correction."),
33:("Oh, I'm sorry. I got carried away, and she's not even my ship...","Restore a complete natural apology andhis embarrassment about becoming absorbed in someone else's ship;remove the stilted thought-swept-me-away construction."),
37:("I'm Manuel. I used to be a navigator.","Restore the complete formerly-a-navigator statement instead of an isolated fragment;Manuel matches the original actor23 consumers andno rank orformal retirement is invented."),
48:("I must seem terribly rude. I'm sorry. But please, let me say one last thing.","Preserve his repeated apology,awareness of seeming presumptuous andrequest forone more remark in tactful spoken English."),
52:("This may be none of my business, but this ship is crying. Please take better care of her.","Use the natural unsolicited-advice idiom andrestore the request forbetter care. Crying remains Manuel's affectionate personification andsets up Camille's later callbacks."),
60:("I've spoken out of turn. Please don't take offense. Well, I'll be on my way.","Keep the apology,request not to take offense andpolite departure in a natural connected turn rather than detached presumptuous-words/farewell formulas."),
94:("What do you expect? I don't know the first thing about machinery. I can't help it!","Restore Lil's conversational defensiveness andemphatic technical ignorance;the source excuses her own conduct rather than declaring impersonally that nothing can be done."),
98:("Don't just shrug it off! That's why we need someone to love the ship in {MACRO:FI}'s place.","Camille rebukes her brazen dismissal,not a boast of expertise,andproposes a caretaker in FI's place. Preserve the name substitution andship-care context rather than replacing the admiral."),
112:("You mean become a navigator again? But it's been so many years since I left the sea...","Preserve his question andhesitation about the long time away withan explicit natural subject;add no numerical duration orformal retirement status."),
116:("But you should be just as capable as those of us still at sea. Someone who loves ships that much can't have forgotten the sea.","Restore the comparison withthe currently active crew andkeep his competence as Camille's encouraging belief. The ship affection andnot-forgotten-the-sea reasoning remain linked."),
123:("Then would you take good care of her? We seem to make her cry.","Restore Camille's polite request rather than an abrupt command andretain the affectionate crying callback andself-deprecating persuasion."),
127:("Thank you. If that's how you feel, I'll do it.","Make Manuel's grateful acceptance personal andnatural;the source responds to kind encouragement rather than pressure to insist or an impersonal accepted-position formula."),
134:("Now then, Admiral. May I offer some advice on refitting the flagship's Workrooms?","Restore the active first-person offer andbind Workrooms to the reviewed Help heading,while preserving flagship scope andthe optional advice question."),
153:("Assign officers with high Speech to the First Mate's Office or Chapel to ease the sailors' discontent.","Bind the active Speech skill andboth current room names;preserve the high-stat condition andeffect without adding numerical thresholds absent fromthis dialogue."),
157:("Staff in the Galley and Livestock Room help reduce the fleet's food and water consumption.","Restore the complete fleet-resource sentence andcurrent Livestock Room term. The source groups both rooms/resources without assigning one specific resource to each room oradding breeder as an unbound role."),
161:("A Surgeon in the Infirmary treats fatigue, disease and injuries among officers and sailors.","Bind Surgeon/Infirmary andrestore both affected groups andallthree conditions. Preserve this source's treatment claim without promising instant/full recovery orchanging it to other Help articles' effects."),
169:("A Shipwright like me repairs damage in the Lumber Room at sea. I also help refit and repair ships at shipyards.","Restore his explicit Shipwright self-description,at-sea timing,Lumber Room andboth shipyard services;the predecessor omitted several source facts."),
175:("The fleet's fate rests on your command. Be sure to give refitting the care it deserves.","Retain the working fleet-fate warning andmake the practical instruction a natural complete appeal forcareful refitting,without adding a new mechanic orcondition."),
181:("I see. I'll leave it to you, then.","Restore Manuel's courteous acknowledgment on the decline-advice path. He leaves the decision to the admiral;he does not reject recruitment orrespond withan abrupt dismissal.")
}
RETAIN_NOTES={
16:'The double question marks preserve the original wordless puzzled reaction andlet the interruption build without inventing a new question.',
30:'Enough already andthe direct identity question naturally capture Lil losing patience after several ignored interruptions;the complete turn is faithful andin voice.',
40:'The clipped navigator,huh reaction is natural unimpressed American speech forLil andacknowledges his former profession without adding admiration orrecruitment intent.',
44:'The complete opening sentence andtrailing old-habits thought naturally convey Manuel slipping back into his seafaring mindset when seeing a ship. The ellipsis supports his absorbed/apologetic voice without inventing elapsed years.',
56:'Hey,wait is a complete natural interruption as Manuel starts to leave,andadds no destination ornew demand.',
64:'The short ellipsis-plus-Odd judgment is natural sotto-voce Lil andpreserves her reaction that the man is strange without adding a diagnosis orstronger insult.',
68:'Camille\'s emphatic challenge,admiration andproposal that their ship could use someone like him form a coherent natural turn. Preserve the working FI substitution rather than hardcoding Lil.',
71:'Why is the exact natural short question that invites Camille to explain the proposal;further wording would add an unsupported reaction.',
75:'The direct FI rebuke andcrying explanation faithfully carry Camille\'s ship-care criticism andthe running personification. The emphatic full forms are natural in his gentle lecture;no new literal ship voice is implied.',
87:'The dry additional complaint is idiomatic Fernando andpreserves the optional hard-working-people jab,without adding abuse details ora new relationship.',
102:'The conditional crying callback andpermission question naturally express Camille\'s confidence andrequest to invite the man aboard. Keep his proposal as speech,not an earned gameplay effect.',
106:'The hesitation,named Camille address andqualified assent naturally capture Lil agreeing because he wants it. The turn remains reluctant rather than enthusiastic.',
109:'Sir is an ordinary respectful address here,not a factual rank,andthe complete care-for-our-ship question naturally conveys Camille\'s polite request without inventing kinship.',
119:'The short well-prefaced acknowledgment andellipsis naturally preserve Manuel admitting the point whilestill hesitating;the complete clause needs no rewrite.',
130:'The brief formal reintroduction andat-your-service closing suit Manuel accepting the role,andthe full name exactly matches both original actor23 consumers.',
149:'The complete courteous introduction naturally sets the advice focus on rooms useful forlong voyages. It does not claim to enumerate every room oradd a new voyage condition.',
165:'The complete sentence preserves sick/injured officers,faster recovery andboth reviewed Private Cabin/Recreation Room names without adding a guarantee orconflating it withthe Surgeon\'s treatment.',
172:'The two complete courteous sentences preserve his admission that the explanation was brisk andhis question about whether it helped. They read naturally in his deliberately polite instructional voice.'
}
CHOICE_NOTES={
0:'Please do naturally accepts the immediately offered advice andpreserves the polite request;it does not become a separate hiring decision.',
1:'Decline is a clear standard action label forpolitely passing on the offered advice. Its object is established bythe preceding question andthe separate source response;it does not refuse employment.'
}
