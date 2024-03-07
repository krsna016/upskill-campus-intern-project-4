import tkinter as tk
from tkinter import messagebox, simpledialog
import json
from datetime import datetime

class QuizGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Quiz Game")
        self.root.geometry("600x400")

        self.user_name = ""
        self.questions = self.load_data_from_file("questions.json")
        self.history = self.load_data_from_file("quiz_history.json")

        self.current_question_index = 0
        self.score = 0

        self.quiz_finished = False  # Track whether the quiz is finished

        self.create_widgets()
        self.get_user_name()  # Call get_user_name to prompt for the user's name

    def load_data_from_file(self, file_path):
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
            return data
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def show_error(self, message):
        messagebox.showerror("Error", message)

    def get_user_name(self):
        self.user_name = simpledialog.askstring("Input", "What is your name?")
        if not self.user_name:
            self.user_name = "Anonymous"

    def create_widgets(self):
        self.question_label = tk.Label(self.root, text="", font=("Helvetica", 14))
        self.question_label.pack(pady=10)

        self.radio_var = tk.StringVar()

        self.radio_buttons = []
        for i in range(len(self.questions[0]["options"])):
            radio_button = tk.Radiobutton(self.root, text="", variable=self.radio_var, value="")
            radio_button.pack(anchor="w")
            self.radio_buttons.append(radio_button)

        self.next_button = tk.Button(self.root, text="Next", command=self.next_question)
        self.next_button.pack(pady=10)

        self.previous_button = tk.Button(self.root, text="Previous", command=self.previous_question)
        self.previous_button.pack(pady=10)

        self.history_button = tk.Button(self.root, text="View History", command=self.view_history)
        self.history_button.pack(pady=10)

        self.play_again_button = tk.Button(self.root, text="Play Again", command=self.play_again)
        self.play_again_button.pack(pady=10)

        self.update_question()

    def update_question(self):
        if self.current_question_index < len(self.questions):
            current_question = self.questions[self.current_question_index]
            question_text = f"{self.current_question_index + 1}. {current_question['question']}"
            self.question_label.config(text=question_text)

            for i, (radio_button, option) in enumerate(zip(self.radio_buttons, current_question["options"])):
                radio_button.config(text=option, value=option)

            # Enable or disable the "Previous" button based on quiz_finished
            self.previous_button.config(state=tk.NORMAL if not self.quiz_finished else tk.DISABLED)

            # Disable all buttons if the quiz is finished
            if self.quiz_finished:
                self.disable_all_buttons()
            else:
                self.enable_all_buttons()

        else:
            self.show_final_score()

    def disable_all_buttons(self):
        self.next_button.config(state=tk.DISABLED)
        self.previous_button.config(state=tk.DISABLED)
        for radio_button in self.radio_buttons:
            radio_button.config(state=tk.DISABLED)

    def enable_all_buttons(self):
        self.next_button.config(state=tk.NORMAL)
        self.previous_button.config(state=tk.NORMAL)
        for radio_button in self.radio_buttons:
            radio_button.config(state=tk.NORMAL)

    def update_answer(self):
        current_question = self.questions[self.current_question_index]
        user_answer = self.radio_var.get()

        if user_answer == current_question["correct_answer"]:
            self.score += 1
        elif user_answer == "":
            pass
        else:
            self.score = max(0, self.score - 1)

    def next_question(self):
        selected_option = self.radio_var.get()
        self.update_answer()

        self.current_question_index += 1
        self.reset_options()
        self.update_question()

    def previous_question(self):
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.reset_options()
            self.update_question()

    def show_final_score(self):
        self.disable_all_buttons()  # Disable all buttons before showing the final score
        messagebox.showinfo("Quiz Completed", f"{self.user_name}, your final score: {self.score}/{len(self.questions)}")
        self.history.append(
            {"name": self.user_name, "score": self.score, "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        self.save_data_to_file("quiz_history.json", self.history)

    def view_history(self):
        if not self.history:
            messagebox.showinfo("Quiz History", "No quiz history available.")
        else:
            history_text = "\n".join([f"Name: {entry['name']}, Date: {entry['date']}, Score: {entry['score']}" for entry in self.history])
            messagebox.showinfo("Quiz History", history_text)

    def save_data_to_file(self, file_path, data):
        try:
            with open(file_path, "w") as f:
                json.dump(data, f)
        except Exception as e:
            self.show_error(f"Error saving data to {file_path}: {e}")

    def play_again(self):
        self.current_question_index = 0
        self.score = 0
        self.quiz_finished = False  # Reset the quiz_finished variable
        self.get_user_name()
        self.reset_options()
        self.update_question()

    def reset_options(self):
        self.radio_var.set("")
        for radio_button in self.radio_buttons:
            radio_button.deselect()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizGame(root)
    root.mainloop()
