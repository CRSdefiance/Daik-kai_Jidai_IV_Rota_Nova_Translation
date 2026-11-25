"""Apply the unchanged full stored/native checks to307 ordinary,34 style andten caption records."""
from scripts.check_qualified_rafael_mixed_stored_v3 import source as previous,compound_storage,check_FE_rows,progressive_expand,FE_expand
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    "==rebuilt['style_physical_speech_count']==14":"==rebuilt['style_physical_speech_count']==34",
    "==rebuilt['total_rendered_speech_count']==243":"==rebuilt['total_rendered_speech_count']==341",
    "==rebuilt['typed_choice_count']==12":"==rebuilt['typed_choice_count']==10",
})
if __name__=='__main__':exec(compile(source,__file__+'::same-native-parity-pages-relatives-all351-objects','exec'),globals())
