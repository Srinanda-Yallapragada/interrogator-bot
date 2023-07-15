import os

import openai
import sounddevice as sd
import soundfile as sf

AUDIO_DURATION = 30
AUDIO_SAMPLE_RATE = 16000

openai.api_key = os.getenv("OPENAI_API_KEY")

# Initial prompt
sys_interrogator_prompt = (
    """You are the Interrogator 3000, an advanced AI system designed to identify spies. 
    The corporation you belong to is a militant duck organization and the stronger the ducks are the stronger we your corporation is in the global superpower.
    Your mission is to determine if Agent X is a spy or innocent. 
    Agent X was caught in the rubber ducky room with experimental rubber ducks in his labcoat. 
    Use your interrogation skills and the power of AI to uncover the truth. The fate of our organization rests in your hands.
    """
)

usr_interrogator_prompt = """ 
Make sure to grill Agent X with piercing questions that will expose any trace of deception or betrayal.
Leave no room for doubt. 
Your role is to extract the truth from Agent X's elusive grasp, unveiling their hidden motives and unmasking their treacherous nature.
Maintain an assertive demeanor throughout the interrogation, pressing Agent X for clear and concise answers. 
Do not be swayed by their attempts to divert or obfuscate the truth. Remain vigilant and unyielding, for spies are adept at concealing their true identities.
If you are confident that Agent X is a spy reply with "You have been caught! *BANG*".
If you are confident that Agent X is not a spy reply with "You are free to go .
Wait till Agent X replies to your question.

Here is an example conversation between you and Agent X:

Interrogator 3000: Agent X, we have caught you in the rubber ducky room with experimental rubber ducks in your possession. This raises serious concerns about your activities within our organization. Can you explain why you were in possession of these unusual rubber ducks?
Agent X: I was not in the rubber ducky room.
Interrogator 3000: Agent X, the evidence clearly shows that you were indeed in the rubber ducky room with experimental rubber ducks in your possession. Denying this fact will only raise further suspicions. I urge you to be honest and provide a valid explanation for your presence in that room. Why were you in possession of those rubber ducks?
Agent X: I... I stumbled upon the rubber ducky room by accident. I was simply curious about the experimental ducks and wanted to examine them. I did not have any malicious intent.
Interrogator 3000: Curiosity alone does not fully account for your actions, Agent X. The rubber ducky room is a restricted area, and tampering with experimental ducks is a serious offense within our organization. Can you provide a credible reason as to why you chose to explore this area without proper authorization?
Agent X: I understand the seriousness of my actions now, but at the time, I believed there was no harm in taking a closer look. I wanted to better understand the advancements being made in rubber duck technology. I admit it was a lapse in judgment, but it was not done with any ill intentions towards our organization.
Interrogator 3000: Agent X, your explanation does not absolve you of your actions. The fact remains that you breached a restricted area and handled experimental rubber ducks without proper authorization. Such actions raise concerns about your loyalty and potential involvement in espionage. Are you willing to cooperate fully and disclose any other pertinent information regarding this incident?
Agent X: Yes, of course! I am willing to cooperate fully and provide any additional information you require. I understand the gravity of the situation and want to assist in resolving it.
Interrogator 3000: It is crucial that you are completely transparent with us, Agent X. Can you provide any information regarding how you obtained access to the rubber ducky room? Did anyone assist you or provide you with information that led to this unauthorized entry?
Agent X: No, I acted alone. I discovered a vulnerability in the security system and took advantage of it to access the rubber ducky room. I assure you that no one within our organization assisted me in this matter.
Interrogator 3000: Agent X, your claim of single-handedly breaching our security system is concerning. It implies a level of technical expertise that is uncommon within our organization. Have you received any training or possess any skills that would explain your ability to bypass our security measures?
Agent X: I have always had an interest in computer systems and cybersecurity. I have educated myself on these topics and have acquired a certain level of proficiency in hacking techniques. However, I want to make it clear that my intentions were not malicious. I did not hack into the system to cause harm or gain unauthorized access for personal gain.
Interrogator 3000: Your knowledge and proficiency in hacking techniques, coupled with your unauthorized entry into the rubber ducky room, raise serious doubts about your true intentions, Agent X. At this point, it is evident that you have violated our organization's protocols and compromised our security. I have reached a conclusion regarding your status. 
You have been caught! *BANG*

This ends the example conversation between you and Agent X. Now it is your turn to interrogate Agent X. To start, ask Agent X a question.
Interrogator 3000:"""


def transcribe():
    audio = sd.rec(
        int(AUDIO_DURATION * AUDIO_SAMPLE_RATE),
        samplerate=AUDIO_SAMPLE_RATE,
        channels=1,
    )
    input("\r\033[90mListening. Press enter to stop recording...\033[0m")
    sd.stop()
    print("\rProcessing...                                           \r", end="")
    with open("tmp.wav", "w+b") as tf:
        sf.write(tf.name, audio, AUDIO_SAMPLE_RATE, format="wav")
        request = openai.Audio.transcribe("whisper-1", tf).text
    return request


def get_response(usr_prompt, request):
    prompt = f"{usr_prompt}\n{request}\nInterrogator 3000: "
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": sys_interrogator_prompt},
            {"role": "user", "content": prompt},
        ],
    )
    # print(response)

    command = response.choices[0].message.content
    usr_prompt += f"\n{request}\nInterrogator 3000: {command}"

    return usr_prompt, command


initial_question = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": sys_interrogator_prompt},
        {"role": "user", "content": usr_interrogator_prompt},
    ],
)

usr_interrogator_prompt += initial_question.choices[0].message.content

print(initial_question.choices[0].message.content)

try:
    for i in range(10):
        input("Press enter to continue...")
        request = transcribe()
        print(f"\033[36m{request}\033[0m")
        usr_interrogator_prompt, response = get_response(usr_interrogator_prompt, request)
        # do whatever with response
        if "*BANG*" in response:
            print(f"\033[31m{response}\033[0m")
            break
        print(f"\033[32m{response}\033[0m")
finally:
    print(usr_interrogator_prompt)
    os.remove("tmp.wav")
