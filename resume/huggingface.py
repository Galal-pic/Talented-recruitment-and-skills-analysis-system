# Load model directly
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
from resume.preprocessing import split_into_sentences,extract_entities,cleaning
import spacy ,numpy as np , pandas as pd
from resume.models import seekr
from langchain.embeddings import HuggingFaceEmbeddings
import tensorflow as tf

# tokenizer = AutoTokenizer.from_pretrained("GalalEwida/LLM-BERT-Model-Based-Skills-Extraction-from-jobdescription")
# model = AutoModelForTokenClassification.from_pretrained("GalalEwida/LLM-BERT-Model-Based-Skills-Extraction-from-jobdescription")
# model.save_pretrained("ner_model")
# tokenizer.save_pretrained("tokenizer")
new_model = r'Models\NER_BERT\ner_model'
new_tokenizer = r'Models\NER_BERT\tokenizer'
nlp = pipeline("ner", model=new_model, tokenizer=new_tokenizer)
embedding_model = HuggingFaceEmbeddings(model_name="paraphrase-MiniLM-L6-v2")
spacy_model = spacy.load(r"Models\Spacy_CV\model-last")

def preprocessing_pipeline(text,max_token=150,types =['TECHNOLOGY','TECHNICAL'] ):
    preprcessed_text = cleaning(text)
    list_preprocessed = split_into_sentences(preprcessed_text)
    out_model = nlp(list_preprocessed)
    skills_out1 = extract_entities(out_model,skills=types[0])
    skills_out2 = extract_entities(out_model,skills=types[1])
    return list(set(skills_out1+skills_out2))


def similarty(skills):
    seekr_objects = seekr.query.all()
    cv_names = [Seekr.cv_name for Seekr in seekr_objects]
    embeddings = [Seekr.embedding for Seekr in seekr_objects]
    data = pd.DataFrame({'cv_name': cv_names, 'embedding': embeddings})
    data.dropna(inplace=True)
    data.reset_index(inplace=True,drop=True)
    new_skills = ', '.join(skills)
    # Embedding the new skills

    skills_emb = embedding_model.embed_query(str(skills))
    skills_embeddings = tf.constant([skills_emb])
    data['new_skills_embeddings'] = data['embedding'].apply(lambda x: np.fromstring(x[1:-1], dtype=np.float32, sep=','))
    cosine_loss = tf.keras.losses.CosineSimilarity(axis=-1)
    data['similarity_score'] = data['new_skills_embeddings'].apply(lambda job_skill_tensor: (cosine_loss(job_skill_tensor, skills_embeddings).numpy() * -1))
    top_matches = data.nlargest(10, 'similarity_score')
    output = [(row['cv_name'], row['similarity_score']) for _, row in top_matches.iterrows()]
    output = [(first,round(second,2)) for first, second in output]
    return output

