#!/usr/bin/env python3
"""
Batch prediction script using deployed Gunicorn app.
Queries specified table for specified month/year data,
sends features to the Gunicorn app for prediction, and writes results back to the database.

Usage:
    python batch_app_predict_from_db.py <year> <month> <table_name>

Examples:
    python batch_app_predict_from_db.py 2025 4 customer_features_test2    # April 2025
    python batch_app_predict_from_db.py 2025 12 customer_features_test2   # December 2025
    python batch_app_predict_from_db.py 2024 6 customer_features_prod     # June 2024
"""

import pandas as pd
import sys
import logging
from sqlalchemy import create_engine, text, inspect
from dotenv import load_dotenv
import os
from datetime import datetime
import argparse
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Database configuration
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_URI = f"postgresql+psycopg2://user:{POSTGRES_PASSWORD}@localhost:4321/mydb"

# Gunicorn app configuration
GUNICORN_PREDICT_URL = os.getenv("GUNICORN_PREDICT_URL", "http://0.0.0.0:9999/predict")

# Table configuration
FEATURE_COLUMNS = ["x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8", "x9", "x10"]


def parse_arguments():
    """Parse command line arguments for year, month, and table name."""
    parser = argparse.ArgumentParser(
        description="Batch prediction script for customer persona analysis (Gunicorn app)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python batch_app_predict_from_db.py 2025 4 customer_features_test2    # April 2025
  python batch_app_predict_from_db.py 2025 12 customer_features_test2   # December 2025
  python batch_app_predict_from_db.py 2024 6 customer_features_prod     # June 2024
        """
    )
    parser.add_argument('year', type=int, help='Year to query (e.g., 2025)')
    parser.add_argument('month', type=int, help='Month to query (1-12)', choices=range(1, 13))
    parser.add_argument('table_name', type=str, help='Name of the table to query and update (e.g., customer_features_test2)')
    return parser.parse_args()


def validate_date(year, month):
    """Validate that the date is reasonable."""
    current_year = datetime.now().year
    if year > current_year + 1:
        logger.warning(f"Year {year} is more than 1 year in the future")
    if year < 2020:
        logger.warning(f"Year {year} seems too far in the past")
    logger.info(f"Processing data for {month}/{year}")


def connect_to_database():
    """Create database connection."""
    try:
        engine = create_engine(DB_URI)
        logger.info("✅ Database connection established")
        return engine
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        sys.exit(1)


def query_data_by_month(engine, year, month, table_name):
    """Query data for specified month/year from the specified table."""
    try:
        inspector = inspect(engine)
        columns = [col['name'] for col in inspector.get_columns(table_name)]
        logger.info(f"Available columns in {table_name}: {columns}")
        if 'customer_id' in columns:
            query = f"""
            SELECT customer_id, {', '.join(FEATURE_COLUMNS)}, date
            FROM {table_name}
            WHERE EXTRACT(YEAR FROM date) = {year} 
            AND EXTRACT(MONTH FROM date) = {month}
            ORDER BY customer_id
            """
        else:
            query = f"""
            SELECT {', '.join(FEATURE_COLUMNS)}, date
            FROM {table_name}
            WHERE EXTRACT(YEAR FROM date) = {year} 
            AND EXTRACT(MONTH FROM date) = {month}
            """
        logger.info(f"Querying data for {month}/{year} from {table_name}...")
        df = pd.read_sql(query, engine)
        if 'customer_id' not in df.columns:
            df['temp_id'] = range(len(df))
            logger.info("No customer_id column found, using temporary index")
        logger.info(f"Retrieved {len(df)} records for {month}/{year} from {table_name}")
        return df
    except Exception as e:
        logger.error(f"Failed to query data from {table_name}: {e}")
        sys.exit(1)


def make_predictions_gunicorn(df):
    """Send features to the Gunicorn app for prediction."""
    try:
        features = df[FEATURE_COLUMNS].copy()
        logger.info(f"Sending {len(features)} records to Gunicorn app for prediction...")
        response = requests.post(
            GUNICORN_PREDICT_URL,
            json=features.to_dict(orient="records"),
            timeout=60,
        )
        if response.status_code != 200:
            logger.error(f"Gunicorn app returned status {response.status_code}: {response.text}")
            sys.exit(1)
        result = response.json()
        labels = result.get("labels")
        if labels is None or len(labels) != len(df):
            logger.error("Prediction response missing or mismatched labels.")
            sys.exit(1)
        df['persona'] = labels
        logger.info(f"✅ Received predictions for {len(labels)} records")
        return df
    except Exception as e:
        logger.error(f"Failed to get predictions from Gunicorn app: {e}")
        sys.exit(1)


def update_database(engine, df, table_name):
    """Update the database with the new persona predictions."""
    try:
        logger.info(f"Updating {table_name} with predictions...")
        with engine.connect() as conn:
            if 'customer_id' in df.columns:
                for _, row in df.iterrows():
                    update_query = text(f"""
                        UPDATE {table_name}
                        SET persona = :persona
                        WHERE customer_id = :customer_id
                    """)
                    conn.execute(update_query, {
                        'persona': int(row['persona']),
                        'customer_id': row['customer_id']
                    })
            else:
                logger.info("No customer_id found, using feature-based matching for updates")
                for _, row in df.iterrows():
                    where_conditions = []
                    params = {'persona': int(row['persona'])}
                    for col in FEATURE_COLUMNS:
                        where_conditions.append(f"{col} = :{col}")
                        params[col] = row[col]
                    where_conditions.append("date = :date")
                    params['date'] = row['date']
                    where_clause = " AND ".join(where_conditions)
                    update_query = text(f"""
                        UPDATE {table_name}
                        SET persona = :persona
                        WHERE {where_clause}
                    """)
                    conn.execute(update_query, params)
            conn.commit()
        logger.info(f"✅ Successfully updated {len(df)} records in {table_name}")
    except Exception as e:
        logger.error(f"Failed to update {table_name}: {e}")
        sys.exit(1)


def main():
    args = parse_arguments()
    year = args.year
    month = args.month
    table_name = args.table_name
    validate_date(year, month)
    logger.info(f"Starting batch prediction for {month}/{year} data from {table_name} using Gunicorn app...")
    engine = connect_to_database()
    df = query_data_by_month(engine, year, month, table_name)
    if len(df) == 0:
        logger.warning(f"No data found for {month}/{year} in {table_name}. Exiting.")
        return
    df_with_predictions = make_predictions_gunicorn(df)
    update_database(engine, df_with_predictions, table_name)
    logger.info("=== PREDICTION SUMMARY ===")
    logger.info(f"Table: {table_name}")
    logger.info(f"Total records processed: {len(df)}")
    logger.info(f"Date range: {month}/{year}")
    logger.info(f"Persona distribution:")
    persona_counts = df_with_predictions['persona'].value_counts().sort_index()
    for persona, count in persona_counts.items():
        logger.info(f"  Persona {persona}: {count} customers")
    logger.info("Batch prediction completed successfully!")


if __name__ == "__main__":
    main()