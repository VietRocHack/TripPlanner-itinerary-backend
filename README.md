
# TripPlanner-itinerary-backend

Run these lines (Windows):

`python -m venv venv` (create a virtual environment, first time)

`source venv/bin/activate`

`pip install -r requirements.txt`

`python src/test.py`

It should create a Flask server at port 8000. Run 127.0.0.1:8000 and you should see "Hello World".

You need an OpenAI API key. Use your own or ask for a `settings.py` file from the author. If you have your own key, create a `settings.py` file from root folder, then add a string named `openapi_key` with value as your key.
