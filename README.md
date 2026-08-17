# COOUCodeGuard - Offline Source Code Plagiarism Detection System

**Institution:** Chukwuemeka Odumegwu Ojukwu University (COOU), Uli Campus, Anambra State, Nigeria  
**Department:** Department of Computer Science  
**Architecture:** Offline-First Full-Stack Single Page Web Application (FastAPI + SQLite + HTML5/CSS3/JS)

---

## Overview

**COOUCodeGuard** is a source-code plagiarism and AI-generated pattern detection platform designed specifically for computer science lecturers and departmental examination boards. It operates **100% offline** on local desktop and laptop machines without internet access or external cloud services, safeguarding student intellectual property and privacy.

The system combines:
1. **Abstract Syntax Tree (AST) Structural Comparison (45% Weight)**: Detects deep structural logic invariants even after student renaming of variables, refactoring loops, or rearranging non-dependent statements across Python, Java, and C++.
2. **Normalized Token Sequence Alignment (25% Weight)**: Identifies sequence patterns and Longest Common Subsequences (LCS) across standardized language tokens.
3. **Winnowing Algorithm Fingerprinting (20% Weight)**: Employs position-independent MOSS-like min-hash sliding windows over $k$-grams for collision-resistant matching.
4. **Normalized Text Similarity (10% Weight)**: Strips comments, docstrings, and non-semantic whitespace.
5. **AI-Generated Code Pattern Heuristic Detector**: Flags statistical markers typical of Large Language Model code outputs (such as generic step-by-step explanatory comments, over-regularized docstring schemas, and excessive boilerplate).

---

## Key Features

- **100% Offline Capability**: Runs entirely on localhost with local SQLite database and local filesystem storage.
- **Multi-Language Support**:
  - **Python (`.py`)**: Built-in Python `ast` module parser.
  - **Java (`.java`)**: `javalang` AST parser with syntax fallback.
  - **C++ (`.cpp`, `.cc`, `.h`, `.hpp`)**: Structural grammar tokenizer and AST block extractor.
- **Side-by-Side Dual-Pane Code Diff Viewer**: Synchronized visual diff showing aligned matching code blocks, line numbers, and fast block navigation.
- **AI Pattern Heuristics**: Calculates an AI pattern score with explanatory indicator breakdowns and clear academic review disclaimers.
- **Audit Reports**: Generates formal, print-ready HTML/PDF audit documents with official institutional headers.
- **Pre-Seeded Demo Dataset**: Turnkey out-of-the-box demonstration data featuring COOU computer science courses (CSC 201, CSC 301, CSC 411) and sample plagiarism/AI submissions.

---

## Directory Structure

```
cooucode-guard/
│
├── backend/
│   ├── main.py                  # FastAPI app & static file mounting
│   ├── config.py                # System settings & storage paths
│   ├── database.py              # SQLAlchemy engine & SQLite session
│   ├── auth/                    # JWT & bcrypt authentication
│   ├── models/                  # User, Course, Assignment, Submission, Scan, Comparison, Report
│   ├── schemas/                 # Pydantic data schemas
│   ├── routers/                 # REST API endpoints (Auth, Dashboard, Courses, Submissions, Scans, Reports, System)
│   └── services/                # Safe file storage & demo data seeder
│
├── analysis_engine/
│   ├── python_analyzer.py       # Python AST visitor
│   ├── java_analyzer.py         # Java AST analysis
│   ├── cpp_analyzer.py          # C++ AST analysis
│   ├── tokenizer.py             # Normalization & token streams
│   ├── fingerprinting.py        # Winnowing algorithm & k-gram hashing
│   ├── ast_similarity.py        # AST LCS & structural cosine similarity
│   ├── tree_matching.py         # Block alignment & line match mapper
│   ├── ai_pattern_detector.py   # AI heuristic detector
│   ├── similarity.py            # Multi-layer weighted similarity aggregator
│   └── report_generator.py      # Standalone HTML report generator
│
├── frontend/
│   ├── index.html               # Single Page Application container
│   ├── css/                     # CSS design system (variables, layout, components, code_viewer)
│   └── js/                      # SPA router, state, API client, views, offline vendors
│
├── storage/                     # Local filesystem storage for submissions and reports
├── database/                    # SQLite database file (cooucode_guard.db)
├── tests/                       # Automated unit and integration test suite
├── requirements.txt
└── run.py                       # Single-command launcher
```

---

## Quick Start Guide

### 1. Installation

Clone or extract the repository, open a terminal in the project directory, and install dependencies:

```bash
pip install -r requirements.txt
```

### 2. Launch the Application

Run the turnkey launch script:

```bash
python run.py
```

The server will automatically start at `http://127.0.0.1:8000` and launch your default web browser.

### 3. Demo Credentials

The system automatically initializes with pre-configured demonstration accounts:

- **Lecturer Account**:
  - **Email:** `lecturer@coou.edu.ng`
  - **Password:** `coouguard2026`
- **Department Admin Account**:
  - **Email:** `admin@coou.edu.ng`
  - **Password:** `admin2026`

*(You can also use the **"Auto-Fill Demo Account"** button on the login screen or register your own lecturer account).*

---

## Running Automated Tests

Run the comprehensive test suite with `pytest`:

```bash
pytest tests/ -v
```

---

## Academic Disclaimer

Similarity metrics and AI pattern detection scores produced by COOUCodeGuard are statistical heuristic indicators intended to guide academic review by departmental lecturers. They do not automatically constitute conclusive proof of academic dishonesty. Final decisions remain strictly the prerogative of the course lecturer and the departmental academic integrity board.
