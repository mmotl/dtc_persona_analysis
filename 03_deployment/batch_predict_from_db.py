#!/usr/bin/env python3
"""
Parameterized batch prediction script.
Queries specified table for specified month/year data,
makes predictions using the MLflow model, and writes results back to the database.

Usage:
    python batch_predict_april_2025_param.py <year> <month> <table_name>
    
Examples:
    python batch_predict_april_2025_param.py 2025 4 customer_features_test2    # April 2025
    python batch_predict_april_2025_param.py 2025 12 customer_features_test2   # December 2025
    python batch_predict_april_2025_param.py 2024 6 customer_features_prod     # June 2024
"""

import pandas as pd
import mlflow
import sys
import logging
from sqlalchemy import create_engine, text, inspect
from dotenv import load_dotenv
import os
from datetime import datetime
import argparse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Database configuration
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_URI = f"postgresql+psycopg2://user:{POSTGRES_PASSWORD}@localhost:4321/mydb"

# MLflow configuration
MLFLOW_TRACKING_URI = "http://localhost:5050"
MODEL_NAME = "dtc_persona_clustering_model"
MODEL_STAGE = "Production"
MODEL_URI = f"models:/{MODEL_NAME}/{MODEL_STAGE}"

# Table configuration
FEATURE_COLUMNS = ["x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8", "x9", "x10"]


def parse_arguments():
    """Parse command line arguments for year, month, and table name."""
    parser = argparse.ArgumentParser(
        description="Batch prediction script for customer persona analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python batch_predict_april_2025_param.py 2025 4 customer_features_test2    # April 2025
  python batch_predict_april_2025_param.py 2025 12 customer_features_test2   # December 2025
  python batch_predict_april_2025_param.py 2024 6 customer_features_prod     # June 2024
        """
    )
    
    parser.add_argument(
        'year', 
        type=int, 
        help='Year to query (e.g., 2025)'
    )
    
    parser.add_argument(
        'month', 
        type=int, 
        help='Month to query (1-12)',
        choices=range(1, 13)
    )
    
    parser.add_argument(
        'table_name',
        type=str,
        help='Name of the table to query and update (e.g., customer_features_test2)'
    )
    
    return parser.parse_args()


def validate_date(year, month):
    """Validate that the date is reasonable."""
    current_year = datetime.now().year
    current_month = datetime.now().month
    
    if year > current_year + 1:
        logger.warning(f"Year {year} is more than 1 year in the future")
    
    if year < 2020:
        logger.warning(f"Year {year} seems too far in the past")
    
    logger.info(f"Processing data for {month}/{year}")


def load_model():
    """Load the MLflow model for predictions."""
    try:
        logger.info(f"Connecting to MLflow Tracking Server at: {MLFLOW_TRACKING_URI}")
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        
        logger.info(f"Loading model '{MODEL_NAME}' from stage '{MODEL_STAGE}'...")
        model = mlflow.pyfunc.load_model(model_uri=MODEL_URI)
        
        logger.info("✅ Model loaded successfully!")
        return model
        
    except mlflow.exceptions.RestException as e:
        logger.error(f"MLflow REST API error: {e}")
        logger.error("Check if MLflow server is running and model exists in registry")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error loading model: {e}")
        sys.exit(1)


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
        # First, let's check what columns are actually available in the table
        inspector = inspect(engine)
        columns = [col['name'] for col in inspector.get_columns(table_name)]
        logger.info(f"Available columns in {table_name}: {columns}")
        
        # Check if customer_id exists, if not, we'll use a different approach
        if 'customer_id' in columns:
            query = f"""
            SELECT customer_id, {', '.join(FEATURE_COLUMNS)}, date
            FROM {table_name}
            WHERE EXTRACT(YEAR FROM date) = {year} 
            AND EXTRACT(MONTH FROM date) = {month}
            ORDER BY customer_id
            """
        else:
            # If no customer_id, we'll use all available columns and create a temporary index
            query = f"""
            SELECT {', '.join(FEATURE_COLUMNS)}, date
            FROM {table_name}
            WHERE EXTRACT(YEAR FROM date) = {year} 
            AND EXTRACT(MONTH FROM date) = {month}
            """
        
        logger.info(f"Querying data for {month}/{year} from {table_name}...")
        df = pd.read_sql(query, engine)
        
        # Add a temporary index if no customer_id exists
        if 'customer_id' not in df.columns:
            df['temp_id'] = range(len(df))
            logger.info("No customer_id column found, using temporary index")
        
        logger.info(f"Retrieved {len(df)} records for {month}/{year} from {table_name}")
        return df
        
    except Exception as e:
        logger.error(f"Failed to query data from {table_name}: {e}")
        sys.exit(1)


def make_predictions(model, df):
    """Make predictions using the loaded model."""
    try:
        # Prepare features for prediction
        features = df[FEATURE_COLUMNS].copy()
        
        logger.info("Making predictions...")
        predictions = model.predict(features)
        
        # Add predictions to the dataframe
        df['persona'] = predictions
        
        logger.info(f"✅ Made predictions for {len(df)} records")
        return df
        
    except Exception as e:
        logger.error(f"Failed to make predictions: {e}")
        sys.exit(1)


def update_database(engine, df, table_name):
    """Update the database with the new persona predictions."""
    try:
        logger.info(f"Updating {table_name} with predictions...")
        
        with engine.connect() as conn:
            if 'customer_id' in df.columns:
                # Use customer_id for updates if available
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
                # If no customer_id, we need to use a different approach
                # We'll use a combination of features and date to identify unique records
                logger.info("No customer_id found, using feature-based matching for updates")
                
                for _, row in df.iterrows():
                    # Create a WHERE clause using all feature columns and date
                    where_conditions = []
                    params = {'persona': int(row['persona'])}
                    
                    for col in FEATURE_COLUMNS:
                        where_conditions.append(f"{col} = :{col}")
                        params[col] = row[col]
                    
                    # Add date condition
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
    """Main execution function."""
    # Parse command line arguments
    args = parse_arguments()
    year = args.year
    month = args.month
    table_name = args.table_name
    
    # Validate the date
    validate_date(year, month)
    
    logger.info(f"Starting batch prediction for {month}/{year} data from {table_name}...")
    
    # Load the model
    model = load_model()
    
    # Connect to database
    engine = connect_to_database()
    
    # Query data for specified month/year
    df = query_data_by_month(engine, year, month, table_name)
    
    if len(df) == 0:
        logger.warning(f"No data found for {month}/{year} in {table_name}. Exiting.")
        return
    
    # Make predictions
    df_with_predictions = make_predictions(model, df)
    
    # Update database
    update_database(engine, df_with_predictions, table_name)
    
    # Print summary
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