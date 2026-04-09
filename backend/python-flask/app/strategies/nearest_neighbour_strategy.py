from itertools import groupby
from app.strategies.route_strategy import RouteStrategy, build_route
from app.utils.haversine import calculate_distance


class NearestNeighbourStrategy(RouteStrategy):
    """
    NearestNeighbourStrategy — greedy nearest-neighbour heuristic.

    Matches are grouped by date. For each day, if there are multiple
    matches, we pick the one whose city is closest to our current position.
    This minimises total travel distance compared to a naive date-only sort.
    """

    def optimise(self, matches: list) -> dict:
        if not matches:
            return build_route([], 'nearest-neighbour')

        # Step 1: Sort all matches by kickoff date
        sorted_matches = sorted(matches, key=lambda m: m['kickoff'])

        # Step 2: Group matches by date (YYYY-MM-DD prefix)
        ordered_matches = []
        current_city = None

        groups = groupby(sorted_matches, key=lambda m: m['kickoff'].split('T')[0])

        for _date, group in groups:
            day_matches = list(group)

            if len(day_matches) == 1:
                # Only one match this day — no choice to make
                chosen = day_matches[0]
            else:
                if current_city is None:
                    # No current position yet, just pick the first
                    chosen = day_matches[0]
                else:
                    # Pick the match whose city is closest to current position
                    chosen = min(
                        day_matches,
                        key=lambda m: calculate_distance(
                            current_city['latitude'], current_city['longitude'],
                            m['city']['latitude'], m['city']['longitude']
                        )
                    )

            ordered_matches.append(chosen)
            current_city = chosen['city']

        return build_route(ordered_matches, 'nearest-neighbour')