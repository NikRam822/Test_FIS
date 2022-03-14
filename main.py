import csv
import sqlite3


def get_data_from_db():
    con = sqlite3.connect('test_data.sqlite')
    cursorObj = con.cursor()
    return cursorObj.execute('SELECT * FROM Request ').fetchall()


def view_data_from_db():
    con = sqlite3.connect('test_data.sqlite')
    cursorObj = con.cursor()
    all_data=cursorObj.execute('SELECT * FROM Request ').fetchall()
    for data in all_data:
        print(data)


def main_debt(monthly_payment, interest_debts):
    return monthly_payment - interest_debts


def interest_debt(data_remainder, rate):
    return data_remainder * ((rate / 100) / 12)


def remainder(data_remainder, main_debts):
    return data_remainder - main_debts


def payment(summa, rate, period):
    percent_rate = rate / (100 * 12)
    monthly_payment = summa * (percent_rate / (1 - (1 + percent_rate) ** (-1 * period)))
    return round(monthly_payment, 2)


def write_data_to_csv(write_data):
    file = open('data.csv', 'w')
    with file:
        writer_dara = csv.writer(file)
        writer_dara.writerows(write_data)

    print("Writing complete")


def generate_graph(const_remainder, reates, time):
    data = ["Месяц", "Ежемесячный платеж", "Основной долг", "Долг по процентам", "Остаток"]

    arr_for_data = [data]

    const_payment = payment(const_remainder, rates, time)
    const_main_debt = 0

    for i in range(1, time + 1):
        data = []
        const_remainder = round(remainder(const_remainder, const_main_debt), 2)
        debt = round(interest_debt(const_remainder, rates), 2)
        const_main_debt = round(main_debt(const_payment, debt), 2)
        data.append(i)
        data.append(const_payment)
        data.append(const_main_debt)
        data.append(debt)
        data.append(const_remainder)
        print(data)
        arr_for_data.append(data)

    write_data_to_csv(arr_for_data)


request_from_db = get_data_from_db()
rates = request_from_db[0][4]
const_remainder = request_from_db[0][3]
time = int(request_from_db[0][6].split(' ')[0])


def get_data(request_number):
    request_from_db = get_data_from_db()
    rates = request_from_db[request_number - 1][4]
    const_remainder = request_from_db[request_number - 1][3]
    time = int(request_from_db[request_number - 1][6].split(' ')[0])
    generate_graph(const_remainder, rates, time)


view_data_from_db()
get_data(1)
