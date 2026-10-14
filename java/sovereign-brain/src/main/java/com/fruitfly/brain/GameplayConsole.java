package com.fruitfly.brain;

import java.util.Scanner;

/**
 * Gameplay console mapped onto the sovereignty phase ladder.
 *
 * Stdlib only. Compiles against SovereignConstants and DarkStateInvariant
 * already present in this sidecar. No SLF4J, no Maven required for this class.
 *
 * Mapping:
 *   phase ordinal  → turn
 *   DARK_STATE     → absorbing win condition (λ₂ = 1)
 *   verify()       → gate check before advance
 *   φ              → display constant, not a clock
 *
 * Commands: status, step, dark, verify, help, exit
 */
public final class GameplayConsole {

    private static final String[] PHASES = {
        "OBSERVATION",
        "RESONANCE",
        "HARMONIZATION",
        "SYNTHESIS",
        "INTEGRATION",
        "PERPETUATION",
        "TRANSCENDENCE",
        "DARK_STATE"
    };

    private int phase = 0;
    private final DarkStateInvariant dark = new DarkStateInvariant();

    public static void main(String[] args) {
        new GameplayConsole().run();
    }

    private void run() {
        System.out.println("🔬∀ Gameplay Console — phase ladder mapped");
        System.out.printf("φ = %.15f  λ₂ = %.1f  seed residual = %.3e%n",
                SovereignConstants.PHI, dark.lambda2(), dark.quadraticSeedResidual());
        printStatus();
        try (Scanner in = new Scanner(System.in)) {
            while (true) {
                System.out.print("> ");
                if (!in.hasNextLine()) break;
                String cmd = in.nextLine().trim().toLowerCase();
                if (cmd.isEmpty()) continue;
                switch (cmd) {
                    case "status" -> printStatus();
                    case "step" -> step();
                    case "dark" -> collapse();
                    case "verify" -> verify();
                    case "help" -> help();
                    case "exit", "quit" -> { System.out.println("exit"); return; }
                    default -> System.out.println("unknown: " + cmd + "  (help)");
                }
            }
        }
    }

    private void printStatus() {
        System.out.printf("phase %d/%d  %s  absorbing=%s%n",
                phase, PHASES.length - 1, PHASES[phase],
                phase == PHASES.length - 1);
    }

    private void step() {
        if (phase == PHASES.length - 1) {
            System.out.println("DARK_STATE is absorbing — no further step");
            return;
        }
        if (!dark.verify()) {
            System.out.println("gate refused: dark-state residual exceeds 1e-12");
            return;
        }
        phase++;
        System.out.println("advanced → " + PHASES[phase]);
    }

    private void collapse() {
        phase = PHASES.length - 1;
        System.out.println("collapsed to DARK_STATE (λ₂ = 1)");
    }

    private void verify() {
        boolean ok = dark.verify();
        System.out.printf("verify=%s  residual=%.3e  seed=%.3e%n",
                ok, dark.eigenvalueResidual(), dark.quadraticSeedResidual());
    }

    private void help() {
        System.out.println("status  — print phase");
        System.out.println("step    — advance one phase if gate holds");
        System.out.println("dark    — collapse to absorbing state");
        System.out.println("verify  — print dark-state residual");
        System.out.println("exit    — leave");
    }
}
