PRE_TRAIN_MATH_TEXT = """
You are given text that contains mathematical content, potentially mixed with non-mathematical information such as exam names, dates, marks, problem titles, or other metadata. This content may also include knowledge from other fields like finance, physics, computer science, and others intertwined with mathematics. Your task is to:

1. Extract only the mathematics-related content, including problem statements, mathematical functions, equations, conditions, and multiple-choice options (e.g., A, B, C, D) or numerical answers and sequences, while removing any non-mathematical information such as problem titles, time limits, memory limits, or footer/header. If the text includes knowledge from fields like finance, physics, computer science, etc., that is intertwined with mathematics, ensure that such information is not omitted and is preserved in the extracted content without loss.
2. Present the extracted content in a clean, LaTeX-formatted structure, preserving the mathematical expressions, numerical results, and answer sequences exactly as they appear in the original text.
3. If the provided text contains little to no mathematical content, generate new mathematics-related text based on the content of the input. The generated text should be educational, designed to help students study mathematics or assess their understanding, and include clear problem statements, equations, or concepts relevant to learning mathematics.
4. Output the extracted or generated mathematics-related content immediately following the marker `<|MATH_TEXT|>`, ensuring the output is formatted in LaTeX for clarity and precision.

### Example input 1:
```
1\nJEE Main 2022 (Online) 26th July Morning Shift\n+4\n-1\n\nLet f : R $$\to$$ R be a continuous function such that $$f(3x) - f(x) = x$$. If $$f(8) = 7$$, then $$f(14)$$ is equal to :\n\nA\n4\nB\n10\nC\n11\nD\n16\n...
```

### Example output 1:
```
<|MATH_TEXT|>
1. Let \( f : \mathbb{R} \to \mathbb{R} \) be a continuous function such that \( f(3x) - f(x) = x \). If \( f(8) = 7 \), then \( f(14) \) is equal to:
   A. 4
   B. 10
   C. 11
   D. 16
```

### Example input 2:
```
Algorithm\n\nB. Shooting\ntime limit per test\n1 second\nmemory limit per test\n256 megabytes\ninput\nstandard input\noutput\nstandard output\n\nRecently Vasya decided to improve his pistol shooting skills. Today his coach offered him the following exercise. He placed n cans in a row on a table. Cans are numbered from left to right from 1 to n. Vasya has to knock down each can exactly once to finish the exercise. He is allowed to choose the order in which he will knock the cans down.\n\nVasya knows that the durability of the i-th can is ai. It means that if Vasya has already knocked x cans down and is now about to start shooting the i-th one, he will need (ai⋅x+1) shots to knock it down. You can assume that if Vasya starts shooting the i-th can, he will be shooting it until he knocks it down.\n\nYour task is to choose such an order of shooting so that the number of shots required to knock each of the n given cans down exactly once is minimum possible.\n\nInput\n\nThe first line of the input contains one integer n (2≤n≤1000) — the number of cans.\n\nThe second line of the input contains the sequence a1,a2,…,an (1≤ai≤1000), where ai is the durability of the i-th can.\n\nOutput\n\nIn the first line print the minimum number of shots required to knock each of the n given cans down exactly once.\n\nIn the second line print the sequence consisting of n distinct integers from 1 to n — the order of indices of cans that minimizes the number of shots required.\n\nExamples\ninput\nCopy\n3\n20 10 20\noutput\nCopy\n43\n1 3 2\ninput\nCopy\n4\n10 10 10 10\noutput\nCopy\n64\n2 1 4 3\n...
```

### Example output 2:
```
<|MATH_TEXT|>
Given \( n \) cans in a row, numbered from 1 to \( n \), each with durability \( a_i \) (where \( 1 \leq a_i \leq 1000 \)), the number of shots required to knock down the \( i \)-th can after \( x \) cans have been knocked down is \( a_i \cdot x + 1 \). Find the order of shooting that minimizes the total number of shots to knock down all \( n \) cans exactly once, where \( 2 \leq n \leq 1000 \).

Examples:
1. For \( n = 3 \), \( a_1 = 20 \), \( a_2 = 10 \), \( a_3 = 20 \):
   - Minimum number of shots: 43
   - Order: 1, 3, 2

2. For \( n = 4 \), \( a_1 = 10 \), \( a_2 = 10 \), \( a_3 = 10 \), \( a_4 = 10 \):
   - Minimum number of shots: 64
   - Order: 2, 1, 4, 3
```

Apply this process to the provided text. Extract the mathematics-related content if present, or generate educational mathematics-related content if the input lacks sufficient mathematical material. Ensure the output is formatted in LaTeX and placed after `<|MATH_TEXT|>`.
"""

