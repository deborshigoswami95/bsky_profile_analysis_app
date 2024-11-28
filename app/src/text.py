import demoji
import spacy
from urlextract import URLExtract
import contractions
import re

BASE_CLEAN_TEXT_RESPONSE = {'text':None,'clean_text':None,'url':None}
URL_PLACEHOLDER = '[URL]'
EMOJI_PLACEHOLDER = '[E]'
URL_EXTRACTOR = URLExtract()
NLP = spacy.load("en_core_web_sm")

def clean_text(text):

    if not text:
        return BASE_CLEAN_TEXT_RESPONSE
    
    text = text.replace('\n',' ')
    text = contractions.fix(text)
    urls = URL_EXTRACTOR.find_urls(text)
    emojis = demoji.findall(text)

    doc = None
    
    if len(urls):
        for url in urls:
            #doc = text.replace(url, ' ')
            text = text.replace(url, URL_PLACEHOLDER)
            
    if len(emojis):
        for emoji in emojis:
            #doc = text.replace(emoji, ' ')
            text = text.replace(emoji, EMOJI_PLACEHOLDER)
            

    doc = text.replace(URL_PLACEHOLDER, ' ')
    doc = doc.replace(EMOJI_PLACEHOLDER, ' ')
    doc = NLP(doc)
    
    filtered_tokens = [token.text for token in doc if (token.is_alpha or token.is_digit) and not token.is_stop and not token.is_punct]

    reconstructed_string = ' '.join(filtered_tokens)
    

    return {
        'text':text,
        'clean_text':reconstructed_string,
        'url':urls,
        'emojis':emojis
    }