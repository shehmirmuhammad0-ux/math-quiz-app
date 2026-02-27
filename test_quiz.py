"""
Unit tests for Math Quiz Application
Tests the validation functions and Question class.
"""

import unittest
from quiz_app import Question, validate_name, validate_number, generate_questions

class TestValidation(unittest.TestCase):
    """Tests the validation functions."""
    
    def test_validate_name_with_valid_name(self):
        """Tests that valid names return True."""
        self.assertTrue(validate_name("John"))
        self.assertTrue(validate_name("Alice Smith"))
        self.assertTrue(validate_name("  Bob  "))  # With spaces
    
    def test_validate_name_with_empty_string(self):
        """Tests that empty names return False."""
        self.assertFalse(validate_name(""))
        self.assertFalse(validate_name("   "))  # Only spaces
    
    def test_validate_number_with_valid_input(self):
        """Tests that valid numbers are parsed correctly."""
        is_valid, number = validate_number("42")
        self.assertTrue(is_valid)
        self.assertEqual(number, 42)
        
        is_valid, number = validate_number("-5")
        self.assertTrue(is_valid)
        self.assertEqual(number, -5)
    
    def test_validate_number_with_invalid_input(self):
        """Tests that invalid inputs return False."""
        is_valid, number = validate_number("abc")
        self.assertFalse(is_valid)
        self.assertIsNone(number)
        
        is_valid, number = validate_number("")
        self.assertFalse(is_valid)
        self.assertIsNone(number)


class TestQuestion(unittest.TestCase):
    """Tests the Question class."""
    
    def test_question_creation(self):
        """Tests creating a Question object."""
        q = Question("What is 2+2?", 4)
        self.assertEqual(q.question_text, "What is 2+2?")
        self.assertEqual(q.correct_answer, 4)
    
    def test_is_correct_with_right_answer(self):
        """Tests that correct answers return True."""
        q = Question("What is 5x5?", 25)
        self.assertTrue(q.is_correct(25))
    
    def test_is_correct_with_wrong_answer(self):
        """Tests that wrong answers return False."""
        q = Question("What is 5x5?", 25)
        self.assertFalse(q.is_correct(24))
        self.assertFalse(q.is_correct(26))


class TestQuestionGeneration(unittest.TestCase):
    """Tests the question generation functions."""
    
    def test_generate_square_numbers(self):
        """Tests that square number questions are generated correctly."""
        questions = generate_questions("Square Numbers")
        self.assertEqual(len(questions), 5)
        self.assertIsInstance(questions[0], Question)
    
    def test_generate_multiplication(self):
        """Tests that multiplication questions are generated correctly."""
        questions = generate_questions("Multiplication")
        self.assertEqual(len(questions), 5)
        self.assertIsInstance(questions[0], Question)
    
    def test_generate_addition(self):
        """Tests that addition questions are generated correctly."""
        questions = generate_questions("Addition")
        self.assertEqual(len(questions), 5)
        self.assertIsInstance(questions[0], Question)

if __name__ == '__main__':
    unittest.main()