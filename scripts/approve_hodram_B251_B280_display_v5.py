"""Approve the directly viewed native pages and bridge exact compounds to storage."""
import inspect
from scripts import approve_hodram_B231_B250_display_v2 as previous
from scripts.prepare_hodram_B251_B280_formatting_v1 import ROOT,FORMATTING as DOC
from scripts.review_hodram_B251_B280_contextual_v1 import CURRENT
from scripts.source_locked_derivation_v5118 import checked_text

INITIAL=ROOT/'formatting_v1/FE_plan_v2/automatic_plans.json';INITIAL_VIEW=ROOT/'initial_visual_review_v2.json'
PLAN=ROOT/'formatting_v1/visual_plan_v5/automatic_plans.json';NATIVE=ROOT/'final_native_v5/compiled_native_pages.json'
STYLES=ROOT/'native_objects_v1/styles/compiled_style_objects.json';VIEW=ROOT/'final_visual_approval_v5.json';OUT=ROOT/'storage_inputs_v5'
source=checked_text(inspect.getsource(previous.main),{
    "ROOT/'layout_delta_v2/delta.json'":"ROOT/'layout_delta_v5/delta.json'",
    "ROOT/'changed_body_sheets_v2/sheet_index.json'":"ROOT/'changed_body_sheets_v5/sheet_index.json'",
    "ROOT/'layout_trial_retentions_v2.json'":"ROOT/'layout_trial_retentions_v5.json'",
    "len(doc['records'])==225 and len(plan['records'])==len(native['records'])==223 and native['pages']==228":"len(doc['records'])==216 and len(plan['records'])==len(native['records'])==209 and native['pages']==212",
    "initial['all230_initial_body_pages_directly_viewed'] and initial['all_initial_name_andmenu_sheets_directly_viewed']":
        "initial['all214_initial_body_pages_directly_viewed'] and initial['all_three_menu_sheets_directly_viewed']\n    name_view=load(ROOT/'scoped_names_visual_approval_v1.json')\n    assert name_view['all18_name_strings_directly_viewed'] and name_view['native_sha256']==digest(ROOT/'name_planes_v1/native_name_planes.json')",
    "delta['fresh_pages']==17":"delta['fresh_pages']==14",
    "sum(len(s['included']) for s in sheets['sheets'])==17":"sum(len(s['included']) for s in sheets['sheets'])==14",
    "styles['physical_alternatives']==14":"styles['physical_alternatives']==16",
    "{r['id'] for r in initial['observed_layout_candidates']}":"set(initial['observed_layout_candidates'])",
    "for r in initial['observed_layout_candidates']]":"for r in [dict(id=k,**v) for k,v in initial['observed_layout_candidates'].items()]]",
    'all17_new_native_pages_directly_viewed=True,all230_initial_body_pages_directly_viewed=True':'all14_new_native_pages_directly_viewed=True,all214_initial_body_pages_directly_viewed=True',
    'final_pages=228,visual_layout_revisions=13,visual_candidate_retentions=9':'final_pages=212,visual_layout_revisions=13,visual_candidate_retentions=3',
    'scoped_actors=19,scoped_name_strings=19':'scoped_actors=21,scoped_name_strings=18',
    'all14_style_inputs_andcompiled_bytes_exact_to_original_proof':'all16_style_inputs_andcompiled_bytes_exact_to_original_proof',
    "ROOT/'native_objects_v1/menu/complete_choice_objects.json'":"ROOT/'native_objects_v1/two/complete_choice_objects.json'",
    "    assert len(groups)==1 and sum(len(g['record_IDs']) for g in groups)==2":
        """    threepath=ROOT/'native_objects_v1/three/menu_provider_and_planes.json';three=load(threepath)
    assert three['runtime']==native['runtime'] and three['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
    for obj in three['menus']:
        groups.append(dict(block=obj['block'],source_command_offset=obj['source_command_offset'],target_object_hex=obj['target_object_hex'],
            record_IDs=obj['record_IDs'],original_receipt=str(threepath),original_receipt_sha256=digest(threepath)))
    assert len(groups)==3 and sum(len(g['record_IDs']) for g in groups)==7""",
    '228 final native pages approved; 13 wrap revisions, nine layout retentions.':'212 final native pages approved; 13 wrap revisions, three layout retentions and one FE warning fix.',
})
env={**vars(previous),**globals(),'__file__':__file__}
exec(compile(source,__file__+'::same-offline-approval-and-exact-storage-metadata-bridge','exec'),env)
if __name__=='__main__':env['main']()
