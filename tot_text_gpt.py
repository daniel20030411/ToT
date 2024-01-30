import os
import re
import time
import random
import matplotlib.pyplot as plt
from datetime import date
from openai import OpenAI
from parameters import *

llm = OpenAI(
    api_key = OPENAI_API_KEY
)

def Generator(llm, node):
    new_node ={}
    output = []
    completion_token_3 = 0##calculate usage
    prompt_token_3 = 0 
    ##
    a = node[1]['answer'][0].split('. ')
    a = [sentence.strip() for sentence in a if sentence.strip()]
    for i in range(len(a)):
        a[i] += '.'
    ##put rootnode['answer'] into a 4 or 3 elements list
    print("    Generating...")
    for _ in range(5):
        ans_from_llm = {}
        filtered_ans = ""
        print(f"\tsending request to gpt...{_}")
        for i in range(len(a)):    
            if node[0] == None:###no plan
                user_content = user_cotprompt_1.format(input = a[i])
                ans_from_llm = llm.chat.completions.create(
                    model = 'gpt-3.5-turbo-1106',
                    temperature = 1.0,
                    messages = [
                        {"role": "user", "content": user_content}
                    ]
                )
                filtered_ans += ans_from_llm.choices[0].message.content + "\n"
                # print('ok\t')
                completion_token_3 += ans_from_llm.usage.completion_tokens
                prompt_token_3 += ans_from_llm.usage.prompt_tokens
            else:
                ##
                b = node[0][0]['answer'][0].split('. ')
                b = [sentence.strip() for sentence in b if sentence.strip()]
                for j in range(len(b)):
                    b[j] += '.'
                ##put plan['answer'] into a 4 or 3 elements list
                    
                user_content = user_cotprompt_2.format(input = a[i], plan = b[i])

                check_1 = False        
                for _ in range(5):      
                    if check_1 == False:
                        ans_from_llm = llm.chat.completions.create(
                            model = 'gpt-3.5-turbo-1106',
                            temperature = 1.0,
                            messages = [
                                {"role": "user", "content": user_content}
                            ]
                        )
                        completion_token_3 += ans_from_llm.usage.completion_tokens
                        prompt_token_3 += ans_from_llm.usage.prompt_tokens
                        check_1 = check(ans_from_llm.choices[0].message.content, a[i])
                    else: break
                # print(ans_from_llm.choices[0].message.content + '\n\n')    
                filtered_ans += ans_from_llm.choices[0].message.content + "\n"
                # print('ok\t')
        
        new_node['id'] = id
        increase_id()
        new_node['answer'] = [filtered_ans]
        new_node['value'] = None
        new_node['parent_node'] = node[1]['id']
        new_node['ancester_value'] = None

        output.append(new_node)
    output.append([completion_token_3, prompt_token_3])
        # print('@')
    return output

        

def Evaluator(llm, node):#node = []
    new_node = {}
    output = []
    best = []
    ans_from_llm = {}
    completion_token_3 = 0##calculate usage
    prompt_token_3 = 0

    print("    Evaluating...")
    ans_from_llm = llm.chat.completions.create(
        model = 'gpt-3.5-turbo-1106',
        temperature = 1.0,
        messages = [
            {"role": "system", "content": system_voteprompt},
            {"role": "user", "content": user_voteprompt + 'Choices: ' + node[0]['answer'][0] + node[1]['answer'][0] + node[2]['answer'][0] + node[3]['answer'][0] + node[4]['answer'][0]}
        ]
    )
    completion_token_3 += ans_from_llm.usage.completion_tokens
    prompt_token_3 += ans_from_llm.usage.prompt_tokens
    best = ans_from_llm.choices[0].message.content.split()##暫時用random解決問題

    if len(best) == 5:    
        for i in range(5):
            if best[4] == str(node[i]['id']):
                break
        new_node = node[i]
    else:
        new_node = node[random.randint(0, 4)]
    output.append(new_node)
    output.append([completion_token_3, prompt_token_3])
    return output

def Grade(llm, text):
    scores = []
    completion_tokens_4 = 0
    prompt_tokens_4 = 0

    print("    Grading...")
    for _ in range(5):# grade for 5 times
        print(f"\tsending request to gpt...{_}")
        try:
            ans_from_llm = llm.chat.completions.create(
                model='gpt-4-0613',
                temperature = 1.0,
                messages=[
                    {"role": "user", "content": score_prompt + text}
                ]
            )
            
            completion_tokens_4 += ans_from_llm.usage.completion_tokens
            prompt_tokens_4 += ans_from_llm.usage.prompt_tokens

            filtered_ans = ans_from_llm.choices[0].message.content
            match = re.search(r'\d+', filtered_ans)

            if match and match.group().isdigit():
                scores.append(int(match.group()))
        except Exception as e:
            print(f"An error occurred during grading: {e}")

    average_score = sum(scores) / len(scores) if scores else 0
    return [average_score, [completion_tokens_4, prompt_tokens_4]]

