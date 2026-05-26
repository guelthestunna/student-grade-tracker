#!/usr/bin/env python3
"""
╔══════════════════════════════════════════╗
║       STUDENT GRADE TRACKER v1.0        ║
║     Track subjects, grades & GPA        ║
╚══════════════════════════════════════════╝
Pure Python — no external libraries needed.
Data is saved to grades_data.json
"""

import json
import os
import sys
import datetime
from typing import Optional

# ── Constants ────────────────────────────────────────────────────────────────

DATA_FILE = "grades_data.json"

# Grade to GPA point mapping (standard Philippine/US grading)
GRADE_SCALE = [
    (97, 100, "A+", 4.0),
    (93, 96,  "A",  4.0),
    (90, 92,  "A-", 3.7),
    (87, 89,  "B+", 3.3),
    (83, 86,  "B",  3.0),
    (80, 82,  "B-", 2.7),
    (77, 79,  "C+", 2.3),
    (73, 76,  "C",  2.0),
    (70, 72,  "C-", 1.7),
    (67, 69,  "D+", 1.3),
    (65, 66,  "D",  1.0),
    (0,  64,  "F",  0.0),
]

REMARKS = {
    "A+": "Outstanding",
    "A":  "Excellent",
    "A-": "Very Good",
    "B+": "Good",
    "B":  "Above Average",
    "B-": "Average",
    "C+": "Satisfactory",
    "C":  "Passing",
    "C-": "Barely Passing",
    "D+": "Poor",
    "D":  "Very Poor",
    "F":  "Failed",
}

# ── ANSI Colors ───────────────────────────────────────────────────────────────

class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    # Foreground
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"
    GRAY    = "\033[90m"
    # Background
    BG_BLUE = "\033[44m"
    BG_CYAN = "\033[46m"

def b(text): return f"{C.BOLD}{text}{C.RESET}"
def c(text, color): return f"{color}{text}{C.RESET}"
def grade_color(letter):
    if letter in ("A+", "A", "A-"): return C.GREEN
    if letter in ("B+", "B", "B-"): return C.CYAN
    if letter in ("C+", "C", "C-"): return C.YELLOW
    return C.RED

# ── Data Layer ────────────────────────────────────────────────────────────────

def load_data() -> dict:
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {"students": {}, "created_at": str(datetime.date.today())}

def save_data(data: dict):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ── Grade Utilities ───────────────────────────────────────────────────────────

def score_to_letter(score: float) -> tuple[str, float]:
    for low, high, letter, points in GRADE_SCALE:
        if low <= score <= high:
            return letter, points
    return "F", 0.0

def compute_gpa(subjects: dict) -> Optional[float]:
    if not subjects:
        return None
    total_points = 0.0
    total_units  = 0
    for s in subjects.values():
        if s["grades"]:
            avg = sum(s["grades"]) / len(s["grades"])
            _, pts = score_to_letter(avg)
            units = s.get("units", 3)
            total_points += pts * units
            total_units  += units
    if total_units == 0:
        return None
    return round(total_points / total_units, 3)

def subject_average(subject: dict) -> Optional[float]:
    if not subject["grades"]:
        return None
    return round(sum(subject["grades"]) / len(subject["grades"]), 2)

def gpa_remark(gpa: float) -> str:
    if gpa >= 3.7: return c("Dean's Lister 🏆", C.GREEN)
    if gpa >= 3.0: return c("Good Standing ✓", C.CYAN)
    if gpa >= 2.0: return c("Satisfactory", C.YELLOW)
    if gpa >= 1.0: return c("At Risk ⚠", C.YELLOW)
    return c("Failing ✗", C.RED)

# ── Display Helpers ───────────────────────────────────────────────────────────

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    print(c("""
╔══════════════════════════════════════════════╗
║         STUDENT GRADE TRACKER v1.0          ║
║   Track · Analyze · Improve Your Grades     ║
╚══════════════════════════════════════════════╝""", C.CYAN))

