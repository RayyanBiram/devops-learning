# Challenge 1: Basic Arithmetic Calculator

## Mission
Create a script that takes two numbers as input and performs basic arithmetic operations (addition, subtraction, multiplication, division).

Requirements:

- Prompt user for two numbers
- Perform all four operations
- Display the results
- Handle division by zero

Example output:

Enter first number: 10 Enter second number: 5

Results: 10 + 5 = 15 10 - 5 = 5 10 × 5 = 50 10 ÷ 5 = 2

## Script
```bash
#!/bin/bash

arithmetics() {
        addition=$(($number1 + $number2))
        echo "$number1 + $number2 = $addition"

        subtraction=$(($number1 - $number2))
        echo "$number1 - $number2 = $subtraction"

        multiplication=$(($number1 * $number2))
        echo "$number1 × $number2 = $multiplication"

        if [[ $number2 == 0 ]]; then
                echo "Error: Division by zero is not allowed"
                exit 1
        else
                division=$(($number1 / $number2))
                echo "$number1 ÷ $number2 = $division"
        fi
}

echo "Enter first number: "
read number1

echo "Enter second number: "
read number2

arithmetics
```

## Result
<img src="../images/basic arithmetic calculator.png" width="700"/>