"""render_box.py — component topology of the eight symplectic layers.

Single source: the filesystem listing of this repository at the time of
landing (git tree `main`).  Component counts are real file counts, not the
design-sheet figure of 60.

Co-located with scripts/render_status.py and scripts/prebuild.py in the
same directory; import via sys.path so the trio moves as one unit.
"""

LAYERS = [
    "JVM_LIF",
    "FASTAPI_APP",
    "QUANTUM_CDP",
    "QUANTUM_CORDIS",
    "TEST_SUITE",
    "CONTAINER",
    "SCRIPTS",
    "WORKFLOWS",
]

COMPONENTS = {
    "JVM_LIF": [
        "src/main/java/com/fruitfly/brain/KaTeXMacros.java",
        "src/main/java/com/fruitfly/brain/LIFRK4.java",
        "src/main/java/com/fruitfly/brain/Neuron.java",
        "src/main/java/com/fruitfly/brain/SovereignConstants.java",
        "src/main/java/com/fruitfly/brain/SovereignMain.java",
        "src/main/java/com/fruitfly/brain/WarriorQuadratic.java",
        "src/main/java/com/fruitfly/brain/connectome.java",
    ],
    "FASTAPI_APP": [
        "app/__init__.py",
        "app/main.py",
        "app/routers/__init__.py",
        "app/routers/health.py",
        "app/routers/items.py",
    ],
    "QUANTUM_CDP": [
        "quantum/cdp_convergence/__init__.py",
        "quantum/cdp_convergence/cdp_schema.py",
        "quantum/cdp_convergence/handshake.py",
        "quantum/cdp_convergence/oauth2.py",
        "quantum/cdp_convergence/void_qch.py",
        "quantum/cdp_convergence/websocket_gate.py",
    ],
    "QUANTUM_CORDIS": [
        "quantum/cordis_bridge/__init__.py",
        "quantum/cordis_bridge/bridge.py",
        "quantum/cordis_bridge/platforms.py",
        "quantum/cordis_bridge/schema.py",
    ],
    "TEST_SUITE": [
        "tests/__init__.py",
        "tests/geometry_suite.py",
        "tests/harness.py",
        "tests/harness_core.py",
        "tests/policy_v1_section_test.md",
        "tests/quantum/test_breathing_manifold.py",
        "tests/quantum/test_e10_hyperbolic.py",
        "tests/quantum/test_wood_dragon_gate.py",
        "tests/test_all.py",
        "tests/test_anomaly_distance.py",
        "tests/test_app.py",
        "tests/test_argo.py",
        "tests/test_argo_manifests.py",
        "tests/test_arrow_identities.py",
        "tests/test_axiom_differential.py",
        "tests/test_berry_chern.py",
        "tests/test_bind.py",
        "tests/test_codespace_hook_worker.py",
        "tests/test_consumer_axiom.py",
        "tests/test_declaration_flag.py",
        "tests/test_deepseek_ndjson.py",
        "tests/test_deepseek_rate.py",
        "tests/test_density_rho.py",
        "tests/test_diffuse_kl_cache.py",
        "tests/test_port380_mcp.py",
    ],
    "CONTAINER": [
        ".container/Dockerfile",
        ".container/README.md",
        ".container/aklt_gap.py",
        ".container/app.py",
        ".container/format.py",
        ".container/phi-mod-mean.xml",
        ".container/supervisor.py",
    ],
    "SCRIPTS": [
        "scripts/gitcode_deploy.sh",
        "scripts/ml_sovereign_core.py",
        "scripts/restart_port380.sh",
    ],
    "WORKFLOWS": [
        "workflows/aklt-e2e.yml",
        "workflows/ci-deploy.yml",
    ],
}

ANCHORS = {
    "JVM_LIF": "src/main/java/com/fruitfly/brain/LIFRK4.java",
    "FASTAPI_APP": "app/main.py",
    "QUANTUM_CDP": "quantum/cdp_convergence/handshake.py",
    "QUANTUM_CORDIS": "quantum/cordis_bridge/bridge.py",
    "TEST_SUITE": "tests/test_all.py",
    "CONTAINER": ".container/supervisor.py",
    "SCRIPTS": "scripts/restart_port380.sh",
    "WORKFLOWS": "workflows/ci-deploy.yml",
}

COMPONENT_COUNT = sum(len(paths) for paths in COMPONENTS.values())