def divider(char="─", width=50):
    print(c(char * width, C.GRAY))

def pause():
    input(c("\n  Press Enter to continue...", C.GRAY))

def ask(prompt, default=None) -> str:
    suffix = f" [{default}]" if default else ""
    val = input(f"  {c('›', C.CYAN)} {prompt}{suffix}: ").strip()
    return val if val else (default or "")

def ask_float(prompt, lo=0, hi=100) -> Optional[float]:
    while True:
        raw = ask(prompt)
        if raw.lower() in ("q", "quit", "cancel"):
            return None
        try:
            val = float(raw)
            if lo <= val <= hi:
                return val
            print(c(f"  ✗ Must be between {lo} and {hi}.", C.RED))
        except ValueError:
            print(c("  ✗ Please enter a valid number.", C.RED))

def ask_int(prompt, lo=1, hi=6) -> Optional[int]:
    while True:
        raw = ask(prompt)
        if raw.lower() in ("q", "quit", "cancel"):
            return None
        try:
            val = int(raw)
            if lo <= val <= hi:
                return val
            print(c(f"  ✗ Must be between {lo} and {hi}.", C.RED))
        except ValueError:
            print(c("  ✗ Please enter a whole number.", C.RED))

# ── Student Management ────────────────────────────────────────────────────────

def list_students(data: dict):
    students = data["students"]
    if not students:
        print(c("  No students found.", C.GRAY))
        return
    print(f"\n  {b('ID'):<6}  {b('Name'):<22}  {b('Subjects'):<10}  {b('GPA'):<8}  {b('Standing')}")
    divider()
    for sid, st in students.items():
        gpa = compute_gpa(st["subjects"])
        gpa_str = f"{gpa:.2f}" if gpa else "—"
        gpa_col = C.GREEN if gpa and gpa >= 3.0 else (C.YELLOW if gpa and gpa >= 2.0 else C.RED)
        standing = gpa_remark(gpa) if gpa else c("No grades", C.GRAY)
        print(f"  {c(sid, C.CYAN):<15}  {st['name']:<22}  {len(st['subjects']):<10}  "
              f"{c(gpa_str, gpa_col):<18}  {standing}")

def select_student(data: dict) -> Optional[str]:
    list_students(data)
    if not data["students"]:
        return None
    sid = ask("\nEnter Student ID (or 'q' to cancel)").upper()
    if sid in ("Q", ""):
        return None
    if sid not in data["students"]:
        print(c("  ✗ Student not found.", C.RED))
        return None
    return sid

def add_student(data: dict):
    print(f"\n  {b('── Add New Student ──')}")
    name = ask("Full Name")
    if not name:
        print(c("  ✗ Name cannot be empty.", C.RED))
        return
    # Auto-generate ID from initials + timestamp
    initials = "".join(w[0].upper() for w in name.split() if w)
    ts = str(int(datetime.datetime.now().timestamp()))[-4:]
    sid = f"{initials}{ts}"
    if sid in data["students"]:
        sid += "X"
    year = ask("Year Level (1–5)", "1")
    section = ask("Section / Block", "A")
    data["students"][sid] = {
        "name": name,
        "year": year,
        "section": section,
        "subjects": {},
        "added": str(datetime.date.today()),
    }
    save_data(data)
    print(c(f"\n  ✓ Student '{name}' added! ID: {sid}", C.GREEN))

def remove_student(data: dict):
    print(f"\n  {b('── Remove Student ──')}")
    sid = select_student(data)
    if not sid:
        return
    name = data["students"][sid]["name"]
    confirm = ask(f"Delete '{name}' and ALL their grades? (yes/no)", "no")
    if confirm.lower() == "yes":
        del data["students"][sid]
        save_data(data)
        print(c(f"  ✓ Student '{name}' removed.", C.GREEN))
    else:
        print(c("  Cancelled.", C.GRAY))

# ── Subject Management ────────────────────────────────────────────────────────

