"""
E01-S2 data model tests.
Covers: Gear, ToothDefect, Connection, GearSystem, PuzzleFile,
        SessionLog, EventRecord — all from spec §6.
"""
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
SRC  = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from gearlab.models import (
    Gear, GearType,
    ToothDefect, DefectType,
    Connection, ConnectionType,
    Direction, GearSystem,
    GoalSpec,
    PuzzleFile, PuzzleDifficulty,
    EventRecord, SessionLog,
)


# ── helpers ──────────────────────────────────────────────────────────────────

def make_gear(**kwargs) -> Gear:
    defaults = dict(gear_type=GearType.SPUR, tooth_count=20, module=1.0,
                    position=(0.0, 0.0))
    defaults.update(kwargs)
    return Gear(**defaults)


# ── E01-S2-01 : Gear ─────────────────────────────────────────────────────────

def test_gear_has_auto_uuid():
    g = make_gear()
    assert isinstance(g.id, uuid.UUID)


def test_gear_two_instances_have_different_ids():
    assert make_gear().id != make_gear().id


def test_gear_fields_stored_correctly():
    g = make_gear(tooth_count=12, module=2.5, position=(100.0, -50.0))
    assert g.tooth_count == 12
    assert g.module == 2.5
    assert g.position == (100.0, -50.0)


def test_gear_defaults():
    g = make_gear()
    assert g.rpm == 0.0
    assert g.is_driver is False
    assert g.defects == []


def test_gear_type_enum_values():
    valid = {GearType.SPUR, GearType.RING, GearType.RACK,
             GearType.PULLEY, GearType.SPROCKET, GearType.IDLER}
    assert len(valid) == 6


def test_gear_accepts_all_valid_types():
    for t in GearType:
        g = make_gear(gear_type=t)
        assert g.gear_type == t


def test_gear_defects_are_independent_per_instance():
    """Default mutable list must not be shared between instances."""
    g1 = make_gear()
    g2 = make_gear()
    g1.defects.append(ToothDefect(tooth_index=0, defect_type=DefectType.MISSING))
    assert g2.defects == []


# ── E01-S2-02 : ToothDefect ──────────────────────────────────────────────────

def test_tooth_defect_fields():
    d = ToothDefect(tooth_index=3, defect_type=DefectType.CHIPPED)
    assert d.tooth_index == 3
    assert d.defect_type == DefectType.CHIPPED


def test_defect_type_enum_values():
    valid = {DefectType.MISSING, DefectType.CHIPPED, DefectType.WORN}
    assert len(valid) == 3


def test_defect_attached_to_gear():
    g = make_gear()
    g.defects.append(ToothDefect(tooth_index=0, defect_type=DefectType.WORN))
    assert len(g.defects) == 1
    assert g.defects[0].defect_type == DefectType.WORN


# ── E01-S2-03 : Connection ───────────────────────────────────────────────────

def test_connection_has_auto_uuid():
    a, b = make_gear(), make_gear()
    c = Connection(conn_type=ConnectionType.MESH,
                   element_a=a.id, element_b=b.id)
    assert isinstance(c.id, uuid.UUID)


def test_connection_fields():
    a, b = make_gear(), make_gear()
    c = Connection(conn_type=ConnectionType.BELT,
                   element_a=a.id, element_b=b.id, crossed=True)
    assert c.conn_type == ConnectionType.BELT
    assert c.element_a == a.id
    assert c.element_b == b.id
    assert c.crossed is True


def test_connection_crossed_defaults_false():
    a, b = make_gear(), make_gear()
    c = Connection(conn_type=ConnectionType.CHAIN,
                   element_a=a.id, element_b=b.id)
    assert c.crossed is False


def test_connection_type_enum_values():
    valid = {ConnectionType.MESH, ConnectionType.BELT,
             ConnectionType.CHAIN, ConnectionType.RACK}
    assert len(valid) == 4


# ── E01-S2-04 : GearSystem ───────────────────────────────────────────────────

def test_gear_system_fields():
    g = make_gear(is_driver=True)
    sys_ = GearSystem(elements=[g], connections=[],
                      driver_rpm=100.0, driver_direction=Direction.CW)
    assert sys_.driver_rpm == 100.0
    assert sys_.driver_direction == Direction.CW
    assert g in sys_.elements
    assert sys_.connections == []


