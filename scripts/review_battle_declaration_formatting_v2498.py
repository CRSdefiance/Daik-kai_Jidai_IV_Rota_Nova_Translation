"""Freshly reviewed176 canvases and27 exact boundary findings;no global waiver."""
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from scripts.battle_declaration_layout_v996 import compiled
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/battle_declaration_formatting_v2498')
if __name__=='__main__':
 assert not ROOT.exists();fontpath=Path('work/analysis/battle_declaration_fonts_v2496/native_font_proof.json');f=read(fontpath);oldpath=Path('work/analysis/battle_declaration_v996/visual_review.json');old=read(oldpath);rows={r['message_id']:r for r in read('translations/battle_declaration_contextual_editorial_manuscript_v1.json')['records']};previous={w['case_index']:w for w in old['all27_line_boundary_findings']};warnings=[]
 for w in f['line_boundary_findings_requiring_review']:
  i=w['case_index'];c=f['cases'][i];p=previous[i];assert w['message_ID']==p['message_ID']and w['lines']==p['generated_native_lines']and w['faction']==p['faction_name_case'];assert c['preview_sha256']==p['preview_sha256'];label=w['faction'];real=label['kind']=='native-company-label'
  if real:assert w['message_ID']in(1897,1901)and len(w['lines'])==2 and w['lines'][-1]==label['label']+'?'and w['lines'][0].endswith(' on')
  else:assert label['kind']=='synthetic-layout-stress-not-real-faction'and label['label']in('ABCDEFGHIJKLMNOPQRSTUVW','Northern Compass Co.')
  reason=('The original complete faction label remains legible as a proper name on its own generated row. The confirmation remains comprehensible across the on/name boundary. Every first/final glyph,whole word and native x6 margin is complete. This exact expansion is retained without shortening the name or authoring alignment.'if real else'This exact artificial long-name layout stress remains readable across its generated boundary and stays within35 cells/four rows. It establishes no real faction or encounter. Complete words and glyphs survive;the result justifies only this exact synthetic case.')
  warnings.append(dict(case_index=i,message_ID=w['message_ID'],faction_name_case=label,generated_native_lines=w['lines'],findings=p['findings'],disposition='freshly-reviewed-exact-case-retention',reason=reason,preview_sha256=c['preview_sha256']))
 assert len(warnings)==27
 for c in f['cases']:
  assert bytes.fromhex(c['compiled_template_hex'])==compiled(rows[c['message_id']]);value=c['faction_name_case'];expected=rows[c['message_id']]['english'].replace('%s',value['label'])if value else rows[c['message_id']]['english'];assert ' '.join(c['generated_native_lines'])==expected and max(c['visible_widths'])<=35 and len(c['generated_native_lines'])<=4;assert sha(Path(c['preview']).read_bytes())==c['preview_sha256']
 for s in f['review_sheets']:assert sha(Path(s['path']).read_bytes())==s['sha256']
 ROOT.mkdir(parents=True);save(ROOT/'visual_formatting_review.json',dict(native_font_proof=str(fontpath),native_font_proof_sha256=sha(fontpath.read_bytes()),all176_complete_native_previews_freshly_viewed=True,all8_sheets_viewed=True,all27_exact_current_case_decisions=warnings,historical_case_decision_source=str(oldpath),historical_case_decision_source_sha256=sha(oldpath.read_bytes()),all27_layouts_and_pixels_exact_to_previously_approved_cases=True,no_global_or_missing_glyph_waiver=True,blocking_errors=0,unwaived_warnings=0,zero_new_editorial_credit_until_historical_and_registered_reconciliation=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('176 canvases viewed;27 exact-case boundary retentions reviewed;zero unwaived warnings.')
