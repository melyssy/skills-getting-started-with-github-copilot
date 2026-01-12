import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def reset_activities(client):
    """Reset activities to their initial state after each test"""
    # Store initial state
    from app import activities as app_activities
    initial_state = {
        "Debate Team": {
            "description": "Develop public speaking and argumentation skills through competitive debate",
            "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participants": ["alex@mergington.edu"]
        },
        "Robotics Club": {
            "description": "Build and program robots for competitions",
            "schedule": "Mondays and Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["james@mergington.edu", "noah@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball training and games",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["marcus@mergington.edu"]
        },
        "Soccer Team": {
            "description": "Soccer practice and competitive matches",
            "schedule": "Mondays, Wednesdays, Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 22,
            "participants": ["lucas@mergington.edu", "avery@mergington.edu"]
        },
        "Drama Club": {
            "description": "Theater productions and acting workshops",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 25,
            "participants": ["isabella@mergington.edu"]
        },
        "Visual Arts": {
            "description": "Painting, drawing, and sculpture classes",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["ava@mergington.edu", "grace@mergington.edu"]
        },
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        }
    }
    
    yield client
    
    # Reset to initial state
    app_activities.clear()
    app_activities.update(initial_state)
