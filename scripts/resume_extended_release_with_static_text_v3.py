"""Registered prefix-extension successor retaining the original static_text stage."""
from scripts.registered_canonical_extension_resume_v3 import run_driver


def main():
    run_driver('static_text', __file__)


if __name__ == '__main__':
    main()
