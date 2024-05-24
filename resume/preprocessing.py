from nltk.tokenize import word_tokenize
import re

def cleaning(tx):
    text = tx.replace('\n',' ')
    text = text.replace('\r',' ')
    text = text.replace('/',', ')
    text = re.sub(r'([!"$%\'()*:;<=>?\]\[\\^_`{|}~])', '',text )
    text = re.sub(r'\S+@\S+',' ',text)
    text = re.sub(r'www\S+', ' ', text)
    text = re.sub(' +',' ',text)
    text = text.strip().lower()
    return text

def split_into_sentences(text, max_tokens=150):
    sentences = []
    tokens = word_tokenize(text)
    current_sentence = []
    token_count = 0
    for token in tokens:
        current_sentence.append(token)
        token_count += 1
        if token_count >= max_tokens:
            sentences.append(" ".join(current_sentence))
            current_sentence = []
            token_count = 0
    if current_sentence:  # If there are remaining tokens
        sentences.append(" ".join(current_sentence))
    return sentences


def extract_entities(bio_result,skills):
    entity = ''
    entities = []
    flag = 0
    for dic in bio_result:
        for i in dic: 
            if i['entity'] == f'I-{skills}' and flag == 1 and i['word'][0:2]=='##':
                entity += i['word'].replace(" ##", "").replace("##", "").strip()
            elif  i['entity'] == f'I-{skills}' and flag == 1:
                entity += ' '+i['word'].replace(" ##", "").replace("##", "").strip()
            elif i["entity"] == f'B-{skills}':
                if entity != '':
                    entities.append(entity.title())
                entity = ''
                flag = 1
                entity = i['word'].replace(" ##", "").replace("##", "").strip()
            else:
                flag = 0
                if entity != '':
                    entities.append(entity.title())
                entity = ''

        if entity != '':
                    entities.append(entity.title())
    return entities


