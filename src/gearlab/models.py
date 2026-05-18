"""
GearLab core data model (E01-S2).
All data structures defined in spec §6.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


# ── Enumerations ─────────────────────────────────────────────────────────────

class GearType(str, Enum):
    SPUR      = "spur"
    RING      = "ring"
    RACK      = "rack"
    PULLEY    = "pulley"
    SPROCKET  = "sprocket"
    IDLER     = "idler"


class DefectType(str, Enum):
    MISSING = "missing"
    CHIPPED = "chipped"
    WORN    = "worn"


class ConnectionType(str, Enum):
    MESH  = "mesh"
    BELT  = "belt"
    CHAIN = "chain"
    RACK  = "rack"


class Direction(str, Enum):
    CW  = "CW"
    CCW = "CCW"


class PuzzleDifficulty(str, Enum):
    EASY   = "easy"
    MEDIUM = "medium"
    HARD   = "hard"
    EXPERT = "expert"


# ── §6.2  ToothDefect ────────────────────────────────────────────────────────

@dataclass
class ToothDefect:
    tooth_index: int
    defect_type: DefectType

    def to_dict(self) -> dict:
        return {"tooth_index": self.tooth_index,
                "defect_type": self.defect_type.value}

    @classmethod
    def from_dict(cls, d: dict) -> "ToothDefect":
        return cls(tooth_index=d["tooth_index"],
                   defect_type=DefectType(d["defect_type"]))


# ── §6.1  Gear ───────────────────────────────────────────────────────────────

@dataclass
class Gear:
    gear_type: GearType
    tooth_count: int
    module: float
    position: tuple[float, float]
    id: uuid.UUID             = field(default_factory=uuid.uuid4)
    is_driver: bool           = False
    rpm: float                = 0.0
    defects: list[ToothDefect] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "id":          str(self.id),
            "gear_type":   self.gear_type.value,
            "tooth_count": self.tooth_count,
            "module":      self.module,
            "position":    list(self.position),
            "is_driver":   self.is_driver,
            "rpm":         self.rpm,
            "defects":     [d.to_dict() for d in self.defects],
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Gear":
        return cls(
            id          = uuid.UUID(d["id"]),
            gear_type   = GearType(d["gear_type"]),
            tooth_count = d["tooth_count"],
            module      = d["module"],
            position    = tuple(d["position"]),
            is_driver   = d.get("is_driver", False),
            rpm         = d.get("rpm", 0.0),
            defects     = [ToothDefect.from_dict(x) for x in d.get("defects", [])],
        )


# ── §6.3  Connection ─────────────────────────────────────────────────────────

@dataclass
class Connection:
    conn_type:  ConnectionType
    element_a:  uuid.UUID
    element_b:  uuid.UUID
    id:         uuid.UUID = field(default_factory=uuid.uuid4)
    crossed:    bool      = False

    def to_dict(self) -> dict:
        return {
            "id":        str(self.id),
            "conn_type": self.conn_type.value,
            "element_a": str(self.element_a),
            "element_b": str(self.element_b),
            "crossed":   self.crossed,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Connection":
        return cls(
            id        = uuid.UUID(d["id"]),
            conn_type = ConnectionType(d["conn_type"]),
            element_a = uuid.UUID(d["element_a"]),
            element_b = uuid.UUID(d["element_b"]),
            crossed   = d.get("crossed", False),
        )


# ── §6.4  GearSystem ─────────────────────────────────────────────────────────

@dataclass
class GearSystem:
    elements:         list[Gear]
    connections:      list[Connection]
    driver_rpm:       float
    driver_direction: Direction

    def to_dict(self) -> dict:
        return {
            "elements":         [g.to_dict() for g in self.elements],
            "connections":      [c.to_dict() for c in self.connections],
            "driver_rpm":       self.driver_rpm,
            "driver_direction": self.driver_direction.value,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "GearSystem":
        return cls(
            elements         = [Gear.from_dict(g) for g in d["elements"]],
            connections      = [Connection.from_dict(c) for c in d["connections"]],
            driver_rpm       = d["driver_rpm"],
            driver_direction = Direction(d["driver_direction"]),
        )


# ── §6.5  PuzzleFile ─────────────────────────────────────────────────────────

@dataclass
class GoalSpec:
    """Minimum goal descriptor — extended in E07 (Puzzle Engine)."""
    target_ratio: Optional[float] = None
    extra: dict = field(default_factory=dict)


@dataclass
class PuzzleFile:
    title:              str
    description:        str
    difficulty:         PuzzleDifficulty
    initial_state:      GearSystem
    goal:               GoalSpec
    hints:              list[str]
    locked_element_ids: list[uuid.UUID]
    research:           Optional[dict[str, Any]] = None


# ── §6.6  SessionLog + EventRecord ───────────────────────────────────────────

@dataclass
class EventRecord:
    timestamp_ms: int
    event_type:   str
    puzzle_id:    Optional[str]
    payload:      dict[str, Any]


@dataclass
class SessionLog:
    schema_version: str
    participant_id: str
    session_id:     uuid.UUID
    events:         list[EventRecord]