def check(text, input_data):##examine if last sentence is matched input
    fragment_1 = text.replace(', ', '. ')
    fragments_1 = fragment_1.split('. ')

    for i in range(len(fragments_1)):
        fragments_1[i] = fragments_1[i].strip()

    if fragments_1[-1] in input_data:
        return True
    else:
        return False

def Draw(data_list, folder):##draw the barchart
    plt.bar(range(len(data_list)), height = data_list)

    plt.title('Score for each data')
    plt.xlabel('Data index')
    plt.ylabel('Score')

    for i, value in enumerate(data_list):
        plt.text(i, value + 0.1, str(value), ha='center', va='bottom')

    save_path = os.path.join(folder, 'Data barchart.png')
    plt.savefig(save_path)

if __name__ == '__main__':
    score_list = []## record all the score
    scores = 0
    print(f"generating model = \"gpt-3.5-turbo-1106\", grading model = \"gpt-4-0613\", temperature = 1.0")
    with open('data_100_random_text.txt', 'r', encoding='utf-8') as file:
        data = file.readlines()
    
    folder_name = f'GPT Result {date.today()}'## build new folder 'GPT Result 2024-01-19'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    for i in range(task_start_index, task_end_index):################################################改range就可以指定跑哪幾組###############################
        start = time.time()
        print(f"Solving index = {i}")
        file_name = f'{folder_name}/result_{i}.txt'### txt name    
        root_node = {
            'id':id,
            'answer':[data[i]],
            'value':None,
            'parent_node':None,
            'ancester_value':None
        }
        increase_id()

        completion_token_3 = 0
        prompt_token_3 = 0
        completion_token_4 = 0
        prompt_token_4 = 0
        cost=0

        writing_plans = Generator(llm, [None, root_node])### Generator(llm, [plan, root_node])  no plan -->None
        completion_token_3 += writing_plans[-1][0]
        prompt_token_3 += writing_plans[-1][1]
        writing_plans = writing_plans[:-1]
        
        best_plan = Evaluator(llm, writing_plans)
        completion_token_3 += best_plan[-1][0]
        prompt_token_3 += best_plan[-1][1]
        best_plan = best_plan[:-1]

        passages = Generator(llm, [best_plan, root_node])
        completion_token_3 += passages[-1][0]
        prompt_token_3 += passages[-1][1]
        passages = passages[:-1]

        best_passage = Evaluator(llm, passages)
        completion_token_3 += best_passage[-1][0]
        prompt_token_3 += best_passage[-1][1]
        best_passage = best_passage[:-1]

        graded = Grade(llm, best_passage[0]['answer'][0])
        score = graded[0]
        completion_token_4 = graded[1][0]###
        prompt_token_4 = graded[1][1]###

        cost = (completion_token_3*0.002 + prompt_token_3*0.001 + completion_token_4*0.003 + prompt_token_4*0.001)/1000

        with open(file_name, 'w', encoding='utf-8') as file:### open new txt
            file.write(root_node['answer'][0])
            file.write('\n...........................\n')
            file.write(best_plan[0]['answer'][0])
            file.write('\n--- --- --- --- --- --- ---\n')
            file.write(best_passage[0]['answer'][0])
            file.write('\n---------------------------\n')
            file.write(f"\n\nThe coherent score is {score}")
            file.write(f"\n\ngpt-3.5 completion token = {completion_token_3}")
            file.write(f"\ngpt-3.5 prompt token = {prompt_token_3}")
            file.write(f"\ngpt-4 completion token = {completion_token_4}")
            file.write(f"\ngpt-4 prompt token = {prompt_token_4}")
            file.write(f"\ncost = {cost}")
            print(root_node['answer'][0])
            print('...........................')
            print(best_plan[0]['answer'][0])
            print('--- --- --- --- --- --- ---')
            print(best_passage[0]['answer'][0])
            print('---------------------------')
            print(f"gpt-3.5 completion token = {completion_token_3}")
            print(f"gpt-3.5 prompt token = {prompt_token_3}")
            print(f"gpt-4 completion token = {completion_token_4}")
            print(f"gpt-4 prompt token = {prompt_token_4}")
            print(f"cost = {cost}")
        finish = time.time()
        with open(file_name, 'a', encoding='utf-8') as file:
            file.write(f"\n\ntotal time = {finish - start}\n")
            print(f"total time = {finish - start}")
            print(f"\nid = {i}, score = {score}\n")
       
        score_list.append(score)
        scores += score
        # print(score)
    Draw(score_list, folder_name)
    for i in range(task_start_index, task_end_index):
        print(f"idx {i} : {score_list[i]}")
    avg_score = scores/(task_end_index-task_start_index)
    print(f"\naverage score = {avg_score}")
    # print(finish - start)
    print("\n---------- DONE! ----------")
             
    
