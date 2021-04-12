import os


def success(result={}, code=200, status="success", message="", errors=[]):
	return {"result": result, "code": code, "status": status, "message": message, "errors": errors}


def error(result={}, code=404, status="error", message="", errors=[]):
	return {"result": result, "code": code, "status": status, "message": message, "errors": errors}, code


def fix_confidence_value(confidence):
	confidence = confidence if confidence else 0
	return round(confidence * 100, 2)

