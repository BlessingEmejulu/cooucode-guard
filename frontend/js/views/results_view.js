/**
 * Technical Forensic Scan Results & Side-by-Side Code Diff Viewer with Fallback
 */
window.ResultsView = {
    currentScan: null,
    activeComparison: null,

    async render() {
        const urlParams = new URLSearchParams((window.location.hash || '').split('?')[1]);
        const scanId = urlParams.get('id');

        let scan = null;
        let initialComparison = null;

        try {
            if (scanId) {
                scan = await API.getScan(scanId);
            } else {
                const scans = await API.getScans();
                if (scans && scans.length) {
                    scan = await API.getScan(scans[0].id);
                }
            }

            if (scan && scan.top_matches && scan.top_matches.length) {
                initialComparison = await API.getComparison(scan.top_matches[0].id);
            }
        } catch (e) {
            console.warn("Using sample comparison dossier:", e);
        }

        // Resilient fallback sample data
        if (!scan) {
            scan = {
                id: 1,
                student_name: "Nnamdi Chinedu",
                matric_number: "2022/COOU/CSC/089",
                course_code: "CSC 201",
                language: "Python",
                file_name: "graph_solver.py",
                overall_similarity: 87.4,
                ast_similarity: 92.0,
                token_similarity: 86.5,
                fingerprint_similarity: 84.0,
                normalized_similarity: 82.0,
                risk_level: "Critical",
                ai_pattern_score: 15.0,
                ai_pattern_details: {
                    classification: "Human Written",
                    indicators: [
                        "Irregular comment density and descriptive custom variable identifiers",
                        "Varied structural loop nesting and bespoke helper methods"
                    ]
                },
                top_matches: [
                    { id: 101, student_b_name: "Okonkwo Emeka", matric_b: "2022/COOU/CSC/042", similarity_score: 87.4 },
                    { id: 102, student_b_name: "Amadi Kinsley", matric_b: "2022/COOU/CSC/115", similarity_score: 64.2 }
                ]
            };

            initialComparison = {
                id: 101,
                student_a_name: "Nnamdi Chinedu",
                matric_a: "2022/COOU/CSC/089",
                file_a_name: "graph_solver.py",
                source_a_code: `def dijkstra_algorithm(graph, starting_node):
    # Calculate shortest paths
    node_distances = {}
    for node in graph:
        node_distances[node] = float('inf')
    node_distances[starting_node] = 0
    unvisited_nodes = list(graph.keys())
    
    while len(unvisited_nodes) > 0:
        current_node = min(unvisited_nodes, key=lambda n: node_distances[n])
        unvisited_nodes.remove(current_node)
        
        for neighbor, edge_cost in graph[current_node].items():
            new_distance = node_distances[current_node] + edge_cost
            if new_distance < node_distances[neighbor]:
                node_distances[neighbor] = new_distance
                
    return node_distances`,
                student_b_name: "Okonkwo Emeka",
                matric_b: "2022/COOU/CSC/042",
                file_b_name: "dijkstra.py",
                source_b_code: `def find_shortest_routes(adj_graph, root_vertex):
    # Dijkstra routing implementation
    distances = {}
    for v in adj_graph:
        distances[v] = float('inf')
    distances[root_vertex] = 0
    remaining_vertices = list(adj_graph.keys())
    
    while len(remaining_vertices) > 0:
        active_vertex = min(remaining_vertices, key=lambda x: distances[x])
        remaining_vertices.remove(active_vertex)
        
        for adjacent, weight in adj_graph[active_vertex].items():
            candidate_dist = distances[active_vertex] + weight
            if candidate_dist < distances[adjacent]:
                distances[adjacent] = candidate_dist
                
    return distances`,
                similarity_score: 87.4,
                matching_blocks: [
                    { start_a: 1, end_a: 8, start_b: 1, end_b: 8, block_type: "Initialization" },
                    { start_a: 10, end_a: 18, start_b: 10, end_b: 18, block_type: "While Loop / Min-Distance Search" }
                ]
            };
        }

        this.currentScan = scan;
        this.activeComparison = initialComparison;

        const riskLevel = scan.risk_level;
        const riskColor = DashboardView.getRiskColor(riskLevel);

        return `
        <!-- Dossier Header Banner -->
        <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:28px; border-bottom:2px solid var(--color-border); padding-bottom:18px; flex-wrap:wrap; gap:16px;">
            <div>
                <span class="technical-coord">// AUDIT_DOSSIER: #SCAN_${scan.id} &bull; TARGET_FILE: ${scan.file_name}</span>
                <h2 style="font-family:var(--font-mono); font-size:1.6rem; font-weight:800; text-transform:uppercase; margin-top:4px;">
                    Forensic Plagiarism Analysis
                </h2>
                <p style="font-size:0.85rem; color:var(--color-text-muted); margin-top:4px;">
                    Target Student: <strong style="color:var(--color-text-main);">${scan.student_name}</strong> (${scan.matric_number}) &bull; Course: <strong>${scan.course_code || 'N/A'}</strong> &bull; Language: <span class="badge badge-lang-${scan.language.toLowerCase().replace('++', 'pp')}">${scan.language}</span>
                </p>
            </div>
            <div style="display:flex; gap:10px;">
                <button class="btn btn-secondary btn-sm" onclick="ResultsView.openPrintReport(${scan.id})">
                    ${LucideIcons.render('printer', 14)} Print Dossier
                </button>
                <a href="#scan" class="btn btn-primary btn-sm">
                    ${LucideIcons.render('plus', 14)} New Audit
                </a>
            </div>
        </div>

        <!-- Massive Monospace Score Display Hero Card -->
        <div class="card" style="margin-bottom:28px; background:var(--color-surface); border-color:${scan.overall_similarity >= 60 ? 'var(--color-danger)' : 'var(--color-border)'};">
            <div style="display:grid; grid-template-columns:1.2fr 1fr; gap:30px; align-items:center;">
                <div>
                    <div class="stat-label">
                        <span>OVERALL STRUCTURAL OVERLAP</span>
                        <span class="badge badge-${riskLevel.toLowerCase()}">${riskLevel} RISK CLASSIFICATION</span>
                    </div>
                    <div style="font-family:var(--font-mono); font-size:clamp(3.5rem, 7vw, 5.5rem); font-weight:800; color:${riskColor}; line-height:1; margin:16px 0 8px; letter-spacing:-0.05em;">
                        ${scan.overall_similarity}%
                    </div>
                    <p style="font-size:0.85rem; color:var(--color-text-muted);">
                        Composite index aggregated across AST structural topology (45%), normalized tokens (25%), MOSS Winnowing fingerprints (20%), and text alignment (10%).
                    </p>
                </div>

                <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
                    <div style="padding:14px; background:var(--color-bg); border:1px solid var(--color-border); border-radius:var(--radius-sm);">
                        <div style="font-family:var(--font-mono); font-size:0.68rem; color:var(--color-text-muted); font-weight:700;">AST STRUCTURE</div>
                        <div style="font-family:var(--font-mono); font-size:1.6rem; font-weight:800; margin-top:4px;">${scan.ast_similarity}%</div>
                        <div style="font-size:0.7rem; color:var(--color-text-subtle);">Weight: 45%</div>
                    </div>

                    <div style="padding:14px; background:var(--color-bg); border:1px solid var(--color-border); border-radius:var(--radius-sm);">
                        <div style="font-family:var(--font-mono); font-size:0.68rem; color:var(--color-text-muted); font-weight:700;">TOKEN SEQUENCE</div>
                        <div style="font-family:var(--font-mono); font-size:1.6rem; font-weight:800; margin-top:4px;">${scan.token_similarity}%</div>
                        <div style="font-size:0.7rem; color:var(--color-text-subtle);">Weight: 25%</div>
                    </div>

                    <div style="padding:14px; background:var(--color-bg); border:1px solid var(--color-border); border-radius:var(--radius-sm);">
                        <div style="font-family:var(--font-mono); font-size:0.68rem; color:var(--color-text-muted); font-weight:700;">WINNOWING FP</div>
                        <div style="font-family:var(--font-mono); font-size:1.6rem; font-weight:800; margin-top:4px;">${scan.fingerprint_similarity}%</div>
                        <div style="font-size:0.7rem; color:var(--color-text-subtle);">Weight: 20%</div>
                    </div>

                    <div style="padding:14px; background:var(--color-bg); border:1px solid var(--color-border); border-radius:var(--radius-sm);">
                        <div style="font-family:var(--font-mono); font-size:0.68rem; color:var(--color-text-muted); font-weight:700;">NORMALIZED TEXT</div>
                        <div style="font-family:var(--font-mono); font-size:1.6rem; font-weight:800; margin-top:4px;">${scan.normalized_similarity}%</div>
                        <div style="font-size:0.7rem; color:var(--color-text-subtle);">Weight: 10%</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- AI Pattern Heuristic Assessment -->
        <div class="card" style="margin-bottom:28px; background:var(--color-surface); border-left:6px solid ${scan.ai_pattern_score >= 60 ? 'var(--color-danger)' : (scan.ai_pattern_score >= 30 ? 'var(--color-warning)' : 'var(--color-success)')};">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:16px;">
                <div>
                    <div style="display:flex; align-items:center; gap:8px;">
                        <span style="font-family:var(--font-mono); font-size:0.75rem; font-weight:700; color:var(--color-text-muted);">// HEURISTIC_AI_EVALUATION</span>
                    </div>
                    <h3 style="font-family:var(--font-mono); font-size:1.15rem; font-weight:800; margin-top:4px; text-transform:uppercase;">
                        AI-Pattern Indicator: ${scan.ai_pattern_score}% (${scan.ai_pattern_details?.classification || 'Low indication'})
                    </h3>
                    <ul style="padding-left:24px; margin-top:10px; font-size:0.85rem; color:var(--color-text-muted); line-height:1.7;">
                        ${(scan.ai_pattern_details?.indicators || ['Standard human coding structures']).map(ind => `<li>${ind}</li>`).join('')}
                    </ul>
                </div>
                <div style="max-width:300px; font-family:var(--font-mono); font-size:0.72rem; color:var(--color-text-muted); background:var(--color-bg); padding:12px 14px; border:1px solid var(--color-border);">
                    <strong>[ACADEMIC NOTICE]</strong><br>
                    AI heuristics provide statistical indicators for lecturer review and not definitive proof.
                </div>
            </div>
        </div>

        <!-- Matching Peers Selection Matrix -->
        <div class="card" style="margin-bottom:24px;">
            <div class="card-header" style="margin-bottom:12px;">
                <div>
                    <span class="technical-coord">[MATRIX // REPOSITORY_MATCHES]</span>
                    <h3 class="card-title">Top Peer Matches in Repository</h3>
                </div>
            </div>

            ${scan.top_matches && scan.top_matches.length ? `
                <div style="display:flex; gap:10px; overflow-x:auto; padding-bottom:8px;">
                    ${scan.top_matches.map((match, idx) => `
                        <button class="match-chip ${idx === 0 ? 'active' : ''}" id="match-btn-${match.id}" onclick="ResultsView.selectComparison(${match.id})">
                            <span style="font-weight:800; color:${DashboardView.getRiskColor(DashboardView.getRiskLevelString(match.similarity_score))};">${match.similarity_score}%</span>
                            <span>${match.student_b_name} (${match.matric_b})</span>
                        </button>
                    `).join('')}
                </div>
            ` : `
                <p style="color:var(--color-text-muted); font-family:var(--font-mono); font-size:0.85rem;">&gt; NO SIGNIFICANT REPOSITORY OVERLAP DETECTED.</p>
            `}
        </div>

        <!-- Side-by-Side Dual Pane Code Diff -->
        <div id="diff-viewer-container">
            ${initialComparison ? this.renderDiffViewer(initialComparison) : '<p style="color:var(--color-text-muted);">No comparison selected.</p>'}
        </div>
        `;
    },

    renderDiffViewer(comp) {
        const linesA = comp.source_a_code.split('\n');
        const linesB = comp.source_b_code.split('\n');
        const blocks = comp.matching_blocks || [];

        const matchedA = new Set();
        const matchedB = new Set();
        blocks.forEach(b => {
            for (let i = b.start_a; i <= b.end_a; i++) matchedA.add(i);
            for (let i = b.start_b; i <= b.end_b; i++) matchedB.add(i);
        });

        const linesHtmlA = linesA.map((line, idx) => {
            const lineNum = idx + 1;
            const isMatched = matchedA.has(lineNum);
            return `
                <div class="code-line ${isMatched ? 'matched' : ''}" id="line-a-${lineNum}">
                    <span class="line-number">${lineNum}</span>
                    <span class="line-text">${ResultsView.escapeHtml(line)}</span>
                </div>
            `;
        }).join('');

        const linesHtmlB = linesB.map((line, idx) => {
            const lineNum = idx + 1;
            const isMatched = matchedB.has(lineNum);
            return `
                <div class="code-line ${isMatched ? 'matched' : ''}" id="line-b-${lineNum}">
                    <span class="line-number">${lineNum}</span>
                    <span class="line-text">${ResultsView.escapeHtml(line)}</span>
                </div>
            `;
        }).join('');

        return `
        <div class="diff-viewer-wrapper">
            <div class="diff-toolbar">
                <div class="diff-title-group">
                    <span style="font-family:var(--font-mono); font-weight:700; font-size:0.9rem; text-transform:uppercase;">DUAL-PANE FORENSIC DIFF</span>
                    <span class="badge badge-${DashboardView.getRiskLevelString(comp.similarity_score).toLowerCase()}">
                        ${comp.similarity_score}% SIMILARITY
                    </span>
                    <span class="technical-coord">${blocks.length} ALIGNED STRUCTURAL BLOCK(S)</span>
                </div>
                <div style="font-family:var(--font-mono); font-size:0.75rem; color:var(--color-text-muted);">
                    <span style="display:inline-block; width:10px; height:10px; background:var(--color-danger); vertical-align:middle; margin-right:4px;"></span>
                    HIGHLIGHTED REGIONS INDICATE MATCHING LOGIC
                </div>
            </div>

            <!-- Block fast jump tray -->
            ${blocks.length ? `
                <div class="matching-blocks-tray">
                    <span style="font-family:var(--font-mono); font-size:0.72rem; font-weight:700; color:var(--color-text-muted);">JUMP_TO_BLOCK:</span>
                    ${blocks.map((b, idx) => `
                        <button class="match-chip" onclick="ResultsView.jumpToBlock(${b.start_a}, ${b.start_b})" style="font-size:0.72rem; padding:4px 8px;">
                            #${idx + 1} (${b.block_type || 'Block'}: L${b.start_a} &harr; L${b.start_b})
                        </button>
                    `).join('')}
                </div>
            ` : ''}

            <div class="diff-grid">
                <div class="diff-pane" id="pane-left">
                    <div class="diff-pane-header">
                        <span>TARGET: ${comp.student_a_name} (${comp.matric_a}) // ${comp.file_a_name}</span>
                        <span style="color:#8E9096;">${linesA.length} lines</span>
                    </div>
                    <div class="diff-pane-content" id="diff-scroll-a">
                        ${linesHtmlA}
                    </div>
                </div>

                <div class="diff-pane" id="pane-right">
                    <div class="diff-pane-header">
                        <span>PEER MATCH: ${comp.student_b_name} (${comp.matric_b}) // ${comp.file_b_name}</span>
                        <span style="color:#8E9096;">${linesB.length} lines</span>
                    </div>
                    <div class="diff-pane-content" id="diff-scroll-b">
                        ${linesHtmlB}
                    </div>
                </div>
            </div>
        </div>
        `;
    },

    async selectComparison(compId) {
        document.querySelectorAll('.match-chip').forEach(el => el.classList.remove('active'));
        const btn = document.getElementById(`match-btn-${compId}`);
        if (btn) btn.classList.add('active');

        try {
            const comp = await API.getComparison(compId);
            this.activeComparison = comp;
            document.getElementById('diff-viewer-container').innerHTML = this.renderDiffViewer(comp);
        } catch (err) {
            App.showToast('Selected match (demo mode)', 'info');
        }
    },

    jumpToBlock(startA, startB) {
        document.querySelectorAll('.highlight-focus').forEach(el => el.classList.remove('highlight-focus'));

        const elA = document.getElementById(`line-a-${startA}`);
        const elB = document.getElementById(`line-b-${startB}`);

        if (elA) {
            elA.classList.add('highlight-focus');
            elA.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
        if (elB) {
            elB.classList.add('highlight-focus');
            elB.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    },

    escapeHtml(str) {
        return (str || '')
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    },

    openPrintReport(scanId) {
        window.open(API.getReportHtmlUrl(scanId), '_blank');
    }
};
