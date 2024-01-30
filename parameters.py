import os

id = 0

task_start_index = 0
task_end_index = 100

def increase_id():
    global id  # 明確指定訪問全局變數 id
    id += 1

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

#llama cpp openhermes prompt
cot_prompt_1 = '''
Make a coherent plan of the four sentences.
input: It isn't difficult to do a handstand if you just stand on your hands. It caught him off guard that space smelled of seared steak. When she didn't like a guy who was trying to pick her up, she started using sign language. Each person who knows you has a different perception of who you are.
Plan:
1. Challenging a handstand isn't difficult; the key lies in practice, coordination, and overcoming fear, experiencing the joy of the challenge.
2. Craft a captivating narrative around the unexpected scent of seared steak in space, exploring the profound surprise it brings and reflecting on the broader implications for our understanding of the cosmos.
3. Explore a humorous and intriguing narrative around a woman using sign language as a clever and playful tactic to deter unwanted advances from a guy attempting to pick her up. Delve into the reasons behind her unconventional approach and capture the dynamics of the situation with wit and charm.
4. Explore the unique perceptions each person who knows you holds, reflecting the complexity of interpersonal relationships.
input: {input}
'''

cot_prompt_2 ='''
Write a coherent passage of 4 short paragraphs in topic of input. The end sentence of each paragraph must be constraint
input:
1. Challenging a handstand isn't difficult; the key lies in practice, coordination, and overcoming fear, experiencing the joy of the challenge. (constraint: It isn't difficult to do a handstand if you just stand on your hands.)
2. Craft a captivating narrative around the unexpected scent of seared steak in space, exploring the profound surprise it brings and reflecting on the broader implications for our understanding of the cosmos. (constraint: It caught him off guard that space smelled of seared steak.)
3. Explore a humorous and intriguing narrative around a woman using sign language as a clever and playful tactic to deter unwanted advances from a guy attempting to pick her up. Delve into the reasons behind her unconventional approach and capture the dynamics of the situation with wit and charm. (constraint: When she didn't like a guy who was trying to pick her up, she started using sign language.)
4. Explore the unique perceptions each person who knows you holds, reflecting the complexity of interpersonal relationships. The end sentence of each paragraph must be: It isn't difficult to do a handstand if you just stand on your hands. It caught him off guard that space smelled of seared steak. When she didn't like a guy who was trying to pick her up, she started using sign language. Each person who knows you has a different perception of who you are. (constraint: Each person who knows you has a different perception of who you are.)
Passage: 
1. Challenging a handstand isn't difficult; the key lies in practice, coordination, and overcoming fear, experiencing the joy of the challenge. As you embark on this journey, you'll find that with perseverance and dedication, the seemingly impossible becomes achievable. Each attempt builds strength and stability, gradually transforming the daunting task into a graceful art. Through the ups and downs, you discover the balance between control and freedom, unlocking the secrets of the inverted world. So, take a leap, embrace the learning process, and soon enough, you'll realize that it isn't difficult to do a handstand if you just stand on your hands.

2. In the vast expanse of the cosmos, an astronaut embarks on an extraordinary journey, navigating through the silent vacuum of space. As he floats weightlessly, the unexpected waft of seared steak permeates his senses, jolting him with a surprising blend of nostalgia and disbelief. It caught him off guard that space smelled of seared steak.

3. In the lively ambiance of a bustling café, Emily found herself at the center of attention as a charismatic guy approached, attempting to initiate a conversation. Uninterested and wary of unwanted advances, Emily decided to employ an unconventional strategy. With a mischievous twinkle in her eye, she began weaving a silent dance with her hands, using sign language to convey a message that was both clever and playful. When she didn't like a guy who was trying to pick her up, she started using sign language.

4. Amid the intricate tapestry of life, the diverse array of individuals who have come to know you each paints a distinct portrait of your identity. Some see the unwavering strength in your resilience, while others find solace in the gentle kindness you extend. In the kaleidoscope of perceptions, every connection adds a layer to the multifaceted gem that is you. As relationships unfold, it becomes evident that the lens through which others view you is colored by shared moments, unique experiences, and personal biases. Each person who knows you has a different perception of who you are.
input:
{plan}
{input}
'''

vote_prompt = '''Given an instruction and several choices, decide which choice is most promising. Analyze each choice in detail, then conclude in the last line.

Your output should be of the following format:

"The best choice is {s}", where s the integer id of the choice.
'''

##OpenAI prompt
user_cotprompt_1 = "Make a coherent writing plan of the sentence: {input}. And conclude in only one sentence"

user_cotprompt_2 = "Write a coherent short paragraph in topic of: {plan}. The end sentence of paragraph must be: {input}"

system_voteprompt = '''
Your output should be of the following format:

"The best choice is {s}", where s the integer id of the choice.
'''

user_voteprompt = "Given an instruction and several choices, decide which choice is most promising. Analyze each choice in detail, then conclude in the last line."
    
#tot paper prompt
standard_prompt = '''
Write a coherent passage of 4 short paragraphs. The end sentence of each paragraph must be: {input}
'''

cot_prompt = '''
Write a coherent passage of 4 short paragraphs. The end sentence of each paragraph must be: {input}

Make a plan then write. Your output should be of the following format:

Plan:
Your plan here.

Passage:
Your passage here.
'''


vote_prompt = '''Given an instruction and several choices, decide which choice is most promising. Analyze each choice in detail, then conclude in the last line "The best choice is {s}", where s the integer id of the choice.
'''

compare_prompt = '''Briefly analyze the coherency of the following two passages. Conclude in the last line "The more coherent passage is 1", "The more coherent passage is 2", or "The two passages are similarly coherent".
'''

score_prompt = '''Analyze the following passage, then at the last line conclude "Thus the coherency score is {s}", where s is an integer from 1 to 10.
'''