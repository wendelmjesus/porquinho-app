import csv


def export_transactions_to_csv(file_path, transactions):
    with open(file_path, "w", newline="", encoding="utf-8-sig") as export_file:
        writer = csv.writer(export_file, delimiter=";")
        writer.writerow(["Descrição", "Categoria", "Tipo", "Data", "Valor"])

        for transaction in reversed(transactions):
            writer.writerow([
                transaction["description"],
                transaction["category"],
                transaction["type"],
                transaction["date"],
                f"{transaction['amount']:.2f}".replace(".", ","),
            ])
