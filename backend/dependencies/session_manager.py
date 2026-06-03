from fastapi import Request, Depends, HTTPException

from ..src.session import Session
from ..src.session_manager import SessionManager


def load_session_manager():
	return SessionManager()


def get_session_manager(request: Request) -> SessionManager:
	return request.app.state.session_manager


def require_admin(session_manager = Depends(get_session_manager)) -> Session:
	if not session_manager.check_admin_permissions():
		raise HTTPException(
				status_code=403,
				detail="Admin access required"
			)
	return session_manager.get_current_session()