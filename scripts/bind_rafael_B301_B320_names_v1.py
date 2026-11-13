"""Bind both original name consumers to the new clean-source exchange scope."""
from scripts.bind_rafael_B281_B300_names_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    'Rafael_B281_B300_clean_20261106': 'Rafael_B301_B320_clean_20261106',
    'assert {0, 4, 5, 8, 14, 22, 65, 69, 70, 71, 113, 147, 149, 177, 178, 187} <= set(actors)':
        'assert {0, 4, 5, 7, 8, 17, 19, 92, 95, 97, 135, 148, 151, 162, 182, 192, 197, 199, 203} <= set(actors)',
})

if __name__ == '__main__':
    exec(compile(source, __file__ + '::fresh-source-fields-and-Rafael3894-getters', 'exec'), globals())
