"""Bind the complete clean-source role set against Rafael4347's startup."""
from scripts.bind_rafael_B301_B320_roles_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    'assert len(records)==148 and selectors==[207,208,211,214,215,216,222]':
        'assert len(records)==303 and selectors==[207,208,211,214,215,218]',
})


if __name__ == '__main__':
    exec(compile(source, __file__ + '::same-native-role-binding-for-final-SC0-intake', 'exec'), globals())
