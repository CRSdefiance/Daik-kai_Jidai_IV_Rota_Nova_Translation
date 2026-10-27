"""Fresh49-line opening review, justified retentions and exact inherited display scope."""
from copy import deepcopy
import os
from pathlib import Path
from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_opening_contextual_retention_v1976')
OLD = Path('translations/lil_opening_final_review_v1.json')
OUT = Path('translations/lil_opening_contextual_retention_review_v1.json')
LEDGER = Path('translations/editorial_review_current_v1.json')
HANDOFF = Path('docs/editorial_handoff_current.md')
ROM = Path('out/all_routes_combined_v1971_candidate.nds')
REASONS = {
19: 'Lil\'s gleeful opening keeps finally obtaining the trade permit, her challenge to the world and her boast of making a fortune. Hee hee and just you watch express the playful confidence in natural English.',
23: 'Camille\'s repeated calls preserve his urgency and the FI substitution. Wait for me is the natural contextual force of the second wait as he runs after Lil, without inventing a separate task.',
26: 'Lil hurries Camille, demands the ship be readied and insists on immediate departure. Come on and hurry up keep her impatient authority and use approved Camille.',
30: 'Phew represents his panting breath before the reluctant question. Do we really have to leave today? preserves his wish that immediate departure is unnecessary without asserting a ban or a different date.',
33: 'Camille explains that the unexpectedly quick permit issuance left preparations unfinished. Two conversational sentences and the trailing ellipsis preserve the explanation and his interrupted/hesitant voice.',
36: 'Lil cuts off his grumbling and redirects the conversation. Quit grumbling. Anyway... is brisk and idiomatic; the ellipsis keeps the source lead-in to her captain proposal.',
40: 'The permit being in Lil\'s name is her stated reason to claim captaincy. Right? retains her question and self-serving logic, with no invented legal rule or naval commission.',
44: 'Camille\'s surprise and uncertainty remain in the two hesitant beats. Huh? Oh... really? sounds natural after her abrupt claim rather than supplying confident consent.',
48: 'All hands to your stations is the idiomatic nautical order for everyone to take position. We\'re setting sail preserves her immediate intent already established in the preceding exchange.',
51: 'Lil addresses the people handling sails, orders full sail, then raises the anchor. Sail crew is an ordinary collective address, with no invented officer rank; weigh anchor preserves the action and order.',
54: 'Camille privately doubts how Lil of all people obtained the permit so easily. The leading ellipsis and of all people retain the skeptical, slightly insulting humor and the runtime name.',
58: 'Lil credits her enthusiasm reaching the officials, then playfully offers her dazzling beauty as the alternative. Won them over and dazzled by my beauty localize the joke naturally without asserting bribery or romance.',
61: 'Yeah, yeah conveys Camille\'s indulgent dismissal before he asks what she intends to do with the permit. His question stays practical, without losing the transition from her vanity joke.',
65: 'Lil answers that the permit enables contracts with any city and makes the whole world their customers. The whole world\'s our market conveys that trading metaphor and her expansive ambition.',
69: 'Camille echoes her whole-world ambition skeptically and proposes continuing their established trade near Amsterdam. Like we always have and what\'s wrong with that retain both continuity and his question.',
72: 'Lil complains that their current trading earns little and presents overseas riches as possible. Barely make anything and could make a fortune preserve her hyperbolic optimism without guaranteeing wealth.',
76: 'Camille doubts how easy sudden riches will be. I don\'t know and I doubt keep the cautious response to Lil\'s enthusiasm, rather than stating failure as a fact.',
79: 'Fernando teases Camille for resisting the inevitable departure. You just don\'t know when to give up is the natural force of 往生際が悪い in this exchange; it does not invent a prior defeat.',
83: 'Camille is surprised Fernando is joining after emphatically refusing to sail with them. The two questions and I thought you said preserve recognition, the reversal and the teasing accusation.',
87: 'Fernando evasively admits things changed and urges departure. Well... things happen is natural deliberate vagueness; no motive, payment or relationship is invented.',
90: 'Emilio complains that he is still waiting for promised good food. His direct food question and tired of waiting preserve his appetite and impatience before Fernando explains the inducement.',
94: 'Camille\'s brief surprise that even Emilio is present needs no extra explanation. Emilio too? carries the source recognition and continuing crew-reveal joke.',
98: 'Fernando says Emilio\'s strength might be useful and that food attracted him. Figured he\'d come in handy preserves his expectation; lured him aboard with food delivers the source joke in the actual sailing context.',
102: 'Camille reacts uneasily to the assembled crew and questions whether sailing with them will be all right. Quite a crew... keeps the ironic assessment without adding an insult or a specific danger.',
105: 'Lil shuts down the discussion, urges departure and playfully puts Camille to work. Come on, Camille softens the brisk get to work in her established teasing, bossy voice; no personal relationship is added.',
109: 'Fernando confirms both full sails and raised anchor, then asks for orders. The complete nautical report and plural orders express the same practical readiness without inventing a battle command.',
112: 'Camille reluctantly takes charge of departure preparations for the Arnhem and sends everyone to their stations. Oh, all right preserves the reluctant concession; the ship name and all-hands order remain explicit.',
116: 'Lil admires his newly commanding manner and says she relies on him. Now that\'s more like it is encouraging praise in immediate response to his confident orders; I\'m counting on you keeps the explicit trust without inventing a rank or romance.',
119: 'The written Sigh... represents the source audible sigh in game dialogue, followed by a natural expression of apprehension about what lies ahead. The line keeps a worried future perspective without predicting a particular disaster.',
123: 'Fernando laughs at the contrast between Camille\'s complaints and his readily coming along. Without much of a fight is an idiomatic expression of that easy acquiescence, with no physical fight implied.',
126: 'Camille explains his prior promise to join if Lil obtained the permit. I did promise keeps his defensive tone and the permit condition; it does not invent an unconditional pledge.',
129: 'Fernando explains that the Netherlands is newly formed and favors merchants to strengthen the country. The source political background is retained as game dialogue, without adding dates or extra history.',
133: 'The easy availability of permits provides the punch line to Lil\'s earlier enthusiasm/beauty theory and Camille\'s mistaken assumption. Anyone and without much trouble retain the source generality.',
136: 'Camille realizes how the permit system works, with a stammer and trailing hesitation. S-so that\'s how it works... preserves the embarrassed discovery rather than making him confidently lecture.',
140: 'Fernando adds that the permit apparently exempts trading-post profits from tax. Apparently preserves hearsay; the specific profits and place remain, without expanding this to every kind of tax.',
144: 'Camille\'s startled follow-up stays a natural two-beat exclamation/question. It responds to the tax privilege and adds no new mechanic.',
148: 'Fernando connects the exemption with trade-encouragement policy and concludes that the document also acts as a tax-exemption permit. The causal explanation and too remain explicit.',
152: 'Camille now understands why Lil wanted the permit. No wonder is the idiomatic realization after the tax explanation, and FI remains a runtime substitution.',
156: 'Fernando returns from explaining policy to teasing Camille\'s habitual inability to resist Lil. You might as well give up and always been like this preserve resignation and long familiarity without claiming childhood kinship.',
159: 'Camille\'s short puzzled Huh? naturally prompts Fernando\'s next explanation. No additional emotion or fact is inserted.',
163: 'Fernando jokes about Camille being fated to remain unable to stand up to Lil. Let her boss you around conveys the specific power dynamic involving her, with destined retaining the mock-fatalistic humor; it does not label them partners or relatives.',
166: 'Camille\'s stammered denial and trailing hesitation retain the weak protest to Fernando\'s teasing. N-no... keeps the comic contrast with Fernando\'s certainty.',
170: 'Camille abruptly notices Lil is missing. Wait, where\'s FI? is a natural change of subject and preserves the name substitution without inventing why she left.',
175: 'Lil privately reflects on her hometown, vaguely alludes to past events and trails off. The three ellipsis beats carry the emotional change; no tragedy, abuse or specific backstory is invented. The source leading physical blank is staging, not a necessary English empty row.',
179: 'Camille calls Lil and asks what is wrong. Both the FI substitution and concern remain, with no claim that he knows what she is thinking.',
182: 'Lil recognizes Camille, apologizes twice and dismisses her distraction. Sorry, sorry and it\'s nothing preserve her quick return from introspection to the conversation.',
186: 'Camille is tentative about accepting her reassurance, then reports readiness. Really? Well... all right, then keeps his mild concern before the practical departure update.',
190: 'Fernando impatiently requests the sailing order. Come on and give us the order fit the already-prepared ship and remain distinct from a new course or combat instruction.',
195: 'Lil deliberately resumes command, names the Arnhem and orders departure for the neighboring port of Bruges. All destination and ship facts remain explicit; set sail is the ordinary English order and the initial ellipsis keeps her regained composure.',
}

