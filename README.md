# Weather Data Streaming Pipeline (AWS)

This project is part of my personal portfolio, built to deepen my understanding of AWS data services and real-time pipelines. The idea was to collect weather data from a public API, process it in near real-time using AWS services, and make it queryable for analytics.

---

## 📌 Overview

I designed and deployed a real-time streaming pipeline that ingests weather data from multiple cities around the world, processes and stores it in an analytics-ready format using AWS services. Below are the steps already implemented:

---

## 1. Data Collection (Ingestion)

The pipeline starts by fetching weather data from the [OpenWeatherMap API](https://openweathermap.org/api).

- A Lambda function makes periodic requests to the API.
- The results are sent directly to a Kinesis Data Stream for real-time processing.

---

## 2. Streaming Ingestion

Once in the stream:

- Another AWS Lambda function listens to the Kinesis Data Stream.
- It writes the raw payload into an S3 bucket (`/raw` folder), preserving the original structure for traceability.

---

## 3. ETL (Data Transformation)

To clean and normalize the data:

- I created a Glue Job using PySpark to parse and transform the JSON structure.
- The cleaned data is written to a new folder in the same S3 bucket (`/processed`), in a flattened and analytics-friendly format.

---

## 4. Data Cataloging

To enable query capabilities:

- A Glue Crawler scans the `processed/` folder and updates the AWS Glue Data Catalog with the correct schema.

---

## 5. Analytical Storage (Amazon Redshift)

To support advanced queries:

- I set up a Redshift cluster and created a table matching the transformed schema.
- The data from S3 was loaded into Redshift using the COPY command.

---

## 6. Querying the Data

I successfully queried the weather dataset in Redshift using SQL, performing filters, joins, and aggregations to prepare the data for analytical use.

---

## ✅ Next Steps (coming soon...)

- Schedule the pipeline using Step Functions + EventBridge.
- Add monitoring with CloudWatch.
- Automate deployment using Terraform or AWS CDK.

---

This was a really hands-on way to explore the key components of a modern streaming data pipeline on AWS. It also taught me a lot about debugging and managing AWS services in a sandboxed environment.
