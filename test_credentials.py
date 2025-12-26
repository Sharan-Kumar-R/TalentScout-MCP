from linkedin_client import LinkedInClient
import sys
import json

def test():
    print("--- LinkedIn Credential Test ---")
    try:
        client = LinkedInClient()
        print("1. Attempting to authenticate...")
        client.authenticate()
        print("   [SUCCESS] Authentication successful!")
        
        print("\n2. Testing People Search (query='Python Developer')...")
        people = client.search_people("Python Developer", limit=3)
        if people:
            print(f"   [SUCCESS] Found {len(people)} people.")
            print(f"   Sample: {people[0]}")
        else:
            print("   [WARNING] People search empty.")

        print("\n3. Testing Job Search (query='Python')...")
        jobs = client.search_jobs("Python", limit=3)
        if jobs:
            print(f"   [SUCCESS] Found {len(jobs)} jobs.")
            print(f"   Sample: {jobs[0]}")
        else:
            print("   [WARNING] Job search empty.")

    except Exception as e:
        print(f"\n[FAILURE] Error encountered: {e}")
        print("Please check your .env file and ensure LI_AT and JSESSIONID are correct.")

if __name__ == "__main__":
    test()
