# notes_management.py

import csv
import os

notes = []
next_id = 1
current_diary = None

def new_diary():
    global notes, next_id, current_diary
    notes = []  # Clear existing notes
    next_id = 1  # Reset next ID
    current_diary = None  # Reset the current diary
    print("New diary started. Previous diary cleared.")


def get_notes():
    return notes

def set_current_diary(filename):
    global current_diary
    current_diary = filename

def get_current_diary():
    return current_diary

def add_note(topic, subtopic, content, keywords):
    global notes, next_id
    notes.append({"id": next_id, "topic": topic, "subtopic": subtopic, "content": content, "keywords": keywords.split(',')})
    next_id += 1

def save_notes_to_csv(filename=None):
    global notes, current_diary
    if filename is None:
        filename = current_diary
    if not filename.endswith('.csv'):
        filename += '.csv'
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["id", "topic", "subtopic", "content", "keywords"])
        writer.writeheader()
        for note in notes:
            note_for_csv = note.copy()
            note_for_csv["keywords"] = ",".join(note_for_csv["keywords"])
            writer.writerow(note_for_csv)
    set_current_diary(filename)

def load_notes_from_csv(filename):
    global notes, next_id
    try:
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            notes = []
            next_id = 1
            for row in reader:
                row["id"] = int(row["id"])
                row["keywords"] = row["keywords"].split(',') if row["keywords"] else []
                notes.append(row)
                next_id = max(next_id, row["id"] + 1)
            set_current_diary(filename)
    except FileNotFoundError:
        print("File not found, starting fresh.")
