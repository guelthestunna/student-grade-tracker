#Student Grade Tracker

A command-line application built with Python that helps track student grades, compute GPA, and generate academic reports — all from the terminal.

---

Features

- 👤 **Multi-student support** — manage multiple students, each with a unique auto-generated ID
- 📚 **Subject management** — add subjects with custom credit units per student
- 📝 **Grade entry** — log multiple grades per subject (0–100 scale)
- 🔢 **Automatic GPA calculation** — weighted by credit units using a standard 4.0 scale
- 🏆 **Academic standing** — automatically flags Dean's Lister, Good Standing, At Risk, or Failing
- 📋 **Class summary report** — overview of all students with GPA rankings
- 💾 **Export to .txt** — save a clean grade report file for any student
- 🎨 **Colored terminal UI** — easy to read, navigate, and use
- 💿 **Persistent data** — all grades saved to `grades_data.json`, nothing lost on exit

---

 Preview

```
╔══════════════════════════════════════════════╗
║         STUDENT GRADE TRACKER v1.0          ║
║   Track · Analyze · Improve Your Grades     ║
╚══════════════════════════════════════════════╝

  Students tracked: 3  |  Data file: grades_data.json

  STUDENTS
  1  View All Students
  2  Add New Student
  3  Open Student (view/edit grades)
  4  Remove Student

  REPORTS
  5  Class Summary Report

  0  Exit
```

---

 Grade Scale

| Score     | Letter | GPA Points |
|-----------|--------|------------|
| 97 – 100  | A+     | 4.0        |
| 93 – 96   | A      | 4.0        |
| 90 – 92   | A-     | 3.7        |
| 87 – 89   | B+     | 3.3        |
| 83 – 86   | B      | 3.0        |
| 80 – 82   | B-     | 2.7        |
| 77 – 79   | C+     | 2.3        |
| 73 – 76   | C      | 2.0        |
| 70 – 72   | C-     | 1.7        |
| 67 – 69   | D+     | 1.3        |
| 65 – 66   | D      | 1.0        |
| 0  – 64   | F      | 0.0        |



 Getting Started

Prerequisites

- Python 3.10 or higher
- No external libraries needed — uses Python standard library only

Check your Python version:
```bash
python --version
```

Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/student-grade-tracker.git
```

2. Navigate into the folder:
```bash
cd student-grade-tracker
```

3. Run the app:
```bash
python grade_tracker.py
```

> On Mac/Linux, use `python3` instead of `python`

---

📁 Project Structure

```
student-grade-tracker/
├── grade_tracker.py   # Main application
├── grades_data.json   # Auto-created on first run (stores all data)
└── README.md
```

---

 Built With

- **Python 3** — core language
- **JSON** — lightweight local data storage
- **ANSI escape codes** — colored terminal output
- **OOP + modular functions** — clean, readable code structure

---

 Future Improvements

- [ ] GUI version using Tkinter
- [ ] Export reports to PDF
- [ ] Import grades from CSV/Excel
- [ ] Semester and school year tracking
- [ ] Grade prediction / what-if calculator



 Author
- GitHub: [https://github.com/guelthestunna]
- Portfolio: [https://campuscrumbs.online/Miguel]

📄 License

This project is open source and available under the [MIT License](LICENSE).
