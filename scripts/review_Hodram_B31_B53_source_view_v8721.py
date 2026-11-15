"""Record directly viewed clean panels and narrowly scoped name findings."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B31_B53_source_view_v8721')
DISPLAY=Path('work/analysis/Hodram_B31_B53_source_display_v8720/source_display_andbranch_paths.json')
NAMES=Path('work/analysis/Hodram_B31_actor34_names_v8719/source_names_native_getters_andplanes.json')
if __name__=='__main__':
    assert not ROOT.exists();d,n=read(DISPLAY),read(NAMES)
    assert d['source_names_sha256']==sha(NAMES.read_bytes()) and d['current_B31_B53_English_bodies_still_unconsulted']
    for p in [d['review_sheet'],n['review_sheet']]:assert sha(Path(p['path']).read_bytes())==p['sha256']
    assert d['complete_native_source_page_count']==3 and len(d['records'])==3
    assert [p['text'] for p in n['fresh_actor34_name_planes']]==['Barbarossa Hayreddin','Barbarossa Ｆazul Hayreddin']
    fields=next(r for r in n['complete_clean_current_static_fields'] if r['actor_ID']==34)
    assert [r.get('text') for r in fields['clean']]==['バルバロッサ','ハイレディン','ファーズル']
    ROOT.mkdir(parents=True)
    save(ROOT/'direct_source_view_andscoped_name_findings.json',dict(candidate=d['candidate'],candidate_sha256=d['candidate_sha256'],
        display=str(DISPLAY),display_sha256=sha(DISPLAY.read_bytes()),names=str(NAMES),names_sha256=sha(NAMES.read_bytes()),
        directly_viewed_complete_clean_source_sheet=d['review_sheet'],directly_viewed_name_sheet=n['review_sheet'],
        all3_complete_Japanese_panels_first_internal_final_glyphs_andnative_bounds_directly_viewed=True,
        all3_complete_current_name_literals_directly_viewed=True,
        source_variants_not_consecutive_speeches=True,unnamed_frightening_man_not_identified_from_lore=True,
        source_context_review='Read each B31 variant in full as a separate path, preserving its irritated challenge and the longer before-clause. The original query returns value1 in the own opening context; the alternate value0 path is a structural composition, not a forced predicate or actual event visit. Read B53 as one apparent/reported wanted-status warning and practical caution. The 52->31->53 prerequisite chain is not proof of one continuous scene, original location, earned activation or either B52 choice\'s completion effect.',
        scoped_progressive_name_findings=[dict(actor_ID=34,current='Barbarossa Hayreddin',source_components=['バルバロッサ','ハイレディン'],
            finding='Both complete components appear in the original progressive getter and native name plane. Keep the existing sourced spelling and order provisionally while reviewing the full name consumers; the earlier Hayreddin mention alone did not approve this header.',
            full_editorial_name_approval=False,actual_scene_header_observation=False),
            dict(actor_ID=113,current='Port Worker',source='出港所の兄貴',decision='scoped-retention',
                reason='A natural occupational label for the same gruff practical port-worker voice. 兄貴 is familiar address here and supplies no actual brother, personal name or elevated rank. The European metadata is not a personal surname. The wider role contexts and all207 entries remain open.',
                original_native_consumers=n['scoped_reused_actor113'],actual_B53_header_observation=False)],
        full_name_open_finding=dict(actor_ID=34,current_full_getter='Barbarossa Ｆazul Hayreddin',clean_middle='ファーズル',
            current_middle='Ｆazul',current_middle_hex='8265617a756c',
            finding='The current full getter inserts the independently stored middle field, including a full-width capital F, while the progressive name omits it. This is a real native consumer difference. Do not silently remove the field, treat it as unused, approve its romanization, substitute a historical name or infer a family/rank/biography. Check the source full-name composition, romanization and relevant UI consumers in the ongoing name review.',
            exact_source_current_andlive_RAM_fields=fields,current_RAM=next(r for r in n['exact_current_RAM_fields']['rows'] if r['actor_ID']==34),
            complete_literal_native_style11_plane=n['fresh_actor34_name_planes'][1],
            glyph_proof_does_not_approve_localization_orfull_catalogue_UI=True,remains_in_full207_retrospective_name_scope=True),
        current_B31_B53_English_dialogue_bodies_still_unconsulted=True,
        no_ROM_registry_ledger_orprior_artifact_change=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [DISPLAY,NAMES,Path(__file__)]}))
    print('Viewed all3 clean panels/3name literals; actor113 role retained narrowly; actor34 full getter middle-field/width finding remains open. Earlier dialogue still unread.')
