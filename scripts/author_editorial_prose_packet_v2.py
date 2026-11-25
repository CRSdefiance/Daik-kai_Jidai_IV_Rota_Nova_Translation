"""Same per-record prose gates with explicit batch-specific name evidence."""
import inspect
from scripts import author_editorial_prose_packet as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(inspect.getsource(previous.write_packet),{
    'def write_packet(current_path,decisions,contexts,out,producer):':
        'def write_packet(current_path,decisions,contexts,out,producer,*,names,name_bindings,known_name_reuse,pending_name_findings):',
    "speaker=NAMES[source['source_selector']]":"speaker=names[source['source_selector']]",
    "name_bindings='work/analysis/Hodram_B81_B90_new_names_20261101/names.json'":'name_bindings=name_bindings',
    "known_name_reuse='work/analysis/Hodram_B81_B90_new_names_20261101/known_six_reuse.json'":'known_name_reuse=known_name_reuse',
    "pending_name_display_finding='Actor14 progressive andfull name contain full-width F;body spelling Ferog is retained withnormal ASCII F. Shared name correction remains pending.'":
        'pending_name_display_findings=pending_name_findings',
})
globals().update({k:v for k,v in previous.__dict__.items() if k not in ['__name__','__file__','__builtins__']})
exec(compile(source,__file__+'::batch-qualified-name-evidence','exec'),globals())
