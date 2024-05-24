# Load model directly
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
from resume.preprocessing import split_into_sentences,extract_entities,cleaning
from sentence_transformers import SentenceTransformer
import spacy ,numpy as np , pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from resume.models import seekr
# tokenizer = AutoTokenizer.from_pretrained("GalalEwida/LLM-BERT-Model-Based-Skills-Extraction-from-jobdescription")
# model = AutoModelForTokenClassification.from_pretrained("GalalEwida/LLM-BERT-Model-Based-Skills-Extraction-from-jobdescription")
# model.save_pretrained("ner_model")
# tokenizer.save_pretrained("tokenizer")
new_model = r'Models\NER_BERT\ner_model'
new_tokenizer = r'Models\NER_BERT\tokenizer'
nlp = pipeline("ner", model=new_model, tokenizer=new_tokenizer)
embedding_model = SentenceTransformer('Models\embedding')
spacy_model = spacy.load(r"Models\Spacy_CV\model-last")
title_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
tech_df = pd.read_csv(r"Models/techh.csv")

def preprocessing_pipeline(text,max_token=150,types =['TECHNOLOGY','TECHNICAL'] ):
    preprcessed_text = cleaning(text)
    list_preprocessed = split_into_sentences(preprcessed_text)
    out_model = nlp(list_preprocessed)
    skills_out1 = extract_entities(out_model,skills=types[0])
    skills_out2 = extract_entities(out_model,skills=types[1])
    return list(set(skills_out1+skills_out2))

def normalize_jobtitle(title,df =tech_df ):
    target_term = title
    job_titles = df["job titles"]
    target_embedding = title_model.encode([target_term])
    job_title_embeddings = title_model.encode(job_titles)
    similarities = cosine_similarity(target_embedding, job_title_embeddings)[0]
    max_index = similarities.argmax()
    job_title = job_titles[max_index]
    return job_title 

def similarty(skills):
    # data = pd.read_csv('cvs\cv_embedding.csv')
    seekr_objects = seekr.query.all()
    cv_names = [Seekr.cv_name for Seekr in seekr_objects]
    embeddings = [Seekr.embedding for Seekr in seekr_objects]
    data = pd.DataFrame({'cv_name': cv_names, 'embedding': embeddings})
    data.dropna(inplace=True)
    data.reset_index(inplace=True,drop=True)
    new_skills = ', '.join(skills)
    # Embedding the new skills
    skills_embeddings = embedding_model.encode(new_skills).reshape(1, -1)
    data['new_skills_embeddings'] = data['embedding'].apply(lambda x: np.fromstring(x[2:-2], dtype=np.float32, sep=' '))
    similarity_scores = cosine_similarity(np.vstack(data['new_skills_embeddings']), skills_embeddings)    
    top_indices = np.argsort(similarity_scores, axis=0)[-5:][::-1].flatten()
    top_job_titles = []
    for index in top_indices:
        job_title = data['cv_name'][index]
        similarity_score = similarity_scores[index][0]  # Extract similarity score from 2D array
        # top_job_titles.append((job_title, similarity_score))                              --> for the similarity score not percentage

        # Normalize similarity score to a percentage
        similarity_percentage = (similarity_score + 1) * 50  # Normalize to 0-100 scale    
        top_job_titles.append((job_title, similarity_percentage))
    output = [(first,round(second,2)) for first, second in top_job_titles]
    return output

