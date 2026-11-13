"""Save every contextual revision or justified retention against exact source/current references."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.refine_hodram_B301_B310_clean_drafts_v2 import OUT as DRAFTS,MEANINGS,ROOT
from scripts.review_hodram_B231_B250_contextual_v1 import mark_macros

CURRENT=ROOT/'current_v1/current_effective.json';OBJECTS=ROOT/'current_objects_v1/current_objects.json'
OUT=Path('translations/hodram_B301_B310_contextual_review_v1.json')

RETAIN={
301:{6:'The warm greeting and good-timing remark naturally introduce Matilda’s useful lead, with FI intact.',
9:'The direct question is natural when introducing the Colosseum and sets up the captain’s echo.',
13:'The puzzled echo naturally prompts Matilda’s explanation; no expansion is needed.',
21:'The appreciative acknowledgment and decisive formal order suit Hodram and preserve immediate departure.',
24:'The friendly parting caution and map-purchase reminder are complete and natural.'},
302:{180:'The clipped onward decision follows the companion’s report that the sandstorm will not ease; continued waiting and the order to advance are clear in the exchange.',
193:'The natural tactical judgment and decision to wait preserve the risk assessment after the repeated storm question.',
203:'The conventional system notice preserves exactly one elapsed day.'},
303:{6:'The friendly welcome naturally addresses FI without an invented relationship.',
9:'Safia’s complete, pleased statement preserves her improved dancing and gratitude without specifying an unspoken prior lesson.'},
304:{12:'The casual map question is natural for Sakura before departure; it asks about possessing the needed map.',
16:'The short answer follows that direct question; omitting the repeated subject is idiomatic and the forgotten map remains clear.',
35:'The acknowledgment and thanks naturally answer Sakura’s parting wish.',
98:'The complete imperative is a natural decisive order from Hodram and preserves entering the swamp.',
133:'Gerhard’s polite agreement and qualified estimate of being close preserve the expectation of arrival soon.',
155:'The conventional system notice preserves exactly one elapsed day.',
162:'The polite agreement, contrasting expectation and trailing reservation naturally answer the detour remark.',
168:'The excited discovery call preserves the source’s urgency without requiring a literal phonetic stammer.'},
305:{6:'The familiar greeting naturally acknowledges FI; it does not establish romance or kinship.',
27:'Sakura’s echo, recognition and trailing qualification preserve the temple being not nearby, preparing her partway offer.'},
307:{16:'The explicit unequip instruction is natural game terminology and preserves the equipment-removal requirement.',
59:'The grave figurative English preserves both keeping the Proof from evil people and avoiding corrupt desire; no new religious doctrine or identity is added.',
62:'The courteous collective acknowledgment fits the warning addressed to the expedition and preserves a firm commitment to remember it.'},
309:{89:'The brief frightened cry naturally conveys the sailor’s panic; no lexical stage direction is added.',
98:'The nervous stammer and complete plan question naturally prompt Hodram’s reassurance.',
167:'The clipped scratch dismissal and reassurance are idiomatic in an urgent injury exchange.',
174:'The conventional injury notice preserves FI as the injured captain and the completed injury state.',
226:'The urgent conversational question naturally addresses the injured companion.',
273:'After the companion’s reassurance, this brief acknowledgment conveys acceptance and relief without claiming the wound has already healed.'},
310:{6:'The complete friendly greeting naturally welcomes FI.',
9:'The casual question naturally confirms the city-gate inquiry.',
13:'The colloquial rule statement naturally leads into the next turn’s qualification; the pause need not spell out a conjunction.'},
}

SPECIAL={
(301,17):'Restore Matilda’s complete personal explanation and the reason for offering the Roman-ruins lead instead of telegraphic omitted subjects.',
(302,71):'Use a natural rationing instruction: the long journey calls for making drinking water last, not an unexplained Save our water command.',
(302,108):'Keep the specific sandstorm and Hodram’s firm decision to continue after judging it unlikely to subside.',
(302,137):'The source reports apparent fatigue and some apparent departures, not one confirmed collapsed sailor. Preserve uncertainty and do not invent death.',
(302,141):'Wait for the sandstorm to pass; the source does not diagnose overexertion or order a rest because they pushed too hard.',
(302,187):'Keep apparent sailor fatigue without strengthening it into confirmed exhaustion.',
(302,207):'Preserve the observation that the storm seems to have eased, rather than asserting complete cessation.',
(303,12):'Make the offer a conversational thank-you so it follows Safia’s gratitude naturally.',
(303,16):'The mosque is dedicated to a former king, not said to have been built by him. Restore the far-inland location and reported wonderful treasure.',
(303,20):'The rumor concerns acquiring the treasure through the king’s recognition, not permission to enter an invented vault. Keep it reported and invitational.',
(304,30):'Make Sakura’s friendly parting and safe-journey wish sound conversational without extending her participation.',
(304,129):'Use a natural remark about a considerable shortcut rather than the stilted save us much time construction.',
(304,137):'Preserve apparent fatigue rather than confirmed exhaustion.',
(304,148):'Preserve the explicit turn back before taking another route; this is the alternative swamp path.',
(304,159):'Keep Hodram’s observational estimate of the detour rather than removing the source’s qualification.',
(305,10):'Give Sakura’s personal plan and invitation a natural spoken subject and preserve today.',
(305,13):'Make Hodram’s religious objection a natural personal statement, preserving that he is not Buddhist and the trailing hesitation.',
(305,17):'Sakura reassures him that the visit is only to look around, rather than issuing a disconnected instruction to look around.',
(305,20):'The source recalls a related thought; it does not tell the party to halt.',
(305,24):'Make the nearby referent connect to Sakura’s proposed temple visit and retain the map’s golden-temple description.',
(305,31):'Make the shared journey explicitly partway and preserve the qualified expectation that the map should lead him onward.',
(306,13):'Restore the identifying Kinkaku-ji reference and the request to find a Yuan emperor’s memento without inventing an emperor’s personal name.',
(306,19):'Use the existing item45 label Kublai’s Greatsword and restore the Kinkaku-ji monk’s identifying reference.',
(307,12):'Restore the Kinkaku-ji monk’s identifying reference and the remembered search request.',
(307,30):'Use a natural entrance greeting rather than the abrupt Hey; the source is not an apology.',
(307,34):'Translate the still-Japanese arrival/object-recognition turn and preserve the monk’s startled certainty.',
(307,38):'Preserve the monk’s general confidence in Hodram in natural speech instead of the awkward unsupported formal worthiness declaration.',
(307,42):'Translate the still-Japanese central clue, preserving far northeast of China, the icy sea, small village, map-guardian clan and qualified expectation.',
(307,45):'Far northeast of China is not northeastern China. Restore the direction and distance of the echoed clue.',
(307,49):'Restore the missing base-of-a-vast-peninsula landmark alongside the high mountain on its eastern coast.',
(307,52):'Preserve ordinary-ship difficulty and the monk’s severe warning against treating the remote journey lightly, without inventing a ship class or region name.',
(307,55):'Preserve the same silence using scoped ASCII periods; fresh native glyph checks remain required.',
(309,94):'Use the natural calming command Calm down rather than the isolated adjective Calm.',
(309,117):'Restore the promised action of driving the wolf away rather than only leaving unspecified opponents to Hodram.',
(309,140):'Hodram admits letting his guard down, not being too slow; preserve his responsibility for the injury.',
(309,178):'Use a recognizable formation command and preserve the single concerted push; Ranks alone is not a natural order here.',
(309,249):'Restore the unfinished counterfactual regret about losing his balance and sincere apology rather than a clipped report of what happened.',
(309,280):'Preserve apparent fatigue rather than confirmed exhaustion.',
(309,285):'Keep the assessment tentative and use hungry rather than asserting starvation. Do not add a pack description or count.',
(309,294):'Preserve definite fatigue and apparent departures, not merely lagging behind; no deaths or exact headcount are supplied.',
(310,16):'Preserve the largely nominal isolation policy rather than declaring isolation ended. Keep the clandestine offer as Mihwa’s in-game explanation, not an external historical claim.',
}

STYLE_RETAIN={
(302,24):{1:'The complete map requirement and admiral address are natural and sufficient for the map gate.',
2:'The brisk conversational refusal clearly connects the absent map with being unable to proceed; it adds no route or acquisition requirement.',
5:'The older speaker’s concise cause-and-effect warning is natural and preserves losing the way without a map.',
6:'The short surprised question and warning suit the youthful concern and preserve the missing-map problem.'},
(302,392):{1:'The single trailing complaint exactly preserves the terse heat reaction.',
2:'The breath and clipped heat complaint are idiomatic while traveling in the heat.',
4:'The short emphatic complaint is natural for the blunt voice; it needs no added profanity.',
5:'The understated older-register complaint naturally conveys the considerable heat.',
6:'The breathless, short heat complaint suits the youthful register without an invented age.',
7:'The measured emphatic noun phrase works as a formal observation in this desert exchange.'},
(302,596):{7:'The formal three-part warning states the severe storm, risk of losing the way and question whether to continue; it reads naturally in the decision exchange.'},
(302,1320):{7:'The concise formal acknowledgment naturally accepts the decision to go onward without promising that the journey is safe.'},
(302,1786):{3:'The short assessment that there is no sign of stopping and open question naturally preserve the companion’s worried judgment.',
7:'The complete observation and polite decision question naturally report the continuing storm without adding a time interval.'},
(302,2900):{0:'The urgent attention call naturally points to the coming discovery without prematurely naming it.',
2:'The short shared-alias call naturally draws the admiral’s attention after the desert trek without naming the destination.',
4:'The direct look-there command naturally preserves the blunt pointing reaction.',
5:'The concise older-register attention call preserves the source without added identification.'},
(304,164):{0:'The inclusive departure suggestion naturally covers the exact shared source alternatives.',
2:'The energetic departure call is complete and natural.',4:'The casual departure suggestion suits the blunt voice.',
5:'The older formal suggestion is natural and needs no archaic embellishment.',6:'The cheerful departure call exactly matches the clean-first draft.',
7:'The polite departure question naturally fits the formal variant.'},
(304,296):{0:'The concise obstacle report and practical question are idiomatic in the expedition.',
1:'The terse obstacle report naturally prompts the route choice; an omitted article is normal in this immediate report.',
3:'The surprised observation and short question preserve the elegant voice’s reaction without inventing a hazard.'},
(304,638):{0:'The understated comparison naturally conveys the unexpectedly shallow water after choosing to enter; no depth or safety guarantee is added.',
1:'The brief comparison makes the lower-than-expected depth clear in context.',
2:'The short comparison and positive response naturally convey relief after entering.',
3:'The direct shallow-water observation and explicit relief preserve the emotional turn.',
4:'The blunt short assessment naturally fits the matter-of-fact surprise.',
5:'The initial interjection and understated observation suit the older register.',
6:'The surprised interjection and short comparison preserve the youthful discovery.',
7:'The understated assessment is natural after entering; the expected-depth comparison is implicit without a numerical or safety claim.'},
(309,24):{5:'The older speaker’s complete warning clearly connects the missing map with getting lost.',
6:'The youthful direct statement clearly identifies the needed map before proceeding.'},
(309,322):{0:'The inclusive departure suggestion naturally preserves all four exact source aliases.',
2:'The energetic departure call naturally covers its two exact aliases.',4:'The casual go-ahead is natural for the blunt voice.',
5:'The older formal departure suggestion is natural without invented archaic speech.'},
(309,810):{0:'The urgent warning naturally addresses the admiral and preserves the exact shared aliases.',
2:'The direct warning is idiomatic and keeps the alarm clear.',3:'The urgent watch-out warning preserves the concerned reaction.',
4:'The complete shout exactly matches the independent draft.',5:'The direct older-speaker warning exactly matches the independent draft.',
6:'The urgent admiral-addressed warning preserves the youthful alarm without needing a literal stammer.'},
(309,1006):{0:'The complete urgent welfare question is natural for every shared alias after the captain’s injury.',
2:'The clipped urgent question is idiomatic immediately after an injury.',5:'The older direct question naturally asks about the injury without adding an assessment.',
6:'The short informal welfare question preserves the youthful concern.'},
(309,1214):{0:'The complete danger shout naturally preserves all six shared source aliases.',
4:'The direct danger shout is idiomatic for the rough variant; an extra expletive is unnecessary.',
6:'The short danger shout naturally conveys the youthful warning.'},
(309,1278):{0:'The nonlexical pain cry exactly matches the independent draft across the five source aliases.',
3:'The drawn-out shrill cry exactly matches the independent draft and preserves pain.',
5:'The short nonlexical cry naturally preserves the older speaker’s yelp.'},
(309,1368):{2:'The clipped exclamation is natural for a wounded, breathless speaker and preserves pain.',
3:'The complete expressive pain reaction is natural and accurate.',4:'The blunt dismissive reassurance naturally minimizes the injury, as the source does.',
5:'The pained reassurance naturally says the speaker is still all right without denying the wound.',
6:'The cry and emphatic negative answer preserve the comic contrast with the preceding welfare question.'},
(309,2758):{6:'The youthful deduction naturally expresses the confident hope that the forest should end soon; it does not add a mapped distance or guarantee.'},
(309,2938):{0:'The complete sighting call naturally reports the destination becoming visible across all four exact source aliases.',
2:'The brief recognition is natural after the forest-exit expectation and does not invent the discovery’s name.',
3:'The direct pointing call naturally preserves the admiral address and new sighting.',
5:'The emphatic pointing call naturally suits the older speaker’s sighting.',
6:'The excited admiral-addressed pointing call preserves finding the destination without adding an identity.'},
}

STYLE_REASONS={
(302,24):'Preserve this variant’s complete map-gate reason and register without an added retreat or purchase instruction.',
(302,392):'Restore this heat observation in a measured or natural spoken voice rather than a flattened or awkward phrase.',
(302,596):'Restore the specific risk of losing the way and the variant’s degree of worry and decision question; difficulty or danger alone is not the whole warning.',
(302,1320):'Preserve the companion’s hesitant acceptance, personal register or explicit doubt after the storm decision instead of flattening every reply into confident agreement.',
(302,1786):'Preserve the forecast that the storm shows no sign of easing and the open decision question; do not invent elapsed hours or a prediction that it will never stop.',
(302,2582):'The Japanese estimates when they will leave the desert. It says nothing here about dwindling water. Restore that expectation and this variant’s voice.',
(302,2900):'Restore the admiral-directed sighting call and the source register without prematurely identifying the destination.',
(304,296):'Preserve the surprised obstacle observation and this companion’s conversational, older or formal decision question rather than the same clipped What now in every voice.',
(308,8):'Restore the far-northeast-of-China village, the map-guardian clan and this variant’s urgency, curiosity, reminder or qualified question. The source gloss’s provisional Meihua spelling is unrelated to this direction.',
(309,24):'Use natural English for the missing-map warning, retaining the reason, qualification or question rather than no map means lost or no map is bad.',
(309,422):'Preserve the specific frightened wolf alarm and register. Japanese does not supply a headcount; use the primary animal referent without claiming a pack or that only one animal exists.',
(309,1278):'Preserve the drawn-out startled pain cry rather than a possible stop-command or surprise-only Whoa.',
(309,1368):'Make the injured reply a natural statement that the speaker is managing; the isolated Somehow does not complete that thought in English.',
(309,1590):'Make the treatment reassurance natural and preserve prompt treatment, this variant’s qualifications and the wolf’s departure. Do not turn prompt into a small amount of treatment or claim observed healing or an animal headcount.',
(309,2364):'Represent breathless panting as vocal breaths rather than speaking Pant or Wheeze. Preserve each variant’s safety assertion or tentative question.',
(309,2758):'Use a natural prospective forest-exit estimate rather than the awkward possessive Woods’ end is near, retaining the source’s confidence or question.',
}

CHOICE_RETAIN={(302,1226,0):'The short caption exactly preserves continuing onward.',
    (302,1226,1):'The idiomatic wait-it-out caption naturally means waiting for this sandstorm to subside.',
    (302,2272,0):'After the renewed storm report, Keep going clearly means advancing into the sandstorm; no new branch is invented.',
    (302,2272,1):'The concise caption naturally preserves waiting longer at the second storm decision.',
    (304,576,0):'The preceding swamp question supplies the object; Enter is a complete, natural choice caption.',
    (304,576,1):'Retreat naturally preserves turning back from the swamp.',
    (309,738,2):'The concise Run caption naturally preserves fleeing the wolf encounter.'}

def main():
    assert not OUT.exists();draft,current,objects=map(load,(DRAFTS,CURRENT,OBJECTS))
    assert current['runtime']==objects['runtime'] and current['records']==73 and objects['native_style_getter_cases']==184
    bound={r['id']:r for g in current['groups'] for r in g['records']}
    bound.update({r['id']:r for r in objects['style_records']+objects['choice_records']})
    assert len(bound)==len(draft['records'])==234
    rows=[];glyphs=[];untranslated=[]
    for original in draft['records']:
        row=deepcopy(original);old=bound[row['id']]
        assert all(row[k]==old[k] for k in ['source_reference','source_hex','source_Japanese'])
        for key,value in old.items():
            if key.startswith('current_') or key=='selected_native_pointer':row[key]=deepcopy(value)
        prior=mark_macros(old['current_comparison_paragraph'],row);english=row['english']
        if row.get('kind')=='typed-choice-label':
            key=(row['block'],row['source_command_offset'],row['source_index'])
            reason=CHOICE_RETAIN.get(key)
            if reason:english=prior
            elif key==(309,738,0):reason='Drive alone can mean steering a vehicle; use Drive it off to express frightening the wolf away, distinct from combat.'
            elif key==(309,738,1):reason='The source choice is fighting, not the narrower and unnatural standalone Hit action.'
            else:raise AssertionError(key)
        elif row.get('kind')=='actor-style-alternative':
            key=(row['block'],row['source_command_offset']);i=row['source_style_indices'][0]
            reason=STYLE_RETAIN.get(key,{}).get(i)
            if reason:english=prior
            else:
                reason=STYLE_REASONS[key]+' '+row['source_meaning']
                if key==(308,8):reason=reason.replace(' The source gloss’s provisional Meihua spelling is unrelated to this direction.','')
        else:
            key=(row['block'],row['source_reference']['record_index']);reason=RETAIN.get(key[0],{}).get(key[1])
            if reason:english=prior
            else:reason=SPECIAL[key]
            if key==(303,16):english="Far inland from this town, there's a mosque dedicated to a king from long ago. They say it holds a wonderful treasure."
            if key==(309,178):english="Form up! We'll break through in one push!"
            if key in {(307,34),(307,42)}:
                assert any(ord(c)>127 for c in prior)
                untranslated.append(dict(id=row['id'],source_reference=row['source_reference'],current_reference=row['current_reference'],current_text=prior))
            if key==(307,55):
                assert prior=='…' and english=='...'
                glyphs.append(dict(id=row['id'],current_text=prior,target_text=english,kind='scoped-ASCII-silence-punctuation-consistency'))
        if english==prior and row.get('kind')=='actor-style-alternative' and not STYLE_RETAIN.get((row['block'],row['source_command_offset']),{}).get(row['source_style_indices'][0]):
            reason='The current wording already equals the independent clean-source draft and preserves this variant: '+row['source_meaning']
        english.encode('ascii');assert english.strip()==english and not any(t in english for t in ['{LB','{ALIGN','{PAD}','\n','%'])
        assert all(english.count('{MACRO:'+m+'}')==row.get('source_macros',{}).get(m,0) for m in ['FI','FA','FO'])
        decision='retention' if english==prior else 'revision';assert reason
        row.update(english=english,logical_English=english,decision=decision,finding=reason,
            retention_reason=reason if decision=='retention' else None,localization_note=reason,
            current_comparison_paragraph=old['current_comparison_paragraph'],
            independent_clean_draft_reference=dict(path=str(DRAFTS),id=row['id'],sha256=digest(DRAFTS)),
            current_English_conversation_comparison_pending=False,current_ROM_English_unconsulted=False,current_English_now_exposed=True,
            clean_first_draft_not_final_comparison_approval=False,source_only_not_final_English=False,
            source_current_complete_exchange_comparison_complete=True,new_credit=0)
        assert row['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
        rows.append(row)
    assert len(rows)==234 and len(untranslated)==2 and len(glyphs)==1
    counts=dict(Counter(r['decision'] for r in rows))
    save(OUT,{**draft,'records':rows,'counts':counts,'remaining_contextual_comparisons':0,
        'all_four_individual_prose_gates_pass':True,'all_formatting_gates_pending':True,
        'scoped_native_names_terms_anddisplay_still_pending':True,'current_English_comparisons':234,
        'current_binding':str(CURRENT),'current_binding_sha256':digest(CURRENT),
        'current_objects':str(OBJECTS),'current_objects_sha256':digest(OBJECTS),
        'current_ROM':current['current_ROM'],'current_ROM_sha256':current['current_ROM_sha256'],'native_runtime':current['runtime'],
        'untranslated_current_turns_corrected':untranslated,'findings_requiring_fresh_display_checks':glyphs,
        'native_substitutions_require_fresh_changed_body_checks':True,
        'wolf_headcount_unmarked_no_pack_oronly_one_claim':True,
        'no_new_font_artwork_orengine_changes':True,'prose_only_no_new_ROM_orregistered_credit':True,
        'full_goal_complete':False,'new_credit':0,
        'evidence':{str(p):digest(p) for p in [DRAFTS,MEANINGS,CURRENT,OBJECTS,ROOT/'role_bindings_v1.json',Path(__file__)]}})
    print('Saved234 complete contextual comparisons:',counts,'; scoped names/terms and display gates remain.')

if __name__=='__main__':main()
