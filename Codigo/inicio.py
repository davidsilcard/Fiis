from Codigo.FundsExplorer.ListaFiis import Lista_De_Fundos_Imobiliarios





def main():
    req = Lista_De_Fundos_Imobiliarios()
    # print(req.status_pagina)
    # print(req.cookies)
    req.quantidade_fiis_cadastrados()
    req.listar_fiis_gravar_banco()







if __name__ == '__main__':
    main()