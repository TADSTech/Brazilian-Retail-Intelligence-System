"""Markov chain text model for Portuguese review comments."""

from __future__ import annotations

import random
import re
from collections import defaultdict


class SimpleMarkovChain:
    """Order-N word model trained on a list of strings."""

    def __init__(self, state_size: int = 2):
        self.state_size = state_size
        self.chain: dict[tuple[str, ...], list[str]] = defaultdict(list)
        self.start_words: list[tuple[str, ...]] = []

    def train(self, text_list: list[str]) -> None:
        for text in text_list:
            if not isinstance(text, str):
                continue
            words = re.findall(r"\w+|[.,!?;]", text)
            if len(words) < self.state_size:
                continue
            self.start_words.append(tuple(words[: self.state_size]))
            for i in range(len(words) - self.state_size):
                state = tuple(words[i : i + self.state_size])
                self.chain[state].append(words[i + self.state_size])

    def generate(self, max_words: int = 50) -> str:
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
            state = tuple(result[-self.state_size :])
            if next_word in ".!?":
                break
        return " ".join(result).replace(" .", ".").replace(" ,", ",")
