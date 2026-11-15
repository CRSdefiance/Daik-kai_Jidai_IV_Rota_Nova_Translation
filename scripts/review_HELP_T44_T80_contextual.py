"""Compare 37 sealed clean-source drafts with complete verified current Help articles."""
import re
import struct
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.help_source_links import source_links
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Shared_HELP_T44_T80_clean_20261104')
HEADINGS = ['Shipyard','Buy (Shipyard)','Standard (Buy)','Special (Buy)','Sell (Shipyard)',
 'Repair (Shipyard)','Remodel (Shipyard)','Equipment (Remodel)','Sails (Remodel)',
 'Figurehead (Remodel)','Extra Equipment (Remodel)','Armor (Extra Equipment)',
 'Bow Equipment','Stern Equipment','Guns (Remodel)','Holds (Remodel)','Workrooms (Remodel)',
 'Rename Ship','Dock (Shipyard)','Swap Ships (Dock)','Captain (Dock)','Arrange (Dock)',
 'Create Fleet','Manage Area (Regional Fleet)','Patrol (Regional Fleet)','Dock (Regional Fleet)',
 'Attack Town (Regional Fleet)','Fleet Setup','Disband (Regional Fleet)','Port','Depart (Port)',
 'Sail (Depart)','Auto Move','Deck View','Dock (Port)','Cargo Setup (Port)',
 'Ruins and Churches (Cities Only)']

