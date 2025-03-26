import requests
import os
from datetime import datetime, timedelta
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_leads():
    try:
        url = "https://mapi.indiamart.com/wservce/crm/crmListing/v2/"
        
        
        # Calculate yesterday and today timestamps
        now = datetime.now()
        yesterday = now - timedelta(hours=24)

        start_time = yesterday.strftime("%d-%m-%Y %H:%M")
        end_time = now.strftime("%d-%m-%Y %H:%M")

        api_key = os.getenv("INDIAMART_API_KEY")
        print(api_key)
        logger.info(f"API Key length: {len(api_key) if api_key else 0}")
        
        params = {
            "glusr_crm_key": api_key,
            "start_time": start_time,
            "end_time": end_time,
        }
        
        # Check if API key is set
        if not params["glusr_crm_key"]:
            logger.error("INDIAMART_API_KEY environment variable is not set")
            return []
            
        response = requests.get(url, params=params, timeout=30)  # Add timeout
        response.raise_for_status()  # Raise exception for bad status codes
        
        data = response.json()
        if data.get('STATUS') == 'SUCCESS':
            return data.get("RESPONSE", [])
        else:
            error_msg = data.get('MESSAGE', 'No error message provided')
            logger.warning(f"API returned non-success status: {data.get('STATUS')}. Error: {error_msg}")
            return []
            
    except requests.exceptions.Timeout:
        logger.error("Request timed out while fetching leads")
        return []
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error while fetching leads: {str(e)}")
        return []
    except ValueError as e:
        logger.error(f"Invalid JSON response: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error while fetching leads: {str(e)}")
        return []

if __name__ == '__main__':
    print("Fetching leads from IndiaMART...")
    leads = fetch_leads()
    print(f"Found {len(leads)} leads")
    if leads:
        print("\nLead details:")
        for lead in leads:
            print(f"- {lead.get('COMPANY_NAME', 'Unknown Company')}: {lead.get('ENQUIRY_TEXT', 'No enquiry text')}")