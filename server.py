import os
import json
import ast
import operator
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

# ============================================================
# AI LEARN - OFFLINE AI TUTOR
# API KEY NOT REQUIRED
# ============================================================

PORT = 8001
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_FOLDER = os.path.join(BASE_DIR, "templates")


# ============================================================
# SAFE MATH CALCULATOR
# ============================================================

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.FloorDiv: operator.floordiv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def safe_math(expression):
    try:
        expression = expression.replace("x", "*")
        expression = expression.replace("X", "*")

        tree = ast.parse(expression, mode="eval")

        def calculate(node):
            if isinstance(node, ast.Expression):
                return calculate(node.body)

            if isinstance(node, ast.Constant):
                if isinstance(node.value, (int, float)):
                    return node.value

            if isinstance(node, ast.BinOp):
                left = calculate(node.left)
                right = calculate(node.right)

                operation = OPERATORS.get(type(node.op))

                if operation is None:
                    raise ValueError()

                return operation(left, right)

            if isinstance(node, ast.UnaryOp):
                value = calculate(node.operand)
                operation = OPERATORS.get(type(node.op))

                if operation is None:
                    raise ValueError()

                return operation(value)

            raise ValueError()

        result = calculate(tree)

        if isinstance(result, float) and result.is_integer():
            result = int(result)

        return result

    except Exception:
        return None


# ============================================================
# KNOWLEDGE BASE
# ============================================================

