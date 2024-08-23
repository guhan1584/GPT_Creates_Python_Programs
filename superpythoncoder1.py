import os
from openai import OpenAI
from dotenv import load_dotenv
import subprocess
import random
import colorama
import tqdm

from colorama import Fore, Style
from tqdm import tqdm

load_dotenv()
client = OpenAI(
    organization ='org-2CwskBzgGP5OnJE5rJP2GrIS' ,
    api_key = os.environ.get("Test_Key_Reichman_1")
)
program_options = [ '''If the user described a program do what he asked. If he pressed enter, create one program from the list below: Given two strings str1 and
                    str2, prints all interleavings of the given two strings. You may assume that all characters in both strings are
                    different.Input: str1 = AB, str2 = CD Output: ABCD \n ACBD \n ACDB \n CABD \n CADB \n CDAB]''' ,
                    #'''Input: str1 = AB, str2 = C Output: ABC \n ACB \n CAB  ''',
                    '''Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays.''',
                    #'''a program that checks if a number is a palindrome''',
                    '''Implement pow(x, n), which calculates x raised to the power n (i.e., xn).''',
                    '''A program that finds the kth smallest element in a given binary search tree.''',
                    #'''Find the minimum number in a stack of 20 items'''
                    '''Given an input string (s) and a pattern (p), implement wildcard pattern matching with support for '?' and '*' where:
                    '?' Matches any single character.
                    '*' Matches any sequence of characters (including the empty sequence).
                    The matching should cover the entire input string (not partial).''']
chosen_program = ""

def request_and_responses(): # A function that asks the user for a program and return the input of the user
    user_input= input('''Tell me, which program would you like me to code for you? If you don't have an idea,
                       just press enter and I will choose a random program to code''')
    if(user_input == ""):
        chosen_program = random.choice(program_options)
        return "write the program - " + chosen_program
    else:
        return user_input
    
def gpt_prompting(request):
    chat_completion_1 = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
            "content": '''You are an expert python developer, You are able to create any program in the world in the most aesthetic way without unnecessary text.
                DO NOT write any explanations NOR add any text. JUST SHOw ME THE CODE itself. In addition to the chosen program, include 5 DIFFERENT unit tests. In the unit tests, use asserts methods, that check the logic of the program.
                Again, DO NOT add any texts beside the code itself. Please make sure the code is well-structured with proper indentation.'''},
            {"role": "user", 
            "content": "Hey, can you create for me a python code? any code but WITHOUT any addition text, ONLY THE CODE."},
            {"role": "assistant", 
            "content": "num = 4 \n if(num == 4) \n print(True)"},
            {"role": "user",
            "content": request},
        ]
    )
    response = chat_completion_1.choices[0].message.content
    return response
    
def creating_file(response , file_path):
    with open(file_path, "w+") as file: file.write(response)

request = request_and_responses()
file_path = r"C:\Users\guhan\Desktop\assignments\AI_developing\Assignments_environment\venv\Assignment_1\CreatedCode.py"

generated_errors = []
fail_flag = True # A flag to check if the code generation failed

for i in tqdm(range(5)):
    if not generated_errors:
        generated_response = gpt_prompting(request)
        generated_response += "a" # to make noise for the GPT, else he successeed on the first try
    else:
        generated_response = gpt_prompting(request)

    #print(generated_response) #checking status of responses
    
    creating_file(generated_response, file_path)
    result = subprocess.run(["python" ,file_path],capture_output=True,text=True)
    if(result.returncode == 0):
        print(Fore.BLUE + generated_response + Style.RESET_ALL) #print the fixed code
        print(Fore.GREEN + " Code creation completed successfully !" + Style.RESET_ALL)
        fail_flag = False
        if(os.name == 'nt'):
            os.startfile(file_path)
            #subprocess.call(["open", file_path])
            print(Fore.BLUE + result.stdout + Style.RESET_ALL) #print the output    
        break
    else:
        #error = result.stderr.split(":")[2]
        generated_errors.append(result.stderr)
        request = f'''I have an error, this is my error: \n \n {Fore.RED + generated_errors[-1] + Style.RESET_ALL} \n \n This is the code that triggerd the error: \n \n {Fore.BLUE + generated_response + Style.RESET_ALL} \n \n 
                    You are an expert python programmer. Please, fix the error, and show me the whole code after you fixed it.
                    FIX THE CODE, and Return ONLY the FIXED CODE with 5 unit tests and asserts. No addition text and without the error.
                    '''       
        print(Fore.RED + "Error running generated code! Error:" + result.stderr + Style.RESET_ALL)
        #print(request) # Checking the request

if(fail_flag): print(Fore.RED + "Code generation FAILED" + Style.RESET_ALL)
    