REVISIONS = {
44: "Build and refit ships, store ships you are not using, and create or disband regional fleets. Each job takes time and gold, depending on the work. A [[113|Shipwright]] may reduce the cost. See [[45|Buy]], [[48|Sell]], [[49|Repair]], [[50|Remodel]] and [[62|Dock]].",
45: "Available ship types vary by region. Name each ship after purchase. Choose [[46|Standard]] or [[47|Special]].",
48: "Sell a ship you own. Its sailors move to other ships in your fleet. Transfer the trade goods it carried to other ships using [[79|Cargo Setup]] at the port.",
49: "Restore ship durability. Repairs cost money and take several days. A [[113|Shipwright]] lowers the cost.",
50: "Refit your ship to improve its performance. See [[51|Equipment]] and [[61|Rename]].",
51: "Change or add equipment. Move the cursor to the position you want to change. Press the selection button to cycle through the equipment choices for that position. Once every position shows the equipment you want, press the execution button to carry out the refit. See [[52|Sails]], [[53|Figurehead]], [[54|Extra Equipment]], [[58|Guns]], [[59|Holds]] and [[60|Workrooms]].",
52: "Change the sails on your masts. Each ship has limits on the sails it can carry. Square sails improve speed with a following wind; lateen sails improve speed in a headwind. Adding topsails improves speed with a following wind, while adding staysails improves speed in a headwind.",
53: "Fit a figurehead to the bow. Figureheads can protect the ship from disasters and other hazards. You can do this only if you have an item in the Figurehead category.",
54: "Add or change armor, bow equipment and stern equipment. See [[55|Armor]], [[56|Bow Equipment]] and [[57|Stern Equipment]].",
55: "Extra armor protects the ship from cannon fire. It increases maximum durability but slightly reduces speed.",
56: "Fit a spritsail, bow gun or ram. A spritsail improves speed with a following wind. A bow gun lets you fire ahead of the ship. A ram lets you attack an enemy ship by striking it with your bow.",
57: "Fit a jigger spanker or stern gun. The jigger spanker improves speed in a headwind. A stern gun lets you fire behind the ship.",
59: "Change the use of a [[127|hold]]. The choices are Quarters for marines, Battery for cannons, Rowers, Supplies and Cargo. You cannot change or add Rowers. Some holds restrict which uses are available. Adding holds slightly reduces speed. Each ship can have up to four Quarters and four Batteries, five Cargo holds and any number of Supplies holds.",
60: "Change your [[110|workrooms]]. You cannot convert Captain, Mate, Helm, Survey, Lookout, Mast or Deck to another type of room. Except for Cabin, Mast and Deck, each type can appear only once on a ship.",
62: "Move ships into or out of the dock, and create or disband regional fleets. See [[63|Swap Ships]], [[64|Captain]], [[65|Arrange]], [[66|Create Fleet]], [[71|Fleet Setup]] and [[72|Disband]].",
64: "Appoint a captain for each ship. You can put companions in command of ships other than the flagship, too. Select a companion to make them captain. Cancel the assignment to let an ordinary sailor command that ship. [!] Assign your character as a ship's captain to make it the flagship. [!] Companions serving as captains gain levels more easily.",
66: "Create a regional fleet commanded by a companion with Leadership of at least 150. Choose a policy to delegate its activities; you can change that policy through Info. Each new fleet needs 100,000 gold coins in operating funds. You can create up to six regional fleets. If every ship in one sinks, its commander returns to your main fleet. See [[67|Manage Area]], [[68|Patrol]], [[69|Dock]] and [[70|Attack Town]].",
67: "Delegate activities throughout the sea region to the fleet. Its commander decides when to trade, invest and carry out other activities. You receive a report of its income and expenses each month.",
68: "Station the fleet at sea near a town you have a [[36|contract]] with, ready for attacks by other factions.",
70: "Attack a town you do not have a [[36|contract]] with to reduce other factions' [[150|Market Share]] there.",
71: "Reorganize a regional fleet. You can do this only while it is docked in the same town as your fleet.",
72: "Disband a regional fleet. You can do this only while it is docked in the same town as your fleet. Its commander returns to your main fleet, along with any operating funds it has left.",
73: "Replenish water and food, then set sail. [!] If your water and food are not full, the port official asks whether you want to replenish them. Choose Yes to fill the available capacity with equal amounts of water and food. Choose No to adjust their proportions yourself. See [[74|Depart]], [[78|Dock]] and [[79|Cargo Setup]].",
74: "Begin a voyage. Choose [[75|Sail]], [[76|Auto Move]] or [[77|Deck View]].",
77: "This is the same as [[105|Deck View]] under Shared Commands.",
79: "Transfer cargo between ships. Any cargo left off the ships is discarded.",
80: "As the story progresses, paths to ruins or churches near a town may open. Discovering ruins or churches increases your [[184|Power]]. You may also be able to take part in ceremonies or festivals, which grant experience. [!] Valuable items may lie in the ruins. Be sure to visit."
}
RETENTIONS = {
46: "Buy a standard ship.",
47: "Order a ship matching modifications on one you own. Only available where that ship type is sold.",
58: "Select the gun shown by the wheel to change its type. City Growth unlocks up to six gun types.",
61: "Change a ship's name.",
63: "Store ships or retrieve them. Sailors, cargo, and supplies remain aboard. When retrieving, you may also [[65|Arrange]] and [[139|Assign Sailors]].",
65: "Change ship order. The flagship is always first; choose the second, third, and later ships in order. Confirm after selecting every ship.",
69: "Dock at a [[36|contracted]] city.",
75: "Control the ship yourself.",
76: "Auto Move takes you to a chosen city automatically. It requires a [[120|Captain]] and [[123|Surveyor]]. You can travel only between cities connected by a valid route: the starting city and destination must be linked on the [[104|Route Map]], and your faction must have [[150|market share]] in both cities and every intermediate city. Valid routes are shown in red.",
78: "Same as the [[62|Shipyard Dock]]."
}
FINDINGS = {
44: "Keep the source's job-dependent cost/time and conditional discount. Bind Shipwright to the existing role, restore all six links, and use the native Remodel command label.",
45: "Retain the clear regional selection and naming instructions. Change only the Custom Order choice to the stored UI label Special and restore both links.",
46: "Retain the concise complete sentence: standard ship accurately conveys standard specifications in the Standard purchase context.",
47: "Retain this natural compact help description. It preserves matching modifications and availability only where that ship type is sold; it does not promise copied cargo or crew.",
48: "Correct the lowercase sentence opening; identify sailors as those aboard the sold ship and make the other-ship goods transfer explicit. Use the native Cargo Setup label.",
49: "Retain both clear repair sentences and the definite discount. Change only the role term to the bound Shipwright and restore its original link.",
50: "Restore both original destinations and use the native Equipment/Rename labels. Improve its performance naturally expresses the source's power-up without new statistics.",
51: "The current article asserts A for cycling and Y for execution. Clean source uses circle/triangle symbols. A stored Undo label is associated with Y in prior producer notes; this is a concrete conflict, not proof of the physical execution button. Provisional generic buttons must not ship; localization remains pending a native input binding.",
52: "Restore the omitted ship-specific sail restriction. Preserve the four separate sail/wind relationships; add no all-weather speed benefit.",
53: "Replace the fragment and lowercase figurehead heading with full, natural instructions. Keep item-category ownership as a prerequisite and protection conditional rather than immunity.",
54: "Keep the three alternatives and restore all three original links. Use bow/stern equipment, avoiding the vague bow gear wording.",
55: "Restore the source's protective purpose as well as maximum durability and slight speed loss; invent no armor material.",
56: "Keep the already-reviewed spritsail interpretation and all three directional effects. Replace list fragments/lowercase fire with full sentences; fittings remain alternatives.",
57: "Use the native Jigger Spanker term instead of the shortened spanker and smooth the fragments. Preserve headwind speed and stern firing direction.",
58: "Retain the accurate, clear cannon selection instruction, Growth dependency and six-type maximum. Clean source58 says Growth while source37 says Arms for better ships/cannons; preserve this distinction rather than silently harmonizing different source claims.",
59: "Keep all limits and the unchangeable/unaddable rowing space. Bind actual short choices Quarters/Battery/Rowers/Supplies/Cargo and clarify four of each combat type. Separate clean COMMON1275/1276 descriptions independently state four for each type; this is source reconciliation, not a newly executed equipment-limit test.",
60: "Replace the misleading officer cabins umbrella with workrooms and use actual short labels. Preserve all seven nonconvertible stations and only the three duplicate exceptions. Captain here is a room label, not a newly invented rank.",
61: "Retain the complete, idiomatic one-sentence rename instruction; it matches the whole source without embellishment.",
62: "Restore all six functional links with current command labels. Store/retrieve and create/disband are separate operations, not one vague manage action.",
63: "Retain the natural three-sentence explanation and the important aboard-while-stored fact. Restore the two original links without changing the word chain.",
64: "Clarify appointing a captain rather than an unspecified officer. Cancel means a sailor commands the ship. Preserve the player-character flagship change and easier leveling only for companion captains.",
65: "Retain the clear complete sequence: flagship first, select all remaining positions, then confirm. The semicolon joins the rule naturally to the instruction.",
66: "Clarify that 100,000 coins are operating funds, not a nonrefundable fee. Preserve Leadership at least150, six-fleet limit, Info policy changes and commander return only after every ship sinks. Restore four policy links with native labels.",
67: "Correct Give the whole sea to its commander: the source delegates activities, not ownership. Keep trading/investment as commander decisions and the monthly income/expense report.",
68: "Restore stationing at sea near a contracted town and preparation against attacks; avoid implying free roaming or guaranteed successful defense.",
69: "Retain the clear docking instruction. Contracted city is ordinary generic town wording in this command context, not a new City-class restriction. Restore the contract link in the existing phrase.",
70: "Preserve the no-contract condition and reduction of other factions' market share; promise no capture. Restore both links and use the native Attack Town label.",
71: "Correct your city, which can imply ownership, to same town as your fleet and restore the only-while-docked condition. Reorganize covers fleet composition without narrowing it to sailing order alone.",
72: "Correct the lowercase its and ownership ambiguity; restore same-town-only condition and return of commander plus remaining operating funds.",
73: "Keep Yes versus No as distinct supply actions: equal full supplies versus adjustable ratio. Smooth the instruction, correct lowercase if, and restore three links with native command labels.",
74: "Retain Begin a voyage and the three existing native choice names. Smooth Choose ... or and restore all three links.",
75: "Retain the direct natural sentence; the Sail choice and parent Depart context supply the voyage setting without redundant prose.",
76: "Retain the entire accurate, fluent explanation: both required roles, connected map line, market share at both ends and every intermediate town, and red routes. Repair only wrap/link geometry; do not shorten it to fit.",
77: "Make the cross-reference a complete natural sentence; use Shared Commands and restore the original Deck View link.",
78: "Retain the familiar concise cross-reference. Same as is natural help prose and accurately identifies the identical Shipyard Dock operation; restore its original link.",
79: "Replace off every ship with natural unloaded-cargo wording. Preserve transfer and definite disposal; invent no shore storage.",
80: "Preserve City-only scope, conditional story access, Power gain on discovery, possible experience-giving ceremonies and possible valuable items. Restore the Power link and the inviting final suggestion without promising rewards or assigning an unspecified experience beneficiary."
}

