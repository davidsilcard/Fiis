from Codigo.FundsExplorer.ListaFiis import Lista_De_Fundos_Imobiliarios





def main():
    req = Lista_De_Fundos_Imobiliarios()
    print(req.status_pagina)
    print(req.cookies)








if __name__ == '__main__':
    main()