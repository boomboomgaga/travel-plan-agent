from fastapi import FastAPI
from models import UserPreferences, TripPlan
from langgraph_workflow import TravelPlanner

app = FastAPI(title="Smart Travel Planner")
planner = TravelPlanner()

@app.post("/plan_trip", response_model=TripPlan)
async def plan_trip(preferences: UserPreferences):
    return await planner.plan_trip(preferences)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
