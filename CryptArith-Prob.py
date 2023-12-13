# CS4613 Artificial Intelligence
# Professor: Edward K. Wong
# Fall 2023
# Project 2: Cryptarithmetic Problem
# Authors: Cat Almuete, Rakeeb Hossain

input_file = "Input2.txt"
output_file = "Output2.txt"

# Parse the input file and return a set of variables and a dictionary of domains
def parse_input():
    with open(input_file, "r") as file:
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
        carry1 = f'C{i}'
        carry2 = f'C{i+1}'
        variables.add(carry2)
        domains[carry2] = set(range(2))

        # Add constraints for each column
        if i < len(reversed_puzzle[0]) and i < len(reversed_puzzle[1]) and i < len(reversed_puzzle[2]):
            constraints.append(
                (carry1 ,reversed_puzzle[0][i], reversed_puzzle[1][i], reversed_puzzle[2][i], carry2))

    assignment = {letter: None for letter in variables}
    assignment['C0'] = 0

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

    # Degree heuristic: Among variables with equal remaining values, select the one involved in the most constraints
    def degree_heuristic(var):
        count = 0
        for constraint in constraints:
            if var in constraint:
                count += 1
        return count

    unassigned_vars = sorted(unassigned_vars, key=degree_heuristic, reverse=True)

    # Minimum Remaining Values heuristic: Select variable with the fewest remaining values in its domain
    unassigned_vars = sorted(unassigned_vars, key=lambda var: len(domains[var]))

    if (len(unassigned_vars)==len(variables)):
        print(unassigned_vars)

    return unassigned_vars[0] if unassigned_vars else None

# Orders the domain values of the variable in the assignment in increasing order
def order_domain_values(var, domains):
    return sorted(list(domains[var])) 

# Checks if the value assignment is consistent by checking all constraints
def is_consistent(var, value, assignment, constraints):
    # Check that no other variable has been assigned this value
    for variable, assigned_value in assignment.items():
        if variable != var and len(variable)!=2 and len(var)!=2 and assigned_value == value:
            return False
        
    # Check that all constraints are satisfied
    for constraint in constraints:
        if var in constraint:
            carry1 = value if var == constraint[0] else assignment.get(constraint[0], None)
            addend1 = value if var == constraint[1] else assignment.get(constraint[1], None)
            addend2 = value if var == constraint[2] else assignment.get(constraint[2], None)
            sumVal =  value if var == constraint[3] else assignment.get(constraint[3], None)
            carry2 = value if var == constraint[4] else assignment.get(constraint[4], None)
            if addend1 is not None and addend2 is not None and sumVal is not None and carry1 is not None and carry2 is not None:
                if carry1 + addend1 + addend2 != (sumVal + (carry2*10)):
                    return False
    return True
                
def backtracking_search(variables, domains, assignment, constraints):
    # Check if the assignment is complete
    if is_complete(assignment):
        return assignment  # Return the complete assignment

    # Select an unassigned variable using heuristics
    var = select_unassigned_variable(variables, assignment, domains, constraints)

    # Order the domain values of the selected variable
    ordered_domain = order_domain_values(var, domains)

    for value in ordered_domain:
        # Check if the value assignment is consistent
        if is_consistent(var, value, assignment, constraints):
            # Assign the value to the variable
            assignment[var] = value

            # Recursive call with the updated assignment
            result = backtracking_search(variables, domains, assignment, constraints)
            if result is not None:
                return result  # Return the result if it's a valid assignment

            # Unassign the variable if no valid assignment found
            assignment[var] = None

    return None  # If no solution found

def main():
    variables, assignment, domains, constraints = parse_input()
    print(variables)
    print(assignment)
    print(domains)
    print(constraints)

    # Attempt to print out to Output1.txt
    solution = backtracking_search(variables, domains, assignment, constraints)

    if solution is not None:
        # Create the output string in the specified format
        output_string = ""
        with open(input_file, "r") as file:
            puzzle = file.read().splitlines()
        for line in puzzle:
            for letter in line:
                output_string += str(assignment[letter])
            output_string += "\n"

        # Write the solution to the output file
        with open(output_file, "w") as file:
            file.write(output_string)
        print("Solution written to Output1.txt")
    else:
        print("No solution found.")


main()
