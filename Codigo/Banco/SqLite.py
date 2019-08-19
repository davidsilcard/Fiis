import sqlite3
from Codigo.LerArquivo.LerArquivo import LerArquivo
import datetime as dt


class ConexaoBancoSqlite(object):

    def __init__(self):
        try:

            self.tabelaConf = 'tbl_conf'
            self.tabelaInfo = 'tbl_info'

        except Exception as e:
            print("Erro ao abrir banco: {0}".format(e))

    def connect_conf(self):
        try:

            self.nomeBanco = r'\\192.168.70.149\server\BackupsRobos\ProjetoCapturaImgMaisNegocios\python\MonitoramentoArquivosSeqAdp\venv\Codigo\Banco\banco_config.db'
            self.connConf = sqlite3.connect(self.nomeBanco, check_same_thread=True, timeout=10)
            self.cursorConf = self.connConf.cursor()

        except sqlite3.Error:
            print("Erro ao abrir banco: {0}".format(sqlite3.Error))

    def connect_info(self):

        try:
            self.nomeBanco = r'\\192.168.70.149\server\BackupsRobos\ProjetoCapturaImgMaisNegocios\python\MonitoramentoArquivosSeqAdp\venv\Codigo\Banco\banco_info.db'
            self.connInfo = sqlite3.connect(self.nomeBanco, check_same_thread=True, timeout=10)
            self.cursorInfo = self.connInfo.cursor()

        except sqlite3.Error:
            print("Erro ao abrir banco: {0}".format(sqlite3.Error))

    def close_connect_conf(self):
        if self.connConf:
            self.connConf.commit()
            self.connConf.close()

    def close_connect_info(self):
        if self.connInfo:
            self.connInfo.commit()
            self.connInfo.close()

    def criar_tabela_conf_db(self):

        self.cursorConf.execute(
            """SELECT name FROM sqlite_master WHERE type='table' AND name='{0}'""".format(self.tabelaConf))

        exists = bool(self.cursorConf.fetchone())

        if (exists == False):

            self.cursorConf.execute("""
                        CREATE TABLE tbl_conf (
                            id                  INTEGER PRIMARY KEY AUTOINCREMENT
                                                        NOT NULL,
                            EnderecoPastaOrigem STRING  NOT NULL,
                            EnderecoPastaOk     STRING  NOT NULL,
                            EnderecoPastaErro   STRING  NOT NULL,
                            QtdMaquina          INTEGER,
                            MinBalancear        INTEGER,
                            Usuario             STRING,
                            Senha               STRING,
                            FlagPararRobo       BOOLEAN NOT NULL,
                            FlagRebalancear     BOOLEAN NOT NULL
                        );
                    """.format(self.tabelaConf))
            print("Tabela criada: {0}".format(self.tabelaConf))

            self.cursorConf.execute("""
                INSERT INTO {0} (EnderecoPastaOrigem, EnderecoPastaOk, EnderecoPastaErro, QtdMaquina, MinBalancear, Usuario, Senha, FlagPararRobo, FlagRebalancear)
                VALUES('{1}', '{2}', '{3}',1, 30,'x050432','','0','0')
            """.format(self.tabelaConf, r'\\192.168.70.149\server\CapturaImagensMaisNegocios\01_Inicio',
                       r'\\192.168.70.149\server\CapturaImagensMaisNegocios\01_Inicio\Ok',
                       r'\\192.168.70.149\server\CapturaImagensMaisNegocios\01_Inicio\Erro'))
            self.connConf.commit()

        else:

            print("Tabela já existe: {0}".format(self.tabelaConf))

    def criar_tabela_info_db(self):

        self.cursorInfo.execute(
            """SELECT name FROM sqlite_master WHERE type='table' AND name='{0}'""".format(self.tabelaInfo))

        exists = bool(self.cursorInfo.fetchone())

        if (exists == False):

            self.cursorInfo.execute("""
                        CREATE TABLE tbl_info (
                            id               INTEGER      PRIMARY KEY AUTOINCREMENT
                                                          NOT NULL,
                            Contratos        VARCHAR (11) NOT NULL,
                            SeqAdp           VARCHAR (11) NOT NULL,
                            Contratos_SeqAdp VARCHAR (22) NOT NULL,
                            DtInsertArq      DATETIME     NOT NULL,
                            MaqRb            INTEGER,
                            QtdPg            INTEGER,
                            SttRb            VARCHAR,
                            DtRb             DATETIME,
                            FlagExportar     BOOLEAN      DEFAULT (False) 
                                                          NOT NULL,
                            NrMaq            INTEGER
                        );
                    """.format(self.tabelaInfo))
            print("Tabela criada: {0}".format(self.tabelaInfo))

        else:

            print("Tabela já existe: {0}".format(self.tabelaInfo))

    def inserir_contratos(self, lista):

        dataAtual = dt.datetime.now()
        dataAtual = f'{dataAtual:%d/%m/%Y}'

        for linha in lista:

            dados = linha.split(";")

            if dados[0] != '' and dados[1] != '':

                sql = """SELECT * FROM {0} where contratos = '{1}' and DtInsertArq >= '{2} 00:00:00' and DtInsertArq <= '{2} 23:59:59';""".format(
                    self.tabelaInfo, dados[0], dataAtual)
                print(sql)
                self.cursorInfo.execute(sql)
                qtd = len(self.cursorInfo.fetchall())

                if qtd == 0:
                    sql = """
                                INSERT INTO {0} (Contratos, SeqAdp, Contratos_SeqAdp, DtInsertArq, NrMaq)
                                VALUES ('{1}', '{2}', '{3}', '{4}', 0)
                          """.format(self.tabelaInfo, dados[0], dados[1], '{0}_{1}'.format(dados[0], dados[1]),
                                     dados[2])

                    print(sql)
                    self.cursorInfo.execute(sql)
                    self.connInfo.commit()

    def monitorar_Pastas(self):

        sql = """SELECT EnderecoPastaOrigem, EnderecoPastaOk, EnderecoPastaErro FROM {0};""".format(self.tabelaConf)
        # print(sql)
        self.cursorConf.execute(sql)
        enderecos = self.cursorConf.fetchall()
        return enderecos

    def quantidade_maq(self):

        sql = """SELECT QtdMaquina FROM {0};""".format(self.tabelaConf)
        # print(sql)
        self.cursorConf.execute(sql)
        nrMaq = self.cursorConf.fetchall()
        return nrMaq[0][0]

    def flag_rebalancear(self, flag):

        sql = """
                UPDATE {0}
                SET FlagRebalancear = {1}
            """.format(self.tabelaConf, flag)

        if flag == True:
            print('Robo de imagens pausado')
        else:
            print('Robo de imagens liberado')

        # print(sql)
        self.cursorConf.execute(sql)
        self.connConf.commit()

    def queryTempoDivisao(self):
        sql = """SELECT MinBalancear FROM {0};""".format(self.tabelaConf)
        # print(sql)
        self.cursorConf.execute(sql)
        tmp = self.cursorConf.fetchall()
        return tmp[0][0]

    def atualizar_divisao(self, nrMaq):

        try:

            sql = """UPDATE tbl_info SET NrMaq = 0 WHERE SttRb is null;"""
            self.cursorInfo.execute(sql)
            self.connInfo.commit()

            sql = """SELECT Contratos_SeqAdp FROM {0} where SttRb is null GROUP BY Contratos_SeqAdp;""".format(self.tabelaInfo)
            # print(sql)
            self.cursorInfo.execute(sql)
            qtd = len(self.cursorInfo.fetchall())

            if qtd > 0:

                divisao = int((qtd - 1) / nrMaq)
                for x in range(nrMaq):
                    y = x + 1
                    sql = """
                            UPDATE {0} SET NrMaq = {1} where Contratos_SeqAdp in  (
                            SELECT Contratos_SeqAdp FROM tbl_info WHERE SttRb is null and NrMaq = 0 GROUP BY Contratos_SeqAdp LIMIT {2}) ;
                    """.format(self.tabelaInfo, y, divisao)
                    # print(sql)
                    self.cursorInfo.execute(sql)
                    self.connInfo.commit()

                sql = """
                            UPDATE {0} SET NrMaq = 1 where Contratos_SeqAdp in  (
                            SELECT Contratos_SeqAdp FROM tbl_info WHERE SttRb is null and NrMaq = 0);
                        """.format(self.tabelaInfo, y, divisao)
                self.cursorInfo.execute(sql)
                self.connInfo.commit()


        except Exception as e:
            pass

        # def atualizar_linhas():

# c = ConexaoBancoSqlite()
# 
# c.connect_conf()
# c.criar_tabela_conf_db()
# c.close_connect_conf()
# 
# c.connect_info()
# c.criar_tabela_info_db()
# c.inserir_contratos()
# c.close_connect_info()
# 
# print(c.lista.lista)