def view_subjects(student: dict):
    subjects = student["subjects"]
    if not subjects:
        print(c("  No subjects enrolled.", C.GRAY))
        return
    print(f"\n  {b('Subject'):<28}  {b('Units'):<6}  {b('Grades'):<30}  "
          f"{b('Avg'):<8}  {b('Letter'):<8}  {b('Remark')}")
    divider(width=100)
    for sname, s in subjects.items():
        avg = subject_average(s)
        if avg is not None:
            letter, _ = score_to_letter(avg)
            col = grade_color(letter)
            avg_str = f"{avg:.1f}"
            letter_str = c(letter, col)
            remark = c(REMARKS.get(letter, ""), col)
        else:
            avg_str = "—"
            letter_str = c("—", C.GRAY)
            remark = c("No grades yet", C.GRAY)
        grades_str = ", ".join(f"{g:.1f}" for g in s["grades"]) if s["grades"] else c("none", C.GRAY)
        units = s.get("units", 3)
        print(f"  {sname:<28}  {units:<6}  {grades_str:<30}  {avg_str:<8}  {letter_str:<18}  {remark}")

def add_subject(data: dict, sid: str):
    student = data["students"][sid]
    print(f"\n  {b('── Add Subject ──')}  (for {student['name']})")
    sname = ask("Subject Name (e.g. 'Data Structures')").strip().title()
    if not sname:
        print(c("  ✗ Subject name cannot be empty.", C.RED))
        return
    if sname in student["subjects"]:
        print(c("  ✗ Subject already exists.", C.RED))
        return
    units = ask_int("Credit Units (1–6)", lo=1, hi=6)
    if units is None:
        return
    student["subjects"][sname] = {"grades": [], "units": units}
    save_data(data)
    print(c(f"  ✓ Subject '{sname}' added ({units} units).", C.GREEN))

def remove_subject(data: dict, sid: str):
    student = data["students"][sid]
    view_subjects(student)
    if not student["subjects"]:
        return
    sname = ask("\nSubject name to remove (or 'q' to cancel)").strip().title()
    if sname.lower() == "q" or not sname:
        return
    if sname not in student["subjects"]:
        print(c("  ✗ Subject not found.", C.RED))
        return
    del student["subjects"][sname]
    save_data(data)
    print(c(f"  ✓ Subject '{sname}' removed.", C.GREEN))

# ── Grade Entry ───────────────────────────────────────────────────────────────

def add_grade(data: dict, sid: str):
    student = data["students"][sid]
    view_subjects(student)
    if not student["subjects"]:
        print(c("\n  Add a subject first.", C.YELLOW))
        return
    print()
    sname = ask("Subject name (or 'q' to cancel)").strip().title()
    if sname.lower() == "q" or not sname:
        return
    if sname not in student["subjects"]:
        print(c("  ✗ Subject not found.", C.RED))
        return
    print(c("  Enter grade (0–100). Type 'q' to stop adding.", C.GRAY))
    subject = student["subjects"][sname]
    added = 0
    while True:
        label = f"Grade #{len(subject['grades']) + 1}"
        score = ask_float(label, 0, 100)
        if score is None:
            break
        letter, pts = score_to_letter(score)
        col = grade_color(letter)
        print(c(f"    → {letter} ({pts:.1f} pts) — {REMARKS.get(letter, '')}", col))
        subject["grades"].append(score)
        added += 1
        more = ask("Add another grade? (y/n)", "y")
        if more.lower() != "y":
            break
    if added:
        save_data(data)
        avg = subject_average(subject)
        letter, _ = score_to_letter(avg)
        print(c(f"\n  ✓ {added} grade(s) added. New average: {avg:.2f} ({letter})", C.GREEN))

