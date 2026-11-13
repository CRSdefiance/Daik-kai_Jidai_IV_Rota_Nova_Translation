"""Fresh complete lesson review: one affiliation correction,63 justified retentions."""
from copy import deepcopy
import os
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inventory_lil_lessons_v1717 import inventory
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_lessons_contextual_v1977')
OLD = Path('translations/lil_lessons_final_review_v1.json')
DOC = Path('translations/lil_lessons_editorial_manuscript_v6.json')
MENU = Path('translations/lil_lesson_choices_editorial_draft_v3.json')
LEDGER = Path('translations/editorial_review_current_v1.json')
HANDOFF = Path('docs/editorial_handoff_current.md')
ROM = Path('out/all_routes_combined_v1971_candidate.nds')
COMMON_SCOPE = Path('work/analysis/lil_opening_contextual_retention_v1976b/COMMON_delta_scope.json')
CHANGED = 'DK4_MES_B23_R0142'
REASONS120 = {
5:'Lil enjoys finally being at sea,the sea breeze andgulls,then impatiently asks Camille toissue orders. The three conversational beats retain her enthusiasm andbossiness.',
9:'Camille delays those orders toteach Lil too. Before that andtoo retain the interruption andher own need tolearn;FI remains dynamic.',
12:'Lil declines because she isbad at sailing. No thanks andI\'m no good at that keep her evasive,casual voice without inventing fear.',
15:'Camille insists she learn despite her difficulty because the future isuncertain andemergencies may arise. The practical explanation remains explicit without predicting a disaster.',
19:'Lil reluctantly gives in with an annoyed interjection anddrawn-out acceptance. Ugh... All right! keeps that response ratherthan eagerness.',
23:'Camille begins the lesson bychecking ship direction. Ship\'s heading isidiomatic nautical English forwhich way itfaces,not aninvented destination.',
27:'Lil musttell everyone thefleet\'s course. You\'re theone retains her responsibility andthe FI address without assigning a new formal rank.',
31:'Camille explains thebasic relationship between ship orientation andmovement. Point itinthat direction isclear conversational instruction with the same condition.',
36:'The system panel names both D-pad andstylus steering. Steer naturally expresses selecting direction;no control option isomitted.',
39:'The system explicitly says press toward thedesired direction or tap thatdirection. The two alternatives remain clear andequivalent.',
42:'Camille checks whether Lil thinks she canmanage. The short encouraging question flows into both original choice labels.',
62:'This conditional copy keeps Camille\'s private worry,Bruges southwest ofAmsterdam andhis encouragement. Itdoes not claim Lil hasalready succeeded.',
80:'The repeated conditional copy hasthesame private worry,direction andencouragement. Retain theidentical wording because thesource isidentical,without inventing a distinct reaction.',
109:'The repeated conditional copy isidentical inJapanese. Keeping thesame worry,Bruges direction andgood-luck wish preserves thescript\'s branch equivalence.',
134:'Camille praises successful practice andaddresses Lil asAdmiral,as thesource does. Nice work andI\'m counting onyou retain encouragement without a new naval commission.',
137:'Lil stammers andasks nottobe distracted while reasoning about wind andsails. The ellipses andself-directed explanation keep her concentration anduncertainty.',
142:'Lil understands steering butwants tocatch thewind andmove muchfaster. Pick upspeed isthenatural energetic expression ofher wish,not a new speed guarantee.',
146:'Camille explains thatproper wind capture requires adjusting the sails andgiving their direction. Both theprerequisite andthe next action remain explicit.',
150:'Lil stammers about theeffort involved. Wh-what a hassle keeps her reluctant comic voice without escalating thecomplaint.',
155:'The panel maps sail angle toL/R andtells theplayer adjustment increases speed. Buttons andeffect remain complete.',
159:'The panel explicitly maps L toleft andR toright. Both directions andcontrols remain distinct.',
163:'Stylus useautomatically optimizes sail angle; tapping theflagship stops. The automatic behavior andstop target remain,without inventing another button.',
167:'Camille explains watching wind relative tothe ship\'s heading andreceiving itbehind the sails. The English keeps that spatial reference anddoes not replace itwith anunrelated compass direction.',
171:'Lil expresses uncertainty ratherthan total refusal. Huh? I\'m notsure Iget it... matches her confused reaction.',
174:'Camille reassures her thatpractice willhelp andurges morepractice. The hopeful reassurance remains conditional ongetting used toit.',
177:'The panel identifies theonscreen speedometer andmaximizing itsbar byadjusting sails. The display andspecific practical instruction remain complete.',
186:'The final repeated line keeps theoriginal private concern,Bruges southwest ofAmsterdam andgood-luck wish. Identical conditional content remains identical.',
}
REASONS23 = {
5:'Camille starts thenext topic with anunfinished lead-in. Next up... keeps thetransition into Lil\'s complaint.',
9:'Lil thought thelesson wasfinished. Her surprised question keeps thecomic resistance toanother topic.',
13:'Camille distinguishes thecompleted ship-handling lesson fromupcoming crew assignments. Both topics andtheir sequence remain explicit.',
30:'This branch accepts Lil\'s claim ofknowledge andasks whether hecanleave assignments toher. Right? preserves thetentative challenge ratherthan declaring mastery.',
40:'Lil complains thatlearning assignments isbothersome. Ugh... What apain retains her reluctant voice without a new factual claim.',
44:'Camille says anadmiral hasmany duties andteasingly offers toreplace Lil. Put meincharge carries theproposal without adding aninstitutional naval rank transfer.',
47:'Lil emphatically refuses relinquishing command. No way keeps thebrief,firm reaction.',
51:'Camille draws theconsequence thatshe mustpay attention andlearn. The English preserves instruction ratherthan a punishment.',
54:'Lil gives a reluctant,drawn-out yes. Okaaay isthenatural written effect ofthat delivery.',
58:'Camille introduces posts,their roles andassigning each officer tokeep voyages smooth. Officer refers tothe named party members,not aninvented naval commission.',
62:'Lil iscaptain andshould stay inthe captain\'s cabin except emergencies because a ship needs itscaptain. All source conditions andFI remain.',
65:'Sail Handlers adjust sails tothe wind,an important task requiring oneperson permast. The plural role andper-mast requirement areboth retained.',
69:'At Half Open,the Sail Handlers automatically adjust thesails. The quoted setting andautomatic behavior remain precise.',
72:'Lil realizes Half Open avoids issuing sail-angle orders andcomplains thatCamille didnot sayso earlier. Her delighted shortcut-seeking voice remains.',
76:'Camille warns Full Open issometimes necessary andtells her topractice now toavoid laterpanic. The situational need isnot changed toalways using thatsetting.',
79:'Lil\'s brief thoughtful acknowledgment remains noncommittal. Hmm... preserves thatbeat afterthewarning.',
91:'This conditional panel exactly repeats L/R sail adjustment andspeed guidance. Retain thesame English;its FE consumer remains separate fromprogressive dialogue.',
95:'This conditional panel repeats automatic stylus sail adjustment andtapping theflagship tostop. The source identity supports exact repeated wording.',
104:'The Helmsman turns theship; a skilled officer allows quick turning. The role,importance andskill recommendation remain complete.',
107:'Camille explains thatgood steering helps quickly reach anadvantageous battle position. Can preserves thecapability ratherthan promising victory.',
110:'A Surveyor enables Auto Move andprovides fleet latitude/longitude. Both thefeature andcoordinates remain explicit with current role/UI terms.',
120:'Fernando volunteers forLookout duty energetically. Leave itto me keeps hisconfident voice without assigning him automatically.',
123:'Camille recommends Fernando because hisObservation suits Lookout work. The statistic androle remain clear andno guaranteed outcome isadded.',
127:'Lil asks what aLookout is. The short two-part question preserves her ignorance andsets up Fernando\'s teasing.',
131:'Fernando mocks going tosea without knowing theLookout\'s job. Oh,comeon expresses hisexasperation without a new insult orrelationship.',
135:'Lil snaps back andinsists she merelyforgot. Ionlyforgot foramoment preserves her defensive face-saving explanation ratherthan confirming she knew nothing.',
138:'Camille calms both arguing crewmates. Easy,both ofyou isidiomatic mediation without taking sides.',
142:'Revise fleets towho other ships belong to. 所属 identifies affiliation/ownership without restricting ittoa fleet. The lookout\'s at-sea reporting oncities remains;we\'re reads conversationally without adding a mechanic.',
146:'Higher Observation extends therange forspotting cities andrareitems. Farther away preserves thegraded range effect without promising particular discoveries.',
153:'Camille reminds Lil thatshe makes finalduty assignments. Still andFI preserve her authority afterthe otherofficers\' suggestions.',
157:'Camille limits thelesson toordinary sailing andwonders ifhe explained too much atonce. Both scope andconcern remain,without calling itall possible duties.',
161:'Lil hesitates butagrees totry. Well... I\'ll give itatry retains tentative resolve ratherthan confident mastery.',
166:'The FE panel names X,Deck View selection andchanging officers\' posts onthe Deck screen. Current UI terms remain exact;this modal panel keeps itsseparate consumer.',
}

