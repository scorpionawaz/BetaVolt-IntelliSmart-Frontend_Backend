import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project root to sys.path
sys.path.append(os.getcwd())

# Import db first to ensure connection but tools.py does it too
from databaseop.database import db

# Mocking the TOOL_DECLARATIONS if needed, but we just want the functions
from nimipersonal.tools import get_home_state, device_control

def test_sync():
    customer_id = "cust-123" # This is the hardcoded ID we used in agent.py and tools.py
    
    print(f"--- Testing get_home_state for {customer_id} ---")
    state = get_home_state(customer_id)
    print(f"Status: {state['status']}")
    
    if state['status'] == 'success':
        print(f"Found {len(state['devices'])} devices.")
        tariff = state['current_tariff'].get('current_rate_INR', 'N/A')
        print(f"Current Tariff Rate: {tariff}")
        
        print("\n--- Testing device_control ---")
        if state['devices']:
            device = state['devices'][0]
            device_id = device['device_id']
            name = device['name']
            old_status = device['status']
            new_action = "turn_off" if old_status == "on" else "turn_on"
            
            print(f"Toggling {name} ({device_id}) from {old_status} to {new_action}...")
            result = device_control(device_id=device_id, device_name=name, action=new_action, reason="Verification Test")
            print(f"Result: {result}")
            
            # Verify in DB
            updated_device = db.Devices.find_one({"device_id": device_id})
            print(f"New Status in DB: {updated_device['status']}")
            
            expected_status = "on" if new_action == "turn_on" else "off"
            if updated_device['status'] == expected_status:
                print("✅ Database Synchronization Successful!")
            else:
                print(f"❌ Database Synchronization Failed! Expected {expected_status}, got {updated_device['status']}")
        else:
            print("No devices found in DB. Please ensure devices are seeded.")
    else:
        print(f"❌ get_home_state failed: {state.get('message')}")

if __name__ == "__main__":
    test_sync()
