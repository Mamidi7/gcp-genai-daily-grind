# Day 5: JSON + File I/O

## Goal
Learn to read files, write files, and work with JSON data.

## Files
```
day5/
├── data/
│   ├── config.json       # app settings (theme, language, etc.)
│   ├── grades.csv        # student names + scores
│   └── todos.json        # todo list with done status
├── exercises.py          # 5 exercises to fill
└── solution.py           # complete working version
```

## Run
```bash
python3 solution.py    # see what correct code does
python3 exercises.py   # test your work
```

## 5 Concepts
| # | Function | Concept |
|---|----------|---------|
| 1 | `read_file` | `with open("r")` + `f.read()` |
| 2 | `save_settings` | `json.dump(dict, f, indent=2)` |
| 3 | `load_settings` | `json.load(f)` |
| 4 | `file_exists` | `os.path.exists()` |
| 5 | `list_json_files` | `os.listdir()` + filter |