if __name__ == '__main__':
    assert not ROOT.exists() and not DOC.exists() and not MENU.exists()
    old = read(OLD)
    image, previous, clean = map(NdsImage.open,(ROM,old['candidate'],'work/clean.nds'))
    digest = sha(ROM.read_bytes())
    assert digest == 'c4c998e446b7ac410d2294563fc4e5d5181cef6938c25254b1bd3679492efa20'
    arm = image.read_file('/__arm9__.bin')
    assert arm == previous.read_file('/__arm9__.bin')
    common_scope = read(COMMON_SCOPE)
    assert sha(previous.read_file('/COMMON/MESFILE.DK4')) == common_scope['original_COMMON_sha256']
    assert sha(image.read_file('/COMMON/MESFILE.DK4')) == common_scope['current_COMMON_sha256']
    assert common_scope['all_other3662_messages_and_all_native_offsets_copy_spans_exact']
    for path,expected in old['proofs'].items(): assert sha(Path(path).read_bytes()) == expected,path
    blocks, earlier, jp = (IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks for im in (image,previous,clean))
    specs = []
    for number in (120,23):
        assert blocks[number] == earlier[number]
        current_commands, current_speeches = inventory(arm,blocks[number])
        clean_commands, clean_speeches = inventory(clean.read_file('/__arm9__.bin'),jp[number])
        assert [c['word'] for c in current_commands] == [c['word'] for c in clean_commands]
        assert len(current_speeches) == len(clean_speeches)
        specs.append(dict(block=number,clean_block_sha256=sha(jp[number]),current_block_sha256=sha(blocks[number]),
            all_clean_native_commands=clean_commands,all_current_native_commands=current_commands))
    assert sum(len(s['all_current_native_commands']) for s in specs) == 124
    context = ('Complete sailing andcrew lessons andboth responses ofboth choices reread inclean Japanese. Lil\'s reluctant learning andsearch forshortcuts,Camille\'s patient insistence,Fernando\'s confident lookout offer andteasing,andall nineanonymous FE controls retain distinct voices. Preserve heading,wind/sail controls,Half Open automation,Full Open practice,staff roles,stat/range effects,coordinates andX/Deck View instructions. No newrank,relationship ormechanic. One Lookout affiliation over-specification needsrevision;63other entries retain wording withindividual reasons. New native/typed-reference/focused revised/release gates remainpending.')
    records, choices, source_rows = [], [], []
    for old_row in old['records']:
        row = deepcopy(old_row)
        number = row['block']
        source, current = bytes.fromhex(row['source_hex']), bytes.fromhex(row['current_text_hex'])
        ja, at = row['source_reference']['offset'], row['current_reference']['offset']
        assert jp[number][ja:ja+len(source)] == source and jp[number][ja+len(source)] == 0
        assert blocks[number][at:at+len(current)] == current and blocks[number][at+len(current)] == 0
        choice = 'CHOICE' in row['id']
        source_row = dict(id=row['id'],file_path='/data/SC2.DK4',block=number,
            source_reference=deepcopy(row['source_reference']),current_reference=deepcopy(row['current_reference']),
            source_hex=source.hex(),current_text_hex=current.hex(),clean_Japanese=(source if choice else source[1:]).decode('cp932'),
            current_stored_English=(current if choice else current[1:]).decode('cp932'))
        if not choice:
            source_index = int(row['id'].rsplit('R',1)[1])
            prefix = source[:1].hex()
            preamble = b'\0\x40\xff\xff\0'+source[:1]
            assert jp[number][ja-5:ja+1] == blocks[number][at-5:at+1] == preamble
            note = (REASONS120 if number == 120 else REASONS23)[source_index]
            source_row.update(source_record_index=source_index,record_index=blocks[number][:at].count(b'\0'),
                source_presentation_prefix_hex=prefix,source_complete_preamble_hex=preamble.hex())
            english = row['english']
            if row['id'] == CHANGED:
                assert 'which fleets other ships belong to' in english
                english = "{SPEAKER:09}A Lookout checks who other ships belong to and reports on cities while we're at sea."
            english += '{PAD}'
        else:
            english = row['english']
            source_row.update(source_command_offset=row['command_offset'],
                command_offset=row['current_reference']['choice_command_offset'],option_index=row['option_index'])
            note = {('120',0):'Count onme retains Lil\'s confident volunteer response. The branch meaning ispreserved without inferring a specific successful outcome.',
                ('120',1):'What aboutthewind? naturally asks whether wind needsconsideration andcontrasts withthe confident firstchoice;no directional mechanic islost.',
                ('23',0):'That\'s newtome... admits unfamiliarity withcrew assignment andkeeps thehesitant ellipsis.',
                ('23',1):'Ialreadyknowthat preserves Lil\'s impatient claim thatshe understands without hearing theexplanation;itdoes not claim theplayer hasvisited thelesson.'}[(str(number),row['option_index'])]
        entry = {**source_row,'source_Japanese':source_row['clean_Japanese'],'speaker':row['speaker'],
            'source_meaning':row['source_meaning'],'english':english,'context':context,
            'editorial_decision':'revise' if row['id'] == CHANGED else 'retain-wording',
            'localization_note':note,'fresh_retained_wording_justification':note if row['id'] != CHANGED else None,
            'historical_review':str(OLD),'historical_review_sha256':sha(OLD.read_bytes()),
            'historical_actual_samples':row.get('actual_samples',[]),
            'review':dict(source=True,context=True,localization=True,naturalness=True,formatting=False)}
        source_rows.append(source_row)
        (choices if choice else records).append(entry)
    assert len(records) == 60 and len(choices) == 4
    assert sum(r['source_presentation_prefix_hex'] == 'fe' for r in records) == 9
    assert sum(r['editorial_decision'] == 'revise' for r in records+choices) == 1
    raw = LEDGER.read_bytes()
    ledger, before = read(LEDGER), read(LEDGER)
    fresh = ledger['contextual_story_natural_dialogue_pass_v1871']
    ids = [r['id'] for r in records+choices]
    assert not set(ids) & set(fresh['record_IDs'])
    assert fresh['fresh_pass_records_explicitly_reread'] == fresh['fresh_pass_records_integrated'] == 364
    ROOT.mkdir(parents=True)
    packet = ROOT/'all64_clean_current_full_exchange_and_native_commands.json'
    save(packet,dict(candidate=str(ROM),candidate_sha256=digest,ARM9_sha256=sha(arm),blocks=specs,records=source_rows,
        complete_native_command_count=124,COMMON_late_delta_scope=str(COMMON_SCOPE),COMMON_late_delta_scope_sha256=sha(COMMON_SCOPE.read_bytes()),
        old_family_review=str(OLD),old_family_review_sha256=sha(OLD.read_bytes()),
        old_actual_scope=old['actual_verification_scope'],old_five_conditional_unvisited=old['unvisited_conditional_records'],
        new_gameplay_claim=False,new_revision_native_and_reference_approval_pending=True,full_goal_complete=False))
    base = dict(format='dk4-natural-dialogue-editorial-draft-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        encoder='dialogue-fixed-v1',dialogue_profile='lil-opening-editorial-native-v1',file_path='/data/SC2.DK4',
        review_gates=['source','context','localization','naturalness'],formatting_review_pending=True,
        source_context=str(packet),source_context_sha256=sha(packet.read_bytes()),current_ROM=str(ROM),current_ROM_sha256=digest,
        source_clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),required_runtime_ARM9_sha256=sha(arm),
        approved_names=['Rafael','Hodram','Joakim','Maria','Camille'],
        status='fresh-source-context-prose-reviewed;one-native-layout-and-registered-integration-pending',
        prior_approved_manuscripts=old['manuscripts'],historical_native_and_actual_scope=old['actual_verification_scope'],
        scoped_common_delta=str(COMMON_SCOPE),full_goal_complete=False)
    save(DOC,{**base,'records':records,'changed_IDs':[CHANGED],'justified_retained_speech_count':59})
    save(MENU,{**base,'format':'dk4-typed-choice-editorial-draft-v1','records':choices,
        'all_four_labels_retain_wording':True,'typed_choice_native_geometry_and_result_mapping_inherited_not_new_gameplay':True})
    (ROOT/'ledger_before.json').write_bytes(raw)
    (ROOT/'handoff_before.md').write_bytes(HANDOFF.read_bytes())
    fresh['record_IDs'] += ids
    fresh.update(fresh_pass_records_explicitly_reread=428,fresh_pass_records_integrated=364,fresh_pass_records_pending_native_actual_release=64,
        latest_contextual_manuscript=str(DOC),latest_contextual_choice_draft=str(MENU),
        coverage_note='364entries integrated/reconciled;earlier sailing/crew64 freshly reread withone Lookout affiliation revision and63justified retentions pending validated native/reference/revised/integration gates. Historical1831 totals unchanged;1467 historical completions outside the reconciled fresh pass include this pending64.')
    fresh.setdefault('pending_historical_reconciliations',[]).append(dict(id='Lil-sailing-and-crew-lessons64',record_IDs=ids,
        manuscripts=list(map(str,(DOC,MENU))),source_context=str(packet),revised_IDs=[CHANGED],retained_count=63,
        source_context_prose_complete=True,new_native_reference_revised_release_pending=True))
    ledger['coverage_units'].append(dict(id='Lil-sailing-crew64-contextual-v1977',file_path='/data/SC2.DK4',blocks=[120,23],record_IDs=ids,
        status='fresh-contextual-source-prose-reviewed;one-revision-native-reference-integration-pending',
        source_context=str(packet),manuscripts=list(map(str,(DOC,MENU))),revised_IDs=[CHANGED],justified_retained_count=63,
        completed_entries_added=0,source_prose_reviews_added=0,historical_entries_reconciled=0,full_goal_complete=False))
    ledger['active_source_prose_drafts']['manuscripts'] += list(map(str,(DOC,MENU)))
    ledger['active_source_prose_drafts'].update(status='116-reviewed-COMMON-and64-fresh-historical-lesson-reconciliation-open',
        note='Lesson64 freshly reread;one affiliation wording change and63justified retentions. Historical completion totals remain;fresh reconciliation waits fornecessary new native/reference/revised/release checks. All broader prose remainsopen.')
    summary = ('V1977 full sailing/crew64 fresh clean-Japanese contextual review:one proposed revision DK4_MES_B23_R0142 removes unsupported fleet-specific wording fromship affiliation;63justified retentions,including both two-label choices. '
        'Fresh428 explicitly reread,364integrated/reconciled,64pending;historical1831(1362revised469retained) andsource/prose1947 unchanged. '
        'B120/B23 andARM9 matchpriorV1775 exactly;COMMON differs only bythe already-proven sixreinforcement announcements. '
        'Existing55unique actual speeches/fiveconditional equivalents remain historical coverage;no newgameplay ornewnative-format approval claimed. '
        'Currentrecord indices differ fromclean indices afterprior relocation:Lookout cleanR0142/currentrecord141,sourceoffset1845/current2095. Preserve distinct references. '
        'RegisteredV1971/clean patch unchanged;116COMMON,allbroader prose,graphics/all18plaques andlaterolder-record technical re-audit stayopen;fullgoalactive.')
    ledger['latest_checkpoint'] = summary
    ledger['research_checkpoints'].append(dict(id='V1977-lessons64-fresh-contextual-prose',proof=str(ROOT/'source_prose_review_receipt.json'),
        completed_entries_added=0,source_prose_reviews_added=0,fresh_contextual_rereads_added=64,new_revisions_proposed=1,full_goal_complete=False))
    for key in ('records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed','records_with_source_and_prose_pass',
        'completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file','current_integrated_candidate',
        'unresolved_graphics_work','reviewed_but_incomplete_COMMON_IDs','older_record_reaudit_after_full_editorial_goal'):
        assert ledger[key] == before[key],key
    assert len(fresh['record_IDs']) == len(set(fresh['record_IDs'])) == 428
    assert ledger['goal_status'] == 'active' and not ledger['full_goal_complete']
    pending = LEDGER.with_name('editorial_review_current_v1977_pending.json')
    assert not pending.exists() and LEDGER.read_bytes() == raw
    save(pending,ledger)
    os.replace(pending,LEDGER)
    text = HANDOFF.read_text(encoding='utf-8').replace('# Current editorial handoff - V1976','# Current editorial handoff - V1977',1)
    old_line = 'Fresh V1871 contextual pass:364 explicitly reread andintegrated/reconciled(Stockholm51 +London111 +Speyer59 +Hamburg81 +trade-route/officer13 +opening49 retained). Prior1467 completions require explicit reconciliation.'
    assert old_line in text
    text = text.replace(old_line,'Fresh V1871 contextual pass:428 explicitly reread;364integrated/reconciled;64sailing/crew lesson entries pending(one revision63retentions). Prior1467 historical completions outside the reconciled fresh pass include this pending64.')
    anchor = '## Earlier B22 opening fresh contextual retention pass - V1976'
    chapter = ('## Active unit: earlier sailing/crew64 fresh contextual pass - V1977\n\n'+summary+'\n\n'
        f'- Source:{packet.as_posix()};speechdraft:{DOC.as_posix()};choices:{MENU.as_posix()}. All60 speeches/system panels andfourlabels read ascomplete exchanges.\n'
        '- ChangeR0142 to: A Lookout checks who other ships belong to and reports on cities while we\'re at sea. Source他の船の所属 doesnot restrict affiliation tofleets. Other63entries retain exactwords withspecific reasons.\n'
        '- Next:focused native/font check forthe changed progressive paragraph;bind59unchanged speech targets/nineFE andfourlabels toexisting exactproofs;complete current-source B23typed relocation/branch/reference map;target revised Lookout display andnormal return withoriginal controls;register a successor onlyafternecessary checks. No need repeat allB120 wind paths orall60 earlier speech visits.\n'
        '- Preserve distinct clean/current indices afterprior relocation. Lookout IDR0142 hascleanrecord142/currentrecord141;sourceoffset1845/current2095. Current typed choices atB1201138 andB23150. Sourcechoice commands1050/126 remainseparate.\n'
        '- Do not pass FE throughprogressive actor/macro logic. ExistingnineFE mode1/display proof remainsdistinct;threeunvisited repeatedCamille andtwounvisited repeatedFE objects retain equivalent-consumer evidence,no individual visit claim.\n\n')
    HANDOFF.write_text(text.replace(anchor,chapter+anchor),encoding='utf-8')
    for name in ('translation_progress.md','todo.md','editorial_review_goal.md'):
        with (Path('docs')/name).open('a',encoding='utf-8') as stream: stream.write('\n\n## V1977 lessons64 fresh contextual pass\n\n'+summary+'\n')
    save(ROOT/'source_prose_review_receipt.json',dict(source_context=str(packet),source_context_sha256=sha(packet.read_bytes()),
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),choices=str(MENU),choices_sha256=sha(MENU.read_bytes()),
        current_candidate=str(ROM),candidate_sha256=digest,fresh_rereads_added=64,revisions_proposed=1,justified_retentions=63,
        fresh_reread_total=428,fresh_integrated_reconciled=364,fresh_pending=64,historical_completed_unchanged=1831,
        new_ROM_or_gameplay_credit=False,ledger_sha256=sha(LEDGER.read_bytes()),handoff_sha256=sha(HANDOFF.read_bytes()),
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(fresh_reread=428,fresh_integrated=364,fresh_pending=64,revisions_proposed=1,justified_retentions=63,ROM_unchanged=True))
