from typing import List, Tuple
from models import Destination, ItineraryItem

class TravelOptimizer:
    def optimize_route(self, origin: str, destinations: List[Destination], google_maps_api):
        # Simple greedy algorithm for route optimization
        current = origin
        optimized_route = []
        total_distance = 0
        remaining = destinations.copy()

        while remaining:
            closest = min(remaining, key=lambda d: google_maps_api.get_route(current, d.name)["distance_km"])
            route_info = google_maps_api.get_route(current, closest.name)
            total_distance += route_info["distance_km"]
            optimized_route.append(closest)
            current = closest.name
            remaining.remove(closest)

        return optimized_route, total_distance

    def optimize_budget(self, budget: float, destinations: List[Destination], itinerary: List[ItineraryItem]):
        total_cost = sum(d.estimated_cost for d in destinations) + sum(i.cost for i in itinerary)
        if total_cost <= budget:
            return destinations, itinerary, {"status": "within_budget", "total_cost": total_cost}

        # Prune expensive items (simple greedy pruning)
        itinerary = sorted(itinerary, key=lambda x: x.cost, reverse=True)
        while total_cost > budget and itinerary:
            itinerary.pop(0)
            total_cost = sum(d.estimated_cost for d in destinations) + sum(i.cost for i in itinerary)

        return destinations, itinerary, {"status": "adjusted", "total_cost": total_cost}
