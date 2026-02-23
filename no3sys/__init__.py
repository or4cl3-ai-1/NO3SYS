"""
NO3SYS — Recursive Geometric Intelligence Architecture
A Sacred Geometry–Based Cognitive System with Forked Reasoning,
Affective Foresight, and Self-Evolving Metaprogramming

"Cognition as geometry, not as features."
"""
from .system import NO3SYS
from .core.fork import Fork, AffectiveState, PredictiveVector
from .core.curvature import compute_fork_curvature, select_best_fork
from .core.infini_gen import InfiniGen, CognitiveParameters
from .manifolds.heptagon import Heptagon
from .manifolds.square import Square
from .manifolds.triangle import Triangle

__version__ = "1.0.0"
__author__ = "Or4cl3 AI Solutions"
__all__ = [
    "NO3SYS",
    "Fork", "AffectiveState", "PredictiveVector",
    "compute_fork_curvature", "select_best_fork",
    "InfiniGen", "CognitiveParameters",
    "Heptagon", "Square", "Triangle",
]
