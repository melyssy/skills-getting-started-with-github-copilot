import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app


class TestActivitiesEndpoint:
    """Tests for GET /activities endpoint"""

    def test_get_activities_success(self, reset_activities):
        """Test that we can fetch all activities"""
        response = reset_activities.get("/activities")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, dict)
        assert "Debate Team" in data
        assert "Robotics Club" in data
        assert "Basketball Team" in data
        assert "Soccer Team" in data
        assert "Drama Club" in data
        assert "Visual Arts" in data
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Gym Class" in data

    def test_activity_structure(self, reset_activities):
        """Test that each activity has the correct structure"""
        response = reset_activities.get("/activities")
        data = response.json()
        
        activity = data["Debate Team"]
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
        assert isinstance(activity["participants"], list)

    def test_activity_has_initial_participants(self, reset_activities):
        """Test that activities have their initial participants"""
        response = reset_activities.get("/activities")
        data = response.json()
        
        assert "alex@mergington.edu" in data["Debate Team"]["participants"]
        assert len(data["Robotics Club"]["participants"]) == 2


class TestSignupEndpoint:
    """Tests for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_success(self, reset_activities):
        """Test successful signup for an activity"""
        response = reset_activities.post(
            "/activities/Debate Team/signup?email=newstudent@mergington.edu"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "newstudent@mergington.edu" in data["message"]

    def test_signup_adds_participant(self, reset_activities):
        """Test that signup actually adds the participant"""
        # Sign up
        reset_activities.post(
            "/activities/Debate Team/signup?email=newstudent@mergington.edu"
        )
        
        # Verify participant was added
        response = reset_activities.get("/activities")
        participants = response.json()["Debate Team"]["participants"]
        assert "newstudent@mergington.edu" in participants

    def test_signup_nonexistent_activity(self, reset_activities):
        """Test signup to a non-existent activity"""
        response = reset_activities.post(
            "/activities/Nonexistent Activity/signup?email=student@mergington.edu"
        )
        
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_signup_already_registered(self, reset_activities):
        """Test that a student cannot sign up twice"""
        # First signup
        response1 = reset_activities.post(
            "/activities/Debate Team/signup?email=alex@mergington.edu"
        )
        
        # Alex is already registered, should fail
        assert response1.status_code == 400
        data = response1.json()
        assert "already signed up" in data["detail"]

    def test_signup_multiple_activities(self, reset_activities):
        """Test that a student can signup for multiple activities"""
        email = "versatile@mergington.edu"
        
        # Sign up for first activity
        response1 = reset_activities.post(
            f"/activities/Debate Team/signup?email={email}"
        )
        assert response1.status_code == 200
        
        # Sign up for second activity
        response2 = reset_activities.post(
            f"/activities/Robotics Club/signup?email={email}"
        )
        assert response2.status_code == 200
        
        # Verify both signups
        response = reset_activities.get("/activities")
        data = response.json()
        assert email in data["Debate Team"]["participants"]
        assert email in data["Robotics Club"]["participants"]


class TestUnregisterEndpoint:
    """Tests for POST /activities/{activity_name}/unregister endpoint"""

    def test_unregister_success(self, reset_activities):
        """Test successful unregister from an activity"""
        response = reset_activities.post(
            "/activities/Debate Team/unregister?email=alex@mergington.edu"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "alex@mergington.edu" in data["message"]

    def test_unregister_removes_participant(self, reset_activities):
        """Test that unregister actually removes the participant"""
        # Unregister
        reset_activities.post(
            "/activities/Debate Team/unregister?email=alex@mergington.edu"
        )
        
        # Verify participant was removed
        response = reset_activities.get("/activities")
        participants = response.json()["Debate Team"]["participants"]
        assert "alex@mergington.edu" not in participants

    def test_unregister_nonexistent_activity(self, reset_activities):
        """Test unregister from a non-existent activity"""
        response = reset_activities.post(
            "/activities/Nonexistent Activity/unregister?email=student@mergington.edu"
        )
        
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_unregister_not_registered(self, reset_activities):
        """Test unregister when student is not registered"""
        response = reset_activities.post(
            "/activities/Debate Team/unregister?email=notregistered@mergington.edu"
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "not registered" in data["detail"]

    def test_signup_then_unregister(self, reset_activities):
        """Test signing up and then unregistering"""
        email = "testuser@mergington.edu"
        
        # Sign up
        response1 = reset_activities.post(
            f"/activities/Debate Team/signup?email={email}"
        )
        assert response1.status_code == 200
        
        # Verify signup
        response = reset_activities.get("/activities")
        assert email in response.json()["Debate Team"]["participants"]
        
        # Unregister
        response2 = reset_activities.post(
            f"/activities/Debate Team/unregister?email={email}"
        )
        assert response2.status_code == 200
        
        # Verify unregister
        response = reset_activities.get("/activities")
        assert email not in response.json()["Debate Team"]["participants"]


class TestRootEndpoint:
    """Tests for GET / endpoint"""

    def test_root_redirect(self, reset_activities):
        """Test that root redirects to /static/index.html"""
        response = reset_activities.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert "/static/index.html" in response.headers["location"]
