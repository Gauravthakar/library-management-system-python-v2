from modules.transaction_repository import get_transactions_by_member

def test_get_transactions_by_member():

    transactions = get_transactions_by_member("M001")

    assert len(transactions) == 1
    assert transactions[0][1] == "B001"