import requests
import json

# Configuration
BASE_URL = "http://localhost:8000/api"
ROADMAP_URL = f"{BASE_URL}/roadmap/"
LEARNING_URL = f"{BASE_URL}/learning/"

# 1. 17 Core Skills for Roadmap
roadmap_skills = [
    {"skill_name": "SQL (Joins, Window Functions, Optimization)", "category": "Data Engineering", "difficulty": "Medium", "importance": "High"},
    {"skill_name": "Python (Pandas, API, Automation)", "category": "Data Engineering", "difficulty": "Medium", "importance": "High"},
    {"skill_name": "Data Formats (CSV, JSON, Parquet, Columnar)", "category": "Data Engineering", "difficulty": "Easy", "importance": "Medium"},
    {"skill_name": "ETL / ELT Pipelines", "category": "Data Engineering", "difficulty": "Hard", "importance": "High"},
    {"skill_name": "Data Ingestion & Incremental Loading", "category": "Data Engineering", "difficulty": "Medium", "importance": "High"},
    {"skill_name": "Data Transformation Pipelines", "category": "Data Engineering", "difficulty": "Medium", "importance": "High"},
    {"skill_name": "Apache Airflow (DAGs, Scheduling)", "category": "Data Engineering", "difficulty": "Hard", "importance": "High"},
    {"skill_name": "Data Warehousing (Star Schema, OLAP)", "category": "Data Engineering", "difficulty": "Medium", "importance": "High"},
    {"skill_name": "dbt (Transformation & Testing)", "category": "Data Engineering", "difficulty": "Medium", "importance": "Medium"},
    {"skill_name": "Apache Spark / PySpark", "category": "Data Engineering", "difficulty": "Hard", "importance": "High"},
    {"skill_name": "AWS Cloud (S3, Redshift, Glue, Lambda)", "category": "Data Engineering", "difficulty": "Medium", "importance": "High"},
    {"skill_name": "Docker (Containerization)", "category": "Data Engineering", "difficulty": "Medium", "importance": "Medium"},
    {"skill_name": "Git & GitHub (Version Control)", "category": "Data Engineering", "difficulty": "Easy", "importance": "High"},
    {"skill_name": "Linux Basics (Terminal, File Mgmt)", "category": "Data Engineering", "difficulty": "Easy", "importance": "Medium"},
    {"skill_name": "CI/CD Basics (GitHub Actions)", "category": "Data Engineering", "difficulty": "Medium", "importance": "Medium"},
    {"skill_name": "Kubernetes Basics", "category": "Data Engineering", "difficulty": "Hard", "importance": "Medium"},
    {"skill_name": "Data Engineering Architecture (Lakes, Modern Stack)", "category": "Data Engineering", "difficulty": "Hard", "importance": "High"}
]

