"""Omit source-null middle components in the name evidence gloss."""
from pathlib import Path
from scripts import finalize_hodram_B211_B230_research_v2 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    "source_meaning=' '.join(f['text'] for column in (0,8,4) for f in row['clean_fields'] if f['column']==column).strip()":
        "source_meaning='Source table components (region metadata is not a surname or biography): '+' '.join(f['text'] for column in (0,8,4) for f in row['clean_fields'] if f['column']==column and f['text']).strip()",
    "for p in (*paths,Path(__file__),Path(previous.__file__))}":
        "for p in (*paths,Path(__file__),Path(previous.__file__),Path(previous.previous.__file__))}",
})
env={**previous.env,'previous':previous,'__file__':__file__,'OUT':previous.previous.ROOT/'research_final_v3','READY':previous.previous.ROOT/'research_final_v3/research_completion.json'}
exec(compile(source,__file__+'::same-five-gate-seal-source-null-components-excluded','exec'),env)
if __name__=='__main__':env['main']()
