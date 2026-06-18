class RecommendationScorer:
    def __init__(self):
        """
        Initialize the scorer with an empty list of scoring components.
        """
        self.scorers = []

    def add_scorer(self, name, function, weight):
        """
        Register a scoring function with a specific weight.
        - function: Must take (user_id, item_id, context) and return a float [0.0, 1.0]
        - weight: The importance multiplier for this score
        """
        self.scorers.append({
            "name": name,
            "function": function,
            "weight": weight
        })

    def calculate_score(self, user_id, item_id, context=None):
        """
        Calculates the combined score for a single item by aggregating all registered scorers.
        Also returns a brief human-readable explanation of why it scored well.
        """
        if not self.scorers:
            return 0.0, "No scorers registered"
            
        total_score = 0.0
        total_weight = 0.0
        explanations = []
        
        for scorer in self.scorers:
            try:
                score = scorer["function"](user_id, item_id, context)
            except Exception:
                score = 0.0 # Fail gracefully if scorer has an issue
                
            weight = scorer["weight"]
            
            total_score += score * weight
            total_weight += weight
            
            if score >= 0.5: # Include in explanation if it was a strong signal
                explanations.append(f"high {scorer['name']}")
                
        final_score = total_score / total_weight if total_weight > 0 else 0.0
        
        if explanations:
            explanation = "Recommended due to: " + ", ".join(explanations)
        else:
            explanation = "General recommendation"
            
        return final_score, explanation

    def rank_candidates(self, user_id, candidates, limit=10, context=None):
        """
        Scores a list of candidates and returns the top `limit` results.
        """
        if not candidates:
            return []
            
        scored_candidates = []
        for item_id in candidates:
            score, explanation = self.calculate_score(user_id, item_id, context)
            scored_candidates.append({
                "item_id": item_id,
                "score": score,
                "explanation": explanation
            })
            
        # Sort descending by score
        scored_candidates.sort(key=lambda x: x["score"], reverse=True)
        return scored_candidates[:limit]