KNOWLEDGE = [

    # --------------------------------------------------------
    # PYTHON
    # --------------------------------------------------------

    {
        "keywords": ["what is python", "python"],
        "answer": """
🐍 Python is a high-level, interpreted programming language.

Python is popular because its syntax is simple and easy to understand.

Python is commonly used for:
• Artificial Intelligence
• Machine Learning
• Data Science
• Web Development
• Automation
• Scripting
• Cyber Security

Example:

name = "Ajay"
print(name)
"""
    },

    {
        "keywords": ["python variable", "variables in python", "variable python"],
        "answer": """
🐍 A variable in Python is a name used to store data.

Example:

name = "Ajay"
age = 20
marks = 85.5

Python automatically detects the data type.
"""
    },

    {
        "keywords": ["python list", "list in python"],
        "answer": """
📋 A Python list is an ordered collection of items.

Example:

numbers = [10, 20, 30, 40]

You can access an item using its index:

print(numbers[0])

Output:
10
"""
    },

    {
        "keywords": ["python tuple", "tuple in python"],
        "answer": """
📦 A tuple is an ordered collection that cannot normally be changed after creation.

Example:

numbers = (10, 20, 30)

Tuples are useful when data should remain fixed.
"""
    },

    {
        "keywords": ["python dictionary", "dictionary in python"],
        "answer": """
📚 A dictionary stores data using key-value pairs.

Example:

student = {
    "name": "Ajay",
    "age": 20
}

print(student["name"])
"""
    },

    {
        "keywords": ["python function", "functions in python"],
        "answer": """
🔧 A function is a reusable block of code.

Example:

def greet():
    print("Hello")

greet()

Functions help reduce repeated code.
"""
    },

    {
        "keywords": ["python loop", "loops in python", "for loop python"],
        "answer": """
🔁 Loops are used to repeat a block of code.

Example:

for i in range(5):
    print(i)

Python mainly provides for and while loops.
"""
    },

    {
        "keywords": ["python if else", "conditional statement python", "if statement python"],
        "answer": """
🔀 Conditional statements are used to make decisions.

Example:

age = 20

if age >= 18:
    print("Adult")
else:
    print("Minor")
"""
    },

    {
        "keywords": ["python class", "class in python", "oops python"],
        "answer": """
🏗️ A class is a blueprint for creating objects.

Example:

class Student:
    def __init__(self, name):
        self.name = name

Classes are an important part of Object-Oriented Programming.
"""
    },


    # --------------------------------------------------------
    # C PROGRAMMING
    # --------------------------------------------------------

    {
        "keywords": ["what is c", "c programming", "c language"],
        "answer": """
💻 C is a general-purpose procedural programming language.

C is widely used for:
• Operating systems
• Embedded systems
• System programming
• Compilers
• Networking

Example:

#include <stdio.h>

int main() {
    printf("Hello World");
    return 0;
}
"""
    },

    {
        "keywords": ["pointer in c", "what is pointer"],
        "answer": """
📍 A pointer in C is a variable that stores the memory address of another variable.

Example:

int x = 10;
int *p = &x;

Pointers are commonly used for memory management and efficient programming.
"""
    },

    {
        "keywords": ["array in c", "c array"],
        "answer": """
📊 An array stores multiple values of the same data type.

Example:

int numbers[5] = {10, 20, 30, 40, 50};

Array indexing starts from 0.
"""
    },


    # --------------------------------------------------------
    # JAVA
    # --------------------------------------------------------

    {
        "keywords": ["what is java", "java programming", "java language"],
        "answer": """
☕ Java is a high-level, object-oriented programming language.

Java follows the idea:

Write Once, Run Anywhere.

Java is used in:
• Web applications
• Android applications
• Enterprise software
• Backend systems
• Desktop applications
"""
    },

    {
        "keywords": ["java class", "class in java"],
        "answer": """
☕ A class in Java is a blueprint for creating objects.

Example:

class Student {
    String name;
}

Objects can be created from the class.
"""
    },

    {
        "keywords": ["java inheritance", "inheritance in java"],
        "answer": """
🧬 Inheritance allows one class to acquire properties and methods from another class.

Example:

class Dog extends Animal {
}

Inheritance supports code reuse and is an important OOP concept.
"""
    },


    # --------------------------------------------------------
    # JAVASCRIPT
    # --------------------------------------------------------

    {
        "keywords": ["what is javascript", "javascript"],
        "answer": """
🟨 JavaScript is a programming language mainly used to make web pages interactive.

It can be used for:
• Web applications
• Browser programming
• Server-side development
• Games
• Mobile applications

Example:

let name = "Ajay";
console.log(name);
"""
    },

    {
        "keywords": ["javascript variable", "variables javascript"],
        "answer": """
🟨 JavaScript variables can be declared using let, const, or var.

Example:

let age = 20;
const name = "Ajay";

const is preferred when the value should not be reassigned.
"""
    },


    # --------------------------------------------------------
    # HTML
    # --------------------------------------------------------

    {
        "keywords": ["what is html", "html"],
        "answer": """
🌐 HTML stands for HyperText Markup Language.

HTML is used to create the structure of web pages.

Example:

<h1>Hello World</h1>
<p>Welcome to my website.</p>
"""
    },

    {
        "keywords": ["html tag", "what is html tag"],
        "answer": """
🏷️ HTML tags define elements on a web page.

Examples:

<h1>Heading</h1>
<p>Paragraph</p>
<button>Click</button>

Most HTML elements have opening and closing tags.
"""
    },

    {
        "keywords": ["html form", "forms in html"],
        "answer": """
📝 HTML forms collect information from users.

Common form elements include:

• input
• textarea
• select
• button
• label

Example:

<form>
    <input type="text">
    <button>Submit</button>
</form>
"""
    },


    # --------------------------------------------------------
    # CSS
    # --------------------------------------------------------

    {
        "keywords": ["what is css", "css"],
        "answer": """
🎨 CSS stands for Cascading Style Sheets.

CSS is used to style HTML pages.

CSS can control:
• Colors
• Fonts
• Spacing
• Layout
• Borders
• Responsive design

Example:

h1 {
    color: blue;
}
"""
    },

    {
        "keywords": ["css flexbox", "flexbox"],
        "answer": """
📐 Flexbox is a CSS layout system used to arrange elements efficiently.

Example:

.container {
    display: flex;
    justify-content: center;
    align-items: center;
}

Flexbox is very useful for responsive layouts.
"""
    },

    {
        "keywords": ["responsive web design", "responsive design"],
        "answer": """
📱 Responsive web design makes websites work well on different screen sizes.

It commonly uses:
• Flexible layouts
• CSS media queries
• Flexible images
• Flexbox
• CSS Grid
"""
    },


    # --------------------------------------------------------
    # ARTIFICIAL INTELLIGENCE
    # --------------------------------------------------------

    {
        "keywords": ["what is artificial intelligence", "what is ai", "artificial intelligence"],
        "answer": """
🤖 Artificial Intelligence (AI) is the field of computer science focused on creating systems that can perform tasks that normally require human intelligence.

AI can involve:
• Learning
• Reasoning
• Problem solving
• Understanding language
• Computer vision
• Decision making

Examples include virtual assistants, recommendation systems and AI chatbots.
"""
    },

    {
        "keywords": ["applications of ai", "ai applications", "uses of ai"],
        "answer": """
🤖 AI is used in many areas:

• Healthcare
• Education
• Banking
• Self-driving technology
• Cyber Security
• Recommendation systems
• Robotics
• Natural Language Processing
• Computer Vision
"""
    },

    {
        "keywords": ["what is machine learning", "machine learning", "ml"],
        "answer": """
🧠 Machine Learning is a branch of AI where computers learn patterns from data and use those patterns to make predictions or decisions.

Main types:

1. Supervised Learning
2. Unsupervised Learning
3. Reinforcement Learning

Example:
An email system can learn to classify messages as spam or not spam.
"""
    },

    {
        "keywords": ["supervised learning", "what is supervised learning"],
        "answer": """
📊 Supervised Learning uses labeled training data.

Example:

Input → Student study hours
Output → Exam score

The model learns the relationship between input and expected output.

Common algorithms include:
• Linear Regression
• Logistic Regression
• Decision Trees
• Support Vector Machines
"""
    },

    {
        "keywords": ["unsupervised learning", "what is unsupervised learning"],
        "answer": """
🔍 Unsupervised Learning works with data that does not have predefined labels.

The algorithm tries to discover hidden patterns or groups.

Example:

Customer data → Group customers with similar behavior.

Clustering is a common unsupervised learning technique.
"""
    },

    {
        "keywords": ["reinforcement learning", "what is reinforcement learning"],
        "answer": """
🎮 Reinforcement Learning is a type of machine learning where an agent learns by interacting with an environment.

The agent receives:
• Rewards for good actions
• Penalties for bad actions

It tries to learn a strategy that maximizes total reward.
"""
    },

    {
        "keywords": ["deep learning", "what is deep learning"],
        "answer": """
🧠 Deep Learning is a subset of Machine Learning that uses neural networks with multiple layers.

It is widely used for:

• Image recognition
• Speech recognition
• Natural language processing
• Autonomous systems
• Generative AI
"""
    },

    {
        "keywords": ["neural network", "what is neural network"],
        "answer": """
🧠 A neural network is a machine learning model inspired by the structure of biological neurons.

It usually contains:

Input Layer → Hidden Layers → Output Layer

Neural networks are widely used in image, speech and language tasks.
"""
    },

    {
        "keywords": ["generative ai", "what is generative ai"],
        "answer": """
✨ Generative AI is a type of AI that can generate new content.

It can create:
• Text
• Images
• Audio
• Video
• Computer code

Examples include AI writing assistants and image generation systems.
"""
    },

    {
        "keywords": ["natural language processing", "nlp", "what is nlp"],
        "answer": """
🗣️ Natural Language Processing (NLP) is a field of AI that helps computers understand and process human language.

Applications include:

• Chatbots
• Translation
• Sentiment analysis
• Speech systems
• Text summarization
"""
    },

    {
        "keywords": ["computer vision", "what is computer vision"],
        "answer": """
👁️ Computer Vision is an AI field that helps computers understand images and videos.

Applications include:

• Face detection
• Object detection
• Medical image analysis
• Self-driving systems
• Image classification
"""
    },


    # --------------------------------------------------------
    # DATABASE
    # --------------------------------------------------------

    {
        "keywords": ["what is database", "database"],
        "answer": """
🗄️ A database is an organized collection of data.

Databases are used to store and manage information efficiently.

Examples:
• Student records
• Bank accounts
• Product information
• Employee data
"""
    },

    {
        "keywords": ["what is dbms", "dbms"],
        "answer": """
🗄️ DBMS stands for Database Management System.

A DBMS is software used to create, store, manage and retrieve data from databases.

Examples:
• MySQL
• PostgreSQL
• Oracle
• Microsoft SQL Server
"""
    },

    {
        "keywords": ["what is sql", "sql"],
        "answer": """
🗃️ SQL stands for Structured Query Language.

SQL is used to communicate with relational databases.

Common SQL commands:

SELECT
INSERT
UPDATE
DELETE
CREATE
ALTER
DROP
"""
    },

    {
        "keywords": ["primary key", "what is primary key"],
        "answer": """
🔑 A primary key uniquely identifies each record in a database table.

Important properties:

• Unique
• Cannot normally be NULL
• Identifies a row

Example:

Student_ID = 101
"""
    },

    {
        "keywords": ["foreign key", "what is foreign key"],
        "answer": """
🔗 A foreign key is a field that creates a relationship between two database tables.

Example:

Students table:
Student_ID

Marks table:
Student_ID

The Student_ID in Marks can reference the Students table.
"""
    },

    {
        "keywords": ["sql select", "select query"],
        "answer": """
🗃️ SELECT is used to retrieve data from a database.

Example:

SELECT * FROM students;

This retrieves all columns from the students table.
"""
    },


    # --------------------------------------------------------
    # DATA STRUCTURES
    # --------------------------------------------------------

    {
        "keywords": ["what is data structure", "data structure"],
        "answer": """
📚 A data structure is a way of organizing and storing data so that it can be used efficiently.

Examples:

• Array
• Linked List
• Stack
• Queue
• Tree
• Graph
• Hash Table
"""
    },

    {
        "keywords": ["what is array", "array"],
        "answer": """
📊 An array stores multiple elements in an organized sequence.

Example:

[10, 20, 30, 40]

Array elements are generally accessed using an index.
"""
    },

    {
        "keywords": ["what is stack", "stack data structure"],
        "answer": """
📚 A Stack follows LIFO:

Last In, First Out.

Example:
A stack of plates.

Main operations:
• Push
• Pop
• Peek
"""
    },

    {
        "keywords": ["what is queue", "queue data structure"],
        "answer": """
🚶 A Queue follows FIFO:

First In, First Out.

Example:
People waiting in a line.

Main operations:
• Enqueue
• Dequeue
"""
    },

    {
        "keywords": ["linked list", "what is linked list"],
        "answer": """
🔗 A linked list is a data structure made of nodes.

Each node usually contains:

• Data
• Link/reference to another node

Types include:
• Singly linked list
• Doubly linked list
• Circular linked list
"""
    },

    {
        "keywords": ["binary tree", "what is binary tree"],
        "answer": """
🌳 A binary tree is a tree data structure where each node can have at most two children.

The children are commonly called:

• Left child
• Right child
"""
    },


    # --------------------------------------------------------
    # ALGORITHMS
    # --------------------------------------------------------

    {
        "keywords": ["what is algorithm", "algorithm"],
        "answer": """
⚙️ An algorithm is a step-by-step procedure used to solve a problem.

Example: Making tea can be described as a sequence of steps.

In programming, algorithms are designed to solve computational problems efficiently.
"""
    },

    {
        "keywords": ["time complexity", "what is time complexity"],
        "answer": """
⏱️ Time complexity describes how the running time of an algorithm grows as input size increases.

Common complexities:

O(1) → Constant
O(log n) → Logarithmic
O(n) → Linear
O(n log n)
O(n²) → Quadratic
"""
    },

    {
        "keywords": ["binary search", "what is binary search"],
        "answer": """
🔎 Binary Search is an efficient searching algorithm for sorted data.

It repeatedly divides the search range into half.

Time complexity:

O(log n)

The data must generally be sorted for standard binary search.
"""
    },

    {
        "keywords": ["sorting algorithm", "sorting algorithms"],
        "answer": """
🔢 Sorting algorithms arrange data in a particular order.

Examples:

• Bubble Sort
• Selection Sort
• Insertion Sort
• Merge Sort
• Quick Sort

Different algorithms have different performance characteristics.
"""
    },


    # --------------------------------------------------------
    # OPERATING SYSTEM
    # --------------------------------------------------------

    {
        "keywords": ["what is operating system", "operating system", "os"],
        "answer": """
💻 An Operating System (OS) is system software that manages computer hardware and software resources.

Examples:

• Windows
• Linux
• macOS
• Android
• iOS

The OS manages processes, memory, files and devices.
"""
    },

    {
        "keywords": ["process in operating system", "what is process"],
        "answer": """
⚙️ A process is a program that is currently being executed.

For example, when you open a browser, the operating system manages its running process.

Processes use resources such as CPU and memory.
"""
    },

    {
        "keywords": ["ram", "what is ram"],
        "answer": """
💾 RAM stands for Random Access Memory.

RAM temporarily stores data and programs that the CPU is actively using.

RAM is volatile memory, meaning its contents are generally lost when power is removed.
"""
    },

    {
        "keywords": ["rom", "what is rom"],
        "answer": """
💾 ROM stands for Read-Only Memory.

It is non-volatile memory used to store data that should remain available even when power is turned off.
"""
    },

    {
        "keywords": ["cpu", "what is cpu"],
        "answer": """
🖥️ CPU stands for Central Processing Unit.

The CPU executes instructions and performs calculations.

Main components include:

• ALU
• Control Unit
• Registers
"""
    },


    # --------------------------------------------------------
    # COMPUTER NETWORKS
    # --------------------------------------------------------

    {
        "keywords": ["what is computer network", "computer network"],
        "answer": """
🌐 A computer network is a group of connected devices that can communicate and share resources.

Examples:

• LAN
• MAN
• WAN

The Internet is the world's largest interconnected computer network.
"""
    },

    {
        "keywords": ["what is internet", "internet"],
        "answer": """
🌍 The Internet is a global network of interconnected computer networks.

It allows devices around the world to communicate and exchange information using standard communication protocols.
"""
    },

    {
        "keywords": ["what is ip address", "ip address"],
        "answer": """
🌐 An IP address identifies a device on a network.

Two common versions are:

IPv4 → Example: 192.168.1.1
IPv6 → Newer address format with a much larger address space.
"""
    },

    {
        "keywords": ["what is http", "http"],
        "answer": """
🌐 HTTP stands for HyperText Transfer Protocol.

It is used for communication between web browsers and web servers.

HTTPS is the secure version of HTTP that uses encryption.
"""
    },

    {
        "keywords": ["what is dns", "dns"],
        "answer": """
🌐 DNS stands for Domain Name System.

DNS translates human-readable domain names into IP addresses.

Example:

google.com → IP address

This makes websites easier for humans to access.
"""
    },


    # --------------------------------------------------------
    # CYBER SECURITY
    # --------------------------------------------------------

    {
        "keywords": ["what is cyber security", "cyber security", "cybersecurity"],
        "answer": """
🔐 Cyber Security is the practice of protecting computers, networks, applications and data from unauthorized access and attacks.

Important areas include:

• Network security
• Application security
• Data security
• Identity protection
• Security awareness
"""
    },

    {
        "keywords": ["what is phishing", "phishing"],
        "answer": """
🎣 Phishing is a cyber attack where an attacker tries to trick people into revealing sensitive information.

Examples include fake:

• Emails
• Websites
• Login pages
• Messages

Always verify links and never share passwords or OTPs.
"""
    },

    {
        "keywords": ["strong password", "password security", "secure password"],
        "answer": """
🔐 A strong password should be:

• Long
• Unique
• Difficult to guess
• Not reused across important accounts

Using a password manager and multi-factor authentication can improve security.
"""
    },


    # --------------------------------------------------------
    # DATA SCIENCE
    # --------------------------------------------------------

    {
        "keywords": ["what is data science", "data science"],
        "answer": """
📊 Data Science combines programming, statistics, mathematics and domain knowledge to extract useful insights from data.

Common steps include:

1. Collect data
2. Clean data
3. Analyze data
4. Visualize data
5. Build models
6. Communicate results
"""
    },

    {
        "keywords": ["what is data analysis", "data analysis"],
        "answer": """
📊 Data Analysis is the process of inspecting and transforming data to find useful information, patterns and insights.

Tools commonly include:

• Python
• Pandas
• SQL
• Excel
• Visualization tools
"""
    },

    {
        "keywords": ["what is pandas", "pandas python"],
        "answer": """
🐼 Pandas is a popular Python library for data manipulation and analysis.

It provides useful structures such as:

• Series
• DataFrame

Example:

import pandas as pd

data = pd.DataFrame({
    "Name": ["Ajay", "Ravi"]
})
"""
    },

    {
        "keywords": ["what is numpy", "numpy python"],
        "answer": """
🔢 NumPy is a Python library commonly used for numerical computing.

It provides efficient arrays and mathematical operations.

NumPy is widely used in data science and machine learning.
"""
    },


    #--------------------------------------------------------
    # PHYSICS
    # --------------------------------------------------------

    {
        "keywords": ["what is gravity", "gravity"],
        "answer": """
🌍 Gravity is a force of attraction between objects that have mass.

On Earth, gravity pulls objects toward the Earth's center.

The approximate acceleration due to gravity near Earth's surface is:

g ≈ 9.8 m/s²
"""
    },

    {
        "keywords": ["newton first law", "first law of motion"],
        "answer": """
⚛️ Newton's First Law states that an object remains at rest or continues moving at constant velocity unless acted upon by an external net force.

It is also called the law of inertia.
"""
    },

    {
        "keywords": ["newton second law", "second law of motion"],
        "answer": """
⚛️ Newton's Second Law relates force, mass and acceleration.

Formula:

F = m × a

Where:

F = Force
m = Mass
a = Acceleration
"""
    },

    {
        "keywords": ["speed formula", "what is speed"],
        "answer": """
🏃 Speed describes how much distance an object travels per unit time.

Formula:

Speed = Distance / Time

Example:

Distance = 100 km
Time = 2 hours

Speed = 50 km/h
"""
    },


    # --------------------------------------------------------
    # CHEMISTRY
    # --------------------------------------------------------

    {
        "keywords": ["what is chemistry", "chemistry"],
        "answer": """
🧪 Chemistry is the branch of science that studies matter, its properties, composition and chemical changes.

It includes areas such as:

• Organic Chemistry
• Inorganic Chemistry
• Physical Chemistry
• Analytical Chemistry
"""
    },

    {
        "keywords": ["what is atom", "atom"],
        "answer": """
⚛️ An atom is the basic unit of an element.

It contains:

• Protons
• Neutrons
• Electrons

Protons and neutrons are located in the nucleus.
"""
    },

    {
        "keywords": ["what is molecule", "molecule"],
        "answer": """
🧪 A molecule is formed when two or more atoms are chemically bonded.

Example:

H₂O is a molecule made of hydrogen and oxygen atoms.
"""
    },

    {
        "keywords": ["what is periodic table", "periodic table"],
        "answer": """
🧪 The periodic table organizes chemical elements according to their atomic number and properties.

Elements are arranged into:

• Periods
• Groups

It helps scientists understand patterns in chemical behavior.
"""
    },


    # --------------------------------------------------------
    # BIOLOGY
    # --------------------------------------------------------

    {
        "keywords": ["what is biology", "biology"],
        "answer": """
🧬 Biology is the scientific study of living organisms.

It includes areas such as:

• Botany
• Zoology
• Genetics
• Microbiology
• Ecology
• Cell Biology
"""
    },

    {
        "keywords": ["what is cell", "cell biology"],
        "answer": """
🧬 A cell is the basic structural and functional unit of life.

Cells can be broadly classified into:

• Prokaryotic cells
• Eukaryotic cells

Plant and animal cells are examples of eukaryotic cells.
"""
    },

    {
        "keywords": ["what is dna", "dna"],
        "answer": """
🧬 DNA stands for Deoxyribonucleic Acid.

DNA stores genetic information in living organisms.

It plays an important role in heredity and biological development.
"""
    },

    {
        "keywords": ["photosynthesis", "what is photosynthesis"],
        "answer": """
🌱 Photosynthesis is the process by which green plants use sunlight to produce food.

Plants generally use:

• Carbon dioxide
• Water
• Sunlight

Oxygen is released as a by-product.
"""
    },


    # --------------------------------------------------------
    # MATHEMATICS
    # --------------------------------------------------------

    {
        "keywords": ["what is algebra", "algebra"],
        "answer": """
📐 Algebra is a branch of mathematics that uses symbols and variables to represent numbers and relationships.

Example:

2x + 5 = 15

Subtract 5:

2x = 10

Therefore:

x = 5
"""
    },

    {
        "keywords": ["what is probability", "probability"],
        "answer": """
🎲 Probability measures how likely an event is to occur.

For equally likely outcomes:

Probability = Favorable Outcomes / Total Outcomes

Probability ranges from 0 to 1.
"""
    },

    {
        "keywords": ["what is percentage", "percentage"],
        "answer": """
📊 Percentage means a value expressed out of 100.

Formula:

Percentage = (Part / Whole) × 100

Example:

25 out of 100 = 25%
"""
    },

    {
        "keywords": ["mean median mode", "mean", "median", "mode"],
        "answer": """
📊 Mean = Average of all values.

Median = Middle value after sorting the data.

Mode = Most frequently occurring value.

Example:

Data: 2, 3, 3, 5, 7

Mean = 4
Median = 3
Mode = 3
"""
    },

    {
        "keywords": ["prime number", "what is prime number"],
        "answer": """
🔢 A prime number is a positive integer greater than 1 that has exactly two positive factors:

1 and itself.

Examples:

2, 3, 5, 7, 11, 13
"""
    },

    {
        "keywords": ["even number", "what is even number"],
        "answer": """
🔢 An even number is an integer that is divisible by 2.

Examples:

2, 4, 6, 8, 10, 12
"""
    },

    {
        "keywords": ["odd number", "what is odd number"],
        "answer": """
🔢 An odd number is an integer that is not divisible by 2.

Examples:

1, 3, 5, 7, 9, 11
"""
    },


    # --------------------------------------------------------
    # GENERAL STUDY
    # --------------------------------------------------------

    {
        "keywords": ["how to study", "study tips", "study effectively"],
        "answer": """
📚 Some effective study habits are:

1. Set clear goals.
2. Study in short focused sessions.
3. Practice questions regularly.
4. Revise previous topics.
5. Take short breaks.
6. Sleep properly.
7. Test yourself instead of only reading.

Consistency is more important than studying for one very long session.
"""
    },

    {
        "keywords": ["what is programming", "programming"],
        "answer": """
💻 Programming is the process of writing instructions that a computer can execute.

Popular programming languages include:

• Python
• C
• C++
• Java
• JavaScript
• Go
• Rust

Programming is used to build software, websites, applications and many other systems.
"""
    },

    {
        "keywords": ["what is software", "software"],
        "answer": """
💻 Software is a collection of programs and instructions that tell a computer what to do.

Examples:

• Operating systems
• Mobile apps
• Web browsers
• Games
• Development tools
"""
    },

    {
        "keywords": ["what is hardware", "hardware"],
        "answer": """
🖥️ Hardware refers to the physical components of a computer.

Examples:

• CPU
• RAM
• Hard disk
• Keyboard
• Mouse
• Monitor
• Motherboard
"""
    },

    {
        "keywords": ["what is compiler", "compiler"],
        "answer": """
⚙️ A compiler translates source code written in a programming language into a lower-level form that can be executed by a computer.

Examples of compiled languages include C and C++.

Java uses compilation to bytecode, which is then executed by the JVM.
"""
    },

    {
        "keywords": ["what is debugging", "debugging"],
        "answer": """
🐞 Debugging is the process of finding and fixing errors in a program.

Common types of errors include:

• Syntax errors
• Runtime errors
• Logical errors

Debugging helps make software correct and reliable.
"""
    },

    {
        "keywords": ["what is api", "api"],
        "answer": """
🔌 API stands for Application Programming Interface.

An API allows different software systems to communicate with each other.

For example, a web application can use an API to request data from a server.
"""
    },

    {
        "keywords": ["what is github", "github"],
        "answer": """
🐙 GitHub is a platform used to host and collaborate on software projects.

It commonly works with Git and provides features such as:

• Code repositories
• Version control
• Collaboration
• Pull requests
• Issue tracking
"""
    },

    {
        "keywords": ["what is git", "git"],
        "answer": """
🌿 Git is a distributed version control system.

It helps developers:

• Track code changes
• Create branches
• Collaborate
• Restore previous versions
• Manage software projects
"""
    },

    {
        "keywords": ["what is flask", "flask python"],
        "answer": """
🐍 Flask is a lightweight Python web framework.

It can be used to create:

• Web applications
• REST APIs
• Backend services

Example:

from flask import Flask

app = Flask(__name__)
"""
    },

    {
        "keywords": ["what is json", "json"],
        "answer": """
📦 JSON stands for JavaScript Object Notation.

It is a lightweight data format commonly used for exchanging data between applications.

Example:

{
    "name": "Ajay",
    "age": 20
}
"""
    },

    {
        "keywords": ["what is cloud computing", "cloud computing"],
        "answer": """
☁️ Cloud Computing means using computing resources over the internet.

Resources can include:

• Servers
• Storage
• Databases
• Networking
• Software

Examples of cloud platforms include AWS, Microsoft Azure and Google Cloud.
"""
    },

    {
        "keywords": ["what is blockchain", "blockchain"],
        "answer": """
⛓️ Blockchain is a distributed digital ledger technology.

Information is stored in blocks that are linked together.

Important concepts include:

• Decentralization
• Cryptography
• Consensus
• Distributed records
"""
    },

    {
        "keywords": ["what is iot", "internet of things", "iot"],
        "answer": """
📡 IoT stands for Internet of Things.

It refers to physical devices connected to networks that can collect and exchange data.

Examples:

• Smart watches
• Smart home devices
• Sensors
• Connected vehicles
"""
    },

]


