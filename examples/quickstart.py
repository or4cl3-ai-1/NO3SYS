"""
NO3SYS Quickstart — Complete 9-Phase Cognitive Cycle Demo
"""
from no3sys import NO3SYS


def main():
    print("=" * 60)
    print("NO3SYS v1.0.0 — Geometric Intelligence Architecture")
    print("=" * 60)

    # Initialize system
    system = NO3SYS(user_id="researcher", fork_depth=3, kappa_max=0.8)

    # Seed the belief manifold
    system.remember("domain", "AI safety and cognitive architecture")
    system.remember("project", "OR4CL3 geometric intelligence ecosystem")
    system.remember("constraint", "All mutations must satisfy κ < κ_max")

    print("\n[Phase 1-9] Processing query...\n")

    # Run the complete cognitive cycle
    result = system.process(
        "What are the ethical implications of self-evolving AI systems?"
    )

    print(f"Response: {result['response']}")
    print(f"\nSelected Fork ID: {result['selected_fork']['fork_id']}")
    print(f"Confidence: {result['selected_fork']['confidence']:.3f}")
    print(f"Curvature (κ): {result['selected_fork']['curvature']:.3f}")

    print("\nAffective State:")
    sentiment = result['selected_fork']['sentiment']
    for k, v in sentiment.items():
        bar = "█" * int(v * 20)
        print(f"  {k:15s}: {bar:20s} {v:.3f}")

    print("\nPredictive Vector:")
    future = result['selected_fork']['future']
    for k, v in future.items():
        bar = "█" * int(v * 20)
        print(f"  {k:15s}: {bar:20s} {v:.3f}")

    print(f"\nForks generated: {result['fork_count']}")
    print(f"Ensemble confidence: {result['ensemble_confidence']:.3f}")

    if result['discovery']:
        print(f"\nDiscovery insight: {result['discovery']}")

    # Run several cycles to trigger InfiniGen evolution
    print("\n[Running 4 more cycles to trigger InfiniGen evolution...]")
    queries = [
        "How does fork-based reasoning improve decision quality?",
        "Explain the relationship between curvature and ethical alignment",
        "What is the role of the Heptagon in affective foresight?",
        "How does InfiniGen maintain safety during self-evolution?",
    ]
    for q in queries:
        r = system.process(q)
        print(f"  Cycle {r['cycle']}: κ={r['selected_fork']['curvature']:.3f}, "
              f"conf={r['selected_fork']['confidence']:.3f}")

    # System status
    print("\n[System Status]")
    status = system.status()
    print(f"  Total cycles: {status['cycles_completed']}")
    print(f"  Total forks:  {status['total_forks']}")
    print(f"  InfiniGen gen: {status['infini_gen']['generation']}")
    print(f"  Mutations accepted: {status['infini_gen']['mutations_accepted']}")
    print(f"  Mutations rejected (κ): {status['infini_gen']['mutations_rejected']}")

    print("\n✓ NO3SYS cognitive cycle complete.")
    print("  Geometry thinks. Curvature guides. Evolution adapts.")


if __name__ == "__main__":
    main()
