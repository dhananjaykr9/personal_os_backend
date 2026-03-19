import requests
import json

# Configuration
BASE_URL = "http://localhost:8000/api"
ROADMAP_URL = f"{BASE_URL}/roadmap/"
LEARNING_URL = f"{BASE_URL}/learning/"

# 1. 17 Core Skills for Roadmap (1:1 with user's 1-17 list)
roadmap_skills = [
    {"skill_name": "SQL (Joins, Window Functions, Aggregations, Optimization)", "category": "Data Engineering", "difficulty": "Medium", "importance": "High"},
    {"skill_name": "Python (Pandas, API, Automation)", "category": "Data Engineering", "difficulty": "Medium", "importance": "High"},
    {"skill_name": "Data Formats (CSV, JSON, Parquet, Columnar)", "category": "Data Engineering", "difficulty": "Easy", "importance": "Medium"},
    {"skill_name": "ETL / ELT Pipelines", "category": "Data Engineering", "difficulty": "Hard", "importance": "High"},
    {"skill_name": "Data Ingestion & Incremental Loading", "category": "Data Engineering", "difficulty": "Medium", "importance": "High"},
    {"skill_name": "Data Transformation Pipelines", "category": "Data Engineering", "difficulty": "Medium", "importance": "High"},
    {"skill_name": "Apache Airflow (DAGs, Scheduling, Retries, Monitoring)", "category": "Data Engineering", "difficulty": "Hard", "importance": "High"},
    {"skill_name": "Data Warehousing (OLTP vs OLAP, Star Schema, Fact/Dimensions)", "category": "Data Engineering", "difficulty": "Medium", "importance": "High"},
    {"skill_name": "dbt (Transformation, Testing, Documentation)", "category": "Data Engineering", "difficulty": "Medium", "importance": "Medium"},
    {"skill_name": "Apache Spark / PySpark (DataFrames, transformations, joins, partitioning)", "category": "Data Engineering", "difficulty": "Hard", "importance": "High"},
    {"skill_name": "AWS Cloud (S3, Redshift, Glue, Lambda basics)", "category": "Data Engineering", "difficulty": "Medium", "importance": "High"},
    {"skill_name": "Docker (containerization, Dockerfile, Docker Compose)", "category": "Data Engineering", "difficulty": "Medium", "importance": "Medium"},
    {"skill_name": "Git & GitHub (repositories, branching, pull requests, collaboration)", "category": "Data Engineering", "difficulty": "Easy", "importance": "High"},
    {"skill_name": "Linux Basics (terminal commands, file management)", "category": "Data Engineering", "difficulty": "Easy", "importance": "Medium"},
    {"skill_name": "CI/CD Basics (GitHub Actions, pipeline automation)", "category": "Data Engineering", "difficulty": "Medium", "importance": "Medium"},
    {"skill_name": "Kubernetes Basics (container orchestration concepts)", "category": "Data Engineering", "difficulty": "Hard", "importance": "Medium"},
    {"skill_name": "Data Engineering Architecture (data lakes, warehouses, modern data stack)", "category": "Data Engineering", "difficulty": "Hard", "importance": "High"}
]

