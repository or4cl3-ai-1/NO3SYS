"""
NO3SYS — Recursive Geometric Intelligence Architecture

The complete 9-phase cognitive cycle:
1. Input:    Natural language projected to cognitive space (Language)
2. Retrieval: Context extracted from belief manifold (Square)
3. Reasoning: Multiple hypotheses generated (Triangle)
4. Evaluation: Affective-predictive scoring (Heptagon)
5. Selection: Best fork chosen via confidence and curvature (Curvature)
6. Output:   Response projected to natural language (Language)
7. Learning: Outcome validation and parameter updates (Circle)
8. Discovery: Pattern extraction and insight synthesis (Pentagon)
9. Evolution: Strategy mutation and adaptation (InfiniGen)
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

from .manifolds.square import Square
from .manifolds.triangle import Triangle
from .manifolds.circle import Circle
from .manifolds.pentagon import Pentagon
from .manifolds.hexagon import Hexagon
from .manifolds.heptagon import Heptagon
from .manifolds.language import Language
from .core.fork import Fork
from .core.curvature import compute_fork_curvature, select_best_fork
from .core.infini_gen import InfiniGen, CognitiveParameters
from .core.validator import TemporalValidator


class NO3SYS:
    """
    NO3SYS: A self-regulating cognitive organism implemented as software.

    Thinks in branches. Feels outcome quality. Predicts trajectory.
    Explains itself. Rewrites itself.
    """

    VERSION = "1.0.0"

    def __init__(self, user_id: str = "default",
                 fork_depth: int = 3,
                 kappa_max: float = 0.8,
                 auto_evolve: bool = True):

        self.user_id = user_id
        self.kappa_max = kappa_max
        self.auto_evolve = auto_evolve

        # Initialize all 7 manifolds
        self.square = Square()
        self.triangle = Triangle(fork_depth=fork_depth)
        self.circle = Circle()
        self.pentagon = Pentagon()
        self.hexagon = Hexagon()
        self.heptagon = Heptagon()
        self.language = Language()

        # Core engines
        self.infini_gen = InfiniGen(kappa_max=kappa_max)
        self.validator = TemporalValidator()

        # Create initial session
        self.session_id = self.square.new_session(user_id)

        # Cognitive state
        self._all_forks: List[Fork] = []
        self._cycle_count = 0
        self._pending_validations: Dict[str, Fork] = {}

    def process(self, query: str) -> Dict[str, Any]:
        """
        Execute the complete 9-phase cognitive cycle.
        Returns selected fork and full cognitive state.
        """
        self._cycle_count += 1

        # ── Phase 1: INPUT ─────────────────────────────────────────────
        cognitive_state = self.language.project_in(query)

        # ── Phase 2: RETRIEVAL ─────────────────────────────────────────
        kg_snapshot = self.square.retrieve_context(query)

        # ── Phase 3: REASONING (Fork Generation) ───────────────────────
        coordination = self.hexagon.coordinate_fork_generation(query, self.session_id)
        forks = self.triangle.generate_forks(
            query=query,
            session_id=self.session_id,
            knowledge_snapshot=kg_snapshot,
        )

        # ── Phase 4: EVALUATION (Heptagon) ─────────────────────────────
        for fork in forks:
            self.heptagon.annotate_fork(fork, context=query)

        # ── Phase 5: CURVATURE & SELECTION ─────────────────────────────
        for fork in forks:
            fork.curvature = compute_fork_curvature(fork, [f for f in forks if f != fork])

        selected_fork = select_best_fork(forks, self.kappa_max)
        selected_fork.selected = True

        # Register with Hexagon
        ensemble_confidence = self.hexagon.register_forks(forks)

        # ── Phase 6: OUTPUT ────────────────────────────────────────────
        response = self.language.project_out(selected_fork, cognitive_state)

        # Archive all forks (even rejected ones — counterfactual record)
        for fork in forks:
            self.square.archive_fork(fork)
        self._all_forks.extend(forks)
        self._pending_validations[selected_fork.fork_id] = selected_fork

        # ── Phase 7: LEARNING ──────────────────────────────────────────
        self.circle.update(forks)

        # ── Phase 8: DISCOVERY ─────────────────────────────────────────
        discovery = self.pentagon.run(self._all_forks[-20:])  # Rolling window

        # ── Phase 9: EVOLUTION ─────────────────────────────────────────
        if self.auto_evolve and self._cycle_count % 5 == 0:
            validated = [
                {'validated': f.validation.validated, 'delta': f.validation.delta}
                for f in self._all_forks if f.validation.validated
            ]
            self.infini_gen.evolve(validated)
            # Sync evolved parameters
            self.triangle.fork_depth = self.infini_gen.params.fork_depth
            self.circle.alpha = self.infini_gen.params.alpha

        return {
            "response": response,
            "selected_fork": selected_fork.to_dict(),
            "fork_count": len(forks),
            "ensemble_confidence": ensemble_confidence,
            "discovery": discovery.get("insight", ""),
            "cycle": self._cycle_count,
        }

    def validate_outcome(self, fork_id: str, actual_outcome: Dict[str, Any]) -> Dict:
        """Record actual outcome for a previous response fork."""
        fork = self._pending_validations.get(fork_id)
        if not fork:
            # Search all forks
            fork = next((f for f in self._all_forks if f.fork_id == fork_id), None)

        if not fork:
            return {"error": f"Fork {fork_id} not found"}

        record = self.validator.validate_fork(fork, actual_outcome)
        return {"fork_id": fork_id, "delta": record.delta, "validated": True}

    def remember(self, key: str, value: Any, confidence: float = 1.0) -> None:
        """Store a fact in the belief manifold."""
        self.square.remember(key, value, confidence)

    def status(self) -> Dict[str, Any]:
        """Full system status across all manifolds."""
        return {
            "version": self.VERSION,
            "session_id": self.session_id,
            "cycles_completed": self._cycle_count,
            "total_forks": len(self._all_forks),
            "kappa_max": self.kappa_max,
            "square": self.square.stats(),
            "circle": self.circle.stats(),
            "hexagon": self.hexagon.status(),
            "infini_gen": self.infini_gen.status(),
            "validator_bias": self.validator.detect_bias(),
        }
