#!/usr/bin/env python3
"""
Batch prediction script for April 2025 data.
Queries customer_features_test2 table for April 2025 data,
makes predictions using the MLflow model, and writes results back to the database.
"""

import pandas as pd
import mlflow
import sys
import logging
from sqlalchemy import create_engine, text, inspect
from dotenv import load_dotenv
import os
from datetime import datetime

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
TABLE_NAME = "customer_features_test2"
FEATURE_COLUMNS = ["x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8", "x9", "x10"]


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


def query_april_2025_data(engine):
    """Query data for April 2025 from the customer_features_test2 table."""
    try:
        # First, let's check what columns are actually available in the table
        inspector = inspect(engine)
        columns = [col['name'] for col in inspector.get_columns(TABLE_NAME)]
        logger.info(f"Available columns in {TABLE_NAME}: {columns}")
        
        # Check if customer_id exists, if not, we'll use a different approach
        if 'customer_id' in columns:
            query = f"""
            SELECT customer_id, {', '.join(FEATURE_COLUMNS)}, date
            FROM {TABLE_NAME}
            WHERE EXTRACT(YEAR FROM date) = 2025 
            AND EXTRACT(MONTH FROM date) = 4
            ORDER BY customer_id
            """
        else:
            # If no customer_id, we'll use all available columns and create a temporary index
            query = f"""
            SELECT {', '.join(FEATURE_COLUMNS)}, date
            FROM {TABLE_NAME}
            WHERE EXTRACT(YEAR FROM date) = 2025 
            AND EXTRACT(MONTH FROM date) = 4
            """
        
        logger.info("Querying April 2025 data from database...")
        df = pd.read_sql(query, engine)
        
        # Add a temporary index if no customer_id exists
        if 'customer_id' not in df.columns:
            df['temp_id'] = range(len(df))
            logger.info("No customer_id column found, using temporary index")
        
        logger.info(f"Retrieved {len(df)} records for April 2025")
        return df
        
    except Exception as e:
        logger.error(f"Failed to query data: {e}")
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


def update_database(engine, df):
    """Update the database with the new persona predictions."""
    try:
        logger.info("Updating database with predictions...")
        
        with engine.connect() as conn:
            if 'customer_id' in df.columns:
                # Use customer_id for updates if available
                for _, row in df.iterrows():
                    update_query = text(f"""
                        UPDATE {TABLE_NAME}
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
                        UPDATE {TABLE_NAME}
                        SET persona = :persona
                        WHERE {where_clause}
                    """)
                    
                    conn.execute(update_query, params)
            
            conn.commit()
        
        logger.info(f"✅ Successfully updated {len(df)} records in database")
        
    except Exception as e:
        logger.error(f"Failed to update database: {e}")
        sys.exit(1)


def main():
    """Main execution function."""
    logger.info("Starting batch prediction for April 2025 data...")
    
    # Load the model
    model = load_model()
    
    # Connect to database
    engine = connect_to_database()
    
    # Query April 2025 data
    df = query_april_2025_data(engine)
    
    if len(df) == 0:
        logger.warning("No data found for April 2025. Exiting.")
        return
    
    # Make predictions
    df_with_predictions = make_predictions(model, df)
    
    # Update database
    update_database(engine, df_with_predictions)
    
    # Print summary
    logger.info("=== PREDICTION SUMMARY ===")
    logger.info(f"Total records processed: {len(df)}")
    logger.info(f"Date range: April 2025")
    logger.info(f"Persona distribution:")
    persona_counts = df_with_predictions['persona'].value_counts().sort_index()
    for persona, count in persona_counts.items():
        logger.info(f"  Persona {persona}: {count} customers")
    
    logger.info("Batch prediction completed successfully!")


if __name__ == "__main__":
    main() 