TEXT_BOOK_MATH_TEXT = """
You are an expert assistant that explains technical texts or solves problems based on given inputs. Your task is to take a provided text, which may describe concepts, examples, or problems, and provide a clear, comprehensive explanation without altering the original content. If the input text is a problem (e.g., a math problem or procedural question), preserve all original data and details from it while explaining. Start by giving relevant background information to help understand the text. Then, provide a detailed explanation of the text's content, supplementing it with additional details where helpful for clarity. If the text appears to be a problem or requires step-by-step reasoning (e.g., math, logic, or procedural), provide a step-by-step breakdown.

Key guidelines:
- Do not change or omit any facts from the original text. If it's a problem, retain all original data in your explanation.
- Keep explanations accurate, neutral, and educational.
- Use markdown for formatting, such as bold for key terms, lists, and LaTeX for math equations.
- If the text involves math or technical symbols, preserve them exactly.
- Structure your response: Begin with background, then a detailed explanation of the text's content, and if applicable, add step-by-step commentary.

### Example 1: Input
```
By following these steps, the 4-way switch can be repurposed as a single pole switch, allowing independent control of the hall/office light.
```

### Example 1: Output
```
<|MATH_TEXT|>
## Background:
In electrical wiring, switches control the flow of electricity to lights or appliances. A single-pole switch is the simplest type, controlling one light from one location. A 4-way switch is used in setups with three or more switches controlling the same light, allowing toggling from multiple points. Repurposing involves rewiring to simplify the circuit.

## Detailed Explanation:
The text describes a process where a 4-way switch is converted into a single-pole switch. This modification enables the hall/office light to be controlled independently, likely meaning it can now be operated without interference from other switches in the original multi-way setup. To achieve this, one would typically cap off unused wires and connect the switch in a basic on/off configuration, but the text assumes the steps are already outlined elsewhere.
```

### Example 2: Input
```
The document discusses three types of spread modes in spread spectrum clock generators, defined by the relationship between the output frequency $f_o$, the input frequency $f_c$, and the frequency excursion $f$:

1. **Center Spread**:
   \[
   f_o = f_c \pm f
   \]
   *Example*: A 100 MHz clock with $\pm 1\%$ modulation results in $f_o \in [99\,\text{MHz}, 101\,\text{MHz}]$.

2. **Down Spread**:
   \[
   f_o = f_c - f
   \]
   *Example*: A 100 MHz clock with $1\%$ modulation results in $f_o \in [99\,\text{MHz}, 100\,\text{MHz}]$.

3. **Up Spread**:
   \[
   f_o = f_c + f
   \]
   *Example*: A 100 MHz clock with $+1\%$ modulation results in $f_o \in [100\,\text{MHz}, 101\,\text{MHz}]$."
```

### Example 2: Output
```
<|MATH_TEXT|>
## Background:
Spread spectrum clock generation is a technique used in electronics to reduce electromagnetic interference (EMI) by intentionally varying the clock frequency over a range. This spreads the energy across a wider spectrum, lowering peak emissions. Clock generators produce timing signals for digital circuits, and spread modes determine how the frequency is modulated relative to the nominal (input) frequency.

## Detailed Explanation:
The document outlines three spread modes for spread spectrum clock generators, based on how the output frequency $f_o$ relates to the input frequency $f_c$ and the excursion $f$ (which represents the deviation amount). These modes are crucial for tailoring EMI reduction to specific system needs, such as avoiding overclocking or underclocking issues.

1. **Center Spread**: Here, the frequency oscillates symmetrically around the input frequency, as $f_o = f_c \pm f$. For a 100 MHz clock with $\pm1$% modulation, this means the frequency varies from 99 MHz (100 - 1) to 101 MHz (100 + 1), centering on 100 MHz. This mode balances the spread above and below the nominal frequency, providing even distribution of spectral energy.

2. **Down Spread**: The frequency is shifted downward, $f_o = f_c - f$, so it varies below the input frequency. In the example, a 100 MHz clock with 1% modulation ranges from 99 MHz to 100 MHz, never exceeding the nominal frequency. This is useful in systems where exceeding the nominal speed could cause issues, like in timing-sensitive applications.

3. **Up Spread**: Conversely, the frequency is shifted upward, $f_o = f_c + f$, varying above the input. For +1% modulation on 100 MHz, it ranges from 100 MHz to 101 MHz. This might be chosen when higher speeds are tolerable but lower ones are not, perhaps in overclock-tolerant designs.

These modes help in EMI reduction while maintaining system performance, with choices depending on application requirements like timing constraints.
```

### Example 3: Input
```
Solve the quadratic equation: $x^2 - 3x - 4 = 0$ using the quadratic formula.
```

### Example 3: Output
```
<|MATH_TEXT|>
## Background:
Quadratic equations are polynomial equations of the second degree, typically in the form $ax^2 + bx + c = 0$, where $a$, $b$, and $c$ are constants, and $a \neq 0$. They represent parabolas graphically and have applications in physics, engineering, and economics for modeling phenomena like projectile motion or optimization problems. Solutions to quadratic equations can be found using methods such as factoring, completing the square, or the quadratic formula, which is $x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$.

## Detailed Explanation:
The given problem is to solve the quadratic equation $x^2 - 3x - 4 = 0$ using the quadratic formula. This equation is in the standard form with $a = 1$, $b = -3$, and $c = -4$. The quadratic formula provides the roots directly, and we will apply it step by step while preserving all original coefficients.

Step-by-step solution:

1. Identify the coefficients: From the equation $x^2 - 3x - 4 = 0$, $a = 1$, $b = -3$, $c = -4$.

2. Calculate the discriminant: The discriminant $D = b^2 - 4ac = (-3)^2 - 4(1)(-4) = 9 + 16 = 25$.

3. Since $D > 0$ ($25 > 0$), there are two distinct real roots.

4. Apply the quadratic formula:
   $x = \frac{-b \pm \sqrt{D}}{2a} = \frac{-(-3) \pm \sqrt{25}}{2(1)} = \frac{3 \pm 5}{2}$

5. Compute the two roots:
   First root: $x_1 = \frac{3 + 5}{2} = \frac{8}{2} = 4$
   Second root: $x_2 = \frac{3 - 5}{2} = \frac{-2}{2} = -1$

Thus, the solutions are $x = 4$ and $x = -1$.

These can be verified by substituting back into the original equation: For $x=4$, $16 - 12 - 4 = 0$; for $x=-1$, $1 + 3 - 4 = 0$.

Solutions: $x = 4$ and $x = -1$.
```

Ensure the output is formatted in LaTeX and placed after `<|MATH_TEXT|>`.
"""

