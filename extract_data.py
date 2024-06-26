import re
import json

def convert_latex_to_math(expression):
    # Convert exponents
    expression = re.sub(r'\^', '**', expression)
    # Convert fractions
    expression = re.sub(r'\\frac\{(\S+)\}\{(\S+)\}', r'(\1) / (\2)', expression)
    # Convert square roots
    expression = re.sub(r'\\sqrt\{(\S+)\}', r'sqrt(\1)', expression)
    # Convert matrices
    expression = re.sub(r'\\begin\{bmatrix\}(.*)\\end\{bmatrix\}', r'[\1]', expression)
    return expression

def remove_latex_commands(text):
    # Remove LaTeX commands and symbols
    text = re.sub(r'\\[a-zA-Z]+', '', text)
    return text

def extract_questions(file_path):
    questions = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        current_question = {}
        for line in lines:
            line = line.strip()
            # Extracting Question ID
            if "Question ID" in line:
                current_question["questionId"] = int(re.search(r'\d+', line).group())
            # Extracting Question Text and converting LaTeX to math expression
            elif line and not line.startswith("Sol.") and not line.startswith("Answer"):
                # Filter out unwanted lines
                if line.startswith("(") and ")" in line:
                    # Extract options and correct answer
                    option_number = line.split(")")[0].strip().replace("(", "")
                    option_text = line.split(")")[1].strip()
                    option_text = remove_latex_commands(option_text)
                    option_text = convert_latex_to_math(option_text)
                    current_question.setdefault("options", []).append({"optionNumber": option_number, "optionText": option_text})
                    if line.startswith("(A)"):
                        current_question["answer"] = option_number
                else:
                    # Extract question text
                    current_question.setdefault("questionText", "")
                    current_question["questionText"] += " " + line
                    current_question["questionText"] = remove_latex_commands(current_question["questionText"])
            # Extracting Solution Text
            elif line.startswith("Sol."):
                current_question["solutionText"] = line[5:].strip()
                questions.append(current_question)
                current_question = {}
    return questions

# File path of the text file containing questions
file_path = "Task.txt"

# Extract questions from the text file
questions = extract_questions(file_path)

# Convert to JSON
json_data = json.dumps(questions, indent=2)

# Output JSON data to a file
output_file_path = "output.json"
with open(output_file_path, "w") as output_file:
    output_file.write(json_data)

print("JSON data has been written to:", output_file_path)
