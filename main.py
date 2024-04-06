import notes_management as nm

def main_menu():
    print("\nMain Menu:")
    print("[1] Add Note")
    print("[2] View Notes")
    print("[3] Edit Note")
    print("[4] Delete Note")
    print("[5] Search Notes")
    print("[6] Load Diary")
    print("[7] Save Diary")
    print("[8] New Diary")  
    print("[Q] Quit")

def add_note_ui():
    topic = input("Topic: ")
    subtopic = input("Subtopic: ")
    content = input("Content: ")
    keywords = input("Keywords (comma-separated): ")
    nm.add_note(topic, subtopic, content, keywords)
    print("Note added successfully.")

def view_notes_ui():
    notes = nm.get_notes()
    if not notes:
        print("No notes to display.")
        return
    for note in notes:
        keywords_str = ', '.join(note["keywords"])
        print(f'ID: {note["id"]}, Topic: {note["topic"]}, Subtopic: {note["subtopic"]}, Content: {note["content"]}, Keywords: {keywords_str}')

def edit_note_ui():
    note_id = int(input("Enter note ID to edit: "))
    note = nm.get_note_by_id(note_id)
    if note is None:
        print("Note not found.")
        return
    topic = input("New Topic (leave blank to keep current): ") or note["topic"]
    subtopic = input("New Subtopic (leave blank to keep current): ") or note["subtopic"]
    content = input("New Content (leave blank to keep current): ") or note["content"]
    keywords = input("New Keywords (comma-separated, leave blank to keep current): ") or ', '.join(note["keywords"])
    nm.edit_note(note_id, topic, subtopic, content, keywords)
    print("Note updated.")

def delete_note_ui():
    note_id = int(input("Enter note ID to delete: "))
    if nm.delete_note(note_id):
        print("Note deleted.")
    else:
        print("Note not found.")

def search_notes_ui():
    query = input("Enter search query: ")
    matching_notes = nm.search_notes(query)
    if not matching_notes:
        print("No matching notes found.")
        return
    for note in matching_notes:
        keywords_str = ', '.join(note["keywords"])
        print(f'ID: {note["id"]}, Topic: {note["topic"]}, Subtopic: {note["subtopic"]}, Content: {note["content"]}, Keywords: {keywords_str}')

def load_diary_ui():
    print("Available diaries:")
    csv_files = nm.list_csv_files()
    for i, file in enumerate(csv_files, start=1):
        print(f"{i}. {file}")
    file_index = int(input("Enter the number of the diary to load: ")) - 1
    if 0 <= file_index < len(csv_files):
        nm.load_notes_from_csv(csv_files[file_index])
        print(f"Diary '{csv_files[file_index]}' loaded successfully.")
    else:
        print("Invalid selection.")

def save_diary_ui():
    filename = input("Enter diary filename to save (leave blank to use current diary): ")
    nm.save_notes_to_csv(filename)
    print("Diary saved successfully.")

def new_diary_ui():
    confirmation = input("Are you sure you want to start a new diary? This will clear all current notes. (y/n): ")
    if confirmation.lower() == 'y':
        nm.new_diary()
        print("New diary started. All previous notes have been cleared.")
    else:
        print("New diary creation cancelled.")


def main():
    while True:
        main_menu()
        choice = input("Choose an action: ").strip().upper()

        if choice == "1":
            add_note_ui()
        elif choice == "2":
            view_notes_ui()
        elif choice == "3":
            edit_note_ui()
        elif choice == "4":
            delete_note_ui()
        elif choice == "5":
            search_notes_ui()
        elif choice == "6":
            load_diary_ui()
        elif choice == "7":
            save_diary_ui()
        elif choice == "8":
            new_diary_ui()
        elif choice == "Q":
            print("Exiting Notes App.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