def remove_last_grade(data: dict, sid: str):
    student = data["students"][sid]
    view_subjects(student)
    if not student["subjects"]:
        return
    sname = ask("\nSubject name (or 'q' to cancel)").strip().title()
    if sname.lower() == "q" or not sname:
        return
    if sname not in student["subjects"]:
        print(c("  ✗ Subject not found.", C.RED))
        return
    grades = student["subjects"][sname]["grades"]
    if not grades:
        print(c("  No grades to remove.", C.YELLOW))
        return
    removed = grades.pop()
    save_data(data)
    print(c(f"  ✓ Removed last grade: {removed:.1f}", C.GREEN))

# ── Reports ───────────────────────────────────────────────────────────────────

def student_report(data: dict, sid: str):
    student = data["students"][sid]
    gpa = compute_gpa(student["subjects"])
    clear()
    banner()
    print(f"\n  {c('═' * 50, C.CYAN)}")
    print(f"  {b('GRADE REPORT')}")
    print(f"  {c('═' * 50, C.CYAN)}")
    print(f"  {b('Name')}    : {student['name']}")
    print(f"  {b('ID')}      : {sid}")
    print(f"  {b('Year')}    : {student['year']}  |  {b('Section')}: {student['section']}")
    print(f"  {b('Date')}    : {datetime.date.today()}")
    print(f"  {c('─' * 50, C.GRAY)}")

    view_subjects(student)

    print(f"\n  {c('─' * 50, C.GRAY)}")
    if gpa is not None:
        gpa_col = C.GREEN if gpa >= 3.0 else (C.YELLOW if gpa >= 2.0 else C.RED)
        print(f"  {b('Cumulative GPA')} : {c(f'{gpa:.3f}', gpa_col)} / 4.000")
        print(f"  {b('Academic Standing')} : {gpa_remark(gpa)}")
    else:
        print(c("  No grades recorded yet.", C.GRAY))
    print(f"  {c('═' * 50, C.CYAN)}\n")

def class_summary(data: dict):
    students = data["students"]
    if not students:
        print(c("  No students found.", C.GRAY))
        return
    clear()
    banner()
    print(f"\n  {b('CLASS SUMMARY REPORT')}  — {datetime.date.today()}")
    divider(width=70)

    gpas = []
    for sid, st in students.items():
        gpa = compute_gpa(st["subjects"])
        if gpa:
            gpas.append(gpa)

    if gpas:
        class_avg = sum(gpas) / len(gpas)
        highest = max(gpas)
        lowest  = min(gpas)
        passing = sum(1 for g in gpas if g >= 2.0)
        print(f"  Total Students   : {b(len(students))}")
        print(f"  With Grades      : {b(len(gpas))}")
        print(f"  Class Avg GPA    : {c(f'{class_avg:.3f}', C.CYAN)}")
        print(f"  Highest GPA      : {c(f'{highest:.3f}', C.GREEN)}")
        print(f"  Lowest GPA       : {c(f'{lowest:.3f}', C.RED)}")
        print(f"  Passing (≥ 2.0)  : {b(passing)} / {len(gpas)}")
        print()

    list_students(data)
    print()

# ── Export ────────────────────────────────────────────────────────────────────

def export_report(data: dict, sid: str):
    student = data["students"][sid]
    gpa = compute_gpa(student["subjects"])
    filename = f"report_{sid}_{datetime.date.today()}.txt"
    lines = []
    lines.append("=" * 55)
    lines.append("        STUDENT GRADE REPORT")
    lines.append("=" * 55)
    lines.append(f"Name    : {student['name']}")
    lines.append(f"ID      : {sid}")
    lines.append(f"Year    : {student['year']}  |  Section: {student['section']}")
    lines.append(f"Date    : {datetime.date.today()}")
    lines.append("-" * 55)
    lines.append(f"{'Subject':<25} {'Units':>5} {'Avg':>7} {'Grade':>6} {'Remark'}")
    lines.append("-" * 55)
    for sname, s in student["subjects"].items():
        avg = subject_average(s)
        if avg is not None:
            letter, _ = score_to_letter(avg)
            remark = REMARKS.get(letter, "")
            lines.append(f"{sname:<25} {s.get('units',3):>5} {avg:>7.2f} {letter:>6}  {remark}")
        else:
            lines.append(f"{sname:<25} {s.get('units',3):>5} {'—':>7} {'—':>6}  No grades")
    lines.append("-" * 55)
    if gpa:
        lines.append(f"Cumulative GPA : {gpa:.3f} / 4.000")
    lines.append("=" * 55)
    with open(filename, "w") as f:
        f.write("\n".join(lines))
    print(c(f"  ✓ Report exported to '{filename}'", C.GREEN))

