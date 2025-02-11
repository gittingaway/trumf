import json
import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_API_URL = os.getenv("SUPABASE_API_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_API_URL or not SUPABASE_SERVICE_ROLE_KEY:
    raise ValueError(
        "Please set the SUPABASE_API_URL and SUPABASE_SERVICE_ROLE_KEY environment variables."
    )

supabase = create_client(SUPABASE_API_URL, SUPABASE_SERVICE_ROLE_KEY)


def load_dummy_data():
    with open("./dummy_data.json", "r") as file:
        data = json.load(file).get("merchants")
    return data


def insert_merchants(merchants):
    return supabase.table("merchants").insert(merchants).execute()


def get_merchants():
    res = supabase.table("merchants").select("*").execute()
    return res.model_dump(mode="python").get("data")


def get_cashback_value_type(cashback):
    if "%" in cashback:
        return "percentage"
    return "kroner"


def convert_cashback_to_float(cashback):
    cashback.replace(" ", "")
    if "%" in cashback:
        cashback = cashback.replace("%", "")
    if "kr" in cashback:
        cashback = cashback.replace("kr", "")
    return float(cashback)


def calculate_cashback_change(old_merchants, new_merchant_data, days_ago):
    if not old_merchants:
        return None

    now = datetime.now()
    days_ago = now - timedelta(days=days_ago)

    for merchant in old_merchants:
        ## we only care about the date, not hours, minutes, seconds etc
        ## created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S") this is the date format. But we only care about Y-m-d
        ## but H M S will not be equal to 0, so we need to set them to 0
        created_at = datetime.strptime(merchant["created_at"], "%Y-%m-%d %H:%M:%S")
        created_at = created_at.replace(hour=0, minute=0, second=0)
        if created_at == days_ago:
            index = old_merchants.index(merchant)
            break

    try:
        old_cashback = convert_cashback_to_float(old_merchants[index]["cashback"])
        new_cashback = convert_cashback_to_float(new_merchant_data["cashback"])
        return new_cashback - old_cashback
    except IndexError:
        return None


def calculate_low_high(old_merchant, new_merchant_data, lowest=True):
    if not old_merchant:
        return new_merchant_data.get("cashback")

    old_cashback = convert_cashback_to_float(old_merchant[0].get("cashback"))
    new_cashback = convert_cashback_to_float(new_merchant_data.get("cashback"))

    if lowest:
        return min(old_cashback, new_cashback)
    return max(old_cashback, new_cashback)


def process_new_merchant(new_merchant_data):
    cashback_value_type = get_cashback_value_type(new_merchant_data.get("cashback"))

    old_merchants = (
        supabase.table("merchants")
        .select("*")
        .eq("name", new_merchant_data.get("name"))
        .eq("cashback_value_type", cashback_value_type)
        .order("created_at", desc=True)
        .limit(30)
        .execute()
        .model_dump(mode="python")
        .get("data")
    )

    return {
        **new_merchant_data,
        "cashback_change_last_24h": calculate_cashback_change(
            old_merchants, new_merchant_data, 0
        ),
        "cashback_change_last_7d": calculate_cashback_change(
            old_merchants, new_merchant_data, 6
        ),
        "cashback_change_last_30d": calculate_cashback_change(
            old_merchants, new_merchant_data, 29
        ),
        "cashback_lowest": calculate_low_high(
            old_merchants, new_merchant_data, lowest=True
        ),
        "cashback_highest": calculate_low_high(
            old_merchants, new_merchant_data, lowest=False
        ),
    }


def main():
    data = load_dummy_data()
    [process_new_merchant(merchant) for merchant in data]
    # merchants = get_merchants()
    # for merchant in merchants:
    #    print(merchant)


if __name__ == "__main__":
    main()
