#pip install pylatex
#png files should be in the question_pool directory
#png files should have dimensions 1980 width and 1100 height in pixels with 300 dpi


import os
import random
from pylatex import Document, Section, Subsection, Command, Figure
from pylatex.utils import NoEscape
#from datetime import datetime

def load_questions_from_directory(directory_path, exclude_files=[]):
    """Loads PNG questions from files in the specified directory, excluding specified files."""
    questions = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".png") and filename not in exclude_files:
            questions.append(filename)
    return questions

def generate_exam(questions, total_num_questions, num_variants, fixed_question_files, output_directory, preamble, lecture_number, title, examiner, exam_date, exam_time):
    os.makedirs(output_directory, exist_ok=True)
    
    # Load fixed questions
    fixed_questions_content = []
    if fixed_question_files:  # This checks if the list is not empty
        fixed_questions_content = [fq for fq in fixed_question_files if os.path.exists(os.path.join(questions_directory, fq))]
    
    # Calculate the number of random questions to select
    num_random_questions = total_num_questions - len(fixed_questions_content)
    
    for variant in range(num_variants):
        doc = Document('basic')
        
        # Add custom preamble for title page font size increase, suppressing page number, and reducing margins
        doc.preamble.append(NoEscape(r'\usepackage[margin=0.8in]{geometry}'))
        doc.preamble.append(NoEscape(r'\usepackage{titlesec}'))
        doc.preamble.append(NoEscape(r'\usepackage{titling}'))
        doc.preamble.append(NoEscape(r'\usepackage{fancyhdr}'))
        doc.preamble.append(NoEscape(r'\pagestyle{fancy}'))
        doc.preamble.append(NoEscape(r'\fancyhf{}'))
        doc.preamble.append(NoEscape(r'\fancyhead[L]{\fontsize{12}{14}\selectfont Examination: ' + lecture_number + ' ' + title + '}'))
        doc.preamble.append(NoEscape(r'\fancyhead[R]{\fontsize{12}{14}\selectfont ' + exam_date + '}'))
        doc.preamble.append(NoEscape(r'\renewcommand{\footrulewidth}{0.4pt}'))  # Overline on the footer
        doc.preamble.append(NoEscape(r'\fancyfoot[C]{\fontsize{12}{14}\selectfont \thepage}'))  # Increase footer font size

        # Set the date to empty
        doc.preamble.append(NoEscape(r'\date{}'))
        
        doc.preamble.append(NoEscape(r'\pretitle{\vspace{1cm}\begin{center}\Huge\bfseries}'))
        doc.preamble.append(NoEscape(r'\posttitle{\par\end{center}\vspace{0.5cm}}'))
        doc.preamble.append(NoEscape(r'\preauthor{\vspace{0.5cm}\begin{center}\LARGE}'))
        doc.preamble.append(NoEscape(r'\postauthor{\end{center}\vspace{0.5cm}}'))
        doc.preamble.append(NoEscape(r'\titleformat{\section}{\large\bfseries}{}{0pt}{}'))
        doc.preamble.append(NoEscape(r'\titleformat{\subsection}{\large\bfseries}{}{0pt}{}'))
        doc.preamble.append(NoEscape(r'\titleformat{\subsubsection}{\large\bfseries}{}{0pt}{}'))
        doc.preamble.append(NoEscape(r'\pagenumbering{gobble}'))  # Suppress page number on the first page

        # Title page with specified lines
        doc.preamble.append(NoEscape(r'''
            \title{
                \begin{center}
                    {\LARGE ''' + preamble + r'''}\\[1cm]
                    \textbf{\LARGE ''' + lecture_number + r'''}\\[0.5cm]
                    \textbf{\Huge ''' + title + r'''}\\[1cm]
                    {\Large \normalfont ''' + examiner + r'''}\\[0.5cm]
                    {\Large \normalfont Innsbruck, ''' + exam_date + r'''}\\[0.5cm]
                    {\Large \normalfont ''' + exam_time + r'''}
                \end{center}
            }
        '''))

        # Add title and other information
        doc.append(NoEscape(r'\maketitle'))
        
        doc.append(NoEscape(r'\noindent\rule{\textwidth}{0.4pt}\vspace{1cm}'))  # Horizontal line

        # Guidelines section
        doc.append(NoEscape(r'\section*{\fontsize{16}{18}\selectfont Guidelines:}'))
        doc.append(NoEscape(r'\begin{itemize}'))
        doc.append(NoEscape(r'\item \fontsize{14}{16}\selectfont Time: 60 minutes.'))
        doc.append(NoEscape(r'\item \fontsize{14}{16}\selectfont Turn off your mobile devices or put them in your bag.'))
        doc.append(NoEscape(r'\item \fontsize{14}{16}\selectfont Leave one empty seat between you and your neighbor.'))
        doc.append(NoEscape(r'\item \fontsize{14}{16}\selectfont Do NOT work in teams.'))
        doc.append(NoEscape(r'\end{itemize}'))
        
        doc.append(NoEscape(r'\newpage'))
        doc.append(NoEscape(r'\pagenumbering{arabic}'))  # Resume page numbering from the second page

        # Make sure there are enough questions in the pool after excluding fixed ones
        if len(questions) < num_random_questions:
            print(f"Not enough questions in the pool to select {num_random_questions}.")
            return

        # Select random questions from pool
        selected_random_questions = random.sample(questions, num_random_questions) if num_random_questions > 0 else []
        
        # Combine fixed and random questions then randomize
        combined_questions = fixed_questions_content + selected_random_questions
        random.shuffle(combined_questions)

        # Append combined questions to document
        with doc.create(Section(" ", numbering=False)):
            for i, question in enumerate(combined_questions, start=1):
                with doc.create(Subsection(f"Question {i}", numbering=False)):
                    with doc.create(Figure(position='h!')) as fig:
                        fig.add_image(os.path.join(questions_directory, question), width=NoEscape(r'\textwidth'))
                if i % 2 == 0:  # Add a page break after every second question
                    doc.append(NoEscape(r'\newpage'))

        # Generate PDF
        doc.generate_pdf(f"{output_directory}/exam_variant_{variant + 1}", clean_tex=True) # Change clean_tex to False if you want to keep the intermediate .tex files



# !!!ADJUST YOUR PARAMETERS HERE!!!
questions_directory = "/home/mot/code/random_exam/question_pool"                    #adjust question pool directory
fixed_questions = ['dice1.png']                                                     #adjust based on the actual fixed questions you have as "Q_01.png", "Q_02.png", etc.


questions = load_questions_from_directory(questions_directory, exclude_files=fixed_questions)

generate_exam(
    questions, 
    total_num_questions=3,                                                           #adjust the total number of questions for the exam  
    num_variants=5,                                                                  #adjust the number of variants for the exam
    fixed_question_files=fixed_questions, 
    output_directory="/home/mot/code/random_exam/producedExams",                 #adjust the output directory for the produced exams
    preamble="Examination of the Lecture",                                           #title preamble    
    lecture_number="VO 724650",                                                      #lecture number
    title="Advanced Quantum Chemistry",                                              #lecture title
    examiner="Assoz Prof. Dr. Thomas Hofer",
    exam_date="17.07.2024",                                                          #adjust exam date
    exam_time="10:00"                                                                #adjust exam time
)

print("Exams have been generated.")