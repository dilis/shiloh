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
The Review Analyzer component serves as the core data processing engine for the Amazon Product Intelligence system. It orchestrates the ingestion, analysis, and finalization of raw review data, implementing a robust data pipeline.

- **Data Pipeline**:
  - _Ingestion_: This stage involves the acquisition of raw review data from the designated data source. Initial data cleansing operations are performed like basic format normalization and removal of extraneous characters.
  - _Analysis_: Each preprocessed review is submitted to the Large Language Model (LLM) for sentiment analysis and entity extraction. The resulting analysis data is then persisted to the system's database.
  - _Finalization_: Upon completion of the analysis run, this stage performs necessary post-processing tasks, such as updating run status records.
- **Asynchronous Processing**:
  - The component leverages `Celery`, a distributed task queue, to enable asynchronous and parallel processing of review data. This architecture facilitates efficient handling of large review volumes, significantly reducing processing latency.
- **Scalability**:
  - Currently, Celery workers are deployed within the same containerized environment as the Review Analyzer. To enhance scalability and resilience, future deployments may transition to a distributed worker architecture. At its current state, it is expected that minimal to no modification is required to do so. This will allow workers to operate as independent containers or on separate hosts, enabling horizontal scaling and improved resource utilization. This will enable the system to handle dramatically larger workloads.

2. **API Layer**
The API Layer provides ReSTFUL endpoints to fetch a single product insight or a list of products.
- Implemented with `FastAPI`
  - Automatic documentation
  - Asynchronous operation
  - Nice developer experience
- ORM is provided by `SQLModel`/`SQLAlchemy` tandem

3. **Database (Postgres)**
This provides data persistence

4. **Message Queue/Broker for Celery (Redis)**
This allows Celery workers to communicate and coordinate each other. It also facilitates the transfer of results to requesting process.

Let's refine that to be more informative and technically accurate:

4. **Message Queue/Broker for Celery (Redis)**
Redis serves as the message queue/broker for `Celery`, enabling efficient and reliable communication and coordination between Celery worker processes. Specifically:

- **Task Distribution and Coordination**:
Redis facilitates the distribution of tasks from the Review Analyzer to available Celery workers.
It enables workers to coordinate their activities, ensuring that tasks are processed in the correct order and preventing conflicts.
- **Asynchronous Result Transfer**:
Redis enables the asynchronous transfer of task results from worker processes to the requesting process or designated storage.
This decoupling of task execution and result retrieval improves the responsiveness of the overall system.