# 2. 17 Detailed Learning Topics
learning_topics = [
    {
        "topic": "Data Formats and Storage",
        "category": "Data Engineering",
        "syllabus": {
            "goal": "Understand how different data formats are stored and used efficiently in data pipelines.",
            "sections": [
                {"title": "Data Storage Fundamentals", "items": ["Why data formats matter", "Structured vs semi-structured data", "Row-based vs column-based storage", "Trade-offs between storage formats", "storage efficiency", "query performance", "compression", "schema structure"]},
                {"title": "CSV (Comma-Separated Values)", "items": ["Overview: Simple text-based tabular data format", "CSV file structure", "delimiters", "headers", "encoding formats", "reading/writing CSV files", "handling large CSV files", "dealing with missing values", "Advantages: easy to create, human readable, widely supported", "Limitations: large file sizes, slower processing, no schema enforcement"]},
                {"title": "JSON (JavaScript Object Notation)", "items": ["Common format for semi-structured data", "JSON structure", "nested objects", "arrays", "key-value representation", "reading JSON data", "parsing nested JSON", "flattening JSON structures", "Use cases: API responses, event logs, configuration data", "Limitations: larger storage size, slower analytical queries"]},
                {"title": "Parquet (Columnar Storage Format)", "items": ["Optimized storage format used in modern data pipelines", "columnar storage structure", "compression mechanisms", "efficient column reading", "schema support", "reading Parquet files", "writing Parquet datasets", "partitioned Parquet storage", "Advantages: high compression, fast analytical queries, efficient column selection", "Common usage: data lakes, big data processing, data warehouse storage"]},
                {"title": "Columnar Storage Basics", "items": ["Data stored by columns instead of rows", "Row-based storage: sequential rows", "Column-based storage: columns stored together", "Benefits: faster analytical queries, reduced disk I/O, better compression"]},
                {"title": "Choosing the Right Format", "items": ["CSV: small datasets, simple data exchange", "JSON: semi-structured data, API responses, event logs", "Parquet: large datasets, data lakes, analytics systems"]}
            ]
        }
    },
    {
        "topic": "Data Engineering Architecture",
        "category": "Data Engineering",
        "syllabus": {
            "goal": "Understand how complete data systems are designed and how data flows from source to analytics.",
            "sections": [
                {"title": "Data Architecture Fundamentals", "items": ["What is data architecture", "Components of a data platform", "End-to-end data flow in organizations", "Data lifecycle", "Typical pipeline flow: Source -> Ingestion -> Processing -> Storage -> Analytics", "Concepts: scalability, reliability, maintainability"]},
                {"title": "Data Lakes", "items": ["Large storage for raw data in original format", "object storage (S3, GCS)", "schema-on-read concept", "storing logs, raw API data, event data, raw files", "Advantages: flexible storage, scalable, supports multiple formats"]},
                {"title": "Data Warehouses", "items": ["Systems optimized for analytical queries and reporting", "structured analytical storage", "optimized query engines", "Snowflake, BigQuery, Redshift", "Characteristics: columnar storage, aggregation-heavy queries, structured schema"]},
                {"title": "Data Lake vs Data Warehouse", "items": ["Data lake: raw data, flexible schema, multiple formats", "Data warehouse: structured analytical data, reporting queries", "Typical architecture: Raw data -> Data lake -> Transformations -> Data warehouse"]},
                {"title": "Modern Data Stack", "items": ["Ingestion: APIs, batch ingestion", "Storage: cloud data lakes", "Transformation: dbt, SQL transformations", "Processing: Spark", "Warehouse: Snowflake, BigQuery, Redshift", "Orchestration: Airflow"]},
                {"title": "Batch vs Streaming Pipelines", "items": ["Batch: scheduled intervals, large volumes, predictable workloads", "Streaming: real-time event tracking, live analytics, low latency (Kafka, Spark Streaming, Flink)", "Outcome: Understanding which architecture fits different use cases"]},
                {"title": "Pipeline Reliability", "items": ["retry mechanisms", "monitoring pipeline runs", "error handling", "data validation", "logging pipeline steps", "alerting on failures"]}
            ]
        }
    },
    {
        "topic": "ETL / ELT Pipeline Development",
        "category": "Data Engineering",
        "syllabus": {
            "goal": "Design and build automated data pipelines that extract, transform, and load data reliably.",
            "sections": [
                {"title": "ETL vs ELT", "items": ["ETL: Extract -> Transform -> Load (transform before loading)", "ELT: Extract -> Load -> Transform (load raw first, transform inside warehouse)", "Modern cloud warehouses use ELT for large datasets"]},
                {"title": "Data Sources and Ingestion", "items": ["APIs (pagination, auth)", "Databases (SQL extraction, incremental queries)", "Files (reading CSV, JSON, Parquet)"]},
                {"title": "Batch Data Pipelines", "items": ["Scheduled pipeline execution (daily/hourly)", "Processing data in batches", "batch scheduling", "pipeline dependencies", "retry mechanisms"]},
                {"title": "Incremental Data Loading", "items": ["Loading only new/updated data", "timestamp based loading", "change tracking", "watermark techniques", "upserts"]},
                {"title": "Data Transformation Pipelines", "items": ["Data cleaning (duplicates, missing values)", "normalization (formatting, types)", "aggregation (group operations, metrics)", "enrichment (combining datasets)", "Tools: Python (pandas), SQL, dbt"]},
                {"title": "Data Loading", "items": ["PostgreSQL/MySQL", "Snowflake/BigQuery/Redshift", "bulk loading", "upserts", "partitioned data loading"]},
                {"title": "Pipeline Automation & Monitoring", "items": ["Apache Airflow, Prefect", "logging pipeline activity", "validating row counts", "schema validation", "alerting on failures", "observability", "debugging pipeline failures"]}
            ]
        }
    },
    {
        "topic": "Data Warehousing",
        "category": "Data Engineering",
        "syllabus": {
            "goal": "Design, store, and query structured analytical data efficiently.",
            "sections": [
                {"title": "OLTP vs OLAP", "items": ["OLTP: handles transactional data, normalized structure, frequent updates (banking, ecommerce)", "OLAP: optimized for analysis/reporting, large dataset queries, denormalized structure (BI dashboards, analytics)"]},
                {"title": "Dimensional Data Modeling", "items": ["Dimension modeling principles", "Fact Tables: measurable metrics (sales amount, quantity)", "Dimension Tables: descriptive attributes (customer, product, time)", "Star Schema: central fact table with surrounding dimensions", "Partitioning: improving scan size and query performance"]},
                {"title": "Cloud Data Warehouses", "items": ["Google BigQuery: serverless, columnar storage, automatic scaling", "Snowflake: compute and storage separation, virtual warehouses, data sharing"]},
                {"title": "Querying Analytical Data", "items": ["aggregations across dimensions", "filtering large datasets", "joining fact and dimension tables", "sales by region, revenue by category, activity trends"]}
            ]
        }
    },
    {
        "topic": "Data Ingestion & Incremental Loading",
        "category": "Data Engineering",
        "syllabus": {
            "goal": "Build reliable data ingestion pipelines and implement efficient incremental loading strategies for scalable data systems.",
            "sections": [
                {"title": "Data Ingestion Fundamentals", "items": ["source -> ingestion -> storage flow", "batch vs real-time ingestion (cron jobs, stream consumers)", "data flow architecture"]},
                {"title": "Extraction & Loading Strategies", "items": ["Connectors (pulling vs pushing)", "Extracting from Databases/APIs/Files", "Full load vs Incremental load", "Initial data load", "overwrite vs append", "data freshness"]},
                {"title": "Incremental Loading Techniques", "items": ["change tracking", "data deltas", "timestamp-based loading", "ID-based loading (auto-increment keys)", "high/low watermark / watermark techniques"]},
                {"title": "Change Data Capture (CDC)", "items": ["Database change tracking", "Log-based CDC", "insert, update, delete tracking from event logs"]},
                {"title": "Reliability & Quality", "items": ["Data Deduplication", "Idempotency (safe reprocessing)", "Schema validation", "Data completeness checks", "Error Handling & Retry Mechanisms", "Partitioning for performance"]}
            ]
        }
    },
    {
        "topic": "APIs, Data Validation, and Error Handling",
        "category": "Data Engineering",
        "syllabus": {
            "goal": "Build reliable data ingestion pipelines that safely fetch, validate, and process external data.",
            "sections": [
                {"title": "API Fundamentals", "items": ["REST APIs", "Request-response architecture", "HTTP methods (GET, POST, PUT, DELETE)", "endpoints, headers, parameters, auth tokens"]},
                {"title": "Working with APIs in Python", "items": ["Library: requests", "making GET requests", "passing parameters/headers", "handling JSON responses", "status codes (200, 400, 401, 404, 500)"]},
                {"title": "API Data Ingestion Pipelines", "items": ["handling pagination", "fetching multiple pages", "collecting responses into datasets", "workflow: fetch -> parse -> transform -> store", "API key/bearer token authentication"]},
                {"title": "Data Validation & Schema", "items": ["required fields", "data type/range validation", "null value detection", "schema consistency (expected columns, record format)"]},
                {"title": "Resiliency: Errors & Retries", "items": ["try / except blocks", "catching specific exceptions (timeout, API failure)", "retry logic (delays, max attempts)", "Logging errors and events (record start/success/warnings)"]}
            ]
        }
    },
    {
        "topic": "Python for Data Engineering",
        "category": "Data Engineering",
        "syllabus": {
            "goal": "Apply Python foundations and libraries (Pandas) to build data pipelines.",
            "sections": [
                {"title": "Python Foundations", "items": ["Virtual environments (venv)", "Package management (pip)", "Project folder structure", "Writing clean reusable functions", "Modules and packages", "Environment variables (.env)"]},
                {"title": "Data Processing with pandas", "items": ["DataFrame operations (Selection, filtering, sorting)", "Data transformation (GroupBy, Aggregations, Merge, Join, Concatenation)", "Data cleaning (missing values, duplicates, type conversions)", "Performance: Vectorized operations"]},
                {"title": "Reading/Writing Data Formats", "items": ["CSV (pandas, csv module, delimiters, large files)", "JSON (json module, pandas, parsing nested/flattened)", "Parquet (pyarrow, compression benefits)"]},
                {"title": "Pipeline Scripts", "items": ["API Ingestion (requests, pagination, limits)", "File Handling (os, pathlib, shutil, line by line)", "Logging module (levels, writing to files)", "Modular script structure"]}
            ]
        }
    },
    {
        "topic": "Python for Automation",
        "category": "Data Engineering",
        "syllabus": {
            "goal": "Automate repetitive data tasks such as ingestion, processing, scheduling, and file management.",
            "sections": [
                {"title": "Automation Fundamentals", "items": ["What automation means in DE", "Identifying repetitive tasks", "Benefits: efficiency, reduced manual error", "automated ingestion, processing, scheduling, report generation"]},
                {"title": "Script-Based Automation", "items": ["Writing standalone automation scripts", "command line execution", "script parameters", "reusable scripts", "Automating data movement"]},
                {"title": "System Automation", "items": ["File system (listing, creating, moving, deleting files)", "archiving processed files", "organizing raw datasets", "Automated transformations", "Automating paginated API collection"]},
                {"title": "Scheduling & Monitoring", "items": ["Python scheduling (schedule library)", "System scheduling (cron jobs)", "hourly data processing, daily ingestion, weekly reports", "Logging in automated systems: tracking failures, monitoring task execution", "Error handling in automation: retry logic, network error prevention"]},
                {"title": "Config-Based Automation", "items": ["Storing API endpoints/DB connections in config files", "controlling pipeline parameters", "flexible/reusable automation systems"]}
            ]
        }
    },
    {
        "topic": "Big Data Processing (PySpark)",
        "category": "Data Engineering",
        "syllabus": {
            "goal": "Process large-scale datasets efficiently using distributed computing.",
            "sections": [
                {"title": "Big Data Fundamentals", "items": ["Limitations of single-machine processing", "Distributed computing concept", "Parallel data processing", "Cluster computing (nodes, clusters)", "fault tolerance"]},
                {"title": "Apache Spark Architecture", "items": ["Driver", "Executors", "Cluster manager", "Worker nodes", "Lazy evaluation", "DAG execution model (jobs, stages, tasks)"]},
                {"title": "Environment & DataFrames", "items": ["Spark session creation", "configuration basics", "Reading CSV/JSON/Parquet", "basic operations (select, filter, sort, transformations)"]},
                {"title": "Transformations & Actions", "items": ["Transformations (select, filter, withColumn, groupBy, join)", "Lazy evaluation", "building transformation pipelines", "Actions trigger computation (show, collect, count, write)"]},
                {"title": "Large Dataset Optimization", "items": ["minimizing data shuffling", "filtering early", "Partitioning: improving distribution, repartition vs coalesce", "partition-based queries", "Parallel execution benefits"]}
            ]
        }
    },
    {
        "topic": "Workflow Orchestration (Airflow)",
        "category": "Data Engineering",
        "syllabus": {
            "goal": "Automate, schedule, and manage data pipelines reliably.",
            "sections": [
                {"title": "Orchestration Fundamentals", "items": ["What is workflow orchestration", "Why needed (multi-step pipelines)", "Scheduling vs orchestration", "managing task dependencies"]},
                {"title": "Airflow Architecture", "items": ["core components: Scheduler, Web Server, Worker, Metadata DB", "Key concepts: DAG (Directed Acyclic Graph), Operators, Tasks, Task instances"]},
                {"title": "DAG Structure", "items": ["Creating DAGs in Python", "DAG definition (start date, schedule interval)", "Task creation: PythonOperator, BashOperator, DummyOperator"]},
                {"title": "Task Dependencies & Scheduling", "items": ["Defining execution order (task1 >> task2)", "Upstream vs downstream", "Cron expressions", "backfilling", "manual triggers"]},
                {"title": "Monitoring & Resiliency", "items": ["Airflow web interface monitoring", "task/DAG status tracking", "logs inspection", "Retry configuration (retry count, delay)", "Debugging pipeline issues, troubleshooting failures"]},
                {"title": "Airflow Best Practices", "items": ["modular DAGs", "separating logic from orchestration", "managing env variables", "clean structures"]}
            ]
        }
    },
    {
        "topic": "Data Transformation Framework (dbt)",
        "category": "Data Engineering",
        "syllabus": {
            "goal": "Build structured, maintainable transformation layers on top of raw data in a data warehouse.",
            "sections": [
                {"title": "dbt Fundamentals", "items": ["What is dbt", "Role in Modern Data Stack", "ELT workflow (transformation inside warehouse)", "raw -> transformation -> analytics layer workflow"]},
                {"title": "dbt Project Structure", "items": ["models directory", "seeds, tests, macros directories", "dbt_project.yml", "profiles configuration"]},
                {"title": "SQL-Based Transformations", "items": ["staging models", "intermediate models", "final analytics models", "Materializations: table, view, incremental", "Model dependency management"]},
                {"title": "Incremental Models", "items": ["Efficient processing by loading only new records", "avoiding full table rebuilds", "performance/scalable transformations"]},
                {"title": "Data Testing & Docs", "items": ["Schema tests: uniqueness, non-null, relationship", "custom business rule validation", "automated documentation generation", "visual lineage graphs", "data lineage tracking"]}
            ]
        }
    },
    {
        "topic": "Cloud Basics for Data Engineering (AWS)",
        "category": "Data Engineering",
        "syllabus": {
            "goal": "Understand how data pipelines are built and executed in cloud environments using AWS services.",
            "sections": [
                {"title": "Cloud Computing Fundamentals", "items": ["IaaS, PaaS", "scalability, on-demand infrastructure", "pay-as-you-go pricing", "global AWS infrastructure (Regions, AZs)", "IAM permissions & access keys"]},
                {"title": "Amazon S3 (Data Lake Storage)", "items": ["Buckets and objects", "upload/download", "folder structures", "access control", "storing raw data, processed datasets, logs"]},
                {"title": "Amazon Redshift (Data Warehouse)", "items": ["Redshift architecture", "creating tables", "loading data from S3", "analytical SQL queries", "columnar storage, large-scale queries"]},
                {"title": "AWS Lambda (Serverless Processing)", "items": ["serverless concept", "triggering Lambda (S3 events, API requests)", "lightweight transformations", "automation tasks"]},
                {"title": "Monitoring & Cost", "items": ["managing storage usage", "controlling compute costs", "Cloud data pipeline architecture (Ingest -> S3 -> Python -> Redshift -> Query)"]}
            ]
        }
    },
    {
        "topic": "Docker for Data Engineering",
        "category": "Data Engineering",
        "syllabus": {
            "goal": "Package and run data pipelines in isolated, reproducible environments.",
            "sections": [
                {"title": "Containerization Fundamentals", "items": ["Containers vs VMs", "application isolation", "environment consistency", "reproducible environments"]},
                {"title": "Docker Architecture", "items": ["Docker Engine", "Images", "Containers", "Docker Registry", "image layers", "container lifecycle"]},
                {"title": "Using Docker", "items": ["docker run, ps, stop, rm command", "pulling images from registry", "base images, reusable environments"]},
                {"title": "Building Images (Dockerfile)", "items": ["instructions: FROM, WORKDIR, COPY, RUN, CMD", "installing Python, dependencies, copying pipeline scripts", "docker build and tagging"]},
                {"title": "Advanced Docker for DE", "items": ["Running containerized apps (docker exec)", "Docker Volumes (persistent storage, data sharing)", "Docker Networking basics (container communication, connecting to DBs)", "DE Use cases: packaging pipelines, running Airflow locally"]}
            ]
        }
    },
    {
        "topic": "Git & GitHub (Version Control)",
        "category": "Data Engineering",
        "syllabus": {
            "goal": "Maintain organized, version-controlled codebases and collaborate effectively in team-based data engineering projects.",
            "sections": [
                {"title": "Version Control Fundamentals", "items": ["Importance in tracking code changes", "Local vs Remote repository", "version history"]},
                {"title": "Git Basics", "items": ["git init, add, commit, status, log", "staging area", "commit history snapshots", "managing history locally"]},
                {"title": "GitHub Collaboration", "items": ["creating remote repos", "git clone, push, pull", "Syncing codebase between local and remote"]},
                {"title": "Development Workflow", "items": ["Branching: main, development, feature branches", "Isolated development workflow: branch -> implement -> push -> pull request -> review -> merge"]},
                {"title": "Collaboration & Merge", "items": ["Managing team contributions", "Pull Requests & Code Reviews", "correctness, readability, performance reviews", "handling merge conflicts (conflict detection, manual resolution)", "merge commits vs fast-forward"]},
                {"title": "Repo Management & Structure", "items": ["Project structure (source, config, docs, pipeline scripts)", ".gitignore usage", "README documentation (setup, architecture)", "Issue tracking (GitHub Issues, project boards)", "Commit best practices"]}
            ]
        }
    },
    {
        "topic": "Linux Basics (Terminal & File Management)",
        "category": "Data Engineering",
        "syllabus": {
            "goal": "Use Linux terminal commands to manage files and execute data pipeline scripts.",
            "sections": [
                {"title": "Terminal Fundamentals", "items": ["Opening terminal", "command syntax", "user permissions", "sudo execution"]},
                {"title": "File & Directory Management", "items": ["listing (ls)", "moving (mv)", "copying (cp)", "deleting (rm)", "creating (mkdir, touch)", "working directory (pwd, cd)"]},
                {"title": "File Content & Permissions", "items": ["viewing files (cat, less, head, tail)", "searching (grep)", "editing (nano, vim)", "chmod permissions management"]},
                {"title": "DE Usage", "items": ["Executing Python scripts from shell", "path management", "automation using shell scripts (basics)"]}
            ]
        }
    },
    {
        "topic": "CI/CD for Data Engineering",
        "category": "Data Engineering",
        "syllabus": {
            "goal": "Automate testing, integration, and deployment of data pipelines.",
            "sections": [
                {"title": "CI/CD Fundamentals", "items": ["Continuous Integration (integrating changes, running tests)", "Continuous Delivery/Deployment (automating prepararation/deployment)", "Automation purpose: software/pipeline reliability"]},
                {"title": "CI/CD in Data Engineering", "items": ["updating ETL scripts", "deploying/updating Airflow DAGs/dbt models", "deploying containerized pipelines", "automated pipeline updates, automated testing of transformations"]},
                {"title": "GitHub Actions", "items": ["automation using workflows", "event-based triggers (push, pull request, schedule)", "workflow files, job definitions, task steps"]},
                {"title": "Automated Testing & Build", "items": ["running Python tests in CI", "validating SQL transformations", "preventing faulty deployments", "building Docker images", "installing dependencies, environment preparation"]},
                {"title": "Deployment & Management", "items": ["Automated deployment to staging/production", "updating containers/DAGs", "config separation by environment (dev, staging, production)", "monitoring build success/failure, debugging pipeline failures"]}
            ]
        }
    },
    {
        "topic": "Kubernetes for Data Engineering",
        "category": "Data Engineering",
        "syllabus": {
            "goal": "Understand how containerized data pipelines are deployed, scaled, and managed using Kubernetes.",
            "sections": [
                {"title": "Kubernetes Fundamentals", "items": ["Container orchestration concept", "problems solved: scaling containers, managing multiple services, auto-recovery of failed containers"]},
                {"title": "Architecture & Pods", "items": ["Control Plane (API, Scheduler) vs Worker Nodes (Kubelet, Pods)", "Pod: smallest unit, container grouping, shared network/storage"]},
                {"title": "Deployments & Services", "items": ["Managing replicas", "rolling updates", "scaling applications based on demand", "Services (ClusterIP, NodePort, LoadBalancer) for networking and exposing apps"]},
                {"title": "Configuration & Storage", "items": ["ConfigMaps & Secrets for safe env management", "Persistent Volumes (PV) & Volume Claims (PVC) for pipeline data storage"]},
                {"title": "DE Case Studies", "items": ["Running Spark workloads", "Airflow workers on Kubernetes", "containerized ETL pipelines", "fault tolerance in large-scale data workloads", "Kubernetes cluster interaction commands (creating deployments, viewing pods, checking logs)"]}
            ]
        }
    },
    {
        "topic": "Data Transformation Pipelines",
        "category": "Data Engineering",
        "syllabus": {
            "goal": "Design and implement scalable data transformation workflows to convert raw data into clean, structured, and analysis-ready datasets.",
            "sections": [
                {"title": "Transformation Fundamentals", "items": ["Role in ETL/ELT", "Raw -> cleaned -> structured data lifecycle", "data standardization", "transformation logic design", "reusable modular pipelines"]},
                {"title": "Techniques & Cleaning", "items": ["Filtering, Aggregations, Joins, Merges, Sorting, Grouping", "Row-level vs column-level transformations", "Data quality: handling null values, duplicates, inconsistent data"]},
                {"title": "Advanced Transformations", "items": ["Schema evolution and enforcement", "Distributed processing (PySpark DataFrames, lazy evaluation)", "Nested data (JSON parsing)", "Window functions", "Derived columns"]},
                {"title": "Enrichment & Efficiency", "items": ["Combining multiple datasets (lookup tables, joins)", "Incremental transformations (watermarking, delta processing)", "Performance optimization (partitioning, caching, efficient joins, minimizing shuffling)"]},
                {"title": "Reliability & Output", "items": ["Data validation & quality checks (constraints, integrity)", "Error Handling & Debugging (logging, monitoring fault-tolerant pipelines)", "Writing Transformed Data (output formats like Parquet, overwrite vs append, partitioned storage)"]}
            ]
        }
    }
]

def inject():
    # Clear existing to avoid duplicates if needed, but here we just post.
    # The backend should handle duplicates or we just allow multiple efforts.
    
    print("--- Injecting Roadmap Skills (17 Items) ---")
    for skill in roadmap_skills:
        try:
            r = requests.post(ROADMAP_URL, json=skill)
            if r.status_code == 200:
                print(f"[OK] Roadmap: {skill['skill_name']}")
            elif r.status_code == 400: # Assuming 400 for existing/duplicate if implemented
                print(f"[EXISTS] Roadmap: {skill['skill_name']}")
            else:
                print(f"[ERR] Roadmap: {skill['skill_name']} - {r.text}")
        except Exception as e:
            print(f"[FAIL] {skill['skill_name']}: {e}")

    print("\n--- Injecting Full Modular Syllabi (17 Topics) ---")
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
