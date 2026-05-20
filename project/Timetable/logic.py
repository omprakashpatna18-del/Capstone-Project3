from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
import uvicorn
import random

router = APIRouter()

# Jinja2 templates setup (assuming aapki HTML files 'templates' folder mein hain)
templates = Jinja2Templates(directory="templates")

# LOGIC
def generate_timetable(data):

    def to_min(t):
        try:
            h, m = map(int, t.split(":"))
            return h * 60 + m
        except:
            return None

    def format_time(m):
        return f"{m//60:02d}:{m%60:02d}"

    def clean(arr):
        return [s.strip().lower() for s in arr if s.strip()]

    days = int(data["days"])

    subjects = clean(data["subjects"].split(","))
    weak = clean(data["weak"].split(","))
    strong = clean(data["strong"].split(","))

    if not subjects:
        subjects = ["general study"]

    if not weak:
        weak = subjects.copy()

    if not strong:
        strong = subjects.copy()

    strong = [s for s in strong if s not in weak]
    normal = [s for s in subjects if s not in weak and s not in strong]

    if not normal:
        normal = subjects.copy()

    start = to_min(data["start"]) or 480
    base_duration = int(data["duration"])
    break_after = int(data["break_after"])
    base_break = int(data["break_duration"])
    study_minutes_goal = int(data["study_hours"]) * 60
    break_minutes_goal = int(data["break_hours"]) * 60

    meals = {
        "Breakfast": (to_min(data["b_start"]), to_min(data["b_end"])),
        "Lunch": (to_min(data["l_start"]), to_min(data["l_end"])),
        "Dinner": (to_min(data["d_start"]), to_min(data["d_end"]))
    }

    output = []

    def pick_subject():
        r = random.random()

        if r < 0.5:
            return random.choice(weak)
        elif r < 0.8:
            return random.choice(normal)

        return random.choice(strong)

    for d in range(1, days + 1):
        output.append(f"DAY {d}")

        current = start
        end_day = start + 1440

        session_count = 0
        meal_done = {k: False for k in meals}
        total_study_done = 0
        total_break_done = 0

        while current < end_day:

            if (
                total_study_done >= study_minutes_goal
                and total_break_done >= break_minutes_goal
            ):
                break

            # MEALS 
            for name, (s, e) in meals.items():
                if (
                    s is not None
                    and not meal_done[name]
                    and s <= current < e
                ):
                    output.append(
                        f"{name}: {format_time(current)} - {format_time(e)}"
                    )
                    current = e
                    meal_done[name] = True

            # STUDY
            if total_study_done < study_minutes_goal:

                subject = pick_subject()
                duration = base_duration

                if subject in weak:
                    duration += 15
                elif subject in strong:
                    duration -= 10

                duration = max(
                    25,
                    min(duration, study_minutes_goal - total_study_done)
                )

                # if study would cross a meal
                meal_interrupted = False

                for name, (s, e) in meals.items():

                    if (
                        s is not None
                        and not meal_done[name]
                        and current < s < current + duration
                    ):
                        output.append(
                            f"{subject.title()}: {format_time(current)} - {format_time(s)}"
                        )

                        total_study_done += (s - current)
                        current = s

                        output.append(
                            f"{name}: {format_time(current)} - {format_time(e)}"
                        )

                        current = e
                        meal_done[name] = True

                        session_count += 1
                        meal_interrupted = True
                        break

                if meal_interrupted:
                    continue

                output.append(
                    f"{subject.title()}: {format_time(current)} - {format_time(current + duration)}"
                )

                current += duration
                total_study_done += duration
                session_count += 1

                if session_count >= break_after:
                    b = min(
                        base_break,
                        break_minutes_goal - total_break_done
                    )

                    output.append(
                        f"Break: {format_time(current)} - {format_time(current + b)}"
                    )

                    current += b
                    total_break_done += b
                    session_count = 0

        output.append(f"Summary: {total_study_done//60}h study")

    return output


# ROUTES 

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("Index.html", {"request": request})


@router.post("/result", response_class=HTMLResponse)
async def result(request: Request):
    # Form data parse karna FastAPI mein async hota hai
    form_data = await request.form()
    data = dict(form_data)
    
    timetable = generate_timetable(data)
    return templates.TemplateResponse("result.html", {"request": request, "timetable": timetable})


@router.get("/stats", response_class=HTMLResponse)
async def stats(request: Request):
    return templates.TemplateResponse("stats.html", {"request": request})


