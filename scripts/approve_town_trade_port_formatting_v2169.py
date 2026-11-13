"""Offline formatting approval; actual revised release remains pending."""
from pathlib import Path
from copy import deepcopy
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
root=Path('work/analysis/town_trade_port_formatting_v2169');docpath=Path('translations/town_trade_port_contextual_editorial_manuscript_v2.json');oldpath=Path('translations/town_trade_port_contextual_editorial_manuscript_v1.json')
assert not root.exists()and not docpath.exists();root.mkdir(parents=True)
paths=['work/analysis/town_trade_port_payload_v2165/native_payload_plan.json','work/analysis/town_trend_runtime_v2162/runtime_plan.json','work/analysis/town_trend_selector_v2164/all_eight_parent_lowword_fullword_stack_and_R2_ABI.json','work/analysis/town_trend_references_v2166/all_unit_references_and_ARMv5_instruction_audit.json','work/analysis/town_trade_port_fonts_v2167/all_native_layout_inheritance_and_full_font_samples.json','work/analysis/town_trade_port_copies_v2168/all_native_copies_and_prefix_cache_sequence.json','work/analysis/yard_modal_actual_verification_v2158/actual267_native_geometry_direct_font_and_foreground.json','work/analysis/town_trend_balanced_layouts_v2163/all248_revised_product_layouts.json']
proofs=list(map(read,paths));fonts=proofs[4]
assert proofs[2]['total_cases']==1057968 and fonts['full_font_count']==203 and len(fonts['physical_sheets'])==17 and len(fonts['all60_nonmodal_message_IDs_covered'])==60 and proofs[5]['complete_native_copies']==7336 and len(proofs[5]['sequenced_cache_cases'])==180 and proofs[6]['actual_bounds']==[0,0,228,48]and proofs[7]['count']==248
assert all(not r['findings']for r in fonts['all32552_layouts'])
doc=deepcopy(read(oldpath));assert len(doc['records'])==61
doc.update(supersedes_manuscript=str(oldpath),English_bodies_identical_to_v1=True,formatting_review_pending=False,consumer_layout_profile='common-source-parents-balanced654655-production228x48-four12rows-physical16pitch-direct267-x0',offline_formatting_complete_revised_actual_and_registered_release_pending=True,final_research_payload=paths[0],source_owned_runtime=paths[1],native_font_proof=paths[4],no_geometry_or_font_change=True)
for row in doc['records']:
 row['review']['formatting']=True;row['status']='offline-formatting-approved-revised-actual-and-registered-release-pending'
 row['formatting_gate_scope']='Native fullbytes/guards/orderedglyphs/first-lastletters/bounds/pagination at228x48logical/6x12metrics. Separate physical16pitchoracle. All203planes viewed.'
 if row['message_id']==267:row['formatting_gate_scope']='Actual direct systemfont228x48,x0;complete native continuation andactualforeground verified.240wasanofflinecanvas,notviewgeometry.'
 if row['message_id']in(654,655):row['wrap_findings_resolution']='Existingbalancedliteralpath handlesall124products throughsource-guarded selector;reviewedEnglishunchanged.All220stylefindingsresolved,nowaivers.'
validate_natural_dialogue_batch(doc);save(docpath,doc)
save(root/'offline_formatting_approval.json',dict(manuscript=str(docpath),manuscript_sha256=sha(docpath.read_bytes()),English_identical_to_v1=True,records=61,revised_IDs=[654,655],justified_retentions=59,all203_native_physical_planes_on17sheets_viewed=True,actual_current267_full_hold_viewed=True,all248revisedproductlayouts_no_style_findings_or_waivers=True,all203sample_layouts_freshlyexecuted_oncombined_target=True,production_logical_four12rows_notphysical16pitch_capacity=True,registered_release_and_revised_trend_actual_pending=True,evidence={p:sha(Path(p).read_bytes())for p in paths+[str(oldpath),str(docpath)]},producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(offline_records=61,planes_viewed=203,sheets=17,style_findings=0,actual_and_release_pending=True))
