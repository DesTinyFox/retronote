import csv
import os

notes = []  # This will store our notes, each note is a dictionary
next_id = 1  # This will help us assign a unique ID to each note
current_diary = None  # Keeps track of the currently loaded diary file

def save_notes_to_csv():
    global notes, next_id, current_diary
    if current_diary:
        print(f"Current diary: {current_diary}")
        filename = input("Enter filename to save to (leave blank to use current diary): ").strip()
        if not filename:
            filename = current_diary
    else:
        filename = input("Enter a new diary filename to save: ").strip()

    if not filename.endswith('.csv'):
        filename += '.csv'

    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["id", "topic", "subtopic", "content"])
        writer.writeheader()
        for note in notes:
            writer.writerow(note)
    
    print(f"Notes saved to diary: {filename}")

    # Ask if the user wants to start a new diary or continue with the current
    if input("Start a new diary? (y/n): ").lower().startswith('y'):
        notes = []  # Clear existing notes
        next_id = 1  # Reset next ID
        current_diary = None  # Reset current diary
        print("Ready for a new diary.")
    else:
        # If not starting a new diary, optionally reload the current diary
        if input("Reload the current diary? (y/n): ").lower().startswith('y'):
            load_notes_from_csv(filename)  # Ensure this function can accept a filename

def list_csv_files():
    print("Available diaries:")
    csv_files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.csv')]
    for i, file in enumerate(csv_files, start=1):
        print(f"{i}. {file}")
    return csv_files

def load_notes_from_csv(filename=None):
    global notes, next_id, current_diary
    if not filename:
        csv_files = list_csv_files()
        if not csv_files:
            print("No diary files found. Starting fresh.")
            return
        
        file_index = input("Enter the number of the diary to load: ").strip()
        try:
            file_index = int(file_index) - 1
            if file_index >= 0 and file_index < len(csv_files):
                filename = csv_files[file_index]
            else:
                print("Invalid selection.")
                return
        except ValueError:
            print("Please enter a valid number.")
            return

    try:
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            notes = []  # Clear existing notes
            next_id = 1  # Reset next ID
            for row in reader:
                notes.append({"id": int(row["id"]), "topic": row["topic"], "subtopic": row["subtopic"], "content": row["content"]})
                next_id = max(next_id, int(row["id"]) + 1)
            current_diary = filename
            print(f"Diary loaded: {filename}")
    except FileNotFoundError:
        print("Diary file not found. Starting fresh.")

def add_note():
    global next_id
    topic = input("Topic: ")
    subtopic = input("Subtopic: ")
    content = input("Content: ")
    keywords_input = input("Keywords (comma-separated): ")
    keywords = [keyword.strip() for keyword in keywords_input.split(',')] if keywords_input else []
    notes.append({"id": next_id, "topic": topic, "subtopic": subtopic, "content": content, "keywords": keywords})
    print(f"Note added with ID {next_id}.")
    next_id += 1
    
def view_notes():
    if not notes:
        print("No notes to display.")
        return
    
    print("Your notes:")
    for note in notes:
        keywords_str = ', '.join(note["keywords"])
        print(f'ID: {note["id"]}, Topic: {note["topic"]}, Subtopic: {note["subtopic"]}, Content: {note["content"]}, Keywords: {keywords_str}')

def get_note_by_id(note_id):
    for note in notes:
        if note["id"] == note_id:
            return note
    return None
def delete_note():
    note_id = int(input("Enter note ID to delete: "))
    note = get_note_by_id(note_id)
    
    if note is None:
        print("Note not found.")
        return
    
    notes.remove(note)
    print("Note deleted.")

def search_notes():
    query = input("Enter search query: ").lower()
    matching_notes = [note for note in notes if query in note["topic"].lower() or 
                      query in note["subtopic"].lower() or query in note["content"].lower() or 
                      any(query in keyword.lower() for keyword in note["keywords"])]
    
    if not matching_notes:
        print("No matching notes found.")
        return
    
    print("Matching notes:")
    for note in matching_notes:
        keywords_str = ', '.join(note["keywords"])
        print(f'ID: {note["id"]}, Topic: {note["topic"]}, Subtopic: {note["subtopic"]}, Content: {note["content"]}, Keywords: {keywords_str}')



def edit_note():
    note_id = int(input("Enter note ID to edit: "))
    note = get_note_by_id(note_id)
    
    if note is None:
        print("Note not found.")
        return
    
    note["topic"] = input("New Topic (leave blank to keep current): ") or note["topic"]
    note["subtopic"] = input("New Subtopic (leave blank to keep current): ") or note["subtopic"]
    note["content"] = input("New Content (leave blank to keep current): ") or note["content"]
    print("Note updated.")

def main():
    global current_diary
    while True:
        print("\n[1] Add Note [2] View Notes [3] Edit Note [4] Delete Note [5] Search Notes [6] Load Diary [7] Save Diary [Q] Quit")
        choice = input("Choose an action: ").strip().upper()
        
        if choice == "1":
            add_note()
        elif choice == "2":
            view_notes()
        elif choice == "3":
            edit_note()
        elif choice == "4":
            delete_note()
        elif choice == "5":
            search_notes()
        elif choice == "6":
            load_notes_from_csv()
        elif choice == "7":
            save_notes_to_csv()
        elif choice == "Q":
            print("Exiting Notes App. Remember to save your diary!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()