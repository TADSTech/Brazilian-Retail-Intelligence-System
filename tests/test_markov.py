from __future__ import annotations

from ordergen.markov import SimpleMarkovChain


def test_markov_generates_text_after_training():
    model = SimpleMarkovChain(state_size=1)
    model.train(["Produto excelente recomendo", "Produto ruim não recomendo"])
    text = model.generate(max_words=10)
    assert isinstance(text, str)
    assert text


def test_markov_untrained_returns_fallback():
    model = SimpleMarkovChain()
    assert model.generate() == "Great product!"


def test_markov_skips_short_and_non_string():
    model = SimpleMarkovChain(state_size=2)
    model.train(["hi", None, 42, "one two three"])
    assert model.start_words
