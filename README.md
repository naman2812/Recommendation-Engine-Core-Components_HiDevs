# Recommendation Engine Core Components

This project contains the core algorithmic components of a recommendation engine. These modules work together to calculate similarities, generate item candidates, score/rank them, and evaluate the quality of the recommendations.

## Project Structure

*   **`similarity.py`**: Contains the `SimilarityCalculator` module. Used to measure similarities between users, items, or skills using metrics like Cosine Similarity, Jaccard Index, and Pearson Correlation.
*   **`candidate_gen.py`**: Contains the `CandidateGenerator` module. Implements strategies to retrieve potential candidates, such as collaborative filtering, content-based filtering, popularity generation, and hybrid techniques.
*   **`scorer.py`**: Contains the `RecommendationScorer` module. Used to apply personalized and business-logic-based scoring algorithms to rank candidate items. Supports adding weighted scoring functions and provides explanations for recommendations.
*   **`evaluator.py`**: Contains the `RecommendationEvaluator` module. Calculates offline metrics like Precision@K, Recall@K, and NDCG@K to validate the accuracy of recommendations against a ground-truth dataset.
*   **`test.py`**: A test suite that runs simple test cases for each component, verifying that calculations, sorting, and edge cases are handled correctly.

## How They Fit Together

1.  The **Similarity Calculator** pre-computes similarities between users or items (e.g., finding out that User A and User B have a high Cosine Similarity).
2.  The **Candidate Generator** utilizes these similarities (along with popularity data and user history) to retrieve a pool of items that the user might be interested in.
3.  The **Scorer** takes the pool of candidate items and applies weighted scoring factors to compute a final list of top N recommendations with human-readable explanations.
4.  The **Evaluator** checks if the predicted top N items match what users actually ended up liking to measure the overall system performance.

## Usage

To run the sample tests and see the components in action:
```bash
python test.py

```

## Future Improvements

While this project builds the foundational algorithmic "engine," the following additions would help scale this into a complete, production-ready system:

*   **Database Integration**: Replace hardcoded Python dictionaries with a robust database (e.g., PostgreSQL for user/item metadata and Redis for fast similarity lookups).
*   **API Layer**: Wrap the components in a web framework like FastAPI or Flask to serve recommendations over HTTP to a front-end application.
*   **Advanced ML Models**: Integrate advanced machine learning techniques, such as Matrix Factorization (SVD) or Neural Collaborative Filtering, to discover deeper hidden patterns.
*   **Real-Time Processing**: Implement an event-streaming architecture (e.g., Apache Kafka) to update user histories and candidate scores instantaneously as users interact with items.
*   **Business Logic Filters**: Add hard constraint filters post-generation (e.g., hiding out-of-stock items, or applying age-rating filters).
*   **A/B Testing Framework**: Create an online routing system to test different scoring algorithms against each other in real-time to optimize for actual click-through r