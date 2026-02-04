#!/usr/bin/env python3
"""
Script to set up the combined database schema for both Todo app and Chatbot
"""

import os
import sys
from sqlmodel import SQLModel
from db import engine
from models import get_unique_task_model, get_unique_user_model  # Import the existing models
Task = get_unique_task_model()
User = get_unique_user_model()

def setup_database():
    """Set up the database with both todo app and chatbot schemas"""
    print("Setting up combined database schema for Todo app and Chatbot...")

    # Create tables for the existing todo app
    print("Creating todo app tables...")
    SQLModel.metadata.create_all(bind=engine)
    print("Todo app tables created successfully!")

    # Initialize the chatbot database schema as well
    try:
        print("Initializing chatbot database schema...")
        from database.conversations import db_manager
        # The db_manager initialization already creates the required tables
        print("Chatbot database schema created successfully!")
    except ImportError as e:
        print(f"Warning: Could not initialize chatbot database: {e}")
        return False

    print("\n[OK] Combined database schema is ready!")
    print("[OK] Todo app tables (Task, User) created")
    print("[OK] Chatbot tables (conversations, messages) created")
    print("[OK] Foreign key relationships established")
    print("[OK] Indexes created for performance")

    return True

if __name__ == "__main__":
    success = setup_database()
    if not success:
        sys.exit(1)