"""Registered prefix-extension successor retaining the original reviewed_text_data_v3 stage."""
from scripts.registered_canonical_extension_resume_v3 import run_driver


def main():
    run_driver('reviewed_text_data_v3', __file__)


if __name__ == '__main__':
    main()
