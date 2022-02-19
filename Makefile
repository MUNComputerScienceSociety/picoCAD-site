run:
	uvicorn app.main:app --reload --log-level debug

black:
	black app/*.py
