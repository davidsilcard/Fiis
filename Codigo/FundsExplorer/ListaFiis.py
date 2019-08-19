import requests
from bs4 import BeautifulSoup


class Lista_De_Fundos_Imobiliarios(object):

    def __init__(self):
        self.s = requests.Session()
        url = 'https://www.fundsexplorer.com.br'
        self.headers = {
            # 'Accept': 'image/gif, image/jpeg, image/pjpeg, application/x-ms-application, application/xaml+xml, application/x-ms-xbap, */*',
            # 'Accept-Encoding': 'gzip, deflate',
            # 'Accept-Language': 'pt-BR',
            # 'Connection': 'Keep-Alive',
            # 'Content-Type': 'application/x-www-form-urlencoded',
            # 'Host': 'www.gestaojudicial.com.br',
            # 'Referer': 'https://www.fundsexplorer.com.br/',
            # 'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        }

        self.r = self.s.get(url, headers=self.headers)
        self.status_pagina = self.r.status_code
        self.cookies = (self.r.cookies.get_dict())

    def quantidade_fiis_cadastrados(self):
        try:

            url = 'https://www.fundsexplorer.com.br/funds'
            self.r = self.s.get(url, headers=self.headers, cookies=self.cookies)
            status_pagina = self.r.status_code

            with open('fundsexplorer.html', 'w') as f:
                f.write(self.r.text)

            soup = BeautifulSoup(self.r.content, 'lxml')

            aviso = soup.find("span", id="filters-results-count").b.text
            print('Exitem {0} Fiis listados.'.format(aviso))

        except Exception as e:
            print('Erro pesquisar_contrato: {0}'.format(e))
            return False

    def listar_fiis_gravar_banco(self):
        pass
