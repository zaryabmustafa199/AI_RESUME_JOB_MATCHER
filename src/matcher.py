import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from .utils import load_sentence_transformer_model
import streamlit as st

# Load the Sentence Transformer model once
sentence_model = load_sentence_transformer_model('all-MiniLM-L6-v2')

def get_semantic_embedding(text):
    """
    Generates a semantic embedding vector for a given text.
    Uses the pre-loaded SentenceTransformer model.

    Args:
        text (str): The preprocessed text.

    Returns:
        numpy.ndarray: The embedding vector.
    """
    if not isinstance(text, str) or not text.strip():
        # Return a zero vector for empty/invalid text to avoid errors
        return np.zeros(sentence_model.get_sentence_embedding_dimension())
    return sentence_model.encode(text, convert_to_numpy=True)

def calculate_cosine_similarity(embedding1, embedding2):
    """
    Calculates the cosine similarity between two embedding vectors.

    Args:
        embedding1 (numpy.ndarray): First embedding vector.
        embedding2 (numpy.ndarray): Second embedding vector.

    Returns:
        float: Cosine similarity score between 0 and 1.
    """
    if embedding1.ndim == 1:
        embedding1 = embedding1.reshape(1, -1)
    if embedding2.ndim == 1:
        embedding2 = embedding2.reshape(1, -1)
    
    # Handle cases where one or both embeddings might be zero vectors
    if np.all(embedding1 == 0) or np.all(embedding2 == 0):
        return 0.0 # No similarity if one or both are empty/invalid

    return cosine_similarity(embedding1, embedding2)[0][0]

def calculate_skill_overlap_score(resume_skills, job_skills):
    """
    Calculates a score based on the overlap of skills.
    Uses Jaccard Index for unique skills.

    Args:
        resume_skills (list): List of skills extracted from resume.
        job_skills (list): List of skills extracted from job description.

    Returns:
        float: Skill overlap score between 0 and 1.
    """
    if not resume_skills or not job_skills:
        return 0.0

    set_resume_skills = set(s.lower() for s in resume_skills)
    set_job_skills = set(s.lower() for s in job_skills)

    intersection = len(set_resume_skills.intersection(set_job_skills))
    union = len(set_resume_skills.union(set_job_skills))

    if union == 0:
        return 0.0
    return intersection / union

def calculate_experience_overlap_score(resume_experience_text, job_description_text):
    """
    A simple approach to estimate experience overlap based on presence of keywords.
    This is highly simplified and can be improved with more sophisticated NER for years/months.

    Args:
        resume_experience_text (str): Preprocessed text from resume potentially containing experience.
        job_description_text (str): Preprocessed text from job description potentially containing experience.

    Returns:
        float: A score between 0 and 1.
    """
    score = 0.0
    # Basic check for common experience indicators. Can be expanded.
    exp_indicators = ['year', 'experience', 'senior', 'lead', 'junior', 'entry']
    
    resume_has_exp = any(ind in resume_experience_text for ind in exp_indicators)
    job_has_exp = any(ind in job_description_text for ind in exp_indicators)
    
    if resume_has_exp and job_has_exp:
        score = 0.5 # Both mention experience, gives a base score
        # Further logic could be implemented here to parse actual years (e.g., regex)
        # For a full-fledged solution, you'd want to extract 'years of experience' as a number.
        
    return score

def get_matching_score(resume_text_processed, job_desc_text_processed,
                       resume_entities, job_entities):
    """
    Calculates a combined matching score.

    Args:
        resume_text_processed (str): Preprocessed resume text.
        job_desc_text_processed (str): Preprocessed job description text.
        resume_entities (dict): Entities extracted from resume.
        job_entities (dict): Entities extracted from job description.

    Returns:
        dict: A dictionary containing overall score and breakdown.
    """
    scores = {
        'semantic_similarity': 0.0,
        'skill_overlap': 0.0,
        'qualification_overlap': 0.0,
        'experience_alignment': 0.0 # Placeholder, more robust implementation needed
    }

    # 1. Semantic Similarity
    resume_embedding = get_semantic_embedding(resume_text_processed)
    job_embedding = get_semantic_embedding(job_desc_text_processed)
    scores['semantic_similarity'] = calculate_cosine_similarity(resume_embedding, job_embedding)

    # 2. Skill Overlap
    resume_skills = resume_entities.get('SKILLS', [])
    job_skills = job_entities.get('SKILLS', [])
    scores['skill_overlap'] = calculate_skill_overlap_score(resume_skills, job_skills)

    # 3. Qualification Overlap
    resume_qualifications = resume_entities.get('QUALIFICATION', [])
    job_qualifications = job_entities.get('QUALIFICATION', []) # Job descriptions might not have explicit QUALIFICATION, but you can infer from text
    # Simple check for common qualifications (e.g., 'bachelor', 'master', 'phd')
    qual_score = 0.0
    for qual_res in resume_qualifications:
        for qual_job in job_qualifications: # This needs a smarter comparison, perhaps using semantic similarity for these too
            if qual_res in qual_job or qual_job in qual_res:
                qual_score = 1.0 # A simple boolean match for now
                break
        if qual_score == 1.0:
            break
    scores['qualification_overlap'] = qual_score # This needs significant improvement for real-world use

    # 4. Experience Alignment (needs better implementation)
    # This is a very rough estimate. A better approach would involve parsing actual years of experience.
    scores['experience_alignment'] = calculate_experience_overlap_score(
        resume_text_processed, job_desc_text_processed
    )


    # Combine scores with weights
    # These weights are arbitrary and should be tuned based on desired outcome and data
    weights = {
        'semantic_similarity': 0.4,
        'skill_overlap': 0.4,
        'qualification_overlap': 0.1,
        'experience_alignment': 0.1
    }

    overall_score = (
        scores['semantic_similarity'] * weights['semantic_similarity'] +
        scores['skill_overlap'] * weights['skill_overlap'] +
        scores['qualification_overlap'] * weights['qualification_overlap'] +
        scores['experience_alignment'] * weights['experience_alignment']
    )

    return {
        'overall_score': round(overall_score * 100, 2), # Percentage score
        'breakdown': {k: round(v, 3) for k, v in scores.items()}
    }