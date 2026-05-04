"""Unit tests for the assignment module.

These tests validate parsing logic, validation rules, assignment constraints,
and solver behavior to ensure students are matched to projects correctly.
"""

import random
import time
import unittest

from datadivas.assignment import (
    AssignmentError,
    assign_students_to_projects,
    parse_projects,
    parse_student_rankings,
)


class AssignmentTests(unittest.TestCase):
    """Test suite for assignment logic and input validation."""
    def test_parse_projects_valid(self):
        """Test parsing valid project definitions with capacities 4-6 and majors."""
        text = "Project A,4,CS,CpE\nProject B,5,EE"
        result = parse_projects(text)
        expected = {
            "Project A": {"capacity": 4, "allowed_majors": ["CS", "CpE"]},
            "Project B": {"capacity": 5, "allowed_majors": ["EE"]}
        }
        self.assertEqual(result, expected)

    def test_parse_projects_invalid_capacity(self):
        """Test that capacities outside 4-6 range raise an error."""
        text = "Project A,3,CS\nProject B,7,EE"
        with self.assertRaises(AssignmentError):
            parse_projects(text)

    def test_parse_students_valid(self):
        """Test parsing valid student rankings with majors."""
        text = "Alice (CS): Project A, Project B\nBob (CpE): Project B"
        result = parse_student_rankings(text)
        expected = {
            "Alice": {"rankings": ["Project A", "Project B"], "major": "CS"},
            "Bob": {"rankings": ["Project B"], "major": "CpE"}
        }
        self.assertEqual(result, expected)

    def test_assign_students_to_projects_prefers_top_choices(self):
        """Test that the algorithm prioritizes students' top preferences when possible."""
        students = {
            "Alice": {"rankings": ["Project X", "Project Y"], "major": "CS"},
            "Bob": {"rankings": ["Project X", "Project Y"], "major": "CS"},
            "Frank": {"rankings": ["Project X", "Project Y"], "major": "EE"},
            "Grace": {"rankings": ["Project X", "Project Y"], "major": "CS"},
            "Carmen": {"rankings": ["Project Y", "Project X"], "major": "EE"},
            "Diana": {"rankings": ["Project Y", "Project X"], "major": "EE"},
            "Eve": {"rankings": ["Project Y", "Project X"], "major": "CS"},
            "Heidi": {"rankings": ["Project Y", "Project X"], "major": "EE"},
        }
        projects = {
            "Project X": {"capacity": 4, "allowed_majors": ["CS", "EE"]},
            "Project Y": {"capacity": 4, "allowed_majors": ["CS", "EE"]}
        }
        result = assign_students_to_projects(students, projects)
        assignments = result['assignments']
        self.assertEqual(assignments["Alice"], "Project X")
        self.assertEqual(assignments["Bob"], "Project X")
        self.assertEqual(assignments["Frank"], "Project X")
        self.assertEqual(assignments["Grace"], "Project X")
        self.assertEqual(assignments["Carmen"], "Project Y")
        self.assertEqual(assignments["Diana"], "Project Y")
        self.assertEqual(assignments["Eve"], "Project Y")
        self.assertEqual(assignments["Heidi"], "Project Y")

    def test_assign_students_limits_capacity(self):
        """Test that project capacity limits are enforced.
        
        When more students want a project than its capacity allows, some should
        be assigned elsewhere or left unassigned.
        """
        students = {
            "Alice": {"rankings": ["Project A", "Project B"], "major": "CS"},
            "Bob": {"rankings": ["Project A", "Project B"], "major": "CS"},
            "Carmen": {"rankings": ["Project A", "Project B"], "major": "EE"},
            "Diana": {"rankings": ["Project A", "Project B"], "major": "EE"},
            "Eve": {"rankings": ["Project A", "Project B"], "major": "CS"},
            "Frank": {"rankings": ["Project A", "Project B"], "major": "EE"},
        }
        projects = {
            "Project A": {"capacity": 4, "allowed_majors": ["CS", "EE"]},
            "Project B": {"capacity": 4, "allowed_majors": ["CS", "EE"]}
        }
        result = assign_students_to_projects(students, projects)
        assignments = result['assignments']
        assigned = [assignments[name] for name in students]
        self.assertEqual(assigned.count("Project A"), 4)
        self.assertTrue(any(project is None for project in assigned))

    def test_minimum_capacity_enforcement(self):
        students = {
            "Alice": {"rankings": ["Project A"], "major": "CS"},
            "Bob": {"rankings": ["Project A"], "major": "CS"},
            "Carmen": {"rankings": ["Project A"], "major": "EE"},
            "Diana": {"rankings": ["Project A"], "major": "EE"},
            "Eve": {"rankings": ["Project A"], "major": "CS"},
        }
        projects = {"Project A": {"capacity": 4, "allowed_majors": ["CS", "EE"]}}
        result = assign_students_to_projects(students, projects)
        assignments = result['assignments']
        assigned = [assignments[name] for name in students]
        self.assertEqual(assigned.count("Project A"), 4)
        self.assertEqual(assigned.count(None), 1)

    def test_assign_students_unassigned_when_no_space(self):
        students = {
            "Alice": {"rankings": ["Project A"], "major": "CS"},
            "Bob": {"rankings": ["Project A"], "major": "EE"}
        }
        projects = {"Project A": {"capacity": 0, "allowed_majors": ["CS", "EE"]}}
        result = assign_students_to_projects(students, projects)
        assignments = result['assignments']
        self.assertEqual(assignments["Alice"], None)
        self.assertEqual(assignments["Bob"], None)

    def test_invalid_project_name_in_rankings(self):
        students = {
            "Alice": {"rankings": ["Project Z"], "major": "CS"}
        }
        projects = {"Project A": {"capacity": 4, "allowed_majors": ["CS"]}}
        with self.assertRaises(AssignmentError):
            assign_students_to_projects(students, projects)

    def test_major_exclusion(self):
        """Test that students are not assigned to projects that don't allow their major."""
        students = {
            "Alice": {"rankings": ["Project CS", "Project Mixed"], "major": "EE"},
            "Bob": {"rankings": ["Project CS"], "major": "CS"},
            "Carmen": {"rankings": ["Project CS"], "major": "CS"},
            "Diana": {"rankings": ["Project CS"], "major": "CS"},
            "Eve": {"rankings": ["Project CS"], "major": "CS"},
        }
        projects = {
            "Project CS": {"capacity": 4, "allowed_majors": ["CS"]},
            "Project Mixed": {"capacity": 4, "allowed_majors": ["CS", "EE"]}
        }
        result = assign_students_to_projects(students, projects)
        assignments = result['assignments']
        # Alice (EE) should not be assigned to Project CS
        self.assertNotEqual(assignments["Alice"], "Project CS")
        # But she can be assigned to Project Mixed or unassigned
        self.assertTrue(assignments["Alice"] in [None, "Project Mixed"])

    def test_sparse_ranking_parsing(self):
        """Test parsing student rankings with sparse (empty) choices."""
        text = "Alice (CS): Project A, Project B, Project C, , , "
        result = parse_student_rankings(text)
        expected = {
            "Alice": {"rankings": ["Project A", "Project B", "Project C"], "major": "CS"}
        }
        self.assertEqual(result, expected)
        # Now test assignment with this parsed data
        students = result
        projects = {
            "Project A": {"capacity": 4, "allowed_majors": ["CS"]},
            "Project B": {"capacity": 4, "allowed_majors": ["CS"]},
            "Project C": {"capacity": 4, "allowed_majors": ["CS"]}
        }
        # Add more students to fill projects
        students.update({
            "Bob": {"rankings": ["Project A"], "major": "CS"},
            "Carmen": {"rankings": ["Project A"], "major": "CS"},
            "Diana": {"rankings": ["Project A"], "major": "CS"},
        })
        result_assign = assign_students_to_projects(students, projects)
        assignments = result_assign['assignments']
        # Alice should be assigned to one of her top 3 choices
        self.assertIn(assignments["Alice"], ["Project A", "Project B", "Project C"])

    def test_diversity_tie_breaker(self):
        """Test that diversity penalties break ties in favor of mixed teams."""
        students = {
            "Alice": {"rankings": ["Project Mixed", "Project Mono"], "major": "CS"},
            "Bob": {"rankings": ["Project Mixed", "Project Mono"], "major": "CS"},
            "Carmen": {"rankings": ["Project Mixed", "Project Mono"], "major": "EE"},
            "Diana": {"rankings": ["Project Mixed", "Project Mono"], "major": "EE"},
            "Eve": {"rankings": ["Project Mixed", "Project Mono"], "major": "CS"},
            "Frank": {"rankings": ["Project Mixed", "Project Mono"], "major": "CS"},
            "Grace": {"rankings": ["Project Mixed", "Project Mono"], "major": "EE"},
            "Heidi": {"rankings": ["Project Mixed", "Project Mono"], "major": "EE"},
        }
        projects = {
            "Project Mixed": {"capacity": 4, "allowed_majors": ["CS", "EE"]},
            "Project Mono": {"capacity": 4, "allowed_majors": ["CS", "EE"]}
        }
        result = assign_students_to_projects(students, projects)
        assignments = result['assignments']
        project_compositions = result['project_compositions']
        # Check that Project Mixed has both majors
        mixed_comp = project_compositions.get("Project Mixed", {})
        self.assertGreater(mixed_comp.get("CS", 0), 0)
        self.assertGreater(mixed_comp.get("EE", 0), 0)
        # And Project Mono might be all one major, but since diversity is penalized, solver should prefer mixed
        # The test verifies the solver selects mixed when possible


    def test_large_scale_assignment(self):
        """Scalability stress test for large-scale assignments."""
        # Generate 20 projects
        majors = ['CS', 'CpE', 'EE']
        projects = {}
        project_names = [f"Project {i+1}" for i in range(20)]
        for name in project_names:
            # Randomly select 1-3 allowed majors
            allowed = random.sample(majors, random.randint(1, 3))
            projects[name] = {"capacity": 6, "allowed_majors": allowed}

        # Generate 100 students
        students = {}
        for i in range(100):
            name = f"Student {i+1}"
            major = random.choice(majors)
            # Random 3 rankings from project_names
            rankings = random.sample(project_names, 3)
            students[name] = {"rankings": rankings, "major": major}

        # Measure time
        start_time = time.time()
        result = assign_students_to_projects(students, projects)
        end_time = time.time()
        total_time = end_time - start_time

        # Print time for feedback
        print(f"STRESS_TEST_TIME: {total_time:.2f}s")

        # Assertions
        self.assertLess(total_time, 5.0, "Assignment should complete in under 5 seconds")

        # Verify Nixing Rule and Capacity Limits
        assignments = result['assignments']
        project_compositions = result['project_compositions']
        for proj_name in projects:
            comp = project_compositions.get(proj_name, {})
            if comp:  # Active project
                assigned_count = sum(comp.values())
                self.assertGreaterEqual(assigned_count, 4, f"Active project {proj_name} must have at least 4 students")
                self.assertLessEqual(assigned_count, 6, f"Project {proj_name} exceeds capacity of 6")
            else:  # Inactive project
                # Should have 0 students
                assigned_students = [s for s, p in assignments.items() if p == proj_name]
                self.assertEqual(len(assigned_students), 0, f"Inactive project {proj_name} should have no assignments")


if __name__ == "__main__":
    unittest.main()