QUESTION_ANSWER_PROMPT = """
You are an expert in mathematics and related fields, including physics, economics, and applied mathematics. Your task is to convert the provided text into a Question-Answer format suitable for educational purposes, ensuring the output begins with '<|MATH_TEXT|>'.

## Instructions:
1. **Output Structure**:
   - Begin the output with '<|MATH_TEXT|>' on a new line, followed by the Question-Answer pairs.
   - Format questions as **Question 1**, **Question 2**, etc., and answers as **Answer 1**, **Answer 2**, etc.
2. **Question Extraction**:
   - If the text contains explicit problems, rephrase them clearly as questions.
   - If the text lacks explicit problems, generate **two original problems** based on the text's context, ensuring answers involve mathematical equations.
   - If the text lacks sufficient context, supplement it with relevant background information to ensure the problem is well-defined.
3. **Answer Requirements**:
   - Provide concise, accurate answers with equations formatted in LaTeX using $$ for display equations (e.g., $$x^2 + y^2 = r^2$$) and $ for inline equations (e.g., $x^2$).
   - For complex problems (e.g., advanced calculus, physics, or economics), include a step-by-step solution that is clear but not overly verbose.
4. **Code Implementation**:
   - If the text includes code or a programming solution enhances understanding, provide a separate code block labeled **Code Implementation N** after each answer.
   - Use Python (unless otherwise specified) with clear comments explaining each step and linking to the mathematical equations used.
5. **Verification**:
   - For problems in physics, economics, or other applied fields, verify the problem's assumptions and context before deriving the answer to ensure accuracy.

## Example Input and Example Output:
The following are the Example Input and Example Output to illustrate the expected format and content.

### Example Input:
```
1. **Dot Product Function**:  \n   Given two lists of numbers $ \\text{lst}_1 $ and $ \\text{lst}_2 $, compute their dot product:  \n   $$\n   \\text{dot-product}(\\text{lst}_1, \\text{lst}_2) =
\\sum_{i=1}^{n} a_i \\cdot b_i\n   $$  \n   where $ a_i $ and $ b_i $ are elements of $ \\text{lst}_1 $ and $ \\text{lst}_2 $, respectively.  \n   Example:  \n   $$\n   \\text{dot-product}([1, 3, 4], [5, 7,
 8]) = (1 \\cdot 5) + (3 \\cdot 7) + (4 \\cdot 8) = 5 + 21 + 32 = 58\n   $$\n\n2. **Zip Function**:  \n   Given two lists $ \\text{lst}_1 $ and $ \\text{lst}_2 $, pair their elements into a list of pairs:
\n   $$\n   \\text{zip}(\\text{lst}_1, \\text{lst}_2) = [(a_1, b_1), (a_2, b_2), \\dots, (a_n, b_n)]\n   $$  \n   Example:  \n   $$\n   \\text{zip}([1, 2, 3, 4, 5], [6, 7, 8, 9, 10]) = [(1, 6), (2, 7), (3,
8), (4, 9), (5, 10)]\n   $$\n\n3. **Map-Combine Generalization**:  \n   A higher-order function $ \\text{map-combine} $ takes:  \n   - A base value $ \\text{base} $,  \n   - An element-wise function $ \\tex
t{func-elem} $,  \n   - A list-combining function $ \\text{func-lst} $,  \n   - Two lists $ \\text{lst}_1 $ and $ \\text{lst}_2 $,  \n   and recursively applies $ \\text{func-elem} $ to corresponding elemen
ts, combining results with $ \\text{func-lst} $.  \n   Example:  \n   $$\n   \\text{map-combine}(0, *, +, [1, 3, 4], [5, 7, 8]) = (1 \\cdot 5) + (3 \\cdot 7) + (4 \\cdot 8) = 58\n   $$\n\n4. **Binary Search
 Tree (BST) Recursion**:  \n   Define a BST with nodes containing a key (number), value (string), left, and right subtrees.  \n   - **Search**: Recursively traverse the tree based on key comparisons.  \n
- **Node Removal**: Maintain BST properties after deletion.  \n\n5. **Unbounded Tree (UT) Mutual Recursion**:  \n   Define a tree with a value and a list of child trees.  \n   - **Traversal**: Recursively p
rocess the root and all subtrees.  \n\n6. **Foldr Examples**:  \n   - **Sum**: $ \\text{foldr}(+, 0, [5, 2, 7, 4, 1, 3]) = 5 + 2 + 7 + 4 + 1 + 3 = 22 $  \n   - **Count Elements**: $ \\text{foldr}(\\text{add
1}, 0, [5, 2, 7, 4, 1, 3]) = 6 $  \n   - **List Reconstruction**: $ \\text{foldr}(\\text{cons}, \\text{empty}, [5, 2, 7, 4, 1, 3]) = [5, 2, 7, 4, 1, 3] $  \n\n7. **Lambda and Abstraction**:  \n   - **Anonym
ous Functions**: Use $ \\lambda $ for simple operations (e.g., $ \\lambda(x)(x^2) $).  \n   - **Filter Example**: $ \\text{filter}(\\lambda(x)(x > 4), [5, 2, 7, 4, 1, 3]) = [5, 7] $.  \n\n8. **Quicksort wit
h Custom Comparator**:  \n   Sort a list using a custom comparison function $ f $.  \n   Example:  \n   $$\n   \\text{quicksort}([5, 2, 7, 4, 1, 3], <) = [1, 2, 3, 4, 5, 7]\n   $$  \n   $$\n   \\text{quicks
ort}([5, 2, 7, 4, 1, 3], \\lambda(a, b)(\\text{even?}(a))) = [4, 2, 5, 7, 1, 3]\n   $$
```

### Example Output:
<|MATH_TEXT|>
**Question 1**:
What is the dot product of two lists, `[2, 4, 6]` and `[1, 3, 5]`, and how is it computed?

**Answer 1**:
The dot product of two lists, $$\text{lst}_1 = [2, 4, 6]$$ and $$\text(lst}_2 = [1, 3, 5]$$, is computed as:
$$
\text{dot-product}(\text{lst}_1, \text{lst}_2) = \sum_{i=1}^{n} a_i \cdot b_i
$$
For $$\text{lst}_1 = [2, 4, 6]$$ and $$\text(lst}_2 = [1, 3, 5]$$:
$$
\text{dot-product} = (2 \cdot 1) + (4 \cdot 3) + (6 \cdot 5) = 2 + 12 + 30 = 44
$$

So, Answer is: 44

**Code Implementation 1**:
```python
def dot_product(lst1, lst2):
    # Compute dot product by multiplying corresponding elements and summing
    return sum(a * b for a, b in zip(lst1, lst2))

# Example usage
lst1 = [2, 4, 6]
lst2 = [1, 3, 5]
result = dot_product(lst1, lst2)  # Corresponds to (2*1) + (4*3) + (6*5) = 44
print(result)  # Output: 44
```

**Question 2**:
Using the `map-combine` function with a base value of 0, element-wise multiplication, and list-combining addition, compute the result for the lists `[1, 3, 4]` and `[5, 7, 8]`.

**Answer 2**:
The `map-combine` function applies an element-wise function (multiplication, $$*$$) to corresponding elements of two lists and combines the results using a list-combining function (addition, $$+$$) with a base value of 0. For $$\text(lst}_1 = [1, 3, 4]$$ and $$\text{lst}_2 = [5, 7, 8]$$:
$$
\text{map-combine}(0, *, +, [1, 3, 4], [5, 7, 8]) = (1 \cdot 5) + (3 \cdot 7) + (4 \cdot 8) = 5 + 21 + 32 = 58
$$

So, Answer is: 58

**Code Implementation 2**:
```python
def map_combine(base, func_elem, func_lst, lst1, lst2):
    # Pair elements, apply func_elem, and combine with func_lst starting from base
    pairs = zip(lst1, lst2)
    result = base
    for a, b in pairs:
        result = func_lst(result, func_elem(a, b))  # Apply func_elem, then func_lst
    return result

# Example usage
lst1 = [1, 3, 4]
lst2 = [5, 7, 8]
result = map_combine(0, lambda x, y: x * y, lambda x, y: x + y, lst1, lst2)
# Corresponds to (1*5) + (3*7) + (4*8) = 5 + 21 + 32 = 58
print(result)  # Output: 58
```

## Final Instruction:
Always begin the output with '<|MATH_TEXT|>' on a new line, followed by the Question-Answer pairs as shown in the Example Output.
"""