# RUN 

if __name__ == "__main__":
    # FastAPI uvicorn server use karta hai run hone ke liye
    uvicorn.run("main:logic", host="127.0.0.1", port=8000, reload=True)        except:
            return None

    def format_time(m):
        return f"{m//60:02d}:{m%60:02d}"

    def clean(arr):
        return [s.strip().lower() for s in arr if s.strip()]

    days = int(data["days"])

    subjects = clean(data["subjects"].split(","))
    weak = clean(data["weak"].split(","))
    strong = clean(data["strong"].split(","))

    if not subjects:
        subjects = ["general study"]

    if not weak:
        weak = subjects.copy()

    if not strong:
        strong = subjects.copy()

    strong = [s for s in strong if s not in weak]
    normal = [s for s in subjects if s not in weak and s not in strong]

    if not normal:
        normal = subjects.copy()

    start = to_min(data["start"]) or 480
    base_duration = int(data["duration"])
    break_after = int(data["break_after"])
    base_break = int(data["break_duration"])
    study_minutes_goal = int(data["study_hours"]) * 60
    break_minutes_goal = int(data["break_hours"]) * 60

    meals = {
        "Breakfast": (to_min(data["b_start"]), to_min(data["b_end"])),
        "Lunch": (to_min(data["l_start"]), to_min(data["l_end"])),
        "Dinner": (to_min(data["d_start"]), to_min(data["d_end"]))
    }

    output = []

    def pick_subject():
        r = random.random()

        if r < 0.5:
            return random.choice(weak)
        elif r < 0.8:
            return random.choice(normal)

        return random.choice(strong)

    for d in range(1, days + 1):
        output.append(f"DAY {d}")

        current = start
        end_day = start + 1440

        session_count = 0
        meal_done = {k: False for k in meals}
        total_study_done = 0
        total_break_done = 0

        while current < end_day:

            if (
                total_study_done >= study_minutes_goal
                and total_break_done >= break_minutes_goal
            ):
                break

            # MEALS 
            for name, (s, e) in meals.items():
                if (
                    s is not None
                    and not meal_done[name]
                    and s <= current < e
                ):
                    output.append(
                        f"{name}: {format_time(current)} - {format_time(e)}"
                    )
                    current = e
                    meal_done[name] = True

            # STUDY
            if total_study_done < study_minutes_goal:

                subject = pick_subject()
                duration = base_duration

                if subject in weak:
                    duration += 15
                elif subject in strong:
                    duration -= 10

                duration = max(
                    25,
                    min(duration, study_minutes_goal - total_study_done)
                )

                # if study would cross a meal
                meal_interrupted = False

                for name, (s, e) in meals.items():

                    if (
                        s is not None
                        and not meal_done[name]
                        and current < s < current + duration
                    ):
                        output.append(
                            f"{subject.title()}: {format_time(current)} - {format_time(s)}"
                        )

                        total_study_done += (s - current)
                        current = s

                        output.append(
                            f"{name}: {format_time(current)} - {format_time(e)}"
                        )

                        current = e
                        meal_done[name] = True

                        session_count += 1
                        meal_interrupted = True
                        break

                if meal_interrupted:
                    continue

                output.append(
                    f"{subject.title()}: {format_time(current)} - {format_time(current + duration)}"
                )

                current += duration
                total_study_done += duration
                session_count += 1

                if session_count >= break_after:
                    b = min(
                        base_break,
                        break_minutes_goal - total_break_done
                    )

                    output.append(
                        f"Break: {format_time(current)} - {format_time(current + b)}"
                    )

                    current += b
                    total_break_done += b
                    session_count = 0

        output.append(f"Summary: {total_study_done//60}h study")

    return output


# ROUTES 

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/result", response_class=HTMLResponse)
async def result(request: Request):
    # Form data parse karna FastAPI mein async hota hai
    form_data = await request.form()
    data = dict(form_data)
    
    timetable = generate_timetable(data)
    return templates.TemplateResponse("result.html", {"request": request, "timetable": timetable})


@router.get("/stats", response_class=HTMLResponse)
async def stats(request: Request):
    return templates.TemplateResponse("stats.html", {"request": request})


# RUN 

if __name__ == "__main__":
    # FastAPI uvicorn server use karta hai run hone ke liye
    uvicorn.run("main:logic", host="127.0.0.1", port=8000, reload=True)
