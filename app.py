from flask import Flask, render_template, request, jsonify
from world import WumpusWorld
from logic import KnowledgeBase

app = Flask(__name__)

world = None
kb = None


@app.route("/")
def index():
    return render_template("indexe.html")


@app.route("/generate", methods=["POST"])
def generate():
    global world, kb

    data = request.json
    rows = int(data["rows"])
    cols = int(data["cols"])

    world = WumpusWorld(rows, cols)
    kb = KnowledgeBase(rows, cols)

    state = world.get_visible_grid()
    percepts = world.get_percepts(world.agent_pos)

    kb.tell(world.agent_pos, percepts)

    return jsonify({
        "grid": state,
        "percepts": percepts,
        "steps": kb.inference_steps
    })


@app.route("/move", methods=["POST"])
def move():
    global world, kb

    if not world:
        return jsonify({"error": "World not generated"}), 400

    moved = world.move_agent(kb)

    percepts = world.get_percepts(world.agent_pos)
    kb.tell(world.agent_pos, percepts)

    return jsonify({
        "grid": world.get_visible_grid(),
        "percepts": percepts,
        "steps": kb.inference_steps,
        "position": world.agent_pos,
        "status": moved
    })


if __name__ == "__main__":
    app.run(debug=True)
