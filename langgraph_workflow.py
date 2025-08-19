from langgraph.graph import StateGraph, END
from typing import TypedDict, List
from models import UserPreferences, Destination, ItineraryItem, TripPlan
from api_integrations import SkyscannerAPI, GoogleMapsAPI, TripAdvisorAPI
from optimizer import TravelOptimizer

class TravelState(TypedDict):
    preferences: UserPreferences
    destinations: List[Destination]
    itinerary: List[ItineraryItem]
    total_cost: float
    cost_breakdown: dict

class TravelPlanner:
    def __init__(self):
        self.skyscanner = SkyscannerAPI()
        self.google_maps = GoogleMapsAPI()
        self.tripadvisor = TripAdvisorAPI()
        self.optimizer = TravelOptimizer()
        self.graph = self._build_graph()

    async def suggest_destinations(self, state: TravelState) -> TravelState:
        # Mock Generative AI call (replace with actual API)
        preferences = state["preferences"]
        destinations = [
            Destination(name="Paris", country="France", description="Cultural hub", estimated_cost=1000),
            Destination(name="Tokyo", country="Japan", description="Vibrant city", estimated_cost=1200),
        ]
        state["destinations"] = destinations
        return state

    async def generate_itinerary(self, state: TravelState) -> TravelState:
        itinerary = []
        for dest in state["destinations"]:
            activities = await self.tripadvisor.get_activities(dest.name, state["preferences"].interests)
            for i, activity in enumerate(activities[:2], 1):  # Limit to 2 activities per destination
                itinerary.append(ItineraryItem(day=i, activity=activity["name"], location=dest.name, cost=activity["cost"]))
        state["itinerary"] = itinerary
        return state

    async def optimize_plan(self, state: TravelState) -> TravelState:
        destinations, itinerary, cost_info = self.optimizer.optimize_budget(
            state["preferences"].budget, state["destinations"], state["itinerary"]
        )
        state["destinations"] = destinations
        state["itinerary"] = itinerary
        state["total_cost"] = cost_info["total_cost"]
        state["cost_breakdown"] = {
            "flights": sum(d.estimated_cost for d in destinations) * 0.5,
            "hotels": sum(d.estimated_cost for d in destinations) * 0.3,
            "activities": sum(i.cost for i in itinerary)
        }
        return state

    def _build_graph(self):
        workflow = StateGraph(TravelState)
        workflow.add_node("suggest_destinations", self.suggest_destinations)
        workflow.add_node("generate_itinerary", self.generate_itinerary)
        workflow.add_node("optimize_plan", self.optimize_plan)

        workflow.set_entry_point("suggest_destinations")
        workflow.add_edge("suggest_destinations", "generate_itinerary")
        workflow.add_edge("generate_itinerary", "optimize_plan")
        workflow.add_edge("optimize_plan", END)

        return workflow.compile()

    async def plan_trip(self, preferences: UserPreferences) -> TripPlan:
        state = await self.graph.ainvoke({
            "preferences": preferences,
            "destinations": [],
            "itinerary": [],
            "total_cost": 0,
            "cost_breakdown": {}
        })
        return TripPlan(
            destinations=state["destinations"],
            itinerary=state["itinerary"],
            total_cost=state["total_cost"],
            cost_breakdown=state["cost_breakdown"]
        )
