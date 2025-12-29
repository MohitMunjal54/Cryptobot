
# utils/summarizer.py
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
import json
import os

MEMORY_FILE = "summaries_memory.json"

# Load memory of posted summaries to avoid repetition
if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r") as f:
        MEMORY = json.load(f)
else:
    MEMORY = {"posted": []}

def smart_summarize(text, sentences_count=3):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LexRankSummarizer()
    summary_sentences = summarizer(parser.document, sentences_count)
    summary = " ".join([str(s) for s in summary_sentences])

    # Avoid repetition
    if summary in MEMORY["posted"]:
        return ""
    MEMORY["posted"].append(summary)
    with open(MEMORY_FILE, "w") as f:
        json.dump(MEMORY, f)
    return summary

def analyst_wrap(summary):
    if not summary:
        return "No new insights today."
    # Human-like wrapping
    return f"{summary}\n\nInsightful update from the crypto markets."
