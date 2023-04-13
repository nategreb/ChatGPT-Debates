import os
import textwrap
import openai


openai.api_key = os.environ['API_KEY']
MODEL = "gpt-3.5-turbo"


# 1-2 sentence ~= 30 tokens

class Debater:
    def __init__(self, subject, position, max_sentences):
        self.subject = subject
        self.position = position
        self.max_tokens = int(max_sentences) * 40
        self.max_sentences = max_sentences
        self.name = self.position.replace(' ', '-')

    def send_message(self, message):
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=self.create_prompt(message),
            temperature=1,
            max_tokens=self.max_tokens
        )
        return response

    def create_prompt(self, message):
        return [{
            'role': 'user',
            'name': self.name,
            'content':
                f'Your position is {self.position} in the {self.subject}. Answer in a way that aligns with this '
                f'position. Keep your answer to {self.max_sentences} sentences.'                                
                f'Respond to the following: message:{message}'
                f'answer: '
        }]


if __name__ == '__main__':
    debate_subject = input("Give the agents a subject: ")

    agent1_position = input("Give agent 1 a position: ")
    agent2_position = input("Give agent 2 a position: ")

    max_sentences = input("Response sentence length: ")

    agent1 = Debater(debate_subject, agent1_position, max_sentences)
    agent2 = Debater(debate_subject, agent2_position, max_sentences)

    # moderator: initiate the conversation
    moderator_input = input('Moderation start the conversation. Ask your first question: ')

    # moderator_input keeps track of the last message
    while True:
        if moderator_input.lower() == 'q':
            print("Exiting program...")
            break
        else:
            agent1_response = agent1.send_message(moderator_input).choices[0]['message']['content']
            print(textwrap.fill(agent1_response, width=80))
            moderator_input = input('Moderation guide the message to the next agent: ')
            agent2_response = agent2.send_message(f'{moderator_input} {agent1_response}').choices[0]['message'][
                'content']
            print(textwrap.fill(agent2_response, width=80))
            moderator_input = agent2_response
