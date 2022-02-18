run:
	uvicorn app.main:app --reload

black:
	black app/*.py
