"""Supply the unchanged FE helper to the zero-authored-layout native runner."""
from scripts.check_editorial_compiled_pages_v6 import source, check_FE_rows
from scripts.check_editorial_compiled_pages_v7 import validate_documented_layouts

exec(compile(source, __file__ + '::same-complete-native-checks-and-FE-helper', 'exec'), globals())
