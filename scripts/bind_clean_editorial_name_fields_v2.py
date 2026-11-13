"""Keep explicit null name components as metadata; reject other unmapped pointers."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/bind_clean_editorial_name_fields.py').read_text(encoding='utf-8'),{
    "            value=string(arm,pointer);assert value['status']=='printable-static-string'":
    """            value=string(arm,pointer)
            if pointer==0:
                assert value['status']=='outside-arm9-static-text'
                value={**value,'status':'source-null-component-no-text','text':None,'hex':'','byte_length':0,'native_consumer_behavior_not_inferred':True}
            else:assert value['status']=='printable-static-string'""",
})
exec(compile(source,__file__+'::exact-null-source-component','exec'),globals())
