# apps/expenses/utils.py
import re
from datetime import date
from common.models import MerchantMapping
from common.models import Category
from expenses.models import Transaction
from django.utils import timezone
from decimal import Decimal, InvalidOperation

AMOUNT_RE = re.compile(r'(?:₹|Rs\.?|INR)\s*([0-9,]+(?:\.[0-9]{1,2})?)', re.I)

# Fallback number regex (be careful — may match dates; we use only if amount token not found)
FALLBACK_NUM_RE = re.compile(r'([0-9]+(?:\,[0-9]{3})*(?:\.\d+)?)')

MERCHANT_PATTERNS = [
    re.compile(r'paid to\s+([A-Za-z0-9&\.\-\' ]+?)\s+(?:on|using|via|upi|ref|txn|txn:|txnid|$)', re.I),
    re.compile(r'to\s+([A-Za-z0-9&\.\-\' ]+?)\s+(?:using|on|via|ref|txn|$)', re.I),
    re.compile(r'([A-Za-z0-9&\.\-\' ]+?)\s+UPI', re.I),
    re.compile(r'pay to\s+([A-Za-z0-9&\.\-\' ]+?)\s', re.I),
    re.compile(r'credited to\s+([A-Za-z0-9&\.\-\' ]+?)\s', re.I),
]

def parse_amount(text: str):
    text = text or ''
    m = AMOUNT_RE.search(text)
    if m:
        raw = m.group(1)
    else:
        m2 = FALLBACK_NUM_RE.search(text)
        raw = m2.group(1) if m2 else None
    if not raw:
        return None
    # strip commas and convert
    raw = raw.replace(',', '')
    try:
        return Decimal(raw)
    except InvalidOperation:
        return None

def parse_merchant(text: str):
    text = text or ''
    for patt in MERCHANT_PATTERNS:
        m = patt.search(text)
        if m:
            candidate = m.group(1).strip(' .,-')
            # remove trailing words like 'upi' etc
            return candidate
    # fallback heuristic: take first capitalized token or first word group before 'on' or 'via'
    # simpler fallback: return first sequence of letters >3 chars
    fallback = re.search(r'([A-Za-z]{3,}(?: [A-Za-z]{2,})*)', text)
    return fallback.group(1).strip() if fallback else None

def find_mapping_for_merchant(merchant_text: str):
    if not merchant_text:
        return None
    merchant_text_low = merchant_text.lower()
    for mapping in MerchantMapping.objects.all():  # ordered by priority
        if mapping.keyword.lower() in merchant_text_low:
            return mapping
    return None

def create_category_for_user_if_missing(user, category_name, category_type='expense'):
    from common.models import Category
    cat, created = Category.objects.get_or_create(user=user, name=category_name, defaults={'type': category_type})
    return cat

def parse_upi_message_and_create_transaction(user, message_text, provided_date=None, txn_ref=None):
    """
    Parse a UPI/SMS message, create category if needed, create Transaction and Notification.
    Returns (transaction_obj, created_flag, reason_or_error)
    """
    amt = parse_amount(message_text)
    if amt is None:
        return (None, False, 'amount_not_found')

    merchant = parse_merchant(message_text) or 'Unknown'
    mapping = find_mapping_for_merchant(merchant)
    if mapping:
        category_name = mapping.category_name
        cat_type = mapping.category_type
    else:
        # fallback: create category 'Uncategorized' for user
        category_name = 'Uncategorized'
        cat_type = 'expense'

    # ensure category exists for this user
    category = create_category_for_user_if_missing(user, category_name, category_type=cat_type)

    tx_date = provided_date or (timezone.now().date() if provided_date is None else provided_date)
    # create transaction
    tx = Transaction.objects.create(
        user=user,
        amount=amt,
        category=category,
        date=tx_date,
        notes=message_text[:250],
        is_expense=(cat_type == 'expense')
    )
    return (tx, True, {'merchant': merchant, 'category': category.name})
