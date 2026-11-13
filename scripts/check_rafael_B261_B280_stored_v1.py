"""Verify the rebuilt storage with the original layout and relative-command checks."""
from scripts import check_rafael_B241_B260_stored_v1 as previous
from scripts.plan_rafael_B261_B280_v1 import MACROS
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous.source, {
    """    assert identity['runtime']==runtime and identity['exact_unchanged_actor0_macro_dependencies']
    inherited=load(PREVIOUS_NAMES[0])
    ownpath=Path(inherited['same_Rafael_default_macro_proof'])
    assert sha(ownpath.read_bytes())==inherited['same_Rafael_default_macro_proof_sha256']
    own=load(ownpath);assert own['runtime']['ARM9_sha256']==runtime['ARM9_sha256'] and own['runtime']['COMMON_sha256']==runtime['COMMON_sha256']
    assert own['macro_ascii_lengths']==dict(FI=6,FA=6,FO=10) and len(own['own_native_default_macro_cases']['cases'])==4
    assert sha(macro_path.read_bytes())==own['previous_complete_preamble_macro_proof_sha256']
    assert identity['macro_ascii_lengths']==dict(FI=6,FA=6,FO=10,FU=13) and load(MACROS)['macro_widths']['FU']==78 and identity['evidence'][str(MACROS)]==sha(MACROS.read_bytes())""":
        """    assert identity['runtime']==runtime and identity['all_scoped_getters_fresh_on_registered_ARM9']
    ownpath=MACROS
    own=load(ownpath)
    assert own['runtime']==runtime and own['macro_ascii_lengths']==identity['macro_ascii_lengths']==dict(FI=6,FA=6,FO=10,FU=13)
    assert len(own['three_logical_FI_records'])==3 and all(len(v['cases'])==4 for v in own['current_default_expansions'].values())
    assert macros['source_owned_progressive_adapter']==own['source_owned_progressive_adapter']
    assert identity['current_native_macro_proof_sha256']==sha(ownpath.read_bytes())""",
    "len(rows)==272 and len(style_records)==rebuilt['style_physical_speech_count']==14":
        "len(rows)==114 and len(style_records)==rebuilt['style_physical_speech_count']==16",
    "rebuilt['total_rendered_speech_count']==286": "rebuilt['total_rendered_speech_count']==130",
    "len(typed)==3 and sum(len(item['labels']) for item in typed)==rebuilt['typed_choice_count']==6":
        "len(typed)==2 and sum(len(item['labels']) for item in typed)==rebuilt['typed_choice_count']==5",
    '==[0x2100]*3': '==[0x2100,0x2200]',
    'fresh_pages+reused_pages==294': 'fresh_pages+reused_pages==131',
    'typed_labels_checked=6': 'typed_labels_checked=5',
    'macro_path,ownpath,MACROS,PREVIOUS_NAMES[0],menu_path,styles_path,Path(__file__)':
        'macro_path,ownpath,menu_path,styles_path,Path(__file__)',
})


if __name__ == '__main__':
    storage = dict(previous.compound_storage.__globals__)
    exec(compile(previous.storage, __file__ + '::same-compound-storage', 'exec'), storage)
    env = {**previous.prior.env, 'compound_storage': storage['compound_storage'],
           'MACROS': MACROS, '__file__': __file__, '__name__': 'stored_B261_B280'}
    exec(compile(source, __file__ + '::same-native-guards-current-macro-proof', 'exec'), env)
    env['main']()
