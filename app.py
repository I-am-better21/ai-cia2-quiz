import streamlit as st
import random
import time

#configuration
st.set_page_config(page_title="AI Interactive Quiz - DSC401", page_icon="🧠", layout="centered")

#initializing session state
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'feedback' not in st.session_state:
    st.session_state.feedback = ""

#question bank dictionary
all_questions = [
    #10 real world AI applications scenarios
    {
        "type": "Scenario - Real World Application",
        "question": "A smart room thermostat is programmed to turn on the AC only when the temperature exceeds 24°C. What type of agent is this?",
        "options": ["Model-Based Reflex Agent", "Simple Reflex Agent", "Goal-Based Agent", "Utility-Based Agent"],
        "answer": "Simple Reflex Agent",
        "hint": "It acts solely on the current temperature percept, ignoring past data."
    },
    {
        "type": "Scenario - Real World Application",
        "question": "For a self-driving Uber navigating Bengaluru traffic, what constitutes the 'Actuators' in its PEAS formulation?",
        "options": ["Cameras, LiDAR, GPS, Speedometer", "Safe driving, reaching the destination, avoiding bumps", "Steering wheel, accelerator, brake, signal indicators", "Roads, pedestrians, other vehicles, weather"],
        "answer": "Steering wheel, accelerator, brake, signal indicators",
        "hint": "Actuators are the mechanisms the agent uses to affect its environment."
    },
    {
        "type": "Scenario - Real World Application",
        "question": "You are building an AI to play Chess against a human opponent. How would you classify this environment?",
        "options": ["Partially observable, Stochastic, Continuous", "Fully observable, Deterministic, Discrete", "Fully observable, Stochastic, Episodic", "Partially observable, Deterministic, Static"],
        "answer": "Fully observable, Deterministic, Discrete",
        "hint": "You can see the whole board, moves have guaranteed outcomes, and there are distinct turns."
    },
    {
        "type": "Scenario - Real World Application",
        "question": "You are developing a robotic AI for the international RoboCup soccer tournament. Classify the nature of this environment.",
        "options": ["Fully observable, Deterministic, Static", "Partially observable, Stochastic, Continuous", "Fully observable, Deterministic, Discrete", "Partially observable, Deterministic, Episodic"],
        "answer": "Partially observable, Stochastic, Continuous",
        "hint": "Cameras have blind spots, ball physics/opponent moves are unpredictable, and movement is fluid."
    },
    {
        "type": "Scenario - Real World Application",
        "question": "Google Maps routing algorithms need to find the shortest path while knowing the physical coordinates of the destination. Which search algorithm is best suited?",
        "options": ["Breadth-First Search (BFS)", "Depth-First Search (DFS)", "A* Search", "Iterative Deepening Search"],
        "answer": "A* Search",
        "hint": "It uses a heuristic (spatial straight-line distance) to intelligently guide the search."
    },
    {
        "type": "Scenario - Real World Application",
        "question": "Christ University needs an automated system to schedule exams for 10,000 students without overlapping subjects for any single student. This is best formulated as a...",
        "options": ["Constraint Satisfaction Problem (CSP)", "Turing Test", "Means-End Analysis", "Production System"],
        "answer": "Constraint Satisfaction Problem (CSP)",
        "hint": "You have variables (exams), domains (times), and rules you cannot break (no overlaps)."
    },
    {
        "type": "Scenario - Real World Application",
        "question": "An Amazon AI recommender system doesn't just find a random product; it finds the product that maximizes the user's likelihood of purchasing based on past behavior. What type of agent is this?",
        "options": ["Simple Reflex Agent", "Goal-Based Agent", "Utility-Based Agent", "Model-Based Reflex Agent"],
        "answer": "Utility-Based Agent",
        "hint": "It's trying to maximize a specific 'happiness' or 'success' score (conversion rate), not just achieve a binary goal."
    },
    {
        "type": "Scenario - Real World Application",
        "question": "A customer service chatbot on a banking website successfully convinces a user they are talking to a real human agent. This means the chatbot has successfully passed the...",
        "options": ["Rational Agent Test", "Turing Test", "Chinese Room Experiment", "Heuristic Evaluation"],
        "answer": "Turing Test",
        "hint": "This test measures a machine's ability to exhibit intelligent behavior indistinguishable from a human."
    },
    {
        "type": "Scenario - Real World Application",
        "question": "An AI predicting stock prices gets stuck because it found a strategy that works well in a short 1-week window, but it fails over the whole year. What specific search issue did it encounter?",
        "options": ["Global Maximum", "Local Maxima", "Plateau", "Ridge"],
        "answer": "Local Maxima",
        "hint": "It found a 'peak' that looked like the best option locally, but missed the bigger picture."
    },
    {
        "type": "Scenario - Real World Application",
        "question": "A GPS navigation system calculates the difference between your current location and the destination, and applies a sub-goal to just get onto the nearest highway to reduce this difference. What AI technique is this?",
        "options": ["Means-End Analysis", "Constraint Satisfaction", "Depth-First Search", "Simulated Annealing"],
        "answer": "Means-End Analysis",
        "hint": "It breaks the main goal into smaller sub-goals that reduce the 'distance' to the final goal."
    },

    #5 state-space/search problem calculations
    {
        "type": "State Space Search Problem",
        "question": "In the classic Water Jug problem with a 4-gallon jug and a 3-gallon jug, what is the mathematical representation of the initial state if both are empty?",
        "options": ["(4, 3)", "(0, 0)", "(x, y)", "(Empty, Empty)"],
        "answer": "(0, 0)",
        "hint": "State space is usually represented as a tuple of integers (Jug1_volume, Jug2_volume)."
    },
    {
        "type": "State Space Search Problem",
        "question": "In the 8-puzzle problem, if we use the Manhattan Distance heuristic, what exactly does it calculate to inform the search?",
        "options": ["The number of tiles currently in the wrong position", "The sum of the straight-line distances of each tile from its goal position", "The sum of horizontal and vertical distances of each tile to its goal position", "The depth of the search tree"],
        "answer": "The sum of horizontal and vertical distances of each tile to its goal position",
        "hint": "Manhattan distance refers to grid-like movement (up/down/left/right), not diagonals."
    },
    {
        "type": "State Space Search Problem",
        "question": "Which specific data structures do Breadth-First Search (BFS) and Depth-First Search (DFS) use to manage their frontier (open list), respectively?",
        "options": ["BFS uses a Stack (LIFO), DFS uses a Queue (FIFO)", "BFS uses a Queue (FIFO), DFS uses a Stack (LIFO)", "BFS uses a Priority Queue, DFS uses a Hash Table", "BFS uses a Hash Table, DFS uses a Priority Queue"],
        "answer": "BFS uses a Queue (FIFO), DFS uses a Stack (LIFO)",
        "hint": "BFS evaluates level-by-level (first in, first out), DFS goes as deep as possible (last in, first out)."
    },
    {
        "type": "State Space Search Problem",
        "question": "An A* search algorithm's heuristic function h(n) is mathematically considered 'admissible' only if it...",
        "options": ["Exactly matches the true cost to reach the goal", "Overestimates the true cost to reach the goal", "Never overestimates the true cost to reach the goal", "Ignores the path cost g(n)"],
        "answer": "Never overestimates the true cost to reach the goal",
        "hint": "It must be optimistic. If it thinks the goal is further away than it actually is, A* might miss the shortest path."
    },
    {
        "type": "State Space Search Problem",
        "question": "If a problem's state space is infinite and has no reachable goal state, what will mathematically happen if we execute a standard Depth-First Search (DFS)?",
        "options": ["It will switch to BFS automatically", "It will return a failure immediately", "It will get stuck traversing an infinitely deep path and never terminate", "It will find a suboptimal solution"],
        "answer": "It will get stuck traversing an infinitely deep path and never terminate",
        "hint": "DFS dives down the left-most branch without stopping. If the branch never ends, neither does the search."
    },

    #remaining 35+ syllabus questions
    {
        "type": "MCQ - Problem Characteristics",
        "question": "In the context of AI problem characteristics, if a problem can be broken down into smaller, independent sub-problems that can be solved separately (like computing the integral of a complex polynomial), what type of problem is it?",
        "options": ["Decomposable Problem", "Recoverable Problem", "Ignorable Problem", "Stochastic Problem"],
        "answer": "Decomposable Problem",
        "hint": "Think of the word used when you 'decompose' a large task into smaller, manageable chunks."
    },
    {
        "type": "MCQ - Foundations",
        "question": "Which researcher officially coined the term 'Artificial Intelligence' at the Dartmouth Conference in 1956?",
        "options": ["Alan Turing", "John McCarthy", "Marvin Minsky", "Arthur Samuel"],
        "answer": "John McCarthy",
        "hint": "He is also the inventor of the Lisp programming language."
    },
    {
        "type": "True/False",
        "question": "The Turing Test was designed to evaluate an AI's physical and robotic capabilities to see if it acts humanly.",
        "options": ["True", "False"],
        "answer": "False",
        "hint": "The standard Turing test relies solely on a text-based conversational interface to test cognitive ability, not physical robotics."
    },
    {
        "type": "Assertion-Reason",
        "question": "Assertion (A): A rational agent is considered omniscient.\nReason (R): A rational agent knows the actual outcome of its actions in advance.",
        "options": [
            "Both A and R are True, and R is the correct explanation of A", 
            "Both A and R are True, but R is not the correct explanation of A", 
            "A is True, but R is False", 
            "Both A and R are False"
        ],
        "answer": "Both A and R are False",
        "hint": "Omniscience is impossible in reality. Rationality relies on maximizing expected utility based on *current percepts*, not knowing the future."
    },
    {
        "type": "Fill in the Blanks",
        "question": "The 'Chinese Room' thought experiment was proposed by John Searle to argue against the concept of _______ AI.",
        "options": ["Weak", "Strong", "Narrow", "Symbolic"],
        "answer": "Strong",
        "hint": "It challenges the idea that a machine can possess true consciousness or understanding."
    },
    {
        "type": "Match the Following",
        "question": "Match the AI approach to its definition:\n1) Thinking Humanly\n2) Acting Rationally\n3) Acting Humanly\n\nA) The Turing Test approach\nB) Cognitive Modeling approach\nC) The Rational Agent approach",
        "options": ["1-A, 2-C, 3-B", "1-B, 2-C, 3-A", "1-C, 2-B, 3-A", "1-B, 2-A, 3-C"],
        "answer": "1-B, 2-C, 3-A",
        "hint": "Turing test = Acting Humanly. Cognitive = Thinking Humanly."
    },
    {
        "type": "MCQ - Agent Types",
        "question": "If you build an automated Python AI voice assistant named 'FRIDAY' that eventually adjusts its responses by observing which volume levels you prefer over time, what specific component allows it to improve?",
        "options": ["Performance Element", "Learning Element", "Critic", "Actuator"],
        "answer": "Learning Element",
        "hint": "It takes feedback from the critic and modifies the performance element."
    },
    {
        "type": "True/False",
        "question": "An agent that selects its actions solely based on the current percept, ignoring all previous history, is called a Model-Based Reflex Agent.",
        "options": ["True", "False"],
        "answer": "False",
        "hint": "Model-based agents keep an internal state to track history. This describes a Simple Reflex Agent."
    },
    {
        "type": "MCQ - Environments",
        "question": "A team is developing a full-stack Campus Placement Management System that matches candidate resumes to distinct job postings. How would you classify the time dimension of this environment?",
        "options": ["Continuous", "Discrete", "Dynamic", "Stochastic"],
        "answer": "Discrete",
        "hint": "There are distinct, individual candidates and specific job postings, rather than a constantly flowing time-stream."
    },
    {
        "type": "Fill in the Blanks",
        "question": "In the PEAS framework used for designing intelligent agents, the 'P' stands for _______ Measure.",
        "options": ["Probability", "Percept", "Performance", "Production"],
        "answer": "Performance",
        "hint": "It evaluates how successful the agent is at its task."
    },
    {
        "type": "Assertion-Reason",
        "question": "Assertion (A): Playing Solitaire is a single-agent environment.\nReason (R): There is no opposing entity trying to maximize its own performance measure against you.",
        "options": [
            "Both A and R are True, and R is the correct explanation of A", 
            "Both A and R are True, but R is not the correct explanation of A", 
            "A is True, but R is False", 
            "Both A and R are False"
        ],
        "answer": "Both A and R are True, and R is the correct explanation of A",
        "hint": "You are the only agent altering the state space."
    },
    {
        "type": "MCQ - Agents",
        "question": "An agent tasked with navigating a maze must reach the exit but also wants to find the shortest possible route. Which agent architecture applies?",
        "options": ["Goal-Based Agent", "Utility-Based Agent", "Simple Reflex Agent", "Learning Agent"],
        "answer": "Utility-Based Agent",
        "hint": "It doesn't just want to reach the goal (exit); it wants a high 'happiness/efficiency' score."
    },
    {
        "type": "Fill in the Blanks",
        "question": "A search space where actions can be easily undone to return to the previous state (like moving a tile in the 8-puzzle) is known as a _______ problem.",
        "options": ["Decomposable", "Recoverable", "Ignorable", "Stochastic"],
        "answer": "Recoverable",
        "hint": "You can 'recover' from mistakes."
    },
    {
        "type": "True/False",
        "question": "In a formal state-space search formulation, the 'Path Cost' function assigns a numeric cost to each path.",
        "options": ["True", "False"],
        "answer": "True",
        "hint": "Usually denoted as g(n), it adds up the step costs."
    },
    {
        "type": "Match the Following",
        "question": "Match the components of a Production System:\n1) Global Database\n2) Production Rules\n3) Control Strategy\n\nA) Condition-Action pairs\nB) Central data structure representing the state\nC) Conflict resolution logic",
        "options": ["1-A, 2-B, 3-C", "1-B, 2-C, 3-A", "1-B, 2-A, 3-C", "1-C, 2-A, 3-B"],
        "answer": "1-B, 2-A, 3-C",
        "hint": "The database holds the state, rules are 'IF-THEN', and control resolves conflicts."
    },
    {
        "type": "Assertion-Reason",
        "question": "Assertion (A): Theorem proving is considered an ignorable problem characteristic.\nReason (R): The exact sequence of steps taken to prove the theorem does not matter, as long as the final proof is valid.",
        "options": [
            "Both A and R are True, and R is the correct explanation of A", 
            "Both A and R are True, but R is not the correct explanation of A", 
            "A is True, but R is False", 
            "Both A and R are False"
        ],
        "answer": "Both A and R are True, and R is the correct explanation of A",
        "hint": "If you derive unnecessary facts along the way, you can just ignore them at the end."
    },
    {
        "type": "MCQ - Problem Spaces",
        "question": "Which of the following is NOT an issue typically encountered in the design of search programs?",
        "options": ["Direction in which to conduct the search (forward/backward)", "How to represent nodes", "Selecting the right control strategy", "Increasing the clock speed of the CPU"],
        "answer": "Increasing the clock speed of the CPU",
        "hint": "The first three are algorithmic design issues; the last is a hardware constraint."
    },
    {
        "type": "Assertion-Reason",
        "question": "Assertion (A): Iterative Deepening DFS is generally preferred over standard BFS when memory space is limited.\nReason (R): Iterative Deepening has a linear space complexity O(bd) while BFS has an exponential space complexity O(b^d).",
        "options": [
            "Both A and R are True, and R is the correct explanation of A", 
            "Both A and R are True, but R is not the correct explanation of A", 
            "A is True, but R is False", 
            "Both A and R are False"
        ],
        "answer": "Both A and R are True, and R is the correct explanation of A",
        "hint": "IDDFS gives you the completeness of BFS but uses the memory-efficient approach of DFS."
    },
    {
        "type": "Match the Following",
        "question": "Match the uninformed search algorithm to its time complexity (where b = branching factor, d = depth of shallowest goal, m = maximum depth):\n1) BFS\n2) DFS\n3) Iterative Deepening\n\nA) O(b^m)\nB) O(b^d)\nC) O(b^d)",
        "options": ["1-B, 2-A, 3-C", "1-A, 2-B, 3-C", "1-C, 2-A, 3-B", "1-B, 2-C, 3-A"],
        "answer": "1-B, 2-A, 3-C",
        "hint": "BFS and IDDFS are bound by goal depth (d). DFS is bound by max depth (m)."
    },
    {
        "type": "True/False",
        "question": "Depth-First Search (DFS) is an optimal search strategy when all step costs are equal.",
        "options": ["True", "False"],
        "answer": "False",
        "hint": "DFS might find a deeply nested goal first, completely missing a shallower (more optimal) goal."
    },
    {
        "type": "Fill in the Blanks",
        "question": "In Hill Climbing, a _______ is an area of the search space that is higher than surrounding areas, but cannot be traversed by single moves because it drops off steeply on the sides.",
        "options": ["Plateau", "Local Maximum", "Ridge", "Global Maximum"],
        "answer": "Ridge",
        "hint": "Think of a mountain ridge that requires zig-zag movements."
    },
    {
        "type": "True/False",
        "question": "Steepest-Ascent Hill Climbing evaluates all neighboring states and chooses the one closest to the goal, rather than just picking the first better state it finds.",
        "options": ["True", "False"],
        "answer": "True",
        "hint": "Standard hill climbing takes the first better option; steepest-ascent checks all neighbors first."
    },
    {
        "type": "MCQ - Local Search",
        "question": "What is the primary method 'Random-Restart Hill Climbing' uses to overcome getting stuck in local maxima?",
        "options": ["It increases a temperature parameter", "It conducts a series of hill-climbing searches from randomly generated initial states", "It stores a memory of visited nodes", "It switches to Breadth-First Search"],
        "answer": "It conducts a series of hill-climbing searches from randomly generated initial states",
        "hint": "If you get stuck on a small hill, teleport to a random spot on the map and try climbing again."
    },
    {
        "type": "Assertion-Reason",
        "question": "Assertion (A): Simulated Annealing sometimes accepts a move that results in a worse state.\nReason (R): This helps the algorithm jump out of local maxima.",
        "options": [
            "Both A and R are True, and R is the correct explanation of A", 
            "Both A and R are True, but R is not the correct explanation of A", 
            "A is True, but R is False", 
            "Both A and R are False"
        ],
        "answer": "Both A and R are True, and R is the correct explanation of A",
        "hint": "It uses a 'temperature' schedule to occasionally allow bad moves to escape local peaks."
    },
    {
        "type": "Match the Following",
        "question": "Match the Hill Climbing issue to its definition:\n1) Local Maximum\n2) Plateau\n3) Ridge\n\nA) A flat area where all neighbors have the same value\nB) A peak that is higher than neighbors, but lower than the global peak\nC) A sequence of local maxima difficult to traverse",
        "options": ["1-B, 2-A, 3-C", "1-A, 2-B, 3-C", "1-C, 2-A, 3-B", "1-B, 2-C, 3-A"],
        "answer": "1-B, 2-A, 3-C",
        "hint": "Local max is a fake peak. Plateau is flat. Ridge is steep."
    },
    {
        "type": "Fill in the Blanks",
        "question": "In informed search strategies, the function usually denoted as ____(n) estimates the cost of the cheapest path from node n to the goal.",
        "options": ["g", "f", "h", "c"],
        "answer": "h",
        "hint": "It stands for the heuristic function."
    },
    {
        "type": "MCQ - Heuristics",
        "question": "Vinit and Karan are coding an A* search algorithm for Bengaluru traffic routing. Their evaluation function is f(n) = g(n) + h(n). What does g(n) represent here?",
        "options": ["The estimated cost from n to the destination", "The total estimated cost of the entire trip", "The actual path cost from the start node to node n", "The straight-line distance between nodes"],
        "answer": "The actual path cost from the start node to node n",
        "hint": "g(n) is the 'ground' you've already covered."
    },
    {
        "type": "True/False",
        "question": "Greedy Best-First Search evaluates nodes purely based on f(n) = h(n), meaning it only looks at how close a node appears to be to the goal.",
        "options": ["True", "False"],
        "answer": "True",
        "hint": "It is 'greedy' because it ignores the path cost g(n) taken so far."
    },
    {
        "type": "Assertion-Reason",
        "question": "Assertion (A): The A* search algorithm is optimally efficient for a given admissible heuristic.\nReason (R): No other optimal algorithm will expand fewer nodes than A* using the same heuristic.",
        "options": [
            "Both A and R are True, and R is the correct explanation of A", 
            "Both A and R are True, but R is not the correct explanation of A", 
            "A is True, but R is False", 
            "Both A and R are False"
        ],
        "answer": "Both A and R are True, and R is the correct explanation of A",
        "hint": "A* is mathematically proven to do the least amount of work possible while still guaranteeing the shortest path."
    },
    {
        "type": "MCQ - CSP",
        "question": "In a Constraint Satisfaction Problem (CSP), what do we call the set of allowable values for a specific variable?",
        "options": ["Scope", "Domain", "Relation", "Node"],
        "answer": "Domain",
        "hint": "Variables map to this set."
    },
    {
        "type": "Fill in the Blanks",
        "question": "Sudoku is a classic example of a Constraint Satisfaction Problem. The rule that no number can repeat in a row is an example of a _______ constraint.",
        "options": ["Unary", "Binary", "Global / Alldiff", "Domain"],
        "answer": "Global / Alldiff",
        "hint": "It involves multiple variables having to be 'all different'."
    },
    {
        "type": "Match the Following",
        "question": "Match the CSP terminology:\n1) Variables\n2) Domain\n3) Constraints\n\nA) Conditions that specify allowable combinations of values\nB) The entities that need to be assigned values\nC) The set of possible values",
        "options": ["1-B, 2-C, 3-A", "1-A, 2-B, 3-C", "1-C, 2-B, 3-A", "1-B, 2-A, 3-C"],
        "answer": "1-B, 2-C, 3-A",
        "hint": "Variables take values from the Domain without violating Constraints."
    },
    {
        "type": "Assertion-Reason",
        "question": "Assertion (A): Means-End Analysis solves problems by finding differences between the current state and the goal state.\nReason (R): It applies operators that reduce this specific difference, often creating sub-goals along the way.",
        "options": [
            "Both A and R are True, and R is the correct explanation of A", 
            "Both A and R are True, but R is not the correct explanation of A", 
            "A is True, but R is False", 
            "Both A and R are False"
        ],
        "answer": "Both A and R are True, and R is the correct explanation of A",
        "hint": "It analyzes the 'means' to achieve the 'ends'."
    },
    {
        "type": "True/False",
        "question": "In Means-End Analysis, if an operator cannot be applied to the current state, the algorithm immediately fails and terminates.",
        "options": ["True", "False"],
        "answer": "False",
        "hint": "If it can't apply the operator, it creates a 'sub-goal' to reach a state where the operator CAN be applied."
    },
    {
        "type": "MCQ - MEA",
        "question": "Which early AI program, developed by Newell and Simon, is most famous for implementing Means-End Analysis to solve logical problems?",
        "options": ["ELIZA", "General Problem Solver (GPS)", "Deep Blue", "MYCIN"],
        "answer": "General Problem Solver (GPS)",
        "hint": "It was designed in 1959 to solve general problems using difference tables."
    }
]