def test_direction_enum_values():
    assert {Direction.CW, Direction.CCW} == {Direction.CW, Direction.CCW}


def test_gear_system_serialise_roundtrip():
    """to_dict() / from_dict() must reconstruct an identical GearSystem."""
    g1 = make_gear(tooth_count=16, is_driver=True)
    g2 = make_gear(tooth_count=32)
    conn = Connection(conn_type=ConnectionType.MESH,
                      element_a=g1.id, element_b=g2.id)
    sys_ = GearSystem(elements=[g1, g2], connections=[conn],
                      driver_rpm=60.0, driver_direction=Direction.CCW)
    data = sys_.to_dict()
    sys2 = GearSystem.from_dict(data)

    assert len(sys2.elements) == 2
    assert len(sys2.connections) == 1
    assert sys2.driver_rpm == 60.0
    assert sys2.driver_direction == Direction.CCW
    assert sys2.elements[0].tooth_count == 16
    assert sys2.elements[1].tooth_count == 32
    assert sys2.connections[0].conn_type == ConnectionType.MESH


# ── E01-S2-06 : PuzzleFile ───────────────────────────────────────────────────

def test_puzzle_file_required_fields():
    g = make_gear(is_driver=True)
    initial = GearSystem(elements=[g], connections=[],
                         driver_rpm=60.0, driver_direction=Direction.CW)
    goal = GoalSpec(target_ratio=2.0)
    pf = PuzzleFile(title="Test Puzzle",
                    description="A simple test.",
                    difficulty=PuzzleDifficulty.EASY,
                    initial_state=initial,
                    goal=goal,
                    hints=["Try adding a gear."],
                    locked_element_ids=[])
    assert pf.title == "Test Puzzle"
    assert pf.difficulty == PuzzleDifficulty.EASY
    assert pf.research is None


def test_puzzle_difficulty_enum_values():
    valid = {PuzzleDifficulty.EASY, PuzzleDifficulty.MEDIUM,
             PuzzleDifficulty.HARD, PuzzleDifficulty.EXPERT}
    assert len(valid) == 4


def test_puzzle_file_researcher_metadata_optional():
    g = make_gear(is_driver=True)
    initial = GearSystem(elements=[g], connections=[],
                         driver_rpm=60.0, driver_direction=Direction.CW)
    goal = GoalSpec(target_ratio=3.0)
    pf = PuzzleFile(title="P", description="D",
                    difficulty=PuzzleDifficulty.HARD,
                    initial_state=initial, goal=goal,
                    hints=[], locked_element_ids=[],
                    research={"expected_difficulty_rating": 7.5,
                               "domain_prior_required": False,
                               "spatial_reasoning_type": "ratio",
                               "cognitive_load_notes": "moderate"})
    assert pf.research["expected_difficulty_rating"] == 7.5


# ── E01-S2-07 : SessionLog + EventRecord ─────────────────────────────────────

def test_event_record_fields():
    e = EventRecord(timestamp_ms=1500, event_type="gear_placed",
                    puzzle_id="p1", payload={"gear_id": "abc"})
    assert e.timestamp_ms == 1500
    assert e.event_type == "gear_placed"
    assert e.puzzle_id == "p1"
    assert e.payload["gear_id"] == "abc"


def test_event_record_puzzle_id_nullable():
    e = EventRecord(timestamp_ms=0, event_type="session_start",
                    puzzle_id=None, payload={})
    assert e.puzzle_id is None


def test_session_log_fields():
    sid = uuid.uuid4()
    log = SessionLog(schema_version="1.0", participant_id="P42",
                     session_id=sid, events=[])
    assert log.schema_version == "1.0"
    assert log.participant_id == "P42"
    assert log.session_id == sid
    assert log.events == []


def test_session_log_stores_events():
    e = EventRecord(timestamp_ms=200, event_type="hint_viewed",
                    puzzle_id="p2", payload={})
    log = SessionLog(schema_version="1.0", participant_id="P01",
                     session_id=uuid.uuid4(), events=[e])
    assert len(log.events) == 1
    assert log.events[0].event_type == "hint_viewed"
