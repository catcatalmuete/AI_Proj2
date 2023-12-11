# CS4613 Artificial Intelligence
# Professor: Edward K. Wong
# Fall 2023
# Project 2: Cryptarithmetic Problem
# Authors: Cat Almuete, Rakeeb Hossain

# Parse the input file and return a set of variables and a dictionary of domains
def parse_input():
    with open("Input1.txt", "r") as file:
        puzzle = file.read().splitlines()

    variables = set()
    domains = {}
    constraints = []

    for line in puzzle:
        for letter in line:
            variables.add(letter)
            # Handles special case of first letter in a line (cannot be 0)
            if letter not in domains and letter != line[0]:
                domains[letter] = set(range(10))
            elif letter == line[0]:
                domains[letter] = set(range(1, 10))

    # If the sum of the lengths of the addend words is greater than the length of the result word,
    # the first letter of the result word must be 1
    if sum(len(word) for word in puzzle[:-1]) > len(puzzle[-1]):
        domains[puzzle[-1][0]] = {1}

    reversed_puzzle = [word[::-1] for word in puzzle]

    # Add carry variables and constraints to the CSP
    max_len = len(max(reversed_puzzle[0:2], key=len))
    for i in range(max_len):
        carry_var = f'C{i+1}'
        variables.add(carry_var)
        domains[carry_var] = set(range(2))

        # Add constraints for each column
        if i < len(reversed_puzzle[0]) and i < len(reversed_puzzle[1]) and i < len(reversed_puzzle[2]):
            constraints.append(
                (reversed_puzzle[0][i], reversed_puzzle[1][i], reversed_puzzle[2][i], carry_var))

    assignment = {letter: None for letter in variables}

    # If the length of the sum is the same as the length of the longest addend, the carry from the last column must be 0
    if len(puzzle[-1]) == max_len:
        domains[f'C{max_len}'] = {0}
    # If the length of the sum is longer than the length of the longest addend, the carry from the last column must be 1
    elif len(puzzle[-1]) > max_len:
        domains[f'C{max_len}'] = {1}

    return variables, assignment, domains, constraints


# Checks if the assignment is complete by checking if there are any None values
def is_complete(assignment):
    for value in assignment.values():
        if value is None:
            return False
    return True

# Selects the next unassigned variable using the minimum
# remaining values heuristic and the degree heuristic
def select_unassigned_variable(variables, assignment, domains, constraints):
    unassigned_vars = [var for var in variables if assignment[var] is None]

# # Orders the domain values of the variable in the assignment in increasing order
def order_domain_values(var, domains):
    return sorted(list(domains[var])) 

# # Checks if the value assignment is consistent by checking all constraints
def is_consistent(var, value, assignment, constraints):
    # Check that no other variable has been assigned this value
    for variable, assigned_value in assignment.items():
        if variable != var and assigned_value == value:
            return False
        
    # Check that all constraints are satisfied
    for constraint in constraints:
        if var in constraint:
            addend1 = value if var == constraint[0] else assignment.get(constraint[0], None)
            addend2 = value if var == constraint[1] else assignment.get(constraint[1], None)
            sumVal =  value if var == constraint[2] else assignment.get(constraint[2], None)
            carry = value if var == constraint[3] else assignment.get(constraint[3], None)
            if addend1 and addend2 and sumVal and carry:
                if addend1 + addend2 != sumVal + (carry*10):
                    return False
    return True
                

def backtracking_search(variables, domains, assignment, constraints):
    return

def main():
    variables, assignment, domains, constraints = parse_input()
    print(variables)
    print(assignment)
    print(domains)
    print(constraints)

main()
