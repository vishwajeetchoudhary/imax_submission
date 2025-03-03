import os
from datetime import datetime
from config.settings import CRM_DATA_DIR

class CRMService:
    @staticmethod
    def track_customer(name, email, interaction, scenario):
        try:
            os.makedirs(CRM_DATA_DIR, exist_ok=True)
            
            file_path = os.path.join(CRM_DATA_DIR, "customer_interactions.txt")
            
            with open(file_path, "a", encoding="utf-8") as crm_file:
                crm_file.write(f"{datetime.now()} - {name} ({email}) - {scenario}: {interaction}\n")
            
            return "Customer interaction logged successfully."
        except Exception as e:
            print(f"Error logging customer interaction: {e}")
            return f"Failed to log customer interaction: {str(e)}"