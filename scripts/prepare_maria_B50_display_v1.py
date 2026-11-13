"""Reuse the source-complete Maria QA host with an explicitly empty style scope."""
from scripts.prepare_maria270_display_fixtures_v2 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{
    "styles=load(rebuilt['styles']);assert styles['runtime']==stored['runtime']":
        """assert rebuilt['style_physical_speech_count']==rebuilt['typed_choice_count']==rebuilt['compound_objects']==0
    assert all(not g.get('native_objects') and not any(c['word'] in [0x2100,0x2200,0x4100] for c in g['all_target_commands']) for g in rebuilt['groups'])
    assert all(all('speech' in a for a in f['sequence']) for f in selection['fixtures'])
    styles={}  # No style object is requested or credited.""",
})
exec(compile(source,__file__+'::same-bounded-native-command-copy-andhost-no-compound-inference','exec'),globals())
