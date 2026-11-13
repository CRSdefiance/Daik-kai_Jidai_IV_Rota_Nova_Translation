"""Fresh whole-consumer source review; formatting and integration remain pending."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.refit_help import compile_paragraph
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.town_trade_port_contextual_reference_v1 import current_entries
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/refit_editorial_context_v2277')
DOC=Path('translations/refit_contextual_editorial_manuscript_v1.json')
PACKET=Path('work/analysis/refit_context_source_v2272/all43_clean_current_context_catalog.json')
# Each gloss and retention/revision rationale was written after reading the clean
# Japanese and the complete room/equipment or helper/merchant interaction.
NOTES={
1247:('Officers present recover physical condition and mood.','Here clearly identifies the selected room; health and morale retain both benefits and officers remains distinct from sailors.'),
1248:('A ship carpenter enables repairs when a ship is damaged.','The short complete sentence states the conditional repair capability without promising a rate, prevention, or free repairs.'),
1249:('A ship doctor can cure abnormal conditions affecting officers and sailors.','Ailments is natural help prose and preserves both affected groups and the cure rather than mere prevention.'),
1250:('A chief cook reduces food and water consumption and slows sailor fatigue.','Conserves and tire more slowly express the two effects accurately. The sentence does not turn reduced fatigue accumulation into recovery.'),
1251:('Officers here recover mood and make sailors fatigue more slowly.','The two clauses keep officers as the room occupants and sailors as the beneficiaries of slower fatigue. Morale matches1247.'),
1252:('An animal keeper reduces food consumption.','Food supplies last longer preserves the effect naturally; water is deliberately absent because the source names food alone.'),
1253:('A missionary relieves sailor discontent and enables distribution of trade goods in the square.','The coordinated sentence preserves both the onboard benefit and separate Square action without inventing conversions or religious rewards.'),
1254:('A strategist enables schemes in the tavern.','Plan schemes at the tavern is idiomatic and names the actual facility and capability without guaranteeing success.'),
1255:('A purser enables price bargaining and buying up goods.','Corner markets retains the established action wording for buying up stock. The paired capabilities do not promise profits or permanent market control.'),
1256:('A polite helper addresses the Admiral and offers to help with the refit too.','The polite direct offer and too work as the opening of the helper then merchant exchange; Admiral is explicit in the source.'),
1257:('A familiar confident helper addresses the Admiral and offers their own help with the refit.','I is the source first-person pronoun IC, not a substituted character name. The contraction-free can help and exclamation preserve the confident voice.'),
1258:('A helper addresses the Admiral and asks to be allowed to assist with the refit.','Let me help retains the request to participate instead of changing it into an order or a completed action.'),
1259:('A rough, assured helper says they will lend a hand too, addressing the Admiral.','Lend a hand and the final address give the brief source offer an informal assured voice without an invented rank or relationship.'),
1260:('A measured older-sounding helper addresses the Admiral and offers assistance with the refit too.','The full with the refit clause gives this measured offer its own cadence. No literal old-man address or family relationship is introduced.'),
1261:('An eager helper addresses the Admiral and offers to help refit the ship too.','The lively exclamation preserves eagerness. Her conventionally refers to the ship, not the helper, and invents no character gender.'),
1262:('A hesitant helper addresses the Admiral and suggests they could also assist with the refit.','Could and the trailing ellipsis preserve the hesitation within the surrounding offer sequence.'),
1263:('The local shipwright offers a supplied percentage reduction thanks to the helper, then considers the price.','With their help links the companion offer to the merchant discount naturally. The single numeric string and escaped literal percent remain intact; the separate final-price confirmation1246 is not folded into this line.'),
1264:('The local shipwright asks which ship is to be renamed.','The courteous complete question naturally introduces ship selection; it does not presume a selection or successful rename.'),
1265:('The local shipwright invites the player to choose a preferred ship name.','Any name you like is ordinary conversational encouragement before the existing constrained keyboard. It makes no technical promise of unlimited input length.'),
1266:('The local shipwright asks which ship is to be refitted.','The parallel courteous question matches the rename interaction while distinguishing refit from rename.'),
1267:('The local shipwright states the supplied refit duration in days.','The original argument now includes the native number and singular or plural day unit. The sentence takes exactly one string, adds no second unit, and remains natural for all duration bytes.'),
1268:('Installing the named bow sail improves square-sail performance and speed with a following wind.','Revise split sail to spritsail: the clean bow-fitting context1280 and primary maritime terminology identify the period square sail under the bowsprit. Preserve both performance and following-wind effect; this is a contextual English terminology inference, not a claim of official English localization.'),
1269:('A jigger spanker improves fore-and-aft performance and speed in an adverse wind.','The retained term matches the component label; against the wind contrasts clearly with the following-wind square-sail effects without promising direct upwind sailing.'),
1270:('Additional armor improves durability but slightly reduces speed.','The complete contrast preserves the benefit and the slight speed penalty without inventing an amount.'),
1271:('Additional armor2 further improves durability but slightly reduces speed.','Further and Extra Armor2 distinguish the second option while preserving the same stated speed drawback.'),
1272:('A bow gun enables forward fire but has weak attack power.','Ahead and weak shots preserve direction and low power, keeping this drawback distinct from the stern gun accuracy drawback.'),
1273:('A stern gun enables rearward fire but has poor accuracy.','Behind and inaccurate shots retain the correct direction and accuracy limitation; this is not changed to weak damage.'),
1274:('With a ram, the ship can attack by striking an enemy ship in the side.','The sentence explicitly requires a ram and keeps the side-impact condition rather than broadening the attack to any collision.'),
1275:('A marine captain improves boarding attack power; up to four of this room can be added.','The two sentences separate the assigned-officer benefit from the limit on rooms of this type. Four is not generalized to all rooms.'),
1276:('A gunner enables faster cannon fire; up to four of this room can be added.','Speeds up cannon fire preserves firing rate rather than damage. These rooms correctly scopes the four-room limit.'),
1277:('This room stores the ship food and water.','Holds is a natural storage verb and retains both supplies without inventing a consumption benefit.'),
1278:('Cargo holds store trade goods and up to five holds may be added.','The two short complete sentences preserve the distinct cargo type and five-hold capacity, separate from four combat rooms.'),
1279:('A cargo hold can be installed here but slightly lowers speed.','The location refers to the selected slot. The slight speed cost remains explicit and is not applied to every room.'),
1280:('A ram or bow gun can be fitted here, and medium or larger ships can additionally fit the named bow sail.','Revise split sail to spritsail consistently with1268 and the component label. Medium and larger retains the lower size threshold; or preserves alternative fittings instead of promising simultaneous installation.'),
1281:('Additional armor can be fitted here.','The brief complete instruction is appropriate for a selected fitting slot; no extra benefit or size requirement is invented.'),
1282:('A stern gun can be fitted here, or a jigger spanker on a large ship.','Or preserves the alternatives; on large ships qualifies the jigger spanker and is not widened to medium ships like1280.'),
1283:('An owned figurehead can be mounted here.','You own retains the possession requirement. Mount is natural nautical fitting language.'),
1284:('The type of cannon aboard the ship can be changed here.','Change the cannon type preserves replacement choice rather than adding cannons or guaranteeing an upgrade.'),
1285:('Lateen sails perform well in adverse winds, and square sails cannot be placed behind them.','The two complete sentences preserve the wind advantage and direction-specific incompatibility. Read with1287, behind and ahead are reciprocal rather than reversed.'),
1286:('A topsail improves square-sail performance and following-wind speed.','The same performance wording as1268 makes the shared effect clear while retaining the distinct sail type.'),
1287:('Square sails perform well with a following wind, and a lateen sail cannot be placed ahead of one.','The reciprocal restriction agrees with1285. Following wind remains distinct from the fore-and-aft sail advantages.'),
1288:('A staysail improves fore-and-aft performance and speed in adverse winds.','The parallel wording to1269 preserves the same kind of performance benefit without confusing the two different fittings.'),
1289:('This square sail improves both fore-and-aft and square-sail performance.','The explicit both retains the unusual dual performance benefit while still identifying the fitting as a square sail.'),
}

def main():
 assert not ROOT.exists()and not DOC.exists();ROOT.mkdir(parents=True)
 packet=read(PACKET);rom=NdsImage.open(packet['current_ROM']);arm=rom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4');entries=current_entries(common,arm)
 old_paths=['translations/refit_help_editorial_manuscript_v3.json','translations/refit_dialogue_editorial_manuscript_v2.json'];old={r['message_id']:r for p in old_paths for r in read(p)['records']}
 assert set(NOTES)==set(range(1247,1290));rows=[]
 for c in packet['records']:
  n=c['message_ID'];prior=old[n];help_record=n not in range(1256,1268);english=prior['english'];changed=n in(1268,1280)
  assert (compile_paragraph(english)[0][:-1]if help_record else b' '+english.encode())==entries[n].text==bytes.fromhex(c['current_hex'])
  if changed:english=english.replace('split sail','spritsail')
  gloss,reason=NOTES[n]
  row=dict(id=f'COMMON_MESSAGE_{n}',message_id=n,file_path=c['file_path'],source_hex=c['source_hex'],source_Japanese=c['clean_Japanese'],source_reference=c['source_reference'],current_hex=c['current_hex'],current_reference=c['current_reference'],current_stored_English=c['current_stored_English'],english=english,source_meaning=gloss,localization_note=reason,speaker=prior['speaker'],context=('Selected Refit help slot; own168x84 visible help painter,168x108 allocation,generated27-column pair-safe lines and no authored layout.'if help_record else prior['context']),consumer='refit-help27-pair-safe-v1'if help_record else'refit-queued-or-direct-common228x48',editorial_decision='revise'if changed else'retain-wording',fresh_retained_wording_justification=None if changed else reason,review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False))
  if not help_record:
   for k in('native_argument_count','argument_contract','source_voice_classes'):
    if k in prior:row[k]=deepcopy(prior[k])
  rows.append(row)
 clean_arm=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');offset=0x133234;before=arm[offset:offset+12];after=b'Spritsail\0\0\0'
 assert before==b'Split Sail\0\0'and len(before)==len(after)==12
 term=dict(clean_source_label='スプリットセイル',clean_ARM9_offset=0x13322C,clean_hex=clean_arm[0x13322C:0x133240].hex(),current_ARM9_offset=offset,current_hex=before.hex(),proposed='Spritsail',target_hex=after.hex(),COMMON_IDs=[1268,1280],primary_sources=[dict(url='https://www.gamecity.ne.jp/manual/dk4HeN38/jp/3400.html',use='Publisher Japanese manual identifies the named fitting as bow equipment and describes the following-wind benefit; HD manual is supporting context, not a replacement for clean DS source.'),dict(url='https://www.nationalhistoricships.org.uk/sites/default/files/2023-02/c_fittings.compressed.pdf',page=97,use='Manual of Maritime Curatorship identifies a spritsail under the bowsprit on late sixteenth-century ships.')],decision='Contextual inference from the clean Japanese bow-fitting description and primary maritime terminology. English spritsail, not a literal split sail. No claim of publisher-approved English localization.',auxiliary_label_not_extra_COMMON_credit=True,formatting_and_runtime_label_binding_pending=True)
 save(ROOT/'spritsail_source_decision.json',term)
 doc=dict(format='dk4-refit-contextual-manuscript-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],source_ROM_sha256=packet['source_ROM_sha256'],current_ROM=packet['current_ROM'],current_candidate_sha256=packet['current_ROM_sha256'],current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(common),file_path='/COMMON/MESFILE.DK4',source_context_packet=str(PACKET),source_context_packet_sha256=sha(PACKET.read_bytes()),native_context_proof='work/analysis/refit_context_v2274/native_context.json',native_context_proof_sha256=sha(Path('work/analysis/refit_context_v2274/native_context.json').read_bytes()),conversation_groups=[dict(kind='room roles and effects',IDs=list(range(1247,1256))),dict(kind='assigned Shipwright offer then local merchant discount then separate1246price',IDs=list(range(1256,1264)),context_only_already_fresh_IDs=[1246]),dict(kind='rename selection encouragement and constrained keyboard',IDs=[1264,1265]),dict(kind='refit selection and native day-unit duration',IDs=[1266,1267]),dict(kind='equipment performance and selected-slot restrictions',IDs=list(range(1268,1290)))],revised_IDs=[1268,1280],retained_count=41,formatting_review_pending=True,auxiliary_terminology_decision=str(ROOT/'spritsail_source_decision.json'),prior_manuscripts_preserved={p:sha(Path(p).read_bytes())for p in old_paths},records=rows,completion_credit_pending=True,full_goal_complete=False)
 save(DOC,doc)
 save(ROOT/'review_receipt.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),clean_current_records_read=43,individual_retention_reasons=41,proposed_COMMON_revisions=2,auxiliary_ARM9_label_revision=1,formatting_integration_and_revised_gameplay_pending=True,zero_new_completion_credit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print(dict(records=43,retentions=41,revisions=2,auxiliary_label=1,formatting_pending=True))

if __name__=='__main__':main()
