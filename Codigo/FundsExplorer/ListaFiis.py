import requests

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

            url = 'https://www.gestaojudicial.com.br/Paginas/Prontuario_Juridico/Gerencia_Atendimento/Pesquisa/Pesquisa_Resultado.asp'

            self.r = self.s.post(url, headers=self.headers, data=payload, cookies=self.cookies)
            status_pagina = self.r.status_code

            with open('PesquisarContrato.html', 'w') as f:
                f.write(self.r.text)

            resposta = []
            achei = False
            soup = BeautifulSoup(self.r.content, 'lxml')

            aviso = soup.find('font').text.strip('\n').replace('\n', '').strip('\t').strip()
            if aviso == 'Nenhuma informação foi encontrada.':
                resposta.append([status_pagina, achei, aviso])
                return resposta



        except Exception as e:
            print('Erro pesquisar_contrato: {0}'.format(e))
            return False
