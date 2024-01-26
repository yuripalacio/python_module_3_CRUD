from flask import Flask, request, jsonify
from models.task import Task

app = Flask(__name__)

tasks = []
task_id_control = [1]

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    new_task = Task(
        id=task_id_control[0],
        title=data.get("title"),
        description=data.get("description", "")
    )
    tasks.append(new_task)
    task_id_control[0] += 1
    return jsonify(new_task.to_dict())

@app.route('/tasks', methods=['GET'])
def get_tasks():
    task_list = [task.to_dict() for task in tasks]
    output = {
        "tasks": task_list,
        "total": len(task_list)
    }

    return jsonify(output)

@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    for t in tasks:
        if t.id == id:
            return jsonify(t.to_dict())
        
    return jsonify({ "message": "ID not found" }), 404

@app.route('/tasks/<int:id>', methods=['POST'])
def update_task(id):
    task = None

    for t in tasks:
        if t.id == id:
            task = t
            break

    if task == None:
        return jsonify({ "message": "ID not found" }), 404
    
    data = request.get_json()

    if data.get('title'):
        task.title = data['title']
    if data.get('description'):
        task.description = data['description']
    if data.get('completed'):
        task.completed = data['completed']

    return jsonify(task.to_dict())

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete(id):
    for task in tasks:
        if task.id == id:
            tasks.remove(task)
            return jsonify({ "message": "Task deleted successfully" })

    return jsonify({ "message": "ID not found" }), 404

if __name__ == "__main__":
    app.run(debug=True)