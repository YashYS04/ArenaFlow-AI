"""Vercel Serverless Function entry point.

This file exports the FastAPI application instance from the core app module,
serving as the main backend router for Vercel's serverless builder execution.
"""

from app.main import app

__all__ = ["app"]
