"""Read complete clean-only exchanges without exposing current story English."""
from scripts.read_maria303_clean_v1 import main
from pathlib import Path

main.__globals__['ROOT'] = Path('work/Maria_B73_B95_clean_20261109')
if __name__ == '__main__':
    main()
