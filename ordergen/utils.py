import random
import re
from collections import defaultdict

class SimpleMarkovChain:
    def __init__(self, state_size=2):
        self.state_size = state_size
        self.chain = defaultdict(list)
        self.start_words = []

    def train(self, text_list):
        """
        Train the Markov Chain on a list of strings.
        """
        for text in text_list:
            if not isinstance(text, str):
                continue
            
            # Simple tokenization
            words = re.findall(r'\w+|[.,!?;]', text)
            if len(words) < self.state_size:
                continue
                
            self.start_words.append(tuple(words[:self.state_size]))
            
            for i in range(len(words) - self.state_size):
                state = tuple(words[i:i + self.state_size])
                next_word = words[i + self.state_size]
                self.chain[state].append(next_word)

    def generate(self, max_words=50):
        """
        Generate a random sentence.
        """
        if not self.start_words:
            return "Great product!"

        state = random.choice(self.start_words)
        result = list(state)
        
        for _ in range(max_words):
            next_words = self.chain.get(state)
            if not next_words:
                break
            next_word = random.choice(next_words)
            result.append(next_word)
            state = tuple(result[-self.state_size:])
            
            if next_word in '.!?':
                break
                
        return ' '.join(result).replace(' .', '.').replace(' ,', ',')

def get_random_subset(data_list, sample_size=1000):
    if len(data_list) > sample_size:
        return random.sample(data_list, sample_size)
    return data_list
