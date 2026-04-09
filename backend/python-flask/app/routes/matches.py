from flask import Blueprint, jsonify, request
from app.models.match import Match

matches_bp = Blueprint('matches', __name__)

# ============================================================
#  Matches Routes — YOUR TASK #2
#
#  Implement the REST endpoints for matches.
# ============================================================


# ============================================================
#  GET /api/matches — Return matches with optional filters
# ============================================================
#
# TODO: Implement this endpoint (YOUR TASK #2)
#
# Query parameters (both optional):
#   ?city=city-atlanta    → filter by city ID
#   ?date=2026-06-14      → filter by date (YYYY-MM-DD)
#
# Hint: Use request.args.get() to extract optional query parameters.
# Use Match.query with filter_by() or filter() to apply filters.
# Order results by kickoff and convert to dicts using match.to_dict()
#
# ============================================================

@matches_bp.route('', methods=['GET'])
def get_matches():
    # TODO: Replace with your implementation (YOUR TASK #2)
    city = request.args.get('city')
    date = request.args.get('date')

    query = Match.query

    if city:
        query = query.filter(Match.city_id == city)

    if date:
        query = query.filter(Match.kickoff.like(f'{date}%'))

    matches = query.order_by(Match.kickoff).all()
    return jsonify([match.to_dict() for match in matches]), 200


# ============================================================
#  GET /api/matches/<id> — Return a single match by ID
# ============================================================
#
# TODO: Implement this endpoint (YOUR TASK #2)
#
# Hint: Use Match.query.get(id) — returns None if not found.
# Return 404 with an error message if not found.
#
# ============================================================

@matches_bp.route('/<id>', methods=['GET'])
def get_match_by_id(id):
    match = Match.query.get(id)

    if not match:
        return jsonify({'error': 'Match not found'}), 404

    return jsonify(match.to_dict()), 200
