"""Whole-source/current editorial comparisons for22 connected sailing/battle Help articles."""
import re,struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Shared_HELP_T81_T102_clean_20261104')
RETAIN={
81:"Report a Golden Route you discovered. Receive discovery rewards for a limited time. Each route can be reported only once. See [[141|Golden Route Log]] and [[201|Discovery]].",
92:"Win by reducing the enemy flagship's durability to zero, or capturing the enemy flagship. [Tip] Victory lowers enemy [[150|share]] in nearby cities. Captured ships may yield coins and cargo.",
94:"Defeat the monster. You may receive an item.",
96:"Attacks occur automatically. [Tip] Arrange officers for battle on [[105|Deck View]] beforehand. You may still rearrange after battle begins. Actions: [[97|Gunfire]], [[98|Melee]], [[99|Duel]], [[100|Ram]].",
101:"During normal sailing, you can steer with the touchscreen. Touch the direction you want to sail, and the ship moves that way. Touch farther from the ship to sail faster. Touch the ship itself to stop in place."
}
REVISE={
82:"Commands available while sailing: [[83|Manual Sailing]], [[84|Auto Move]], [[85|Info Mode]], [[86|Search]], [[87|Declare War]], [[88|Village]], [[89|Battle]], [[153|Sea Info]] and [[103|Shared Commands]].",
83:"During normal sailing, steer with the D-pad and adjust the sails with L and R. You can also steer [[101|with the touchscreen]]. Press A to open the sails and speed up, or B to close them and slow down. Ships leave port with their sails Half Open. Press A to change to Full Open. While Half Open, the sails adjust automatically if every mast has [[125|a Sail Handler]].",
84:"The ship follows its route automatically. Press B, then confirm with A to cancel Auto Move and return to [[83|manual sailing]]. You cannot restart Auto Move at sea. [Tip] If your ship has an Eagle Figurehead fitted, time passes faster during Auto Move. Press A during Auto Move to restore normal time.",
85:"Press Y to pause and inspect cities and ships on screen. From Info Mode, choose [[86|Search]] or [[87|Declare War]].",
86:"Search around the ship. From [[85|Info Mode]], press Y or R to enter Search Mode, then press A to search. You may find water, food or items. A failed search adds 3 fatigue. Sailors may desert or be attacked by wild animals while searching.",
87:"Start a [[89|battle]] with a fleet or town on screen. From [[85|Info Mode]], press Y twice or L, then select a target to begin. Declaring war puts you [[187|at war]] with that faction and greatly reduces your friendship rating. Declaring war on a town limits its commands. You cannot declare war on an allied fleet.",
88:"You may discover villages while sailing. Villagers may give you food or water, or repair your ships. You give them a few gold coins in return for their help. [Tip] Discovering a village reveals nearby land and sea on the Route Map. [Tip] Villagers ask for a password called [[102|Promised Words]]. Enter the correct password to trigger an event.",
89:"Encountering a fleet you are [[187|at war]] with, or a monster such as a shark, starts a battle. You move ships as in [[83|manual sailing]]; guns and other attacks are automatic. See [[90|Battle Start]], [[91|Victory]] and [[95|Defeat]], plus [[96|Battle Actions]].",
90:"Battle begins when you encounter a fleet you are [[187|at war]] with, [[87|declare war]] on another faction's fleet, come under attack by a town, or are attacked by a monster. Towns under an enemy faction's [[151|exclusive contract]] attack when you approach.",
91:"Meet one victory condition to end battle. Conditions depend on the enemy. See [[92|Fleet Battle]], [[93|Town Battle]] or [[94|Monster Battle]].",
93:"Defeat a town by reducing its Arms rating to zero or making it surrender. A town may surrender as its Arms rating falls. [Tip] Winning a battle against a town earns you [[150|10 percent market share]] there.",
95:"You lose if your flagship's durability reaches zero or it is captured. [Tip] When your flagship is defeated, your character moves to another ship in your fleet and the battle ends.",
97:"Ships attack with mounted guns. More [[129|Batteries]] and stronger guns improve attacks. A [[56|Bow Gun]] adds some forward fire, while an [[57|Aft Gun]] adds some rear fire. [Tip] Put companions with high Aim in every Battery to fire more shots.",
98:"Sailors fight when ships touch. When your flagship touches an enemy ship, your companions fight too, and their results affect the sailors' battle. [Tip] To improve boarding strength, put your character in the [[120|Captain's Cabin]] on the flagship, and assign companions with high Swords to all [[128|Quarters]] and [[126|Deck]] positions.",
99:"A duel begins when the flagships draw close. Your [[128|Boarding Leader]] fights; without one, a [[126|Deckhand]] or your character fights instead.",
100:"A ship with a [[56|ram]] may punch a hole in an enemy ship by striking its side. The target loses a lot of durability; the attacking ship loses a little too.",
102:"In the PC game Uncharted Waters Online, members can earn passwords paired with village names by completing quests. Sail to the named village and enter its password to add new trade goods there and make trading available."
}
NOTES={
81:"Retain the clear report/reward/one-report-per-route instructions. Golden Route Log and Discovery are intelligible cross-reference labels in this whole Golden Route context; they do not rename a command or imply a different reward. Restore both original links and remove premature wraps.",
82:"Replace flattened fragment rows and lowercase info with one readable command list. Restore all nine original links and use native Auto Move plus the bound Sea Info heading and Shared Commands terminology.",
83:"Retain the fluent steering,initial Half Open andall-masts staffing explanation. Restore omitted physical sail controls. Current9101-frame inherited-save test observes B closing toanchor andA reopening;native footer binds L/R rotation. Keep manual sailing andall-masts automation distinct;invent no bonus when fullyopen.",
84:"Correct X toB: current Auto Sail footer,Stop question andA confirmation areobserved. Explicitly include that confirmation. Bind Eagle Figurehead to the actual item name andrequire it fitted,notmerely owned. The fast-time A instruction issource/code-bound,not a newly observed equipped-Eagle speed test.",
85:"Retain the natural first sentence. Correct info capitalization,restore both links andcombine redundant mode-switch instructions. Info Mode is the Help/panel name;Inspect is the existing footer/action alias used inRafael's reviewed tutorial.",
86:"Correct the false causal restriction: onlythe three-point fatigue increase depends onfinding nothing. Desertion/animal attacks mayoccur duringsearch itself. Preserve Y/R entry andA execution,withsource/native references rather thaninventing new keys.",
87:"Separate the At War state fromthe numerical friendship rating;relations do not themselves fall sharply. Correct ship to fleet,retain target selection andtown command restrictions,andlimit the allied-fleet prohibition specifically todeclaring war rather thaninventing immunity toall attacks.",
88:"Restore the gold gift inreturn forhelp,Route Map andthe actual Promised Words feature label. A correct password triggers anevent;the source isnot merelya chance aftercorrect entry. Do notpromise particular rewards orimmediate trading fromthis village introduction.",
89:"Restore the explicit At War fleet condition andshark example,keeping the already-clear manual steering/automatic attacks sentence. Context96 stillallows crew reassignment duringbattle;this passage doesnot prohibit other setup screens. Restore all six links.",
90:"Replace often near an enemy monopoly withthe source's specific hostile exclusive-contract approach condition. Preserve all four triggers andthree links;do not substitute a probability orshare threshold.",
91:"Retain the clear firsttwo sentences. Correct the malformed and/or cross-reference list andlowercase fleet label;use three parallel opponent-specific alternatives. No extra victory condition isintroduced.",
92:"Retain the natural two-alternative win instruction andconditional loot. Nearby cities isgeneric town wording inthis battle context,not a City-class restriction. Restore the market-share link without changing a word;promise no automatic capture ofthe hull.",
93:"Keep both victory routes butreplace anunsupported comparative surrender probability withthe source's conditional surrender asArms falls. Write percent as a word andrestore the share link;earn10-percent share doesnot mean multiply orreset the existingtotal.",
94:"Retain both concise,idiomatic sentences. Defeat the monster expresses victory inthis Victory article;may correctly preserves a possible item rather than a guaranteed reward.",
95:"Replace compressed mixed numbered fragments witha complete sentence anduse your character. Preserve both flagship defeat triggers,transfer toanother fleetship andbattle end;invent no additional game-over orreplacement rules.",
96:"Retain the clear automatic-attacks instruction andthe explicit ability toreassign afterbattle begins. Restore allfive links in the existing natural wording. Officers is the established generic crew term,not a newly invented military rank.",
97:"Retain the gun-count/strength relationship,bind Battery andAim tocurrent labels,andreplace partly forward andback withclear directional fire. Preserve more shots fromhigh-Aim assignments at every Battery;invent no ammunition limit ordamage reduction.",
98:"Preserve sailors-versus-companions participation andthe effect ofcompanions' results. Restore flagship-specific Captain's Cabin placement,all Quarters/Deck positions andthe actual Swords skill instead ofgeneric skilled fighters. Do not arbitrarily restrict those latter positions toone ship.",
99:"Correct the unsupported may anduse native Boarding Leader/Deckhand rather than a guessed Marine Captain rank. Preserve the source's fallback alternatives without inventing selection priority.",
100:"Replace hole an enemy/loses much withnatural punch a hole/loses a lot. Preserve side impact,possible hull puncture,large target durability loss andthe attacker's smaller loss;promise no guaranteed puncture orinstant defeat.",
101:"Retain the complete,fluent touchscreen instructions andall three relations:touch direction,distance controls speed,touching ship stops it. Only formatting changes;no reason toreplace this wording.",
102:"Restore the named PC-game membership/quest tie-in,the village-specific password andthe availability oftrading,which the old online quest shortcut obscures. Use existing Uncharted Waters Online andPromised Words names. This is historical game copy,not a claim ofpresent service/code availability ornew timing rules."
}
HEADINGS={81:'Report Golden Route (Guild)',82:'At-Sea Commands',83:'Manual Sailing',84:'Auto Move',85:'Info Mode (At Sea)',86:'Search Mode (At Sea)',87:'Declare War Mode',88:'Village',89:'Battle',90:'Battle Start',91:'Victory',92:'Victory: Fleet',93:'Victory: Town',94:'Victory: Monster',95:'Defeat',96:'Battle Actions',97:'Gunfire',98:'Boarding',99:'Duel',100:'Ram Attack',101:'Touchscreen Sailing',102:'Promised Words'}

