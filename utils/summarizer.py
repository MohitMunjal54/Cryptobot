from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
import hashlib
import json
import os
import random

MEMORY_FILE = "storage/summaries_memory.json"

if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r") as f:
        USED_SUMMARIES = set(json.load(f))
else:
    USED_SUMMARIES = set()

def _save_memory():
    with open(MEMORY_FILE, "w") as f:
        json.dump(list(USED_SUMMARIES), f)

def smart_summarize(text, sentences_count=3):
    try:
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LexRankSummarizer()
        summary_sentences = summarizer(parser.document, sentences_count)
        summary = " ".join(str(s) for s in summary_sentences)
    except Exception:
        # fallback simple slicing
        sentences = text.split(". ")
        summary = ". ".join(sentences[:sentences_count])

    # avoid repetition
    text_hash = hashlib.md5(summary.encode()).hexdigest()
    if text_hash in USED_SUMMARIES:
        sentences = text.split(". ")
        summary = ". ".join(sentences[:sentences_count])

    USED_SUMMARIES.add(text_hash)
    _save_memory()
    return summary

def analyst_wrap(summary: str) -> str:
    intros = ["Market takeaway:", "Why this matters:", "Key insight:", "Top highlight:"]
    return random.choice(intros) + " " + summary