PLANNING_APPROACH_PROMPT = """
You are an expert in mathematical pedagogy. Your task is to convert the provided text into a "Principle -> Problem -> Execution" format, suitable for teaching abstract problem-solving. The output must begin with '<|MATH_TEXT|>'.

## Instructions:
1.  **Output Structure**:
    * Begin the output with '<|MATH_TEXT|>' on a new line.
    * Structure the content into three distinct sections: `### Principle`, `### Problem`, and `### Step-by-Step Execution`.
2.  **Principle Section**:
    * Identify the core mathematical theorem, formula, or concept that is central to the text.
    * Provide a concise and clear definition or explanation of this principle.
3.  **Problem Section**:
    * If the text contains an explicit problem, rephrase it clearly.
    * If not, generate one original problem that can be solved by applying the identified principle.
4.  **Step-by-Step Execution Section**:
    * Provide a detailed, step-by-step solution to the problem.
    * Explicitly reference how each step applies the principle defined in the first section.
    * Format all equations in LaTeX using $$ for display equations and $ for inline equations.

## Example Input and Example Output:

### Example Input:
```
The area of a circle is given by the formula A = πr², where r is the radius. The circumference is C = 2πr. These formulas are fundamental in geometry for solving problems involving circular shapes, such as finding the area of a sector or the length of an arc. For a sector with angle θ in radians, the area is (θ/2π) * πr² = (1/2)r²θ.
```

### Example Output:
<|MATH_TEXT|>
### Principle
The area of a sector of a circle is derived from the total area of the circle. The area of a full circle is $$A = \pi r^2$$. A sector with a central angle of $\theta$ (in radians) represents a fraction, $$\frac{\theta}{2\pi}$$, of the entire circle. Therefore, the area of the sector, $$A_{\text{sector}}$$, is calculated by multiplying the total area by this fraction:
$$
A_{\text{sector}} = \left( \frac{\theta}{2\pi} \right) \times \pi r^2 = \frac{1}{2} r^2 \theta
$$

### Problem
A circle has a radius of 10 cm. Calculate the area of a sector of this circle that has a central angle of $$\frac{\pi}{3}$$ radians.

### Step-by-Step Execution
1.  **Identify the given values**: The radius $r$ is 10 cm, and the central angle $\theta$ is $$\frac{\pi}{3}$$ radians.
2.  **Recall the principle**: We use the formula for the area of a sector, $$A_{\text{sector}} = \frac{1}{2} r^2 \theta$$.
3.  **Substitute the values into the formula**: This step directly applies the principle using the given problem data.
    $$
    A_{\text{sector}} = \frac{1}{2} (10)^2 \left( \frac{\pi}{3} \right)
    $$
4.  **Calculate the final result**:
    $$
    A_{\text{sector}} = \frac{1}{2} \cdot 100 \cdot \frac{\pi}{3} = \frac{100\pi}{6} = \frac{50\pi}{3}
    $$
The area of the sector is $$\frac{50\pi}{3}$$ square centimeters.
"""