# ── Menus ─────────────────────────────────────────────────────────────────────

def student_menu(data: dict, sid: str):
    student = data["students"][sid]
    while True:
        clear()
        banner()
        gpa = compute_gpa(student["subjects"])
        gpa_str = f"{gpa:.3f}" if gpa else "No grades yet"
        print(f"\n  {c('Student:', C.GRAY)} {b(student['name'])}  "
              f"{c('|', C.GRAY)}  ID: {c(sid, C.CYAN)}  "
              f"{c('|', C.GRAY)}  GPA: {c(gpa_str, C.GREEN if gpa and gpa >= 3.0 else C.YELLOW)}")
        divider()
        print(f"""
  {b('GRADES')}
  {c('1', C.CYAN)}  View Subjects & Grades
  {c('2', C.CYAN)}  Add Subject
  {c('3', C.CYAN)}  Add Grade to Subject
  {c('4', C.CYAN)}  Remove Last Grade
  {c('5', C.CYAN)}  Remove Subject

  {b('REPORTS')}
  {c('6', C.CYAN)}  Full Grade Report
  {c('7', C.CYAN)}  Export Report to .txt

  {c('0', C.GRAY)}  ← Back
""")
        choice = ask("Choose option")
        if choice == "1":
            clear(); banner()
            print(f"\n  {b(student['name'])} — Subjects\n")
            view_subjects(student)
            pause()
        elif choice == "2":
            add_subject(data, sid)
            pause()
        elif choice == "3":
            add_grade(data, sid)
            pause()
        elif choice == "4":
            remove_last_grade(data, sid)
            pause()
        elif choice == "5":
            remove_subject(data, sid)
            pause()
        elif choice == "6":
            student_report(data, sid)
            pause()
        elif choice == "7":
            export_report(data, sid)
            pause()
        elif choice == "0":
            break
        else:
            print(c("  ✗ Invalid option.", C.RED)); pause()

def main_menu():
    data = load_data()
    while True:
        clear()
        banner()
        count = len(data["students"])
        print(f"  {c('Students tracked:', C.GRAY)} {b(count)}  "
              f"{c('|', C.GRAY)}  Data file: {c(DATA_FILE, C.CYAN)}")
        divider()
        print(f"""
  {b('STUDENTS')}
  {c('1', C.CYAN)}  View All Students
  {c('2', C.CYAN)}  Add New Student
  {c('3', C.CYAN)}  Open Student (view/edit grades)
  {c('4', C.CYAN)}  Remove Student

  {b('REPORTS')}
  {c('5', C.CYAN)}  Class Summary Report

  {c('0', C.RED)}  Exit
""")
        choice = ask("Choose option")
        if choice == "1":
            clear(); banner()
            print(f"\n  {b('All Students')}\n")
            list_students(data)
            pause()
        elif choice == "2":
            add_student(data)
            pause()
        elif choice == "3":
            clear(); banner()
            print(f"\n  {b('Select Student')}\n")
            sid = select_student(data)
            if sid:
                student_menu(data, sid)
        elif choice == "4":
            remove_student(data)
            pause()
        elif choice == "5":
            class_summary(data)
            pause()
        elif choice == "0":
            print(c("\n  Goodbye! Keep studying hard! 📚\n", C.CYAN))
            sys.exit(0)
        else:
            print(c("  ✗ Invalid option.", C.RED)); pause()

# ── Entry Point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(c("\n\n  Exited. See you! 👋\n", C.CYAN))
        sys.exit(0)
