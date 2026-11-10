"""Contextual decisions for 48 physical personality variants and 15 menu labels."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.author_editorial_prose_packet import normalize

CURRENT=Path('work/analysis/Hodram_B111_B130_current_objects_20261101/current_objects.json')
OUT=Path('translations/hodram_B111_B130_alternatives_prose_v1.json')
# One decision for each physical source string; aliased personality slots stay shared.
STYLES={
(113,10):[
(0,'Admiral, please look at this!','Restore the polite request and explicit object; source slots 0/1 intentionally share it.'),
(28,'Admiral, look at this!','Restore the explicit pointing in a lighter direct voice; preserve the 2/3 alias.'),
(48,'Admiral, take a look at this!','Keep the more casual emphatic request without inventing a discovery.'),
(74,'Admiral, have a look at this!','Give the gruff request natural English cadence without an invented accent or biography.'),
(100,'Admiral! Look at this!','Keep the youthful calling cadence and explicit object without spelling a babyish accent.'),
(126,'Admiral, do take a look at this!','Preserve the respectful older register through a natural invitation, not a new age statement.'),
],
(119,16):[
(0,"Admiral, it's a dead end.",'Restore a complete matter-of-fact sentence and source address.'),
(24,"Admiral, we've reached a dead end.",'Keep the measured report and address in a complete natural sentence.'),
(46,"Huh? It's a dead end.",'Restore the surprised light opening; no Admiral address occurs in this variant.'),
(70,"Admiral, it's a dead end.",'Restore the source address while preserving the straightforward observation; no artificial gender marker is needed.'),
(92,"Whoa, it's a dead end.",'Preserve the abrupt casual noticing reaction.'),
(116,"Admiral, it's a dead end, then.",'Restore the address and contemplative cadence without inventing an archaic dialect.'),
(142,"Admiral! It's a dead end!",'Keep the called address and youthful immediacy in natural English.'),
(170,'Well, this is a dead end.','Restore the mild surprised opening and composed observation without adding a new address.'),
],
(121,64):[
(0,"Hm? There's someone on the sandbar.",'Restore the location needed for the rescue; shared slots 0/1/2/4/7 have one physical source string.'),
(24,"Oh? There's someone on the sandbar.",'Restore the sandbar and questioning observation without an invented identity.'),
(46,"Hm? There's someone out on the sandbar.",'Restore the location and older cadence without asserting the observer is the grandfather.'),
(70,"Huh? Someone's there.",'Restore the youthful noticing reaction; this variant does not mention the sandbar.'),
],
(121,324):[
(0,None,'Retain the natural confident volunteering; the rescue context makes the task clear for all shared slots.'),
(18,None,'Retain the natural eager elliptical offer to perform the rescue; it is not a request for release.'),
(28,"I'll go!",'Restore the actual volunteering assertion rather than the ambiguous Let me go.'),
(42,"I've got this!",'Localize the rough confident offer idiomatically without inventing a skill claim beyond taking charge.'),
(54,None,'Retain the firm natural offer; no age caricature is needed to preserve the source confidence.'),
(76,"I'll go!",'Restore the youthful volunteer\'s assertion; no new rescuer identity is assigned.'),
],
(122,16):[
(0,'Admiral, look at this!','Restore the explicit pointing toward the jade for the shared physical variant.'),
(16,'Admiral, look!','Restore the request to look while preserving the lighter short address.'),
(30,'Admiral, this!','Restore the source address and excited unfinished pointing; the following line identifies the jade.'),
],
(123,16):[
(0,None,'Retain the complete natural polite call to examine this object, shared by source slots 0/1/7.'),
(28,'Admiral, look at this!','Restore the explicit object in the lighter imperative.'),
(48,'Admiral, take a look at this!','Keep the casual emphatic pointing without flattening it into an address alone.'),
(74,'Admiral, look at this!','Preserve the direct gruff instruction to inspect this object; here is not a new destination.'),
(100,'Admiral, look at this!','Restore the youthful speaker\'s source address rather than the unspecific Hey.'),
],
(125,54):[
(0,"Something about this statue's design seems out of place in this building.",'Restore the tentative assessment of the design; statue comes from the immediately preceding exchange.'),
(46,"Somehow, the design doesn't seem to suit this building.",'Restore the complete measured observation and visual uncertainty.'),
(92,"Doesn't it seem a bit out of place in this building?",'Preserve the light shared-observation cadence and explicit building comparison.'),
(132,"Somehow, it just doesn't go with this building.",'Express ミスマッチ in natural conversational English and retain the slight uncertainty.'),
(170,None,'Retain the natural rough rhetorical question and explicit building comparison.'),
(214,"Somehow, it doesn't seem to belong in this building.",'Keep the older speaker\'s tentative impression in natural prose rather than stiff unsuited phrasing.'),
(268,"It doesn't really go with this building, does it?",'Restore the building comparison and youthful musing without inventing a proposed renovation.'),
(300,"Doesn't its design seem out of place in this building?",'Retain the composed question and explicit design/building relationship.'),
],
(125,450):[
(0,'It has the shape of a figurehead... Could it originally have been one?','Restore the complete shape observation and explicit original-purpose question.'),
(52,'It looks like a figurehead... Wait, could it have been one to begin with?','Preserve the self-correction and tentative original-purpose inference.'),
(106,"Doesn't this look like a figurehead? I mean, could it actually be one?",'Restore both questions; remove the unsupported affirmative Yes in the older English.'),
(182,'It looks sort of like a figurehead... Oh, could that be what it was?','Preserve the conversational hesitation and wondering realization, not a firm identification.'),
(238,None,'Retain the natural rough tentative observation and question; it does not certify the object\'s origin.'),
(304,'It has the shape of a figurehead. No, that is what it was to begin with.','Preserve this older variant\'s affirmative correction and original-purpose conclusion, unlike the other hedged variants.'),
(366,'You could use this as a figurehead. See?','Restore the distinct potential-use statement; it does not assert that the statue used to be a figurehead.'),
(394,'It has the shape of a figurehead... Perhaps that was its original purpose?','Preserve the composed observation and genuine question about original function.'),
],
}
CHOICES={
(114,154):[
(0,'I know.','Restore a complete answer claiming knowledge; preserve option index 0.'),
(1,"I don't know.",'Restore a clear natural admission of not knowing; preserve option index 1.'),
(2,"There's no such animal.",'Preserve denial of the animal\'s existence using the same animal term as the riddle.'),
],
(114,392):[
(0,None,'Retain the clear natural human-species answer; the source parenthesis identifies ourselves as humans.'),
(1,'You, the Sphinx.','Restore the natural definite article and direct identification of the questioner.'),
(2,'Something else.','Use a natural residual answer distinct from humans and the Sphinx; no species is invented.'),
],
(114,782):[
(0,None,'Retain the exact numeral 3; the immediately preceding question supplies babies as the counted people.'),
(1,None,'Retain the exact correct numeral 4 with source option order intact.'),
(2,None,'Retain the exact numeral 5 in its separate incorrect branch.'),
],
(118,372):[
(0,'1 second','Spell out the time unit naturally; the numerical wrong answer and index remain unchanged.'),
(1,'30 seconds','Spell out the time unit without shortening for an untested allocation.'),
(2,'59 seconds','Keep the exact correct answer and explicit plural unit; preserve the third option.'),
],
(119,336):[
(0,None,'Retain the concise natural action Push; the urn mechanism provides the object.'),
(1,'Turn right','Restore the action rather than a bare direction; do not confuse rightward turning with the left-hand clue.'),
(2,'Turn left','Restore the turning action and preserve this separate wrong-direction choice.'),
],
}

def main():
    assert not OUT.exists()
    current=load(CURRENT)
    speeches=[load(Path('translations')/name) for name in ['hodram_B111_B119_editorial_prose_v1.json','hodram_B120_B130_editorial_prose_v1.json']]
    contexts={k:v for p in speeches for k,v in p['complete_exchange_contexts'].items()}
    styles={(b,o,n):(text,note) for (b,o),decisions in STYLES.items() for n,text,note in decisions}
    choices={(b,o,n):(text,note) for (b,o),decisions in CHOICES.items() for n,text,note in decisions}
    rows=[]
    for kind,decisions in [('style_records',styles),('choice_records',choices)]:
        for original in current[kind]:
            row=deepcopy(original)
            physical=int(original['id'].rsplit('_',1)[1]) if kind=='style_records' else original['source_index']
            key=(original['block'],original['source_command_offset'],physical)
            proposed,note=decisions.pop(key)
            prior=normalize(original['current_comparison_paragraph'])
            english=prior if proposed is None else proposed
            assert english.strip()==english and '\n' not in english and '  ' not in english and english.isascii()
            assert not any(t in english for t in ['{LB','{PAD','{ALIGN'])
            retained=english==prior
            row.update(english=english,logical_English=english,source_meaning=original['source_meaning_gloss'],
                speaker='Personality-selected companion (native 4100)' if kind=='style_records' else 'Player menu choice (native 2200)',
                context=f"B{original['block']}: "+contexts[str(original['block'])],
                context_reference=f"#/complete_exchange_contexts/{original['block']}",
                prior_macro_normalized_comparison=prior,prior_effective_paragraph_preserved=original['current_comparison_paragraph'],
                localization_note=note,finding=note,decision='retention' if retained else 'revision',retention_reason=note if retained else None,
                review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
                whole_clean_exchange_andcadence_emotional_progression_reviewed=True,
                no_authored_linebreak_alignment_padding_orallocation_driven_shortening=True,
                all_five_review_gates_pending=False,native_style_dispatch_andall_five_review_gates_pending=False,
                localization_andfive_gate_approval_pending=False,formatting_names_glyph_stored_actual_andregistered_release_pending=True)
            rows.append(row)
        assert not decisions
    assert len(rows)==63 and len({r['id'] for r in rows})==63
    save(OUT,dict(format='dk4-editorial-prose-packet-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        review_gates=['source','context','localization','naturalness','formatting'],
        current_ROM=current['current_ROM'],current_ROM_sha256=current['current_ROM_sha256'],
        current_archive_sha256=current['current_archive_sha256'],file_path='/data/SC1.DK4',
        complete_exchange_contexts=contexts,records=rows,total_editorial_objects=63,
        personality_alternatives=48,personality_alias_slots=64,typed_choice_labels=15,
        native_alias_groups_preserved=True,menu_source_index_order_preserved=True,
        revised=sum(r['decision']=='revision' for r in rows),retained=sum(r['decision']=='retention' for r in rows),
        current_packet=str(CURRENT),current_packet_sha256=sha(CURRENT.read_bytes()),
        ordinary_wrapping_owned_by_formatter=True,all_four_individual_prose_gates_passed=True,
        all_formatting_gates_false=True,new_credit=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [CURRENT,Path(__file__)]}))
    print(OUT,63,'decisions',sum(r['decision']=='revision' for r in rows),'revisions',sum(r['decision']=='retention' for r in rows),'retentions; formatting pending.')

if __name__=='__main__':main()
