"""Expose the frozen preparation constants without repeating the completed prepare."""
from scripts.prepare_maria335_B137_B151_registered_v1 import source
exec(compile(source,__file__+'::same-preparation-with-importable-constants','exec'),globals())
