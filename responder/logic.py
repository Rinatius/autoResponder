from nltk.tokenize import sent_tokenize


def make_paired_sentences(article_text):
    sentences = sent_tokenize(article_text)
    couple_sentences = [f'{sentences[i]} {sentences[i + 1]}' for i in range(len(sentences) - 1)]

    return couple_sentences