def plain(text):return ' '.join(re.sub(r'\[\[\d+\|([^\]]+)\]\]',r'\1',text).split())

if __name__=='__main__':
    output=ROOT/'whole_article_comparisons_v1.json';binding_path=ROOT/'native_controls_roles_items_andterms_v1.json'
    assert not output.exists() and not binding_path.exists()
    draft_path=ROOT/'clean_meanings_andfull_drafts_v1.json';current_path=ROOT/'current_full_articles_verified_parent_v1.json'
    draft,current=map(load,[draft_path,current_path]);assert len(draft['records'])==len(current['records'])==22
    controls_path=Path('work/analysis/HELP83_current_sail_controls_20261104/control_binding_v1.json');controls=load(controls_path)
    assert controls['observed_inputs']==dict(A_opens_sails=True,B_closes_sails=True,A_reopens_from_anchored_state=True,B_opens_Stop_Auto_Move_question=True,A_confirms_return_to_manual=True)
    image=NdsImage.open(current['current_ROM']);arm=image.read_file('/__arm9__.bin');clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert sha(arm)==controls['current_ARM9_sha256'] and sha(Path(current['current_ROM']).read_bytes())==current['current_ROM_sha256']
    startup_path=Path('work/analysis/Early_HELP23_release_verified_20261104/own_registered_startup_verification.json');startup=load(startup_path)
    report=load(Path(startup['capture_report']));snapshot=report['read_only_RAM_snapshot'];ram=Path(snapshot['path']).read_bytes();assert sha(ram)==snapshot['sha256']
    assert arm[0x86314:0x86334]==clean[0x86314:0x86334]==ram[0x86314:0x86334]
    table,original=[struct.unpack_from('<I',v,0x86334)[0]for v in [arm,clean]];roles=[]
    for n,jp,en in [(5,'操帆手','Sail Handler'),(8,'斬込隊長','Boarding Leader'),(15,'甲板要員','Deckhand')]:
        ptr=struct.unpack_from('<I',ram,table-0x02000000+n*4)[0];raw=ram[ptr-0x02000000:].split(b'\0')[0]
        prior=struct.unpack_from('<I',clean,original-0x02000000+n*4)[0];source=clean[prior-0x02000000:].split(b'\0')[0]
        assert raw.rstrip()==en.encode('ascii') and source==jp.encode('cp932')
        roles.append(dict(index=n,source_pointer=prior,current_pointer=ptr,source_hex=source.hex(),current_exact_hex=raw.hex(),Japanese=jp,English=en))
    fields=[]
    for at,jp,en in [(0x148304,'命中力','Aim'),(0x148334,'剣闘術','Swords')]:
        a=arm[at:].split(b'\0')[0];b=clean[at:].split(b'\0')[0];assert a==en.encode('ascii') and b==jp.encode('cp932')
        fields.append(dict(file_path='/__arm9__.bin',offset=at,source_hex=b.hex(),current_hex=a.hex(),Japanese=jp,English=en))
    old_item,item=[struct.unpack_from('<I',a,0x11ecc0)[0]for a in [clean,arm]]
    assert clean[old_item-0x02000000:].split(b'\0')[0]=='大鷲の像'.encode('cp932')
    assert arm[item-0x02000000:].split(b'\0')[0]==b'Eagle Figurehead'
    promised=struct.unpack_from('<I',arm,0x119298)[0];assert ram[promised-0x02000000:].split(b'\0')[0]==b'Promised Words'
    mode_path=Path('work/emulation_v193/generated_modes_v213/capture_report.json');mode=load(mode_path);mode_ram=Path(mode['read_only_RAM_snapshot']['path']).read_bytes();assert sha(mode_ram)==mode['read_only_RAM_snapshot']['sha256']
    mode_spans=[]
    for lo,hi in [(0x68000,0x6e000),(0x119134,0x1191a0)]:
        assert arm[lo:hi]==mode_ram[lo:hi];mode_spans.append(dict(offset=lo,bytes=hi-lo,sha256=sha(arm[lo:hi])))
    assert [r for r in mode['scripted_input_schedule']if r['start']>=16800]==[dict(start=n,duration=12,buttons=['Y'])for n in [17000,17500,18000]]
    tutorial_path=Path('translations/rafael_B46_contextual_final_review_v1.json');tutorial=load(tutorial_path)
    mode_records=[r for r in tutorial['records']if r['id']in ['DK4_MES_B46_R0065','DK4_MES_B46_R0072','DK4_MES_B46_R0091']]
    assert len(mode_records)==3
    assert b'Uncharted Waters Online' in arm
    save(binding_path,dict(current_ROM=current['current_ROM'],current_ROM_sha256=current['current_ROM_sha256'],current_ARM9_sha256=sha(arm),
      current_controls=str(controls_path),current_controls_sha256=sha(controls_path.read_bytes()),native_roles=roles,native_skill_fields=fields,
      Eagle_Figurehead=dict(pointer_field=0x11ecc0,source_pointer=old_item,current_pointer=item,Japanese='大鷲の像',English='Eagle Figurehead'),
      Promised_Words=dict(pointer_field=0x119298,current_pointer=promised,English='Promised Words'),
      current_own_startup=str(startup_path),current_own_startup_sha256=sha(startup_path.read_bytes()),current_own_RAM=snapshot,
      historical_Y_mode_cycles_report=str(mode_path),historical_Y_mode_cycles_report_sha256=sha(mode_path.read_bytes()),matching_mode_dependency_spans=mode_spans,
      L_R_Y_A_tutorial_reference=str(tutorial_path),L_R_Y_A_tutorial_reference_sha256=sha(tutorial_path.read_bytes()),L_R_Y_A_tutorial_record_IDs=[r['id']for r in mode_records],
      source_andhistorical_controls_bound_not_new_current_individual_R_L_search_visits=True,
      equipped_Eagle_fast_time_A_source_bound_not_new_physical_speed_test=True,
      game_brand='Uncharted Waters Online',brand_source='translations/common_online_promotional_manuscript_v2.json',
      historical_tie_in_copy_not_present_day_service_claim=True,native_storage_trailing_blank_phase_preserved_not_copied_to_logical_prose=True,
      no_global_actor_name_review_credit=True,new_credit=0,producer_sha256=sha(Path(__file__).read_bytes())))
    records=[]
    for source,old in zip(draft['records'],current['records'],strict=True):
        n=source['topic_id'];assert old['topic_id']==n and source['source_hex']==old['source_hex']
        english=(RETAIN|REVISE)[n];ids=[int(t)for t in re.findall(r'\[\[(\d+)\|',english)];assert ids==source['original_link_IDs']
        assert english.isascii() and '\n' not in english and not old['complete_current_continuations']
        retained=n in RETAIN
        if retained:assert plain(english)==plain(old['current_English_with_link_IDs'].split('\n',1)[1])
        meaning=source['clean_meaning']
        if n==99:meaning='Nearby flagships trigger a duel;the Boarding Leader fights,orwithout one a Deckhand orthe player character. No added fallback priority.'
        records.append(dict(id=source['id'],topic_id=n,file_path='/COMMON/HELP.DK4',source_reference=source['source_reference'],source_hex=source['source_hex'],
          source_meaning=meaning,source_Japanese_with_link_IDs=source['source_Japanese_with_link_IDs'],current_reference=old['current_reference'],current_hex=old['current_hex'],
          current_English=old['current_English_with_link_IDs'],original_link_IDs=ids,complete_current_continuations=[],heading=HEADINGS[n],english=english,
          decision='retention'if retained else'revision',finding=NOTES[n],retention_reason=NOTES[n]if retained else None,localization_note=NOTES[n],speaker='Help narrator',
          context='Complete connected Guild report/Sea Commands/manual andautomatic controls/Search/Declare War/Villages/Battle conditions andactions/touchscreen/cross-game password exchange81through102;all original destinations reviewed together.',
          review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),native_term_orcontrol_binding_pending=False,
          binding=str(binding_path),binding_sha256=sha(binding_path.read_bytes()),fresh_display_allocation_widgets_andintegration_pending=True,new_credit=0))
    assert sum(r['decision']=='revision'for r in records)==17 and sum(r['decision']=='retention'for r in records)==5
    save(output,dict(records=records,records_count=22,proposed_revisions=17,justified_retentions=5,first_four_gates_passed=22,
      pending_localization_binding_topic_IDs=[],all_fifth_gates_pending=True,translation_policy='natural-dialogue-v2',target_locale='en-US',
      current_ROM=current['current_ROM'],current_ROM_sha256=current['current_ROM_sha256'],five_body_retentions_word_exact_after_removing_wraps_andrestoring_links=True,
      source_draft=str(draft_path),source_draft_sha256=sha(draft_path.read_bytes()),current_packet=str(current_path),current_packet_sha256=sha(current_path.read_bytes()),
      native_binding=str(binding_path),native_binding_sha256=sha(binding_path.read_bytes()),actual_new_control_test_scope=controls['observed_inputs'],
      all_text_formatting_representative_Help_display_andregistered_integration_pending=True,new_credit=0,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print('22 whole-source/current comparisons:17 revisions/5 exact-body retentions,all four prose gates pass.Fresh formatting/Help display/integration pending,no credit.')
