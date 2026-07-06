"""CognitionFM - generative functional music engine.

Renders original, fully-owned long-form audio from evidence-derived recipes.
See docs/01-evidence-review.md for the research each recipe parameter traces to.
"""

import os

__version__ = "0.1.0"

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
