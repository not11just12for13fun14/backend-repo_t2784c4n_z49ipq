import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import db, create_document, get_documents
from schemas import Player, Friend, InventoryItem, Weapon, Vehicle, GameMap, Match

app = FastAPI(title="Battle Royale Prototype API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "service": "battle-royale-api"}


@app.get("/schema")
def get_schema():
    # Expose simple schema info for the frontend (viewer)
    return {
        "collections": [
            "player", "friend", "inventoryitem", "weapon", "vehicle", "gamemap", "match"
        ]
    }


# Players
@app.post("/players", response_model=dict)
async def create_player(player: Player):
    res = await create_document("player", player.dict())
    return {"inserted_id": str(res)}


@app.get("/players", response_model=List[dict])
async def list_players(limit: int = 50):
    docs = await get_documents("player", {}, limit)
    return docs


# Friends
@app.post("/friends", response_model=dict)
async def add_friend(friend: Friend):
    res = await create_document("friend", friend.dict())
    return {"inserted_id": str(res)}


@app.get("/friends/{player_id}")
async def list_friends(player_id: str, limit: int = 100):
    docs = await get_documents("friend", {"player_id": player_id, "status": "accepted"}, limit)
    return docs


# Inventory
@app.post("/inventory", response_model=dict)
async def add_inventory_item(item: InventoryItem):
    res = await create_document("inventoryitem", item.dict())
    return {"inserted_id": str(res)}


@app.get("/inventory/{player_id}")
async def list_inventory(player_id: str, limit: int = 100):
    docs = await get_documents("inventoryitem", {"player_id": player_id}, limit)
    return docs


# Weapons (catalog)
@app.post("/weapons", response_model=dict)
async def create_weapon(weapon: Weapon):
    res = await create_document("weapon", weapon.dict())
    return {"inserted_id": str(res)}


@app.get("/weapons")
async def list_weapons(limit: int = 100):
    docs = await get_documents("weapon", {}, limit)
    return docs


# Vehicles (catalog)
@app.post("/vehicles", response_model=dict)
async def create_vehicle(vehicle: Vehicle):
    res = await create_document("vehicle", vehicle.dict())
    return {"inserted_id": str(res)}


@app.get("/vehicles")
async def list_vehicles(limit: int = 100):
    docs = await get_documents("vehicle", {}, limit)
    return docs


# Maps (catalog)
@app.post("/maps", response_model=dict)
async def create_map(map_: GameMap):
    res = await create_document("gamemap", map_.dict())
    return {"inserted_id": str(res)}


@app.get("/maps")
async def list_maps(limit: int = 50):
    docs = await get_documents("gamemap", {}, limit)
    return docs


# Matchmaking (prototype only - not real-time)
class CreateMatchRequest(BaseModel):
    map_id: str
    mode: str
    max_players: int = 50


@app.post("/matches", response_model=dict)
async def create_match(payload: CreateMatchRequest):
    match = Match(
        match_id=os.urandom(8).hex(),
        map_id=payload.map_id,
        mode=payload.mode,  # type: ignore
        max_players=payload.max_players,
        players=[],
        safe_zone_shrink_rate=1.0,
    )
    res = await create_document("match", match.dict())
    return {"match_id": match.match_id, "inserted_id": str(res)}


@app.get("/matches")
async def list_matches(limit: int = 20):
    docs = await get_documents("match", {}, limit)
    return docs


# Health endpoint
@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
    }
    try:
        collections = db.list_collection_names() if db else []
        response["database"] = "✅ Connected" if collections is not None else "❌ Not Connected"
        response["collections"] = collections
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
