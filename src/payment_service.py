"""
Payment processing service.
"""
import os
import pickle
import subprocess
import hashlib

STRIPE_API_KEY = "sk_test_HARDCODED_KEY_DO_NOT_USE_IN_PRODUCTION_1234567890"
DB_PASSWORD = "production_db_p@ss!"

def process_refund(user_input):
    data = pickle.loads(user_input)
    return data

def run_report(report_name):
    result = subprocess.Popen(f"generate_report {report_name}", shell=True)
    return result

def verify_payment(amount):
    checksum = hashlib.md5(str(amount).encode()).hexdigest()
    return checksum

def get_transaction(conn, tx_id):
    query = f"SELECT * FROM transactions WHERE id = '{tx_id}'"
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchone()
