import os
import httpx
import uvicorn
import asyncio
import base64
import json
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
# from liveagent import LiveAgent
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import asyncio
from datetime import datetime
import pytz
# importing all agents 
from nimipersonal.agent import LiveAgent
from betavoltsupport.agent import BetaVoltSupport
from nimipersonal_tarrif.agent import AgentTarrif
from databaseop.tariff_service import set_live_tariff, get_slot_tariffs, get_latest_tariff
from databaseop.device_service import (
    get_devices_by_customer, add_device, update_device,
    delete_device, seed_default_devices
)
from dotenv import load_dotenv
load_dotenv()

# ============================================================
# Background Tasks (Slot Tariffs)
# ============================================================
async def slot_tariff_updater():
    """Continuously checks the current time against slots and updates live tariff if needed."""
    IST = pytz.timezone('Asia/Kolkata')
    last_applied_slot = None
    
    while True:
        try:
            now_ist = datetime.now(IST)
            hour = now_ist.hour
            
            # Determine current slot
            if 6 <= hour < 18:
                current_slot = "standard"
            elif 18 <= hour < 23:
                current_slot = "peak"
            else:
                current_slot = "off_peak"

            if last_applied_slot != current_slot:
                print(f"[Slot Updater] Shifting to {current_slot} slot.")
                slots = get_slot_tariffs()
                rate = slots.get(current_slot, 6.80)
                reason = f"Auto-transition to {current_slot} hours"
                
                # Update live tariff
                set_live_tariff(rate, reason, "system_auto")
                last_applied_slot = current_slot
                
        except Exception as e:
            print(f"[Slot Updater Error] {e}")
            
        await asyncio.sleep(300) # check every 5 minutes

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create background tasks
    task = asyncio.create_task(slot_tariff_updater())
    yield
    # Shutdown: Cancel background tasks
    task.cancel()

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specifically ["https://sfu.mirotalk.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health():
    return {"status": "ok"}      

# defination of the lunching bot in meet ============
class LaunchRequest(BaseModel):
    room_name: str    
    projectid: str
    duration_minutes: int

async def send_bot_request(url, payload):
    async with httpx.AsyncClient() as client:
        await client.post(url, json=payload, timeout=10.0)

# ============================================================
# code for steeing the tarrif 
# ============================================================
class TariffRequest(BaseModel):
    rate: float
    reason: str
    user: str

@app.post("/tariff")
def update_tariff(request: TariffRequest):
    try:
        result = set_live_tariff(request.rate, request.reason, request.user)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tariff")
def get_tariff():
    try:
        from databaseop.tariff_service import get_latest_tariff
        return get_latest_tariff()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class SlotTariffRequest(BaseModel):
    off_peak: float
    standard: float
    peak: float
    user: str

@app.post("/tariff/slots")
def update_slot_tariffs(request: SlotTariffRequest):
    try:
        from databaseop.tariff_service import set_slot_tariffs
        result = set_slot_tariffs(request.off_peak, request.standard, request.peak, request.user)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tariff/slots")
def get_slots():
    try:
        from databaseop.tariff_service import get_slot_tariffs
        return get_slot_tariffs()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===========================================================
# Devices API — CRUD per customer
# ===========================================================

class DeviceAddRequest(BaseModel):
    name: str
    icon_key: str
    power_consumption_watts: int
    status: str = "off"
    usage_hours_today: float = 0.0
    expected_usage: str = ""

class DeviceUpdateRequest(BaseModel):
    name: str | None = None
    icon_key: str | None = None
    power_consumption_watts: int | None = None
    status: str | None = None
    usage_hours_today: float | None = None
    expected_usage: str | None = None

@app.get("/customers/{customer_id}/devices")
def get_devices(customer_id: str):
    """Return all devices for a given customer."""
    try:
        return get_devices_by_customer(customer_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/customers/{customer_id}/devices")
def create_device(customer_id: str, request: DeviceAddRequest):
    """Add a new device for a customer."""
    try:
        return add_device(
            customer_id=customer_id,
            name=request.name,
            icon_key=request.icon_key,
            power_consumption_watts=request.power_consumption_watts,
            status=request.status,
            usage_hours_today=request.usage_hours_today,
            expected_usage=request.expected_usage,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/customers/{customer_id}/devices/{device_id}")
def modify_device(customer_id: str, device_id: str, request: DeviceUpdateRequest):
    """Update one or more fields of a device."""
    try:
        # Build only non-None fields
        update_data = {k: v for k, v in request.model_dump().items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields provided")
        success = update_device(customer_id, device_id, update_data)
        return {"success": success}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/customers/{customer_id}/devices/{device_id}")
def remove_device(customer_id: str, device_id: str):
    """Delete a device."""
    try:
        success = delete_device(customer_id, device_id)
        if not success:
            raise HTTPException(status_code=404, detail="Device not found")
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/customers/{customer_id}/devices/seed")
def seed_devices(customer_id: str):
    """Seed the 10 default devices for a new customer (no-op if they already exist)."""
    try:
        return seed_default_devices(customer_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===========================================================
# Admin Consumer Search & Support Tickets API
# ===========================================================
from databaseop.database import db
from databaseop.customer_service import (
    set_customer_type as svc_set_customer_type,
    topup_wallet as svc_topup_wallet,
    add_solar_record as svc_add_solar_record,
    get_customer_by_id as svc_get_customer_by_id,
    get_customer_bills as svc_get_customer_bills,
)

@app.get("/customers/search")
def search_customers(q: str):
    """Search for a customer by strictly matching ID, or partial match on name/phone."""
    try:
        if not q:
            return None
        import re
        query_pattern = re.compile(q, re.IGNORECASE)
        
        # Search match logic
        search_filter = {
            "$or": [
                {"customer_id": query_pattern},
                {"full_name": query_pattern},
                {"contact.phone": query_pattern}
            ]
        }
        
        # Try numeric match if numeric
        if q.isdigit():
            search_filter["$or"].append({"customer_id": q})
            
        customer = db['Customers'].find_one(search_filter)
        print(f"[Search] Query '{q}' matched: {customer.get('full_name') if customer else 'None'}")
        
        # If not found by those, try Object ID if it looks like one
        if not customer and len(q) == 24:
            try:
                from bson import ObjectId
                customer = db['Customers'].find_one({"_id": ObjectId(q)})
            except:
                pass
        
        if not customer:
            return None
        
        customer['_id'] = str(customer['_id'])
        cid = customer.get('customer_id')
        
        # Enrich with devices
        devices = []
        if cid:
            devices = get_devices_by_customer(cid)
            
        # Enrich with tickets
        tickets = []
        if cid:
            cursor = db['Support_Tickets'].find({"customer_id": cid}).sort("created_at", -1)
            for t in cursor:
                t['_id'] = str(t['_id'])
                tickets.append(t)
                
        # Enrich with bills
        bills = []
        if cid:
            cursor = db['Bills'].find({"customer_id": cid}).sort("bill_date", -1)
            for b in cursor:
                b['_id'] = str(b['_id'])
                bills.append(b)
                
        customer['devices'] = devices
        customer['support_tickets'] = tickets
        customer['bills'] = bills
        
        return customer
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/customers/{customer_id}/type")
def set_customer_type(customer_id: str, body: dict):
    """Set the type for a customer: prepaid|postpaid|solar"""
    try:
        ctype = body.get("customer_type") if isinstance(body, dict) else None
        if not ctype:
            raise HTTPException(status_code=400, detail="missing customer_type")
        result = svc_set_customer_type(customer_id, ctype)
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error", "failed"))
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/customers/{customer_id}/wallet/topup")
def wallet_topup(customer_id: str, body: dict):
    """Top-up prepaid wallet for a customer. Body: {amount: float}"""
    try:
        amount = float(body.get("amount", 0)) if isinstance(body, dict) else 0
        if amount <= 0:
            raise HTTPException(status_code=400, detail="invalid amount")
        res = svc_topup_wallet(customer_id, amount)
        return res
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/customers/{customer_id}/solar/record")
def add_solar_record(customer_id: str, body: dict):
    """Record solar input/output for solar customers. Body: {input_kwh, output_kwh, timestamp?} """
    try:
        input_kwh = float(body.get("input_kwh", 0)) if isinstance(body, dict) else 0
        output_kwh = float(body.get("output_kwh", 0)) if isinstance(body, dict) else 0
        ts = body.get("timestamp") if isinstance(body, dict) else None
        res = svc_add_solar_record(customer_id, input_kwh, output_kwh, ts)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/customers/{customer_id}")
def get_customer(customer_id: str):
    try:
        c = svc_get_customer_by_id(customer_id)
        if not c:
            raise HTTPException(status_code=404, detail="customer not found")
        return c
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/customers/{customer_id}/wallet")
def get_customer_wallet(customer_id: str):
    try:
        # Read wallet balance and recent transactions
        from databaseop.customer_service import get_wallet_transactions
        c = svc_get_customer_by_id(customer_id)
        if not c:
            raise HTTPException(status_code=404, detail="customer not found")
        balance = c.get("wallet_balance", 0)
        txs = get_wallet_transactions(customer_id)
        return {"wallet_balance": balance, "transactions": txs}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/customers/{customer_id}/solar")
def get_customer_solar(customer_id: str):
    try:
        from databaseop.customer_service import get_solar_records
        c = svc_get_customer_by_id(customer_id)
        if not c:
            raise HTTPException(status_code=404, detail="customer not found")
        records = get_solar_records(customer_id)
        return {"records": records}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/support-tickets")
def get_all_support_tickets():
    """Admin view: gets all support tickets."""
    try:
        cursor = db['Support_Tickets'].find().sort("created_at", -1)
        tickets = []
        for t in cursor:
            t['_id'] = str(t['_id'])
            # fetch the customer name for admin display
            c = db['Customers'].find_one({"customer_id": t.get("customer_id")})
            if c:
                t['customer_name'] = c.get('full_name', 'Unknown')
            else:
                t['customer_name'] = 'Unknown'
            tickets.append(t)
        return tickets
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/customers/{customer_id}/support-tickets")
def get_customer_support_tickets(customer_id: str):
    """Consumer view: gets tickets for a specific user."""
    try:
        cursor = db['Support_Tickets'].find({"customer_id": customer_id}).sort("created_at", -1)
        tickets = []
        for t in cursor:
            t['_id'] = str(t['_id'])
            tickets.append(t)
        return tickets
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/customers/{customer_id}/bills")
def get_customer_bills(customer_id: str):
    """Consumer view: gets bills for a specific user."""
    try:
        return svc_get_customer_bills(customer_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===========================================================
# Admin Billing & Transactions API
# ===========================================================

@app.get("/admin/billing/stats")
def get_billing_stats():
    """Returns high-level financial metrics for the admin dashboard."""
    try:
        all_bills = list(db['Bills'].find())
        total_mtd = 0
        outstanding = 0
        overdue_count = 0
        
        for b in all_bills:
            val_str = b.get('amount', '₹0').replace('₹', '').replace(',', '')
            val = float(val_str)
            
            if b.get('status') == 'Paid' and 'March' in b.get('month', ''):
                total_mtd += val
            elif b.get('status') == 'Unpaid':
                outstanding += val
            elif b.get('status') == 'Overdue':
                outstanding += val
                overdue_count += 1
        
        # Scale: If it's over 1 Lakh, show in Cr/Lakh, otherwise just INR.
        # But for this dashboard's aesthetics, we'll try to keep it looking 'Master Control' style.
        # However, it must not be 0.00. 
        # Let's use a simpler formatting for the demo data.
        def format_currency(val):
            if val >= 10000000:
                return f"₹{(val/10000000):.2f} Cr"
            elif val >= 100000:
                return f"₹{(val/100000):.2f} L"
            else:
                return f"₹{val:,.2f}"

        return {
            "total_mtd": format_currency(total_mtd), 
            "pending_settlements": format_currency(outstanding),
            "failed_24h": overdue_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/admin/billing/bills")
def get_all_bills():
    """Returns the full list of bills."""
    try:
        cursor = db['Bills'].find().sort("bill_date", -1)
        bills = []
        for b in cursor:
            b['_id'] = str(b['_id'])
            bills.append(b)
        return bills
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===========================================================
# when user calling / employee calling boss or agnets bot /
@app.websocket("/BetaVoltHome/")
async def nimi_emp(websocket: WebSocket):
    await websocket.accept()

    source = websocket.query_params.get("source") or "NativeApp"
    customer_id = websocket.query_params.get("customer_id") or "cust-123"

    # 2. Initialize the Agent
    agent = LiveAgent(source=source, customer_id=customer_id)

    # 3. Start the Agent in the BACKGROUND (Non-blocking)
    # This ensures the code below continues to run!
    agent_task = asyncio.create_task(agent.run())
    await asyncio.sleep(1)
    await agent.send_text("User is Conncted Say or Namaste and Say Hi I am BetaVolt By Intellismart developed By ADROIT SDVC. only once in hindi (Continue Converstation in hindi By default): message by system")
    # 4. Define the Browser Reader (Browser -> Agent)
    async def receive_from_browser():
        try:
            while True:
                # We assume the browser sends JSON: {"type": "audio", "data": "BASE64..."}
                message = await websocket.receive_json()
                
                if message.get("type") == "audio":
                    b64_data = message.get("data")
                    if b64_data:
                        # Decode Base64 to Raw Bytes for Gemini
                        audio_bytes = base64.b64decode(b64_data)
                        await agent.send_audio(audio_bytes)
                        
                elif message.get("type") == "text":
                    # Handle text chat if needed
                    await agent.send_text(message.get("data"))
                    
        except WebSocketDisconnect:
            print(f"⚠️ Browser disconnected")
        except Exception as e:
            print(f"❌ Error receiving from browser: {e}")

    # 5. Define the Browser Writer (Agent -> Browser)
    async def send_to_browser():
        try:
            while True:
                output = await agent.output_queue.get()

                # --- START CHANGE ---
                if output.get("type") == "close":
                    print(f"🛑 Escalation triggered. ")
                    await websocket.close() # <--- This kills the connection instantly
                    return 
                # --- END CHANGE ---

                elif output.get("type") == "empid_call_escalation":
                    # Send the specific JSON payload directly to the client
                    payload = output.get("data")
                    print(f"📤 Sending Web Escalation JSON: {payload}")
                    await websocket.send_json(payload)
                    
                    # Optional: Close the socket immediately after sending signal
                    # await websocket.close() 
                    # return

                elif output.get("type") == "device_signal":
                    # This sends the device control JSON to the frontend
                    payload = output.get("data")
                    print(f"🔌 Sending Device Control JSON to Frontend: {payload}")
                    # You can wrap it in a specific structure if your frontend expects it
                    await websocket.send_json({
                        "type": "DEVICE_CONTROL",
                        "payload": payload
                    })

                    
                await websocket.send_json(output)

                

        except Exception as e:
            print(f"❌ Error sending to browser: {e}")
    try:
        await asyncio.gather(
            agent_task,
            receive_from_browser(),
            send_to_browser()
        )
    except Exception as e:
        print(f"Session Error: {e}")
    finally:
        # Cleanup: If browser disconnects, stop the agent
        agent_task.cancel()
        print(f"🛑 Session ended")



@app.websocket("/BetaVoltSupport/")
async def BetaVoltSupportfun(websocket: WebSocket):
    await websocket.accept()

    source = websocket.query_params.get("source") or "NativeApp"

    # 2. Initialize the Agent
    agent = BetaVoltSupport(source=source)

    # 3. Start the Agent in the BACKGROUND (Non-blocking)
    # This ensures the code below continues to run!
    agent_task = asyncio.create_task(agent.run())
    await asyncio.sleep(0.5)
    await agent.send_text("User is Conncted Say or Namaste only once in hindi (Continue Converstation in hindi By default): message by system (Say hello)")
    # 4. Define the Browser Reader (Browser -> Agent)
    async def receive_from_browser():
        try:
            while True:
                # We assume the browser sends JSON: {"type": "audio", "data": "BASE64..."}
                message = await websocket.receive_json()
                
                if message.get("type") == "audio":
                    b64_data = message.get("data")
                    if b64_data:
                        # Decode Base64 to Raw Bytes for Gemini
                        audio_bytes = base64.b64decode(b64_data)
                        await agent.send_audio(audio_bytes)
                        
                elif message.get("type") == "text":
                    # Handle text chat if needed
                    await agent.send_text(message.get("data"))
                    
        except WebSocketDisconnect:
            print(f"⚠️ Browser disconnected")
        except Exception as e:
            print(f"❌ Error receiving from browser: {e}")

    # 5. Define the Browser Writer (Agent -> Browser)
    async def send_to_browser():
        try:
            while True:
                output = await agent.output_queue.get()

                # --- START CHANGE ---
                if output.get("type") == "close":
                    print(f"🛑 Escalation triggered. ")
                    await websocket.close() # <--- This kills the connection instantly
                    return 
                # --- END CHANGE ---

                elif output.get("type") == "empid_call_escalation":
                    # Send the specific JSON payload directly to the client
                    payload = output.get("data")
                    print(f"📤 Sending Web Escalation JSON: {payload}")
                    await websocket.send_json(payload)
                    
                    # Optional: Close the socket immediately after sending signal
                    # await websocket.close() 
                    # return

                elif output.get("type") == "device_signal":
                    # This sends the device control JSON to the frontend
                    payload = output.get("data")
                    print(f"🔌 Sending Device Control JSON to Frontend: {payload}")
                    # You can wrap it in a specific structure if your frontend expects it
                    await websocket.send_json({
                        "type": "DEVICE_CONTROL",
                        "payload": payload
                    })

                    
                await websocket.send_json(output)

                

        except Exception as e:
            print(f"❌ Error sending to browser: {e}")
    try:
        await asyncio.gather(
            agent_task,
            receive_from_browser(),
            send_to_browser()
        )
    except Exception as e:
        print(f"Session Error: {e}")
    finally:
        # Cleanup: If browser disconnects, stop the agent
        agent_task.cancel()
        print(f"🛑 Session ended")


@app.websocket("/BetaVoltHome/")
async def nimi_emp(websocket: WebSocket):
    await websocket.accept()

    source = websocket.query_params.get("source") or "NativeApp"

    # 2. Initialize the Agent
    agent = AgentTarrif(source=source)

    # 3. Start the Agent in the BACKGROUND (Non-blocking)
    # This ensures the code below continues to run!
    agent_task = asyncio.create_task(agent.run())
    await asyncio.sleep(0.5)
    await agent.send_text("Current;y tarrif is So high Due to that we need to swtch off some devices {take the name of the any of the device which consuming more and ask for the permission}")
    # 4. Define the Browser Reader (Browser -> Agent)
    async def receive_from_browser():
        try:
            while True:
                # We assume the browser sends JSON: {"type": "audio", "data": "BASE64..."}
                message = await websocket.receive_json()
                
                if message.get("type") == "audio":
                    b64_data = message.get("data")
                    if b64_data:
                        # Decode Base64 to Raw Bytes for Gemini
                        audio_bytes = base64.b64decode(b64_data)
                        await agent.send_audio(audio_bytes)
                        
                elif message.get("type") == "text":
                    # Handle text chat if needed
                    await agent.send_text(message.get("data"))
                    
        except WebSocketDisconnect:
            print(f"⚠️ Browser disconnected")
        except Exception as e:
            print(f"❌ Error receiving from browser: {e}")

    # 5. Define the Browser Writer (Agent -> Browser)
    async def send_to_browser():
        try:
            while True:
                output = await agent.output_queue.get()

                # --- START CHANGE ---
                if output.get("type") == "close":
                    print(f"🛑 Escalation triggered. ")
                    await websocket.close() # <--- This kills the connection instantly
                    return 
                # --- END CHANGE ---

                elif output.get("type") == "empid_call_escalation":
                    # Send the specific JSON payload directly to the client
                    payload = output.get("data")
                    print(f"📤 Sending Web Escalation JSON: {payload}")
                    await websocket.send_json(payload)
                    
                    # Optional: Close the socket immediately after sending signal
                    # await websocket.close() 
                    # return

                elif output.get("type") == "device_signal":
                    # This sends the device control JSON to the frontend
                    payload = output.get("data")
                    print(f"🔌 Sending Device Control JSON to Frontend: {payload}")
                    # You can wrap it in a specific structure if your frontend expects it
                    await websocket.send_json({
                        "type": "DEVICE_CONTROL",
                        "payload": payload
                    })

                    
                await websocket.send_json(output)

                

        except Exception as e:
            print(f"❌ Error sending to browser: {e}")
    try:
        await asyncio.gather(
            agent_task,
            receive_from_browser(),
            send_to_browser()
        )
    except Exception as e:
        print(f"Session Error: {e}")
    finally:
        # Cleanup: If browser disconnects, stop the agent
        agent_task.cancel()
        print(f"🛑 Session ended")




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)