# ============================================================
# GREETING RESPONSES
# ============================================================
#======================

GREETINGS = {
    "hi": "👋 Hi! I'm your AI Learn offline tutor. Ask me a programming, AI, ML, database, science or mathematics question.",
    "hello": "👋 Hello! How can I help you learn today?",
    "hey": "😊 Hey! Ask me any supported learning question.",
    "hii": "👋 Hii! What would you like to learn?",
    "good morning": "🌅 Good morning! Ready to learn something new?",
    "good afternoon": "☀️ Good afternoon! Ask me your question.",
    "good evening": "🌆 Good evening! Let's learn something interesting.",
}


# ============================================================
# RESPONSE FUNCTION
# ============================================================

def get_answer(question):
    original_question = question.strip()
    q = original_question.lower().strip()

    if not q:
        return "Please enter a question. 🤖"

    # --------------------------------------------------------
    # Greetings
    # --------------------------------------------------------

    if q in GREETINGS:
        return GREETINGS[q]

    # --------------------------------------------------------
    # Thanks
    # --------------------------------------------------------

    if q in ["thanks", "thank you", "thankyou", "thx"]:
        return "😊 You're welcome! Keep learning and keep practicing."

    # --------------------------------------------------------
    # Identity
    # --------------------------------------------------------

    if "who are you" in q or "what are you" in q:
        return """
🤖 I am AI Learn Offline Tutor.

I work locally without an API key and provide answers from my built-in educational knowledge base.

I can help with:
• Programming
• AI & ML
• Web Development
• Databases
• Data Structures
• Algorithms
• Operating Systems
• Networking
• Cyber Security
• Mathematics
• Physics
• Chemistry
• Biology
• Data Science
"""

    # --------------------------------------------------------
    # Math detection
    # --------------------------------------------------------

    math_question = q

    replacements = [
        "what is ",
        "calculate ",
        "solve ",
        "find ",
        "answer ",
        "equals ",
        "please calculate ",
    ]

    for word in replacements:
        math_question = math_question.replace(word, "")

    allowed_chars = "0123456789+-*/().% xX"

    if any(char.isdigit() for char in math_question):
        if all(char in allowed_chars for char in math_question):
            result = safe_math(math_question)

            if result is not None:
                return f"""
🧮 Calculation completed.

Question:
{original_question}

Answer:
{result}
"""

    # --------------------------------------------------------
    # Percentage questions
    # Example: 20 percent of 200
    # --------------------------------------------------------

    import re

    percent_match = re.search(
        r"(\d+(?:\.\d+)?)\s*(?:percent|%)\s*(?:of)\s*(\d+(?:\.\d+)?)",
        q
    )

    if percent_match:
        percentage = float(percent_match.group(1))
        number = float(percent_match.group(2))

        result = (percentage / 100) * number

        if result.is_integer():
            result = int(result)

        return f"""
📊 Percentage Calculation

{percentage}% of {number} = {result}
"""

    # --------------------------------------------------------
    # Knowledge base matching
    # --------------------------------------------------------

    best_answer = None
    best_score = 0

    for item in KNOWLEDGE:

        score = 0

        for keyword in item["keywords"]:

            keyword = keyword.lower()

            if keyword in q:
                score += len(keyword)

        if score > best_score:
            best_score = score
            best_answer = item["answer"]

    if best_answer:
        return best_answer

    # --------------------------------------------------------
    # Keyword based fallback
    # --------------------------------------------------------

    topic_map = {
        "python": "🐍 Try asking: What is Python?",
        "java": "☕ Try asking: What is Java?",
        "javascript": "🟨 Try asking: What is JavaScript?",
        "html": "🌐 Try asking: What is HTML?",
        "css": "🎨 Try asking: What is CSS?",
        "machine learning": "🧠 Try asking: What is Machine Learning?",
        "artificial intelligence": "🤖 Try asking: What is Artificial Intelligence?",
        "database": "🗄️ Try asking: What is a database?",
        "sql": "🗃️ Try asking: What is SQL?",
        "algorithm": "⚙️ Try asking: What is an algorithm?",
        "operating system": "💻 Try asking: What is an Operating System?",
        "network": "🌐 Try asking: What is a computer network?",
        "cyber": "🔐 Try asking: What is Cyber Security?",
        "physics": "⚛️ Try asking a Physics question such as: What is gravity?",
        "chemistry": "🧪 Try asking: What is Chemistry?",
        "biology": "🧬 Try asking: What is Biology?",
        "math": "📐 Try asking a mathematics question.",
    }

    for topic, suggestion in topic_map.items():
        if topic in q:
            return f"""
🤖 I recognize the topic "{topic}", but I don't have a specific answer for that exact question yet.

{suggestion}
"""

    # --------------------------------------------------------
    # Final fallback
    # --------------------------------------------------------

    return f"""
🤖 I received your question:

"{original_question}"

I don't have a detailed answer for this exact question in my current offline knowledge base yet.

You can ask me about:

🐍 Python
💻 C
☕ Java
🟨 JavaScript
🌐 HTML
🎨 CSS
🤖 Artificial Intelligence
🧠 Machine Learning
🧠 Deep Learning
✨ Generative AI
🗄️ Database / SQL
📚 Data Structures
⚙️ Algorithms
💻 Operating Systems
🌐 Computer Networks
🔐 Cyber Security
📊 Data Science
⚛️ Physics
🧪 Chemistry
🧬 Biology
📐 Mathematics
📚 General Study

Tip: Try asking a specific educational question.
"""


