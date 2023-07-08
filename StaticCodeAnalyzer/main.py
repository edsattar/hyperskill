import os
import sys
import re
import ast


class PythonCodeAnalyzer:
    def __init__(self):
        self.inside_string = False
        self.string_start = -1
        self.inside_multiline_string = False
        self.multiline_string_start_pos: tuple[int, int] | None = None
        self.string_delimiter = None
        self.blank_lines_count = 0
        self.quotes = {'"', "'"}


    def split_code_and_comment(self, line: str, line_no: int) -> tuple[str, str]:
        """Split a line into code and comment parts."""
        # Initialize variables to store the starting index of the comment,
        # the code and comment parts of the line, and the current index (i)
        comment_start = -1
        code = ""
        comment = ""

        # Iterate through each character in the line
        i = 0
        while i < len(line):
            char = line[i]

            # Check if the current character is a single or double quote
            if char in self.quotes and line[i - 1] != "\\":
                # check if next 2 characters are also the same quote
                if i + 2 < len(line) and line[i : i + 3] == char * 3:
                    # If the current character is the end of a multiline string,
                    # set the inside_multiline_string flag to False
                    if (
                        self.inside_multiline_string
                        and self.multiline_string_start_pos != (line_no, i)
                        and self.string_delimiter == char
                    ):
                        self.inside_multiline_string = False
                        self.multiline_string_start_pos = None
                        self.string_delimiter = None

                    # If the current character is the start of a multiline string,
                    # set the inside_multiline_string flag to True
                    elif not self.inside_multiline_string:
                        self.inside_multiline_string = True
                        self.multiline_string_start_pos = (line_no, i)
                        self.string_delimiter = char

                    i += 2

                # If the current character is the start of a string,
                elif not self.inside_string and not self.inside_multiline_string:
                    self.inside_string = True
                    self.string_start = i
                    self.string_delimiter = char
                # If the current character is the end of a string,
                elif (
                    self.inside_string
                    and self.string_start != i
                    and not self.inside_multiline_string
                    and self.string_delimiter == char
                ):
                    self.inside_string = False
                    self.string_start = -1
                    self.string_delimiter = None

            # If the current character is a '#' and not inside a string or multiline string,
            # set the comment_start index to the current index and break the loop
            elif (
                char == "#"
                and not self.inside_string
                and not self.inside_multiline_string
            ):
                comment_start = i
                break

            i += 1

        # If a comment_start index was found, split the line into code and comment parts
        if comment_start != -1:
            code = line[:comment_start]
            comment = line[comment_start:]
        # If no comment_start index was found, the entire line is considered code
        else:
            code = line

        # Return the code and comment parts as a tuple
        return code, comment

    def print_code_and_comment(self, line, line_no, end="\n"):
        """Print the code and comment parts of a line."""
        code, comment = self.split_code_and_comment(line, line_no)
        code = code.rstrip("\n")
        comment = comment.rstrip("\n")
        print(f"[{code}][{comment}]--{line_no}", end=end)

    def check_line_length(self, line: str) -> str | None:
        """S001 Check if the line length is greater than 80 characters."""
        if len(line) >= 80:
            return "S001 Line length is greater than 79 characters"
        return None

    def check_indentation(self, code: str) -> str | None:
        """S002 Check if the indentation is NOT a multiple of four."""
        spaces = 0
        for char in code:
            if char == " ":
                spaces += 1
            else:
                break

        if 0 < spaces < 4 or spaces % 4 != 0:
            return "S002 Indentation is a multiple of four"
        return None

    def check_unnecessary_semicolon(self, code: str) -> str | None:
        """S003 Check if there is an unnecessary semicolon after a statement."""
        if code.rstrip().endswith(";"):
            return "S003 Unnecessary semicolon after a statement"
        return None

    def check_inline_comment_spacing(self, code: str, comment: str) -> str | None:
        """S004 Check if there are less than two spaces before inline comments."""

        # # If there is no code, there is no need to check for inline comments
        if not code.lstrip() or not comment:
            return None
        # Check if there are less than two spaces before inline comments
        elif len(code) - len(code.rstrip(" ")) < 2:
            return "S004 Less than two spaces before inline comment"
        return None

    def check_todo_found(self, comment: str) -> str | None:
        """Check if 'TODO' is found in comments (case-insensitive)."""
        if "TODO" in comment.upper():
            return "S005 TODO found"
        return None

    def check_blank_lines(self, line: str) -> str | None:
        """Check if there are more than two blank lines preceding a code line."""
        if not line.strip():
            self.blank_lines_count += 1
        elif line.strip():
            if self.blank_lines_count > 2:
                self.blank_lines_count = 0
                return "S006 More than two blank lines preceding a code line"
            self.blank_lines_count = 0
        return None

    def check_construction_spaces(self, code: str) -> str | None:
        """S007 Check if too many spaces after construction_name (def or class);"""
        if code.startswith("def") or code.startswith("class"):
            code = code.lstrip("def").lstrip("class")
            spaces = 0
            for char in code:
                if char == " ":
                    spaces += 1
                else:
                    break
            if spaces > 1:
                return "S007 More than one space after construction_name"
        return None

    def check_class_name(self, code: str) -> str | None:
        """S008 Check if class names are not in CamelCase."""
        if code.startswith("class"):
            class_name = code.split()[-1].rstrip(":")
            if not re.match(r"^[A-Z][a-z]+([A-Z][a-z]+)*(\([^()\s]*\))*$", class_name):
                return f"S008 Class name '{class_name}' should use CamelCase"
        return None

    def check_function_name(self, code: str) -> str | None:
        """S009 Check if function names are not in snake_case."""
        if code.startswith("def"):
            code = code.lstrip("def")
            function_name = code.strip().split("(")[0]
            if not re.match(r"^_*[a-z0-9]+(_[a-z0-9]+?)*_*$", function_name):
                return f"S009 Function name '{function_name}' should use snake_case"
        return None

    def check_arg_name(self, node: ast.FunctionDef) -> str | None:
        """S010 Check if argument names are not in snake_case."""
        for arg in node.args.args:
            if not re.match(r"^_*[a-z0-9]+(_[a-z0-9]+?)*_*$", arg.arg):
                return f"Line {node.lineno:02}: S010 Argument name '{arg.arg}' should use snake_case"
        return None

    def check_variable_assign(self, node: ast.Assign) -> str | None:
        """S011 Check if variable names are not in snake_case."""
        try:
            var_name = node.targets[0].id
        except AttributeError:
            var_name = node.targets[0].value.id
        finally:
            if not re.match(r"^_*[a-z0-9]+(_[a-z0-9]+?)*_*$", var_name):
                return f"Line {node.lineno:02}: S011 Variable '{var_name}' in function should be snake_case"
        return None

    def check_arg_mutability(self, node: ast.FunctionDef) -> str | None:
        """S012 Check The default argument value is NOT mutable"""
        mutable_types = (ast.List, ast.Dict, ast.Set)
        for arg in node.args.defaults:
            if isinstance(arg, mutable_types):
                return f"Line {node.lineno:02}: S012 Default argument value is mutable"
        return None

    def process_with_ast(self, file_path: str) -> list[str]:
        """Process with help of python ast module"""
        issues = [None, None]
        with open(file_path, "r") as file:
            tree = ast.parse(file.read())
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    issues.append(self.check_arg_name(node))
                    issues.append(self.check_arg_mutability(node))
                    for inner_node in ast.walk(node):
                        if isinstance(inner_node, ast.Assign):
                            issues.append(self.check_variable_assign(inner_node))

        issues = [e for e in issues if e is not None]

        return sorted(issues)

    def process_lines(self, file_path: str) -> list[str]:
        """Process line by line and return a list of issues found."""
        issues = []
        with open(file_path, "r") as file:
            for i, line in enumerate(file.readlines()):
                code, comment = self.split_code_and_comment(line, i + 1)

                code_lstrip = code.lstrip()

                checks = [
                    self.check_line_length(line),
                    self.check_indentation(code),
                    self.check_unnecessary_semicolon(code),
                    self.check_inline_comment_spacing(code, comment),
                    self.check_todo_found(comment),
                    self.check_blank_lines(line),
                    self.check_construction_spaces(code_lstrip),
                    self.check_class_name(code_lstrip),
                    self.check_function_name(code_lstrip),
                ]

                checks = [f"Line {i+1:02}: {e}" for e in checks if e is not None]
                if checks:
                    issues.extend(checks)

        return issues

    def process_file(self, file_path: str) -> None:
        """Process a file and return a list of issues found."""
        file_issues = []
        file_issues.extend(self.process_lines(file_path))
        file_issues.extend(self.process_with_ast(file_path))

        for issue in file_issues:
            print(f"{file_path}: {issue}")


def main():
    analyzer = PythonCodeAnalyzer()
    path = sys.argv[1]
    file_list = []
    if os.path.isfile(path):
        file_list.append(path)
    if os.path.isdir(path):
        file_list = [os.path.join(path, file) for file in sorted(os.listdir(path))]

    for file_path in file_list:
        if file_path.endswith("tests.py") or file_path.endswith("__init__.py"):
            continue
        if file_path.endswith(".py"):
            analyzer.process_file(file_path)


if __name__ == "__main__":
    main()
