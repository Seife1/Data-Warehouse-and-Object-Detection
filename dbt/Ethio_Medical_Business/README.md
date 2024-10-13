# Ethio Medical Business DBT Project

## Overview

The Ethio Medical Business project leverages DBT (Data Build Tool) for data transformation and modeling. This README provides a comprehensive guide to setting up and using DBT to transform the raw data collected from various sources into structured datasets for analysis.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python** (version 3.6 or later)
- **DBT** (Data Build Tool)
- Access to a **PostgreSQL** database (configured in the `profiles.yml` file)

## Getting Started

### 1. Setting Up DBT

To set up DBT, follow these steps:

1. **Install DBT**: Use pip to install DBT by running the following command in your terminal:

```bash
pip install dbt-postgres
```

2. **Initialize a DBT Project**: Create a new DBT project by running:

```bash
dbt init Ethio_Medical_Business
```

After this follow the next step from your terminal to configured in the `profiles.yml` file to connect to your PostgreSQL database.

### 3. Defining Models

DBT models are SQL files that define transformations on your data. In this project:

- Create SQL files in the `models` directory to define transformations based on the `cleaned_scraped_data` table.
- An example of a transformation might involve grouping data by `Channel Title` to analyze engagement.

### 4. Running DBT Models
Once your models are defined, run the following command to execute the transformations and load the data into your data warehouse:

```bash
dbt run
```

### 5. Testing and Documentation
To ensure data quality and provide context for the transformations, you can use DBT’s testing and documentation features:

* **Run Tests**: Validate your models with:
```bash
dbt test
```
Here is a sample image from the `../../data/random` folder:

![Sample Image](../../data/random/dbt_test.jpg)

* **Generate Documentation**: Create documentation for your models and transformations:

```bash
dbt docs generate
```

* **Serve Documentation**: View the generated documentation in your browser:

```bash
dbt docs serve
```

Here is a sample image from the `../../data/random` folder:

![Sample Image](../../data/random/sample_generated_doc.jpg)