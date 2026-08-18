/**
 * Landing Page View - Awwwards-Inspired Editorial Showcase
 */
var LandingView = {
    render() {
        return `
        <div class="landing-wrapper">
            <!-- Top Navigation -->
            <header class="landing-nav">
                <div style="display:flex; align-items:center; gap:10px;">
                    <div style="width:24px; height:24px; background:var(--color-border); color:var(--color-bg); display:flex; align-items:center; justify-content:center; font-family:var(--font-mono); font-weight:800; font-size:0.75rem;">
                        CG
                    </div>
                    <span style="font-family:var(--font-mono); font-weight:700; font-size:0.9rem; letter-spacing:-0.02em;">
                        COOUCODEGUARD
                    </span>
                    <span style="font-family:var(--font-mono); font-size:0.68rem; color:var(--color-text-muted); background:var(--color-bg-subtle); padding:2px 6px; border:1px solid var(--color-border-subtle);">
                        v1.0.0_OFFLINE
                    </span>
                </div>

                <div class="nav-links-group">
                    <a href="#problem">01. PROBLEM</a>
                    <a href="#solution">02. AST ENGINE</a>
                    <a href="#workflow">03. PIPELINE</a>
                    <a href="#tech">04. SPEC</a>
                    <a href="#dashboard" class="btn btn-primary btn-sm">
                        ENTER LAB &rarr;
                    </a>
                </div>
            </header>

            <!-- Hero Section -->
            <section class="hero-section">
                <div>
                    <div class="hero-eyebrow">
                        COOUCodeGuard / SOURCE CODE INTEGRITY SYSTEM
                    </div>
                    <h1 class="hero-title" id="hero-typewriter-text">
                        CODE PLAGIARISM,<br>RE-ENGINEERED.<span class="typewriter-cursor"></span>
                    </h1>
                </div>

                <div class="hero-lead-grid">
                    <div>
                        <p class="hero-description">
                            A local, privacy-sovereign code forensics platform. Detects AST structural invariants, k-gram Winnowing fingerprints, and heuristic AI-generated markers without internet or cloud exposure.
                        </p>
                        <div class="hero-actions">
                            <a href="#dashboard" class="btn btn-primary">
                                START ANALYSIS
                            </a>
                            <a href="#workflow" class="btn btn-secondary">
                                EXPLORE SYSTEM
                            </a>
                        </div>
                    </div>

                    <!-- Live Forensic Terminal Preview -->
                    <div class="hero-terminal-window">
                        <div class="scan-beam"></div>
                        <div class="terminal-header">
                            <span>COOU_AST_ENGINE // LIVE_EMULATOR</span>
                            <span>OFFLINE_MODE : ACTIVE</span>
                        </div>
                        <div class="terminal-body" id="hero-terminal-stream">
                            <div style="color:var(--color-accent); font-weight:700;">&gt; INITIALIZING PARSER FOR [CSC_201_DIJKSTRA.PY]...</div>
                            <div style="color:#8E9096;">&gt; EXTRACTING AST INVARIANTS: 1 FunctionDef, 2 WhileLoops, 3 BinOps</div>
                            <div style="color:#8E9096;">&gt; WINNOWING HASH STREAM: 48 k-grams processed (w=8, k=12)</div>
                            <div style="color:var(--color-warning);">&gt; CORRELATING LOCAL REPOSITORY: 8 Candidate submissions matched</div>
                            <div style="color:var(--color-danger); font-weight:700;">&gt; CRITICAL STRUCTURAL OVERLAP DETECTED: 87.4% SIMILARITY (MATCH #089)</div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Section 1: The Problem -->
            <section id="problem" class="landing-section">
                <span class="section-label-tag">01 // THE ARCHITECTURAL FLAW</span>
                <h2 class="editorial-headline">
                    Most plagiarism checkers read code like text.
                </h2>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:40px; margin-top:30px;">
                    <p style="font-size:1.05rem; line-height:1.7; color:var(--color-text-muted);">
                        Conventional plagiarism systems analyze surface tokens and character sequences. When students rename variable identifiers, invert conditional branches, reorder non-dependent instructions, or inject cosmetic comments, string-matching algorithms fail.
                    </p>
                    <div style="padding:24px; background:var(--color-surface); border:2px solid var(--color-border); font-family:var(--font-mono); font-size:0.8rem; box-shadow:var(--shadow-sm);">
                        <div style="color:var(--color-danger); font-weight:700; margin-bottom:8px;">[TRADITIONAL TEXT-MATCHING DEFEAT]</div>
                        <div style="color:#8E9096;">student_a: <code>def find_max(arr): ...</code></div>
                        <div style="color:#8E9096;">student_b: <code>def get_highest_val(items): ...</code></div>
                        <div style="margin-top:10px; color:var(--color-text-main);">Text Diff: <strong>12% MATCH (FALSE NEGATIVE)</strong></div>
                    </div>
                </div>
            </section>

            <!-- Section 2: The Solution -->
            <section id="solution" class="landing-section">
                <span class="section-label-tag">02 // THE COOU SOLUTION</span>
                <h2 class="editorial-headline">
                    COOUCodeGuard reads the structure.
                </h2>
                <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(320px, 1fr)); gap:24px; margin-top:40px;">
                    <div class="workflow-card">
                        <div style="font-family:var(--font-mono); font-size:0.8rem; color:var(--color-accent); font-weight:700; margin-bottom:10px;">WEIGHT: 45%</div>
                        <h3 class="workflow-title">AST Structural Topology</h3>
                        <p class="workflow-desc">Parses language grammar into abstract syntax trees. Compares structural node frequencies, nesting depths, and longest common statement subsequences.</p>
                    </div>

                    <div class="workflow-card">
                        <div style="font-family:var(--font-mono); font-size:0.8rem; color:var(--color-accent); font-weight:700; margin-bottom:10px;">WEIGHT: 25%</div>
                        <h3 class="workflow-title">Normalized Token Invariants</h3>
                        <p class="workflow-desc">Normalizes variable names into sequential canonical symbols (ID_1, ID_2, KW_DEF) to detect cloned algorithmic flow.</p>
                    </div>

                    <div class="workflow-card">
                        <div style="font-family:var(--font-mono); font-size:0.8rem; color:var(--color-accent); font-weight:700; margin-bottom:10px;">WEIGHT: 20%</div>
                        <h3 class="workflow-title">MOSS Winnowing Fingerprints</h3>
                        <p class="workflow-desc">Constructs position-independent minimum hashes over sliding k-gram windows, rendering matching invariant to relocated code blocks.</p>
                    </div>
                </div>
            </section>

            <!-- Section 3: Workflow Pipeline -->
            <section id="workflow" class="landing-section">
                <span class="section-label-tag">03 // ANALYSIS PIPELINE</span>
                <h2 class="editorial-headline">
                    UPLOAD &rarr; PARSE &rarr; COMPARE &rarr; REPORT
                </h2>
                <div class="workflow-grid">
                    <div class="workflow-card">
                        <div class="workflow-step-num">01</div>
                        <h3 class="workflow-title">Ingest Source</h3>
                        <p class="workflow-desc">Drag and drop student code files (.py, .java, .cpp). Stored locally in SQLite with SHA-256 integrity verification.</p>
                    </div>
                    <div class="workflow-card">
                        <div class="workflow-step-num">02</div>
                        <h3 class="workflow-title">Syntax Extraction</h3>
                        <p class="workflow-desc">Python AST, Java AST, and C++ grammar analyzers extract structural vectors and remove irrelevant noise.</p>
                    </div>
                    <div class="workflow-card">
                        <div class="workflow-step-num">03</div>
                        <h3 class="workflow-title">Local Match</h3>
                        <p class="workflow-desc">Cross-compares target submission against repository peer submissions in milliseconds.</p>
                    </div>
                    <div class="workflow-card">
                        <div class="workflow-step-num">04</div>
                        <h3 class="workflow-title">Audit Dossier</h3>
                        <p class="workflow-desc">Produces side-by-side dual-pane code diffs with line highlighting and printable official reports.</p>
                    </div>
                </div>
            </section>

            <!-- Section 4: Technology & Offline Reality -->
            <section id="tech" class="landing-section">
                <span class="section-label-tag">04 // INSTITUTIONAL SPECIFICATION</span>
                <h2 class="editorial-headline">
                    BUILT FOR THE OFFLINE REALITY.
                </h2>
                <p style="font-size:1.05rem; line-height:1.7; color:var(--color-text-muted); max-width:800px; margin-bottom:30px;">
                    Engineered specifically for Chukwuemeka Odumegwu Ojukwu University (COOU), Uli Campus. Operates entirely without internet connectivity, external APIs, or remote databases. All student intellectual property remains strictly confined to the local machine.
                </p>

                <div style="display:flex; gap:16px; flex-wrap:wrap;">
                    <a href="#dashboard" class="btn btn-primary" style="padding:14px 28px; font-size:0.95rem;">
                        LAUNCH COMMAND CENTER &rarr;
                    </a>
                </div>
            </section>

            <!-- Footer -->
            <footer class="landing-footer">
                <div>
                    <strong>CHUKWUEMEKA ODUMEGWU OJUKWU UNIVERSITY</strong><br>
                    <span style="color:var(--color-text-muted);">Department of Computer Science &bull; Uli Campus, Anambra State, Nigeria</span>
                </div>
                <div>
                    COOUCodeGuard Offline System &bull; 100% Privacy Sovereign
                </div>
            </footer>
        </div>
        `;
    }
};

window.LandingView = LandingView;
