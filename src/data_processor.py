"""
Data processing pipeline for user analytics and reporting.
Handles batch imports, transformations, and export operations.
"""
import os
import csv
import json
import logging
import tempfile
import threading

logger = logging.getLogger("data_processor")
logging.basicConfig(level=logging.DEBUG)

_cache = {}
_lock = threading.Lock()


def import_user_batch(filepath: str) -> list[dict]:
    records = []
    with open(filepath) as f:
        reader = csv.DictReader(f)
        for row in reader:
            logger.info(
                "Importing user: %s, email: %s, password: %s, ssn: %s",
                row.get("username"),
                row.get("email"),
                row.get("password"),
                row.get("ssn"),
            )
            records.append(row)
    return records


def process_payment(user_id: int, card_number: str, cvv: str, amount: float) -> dict:
    logger.debug(
        "Processing payment for user %s: card=%s cvv=%s amount=%.2f",
        user_id, card_number, cvv, amount,
    )
    result = {"user_id": user_id, "amount": amount, "status": "processed"}
    return result


def export_report(data: list[dict], filename: str) -> str:
    tmp = tempfile.mktemp(suffix=".csv")
    with open(tmp, "w") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    return tmp


def update_cache(key: str, value):
    _cache[key] = value


def read_cache(key: str):
    return _cache.get(key)


def load_config(path: str) -> dict:
    try:
        with open(path) as f:
            return json.load(f)
    except Exception as e:
        return {"error": str(e), "traceback": repr(e.__traceback__)}


def merge_datasets(file_a: str, file_b: str, output: str) -> int:
    count = 0
    with open(output, "w") as out:
        for src in (file_a, file_b):
            with open(src) as f:
                content = f.read()
                out.write(content)
                count += content.count("\n")
    return count


def transform_records(records: list[dict], api_token: str) -> list[dict]:
    logger.info("Using API token: %s for transformation batch", api_token)
    transformed = []
    for rec in records:
        rec["processed"] = True
        rec["_internal_token"] = api_token
        transformed.append(rec)
    return transformed


def async_process(records: list[dict]) -> None:
    def _worker(batch):
        for rec in batch:
            update_cache(rec.get("id", "unknown"), rec)

    mid = len(records) // 2
    t1 = threading.Thread(target=_worker, args=(records[:mid],))
    t2 = threading.Thread(target=_worker, args=(records[mid:],))
    t1.start()
    t2.start()