def plain(text):
    return ' '.join(re.sub(r'\[\[\d+\|([^\]]+)\]\]', r'\1', text).split())

def main():
    output=ROOT/'whole_article_comparisons_v1.json';binding_path=ROOT/'native_UI_terms_andfour_limits_v1.json'
    assert not output.exists() and not binding_path.exists()
    draft_path=ROOT/'clean_meanings_andfull_drafts_v1.json';packet_path=ROOT/'current_full_articles_verified_parent_v1.json'
    draft,packet=map(load,[draft_path,packet_path]);assert len(draft['records'])==len(packet['records'])==37
    im=NdsImage.open(packet['current_ROM']);arm=im.read_file('/__arm9__.bin')
    clean=NdsImage.open('work/clean.nds');jp=clean.read_file('/__arm9__.bin')
    assert sha(Path(packet['current_ROM']).read_bytes())==packet['current_ROM_sha256']
    slots=[(0x144754,'修理','Repair'),(0x14475c,'改造','Remodel'),(0x144764,'売却','Sell'),
      (0x14476c,'購入','Buy'),(0x144774,'ドック','Dock'),(0x144784,'特別注文','Special'),
      (0x144790,'装備変更','Equipment'),(0x14479c,'船名変更','Rename'),(0x1447a8,'標準船体','Standard'),
      (0x143c18,'隊列変更','Arrange'),(0x143c30,'艦長任命','Captain'),(0x143c3c,'地方艦隊作成','Create Fleet'),
      (0x143c4c,'地方艦隊編成','    Fleet Setup'),(0x143c5c,'船の入れ替え','Swap Ships'),(0x143c6c,'地方艦隊解散','Disband'),
      (0x144644,'出港','Depart'),(0x144654,'洋上へ','Sail'),(0x14469c,'甲板画面','Deck View'),
      (0x1446a8,'自動移動','Auto Move'),(0x1446b4,'積み荷編成','Cargo Setup'),
      (0x12ff50,'個室','Cabin'),(0x12ff58,'舵輪','Helm'),(0x12ff68,'測量','Survey'),
      (0x12ff70,'甲板','Deck'),(0x12ffa8,'マスト','Mast'),(0x12ffb0,'漕手室','Rowers'),
      (0x12ffd8,'副官室','Mate'),(0x12ffe0,'艦長室','Captain'),(0x12ffe8,'見張台','Lookout'),
      (0x12fff0,'積荷倉庫','Cargo'),(0x12fffc,'海兵詰所','Quarters'),(0x130008,'武装砲台','Battery'),(0x130014,'物資倉庫','Supplies')]
    labels=[]
    for offset,japanese,english in slots:
        a=arm[offset:].split(b'\0')[0];s=jp[offset:].split(b'\0')[0]
        assert a==english.encode('ascii') and s==japanese.encode('cp932'),(hex(offset),a,s)
        labels.append(dict(file_path='/__arm9__.bin',offset=offset,source_hex=s.hex(),current_hex=a.hex(),Japanese=japanese,English=english,scope='stored native label binding, not new command activation'))
    code=MainCodeFile(arm,0x02000000)
    def string(at):
        for section in code.sections:
            off=at-section.ramAddress
            if 0<=off<len(section.data):return bytes(section.data[off:]).split(b'\0')[0]
        raise AssertionError(hex(at))
    for field,japanese,english in [(0x119a40,'海域委任','Manage Area'),(0x119a50,'哨戒','Patrol'),(0x119a60,'寄港','Dock'),(0x119a70,'街攻撃','Attack Town')]:
        pointer=struct.unpack_from('<I',arm,field)[0];original=struct.unpack_from('<I',jp,field)[0]
        assert string(pointer)==english.encode('ascii') and jp[original-0x2000000:].split(b'\0')[0]==japanese.encode('cp932')
        labels.append(dict(file_path='/__arm9__.bin',pointer_field=field,source_pointer=original,current_pointer=pointer,Japanese=japanese,English=english,scope='stored native policy pointer and label, not new fleet activation'))
    for address,japanese,english in [(0x02133224,'ジガースパンカー','Jigger Spanker'),(0x02133234,'スプリットセイル','Spritsail')]:
        assert string(address)==english.encode('ascii') and japanese.encode('cp932')+b'\0' in jp
        labels.append(dict(file_path='/__arm9__.bin',current_address=address,source_Japanese=japanese,English=english,scope='current exact caption; spritsail contextual inference retained from approved source review'))
    prior_path=Path('translations/refit_contextual_final_review_v1.json');prior=load(prior_path)
    from dk4tool.script.common_message_table import common_message_entries
    from dk4tool.formats.ilnk import IlnkContainer
    source_entries=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),jp)
    blocks=IlnkContainer.parse(im.read_file('/COMMON/MESFILE.DK4')).blocks;limits=[]
    for n in [1275,1276,1278]:
        row=next(r for r in prior['records'] if r['message_id']==n)
        assert row['source_hex']==source_entries[n].text.hex() and all(row['review'].values())
        raw=bytes.fromhex(row['integrated_hex']);hits=[(i,block.find(raw)) for i,block in enumerate(blocks) if raw in block]
        assert len(hits)==1
        limits.append(dict(message_id=n,source_reference=row['source_reference'],source_hex=row['source_hex'],source_Japanese=row['source_Japanese'],current_block=hits[0][0],current_block_offset=hits[0][1],current_hex=raw.hex(),retained_English=row['english'],scope='exact stored source/current evidence for per-type limits, no new native gameplay limit test'))
    role_path=Path('work/analysis/refit_context_v2274/native_context.json');role=load(role_path)['role']
    assert role['role']==13 and role['Japanese']=='船大工' and role['English']=='Shipwright'
    assert any(b'Shipwright\0' in bytes(s.data) for s in code.sections)
    save(binding_path,dict(current_ROM=packet['current_ROM'],current_ROM_sha256=packet['current_ROM_sha256'],current_ARM9_sha256=sha(arm),labels=labels,
        source_COMMON_per_type_limits=limits,prior_approved_review=str(prior_path),prior_approved_review_sha256=sha(prior_path.read_bytes()),
        approved_Shipwright_role=role,approved_Shipwright_role_proof=str(role_path),approved_Shipwright_role_proof_sha256=sha(role_path.read_bytes()),
        source51_physical_cycle_andexecute_buttons_pending=True,all_current_labels_offline_only=True,new_credit=0,producer_sha256=sha(Path(__file__).read_bytes())))
    records=[]
    for original,current,title in zip(draft['records'],packet['records'],HEADINGS,strict=True):
        n=original['topic_id'];assert n==current['topic_id'] and original['source_hex']==current['source_hex']
        english=(REVISIONS|RETENTIONS)[n];ids=[int(x) for x in re.findall(r'\[\[(\d+)\|',english)]
        assert ids==original['original_link_IDs'],(n,ids,original['original_link_IDs'])
        assert '\n' not in english and english.isascii()
        retain=n in RETENTIONS
        if retain:
            body=current['current_English_with_link_IDs'].split('\n',1)[1]
            assert plain(english)==plain(body),(n,plain(english),plain(body))
        records.append(dict(id=original['id'],topic_id=n,file_path='/COMMON/HELP.DK4',source_reference=original['source_reference'],source_hex=original['source_hex'],
          source_meaning=original['clean_meaning'],source_Japanese_with_link_IDs=original['source_Japanese_with_link_IDs'],
          current_reference=current['current_reference'],current_hex=current['current_hex'],current_English=current['current_English_with_link_IDs'],
          original_link_IDs=ids,complete_current_continuations=[],title=title,english=english,
          decision='retain-wording' if retain else 'revision',finding=FINDINGS[n],retention_reason=FINDINGS[n] if retain else None,
          localization_note=FINDINGS[n],speaker='Help narrator',context='Read as a complete connected Shipyard/Remodel/Dock/Port/Ruins help exchange; all original destinations and source neighbors44 through80 reviewed together.',
          review=dict(source=True,context=True,localization=n!=51,naturalness=True,formatting=False),
          native_term_orcontrol_binding_pending=n==51,fresh_display_allocation_widgets_andintegration_pending=True,new_credit=0))
    save(output,dict(records=records,records_count=37,proposed_revisions=27,justified_retentions=10,first_four_gates_passed=36,pending_localization_binding_topic_IDs=[51],
      all_fifth_gates_pending=True,translation_policy='natural-dialogue-v2',target_locale='en-US',current_ROM=packet['current_ROM'],current_ROM_sha256=packet['current_ROM_sha256'],
      ten_body_retentions_word_exact_after_removing_old_wraps_andrestoring_link_markup=True,retained_bodies_may_receive_separate_source_bound_title_andlink_formatting_changes=True,
      source_draft=str(draft_path),source_draft_sha256=sha(draft_path.read_bytes()),current_packet=str(packet_path),current_packet_sha256=sha(packet_path.read_bytes()),
      term_binding=str(binding_path),term_binding_sha256=sha(binding_path.read_bytes()),source51_provisional_generic_buttons_must_not_ship=True,
      no_new_gameplay_orcompletion_claim=True,new_credit=0,registered_integration_pending=True,producer_sha256=sha(Path(__file__).read_bytes())))
    print('37 comparisons saved:27 revisions/10 word-exact body retentions;36 four-gate passes,51 input binding pending;all formatting pending,no credit.')

if __name__=='__main__':main()
