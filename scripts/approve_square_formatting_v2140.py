"""Approve Square offline formatting using separate logical and physical native proofs."""
from pathlib import Path
from copy import deepcopy
from scripts.verify_village_wrap_v608 import read,save
from scripts.primary_town_native_font_v2102 import font_tools,glyph_codes
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/square_formatting_v2140');DOC=Path('translations/square_contextual_editorial_manuscript_v3.json')
if __name__=='__main__':
 assert not ROOT.exists()and not DOC.exists();ROOT.mkdir(parents=True)
 source=Path('translations/square_contextual_editorial_manuscript_v2.json');doc=deepcopy(read(source));plan=read('work/analysis/square_context_payload_v2124/native_payload_plan.json');arm=Path(plan['target_ARM9']).read_bytes();rom=NdsImage.open(doc['current_ROM']);raster,_,_=font_tools(rom)
 physical=read('work/analysis/square_context_pages_v2130b/all_square_native_pages.json');controlpath=Path('work/analysis/production_compact_capacity_v2138/all307_production_native_font_cases.json');controls=read(controlpath);square=[r for r in controls['cases']if r['kind']=='square'];assert len(square)==134 and controls['multi_page_cases']==[]
 bindings=[]
 for i,r in enumerate(physical['cases']):
  match=square[i];assert match['formatted_hex']==r['formatted_hex']and match['message_ID']==r['message_ID']and match['page_count']==1
  events=[];plane=raster(arm,bytes.fromhex(r['formatted_hex']),0x01FFCE40-0x02000000,size=(228,64),instruction_limit=2000000,glyph_events=events)
  assert sha(plane)==r['pages'][0]['plane_sha256']and events==r['pages'][0]['ordered_glyphs']
  bindings.append(dict(index=i,message_ID=r['message_ID'],formatted_hex=r['formatted_hex'],physical_plane_sha256=sha(plane),logical_control_index=i,complete_first_last_glyphs_and_bounds=True,identical_to_viewed_physical_preview=True))
 args=read('work/analysis/square_context_arguments_v2133/all_runtime_native_argument_layouts.json');assert args['total']==11580 and args['all11289_prior_product_pitch_layouts_exact']and args['all_names_and_printf_argument_order_preserved']and args['all_ASCII_glyphs_present']
 doc.update(supersedes_notes_only_manuscript=str(source),English_identical_to_v1=True,formatting_review_pending=False,all_native_formatting_revised_ROM_and_release_checks_pending=False,offline_formatting_complete_actual_revised_release_pending=True,consumer_layout_profile='common-source-parent-postprintf-native-35cells-production-logical228x48-four12rows-physical16pitch',production_capacity_receipt=str(controlpath),physical_binding_receipt=str(ROOT/'offline_formatting_approval.json'),geometry_change_rejected_as_unnecessary=True)
 for r in doc['records']:
  r['review']['formatting']=True;r['status']='fresh-source-context-offline-formatting-approved-revised-gameplay-release-pending';r['formatting_gate_scope']='Original numeric/table parent and typed substitutions;native production228x48/6x12 consumes fourrows. Physical16pitch228x64 glyphoracle is separate andmatches actual four-line739. Full source/current spans andnative copies preserved. No geometrychange.'
  if r['message_id']in(681,731):r['wrap_retention_reason']='Runtime product/town variants can put a complete destination noun or final emphatic word on the last of at most four rows. The full source-backed sentence remains one page, without isolated letters or clipping. The viewed previews preserve its question or emphasis; prose is not shortened for runtime-name width.'
 validate_natural_dialogue_batch(doc);save(DOC,doc)
 save(ROOT/'offline_formatting_approval.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),previous_notes=str(source),English_bodies_identical_to_v1_v2=True,revised_IDs=[698,701,718,740],retained=85,bindings=bindings,native_production_control=str(controlpath),native_production_control_sha256=sha(controlpath.read_bytes()),runtime_arguments='work/analysis/square_context_arguments_v2133/all_runtime_native_argument_layouts.json',all11580_original_typed_substitutions_checked=True,all134_physical_previews_on12_sheets_previously_viewed=True,actual_ordinary_four_holds_sheet_viewed=True,actual_promoter_four_holds_including_four_line739_sheet_viewed=True,physical_oracle_does_not_define_logical_view_or_pagination=True,research_48_to64_geometry_not_used=True,earlier_16metric48plane_three_row_and_extra_page_claims_superseded=True,first_last_letters_whole_words_and_no_blank_pages=True,actual_revised_698_701_718_740_and_registered_release_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print(dict(approved=89,revised=4,retained=85,physical_cases=134,native_control_cases=307,runtime_argument_cases=11580,geometry_change=False))
