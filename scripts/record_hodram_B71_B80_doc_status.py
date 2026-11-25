"""Concise current status; leave earlier progress and issue history intact."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load

if __name__=='__main__':
    checkpoint=load('work/analysis/Hodram_B71_B80_release_verified_20261101/completion_checkpoint.json')
    assert checkpoint['counts']['completed']==7687 and not checkpoint['full_goal_complete']
    changes={
        'docs/translation_progress.md':"""## 2026-11-01: Hodram B71-B80 integrated;7,687 completed

The verified registered cumulative successor adds144 once-only contextual reviews:
100 revisions (92 wording/meaning changes and8 glyph-only changes),44 justified
retentions,154 reviewed native pages andfocused B72/B76 gameplay. All652 manifest
entries/114 accepted layers/19 release checks,exact clean-input patch andown4001-frame
startup pass. Counts7,687 completed/7,690 source-prose anddrafts/4,770 integrated
revisions/2,917 retentions;SC1 has607. A stale nested index for224 already-credited
records is reconciled withzero new credit. Main remains unchanged. See
[release and next steps](editorial_hodram_B71_B80_20261101.md).

Next B81-B90 has304 clean-first speech meanings plus2typed-menu meanings. Earlier
English is unconsulted;names/linked context/terminology andthe typed-menu consumer
need scoped review before localization. Full goal active;graphics/later audit
remain separate. Guide photo collection is discontinued;only QA previews/captures
are needed. Preserve all ROMs andprior work.

""",
        'docs/todo.md':"""## 2026-11-01 next: B81-B90 source context andlocalization

B71-B80 is registered,patch/startup-verified andcredited once;do not repeat those
checks. Continue304 complete clean-first speech meanings plus2B87 choice meanings
in work/analysis/Hodram_B81_B90_clean_20261101. Older English is unconsulted.
Resolve names andlinked context,retain source kinship distinctions andfamiliar
nonkin address,bind the real dock/refit terminology,andinclude both B87 choice
labels in the review andsource-qualified menu compiler. B90 hasonly controls.
Reuse compatible consumer evidence;fresh text still needs formatting checks.
See [current release andcontinuation](editorial_hodram_B71_B80_20261101.md).
No guide photo collection. Full story/shared/town/random/name/remaining-prose and
earlier-wrap scope stays active;graphics/later technical audit remain separate.

""",
        'docs/known_issues.md':"""## 2026-11-01: B71-B80 cumulative release verified

The144-record contextual pass removes unsupported exclusive trading rights/noble
titles,corrects the rescue companions' role,restores natural character voices and
fixes eight punctuation-width cases. All154 final pages and420 native relative
cases pass;representative initialized B72/B76 gameplay shows dialogue,continuation,
anonymous FE notices andtown returns. These are disclosed fixtures,not natural
conditional activation orhardware coverage. Registered candidate SHA
8236e9c662eeda8cd091cedcc0c154ac21532841dc4a69c06e24f0a7ebd46290 has652 manifest
entries/114 accepted layers/19 passing checks,exact clean-input reconstruction and
own startup. Registered ASCII right-bound repair,all prior graphics/fonts/names
andmain are preserved. Full-name Fazul/de andwider glyph leads remain open.
See [verified release](editorial_hodram_B71_B80_20261101.md).

""",
        'docs/editorial_review_goal.md':"""## Current continuation - 2026-11-01

B71-B80's144 records are integrated andcredited once in the verified cumulative
release;7,687 completed. Continue from
[the current checkpoint](editorial_hodram_B71_B80_20261101.md),including304 clean
speech meanings andtwo B87 typed-choice meanings before earlier-English comparison.
Preserve the full editorial objective andall prior credit/evidence. The user has
discontinued guide photo collection;retain only required editorial/display QA
previews andfocused gameplay captures,preserving existing images.

""",
    }
    for name,prefix in changes.items():
        path=Path(name);before=path.read_bytes()
        assert not before.startswith(prefix.encode('utf-8'))
        path.write_bytes(prefix.encode('utf-8')+before)
    print('Four current status/goal documents updated;all earlier history preserved.')