if __name__ == '__main__':
    assert not ROOT.exists() and not OUT.exists()
    old = read(OLD)
    image, previous, clean = map(NdsImage.open,(ROM,old['candidate'],'work/clean.nds'))
    digest = sha(ROM.read_bytes())
    assert digest == 'c4c998e446b7ac410d2294563fc4e5d5181cef6938c25254b1bd3679492efa20'
    arm = image.read_file('/__arm9__.bin')
    assert arm == previous.read_file('/__arm9__.bin')
    assert image.read_file('/COMMON/MESFILE.DK4') == previous.read_file('/COMMON/MESFILE.DK4')
    now = IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[22]
    jp = IlnkContainer.parse(clean.read_file('/data/SC2.DK4')).blocks[22]
    assert now == IlnkContainer.parse(previous.read_file('/data/SC2.DK4')).blocks[22]
    for path,expected in old['proofs'].items(): assert sha(Path(path).read_bytes()) == expected,path
    map_path = Path(old['records'][0]['reference_map'])
    mapping = read(map_path)
    assert sha(now) == mapping['target_block_sha256'] and sha(arm) == mapping['required_runtime_ARM9_sha256']
    assert mapping['external_references_complete'] and not mapping['unclassified_function_pointer_literals_to_interpreter']
    profile = get_dialogue_profile('lil-opening-editorial-native-v1')
    rows, waivers = [], []
    assert len(old['records']) == len(REASONS) == 49
    for row in old['records']:
        source, current = bytes.fromhex(row['source_hex']), bytes.fromhex(row['current_text_hex'])
        ja, at = row['source_reference']['offset'], row['current_reference']['offset']
        assert jp[ja:ja+len(source)] == source and jp[ja+len(source)] == 0
        assert now[at:at+len(current)] == current and now[at+len(current)] == 0
        preamble = b'\0\x40\xff\xff\0'+source[:1]
        assert jp[ja-5:ja+1] == now[at-5:at+1] == preamble
        compiled = encode_relocatable_dialogue(source,row['english'],profile)
        assert compiled.encoded.hex() == row['compiled_hex'] and current in (compiled.encoded,compiled.encoded+b' ')
        assert all(d.severity == 'warning' and d.code == 'line-break-count' for d in compiled.diagnostics)
        if compiled.diagnostics: waivers.append(row['id'])
        assert all(source.count(k.encode('ascii')) == row['english'].count('{MACRO:'+k+'}') for k in ('FI','FA','FO'))
        rows.append(dict(id=row['id'],file_path='/data/SC2.DK4',block=22,speaker=row['speaker'],
            source_reference=deepcopy(row['source_reference']),source_hex=source.hex(),clean_Japanese=source[1:].decode('cp932'),
            current_reference=deepcopy(row['current_reference']),current_text_hex=current.hex(),current_stored_English=current[1:].decode('cp932'),
            complete_preamble_hex=preamble.hex(),english=row['english'],source_meaning=row['source_meaning'],
            editorial_decision='retain-wording',retained_wording_justification=REASONS[row['record_index']],
            context='Entire49-speech opening reread together:permit triumph,reluctant preparations,Lil\'s captain claim andvanity,Camille\'s skepticism,crew reveals,his reluctant command,Fernando\'s permit-policy explanation andteasing,Lil\'s private hometown reflection,concern anddeparture forBruges. Bossy/playful Lil,cautious Camille,roughly teasing Fernando andfood-focused Emilio keepdistinct voices. No romance,kinship,naval commission orspecified childhood trauma is invented.',
            fresh_review=dict(source=True,context=True,localization=True,naturalness=True,formatting=True),
            formatting_basis='Exact B22,ARM9 andCOMMON inheritance fromV1711 binds theexisting49 native planes,98 full actual holds,90 original commands,three crew joins andnormal Amsterdam return. Formatter reproduces each stored target. Onlyphysical source-line counts may differ;English ellipses preserve the actual pauses. No newgameplay orlatertechnical re-audit claimed.',
            diagnostics=[dict(code=d.code,severity=d.severity,message=d.message) for d in compiled.diagnostics],
            physical_line_count_warning_justified=bool(compiled.diagnostics),inherited_actual_holds=deepcopy(row['actual_holds']),new_gameplay_visit_claimed=False))
    assert len(waivers) == 15
    raw = LEDGER.read_bytes()
    ledger, before = read(LEDGER), read(LEDGER)
    fresh = ledger['contextual_story_natural_dialogue_pass_v1871']
    ids = [r['id'] for r in rows]
    assert not set(ids) & set(fresh['record_IDs'])
    assert fresh['fresh_pass_records_explicitly_reread'] == fresh['fresh_pass_records_integrated'] == 315
    assert fresh['historical_completed_records_outside_reconciled_fresh_pass'] == 1516
    family = next(f for f in ledger['completed_editorial_families'] if f['id'] == 'Lil-Amsterdam-opening49')
    assert set(family['record_IDs']) == set(ids)
    ROOT.mkdir(parents=True)
    (ROOT/'ledger_before.json').write_bytes(raw)
    (ROOT/'handoff_before.md').write_bytes(HANDOFF.read_bytes())
    save(OUT,dict(format='dk4-contextual-retention-reconciliation-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        family='Lil-Amsterdam-opening49',record_IDs=ids,records=rows,revised_count=0,retained_count=49,
        source_clean_ROM='work/clean.nds',source_clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),
        clean_B22_sha256=sha(jp),current_B22_sha256=sha(now),ARM9_sha256=sha(arm),current_candidate=str(ROM),current_candidate_sha256=digest,
        original_review=str(OLD),original_review_sha256=sha(OLD.read_bytes()),original_gameplay_scope=old['actual_verification_scope'],
        inherited_native_and_actual_evidence_bound_to_unchanged_bytes=True,narrow_physical_line_count_warning_IDs=waivers,
        no_new_ROM_patch_or_gameplay_required_for_unchanged_text=True,no_historical_completion_count_added=True,
        older_record_technical_reaudit_remains_deferred=True,evidence={str(OLD):sha(OLD.read_bytes()),**old['proofs']},
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    fresh['record_IDs'] += ids
    fresh.update(fresh_pass_records_explicitly_reread=364,fresh_pass_records_integrated=364,
        historical_completed_records_outside_reconciled_fresh_pass=1467,latest_final_review=str(OUT),latest_contextual_retention_review=str(OUT),
        latest_reconciled_historical_family='Lil-Amsterdam-opening49',
        coverage_note='Stockholm51,London111,Speyer59,Hamburg81,trade-route/officer13 andearlieropening49 explicitly reread andintegrated/reconciled. Earlier B24/B22 have62individual justified retentions andexact source/current/native evidence. Historical totals unchanged;other1467historical completions needreconciliation.')
    fresh['reconciled_families'].append(dict(id='Lil-Amsterdam-opening49',records=49,final_review=str(OUT),
        historical_reconciliation_only=True,new_revisions=0,justified_retentions=49))
    family['contextual_v1871_reconciliation'] = dict(review=str(OUT),review_sha256=sha(OUT.read_bytes()),
        all49_wordings_retained=True,entire_clean_Japanese_exchange_explicitly_reread=True,current_candidate=str(ROM))
    ledger['coverage_units'].append(dict(id='Lil-Amsterdam-opening49-contextual-v1976',file_path='/data/SC2.DK4',block=22,record_IDs=ids,
        status='fresh-contextual-reconciliation-complete-unchanged-native-target',final_review=str(OUT),historical_entries_reconciled=49,
        source_prose_reviews_added=0,completed_entries_added=0,new_ROM_changes=0,
        actual_coverage='Inherited49speeches98holds,90commands,threejoins andnormal Amsterdamreturn;no newgameplay visits. ExactB22/runtime/COMMON checked.',full_goal_complete=False))
    summary = ('V1976 fresh Lilopening49 contextual reconciliation:entire clean-Japanese exchange reread;49individual justified retentions,no ROM change ornew historical count. '
        'Permit/crew humor,distinct voices,trade-policy hearsay,Fernando\'s teasing andLil\'s introspective turn remainfaithful andnatural. '
        'Fresh pass364 explicitly reread andintegrated/reconciled;1467 historical completions still needreconciliation. Historical1831(1362revised469retained),source/prose1947,116incomplete COMMON andall remaining prose stayopen. '
        'RegisteredV1971 andexact clean-input patch unchanged. Existing49native planes98actual holds90commands/threejoins inheritonly through exactB22/ARM9/COMMON checks. '
        'Fifteen physical-line-count warnings areexplicitly justified;ellipses retain dramatic pauses,no empty leading row. No newgameplay claim;laterolder-record technical re-audit andgraphics/all18plaques stayseparate;fullgoalactive.')
    ledger['latest_checkpoint'] = summary
    ledger['research_checkpoints'].append(dict(id='V1976-opening49-fresh-contextual-retentions',proof=str(ROOT/'reconciliation_receipt.json'),
        completed_entries_added=0,source_prose_reviews_added=0,historical_entries_reconciled=49,full_goal_complete=False))
    for key in ('records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed',
        'records_with_source_and_prose_pass','completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file',
        'current_integrated_candidate','unresolved_graphics_work','reviewed_but_incomplete_COMMON_IDs','older_record_reaudit_after_full_editorial_goal'):
        assert ledger[key] == before[key],key
    assert len(set(fresh['record_IDs'])) == len(fresh['record_IDs']) == 364
    assert ledger['records_editorially_completed']-fresh['fresh_pass_records_integrated'] == 1467
    assert ledger['goal_status'] == 'active' and not ledger['full_goal_complete']
    pending = LEDGER.with_name('editorial_review_current_v1976_pending.json')
    assert not pending.exists() and LEDGER.read_bytes() == raw
    save(pending,ledger)
    os.replace(pending,LEDGER)
    text = HANDOFF.read_text(encoding='utf-8').replace('# Current editorial handoff - V1975','# Current editorial handoff - V1976',1)
    text = text.replace('Fresh V1871 contextual pass:315 explicitly reread andintegrated/reconciled(Stockholm51 +London111 +Speyer59 +Hamburg81 +trade-route/officer13 retained). Prior1516 completions require explicit reconciliation.',
        'Fresh V1871 contextual pass:364 explicitly reread andintegrated/reconciled(Stockholm51 +London111 +Speyer59 +Hamburg81 +trade-route/officer13 +opening49 retained). Prior1467 completions require explicit reconciliation.')
    text = text.replace('116 COMMON entries remain incomplete;1516 historical completions needexplicit reconciliation.',
        '116 COMMON entries remain incomplete;1467 historical completions needexplicit reconciliation.')
    anchor = '## Earlier B24 fresh contextual retention pass - V1975'
    assert text.count(anchor) == 1
    chapter = ('## Earlier B22 opening fresh contextual retention pass - V1976\n\n'+summary+'\n\n'
        f'- Review:{OUT.as_posix()};receipt:{ROOT.as_posix()}/reconciliation_receipt.json. All49 records include exactsource/current refs,cleanJapanese,currentEnglish andspecific retention reasons. Original review andROMs preserved.\n'
        '- Inherited actual scope is49speeches/98holds,90commands,three original crewjoins andnormal Amsterdamreturn. Firstfollowing source isB120 at12,not assumedB23. CurrentB22/ARM9/COMMON matchV1711 exactly;no newwholeROM equality ornewgameplay claim.\n'
        '- Next useful earlier conversation iscomplete sailing/crew lessons B120/B23;then continue remaining Lil/shared town/random/player prose andother routes. Do not automatically credit earlier reviews without explicitly reading theJapanese exchange. Fullgoalactive.\n\n')
    HANDOFF.write_text(text.replace(anchor,chapter+anchor),encoding='utf-8')
    for name in ('translation_progress.md','todo.md','editorial_review_goal.md'):
        with (Path('docs')/name).open('a',encoding='utf-8') as stream:
            stream.write('\n\n## V1976 opening49 fresh contextual retentions\n\n'+summary+'\n\nReview: translations/lil_opening_contextual_retention_review_v1.json.\n')
    save(ROOT/'reconciliation_receipt.json',dict(review=str(OUT),review_sha256=sha(OUT.read_bytes()),current_B22_sha256=sha(now),
        clean_B22_sha256=sha(jp),ARM9_sha256=sha(arm),current_candidate=str(ROM),candidate_sha256=digest,
        explicit_fresh_reread_added=49,justified_retentions=49,new_revisions=0,new_historical_completions=0,
        fresh_contextual_reread_integrated_after=364,historical_outside_reconciled_fresh_pass=1467,
        historical_completed_unchanged=1831,source_prose_reviewed_unchanged=1947,no_new_gameplay_claim=True,
        ledger_sha256=sha(LEDGER.read_bytes()),handoff_sha256=sha(HANDOFF.read_bytes()),
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    assert sha(ROM.read_bytes()) == digest
    print(dict(fresh_reread_retained=49,fresh_total=364,historical_outside_fresh=1467,historical_total_unchanged=1831,ROM_unchanged=True))
