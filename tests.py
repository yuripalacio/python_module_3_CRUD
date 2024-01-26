import pytest
import requests

BASE_URL = 'http://localhost:5000'
tasks = []

def test_create_task():
    new_task_data = {
        "title": "New task",
        "description": "New task description"
    }
    response = requests.post(f"{BASE_URL}/tasks", json=new_task_data)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json['title'] == new_task_data['title']
    tasks.append(response_json)

def test_get_tasks():
    response = requests.get(f"{BASE_URL}/tasks")
    assert response.status_code == 200
    response_json = response.json()
    assert "tasks" in response_json
    assert "total" in response_json

def test_get_task():
    task = tasks[0]
    response = requests.get(f"{BASE_URL}/tasks/{task['id']}")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json['title'] == task['title']

def test_update_task():
    update_task_data = {
        "title": "Title updated",
        "description": "Description updated"
    }
    task = tasks[0]
    response = requests.post(f"{BASE_URL}/tasks/{task['id']}", json=update_task_data)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json['title'] == update_task_data['title']
    assert response_json['description'] == update_task_data['description']

def test_delete_task():
    task = tasks[0]
    response = requests.delete(f"{BASE_URL}/tasks/{task['id']}")
    assert response.status_code == 200
    response_json = response.json()
    assert "message" in response_json
    assert response_json['message'] == "Task deleted successfully"
