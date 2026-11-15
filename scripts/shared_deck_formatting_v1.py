"""Record-bound phrase preferences with the unchanged validated Refit byte formatter."""
import inspect,textwrap
from scripts.source_locked_derivation_v5118 import checked_text
from dk4tool.dialogue.refit_help import compile_paragraph as original

PREFERENCES={
    'DECK_EXPLANATION_LOOKOUT':('A lookout makes it easier to discover towns and other locations at sea.','other locations at sea.','Keep other locations together as a noun phrase.'),
    'DECK_EXPLANATION_CAPTAIN':('A captain slows the rise in sailor fatigue.','in sailor fatigue.','Keep the complete prepositional phrase together rather than end a line with in.'),
    'DECK_EXPLANATION_ADJUTANT':('A First Mate lets you send negotiation documents from the guild.','from the guild.','Keep the source service location together rather than end a line with from.'),
    'DECK_EXPLANATION_OARS':('This is where sailors row the oars. Navigators cannot be assigned here.','cannot be assigned here.','Keep the complete assignment prohibition together rather than split cannot be assigned.')}

def preferred_lines(text,record_id):
    expected,suffix,_=PREFERENCES[record_id]
    assert text==expected and text.endswith(' '+suffix)
    prefix=text[:-len(suffix)].rstrip()
    return textwrap.wrap(prefix,width=27,break_long_words=False,break_on_hyphens=False)+textwrap.wrap(suffix,width=27,break_long_words=False,break_on_hyphens=False)

source=checked_text(inspect.getsource(original),{
    'def compile_paragraph(text):':'def compile_paragraph(text, *, record_id):',
    'lines = textwrap.wrap(text, width=27, break_long_words=False, break_on_hyphens=False)':
        'lines = preferred_lines(text,record_id)',
})
env={**original.__globals__,'preferred_lines':preferred_lines}
exec(compile(source,__file__+'::same-width27-native-pending-flush-formatting-bound-phrase-preferences','exec'),env)
compile_paragraph=env['compile_paragraph']
