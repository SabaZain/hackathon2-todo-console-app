import os
import sys

# Check if DATABASE_URL is set
db_url = os.environ.get('DATABASE_URL', 'not set')
print("DATABASE_URL is set to: " + str(db_url))

# Test importing backend modules
try:
    import backend.main
    print("Main module imported successfully")
except ImportError as e:
    print("Failed to import main module: " + str(e))

try:
    import backend.db
    print("DB module imported successfully")
except ImportError as e:
    print("Failed to import db module: " + str(e))

try:
    import backend.models
    print("Models module imported successfully")
except ImportError as e:
    print("Failed to import models module: " + str(e))

try:
    import backend.auth
    print("Auth module imported successfully")
except ImportError as e:
    print("Failed to import auth module: " + str(e))

try:
    import backend.routes.tasks
    print("Routes tasks module imported successfully")
except ImportError as e:
    print("Failed to import routes tasks module: " + str(e))

print("\nAll required modules are available!")