#UI and logic
st.title("🧠 AI Concepts Quiz: Units I & II")
st.markdown("Test your knowledge on Intelligent Agents, Environments, and Search Strategies.")

if not st.session_state.quiz_started:
    if st.button("Start Quiz"):
        #shuffle questions to meet the "randomized" requirement
        random.shuffle(all_questions)
        st.session_state.questions = all_questions
        st.session_state.quiz_started = True
        st.session_state.score = 0
        st.session_state.current_q = 0
        st.rerun()
else:
    #progress Bar
    progress = st.session_state.current_q / len(st.session_state.questions)
    st.progress(progress)
    st.write(f"Question {st.session_state.current_q + 1} of {len(st.session_state.questions)}")
    
    if st.session_state.current_q < len(st.session_state.questions):
        q = st.session_state.questions[st.session_state.current_q]
        st.subheader(f"[{q['type']}]")
        st.write(q['question'])
        
        #hint Feature
        with st.expander("💡 Need a Lifeline/Hint?"):
            st.info(q['hint'])
            
        choice = st.radio("Select your answer:", q['options'], index=None)
        
        if st.button("Submit Answer"):
            if choice == q['answer']:
                st.session_state.score += 1
                st.success("✅ Correct!")
            else:
                st.error(f"❌ Incorrect. The correct answer was: {q['answer']}")
            
            time.sleep(1.5) #brief pause for immediate feedback
            st.session_state.current_q += 1
            st.rerun()
    else:
        st.balloons()
        st.header("Quiz Complete! 🎉")
        st.subheader(f"Your Final Score: {st.session_state.score} / {len(st.session_state.questions)}")
        if st.button("Restart Game"):
            st.session_state.quiz_started = False
            st.rerun()