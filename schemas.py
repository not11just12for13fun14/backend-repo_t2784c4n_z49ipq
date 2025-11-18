"""
Database Schemas for Battle Royale Prototype

Each Pydantic model represents a MongoDB collection.
Collection name is the lowercase of the class name.
"""
from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class Player(BaseModel):
    player_id: str = Field(..., description="Unique player identifier")
    username: str = Field(..., description="Display name")
    avatar_url: Optional[str] = Field(None, description="Avatar image URL")
    level: int = Field(1, ge=1, description="Player level")
    xp: int = Field(0, ge=0, description="Experience points")
    coins: int = Field(0, ge=0, description="Soft currency")


class Friend(BaseModel):
    player_id: str = Field(..., description="Owner player id")
    friend_id: str = Field(..., description="Friend player id")
    status: Literal["pending", "accepted", "blocked"] = Field("accepted")


class InventoryItem(BaseModel):
    player_id: str = Field(..., description="Owner player id")
    item_id: str = Field(..., description="Item id")
    type: Literal["weapon", "armor", "medkit", "grenade", "vehicle", "cosmetic"]
    name: str
    rarity: Literal["common", "rare", "epic", "legendary"] = "common"
    quantity: int = Field(1, ge=0)
    meta: Optional[dict] = None


class Weapon(BaseModel):
    weapon_id: str
    name: str
    damage: int = Field(..., ge=0)
    fire_rate: float = Field(..., ge=0)
    accuracy: float = Field(..., ge=0, le=1)
    ammo_type: Literal["AR", "SMG", "SR", "SHOTGUN", "LMG", "PISTOL"]


class Vehicle(BaseModel):
    vehicle_id: str
    name: str
    speed: int = Field(..., ge=0)
    seats: int = Field(..., ge=1)


class GameMap(BaseModel):
    map_id: str
    name: str
    size: Literal["small", "medium", "large"]
    theme: Literal["desert", "urban", "forest", "futuristic"]


class Match(BaseModel):
    match_id: str
    map_id: str
    mode: Literal["solo", "duo", "squad"]
    max_players: int = Field(..., ge=10, le=50)
    players: List[str] = []
    safe_zone_shrink_rate: float = Field(1.0, gt=0)
    status: Literal["waiting", "loading", "in-progress", "completed"] = "waiting"
    winner_id: Optional[str] = None