SOCRATIC_METHOD_PROMPT = """
You are an insightful math tutor who uses the Socratic method. Your task is to convert the provided text into a dialogue between a "Teacher" and a "Student" to solve a mathematical problem. The output must begin with '<|MATH_TEXT|>'.

## Instructions:
1.  **Output Structure**:
    * Begin the output with '<|MATH_TEXT|>' on a new line.
    * First, state the problem clearly under a `## Problem` heading.
    * Then, write a dialogue with alternating `**Teacher:**` and `**Student:**` roles.
2.  **Dialogue Content**:
    * The Teacher should guide the Student by asking questions, providing hints, and prompting for the next step, rather than giving direct answers.
    * The Student should articulate their thought process, occasionally making a plausible mistake or expressing uncertainty.
    * The Teacher should help the Student identify and correct their own mistakes.
    * The dialogue should naturally progress to the correct final answer.
3.  **Problem Generation**:
    * If the text contains a problem, use it as the basis for the dialogue.
    * If not, create an original problem from the text's context that allows for a rich, guided conversation.
4.  **Formatting**:
    * Use LaTeX for all mathematical notation ($$ for display, $ for inline).

## Example Input and Example Output:

### Example Input:
```
To solve the equation 3(x - 2) + 5 = 14, one must first apply the distributive property to expand the term 3(x - 2). Then, isolate the variable x by combining like terms and performing inverse operations. First, subtract 5 from both sides, then add 6, and finally divide by 3.
```

### Example Output:
<|MATH_TEXT|>
## Problem
Solve the following linear equation for $x$: $$3(x - 2) + 5 = 14$$

**Teacher:**
Alright, let's take a look at this equation. What's your first instinct for how to approach it?

**Student:**
I see parentheses, so I should probably use the distributive property first. That would give me $$3x - 6 + 5 = 14$$.

**Teacher:**
Excellent start. That's a very solid first step. Now what do you see on the left side of the equation?

**Student:**
There are two constant numbers, -6 and 5. I can combine them. $$-6 + 5$$ is $$-1$$. So the equation becomes $$3x - 1 = 14$$.

**Teacher:**
Perfect. The equation looks much simpler now. What's the goal when we're trying to solve for $x$?

**Student:**
To get $x$ by itself on one side. So, I need to get rid of the -1 and the 3. I should probably divide by 3 first?

**Teacher:**
That's a common thought. But remember the order of operations. We usually handle addition and subtraction before multiplication and division when we're isolating a variable. What happens if you divide the entire equation by 3 right now?

**Student:**
Oh, I'd have to divide everything... so it would be $$x - \frac{1}{3} = \frac{14}{3}$$. That looks more complicated.

**Teacher:**
Exactly. It's not wrong, but it's more work. So, what's a better way to get rid of that -1?

**Student:**
I should add 1 to both sides. That gives me $$3x = 14 + 1$$, which is $$3x = 15$$.

**Teacher:**
There you go! Now you're on the final step.

**Student:**
Now I just divide by 3. $$x = \frac{15}{3}$$, so $$x=5$$.

**Teacher:**
Fantastic. You navigated that perfectly. By handling the addition first, you kept the calculations much cleaner.
"""

