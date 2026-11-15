"""Partition the two overflowing FE paragraphs at their complete sentence boundary;cut no prose."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

PARENT=Path('translations/rafael_B81_B84_contextual_editorial_manuscript_v1.json')
ROOT=Path('work/analysis/Rafael_B84_FE_pagination_20261105')
IDS=['DK4_MES_B84_R0470','DK4_MES_B84_R0539']

if __name__=='__main__':
    assert not ROOT.exists();doc=load(PARENT);sources=[r for r in doc['records'] if r['id'] in IDS];assert len(sources)==2
    children=[];owners=[]
    for row in sources:
        assert row['kind']=='system-FE' and row['source_selector']==254 and not any(row['source_macros'].values())
        marker=' Your ship fires automatically';split=row['english'].index(marker)
        parts=[row['english'][:split],row['english'][split+1:]]
        assert ' '.join(parts)==row['english'] and len(row['english'])==146 and all(s.endswith('.') for s in parts)
        ids=[]
        for index,part in enumerate(parts,1):
            child=deepcopy(row);ident=row['id']+f'_FE_PAGE_{index}';ids.append(ident)
            child.update(id=ident,english=part,planned_English_markup='{SPEAKER:FE}'+part,
                source_editorial_ID=row['id'],native_child_page=index,native_child_page_count=2,
                virtual_formatting_child_not_another_source_editorial_record=True,
                source_complete_paragraph=row['english'],prior_macro_normalized_comparison=None,
                current_English_comparison_pending=False,new_credit=0)
            children.append(child)
        owners.append(dict(source_ID=row['id'],source_reference=row['source_reference'],current_reference=row['current_reference'],
            complete_source_preamble_hex=row['source_complete_preamble_hex'],source_hex=row['source_hex'],current_hex=row['current_hex'],
            unchanged_logical_English=row['english'],child_IDs=ids,page_segments=parts,
            semantic_boundary_reason='The clean paragraph first explains course/sail control andthen automatic fire. Keep both complete sentences,eachon its own native four-row FE information panel. Every original prose character is retained;the paragraph space becomes the native panel boundary.',
            synthetic_command_count=1,source_control_repeated_exactly_not_a_new_actor_orengine_change=True))
    subset=deepcopy(doc);subset.update(records=children,blocks=[84],physical_speech_objects=4,ordinary_speech_objects=0,FE_speech_objects=4,
        typed_choice_objects=0,typed_choice_commands=0,source_editorial_objects=2,
        subset_of=str(PARENT),subset_of_sha256=sha(PARENT.read_bytes()),pagination_owners=owners,
        virtual_children_not_extra_source_coverage=True,native_scoped_FE_command_insertion_andactual_transition_pending=True)
    ROOT.mkdir();save(ROOT/'child_page_manuscript_v1.json',subset);save(ROOT/'owners_v1.json',dict(owners=owners,new_credit=0))
    save(ROOT/'preferences_v1.json',dict(records={}))
    print('Prepared four native child panels for two source paragraphs;full146-character prose/controls retained,not four source credits.')
