def score_candidates(person_contexts, reviews, business_name):
    return [{"name": name, "score": len(contexts)} for name, contexts in sorted(person_contexts.items(), key=lambda x: -len(x[1]))]