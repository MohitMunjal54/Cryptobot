from gensim.summarization import summarize

def ai_summarize(text, ratio=0.25):
    try:
        return summarize(text, ratio=ratio)
    except:
        return text[:500]  # fallback
