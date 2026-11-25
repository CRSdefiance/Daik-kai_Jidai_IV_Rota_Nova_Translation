"""Explicit checkpoint continuation of the original Fernan_field stage."""
from scripts.registered_canonical_checkpoint_resume_v1 import run_driver


def main():
    run_driver('Fernan_field', __file__)


if __name__ == '__main__':
    main()
