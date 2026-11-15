"""Bind both complete source/current B84 menus without interpreting their typed captions as speech."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.reviewed_choice_object_v2 import compile_choices,count_and_base
from scripts.audit_story_glyph_consistency import load,save

MANUSCRIPT=Path('translations/rafael_B81_B84_contextual_editorial_manuscript_v1.json')
ROOT=Path('work/analysis/Rafael_B84_choices_20261105')

if __name__=='__main__':
    assert not ROOT.exists();doc=load(MANUSCRIPT);rows=[deepcopy(r) for r in doc['records'] if r['kind']=='typed-choice-label']
    assert len(rows)==5;groups={}
    for row in rows:
        row['source_choice_object_hex']=row['source_command_hex']
        row['source_reference']=dict(file_path=row['file_path'],block=row['block'],command_offset=row['source_command_offset'],
            offset=row['source_byte_offset'],source_index=row['source_index'],length=len(bytes.fromhex(row['source_hex'])))
        groups.setdefault(row['source_command_offset'],[]).append(row)
    assert list(groups)==[3114,5298]
    ROOT.mkdir();inputs=[]
    for offset,items in groups.items():
        source,current=map(bytes.fromhex,[items[0]['source_choice_object_hex'],items[0]['current_choice_object_hex']])
        n,_=count_and_base(source);assert len(items)==n
        compiled=compile_choices(source,current,items,require_formatting=False)
        subset=deepcopy(doc);subset.update(records=items,blocks=[84],encoder='native-typed-choice-v2',physical_speech_objects=0,
            ordinary_speech_objects=0,FE_speech_objects=0,typed_choice_objects=n,typed_choice_commands=1,
            subset_of=str(MANUSCRIPT),subset_of_sha256=sha(MANUSCRIPT.read_bytes()),
            source_bound_typed_caption_references_added_without_prose_change=True)
        path=ROOT/f'B84_C{offset}_manuscript.json';save(path,subset)
        inputs.append(dict(source_command_offset=offset,labels=n,manuscript=str(path),manuscript_sha256=sha(path.read_bytes()),
            complete_source_object_hex=source.hex(),complete_current_object_hex=current.hex(),compiled_object_hex=compiled.hex(),
            target_bytes=len(compiled),max_caption_bytes=max(len(r['english']) for r in items)))
    save(ROOT/'source_bound_inputs.json',dict(manuscript=str(MANUSCRIPT),manuscript_sha256=sha(MANUSCRIPT.read_bytes()),menus=inputs,
        complete_choice_index_andzero_alignment_only_native_compiler_pass=True,native_provider_display_andactual_controller_pending=True,new_credit=0))
    print('Bound five source/current captions in two complete native objects;all prose unchanged;native provider/display pending.')
