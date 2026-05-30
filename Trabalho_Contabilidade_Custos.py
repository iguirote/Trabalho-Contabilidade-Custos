import pandas as pd

QUANTIDADE = 4000
PRECO_VENDA = 25.00


def ler_planilha(caminho):
    df = pd.read_excel(
        caminho,
        header=0,
        names=["gasto", "valor", "classificacao"],
        usecols=[0, 1, 2]
    )
    return df.to_dict(orient="records")


def classificar_gastos(registros):
    gastos = {
        "custo_variavel": [],
        "custo_fixo": [],
        "despesa": []
    }

    for item in registros:
        classe = str(item.get("classificacao", "")).lower()
        valor = str(item.get("valor", ""))

        valor_num = valor.replace("R$", "").replace("por unidade", "").strip()
        valor_num = float(valor_num.replace(".", "").replace(",", "."))

        item["valor_num"] = valor_num
        item["unitario"] = "por unidade" in valor

        if "custo variavel" in classe or "custo variável" in classe:
            gastos["custo_variavel"].append(item)
        elif "custo fixo" in classe:
            gastos["custo_fixo"].append(item)
        elif "despesa" in classe:
            gastos["despesa"].append(item)

    return gastos


def exibir_resultados(gastos):
    cv_unitario = sum(i["valor_num"] for i in gastos["custo_variavel"])
    cf_total    = sum(i["valor_num"] for i in gastos["custo_fixo"])
    despesa_unit = sum(i["valor_num"] for i in gastos["despesa"] if i["unitario"])

    custo_fixo_unitario  = cf_total / QUANTIDADE
    custo_total_por_pote = cv_unitario + custo_fixo_unitario
    margem_contribuicao  = PRECO_VENDA - custo_total_por_pote - despesa_unit
    pec = cf_total / margem_contribuicao

    print("\n<==========> BELLA ITÁLIA - CUSTOS <==========>")

    print("\n[Custos Variáveis]")
    for i in gastos["custo_variavel"]:
        print(f"  {i['gasto']:<50} R$ {i['valor_num']:.2f}/un")

    print("\n[Custos Fixos]")
    for i in gastos["custo_fixo"]:
        print(f"  {i['gasto']:<50} R$ {i['valor_num']:,.2f}")

    print("\n[Despesas]")
    for i in gastos["despesa"]:
        sufixo = "/un" if i["unitario"] else ""
        print(f"  {i['gasto']:<50} R$ {i['valor_num']:,.2f}{sufixo}")

    print("\n----------------------------------------------")
    print(f"  Custo Variável Unitário        : R$ {cv_unitario:>8.2f}")
    print(f"  Custo Variável Total           : R$ {cv_unitario * QUANTIDADE:>11,.2f}")
    print(f"  Custo Fixo Unitário            : R$ {custo_fixo_unitario:>8.2f}")
    print(f"  Custo Fixo Total               : R$ {cf_total:>11,.2f}")
    print(f"  Custo Total por Pote           : R$ {custo_total_por_pote:>8.2f}")
    print(f"  Margem de Contribuição Unit.   : R$ {margem_contribuicao:>8.2f}")
    print(f"  Ponto de Equilíbrio (PEC)      :    {pec:>7,.0f} potes")
    print("<=============================================>")


def main():
    caminho = "/content/custos.xlsx"
    registros = ler_planilha(caminho)
    gastos = classificar_gastos(registros)
    exibir_resultados(gastos)


if __name__ == "__main__":
    main()