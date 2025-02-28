from typing import List, Dict
import requests
from django.conf import settings
from django.core.cache import cache


import logging

logger = logging.getLogger(__name__)


def get_mutual_funds_data() -> List[Dict]:
    """
    Fetches mutual fund data from a Rapid API endpoint and caches the response.
    """

    if not all(
        [settings.RAPID_API_URL, settings.RAPID_API_HOST, settings.RAPID_API_KEY]
    ):
        logger.error("Missing required API configuration")
        return None
    cache_key = "mutual_fund_data"
    cached_data = cache.get(cache_key)
    if cached_data:
        logger.info("Using cached data")
        return cached_data
    url = settings.RAPID_API_URL
    querystring = {"Mutual_Fund_Family": "Axis Mutual Fund", "Scheme_Type": "Open"}
    headers = {
        "x-rapidapi-host": settings.RAPID_API_HOST,
        "x-rapidapi-key": settings.RAPID_API_KEY,
    }
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        if response.status_code == 200:
            logger.info(f"Error fetching data: {response.status_code}")
            return response.json()
        else:
            logger.warning(f"Error fetching data: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data: {e}")
        return None


def get_single_fund_details(scheme_code: str) -> Dict:
    """
    Fetches details of a single mutual fund from a Rapid API endpoint.
    """
    if not all(
        [settings.RAPID_API_URL, settings.RAPID_API_HOST, settings.RAPID_API_KEY]
    ):
        logger.error("Missing required API configuration")
        return None
    url = settings.RAPID_API_URL
    querystring = {"Scheme_Type": "Open", "Scheme_Code": scheme_code}
    headers = {
        "x-rapidapi-host": settings.RAPID_API_HOST,
        "x-rapidapi-key": settings.RAPID_API_KEY,
    }
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        if response.status_code == 200:
            return response.json()[0]
        else:
            logger.warning(f"Error fetching data: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data: {e}")
        return None