# 2. Detailed Syllabi for Learning Topics
learning_topics = [
    {
        "topic": "Data Formats and Storage",
        "category": "Data Engineering",
        "syllabus": {
            "goal": "Understand how different data formats are stored and used efficiently in data pipelines.",
            "sections": [
                {"title": "Data Storage Fundamentals", "items": ["Structured vs semi-structured", "Row-based vs column-based", "Storage efficiency", "Query performance"]},
                {"title": "CSV (Comma-Separated Values)", "items": ["File structure", "Delimiters", "Encoding", "Reading/Writing large files"]},
                {"title": "JSON (JavaScript Object Notation)", "items": ["Nested objects", "Arrays", "Parsing & Flattening", "API use cases"]},
                {"title": "Parquet (Columnar Storage)", "items": ["Compression mechanisms", "Schema support", "Data lakes usage", "Fast analytical queries"]},
                {"title": "Choosing the Right Format", "items": ["CSV for small datasets", "JSON for semi-structured", "Parquet for analytics"]}
            ]
        }
    },
    {
        "topic": "Data Engineering Understanding",
        "category": "Data Engineering",
        "syllabus": {
            "goal": "Understand how complete data systems are designed and how data flows from source to analytics.",
            "sections": [
                {"title": "Data Architecture Fundamentals", "items": ["Components of a data platform", "End-to-end data flow", "Data lifecycle"]},
                {"title": "Data Lakes vs Data Warehouses", "items": ["S3/GCS Object storage", "Snowflake/BigQuery/Redshift", "Schema-on-read vs Schema-on-write"]},
                {"title": "Modern Data Stack", "items": ["Ingestion (APIs)", "Storage (Cloud Lake)", "Transformation (dbt)", "Orchestration (Airflow)"]},
                {"title": "Batch vs Streaming Pipelines", "items": ["Scheduled vs Continuous", "Kafka/Spark Streaming", "Latency trade-offs"]},
                {"title": "Pipeline Reliability", "items": ["Retry mechanisms", "Monitoring", "Error handling", "Validation"]}
            ]
        }
    },
    {
        "topic": "ETL / ELT Pipeline Development",
        "category": "Data Engineering",
        "syllabus": {
            "goal": "Design and build automated data pipelines that extract, transform, and load data reliably.",
            "sections": [
                {"title": "ETL vs ELT", "items": ["Transformation before loading vs inside warehouse", "Modern cloud architectures"]},
                {"title": "Incision Patterns", "items": ["API extraction", "Database SQL extraction", "Incremental queries"]},
                {"title": "Incremental Data Loading", "items": ["Timestamp based loading", "Change tracking", "Upserts"]},
                {"title": "Data Transformation Pipelines", "items": ["Data cleaning", "Normalization", "Aggregation", "Enrichment"]},
                {"title": "Pipeline Automation & Orchestration", "items": ["Scheduled jobs", "Dependency management", "Failure recovery (Airflow)"]}
            ]
        }
    },
    {
        "topic": "Data Warehousing",
        "category": "Data Engineering",
        "syllabus": {
            "goal": "Design, store, and query structured analytical data efficiently.",
            "sections": [
                {"title": "OLTP vs OLAP", "items": ["Transactional vs Analytical", "Normalized vs Denormalized"]},
                {"title": "Dimensional Data Modeling", "items": ["Fact tables", "Dimension tables", "Star Schema", "Snowflake Schema"]},
                {"title": "Performance Optimization", "items": ["Partitioning", "Clustering", "Query tuning"]},
                {"title": "Modern Cloud Warehouses", "items": ["BigQuery serverless", "Snowflake compute/storage separation"]}
            ]
        }
    },
    {
        "topic": "Python for Data Engineering",
        "category": "Data Engineering",
        "syllabus": {
            "goal": "Automate data tasks such as ingestion, processing, and file management.",
            "sections": [
                {"title": "Foundations", "items": ["Virtual environments", "Environment variables", "Modular scripts"]},
                {"title": "Data Processing with Pandas", "items": ["DataFrames", "Cleaning", "Aggregations", "Joins"]},
                {"title": "API & File Automation", "items": ["Requests library", "File system (pathlib/shutil)", "JSON/CSV/Parquet handling"]},
                {"title": "Orchestration & Error Handling", "items": ["Logging", "Exception handling (try/except)", "Retries"]}
            ]
        }
    }
]

def inject():
    print("--- Injecting Roadmap Skills ---")
    for skill in roadmap_skills:
        try:
            r = requests.post(ROADMAP_URL, json=skill)
            if r.status_code == 200:
                print(f"[OK] Roadmap: {skill['skill_name']}")
            else:
                print(f"[ERR] Roadmap: {skill['skill_name']} - {r.text}")
        except Exception as e:
            print(f"[FAIL] {skill['skill_name']}: {e}")

    print("\n--- Injecting Learning Topics with Syllabi ---")
    for topic in learning_topics:
        try:
            r = requests.post(LEARNING_URL, json=topic)
            if r.status_code == 200:
                print(f"[OK] Topic: {topic['topic']}")
            else:
                print(f"[ERR] Topic: {topic['topic']} - {r.text}")
        except Exception as e:
            print(f"[FAIL] {topic['topic']}: {e}")

if __name__ == "__main__":
    inject()
