"""Entry point for the 2048 teaching project. Run: python main.py --help"""
import sys
import os

# Add src/ to path so the game modules are importable
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from main import main  # imports src/main.py:main (src is now on sys.path)

if __name__ == "__main__":
    main()
