def get_next_id(records):
    if not records:
        return 1

    return max(record["id"] for record in records) + 1


def get_totals(transactions):
    income_total = sum(
        transaction["amount"] for transaction in transactions
        if transaction["amount"] > 0
    )
    expense_total = sum(
        transaction["amount"] for transaction in transactions
        if transaction["amount"] < 0
    )

    return {
        "income": income_total,
        "expense": expense_total,
        "balance": income_total + expense_total,
    }


def get_category_totals(transactions):
    category_totals = {}

    for transaction in transactions:
        key = (transaction["category"], transaction["type"])
        category_totals[key] = category_totals.get(key, 0) + transaction["amount"]

    return sorted(
        category_totals.items(),
        key=lambda item: (item[0][1], item[0][0].lower()),
    )


def get_goal_progress(goal):
    if goal["target"] <= 0:
        return 0

    return min(100, int((goal["current"] / goal["target"]) * 100))


def get_all_categories(categories):
    all_categories = []

    for category in categories.get("Despesa", []) + categories.get("Receita", []):
        if category not in all_categories:
            all_categories.append(category)

    return all_categories


def format_currency(amount):
    formatted = f"R$ {abs(amount):,.2f}"
    formatted = formatted.replace(",", "X").replace(".", ",").replace("X", ".")

    if amount < 0:
        return f"-{formatted}"

    return formatted


def format_summary_currency(amount, compact=False):
    if compact:
        rounded_amount = round(abs(amount))
        formatted = f"R$ {rounded_amount:,.0f}"
        formatted = formatted.replace(",", ".")

        if amount < 0:
            return f"-{formatted}"

        return formatted

    return format_currency(amount)
