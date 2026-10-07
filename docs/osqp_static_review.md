# Static QP, review counts, catalogue

Two repos. This file lives on ClarkeYoursaTee only. It does not copy hello_world.py.

## Static solver

The program is

$$\min_x \tfrac12 x^\top P x + q^\top x \quad\text{subject to}\quad l \le Ax \le u.$$

P and A are the static part. `initSolver()` factorizes them once through `osqp_setup`. After that, `updateGradient`, `updateLowerBound`, `updateUpperBound`, and `updateBounds` change only q, l, and u. That is the warm-start regime. If P or A change, the workspace is stale and `clearSolver()` then `initSolver()` is required.

`solve()` returns false unless `status_val` is exactly Solved. Solved-inaccurate is a failure in that wrapper, even if a point was returned. `clearSolverVariables()` zeros the primal and dual iterates only on the pre-v1 workspace path. Under `OSQP_EIGEN_OSQP_IS_V1` that function returns true and clears nothing.

This is a classical convex quadratic program. It is not a quantum circuit. The OsqpEigen `Solver.cpp` text is Giulio Romualdi, BSD 3-Clause, 2018. It is not vendored here.

## Review counts

Supplied table for hello_world.py main, week of Jun 29 through Sep 28, 2026: 13, 4, 3, 16, 16, 78, 191, 563, 859, 365, 370, 461, 493, 55. The supplied headline is 3,487 commits, July 52, August 1,783, September 1,652, authors AxiomicCoreness 2,909 and Clarke Yoursa Tee 565.

A contents-list probe of that repo for 2026-07-01 through 2026-10-01 returned a last-page link of 3581 at one commit per page. That is not the same number as 3,487. The weekly table is the supplied review, not a recomputed histogram.

## Catalogue, not a proof

The tuple \(\mathcal{A} = (Q, \Sigma, \delta, q_0, \mathcal{I}, \mathcal{L}, \mathcal{H})\) is a naming scheme for a small catalogue. It is not an automaton theorem and not a language-model result.

- \(q_0\) is the label CLARKEYOURSATEE.
- \(\Sigma\) is said to have 34 symbols. That count is not checked here.
- The four displayed equations are not identities of a density matrix. \(\operatorname{Tr}(\rho)=\varphi^3\) is a weighted projector, not a trace-1 state. \(S(\rho_n)=0\) and \(W_n\equiv 0\) are claims, not measurements.
- \(f_n = 6.49\cdot\varphi^n\) is a defined ladder, not a measured spectrum.
- Ledger anchors in that block are names. No Merkle root or HMAC is computed in this file.

Option 11, the 22-operator dagger catalogue, stays a list. Sorting by layer is an ordering rule, not an audit.
