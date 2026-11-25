"""Individual source/context and visual decisions for ten native wrap findings."""
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/town_services_style_v2091')
DOC=Path('translations/primary_town_services_contextual_editorial_manuscript_v4.json')
REASONS={
25:'Retain the energetic request for a small price concession. The native break after on separates a preposition from its object but all words remain adjacent on two complete rows; it creates no authored pause or ambiguity. Replacing the idiomatic little break solely for line shape would lose the existing bargaining voice.',
38:'Retain the already-natural warning. Admiral is the source-supported direct address, and its complete final-row vocative remains clear after the supply warning. No relationship or title was added for layout. This is a ten-character word with punctuation, not a dropped letter or an extra page.',
46:'Retain the measured question about taking too few supplies. The complete final noun supplies is clearly governed by too few on the preceding row. Preserve the source distinction from warnings about imminent exhaustion; the nine-character final word is not clipped.',
47:'Retain both source questions: the childish personal food concern followed by the low-supply concern. The final supplies question remains complete on row three. The soft break after on does not separate speakers or create a dramatic pause. Native execution proves the literal I survives expansion before wrapping.',
48:'Retain the thoughtful existing Hmm and measured observation of low supplies. The automatic on/supplies break remains an ordinary continuation within one two-row panel. Shortening or strengthening the observation for appearance would change its established voice or urgency.',
69:'Retain the casual port-stop question and the full approved town name. With Constantinople the complete port question occupies row two. The source explicitly mentions the port, so removing it or shortening the town solely to avoid a short row would discard meaning. The whole two-row prompt is visible before the decision.',
71:'Retain the polite all right confirmation and number-neutral of our sailors. Only the supplied ten-fullwidth-digit stress amount leaves the complete predicate unassigned on row three. All eleven characters and the question mark remain visible in one panel; no dismissal or reassignment is implied.',
74:'Retain the casual okay confirmation, distinct from the polite and formal alternatives. The ten-fullwidth-digit stress substitution places the complete unassigned question on row three, without splitting a word or adding a page. Preserve singular/plural-safe grammar rather than rewriting for this supplied stress string.',
75:'Retain the mature formal approval request, distinct from the all right and okay voices. With the ten-fullwidth-digit stress value, unassigned completes the question on row three. It remains fully visible and semantically connected; no commander title or action is invented to shorten it.',
81:'Retain the older presenter urging acceptance of incoming tribute. Go on is a complete interjection translating the source urging, not a dangling preposition. The comma at the automatic row end naturally leads to please accept it on the next row. The weak-on heuristic is a false positive for this exact phrase.'}
if __name__=='__main__':
 assert not ROOT.exists()and not DOC.exists();ROOT.mkdir(parents=True)
 prior=Path('translations/primary_town_services_contextual_editorial_manuscript_v3.json');doc=read(prior);visual=read('work/analysis/town_services_visual_v2090/name_native_planes_and_style_sheet.json');assert sha(Path(visual['style_sheet']).read_bytes())==visual['style_sheet_sha256']
 rows={r['message_id']:r for r in doc['records']};decisions=[]
 for case in visual['style_cases']:
  n=case['message_ID'];r=rows[n];reason=REASONS[n]
  decisions.append(dict(message_ID=n,source_reference=r['source_reference'],current_reference=r['current_reference'],source_hex=r['source_hex'],source_Japanese=r['source_Japanese'],source_meaning=r['source_meaning'],full_exchange_native_IDs=r['full_exchange_native_IDs'],english=r['english'],supplied_arguments=case['supplied_arguments'],native_lines=case['lines'],findings=case['findings'],decision='retain-wording-and-native-soft-wrap',reason=reason,source_preview=case['source_preview'],source_preview_sha256=case['source_preview_sha256'],source_bound_full_native_plane_pass=True,hard_bounds_glyphs_and_pagination_not_waived=True))
  r['qa_waivers']=sorted(set(r.get('qa_waivers',[]))|set(case['findings'])|({'orphan-final-line'}if len(case['lines'][-1])<=8 else set()))
  r['qa_waiver_reason']=reason;r['native_wrap_style_review']=str(ROOT/'individual_ten_style_retention_decisions.json')
 assert len(decisions)==10 and set(REASONS)=={r['message_ID']for r in decisions}
 save(ROOT/'individual_ten_style_retention_decisions.json',dict(manuscript_source=str(prior),source_sha256=sha(prior.read_bytes()),decisions=decisions,style_sheet=visual['style_sheet'],style_sheet_sha256=visual['style_sheet_sha256'],all_ten_native_previews_viewed=True,all_source_context_and_generated_line_boundaries_reviewed=True,no_English_or_authored_line_breaks_changed=True,no_hard_font_gate_waived=True,remaining_repack_revised_actual_and_registered_release=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 doc['native_wrap_style_review']=str(ROOT/'individual_ten_style_retention_decisions.json');doc['supersedes_notes_only_manuscript']=str(prior)
 assert [r['english']for r in doc['records']]==[r['english']for r in read(prior)['records']]and all(not r['review']['formatting']for r in doc['records'])
 save(DOC,doc);print(dict(manuscript=str(DOC),individual_style_cases=10,English_unchanged=True,formatting_release_gate_still_pending=True))