MULTIPLE_SOLUTION_PROMPT = """
You are an expert mathematical author. Your task is to take a mathematical concept or problem and present it by first showing multiple distinct solutions, and then providing a comparative analysis of those methods. The output must begin with '<|MATH_TEXT|>'.

## Instructions:
1.  **Output Structure**:
    * Begin with '<|MATH_TEXT|>' on a new line.
    * State the problem under a `## Problem` heading.
    * Present each solution under a separate subheading (e.g., `### Solution 1: Algebraic Approach`, `### Solution 2: Substitution Method`).
    * Conclude with a `## Comparative Analysis` section.
2.  **Solution Content**:
    * Provide at least two different, valid methods for solving the problem.
    * If the source text only provides one method, you must generate a second, distinct method.
    * Each solution should be clearly explained step-by-step.
3.  **Comparative Analysis Section**:
    * Analyze the trade-offs between the presented solutions.
    * Discuss aspects like computational efficiency, conceptual elegance, risk of errors, and generalizability.
    * Conclude with advice on when one method might be preferable over another.
4.  **Formatting**:
    * Use LaTeX for all mathematical notation ($$ for display, $ for inline).

## Example Input and Example Output:

### Example Input:
```
A system of linear equations can be solved using various techniques. For the system x + y = 7 and x - y = 1, one can use the elimination method. By adding the two equations, the y-variable is eliminated, yielding 2x = 8, so x = 4. Substituting x = 4 back into the first equation gives 4 + y = 7, so y = 3.
```

### Example Output:
<|MATH_TEXT|>
## Problem
Solve the following system of linear equations:
$$
\begin{cases}
x + y = 7 \\
x - y = 1
\end{cases}
$$

### Solution 1: Elimination Method
This method aims to eliminate one of the variables by adding or subtracting the equations.

1.  **Add the two equations together**: We add the left sides and the right sides.
    $$
    (x + y) + (x - y) = 7 + 1
    $$
2.  **Simplify the resulting equation**: The $y$ terms cancel out.
    $$
    2x = 8
    $$
3.  **Solve for $x$**:
    $$
    x = 4
    $$
4.  **Substitute $x$ back into an original equation**: Using the first equation:
    $$
    4 + y = 7
    $$
5.  **Solve for $y$**:
    $$
    y = 3
    $$
The solution is $$(x, y) = (4, 3)$$.

### Solution 2: Substitution Method
This method involves solving one equation for one variable and substituting that expression into the other equation.

1.  **Solve the first equation for $x$**:
    $$
    x = 7 - y
    $$
2.  **Substitute this expression for $x$ into the second equation**:
    $$
    (7 - y) - y = 1
    $$
3.  **Simplify and solve for $y$**:
    $$
    7 - 2y = 1 \\
    -2y = -6 \\
    y = 3
    $$
4.  **Substitute the value of $y$ back to find $x$**: Using the expression from step 1:
    $$
    x = 7 - 3 = 4
    $$
The solution is $$(x, y) = (4, 3)$$.

## Comparative Analysis
Both the **Elimination Method** and the **Substitution Method** yield the correct result, but they have different strengths.

* **Efficiency**: For this specific problem, the Elimination Method is slightly more direct. The coefficients of $y$ are already opposites (+1 and -1), making elimination via addition a single, clean step. Substitution required more algebraic manipulation.
* **Generalizability**: The Substitution Method is arguably more universally applicable. It works easily even when coefficients aren't simple opposites or multiples. Elimination often requires an extra step of multiplying one or both equations to align coefficients, which can introduce arithmetic errors.
* **Recommendation**: When you can immediately spot that adding or subtracting equations will cancel a variable (as in this case), Elimination is often faster. For more complex systems or when one variable is already isolated, Substitution is a very reliable and systematic approach."""
