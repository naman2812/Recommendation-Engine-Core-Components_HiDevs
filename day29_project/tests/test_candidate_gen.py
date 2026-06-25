import pytest
from candidate_gen import CandidateGenerator

@pytest.fixture
def sample_data():
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
    
    return CandidateGenerator(user_history, user_sims, item_sims, all_items)

class TestCandidateGenerator:
    def test_collaborative_candidates(self, sample_data):
        collab = sample_data.collaborative_candidates("user1")
        assert set(collab).issubset({"item4", "item5"})
        
    def test_collaborative_candidates_no_history(self, sample_data):
        assert sample_data.collaborative_candidates("unknown_user") == []
        
    def test_content_based_candidates(self, sample_data):
        content = sample_data.content_based_candidates("user1")
        assert set(content).issubset({"item7", "item8"})
        
    def test_popularity_candidates(self, sample_data):
        pop = sample_data.popularity_candidates(limit=2)
        assert pop == ["item1", "item3"] or pop == ["item1", "item2"] # Both appear in multiple histories or just item1 is top
        assert pop[0] == "item1" # item1 is definitely the most popular
        
    def test_hybrid_candidates_cold_start(self, sample_data):
        hybrid = sample_data.hybrid_candidates("user4")
        # Cold start user should get popularity recommendations
        assert len(hybrid) > 0
        assert "item1" in hybrid
