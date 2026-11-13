from flask import Flask, jsonify, request

app = Flask(__name__)


# Simulated event model
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
        }


# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop"),
]


def find_event(event_id):
    """Return the event matching the supplied ID, or None if not found."""
    for event in events:
        if event.id == event_id:
            return event

    return None


@app.route("/", methods=["GET"])
def home():
    """Return a welcome message for the API."""
    return jsonify(
        {
            "message": "Welcome to the Event Management API"
        }
    ), 200


@app.route("/events", methods=["GET"])
def get_events():
    """Return all currently stored events."""
    return jsonify(
        [event.to_dict() for event in events]
    ), 200


@app.route("/events/<int:event_id>", methods=["GET"])
def get_event(event_id):
    """Return one event by ID."""
    event = find_event(event_id)

    if event is None:
        return jsonify(
            {
                "error": "Event not found"
            }
        ), 404

    return jsonify(event.to_dict()), 200


@app.route("/events", methods=["POST"])
def create_event():
    """Create a new event from JSON input."""
    data = request.get_json(silent=True)

    if not data:
        return jsonify(
            {
                "error": "Request body must contain JSON data"
            }
        ), 400

    title = data.get("title")

    if not isinstance(title, str) or not title.strip():
        return jsonify(
            {
                "error": "Title is required"
            }
        ), 400

    # Generate the next available event ID.
    next_id = max(
        (event.id for event in events),
        default=0,
    ) + 1

    new_event = Event(
        next_id,
        title.strip(),
    )

    events.append(new_event)

    return jsonify(new_event.to_dict()), 201


@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    """Update the title of an existing event."""
    event = find_event(event_id)

    if event is None:
        return jsonify(
            {
                "error": "Event not found"
            }
        ), 404

    data = request.get_json(silent=True)

    if not data:
        return jsonify(
            {
                "error": "Request body must contain JSON data"
            }
        ), 400

    title = data.get("title")

    if not isinstance(title, str) or not title.strip():
        return jsonify(
            {
                "error": "Title is required"
            }
        ), 400

    event.title = title.strip()

    return jsonify(event.to_dict()), 200


@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    """Remove an existing event."""
    event = find_event(event_id)

    if event is None:
        return jsonify(
            {
                "error": "Event not found"
            }
        ), 404

    events.remove(event)

    return "", 204


if __name__ == "__main__":
    app.run(debug=True)