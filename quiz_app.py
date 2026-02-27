"""
Author: Muhammad Shehmir

Math Quiz Application
A simple GUI quiz for testing math skills.

"""

import tkinter as tk
from tkinter import messagebox
import csv
import random
import os
from datetime import datetime

class Question:
    """A single quiz question with answer checking."""
    
    def __init__(self, question_text, correct_answer):
        """Creates a new question."""
        self.question_text = question_text
        self.correct_answer = correct_answer
    
    def is_correct(self, answer):
        """Checks if the answer is correct."""
        return answer == self.correct_answer


def validate_name(name):
    """Checks if name is valid (not empty)."""
    return len(name.strip()) > 0


def validate_number(text):
    """Checks if text is a valid number and return it."""
    try:
        number = int(text)
        return (True, number)
    except:
        return (False, None)

def generate_questions(quiz_type):
    """Generates 5 quiz questions based on quiz type."""
    questions = []
    
    if quiz_type == "Square Numbers":
        for _ in range(5):
            num = random.randint(1, 12)
            answer = num * num
            q = Question(f"What is {num}²?", answer)
            questions.append(q)
    
    elif quiz_type == "Multiplication":
        for _ in range(5):
            num1 = random.randint(2, 12)
            num2 = random.randint(2, 12)
            answer = num1 * num2
            q = Question(f"What is {num1} × {num2}?", answer)
            questions.append(q)
    
    else:  # Addition
        for _ in range(5):
            num1 = random.randint(10, 99)
            num2 = random.randint(10, 99)
            answer = num1 + num2
            q = Question(f"What is {num1} + {num2}?", answer)
            questions.append(q)
    
    return questions

