from similarity import SimilarityCalculator
from candidate_gen import CandidateGenerator
from scorer import RecommendationScorer
from evaluator import RecommendationEvaluator

def test_similarity():
    print("--- Testing Similarity Calculator ---")
    calc = SimilarityCalculator()
    
    # 1. Cosine Similarity
    v1 = {"item1": 5, "item2": 3}
    v2 = {"item1": 4, "item2": 2}
    v3 = {"item3": 5} # Completely disjoint
    print(f"Cosine sim (v1, v2): {calc.cosine_similarity(v1, v2):.4f}")
    print(f"Cosine sim (v1, v3): {calc.cosine_similarity(v1, v3):.4f}")
    
    # 2. Jaccard Similarity
    s1 = {"python", "java", "c++"}
    s2 = {"python", "javascript", "ruby"}
    print(f"Jaccard sim (s1, s2): {calc.jaccard_similarity(s1, s2):.4f}")
    
    # 3. Pearson Correlation
    r1 = {"item1": 5, "item2": 3, "item3": 2}
    r2 = {"item1": 4, "item2": 2, "item3": 1}
    r3 = {"item1": 1, "item2": 3, "item3": 5} # Negative correlation
    print(f"Pearson (r1, r2): {calc.pearson_correlation(r1, r2):.4f}")
    print(f"Pearson (r1, r3): {calc.pearson_correlation(r1, r3):.4f}")
    print()

def test_candidate_generator():
    print("--- Testing Candidate Generator ---")
    user_history = {
        "user1": {"item1", "item2", "item3"},
        "user2": {"item1", "item4", "item5"},
        "user3": {"item6"}
    }
    user_sims = {
        "user1": [("user2", 0.8)]
    }
    item_sims = {
        "item1": [("item7", 0.9)],
        "item2": [("item8", 0.8)]
    }
    all_items = {"item1", "item2", "item3", "item4", "item5", "item6", "item7", "item8"}
    
    gen = CandidateGenerator(user_history, user_sims, item_sims, all_items)
    
    collab = gen.collaborative_candidates("user1")
    print(f"Collab candidates for user1: {collab}")
    
    content = gen.content_based_candidates("user1")
    print(f"Content candidates for user1: {content}")
    
    pop = gen.popularity_candidates(limit=2)
    print(f"Popularity candidates: {pop}")
    
    hybrid = gen.hybrid_candidates("user4") # Completely cold start
    print(f"Hybrid candidates for cold start user4: {hybrid}")
    print()

def test_scorer():
    print("--- Testing Scorer ---")
    scorer = RecommendationScorer()
    
    # Example scoring functions that mimic business logic
    def relevance_score(u, i, ctx): 
        return 0.9 if i == "item1" else 0.4
        
    def popularity_score(u, i, ctx): 
        return 0.8 if i in ["item1", "item2"] else 0.2
    
    scorer.add_scorer("Relevance", relevance_score, weight=0.7)
    scorer.add_scorer("Popularity", popularity_score, weight=0.3)
    
    candidates = ["item1", "item2", "item3"]
    ranked = scorer.rank_candidates("user1", candidates)
    
    print("Ranked Candidates:")
    for r in ranked:
        print(f" - Item: {r['item_id']}, Final Score: {r['score']:.4f}, Reason: {r['explanation']}")
    print()

def test_evaluator():
    print("--- Testing Evaluator ---")
    evaluator = RecommendationEvaluator()
    
    recommendations = {
        "user1": ["item1", "item2", "item3", "item4"],
        "user2": ["item5", "item6", "item7"]
    }
    ground_truth = {
        "user1": ["item1", "item3", "item8"], # user1 hit at rank 1 and 3
        "user2": ["item9"]                    # user2 missed completely
    }
    
    metrics = evaluator.evaluate_all(recommendations, ground_truth, k=3)
    print("Evaluation Metrics (k=3):")
    for m, v in metrics.items():
        print(f" - {m}: {v:.4f}")
    print()

if __name__ == "__main__":
    test_similarity()
    test_candidate_generator()
    test_scorer()
    test_evaluator()
    print("All tests completed successfully!")
