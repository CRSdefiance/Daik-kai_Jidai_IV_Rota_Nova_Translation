"""Reconcile13 portrait-escape rows with distinct COMMON and direct-formatter owners."""
from pathlib import Path
OLD=Path('scripts/reconcile_contextual_mood_retentions_v2482.py')
source=OLD.read_text()
changes={
 "fonts['current_parent_projection_controls']==1 and fonts['current_parent_projection_is_shared_ordinary_control_not_current_battle_GPU']":"fonts['current_parent_projection_controls']==0 and fonts['current_modal_font_consumers_no_Deck_parent_projection_claim']",
 "stage['proof']['reviewed_native_IDs']==ids":"set(ids)<=set(stage['proof']['reviewed_native_IDs'])",
 "historical_changed_records=stage['proof']['changed_records'],new_revisions=0":"historical_changed_records=stage['proof']['changed_records'],registered_layer_native_IDs=stage['proof']['reviewed_native_IDs'],selected_escape_native_IDs=ids,new_revisions=0",
 "consumer='252x96 canvas,body y60;216x36 parent crop at screen16,112;registered generated36-column3row pair-safe paragraph'":"display_contract='228x64 shared portrait speech;35 cells x4 rows;16px row stride;native x6 left indent at screen origin16,296;original direct53F0C parent02053F40/table stack+274'",
 'historical_mood_current_binding':'historical_escape_current_binding',
 'scoped_historical_battle_returns_freshly_rechecked':'scoped_historical_cancellation_and_battle_transitions_freshly_rechecked',
 'new_current_mood_ID_visits':'new_current_escape_ID_visits',
 'current_shared_parent_is_ordinary_control_not_mood_gameplay=True':'current_Deck_parent_projection_claim=False',
 'current_native_mood_font':'current_native_direct_escape_font',
 'current_native_direct_escape_font_executions':'current_native_direct_escape_expansion_font_cases',
 'mood0_4_5':'direct_escape35x4',
 'current_parent_draw_controls=1,current_parent_is_ordinary_shared_geometry_control=True':'current_parent_draw_controls=0,current_Deck_parent_projection_claim=False,unique_current_native_font_rasters=1021',
 'historical_returns_current_rechecked':'historical_defeat_and_title_transitions_current_bound',
 'historical_returns_rechecked':'historical_defeat_and_title_transitions_bound',
 'Historical-only battle/return binding':'Historical-only defeat/title-transition binding',
 'ordinary/battle direct_escape35x4 fonts':'corrected direct portrait-speech fonts',
 'mood-fixtures-and-returns':'pre-duel-fixtures-defeat-and-title',
 'font_previews=count':'font_previews=spec["font_previews"]',
 'retentions-original-216x36-crop':'retentions-original-direct-228x64-portrait-speech',
}
for a,b in changes.items():
 assert a in source,a
 source=source.replace(a,b)
needle=' validate_natural_dialogue_batch(notes);'
assert needle in source
extra=""" assert fonts['complete_native_font_cases']==1423 and fonts['unique_native_font_planes']==1021 and len(fonts['all162_exact_current_interjection_boundary_decisions'])==162
 pipelinepath=Path(spec['current_pipeline']);pipeline=read(pipelinepath);assert len(pipeline['all13_current_direct_pipeline_cases'])==13 and len(pipeline['all416_source_voice_choices'])==416 and pipeline['all_executed_section_code_matches_current_ROM']
 formatterpath=Path(spec['formatter_config']);formatter=read(formatterpath);formatterstage=manifest['relocations']['/__arm9__.bin']['escape_direct_formatting'];assert sha(formatterpath.read_bytes())==formatterstage['release_config_sha256']
 effectivepath=Path(formatter['manuscript']);assert sha(effectivepath.read_bytes())==formatter['dependencies'][str(effectivepath)]
 notes.update(current_native_source_pipeline=str(pipelinepath),current_native_source_pipeline_sha256=sha(pipelinepath.read_bytes()),effective_direct_formatter_config=str(formatterpath),effective_direct_formatter_config_sha256=sha(formatterpath.read_bytes()),effective_direct_manuscript=str(effectivepath),effective_direct_manuscript_sha256=sha(effectivepath.read_bytes()),corrected_direct_parent=0x02053F40,corrected_direct_table_stack_offset=0x274)
 for r in notes['records']:
  assert r['consumer']=='original-post-duel-companion-speech'
  r['current_exact_interjection_boundary_decisions']=[w for w in fonts['all162_exact_current_interjection_boundary_decisions']if w['message_ID']==r['message_id']]
"""
source=source.replace(needle,extra+needle)
exec(compile(source,__file__,'exec'),globals())