def save_score(name, quiz_type, score, total):
    """Saves the quiz score to a CSV file."""
    # Create data folder if needed
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Create file with headers if new
    if not os.path.exists('data/scores.csv'):
        with open('data/scores.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Name', 'Quiz Type', 'Score', 'Total'])
    
    # Add new score
    with open('data/scores.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        date = datetime.now().strftime("%Y-%m-%d %H:%M")
        writer.writerow([date, name, quiz_type, score, total])

def load_scores():
    """Loads all scores from the CSV file."""
    scores = []
    
    if os.path.exists('data/scores.csv'):
        with open('data/scores.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                scores.append(row)
    
    return scores

class QuizApp:
    """Main quiz application with GUI."""
    
    def __init__(self, root):
        """Sets up the quiz application window."""
        self.root = root
        self.root.title("Math Quiz")
        self.root.geometry("500x400")
        
        self.questions = []
        self.current_question = 0
        self.score = 0
        self.name = ""
        self.quiz_type = ""
        
        self.show_start_screen()
    
    def clear_screen(self):
        """Removes all widgets from the window."""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_start_screen(self):
        """Displays the start screen with name input and quiz selection."""
        self.clear_screen()
        
        # Title
        tk.Label(self.root, text="Math Quiz", font=("Arial", 20, "bold")).pack(pady=20)
        
        # Name input
        tk.Label(self.root, text="Enter your name:").pack(pady=5)
        self.name_entry = tk.Entry(self.root, font=("Arial", 12))
        self.name_entry.pack(pady=5)
        
        # Quiz type selection
        tk.Label(self.root, text="Choose quiz type:").pack(pady=10)
        self.quiz_var = tk.StringVar(value="Square Numbers")
        
        tk.Radiobutton(self.root, text="Square Numbers", variable=self.quiz_var, 
                       value="Square Numbers").pack()
        tk.Radiobutton(self.root, text="Multiplication", variable=self.quiz_var, 
                       value="Multiplication").pack()
        tk.Radiobutton(self.root, text="Addition", variable=self.quiz_var, 
                       value="Addition").pack()
        
        # Buttons
        tk.Button(self.root, text="Start Quiz", command=self.start_quiz,
                  bg="#4CAF50", fg="white", padx=20, pady=5).pack(pady=20)
        
        tk.Button(self.root, text="View Scores", command=self.show_scores,
                  bg="#2196F3", fg="white", padx=20, pady=5).pack()
    
    def start_quiz(self):
        """Starts the quiz after validating the name."""
        name = self.name_entry.get()
        
        if not validate_name(name):
            messagebox.showerror("Error", "Please enter your name!")
            return
        
        self.name = name
        self.quiz_type = self.quiz_var.get()
        self.score = 0
        self.current_question = 0
        self.questions = generate_questions(self.quiz_type)
        
        self.show_question()
    
    def show_question(self):
        """Displays the current question."""
        self.clear_screen()
        
        # Check if quiz is finished
        if self.current_question >= len(self.questions):
            self.show_results()
            return
        
        question = self.questions[self.current_question]
        
        # Progress
        tk.Label(self.root, 
                 text=f"Question {self.current_question + 1} of {len(self.questions)}",
                 font=("Arial", 10)).pack(pady=10)
        
        # Question
        tk.Label(self.root, text=question.question_text, 
                 font=("Arial", 16)).pack(pady=30)
        
        # Answer input
        tk.Label(self.root, text="Your answer:").pack(pady=5)
        self.answer_entry = tk.Entry(self.root, font=("Arial", 14))
        self.answer_entry.pack(pady=5)
        self.answer_entry.focus()
        
        # Submit button
        tk.Button(self.root, text="Submit", command=self.check_answer,
                  bg="#4CAF50", fg="white", padx=30, pady=5).pack(pady=20)
    
    def check_answer(self):
        """Checks the user's answer and move to next question."""
        answer_text = self.answer_entry.get()
        
        is_valid, answer = validate_number(answer_text)
        
        if not is_valid:
            messagebox.showerror("Error", "Please enter a number!")
            return
        
        question = self.questions[self.current_question]
        
        if question.is_correct(answer):
            self.score += 1
        
        self.current_question += 1
        self.show_question()
    
    def show_results(self):
        """Displays the final quiz results."""
        self.clear_screen()
        
        # Save score
        save_score(self.name, self.quiz_type, self.score, len(self.questions))
        
        # Results
        tk.Label(self.root, text="Quiz Complete!", 
                 font=("Arial", 20, "bold")).pack(pady=20)
        
        percentage = (self.score / len(self.questions)) * 100
        
        tk.Label(self.root, 
                 text=f"Score: {self.score}/{len(self.questions)} ({percentage:.0f}%)",
                 font=("Arial", 16)).pack(pady=10)
        
        # Feedback
        if percentage >= 80:
            message = "Excellent! 🌟"
        elif percentage >= 60:
            message = "Good job! 👍"
        else:
            message = "Keep practicing!"
        
        tk.Label(self.root, text=message, font=("Arial", 14)).pack(pady=10)
        
        # Buttons
        tk.Button(self.root, text="Try Again", command=self.show_start_screen,
                  bg="#4CAF50", fg="white", padx=20, pady=5).pack(pady=10)
        
        tk.Button(self.root, text="View Scores", command=self.show_scores,
                  bg="#2196F3", fg="white", padx=20, pady=5).pack()
    
    def show_scores(self):
        """Displays all saved quiz scores."""
        self.clear_screen()
        
        tk.Label(self.root, text="Past Scores", 
                 font=("Arial", 18, "bold")).pack(pady=10)
        
        scores = load_scores()
        
        if not scores:
            tk.Label(self.root, text="No scores yet!").pack(pady=20)
        else:
            # Display last 10 scores
            for date, name, quiz_type, score, total in scores[-10:]:
                text = f"{date} | {name} | {quiz_type}: {score}/{total}"
                tk.Label(self.root, text=text, font=("Arial", 10)).pack()
        
        tk.Button(self.root, text="Back", command=self.show_start_screen,
                  bg="#2196F3", fg="white", padx=20, pady=5).pack(pady=20)

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()