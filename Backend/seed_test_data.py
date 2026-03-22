import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project root to sys.path
sys.path.append(os.getcwd())

from databaseop.device_service import seed_default_devices

def seed():
    customer_id = "cust-123"
    print(f"Seeding default devices for {customer_id}...")
    result = seed_default_devices(customer_id)
    print(f"Result: {result}")

if __name__ == "__main__":
    seed()
