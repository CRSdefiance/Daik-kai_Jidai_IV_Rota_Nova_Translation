"""Read route aftermath,companion jealousy andSpanish confrontation without older English."""
from pathlib import Path
from scripts.source_only_gloss_v1 import seal

ROOT=Path('work/analysis/Rafael_B61_B80_clean_20261104')
MEANINGS={
71: '''
5|Rafael reflects that the Kurushima faction has fallen.
10|Claudio says this may clear the way to obtaining East Asia's Proof of Conquest.
13|Actor106 reacts approvingly to the news that Kurushima is gone.
17|Claudio chuckles andcasually confirms their success.
27|The local speaker asks whether they are looking for the Proof of Conquest.
30|Rafael confirms that they are andasks whether the speaker knows something about it.
34|The local speaker says that leader Li in Hangzhou is rumored to know something.
39|In the alternative already-informed question,Rafael asks whether the speaker knows where Admiral Maria Li can be found.
43|The local speaker confidently says she is usually in Hangzhou.
58|Rafael asks whether leader Li is famous.
63|The local speaker says that is an understatement:the Kurushima pirates were about the only fools around who would defy Admiral Li.
67|Claudio concludes that they had better avoid a direct fight with her.
74|Rafael thanks the informant anddecides to head for Hangzhou.
''',
72: '''
11|Maria reluctantly acknowledges the visitor as this region's dominant sea power andtells him to accept the offered object;do not invent a formal coronation.
21|Rafael thanks Admiral Li.
25|Maria says she has no choice andwill stay in this land to see whether he proves worthy of that standing.
31|In the unidentified-speaker alternative,Rafael asks who she is.
36|Maria dismisses her identity as unimportant andsays he may forget her.
39|Rafael remains silent at that reply.
58|In the promised-reward branch,Maria acknowledges the effort Rafael has made.
62|Rafael excitedly calls her Maria,then catches himself andswitches to Admiral Li.
67|Shien explains that the admiral has been waiting here andbegins the handover.
71|Maria gives Rafael the promised diagram.
77|Maria recalls his name as FI andwarns him not to let his guard down in other waters.
81|Rafael stammers an emphatic thank-you.
86|Claudio chuckles that Rafael is completely flustered.
90|Rafael protests to Clau andhurriedly orders their departure.
94|Claudio snickers andplayfully complies with the admiral's order.
''',
73: '''
6|Claudio remarks that FI has changed lately,seeming more grown-up.
10|Rafael laughs andasks whether Claudio really thinks so.
15|Claudio explains that Rafael seems calmer andless prone to worrying than before.
18|Rafael is pleased that even Clau notices andadmits that the change is thanks to Eirene.
23|Claudio reacts sharply to Eirene's involvement anddemands an explanation.
26|Rafael is puzzled by the reaction andasks why Claudio is angry.
31|Rafael explains that after their earlier quarrel,Eirene told him not to carry his worries alone.
36|Rafael admits that,because he is admiral andleader of FO,he may have grown presumptuous in trying to handle everything himself.
40|He says her advice that talking can ease a burden proved true andcompares Eirene to an older sister;the comparison does not establish kinship.
44|Claudio pauses silently.
48|Rafael praises Eirene as kind,attentive andunpretentious.
52|Rafael speculates that if everyone knew she was actually a woman,they might all compete for her attention;preserve his hypothetical teasing,not an actual contest orrelationship.
56|Claudio defensively demands who exactly would compete for her.
60|Rafael says he meant it generally,asks why Clau is taking it so seriously,then begins a knowing realization.
65|Claudio stammers a vehement denial andtells Rafael not to say ridiculous things.
69|Rafael insists he was only joking andsays Claudio need not shout.
73|Claudio blames Rafael's strange remarks andstammers that he is going out.
77|Rafael casually sees him off,then privately thinks Claudio is the one acting strangely.
''',
74: '''
5|Actor113 enthusiastically greets FA,says the final confrontation with Valdes is coming andurges him to defeat Spain;the respectful form does not create a new noble title.
8|Actor104 asks whether the decisive battle will be off Seville andwarns him to take care.
12|Actor83 reports that fleets appear to be gathering one after another.
16|Claudio concludes that once they are ready to fight Spain,they should go to Seville andtells FI to remember it.
19|Rafael reflects on the coming clash with Valdes's forces at Seville andsays they should prepare beforehand.
24|Actor147 suggests avoiding the area until they are ready.
27|Rafael thanks the informants andsays he will remember the warning.
32|Actor113 remembers to tell Rafael that the king wants to see him;the identity of the king andevent context still require exact source binding.
''',
75: '''
6|Actor48 rudely tells Rafael's party to move out of his way.
10|Rafael reacts with shock.
15|Claudio angrily calls the man out.
19|The man demands whether Claudio knows whom he is addressing.
23|Claudio says he does not care anddemands why the man acts so superior after colliding with them himself.
27|The man invokes his membership in the Linares family of Cordoba andasks whether they knowingly insult him;do not invent a particular noble rank.
30|Rafael repeats the unfamiliar Linares name.
43|Janus nervously wonders whether the man might be a nobleman orsomething similar.
57|Julio worries that this may become troublesome.
64|Claudio dismisses the family name andinsists that shoving people aside without apologizing is unacceptable.
68|The man pauses before acting.
72|Claudio reacts in surprise andrecognizes the thrown object as a glove.
75|The man orders Claudio to draw a sword anddeclares a duel.
79|Claudio reacts incredulously.
83|Rafael protests that an immediate duel is an excessive response.
88|The man says nobody in the Spanish navy would silently endure an insult to his pride.
91|Claudio scorns that pride andasks whether spoiled,crazy nobles like this are going to dominate their Portugal.
94|The man realizes they are Portuguese andsays that explains their improper attitude toward Spanish military men.
98|He tells them that Spain's Invincible Armada will henceforth be responsible for protecting the Portuguese.
102|He boasts that their peaceful trade is possible only because Spanish forces fight enemies day andnight.
106|Rafael reacts angrily to that claim.
111|The man says he will overlook today's outrage andorders them out of his sight.
114|Rafael sharply tells him to wait.
119|The man asks whether they still fail to understand.
123|Rafael rejects the claim that Spaniards protect them andtells the man to stop deluding himself.
128|The man reacts in disbelief to the defiance.
132|Rafael insists FO operates under its own strength andwill never submit to Spain.
137|The man recognizes Rafael as the presumptuous youth who still claims Portuguese nationality,calling that claim fraudulent.
141|Rafael denies any fraud andinsists that Portugal will always be his homeland,not Spain.
146|The man contemptuously says Rafael is clinging to a country that no longer exists.
150|Rafael insists Portugal is not gone andvows that they will restore it.
155|The man is outraged at the audacity of restoring Portugal.
158|He declares that restoration is rebellion against the Spanish kingdom andtherefore Rafael cannot be allowed to live.
162|He says there is no need to trouble Valdes andwill cut Rafael down here himself,ordering him to draw.
166|Rafael defiantly accepts the challenge,with an initial stammer.
171|Claudio warns that he will not go easy on the man even if he cries partway through.
174|Valdes calls Simon by name anddemands what he is doing.
177|Simon is startled by Valdes's arrival andaddresses him respectfully.
180|Rafael realizes they have been surrounded.
184|Claudio realizes they cannot escape under these conditions.
188|Simon reports that the men were plotting rebellion against His Imperial Majesty andhe was about to execute them;preserve the source皇帝 title without inventing the ruler's personal name.
191|Valdes questions the allegation of rebellion.
195|Simon says they made subversive remarks about restoring Portugal.
198|Valdes hears Portugal andasks whether they belong to FO.
202|Rafael defiantly confirms it.
207|After a pause,Valdes orders Rafael's party to leave.
210|Rafael reacts in surprise to the release.
215|Simon reacts in confused surprise.
219|Claudio is also surprised.
223|Valdes says they will settle matters at sea eventually andorders them to leave the city now.
226|Rafael leaves with frustrated resentment.
231|Claudio asks whether Valdes thinks he is showing mercy.
235|Valdes laughs at the idea of mercy andasks whether they really imagine they can defeat his forces.
238|Valdes boasts that his fleet is invincible as its name says,with an unshakable formation embodying tradition anddignity,andthat they are beneath his notice.
242|Claudio curses andwarns Valdes not to regret this.
246|Simon calls to Valdes after the departing party.
250|Valdes tells Simon it is undignified to quarrel with children like them.
253|Simon nervously acknowledges the rebuke butstarts to protest.
256|Valdes says he cannot bear to soil the great royal capital with the blood of losers;do not replace the game's stated place/status with an unrelated historical capital.
260|Simon claims to understand andapologizes for his rashness.
264|Valdes adds that the opponents will be ideal target practice for the newly assembled combined fleet.
267|Simon respectfully praises Valdes's insight.
'''}
CONTEXT={
71:"Complete Kurushima aftermath/local directions. Different conditional questions cover learning of Li versus already knowing Maria;do not read both as a linear discovery. Hangzhou is explicit. Maria's power is described by a local speaker,not a new player rank.",
72:"Complete alternative handovers:reluctant regional recognition/unidentified Maria andthe known promised-reward meeting. Preserve their condition distinction. Maria stays cool andformal,Rafael slips from her personal name to Admiral Li andbecomes flustered,Claudio teases. No romantic commitment is established.",
73:"Complete companion teasing linked explicitly to the earlier B63 quarrel/reassurance. Rafael's growth is learning to share burdens;Claudio reacts defensively to Eirene andthe hypothetical competition. The source supports jealousy/romantic subtext,not an established partner orcontest. Eirene is privately understood to be a woman;do not globally change Arcadius's public nameplate. Older-sister comparison is figurative.",
74:"Complete local final-battle warnings from four separate speaker selectors:prepare before approaching Seville,where fleets are gathering,andremember the king's summons. Bind each source role/name andthe exact king/event before final prose;no sailor/elder/official rank is inferred solely from an ID.",
75:"Complete collision/glove challenge,Portuguese-Spanish confrontation,Valdes interruption andprivate Spanish coda. Simon invokes his Cordoba family andSpanish navy pride;Claudio refuses his class arrogance. Rafael first tries to avoid a duel,then becomes fierce when Portugal's identity is denied. Valdes releases them from contempt andnaval strategy,not sympathy. Preserve Linares/Simon/Valdes identities,the imperial address,the royal-capital claim andcombined fleet training motive without inventing ranks,kinship orhistorical corrections."}

if __name__=='__main__':
    seal(ROOT/'clean_source_packet.json',ROOT/'B71_B75_116_clean_meanings_v1.json',MEANINGS,CONTEXT,__file__)
