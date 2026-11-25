"""Bind fresh source fields and original names on Rafael3649's startup."""
from scripts.bind_rafael_B261_B280_names_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    'Rafael_B261_B280_clean_20261106': 'Rafael_B281_B300_clean_20261106',
    "    actors = sorted((selectors - {207,254}) | {r['resolved_actor_ID'] for r in roles['native_roles']['rows']} | {65})":
        "    actors = sorted({selector for selector in selectors if selector < 207} | "
        "{r['resolved_actor_ID'] for r in roles['native_roles']['rows']})",
    'assert 65 in actors and 151 in actors': 'assert {0, 4, 5, 8, 14, 22, 65, 69, 70, 71, 113, 147, 149, 177, 178, 187} <= set(actors)',
})

if __name__ == '__main__':
    exec(compile(source, __file__ + '::fresh-source-fields-and-current-getters', 'exec'), globals())
