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
Redis serves as the message queue/broker for `Celery`, enabling efficient and reliable communication and coordination between Celery worker processes. Specifically:

- **Task Distribution and Coordination**:
Redis facilitates the distribution of tasks from the Review Analyzer to available Celery workers.
It enables workers to coordinate their activities, ensuring that tasks are processed in the correct order and preventing conflicts.
- **Asynchronous Result Transfer**:
Redis enables the asynchronous transfer of task results from worker processes to the requesting process or designated storage.
This decoupling of task execution and result retrieval improves the responsiveness of the overall system.

**5. Large Language Model (LLM) Integration (OpenAI/ChatGPT)**  
This forms the core analytical engine for this project. Its integration enables sophisticated natural language processing for accurate sentiment analysis and insightful data extraction.

- **Advanced Review Analysis**:
The LLM performs in-depth analysis of customer reviews, going beyond simple keyword matching to understand the nuanced meaning and context of the text.
It accurately determines customer sentiment, identifying positive, negative, and neutral tones, as well as specific emotional expressions.
- **Insight Generation**:
The LLM extracts relevant insights from review data, including:
Identification of key product features and attributes mentioned by customers.
Detection of recurring themes and patterns in customer feedback.
Generation of summaries and actionable recommendations based on the analysis.

## Key Decisions and Trade-Offs

1. Employing `Celery` is one of the key decisions in this project. Unlike the default concurrency mechanism of `asyncio` which is to multithread, it allowed horizontal scalability out-of-the-box. In this implementation, the workers are all in the same container, but even without changing the code, the workers can be readily migrated to other hosts. This is particularly beneficial in a clustered environment (e.g., k8s clusters). The trade-off is the additional overhead (e.g., the need for message queue/broker), but it's easily out-weighed by benefits.  Please note, though, that over scaling is also a problem since services like OpenAI's have rate-limiter that could be easily hit with just a handful of workers.

2. The use of Postgres is also another key decision. Postgres is durable and known to degrade gracefully. Processing customer reviews will potentially entail managing huge volume of data. With PG, the limit is farther than the alternative. I also particularly like the advance data types it provides (e.g., JSONB). With these, PG can be used like NoSQL databases (which is beneficial in some use cases).

3. The system's current batch processing of reviews, rather than real-time analysis, presents a potential limitation. However, this approach is often forced-upon by several factors: firstly, the latency involved in retrieving data from external sources; and secondly, the constraints imposed by Large Language Model (LLM) providers, including cost considerations and rate-limiting. Consequently, while real-time processing might be conceptually desirable, practical implementation is often infeasible due to these inherent constraints.

## Future Improvements

1. GraphQL is, in my opinion, is etter the better approach in this use case since the data composition/schema usually varies. With ReSTFUL approach, the number of end-points could grow to unmanageable levels.

2. Investigate the cost benefits of deploying own LLM. Just like other managed services, which usually cost more than managing own resources, OpenAI _may_ be costing more than just hosting/deploying own LLM.