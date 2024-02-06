import pandas as pd
import requests
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Programa para que o usuário possa montar um portfólio de ativos e inserir os aportes com data, quantidade e valor
# para que possa ser calculado o preço médio dos ativos e observar o desempenho ao longo do tempo

##############################################################################################################################################################################################
"""
    Conectando à uma API para coletar os valores diários do ativo, criando um dataframe, para que possa ser plotado em um gráfico a evolução do preço do ativo

"""
coin = "SYS"
url = f"https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={coin}&market=USD&apikey=O3N4GIA6JBVS83QG"
api_key = "O3N4GIA6JBVS83QG"

def request(url):
    r = requests.get(url)
    return r.json()

data = request(url)["Time Series (Digital Currency Daily)"]


def parsing(response):
    result = []
    for item, value in response.items():
        day = {
            "coin": coin,
            "date": item,
            "open": response[item]["1b. open (USD)"],
            "high": response[item]["2b. high (USD)"],
            "low": response[item]["3b. low (USD)"],
            "close": response[item]["4b. close (USD)"],
            "volume": response[item]["5. volume"]
        }
        result.append(day)
    return result

df_precos = pd.DataFrame(parsing(data)).sort_values("date")
df_precos["date"] = pd.to_datetime(df_precos["date"]).dt.strftime("%d/%m/%Y")
df_precos[["open", "high", "low", "close", "volume"]] = df_precos[["open", "high", "low", "close", "volume"]].apply(pd.to_numeric)

##############################################################################################################################################################################################

# Definindo função para que o usuário possa inserir os aportes ao longo do tempo

lista_aportes = [{"data_aporte": dt.datetime.strptime("19/09/2022", "%d/%m/%Y"), "ativo_aporte": "SYS", "valor_aporte": "0.17", "quantidade_aporte": "586"},
                 {"data_aporte": dt.datetime.strptime("09/11/2022", "%d/%m/%Y"), "ativo_aporte": "SYS", "valor_aporte": "0.1125", "quantidade_aporte": "923"},
                 {"data_aporte": dt.datetime.strptime("13/11/2022", "%d/%m/%Y"), "ativo_aporte": "SYS", "valor_aporte": "0.115", "quantidade_aporte": "903"},
                 {"data_aporte": dt.datetime.strptime("06/12/2022", "%d/%m/%Y"), "ativo_aporte": "SYS", "valor_aporte": "0.1194", "quantidade_aporte": "4714"},
                 {"data_aporte": dt.datetime.strptime("06/01/2023", "%d/%m/%Y"), "ativo_aporte": "SYS", "valor_aporte": "0.1021", "quantidade_aporte": "1860"}]
def aportes():
    novo_aporte = input("Deseja inserir um novo registro de aporte? (s/n): ").lower()
    while novo_aporte == "s":
        ativo_aporte = input("Digite o nome do ativo: ").upper()
        data_aporte = validar_data()
        valor_aporte = validar_valor_aporte()
        quantidade_aporte = validar_quantidade_aporte()
        aporte_unico = {"data_aporte": data_aporte, "ativo_aporte": ativo_aporte, "valor_aporte": valor_aporte, "quantidade_aporte": quantidade_aporte}
        lista_aportes.append(aporte_unico)
        novo_aporte = input("Deseja inserir um novo registro de aporte? (s/n): ").lower()
        if novo_aporte == "n":
            break
    return lista_aportes

def validar_data():
    formato_data = "%d/%m/%Y"
    while True:
        try:
            data_aporte = input("Digite a data do aporte (dd/mm/yyyy): ")
            return dt.datetime.strptime(data_aporte, formato_data)
            break
        except ValueError:
            print("O formato da data inserido está incorreto, tente novamente (dd/mm/yyyy).")

def validar_valor_aporte():
    while True:
        try:
            valor_aporte = float(input("Digite o valor unitário do ativo: "))
            return valor_aporte
        except ValueError:
            print("Valor precisa ser numérico: ")

def validar_quantidade_aporte():
    while True:
        try:
            quantidade_aporte = float(input("Digite a quantidade do aporte: "))
            return quantidade_aporte
        except ValueError:
            print("Valor precisa ser numérico: ")


"""
def menu():
    opcao_menu = print(input("Selecione uma das opções: \n 1 - Adicionar aporte. \n "))
    opcao_menu
    if opcao_menu == 1:
        aportes()
"""            

aportes()

df_aportes = pd.DataFrame(lista_aportes).sort_values("data_aporte")
df_aportes["data_aporte"] = pd.to_datetime(df_aportes["data_aporte"])#.dt.strftime("%d/%m/%Y")
df_aportes[["valor_aporte", "quantidade_aporte"]] = df_aportes[["valor_aporte", "quantidade_aporte"]].apply(pd.to_numeric)

print(df_aportes)
print("Quantidade total possuído: ", df_aportes["quantidade_aporte"].sum())
# print(df_aportes.info())

print(df_precos)
#print(df_precos.info())



##############################################################################################################################################################################################
# Graficos
"""
fig, ax = plt.subplots(nrows = 1, ncols = 1, sharey = True, sharex = True)

ax.plot(df_precos["date"], df_precos["open"], color = "#1B998B")
ax.scatter(df_aportes["data_aporte"], df_aportes["valor_aporte"], color = "#F75C03", s = 10)

locator = mdates.MonthLocator(bymonth = (1, 4))
formatter = mdates.DateFormatter("%Y")

ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)

ax.xaxis.set_minor_locator(mdates.MonthLocator())
ax.xaxis.set_minor_formatter(mdates.DateFormatter("%b"))
# ax.set_xlim(dt.datetime.strptime("01/09/2022", "%d/%m/%Y"), dt.datetime.strptime("12/02/2023", "%d/%m/%Y"))
# ax.set_ylim(0.08, 0.29)
ax.grid(False)
ax.set_title(f"Preco {coin} em dólares.")

# print(plt.style.available)
plt.style.use("seaborn-v0_8-pastel")

plt.show()


# Esconder o eixo y
# plt.axes().yaxis.set_major_locator(plt.NullLocator())
# Formatar o eixo y
# plt.axes().yaxis.set_major_formatter("${x:1.2f}")

# Esconder o eixo x
# plt.axes().xaxis.set_minor_locator(plt.NullLocator())


# plt.plot(df_aportes["data_aporte"], df_aportes["valor_aporte"], color = "#F75C03")
# plt.plot(df_precos.index, df_precos["open"], color = "#1B998B")
# plt.title(f"Preco {coin} em dólares.")
# plt.ylabel("USD")
# plt.xlabel("Data")

# plt.show()
"""