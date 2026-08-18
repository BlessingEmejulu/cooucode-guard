from datetime import datetime
from sqlalchemy.orm import Session
from backend.models import User, Course, Assignment, Submission, Scan, Comparison, Report
from backend.auth.security import get_password_hash
from backend.services.storage_service import StorageService
from analysis_engine.similarity import SimilarityEngine
from analysis_engine.ai_pattern_detector import AIPatternDetector
from analysis_engine.report_generator import ReportGenerator

def seed_demo_data(db: Session):
    # Check if data already exists
    if db.query(User).first():
        return

    # 1. Create Demo Users (Lecturer, Admin, and Student)
    lecturer = User(
        full_name="Dr. Chukwuma Eze (COOU CS)",
        email="lecturer@coou.edu.ng",
        password_hash=get_password_hash("coouguard2026"),
        role="lecturer"
    )
    admin = User(
        full_name="Department Admin (COOU HOD)",
        email="admin@coou.edu.ng",
        password_hash=get_password_hash("admin2026"),
        role="admin"
    )
    student = User(
        full_name="Okonkwo Emeka (Student)",
        email="student@coou.edu.ng",
        matric_number="2022/COOU/CSC/042",
        password_hash=get_password_hash("cooustudent2026"),
        role="student"
    )
    db.add_all([lecturer, admin, student])
    db.commit()
    db.refresh(lecturer)

    # 2. Create Courses
    csc201 = Course(
        course_code="CSC 201",
        course_title="Computer Programming I (Python)",
        semester="First Semester 2025/2026"
    )
    csc301 = Course(
        course_code="CSC 301",
        course_title="Object-Oriented Programming (Java)",
        semester="First Semester 2025/2026"
    )
    csc411 = Course(
        course_code="CSC 411",
        course_title="Algorithms & Data Structures (C++)",
        semester="First Semester 2025/2026"
    )
    db.add_all([csc201, csc301, csc411])
    db.commit()
    db.refresh(csc201)
    db.refresh(csc301)
    db.refresh(csc411)

    # 3. Create Assignments
    asg_py = Assignment(
        course_id=csc201.id,
        title="Lab 2: Shortest Path & Graph Search Algorithms",
        description="Implement Dijkstra's algorithm and Breadth-First Search for a weighted adjacency graph in Python."
    )
    asg_java = Assignment(
        course_id=csc301.id,
        title="Project 1: Campus Banking & Account Management System",
        description="Design an OOP account hierarchy (SavingsAccount, CurrentAccount) with deposit, withdrawal, and transaction logging."
    )
    asg_cpp = Assignment(
        course_id=csc411.id,
        title="Assignment 3: Dynamic Matrix Multiplication & Benchmarking",
        description="Implement Strassen and Standard 2D Matrix multiplication with memory allocation in C++."
    )
    db.add_all([asg_py, asg_java, asg_cpp])
    db.commit()
    db.refresh(asg_py)
    db.refresh(asg_java)
    db.refresh(asg_cpp)

    # 4. Source Code Samples
    # Python Original (Student A - Okonkwo Emeka)
    py_code_a = '''import heapq

def dijkstra_shortest_path(graph, start_vertex):
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start_vertex] = 0
    pq = [(0, start_vertex)]
    visited = set()

    while pq:
        current_distance, current_vertex = heapq.heappop(pq)

        if current_vertex in visited:
            continue
        visited.add(current_vertex)

        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))

    return distances

def find_all_paths(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if start not in graph:
        return []
    paths = []
    for node in graph[start]:
        if node not in path:
            newpaths = find_all_paths(graph, node, end, path)
            for p in newpaths:
                paths.append(p)
    return paths
'''

    # Python Plagiarized Variant (Student B - Nnamdi Chinedu)
    py_code_b = '''import heapq

def dijkstra_shortest_path(network_map, source_node):
    # Calculate shortest route using priority queue
    cost_table = {node: float('infinity') for node in network_map}
    cost_table[source_node] = 0
    p_queue = [(0, source_node)]
    seen_nodes = set()

    while p_queue:
        curr_dist, curr_node = heapq.heappop(p_queue)

        if curr_node in seen_nodes:
            continue
        seen_nodes.add(curr_node)

        for adjacent, edge_weight in network_map[curr_node].items():
            new_dist = curr_dist + edge_weight
            if new_dist < cost_table[adjacent]:
                cost_table[adjacent] = new_dist
                heapq.heappush(p_queue, (new_dist, adjacent))

    return cost_table

def find_all_paths(net, start_pt, target_pt, current_route=[]):
    # Route search recursion
    current_route = current_route + [start_pt]
    if start_pt == target_pt:
        return [current_route]
    if start_pt not in net:
        return []
    result_routes = []
    for neighbor_node in net[start_pt]:
        if neighbor_node not in current_route:
            sub_paths = find_all_paths(net, neighbor_node, target_pt, current_route)
            for item in sub_paths:
                result_routes.append(item)
    return result_routes
'''

    # Python AI-Generated Code Sample (Student C - Amadi Kinsley)
    py_code_ai = '''"""
Module: Graph Traversal and Shortest Path Utilities
Author: Student Solution
Date: 2026-08-17
"""

import heapq
from typing import Dict, List, Tuple, Any

def dijkstra_shortest_path(graph: Dict[str, Dict[str, float]], start_node: str) -> Dict[str, float]:
    """
    Computes the shortest paths from a single starting vertex to all other vertices.
    
    Parameters:
        graph (Dict[str, Dict[str, float]]): Weighted adjacency dictionary.
        start_node (str): The initial source vertex.
        
    Returns:
        Dict[str, float]: Dictionary mapping each vertex to its minimum distance.
        
    Time Complexity: O((V + E) log V)
    Space Complexity: O(V)
    """
    # Step 1: Initialize distances with infinity
    distances: Dict[str, float] = {vertex: float('inf') for vertex in graph}
    distances[start_node] = 0.0
    
    # Step 2: Initialize min-heap priority queue
    priority_queue: List[Tuple[float, str]] = [(0.0, start_node)]
    visited_vertices = set()
    
    # Step 3: Loop through the priority queue until empty
    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)
        
        # Check if vertex was already evaluated
        if current_vertex in visited_vertices:
            continue
        visited_vertices.add(current_vertex)
        
        # Step 4: Iterate over adjacent neighbor edges
        for neighbor, weight in graph.get(current_vertex, {}).items():
            calculated_distance = current_distance + weight
            
            # Step 5: Relax the edge if a shorter path is discovered
            if calculated_distance < distances[neighbor]:
                distances[neighbor] = calculated_distance
                heapq.heappush(priority_queue, (calculated_distance, neighbor))
                
    # Return the final computed shortest distances
    return distances

# Example usage driver code
if __name__ == "__main__":
    sample_network = {
        'A': {'B': 4, 'C': 2},
        'B': {'A': 4, 'C': 1, 'D': 5},
        'C': {'A': 2, 'B': 1, 'D': 8},
        'D': {'B': 5, 'C': 8}
    }
    result = dijkstra_shortest_path(sample_network, 'A')
    print("Computed shortest paths:", result)
'''

    # Python Independent Code (Student D - Chioma Blessing)
    py_code_clean = '''def solve_graph_reachability(adj_matrix):
    n = len(adj_matrix)
    reach = [row[:] for row in adj_matrix]
    
    for k in range(n):
        for i in range(n):
            for j in range(n):
                reach[i][j] = reach[i][j] or (reach[i][k] and reach[k][j])
                
    return reach

def print_matrix(mat):
    for r in mat:
        print(" ".join(str(int(x)) for x in r))
'''

    # Java Original (Student E - Ifeanyi Obinna)
    java_code_a = '''package edu.coou.banking;

public class BankAccount {
    private String accountNumber;
    private String accountHolder;
    private double balance;

    public BankAccount(String accountNumber, String accountHolder, double initialBalance) {
        this.accountNumber = accountNumber;
        this.accountHolder = accountHolder;
        this.balance = initialBalance;
    }

    public synchronized void deposit(double amount) {
        if (amount > 0) {
            this.balance += amount;
            System.out.println("Deposited: " + amount + ", New Balance: " + this.balance);
        }
    }

    public synchronized boolean withdraw(double amount) {
        if (amount > 0 && this.balance >= amount) {
            this.balance -= amount;
            System.out.println("Withdrew: " + amount + ", Remaining: " + this.balance);
            return true;
        }
        return false;
    }

    public double getBalance() {
        return this.balance;
    }
}
'''

    # Java Plagiarized Variant (Student F - Uche Cynthia)
    java_code_b = '''package edu.coou.banking;

public class BankAccount {
    private String accId;
    private String clientName;
    private double currentFund;

    public BankAccount(String accId, String clientName, double startingAmount) {
        this.accId = accId;
        this.clientName = clientName;
        this.currentFund = startingAmount;
    }

    public synchronized void deposit(double cashIn) {
        if (cashIn > 0) {
            this.currentFund += cashIn;
            System.out.println("Credit: " + cashIn + ", Balance: " + this.currentFund);
        }
    }

    public synchronized boolean withdraw(double cashOut) {
        if (cashOut > 0 && this.currentFund >= cashOut) {
            this.currentFund -= cashOut;
            System.out.println("Debit: " + cashOut + ", Left: " + this.currentFund);
            return true;
        }
        return false;
    }

    public double getBalance() {
        return this.currentFund;
    }
}
'''

    # C++ Original (Student G - Somtochukwu Victor)
    cpp_code_a = '''#include <iostream>
#include <vector>

class MatrixMultiplier {
public:
    static std::vector<std::vector<int>> multiply(const std::vector<std::vector<int>>& A, const std::vector<std::vector<int>>& B) {
        int rowsA = A.size();
        int colsA = A[0].size();
        int colsB = B[0].size();
        std::vector<std::vector<int>> result(rowsA, std::vector<int>(colsB, 0));

        for (int i = 0; i < rowsA; ++i) {
            for (int j = 0; j < colsB; ++j) {
                for (int k = 0; k < colsA; ++k) {
                    result[i][j] += A[i][k] * B[k][j];
                }
            }
        }
        return result;
    }
};
'''

    # C++ Plagiarized (Student H - Emmanuel Chukwudi)
    cpp_code_b = '''#include <iostream>
#include <vector>

class MatrixMultiplier {
public:
    static std::vector<std::vector<int>> multiply(const std::vector<std::vector<int>>& mat1, const std::vector<std::vector<int>>& mat2) {
        int r1 = mat1.size();
        int c1 = mat1[0].size();
        int c2 = mat2[0].size();
        std::vector<std::vector<int>> product(r1, std::vector<int>(c2, 0));

        for (int row = 0; row < r1; ++row) {
            for (int col = 0; col < c2; ++col) {
                for (int mid = 0; mid < c1; ++mid) {
                    product[row][col] += mat1[row][mid] * mat2[mid][col];
                }
            }
        }
        return product;
    }
};
'''

    submissions_info = [
        ("Okonkwo Emeka", "2022/COOU/CSC/042", csc201.id, asg_py.id, "dijkstra.py", py_code_a),
        ("Nnamdi Chinedu", "2022/COOU/CSC/089", csc201.id, asg_py.id, "graph_solver.py", py_code_b),
        ("Amadi Kinsley", "2022/COOU/CSC/115", csc201.id, asg_py.id, "shortest_path.py", py_code_ai),
        ("Chioma Blessing", "2022/COOU/CSC/014", csc201.id, asg_py.id, "reachability.py", py_code_clean),
        ("Ifeanyi Obinna", "2021/COOU/CSC/058", csc301.id, asg_java.id, "BankAccount.java", java_code_a),
        ("Uche Cynthia", "2021/COOU/CSC/073", csc301.id, asg_java.id, "AccountManager.java", java_code_b),
        ("Somtochukwu Victor", "2020/COOU/CSC/003", csc411.id, asg_cpp.id, "matrix_mult.cpp", cpp_code_a),
        ("Emmanuel Chukwudi", "2020/COOU/CSC/061", csc411.id, asg_cpp.id, "fast_matrix.cpp", cpp_code_b),
    ]

    saved_subs = []
    for s_name, matric, course_id, asg_id, fname, code in submissions_info:
        rel_path, fhash, lang = StorageService.save_submission_file(matric, fname, code)
        sub = Submission(
            student_name=s_name,
            matric_number=matric,
            course_id=course_id,
            assignment_id=asg_id,
            language=lang,
            file_name=fname,
            file_path=rel_path,
            source_hash=fhash,
            source_code=code
        )
        db.add(sub)
        saved_subs.append(sub)

    db.commit()
    for s in saved_subs:
        db.refresh(s)

    # 5. Run Initial Scans & Reports for Demo Submissions
    sub_map = {s.matric_number: s for s in saved_subs}

    # Scan 1: Nnamdi Chinedu (Plagiarized from Okonkwo Emeka)
    target_sub = sub_map["2022/COOU/CSC/089"]
    peer_sub = sub_map["2022/COOU/CSC/042"]
    
    comp_result = SimilarityEngine.compare_pair(target_sub.source_code, peer_sub.source_code, target_sub.language)
    ai_result = AIPatternDetector.analyze(target_sub.source_code, target_sub.language)

    scan_1 = Scan(
        submission_id=target_sub.id,
        user_id=lecturer.id,
        scan_type="repository",
        overall_similarity=comp_result["overall_similarity"],
        ast_similarity=comp_result["ast_similarity"],
        token_similarity=comp_result["token_similarity"],
        fingerprint_similarity=comp_result["fingerprint_similarity"],
        normalized_similarity=comp_result["normalized_similarity"],
        ai_pattern_score=ai_result["ai_pattern_score"],
        ai_pattern_details=ai_result,
        risk_level=comp_result["risk_level"],
        status="completed"
    )
    db.add(scan_1)
    db.commit()
    db.refresh(scan_1)

    comp_1 = Comparison(
        scan_id=scan_1.id,
        submission_a_id=target_sub.id,
        submission_b_id=peer_sub.id,
        similarity_score=comp_result["overall_similarity"],
        ast_similarity=comp_result["ast_similarity"],
        token_similarity=comp_result["token_similarity"],
        fingerprint_similarity=comp_result["fingerprint_similarity"],
        normalized_similarity=comp_result["normalized_similarity"],
        matching_blocks=comp_result["matching_blocks"]
    )
    db.add(comp_1)
    db.commit()

    # Generate HTML Report for Scan 1
    report_html_1 = ReportGenerator.generate_html_report(
        scan_data={
            "id": scan_1.id,
            "overall_similarity": scan_1.overall_similarity,
            "ast_similarity": scan_1.ast_similarity,
            "token_similarity": scan_1.token_similarity,
            "fingerprint_similarity": scan_1.fingerprint_similarity,
            "normalized_similarity": scan_1.normalized_similarity,
            "risk_level": scan_1.risk_level,
            "ai_pattern_score": scan_1.ai_pattern_score
        },
        student_info={
            "student_name": target_sub.student_name,
            "matric_number": target_sub.matric_number,
            "course_code": "CSC 201",
            "assignment_title": "Lab 2: Shortest Path & Graph Search Algorithms",
            "language": target_sub.language,
            "file_name": target_sub.file_name
        },
        comparison_matches=[{
            "submission_b": {
                "student_name": peer_sub.student_name,
                "matric_number": peer_sub.matric_number,
                "file_name": peer_sub.file_name
            },
            "similarity_score": comp_result["overall_similarity"],
            "ast_similarity": comp_result["ast_similarity"],
            "token_similarity": comp_result["token_similarity"],
            "fingerprint_similarity": comp_result["fingerprint_similarity"],
            "normalized_similarity": comp_result["normalized_similarity"],
            "matching_blocks": comp_result["matching_blocks"]
        }],
        ai_details=ai_result
    )
    report_path_1 = ReportGenerator.save_report_file(scan_1.id, report_html_1)
    rep_1 = Report(
        scan_id=scan_1.id,
        title=f"Plagiarism Audit - {target_sub.student_name} ({target_sub.matric_number})",
        file_path=str(report_path_1),
        report_format="HTML",
        summary_data={"overall_similarity": scan_1.overall_similarity, "risk_level": scan_1.risk_level}
    )
    db.add(rep_1)

    # Scan 2: Amadi Kinsley (AI-generated code)
    ai_sub = sub_map["2022/COOU/CSC/115"]
    ai_comp_result = SimilarityEngine.compare_pair(ai_sub.source_code, peer_sub.source_code, ai_sub.language)
    ai_det = AIPatternDetector.analyze(ai_sub.source_code, ai_sub.language)

    scan_2 = Scan(
        submission_id=ai_sub.id,
        user_id=lecturer.id,
        scan_type="repository",
        overall_similarity=ai_comp_result["overall_similarity"],
        ast_similarity=ai_comp_result["ast_similarity"],
        token_similarity=ai_comp_result["token_similarity"],
        fingerprint_similarity=ai_comp_result["fingerprint_similarity"],
        normalized_similarity=ai_comp_result["normalized_similarity"],
        ai_pattern_score=ai_det["ai_pattern_score"],
        ai_pattern_details=ai_det,
        risk_level=SimilarityEngine.classify_risk(ai_comp_result["overall_similarity"]),
        status="completed"
    )
    db.add(scan_2)
    db.commit()

    # Scan 3: Java comparison (Uche Cynthia vs Ifeanyi Obinna)
    java_target = sub_map["2021/COOU/CSC/073"]
    java_peer = sub_map["2021/COOU/CSC/058"]
    j_comp = SimilarityEngine.compare_pair(java_target.source_code, java_peer.source_code, java_target.language)
    j_ai = AIPatternDetector.analyze(java_target.source_code, java_target.language)

    scan_3 = Scan(
        submission_id=java_target.id,
        user_id=lecturer.id,
        scan_type="repository",
        overall_similarity=j_comp["overall_similarity"],
        ast_similarity=j_comp["ast_similarity"],
        token_similarity=j_comp["token_similarity"],
        fingerprint_similarity=j_comp["fingerprint_similarity"],
        normalized_similarity=j_comp["normalized_similarity"],
        ai_pattern_score=j_ai["ai_pattern_score"],
        ai_pattern_details=j_ai,
        risk_level=j_comp["risk_level"],
        status="completed"
    )
    db.add(scan_3)
    db.commit()
    db.refresh(scan_3)

    comp_3 = Comparison(
        scan_id=scan_3.id,
        submission_a_id=java_target.id,
        submission_b_id=java_peer.id,
        similarity_score=j_comp["overall_similarity"],
        ast_similarity=j_comp["ast_similarity"],
        token_similarity=j_comp["token_similarity"],
        fingerprint_similarity=j_comp["fingerprint_similarity"],
        normalized_similarity=j_comp["normalized_similarity"],
        matching_blocks=j_comp["matching_blocks"]
    )
    db.add(comp_3)

    # Scan 4: C++ comparison (Emmanuel Chukwudi vs Somtochukwu Victor)
    cpp_target = sub_map["2020/COOU/CSC/061"]
    cpp_peer = sub_map["2020/COOU/CSC/003"]
    c_comp = SimilarityEngine.compare_pair(cpp_target.source_code, cpp_peer.source_code, cpp_target.language)
    c_ai = AIPatternDetector.analyze(cpp_target.source_code, cpp_target.language)

    scan_4 = Scan(
        submission_id=cpp_target.id,
        user_id=lecturer.id,
        scan_type="repository",
        overall_similarity=c_comp["overall_similarity"],
        ast_similarity=c_comp["ast_similarity"],
        token_similarity=c_comp["token_similarity"],
        fingerprint_similarity=c_comp["fingerprint_similarity"],
        normalized_similarity=c_comp["normalized_similarity"],
        ai_pattern_score=c_ai["ai_pattern_score"],
        ai_pattern_details=c_ai,
        risk_level=c_comp["risk_level"],
        status="completed"
    )
    db.add(scan_4)
    db.commit()
    db.refresh(scan_4)

    comp_4 = Comparison(
        scan_id=scan_4.id,
        submission_a_id=cpp_target.id,
        submission_b_id=cpp_peer.id,
        similarity_score=c_comp["overall_similarity"],
        ast_similarity=c_comp["ast_similarity"],
        token_similarity=c_comp["token_similarity"],
        fingerprint_similarity=c_comp["fingerprint_similarity"],
        normalized_similarity=c_comp["normalized_similarity"],
        matching_blocks=c_comp["matching_blocks"]
    )
    db.add(comp_4)
    db.commit()
