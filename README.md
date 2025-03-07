# Amazon Product Intelligence

## Introduction

This project is designed to provide comprehensive analysis of customer reviews from Amazon product listings. Using Large Language Models (LLMs), the system extracts sentiment and actionable insights to facilitate data-driven product development and strategic decision-making.

The core objective is to move beyond basic review aggregation, delivering nuanced understanding of customer feedback. This is achieved through:

- _Sentiment Extraction_: Identifying and quantifying the emotional tone of customer reviews, encompassing positive, negative, and neutral sentiments, as well as specific emotional states (e.g., satisfaction, frustration).
- _Actionable Insight Generation_: Deriving practical, business-relevant insights from review content, including feature-specific feedback, trend identification, and potential product improvement recommendations.

## System Design

![System Design](images/AmazonProductIntelligence.drawio.png)

The system is comprised of 5 components:

1. **Review Analyzer**  
- This component is responsible for for processing raw review data.
- Implements the core data pipeline which consists of 3 stages:
  - Ingestion: Raw data is taken in and do minor cleanup of data.
  - Analysis: Each review is submitted to LLM for analysis and the result is stored in the database.
  - Finalization: Closes the run record.
- Implemented using `Celery` to enable asynchronous and parallel processing of large volume of reviews.
- Currently, the workers run inside the container. However, they should be able to run externally as separate containers or on other hosts, making this highly scaleable

1. **Review Analyzer**  
The Review Analyzer component serves as the core data processing engine for the Amazon Product Intelligence system. It orchestrates the ingestion, analysis, and finalization of raw review data, implementing a robust data pipeline.

- **Data Pipeline**:
  - _Ingestion_: This stage involves the acquisition of raw review data from the designated data source. Initial data cleansing operations are performed like basic format normalization and removal of extraneous characters.
  - _Analysis_: Each preprocessed review is submitted to the Large Language Model (LLM) for sentiment analysis and entity extraction. The resulting analysis data is then persisted to the system's database.
  - _Finalization_: Upon completion of the analysis run, this stage performs necessary post-processing tasks, such as updating run status records.
- **Asynchronous Processing**:
  - The component leverages `Celery`, a distributed task queue, to enable asynchronous and parallel processing of review data. This architecture facilitates efficient handling of large review volumes, significantly reducing processing latency.
- **Scalability**:
  - Currently, Celery workers are deployed within the same containerized environment as the Review Analyzer. To enhance scalability and resilience, future deployments may transition to a distributed worker architecture. At its current state, it is expected that minimal to no modification is required to do so. This will allow workers to operate as independent containers or on separate hosts, enabling horizontal scaling and improved resource utilization. This will enable the system to handle dramatically larger workloads.