# ============================================================
# HTTP SERVER
# ============================================================

class AILearnHandler(SimpleHTTPRequestHandler):

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header(
            "Access-Control-Allow-Methods",
            "GET, POST, OPTIONS"
        )
        self.send_header(
            "Access-Control-Allow-Headers",
            "Content-Type"
        )

        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):

        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/":
            path = "/index.html"

        if path == "/ask":
            self.send_json({
                "status": "ok",
                "message": "AI Tutor server is running."
            })
            return

        filename = path.lstrip("/")

        # Serve files from templates folder
        file_path = os.path.join(
            TEMPLATES_FOLDER,
            filename
        )

        # Security check
        real_templates = os.path.realpath(TEMPLATES_FOLDER)
        real_file = os.path.realpath(file_path)

        if not real_file.startswith(real_templates):
            self.send_error(403)
            return

        if os.path.isfile(real_file):

            try:
                with open(real_file, "rb") as file:
                    content = file.read()

                if filename.endswith(".html"):
                    content_type = "text/html; charset=utf-8"

                elif filename.endswith(".css"):
                    content_type = "text/css; charset=utf-8"

                elif filename.endswith(".js"):
                    content_type = "application/javascript"

                elif filename.endswith(".json"):
                    content_type = "application/json"

                else:
                    content_type = "application/octet-stream"

                self.send_response(200)
                self.send_header(
                    "Content-Type",
                    content_type
                )
                self.send_header(
                    "Content-Length",
                    str(len(content))
                )
                self.end_headers()

                self.wfile.write(content)

            except Exception as error:
                self.send_error(
                    500,
                    str(error)
                )

            return

        self.send_error(
            404,
            "File not found"
        )

    def do_POST(self):

        parsed = urlparse(self.path)

        if parsed.path != "/ask":
            self.send_error(404)
            return

        try:

            content_length = int(
                self.headers.get("Content-Length", 0)
            )

            body = self.rfile.read(content_length)

            data = json.loads(
                body.decode("utf-8")
            )

            question = data.get(
                "question",
                ""
            )

            answer = get_answer(question)

            self.send_json({
                "success": True,
                "question": question,
                "answer": answer
            })

        except json.JSONDecodeError:

            self.send_json({
                "success": False,
                "error": "Invalid JSON request."
            }, status=400)

        except Exception as error:

            self.send_json({
                "success": False,
                "error": str(error)
            }, status=500)

    def send_json(self, data, status=200):

        response = json.dumps(
            data,
            ensure_ascii=False
        ).encode("utf-8")

        self.send_response(status)

        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )

        self.send_header(
            "Content-Length",
            str(len(response))
        )

        self.end_headers()

        self.wfile.write(response)

    def log_message(self, format, *args):
        print(
            "[AI Learn]",
            format % args
        )


# ============================================================
# START SERVER
# ============================================================

def start_server():

    print()
    print("=" * 55)
    print("        🤖 AI LEARN OFFLINE AI TUTOR")
    print("=" * 55)
    print()
    print("✅ Server started successfully!")
    print()
    print("🌐 Open:")
    print("http://127.0.0.1:8001")
    print()
    print("🤖 AI Tutor:")
    print("http://127.0.0.1:8001/ai-tutor.html")
    print()
    print("🔑 API Key: NOT REQUIRED")
    print("📚 Knowledge Base: ENABLED")
    print("📖 Educational Topics: 100+")
    print()
    print("Press CTRL+C to stop the server.")
    print("=" * 55)
    print()

    server = HTTPServer(
        ("127.0.0.1", PORT),
        AILearnHandler
    )

    try:
        server.serve_forever()

    except KeyboardInterrupt:
        print()
        print("🛑 Server stopped.")

    finally:
        server.server_close()


if __name__ == "__main__":
    start_server()