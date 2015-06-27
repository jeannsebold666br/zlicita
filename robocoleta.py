#!/usr/bin/python
#  -*- coding: utf8 -*-
import unittest
import MySQLdb
import re
from datetime import datetime, date, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        
        #self.db = MySQLdb.connect("localhost","root","tux","zlicita")
        self.db = MySQLdb.Connection(user="root",passwd="tux",db="zlicita", host="localhost", charset="utf8",  use_unicode=True)



    def test_main(self):
        lista = self.getColeta()
        
        driver = self.roboLogin()

        for registro  in lista:
            i = datetime.now()
            dtstart = i.strftime('%Y-%m-%d %H:%M:%S')
            print
            print "===< Iniciado dia %s em %s >===" % (registro[3], dtstart)
            print

            driver = self.coletar(driver, registro)

            i = datetime.now()
            dtend = i.strftime('%Y-%m-%d %H:%M:%S')

            #self.finalizaColeta(registro[0], dtstart, dtend)

            print
            print "===> finalizado dia %s em %s <===" % (registro[3], dtend)
            print


    def finalizaColeta(self, id_coleta, dtstart, dtend):
        db = self.db
        cursor = db.cursor()
        sql = "UPDATE FROM coleta SET data_ini_coleta = '"+dtstart+"', data_ini='"+dtend+"', finalizado = true WHERE id_coleta = "+id_coleta
        cursor.execute(sql)
        db.close()


    def coletar(self, driver, registro):
        id_coleta = registro[0]
        total = registro[1]
        coletado = registro[2]
        dia = registro[3]

        # Tela de pesquisa
        driver.get("https://www.comprasnet.gov.br/ConsultaLicitacoes/ConsLicitacao_Filtro.asp")
        self.assertEqual('frmLicitacao', driver.find_element_by_xpath('//*[@id="frmLicitacao"]').get_attribute('name'))

        driver.find_element_by_xpath('//*[@id="dt_publ_ini"]').send_keys(dia)
        driver.find_element_by_xpath('//*[@id="dt_publ_fim"]').send_keys(dia)
        driver.find_element_by_xpath('//*[@id="frmLicitacao"]/table/tbody/tr[2]/td/table[2]/tbody/tr[4]/td[2]/table/tbody/tr/td/table/tbody/tr[4]/td[2]/table/tbody/tr/td/table/tbody/tr[7]/td/input').click();
        driver.find_element_by_xpath('//*[@id="ok"]').click();



        self.assertIn("Comprasnet", driver.title)
        url = driver.current_url
        print "-- URL: %s" % (url)
        #driver.get("https://www.comprasnet.gov.br/ConsultaLicitacoes/ConsLicitacao_Relacao.asp?numprp=&dt_publ_ini="+dia+"&dt_publ_fim="+dia+"&chkModalidade=1,2,3,20,5,99&chk_concor=&chk_pregao=&chk_rdc=&optTpPesqMat=M&optTpPesqServ=S&chkTodos=-1&chk_concorTodos=&chk_pregaoTodos=&txtlstUf=&txtlstMunicipio=&txtlstUasg=&txtlstGrpMaterial=&txtlstClasMaterial=&txtlstMaterial=&txtlstGrpServico=&txtlstServico=&txtObjeto=&numpag=1")

        time.sleep(1)

        resultado = True
        try:
            paginacao = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr[3]/td[2]/table/tbody/tr[1]/td/center")
        except:
            resultado = False


        if(resultado):
            pattern = re.search(r".de (\d+)",paginacao.text)
            total = pattern.group(1)
            total = int(total)
        else:
            print "-- Sem registro --"
            return driver


        print "--- Total: %s - Coletado: %s - Dia:%s ---" % (total, coletado, dia)




        paginas = total/10
        #if coletado == 0: coletado = 1
        coletado = coletado+1
        paginas_start = 1.0 * (coletado / 10)
        form_start = coletado % 10
        if paginas_start < 1 :
            paginas_start = 1
        else:
            paginas_start = int(paginas_start)
        if paginas < 1: paginas = 1
        if form_start == 0: form_start = 10

        for pagina in range(paginas_start,paginas+1):
            print "## Pagina %s ##" % (pagina)

            url = "https://www.comprasnet.gov.br/ConsultaLicitacoes/ConsLicitacao_Relacao.asp?numprp=&dt_publ_ini="+dia+"&dt_publ_fim="+dia+"&chkModalidade=1,2,3,20,5,99&chk_concor=&chk_pregao=&chk_rdc=&optTpPesqMat=M&optTpPesqServ=S&chkTodos=-1&chk_concorTodos=&chk_pregaoTodos=&txtlstUf=&txtlstMunicipio=&txtlstUasg=&txtlstGrpMaterial=&txtlstClasMaterial=&txtlstMaterial=&txtlstGrpServico=&txtlstServico=&txtObjeto=&numpag="+str(pagina)


            for form in range(form_start,11):
                driver.get(url)

                time.sleep(2)

                i = datetime.now()
                registro_dtstart = i.strftime('%Y-%m-%d %H:%M:%S')
                numero_registro = ((pagina-1)*10)+form
                print
                print "--< Iniciando coleta registro #%s em %s >--" % (numero_registro, registro_dtstart)


                cidade_estado = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr[3]/td[2]/form["+str(form)+"]/table/tbody/tr[1]/td[2]/table/tbody/tr/td[2]").text
                #driver.find_element_by_xpath("/html/body/table[2]/tbody/tr[3]/td[2]/form["+str(form)+"]/table/tbody/tr[2]/td[2]/input[3]").click()
                itens = driver.find_elements_by_name('itens')
                itens[form-1].click()
                url_registro = driver.current_url

                print "-- %s --" % (driver.current_url)
                time.sleep(2)

                try:
                    orgao_1 = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr[2]/td/table[2]/tbody/tr[1]/td[2]/table/tbody/tr[1]/td/p").text
                    tmp = re.search(r"UASG:", orgao_1)
                    if (tmp):
                        orgao_1 = ''

                except:
                    orgao_1 = ''

                try:
                    orgao_2 = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr[2]/td/table[2]/tbody/tr[1]/td[2]/table/tbody/tr[2]/td/p").text
                    tmp = re.search(r"UASG:", orgao_2)
                    if (tmp):
                        orgao_2 = ''
                except:
                    orgao_2 = ''

                try:
                    orgao_3 = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr[2]/td/table[2]/tbody/tr[1]/td[2]/table/tbody/tr[3]/td/p").text
                    tmp = re.search(r"UASG:", orgao_3)
                    if (tmp):
                        orgao_3 = ''
                except:
                    orgao_3 = ''

                try:
                    uasg = driver.find_element_by_xpath("(//p[contains(text(),'UASG:')])").text
                    tmp = re.search(r".*UASG:(.*\d+).*", uasg)
                    uasg = tmp.group(1)
                except:
                    uasg = ''


                pregao = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr[2]/td/table[2]/tbody/tr[2]/td[2]/table/tbody/tr/td/p/span").text
                tmp = re.search(ur".*Nº(.*)", pregao)
                if (tmp):
                    pregao = tmp.group(1)

                text = driver.find_element_by_xpath("(//p[contains(text(),'Objeto:')])").text
                text = text.split('\n')
                objeto = text[1]
                tmp = re.search(r".*Objeto:(.*)", objeto)
                if (tmp):
                    objeto = tmp.group(1)

                edital = text[2]
                tmp = re.search(r".*Edital a partir de:(.*)", edital)
                if (tmp):
                    edital = tmp.group(1)

                endereco = text[3]
                tmp = re.search(ur".*Endereço:(.*)", endereco)
                if (tmp):
                    endereco = tmp.group(1)

                telefone = text[4]
                tmp = re.search(ur".*Telefone:(.*)", telefone)
                if (tmp):
                    telefone = tmp.group(1)

                fax = text[5]
                tmp = re.search(ur".*Fax:(.*)", fax)
                if (tmp):
                    fax = tmp.group(1)

                proposta = text[6]
                tmp = re.search(ur".*Entrega da Proposta:(.*)", proposta)
                if (tmp):
                    proposta = tmp.group(1)

                item = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr[2]/td/table[2]/tbody/tr[3]").text
                item_material = ''
                item_servico = ''
                tmp = re.search(ur".*Itens de Serviços.*", item.split("\n")[0])
                if (tmp):
                    item_servico = item
                else:
                    item_material = item


                html = driver.page_source

                # Coleta a url de download
                driver.find_element_by_name('Download').click()
                atual = driver.current_window_handle
                for handle in driver.window_handles:
                    driver.switch_to_window(handle)
                link_download = driver.current_url
                driver.close()
                driver.switch_to_window(atual)

                cidade_estado = cidade_estado.split("-")
                cidade = cidade_estado[0]
                estado = cidade_estado[1]

                print "id_coleta = %s" % (id_coleta)
                print "total = %s" % (total)
                print "numero_registro = %s" % (numero_registro)
                print "cidade = %s" % (cidade)
                print "estado = %s" % (estado)
                print "orgao_1 = %s" % (orgao_1)
                print "orgao_2 = %s" % (orgao_2)
                print "orgao_3 = %s" % (orgao_3)
                print "uasg = %s" % (uasg)
                print "pregao = %s" % (pregao)
                print "objeto = %s" % (objeto)
                print "edital = %s" % (edital)
                print "endereco = %s" % (endereco)
                print "telefone = %s" % (telefone)
                print "fax = %s" % (fax)
                print "proposta = %s" % (proposta)
                print "item_servico = %s" % (item_servico.split("\n")[0])
                print "item_material = %s" % (item_material.split("\n")[0])
                print "link_download = %s" % (link_download)
                print "url_registro = %s" % (url_registro)

                i = datetime.now()
                registro_dtend = i.strftime('%Y-%m-%d %H:%M:%S')
                page_source = driver.page_source

                registros = [
                    str(id_coleta).strip(),
                    str(numero_registro).strip(),
                    str(cidade).strip(),
                    str(estado).strip(),
                    uasg.strip(),
                    orgao_1.strip(),
                    orgao_2.strip(),
                    orgao_3.strip(),
                    pregao.strip(),
                    objeto.strip(),
                    edital.strip(),
                    endereco.strip(),
                    telefone.strip(),
                    fax.strip(),
                    proposta.strip(),
                    item_material.strip(),
                    item_servico.strip(),
                    'teste'.strip(),
                    str(link_download),
                    str(url_registro),
                    str(registro_dtstart),
                    str(registro_dtend)
                ]
                self.insertRegistro(registros)


                print
                print "--> Finalizado coleta registro #%s em %s <--" % (numero_registro, registro_dtend)


            form_start = 1



        return  driver

    def insertRegistro(self, registros):
        db = self.db
        cursor = db.cursor()
        #var_string = ', '.join("'%s'" * len(registros))
        var_string = "'%s'," * len(registros)
        print
        print len(registros)
        var_string = var_string[0:len(var_string)-1]
        sql = "INSERT INTO registro "\
              "(id_coleta, numero_registro, cidade, estado, uasg, orgao1, orgao2, orgao3, pregao, objeto, edital, endereco, telefone, fax, proposta, item_material, item_servico, html, link_download, url, data_inicio_coleta, data_fim_coleta)" \
              " VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');" \
              % (
                registros[0],
                registros[1],
                registros[2],
                registros[3],
                registros[4],
                registros[5],
                registros[6],
                registros[7],
                registros[8],
                registros[9],
                registros[10],
                registros[11],
                registros[12],
                registros[13],
                registros[14],
                registros[15],
                registros[16],
                registros[17],
                registros[18],
                registros[19],
                registros[20],
                registros[21]
              )

        #sql = sql % registros
        print sql
        #cursor.execute(sql, registros)
        cursor.execute(sql)
        db.close()


    def tearDown(self):
        self.driver.close()


    def roboLogin(self):
        print "### Efetuando login no sistema ###"

        driver = self.driver
        driver.get("https://www.comprasnet.gov.br/seguro/loginPortal.asp")
        self.assertIn("SIASG", driver.title)


        # Login
        driver.find_element_by_xpath('//*[@id="perfil"]/option[2]').click()
        driver.find_element_by_xpath('//*[@id="txtLogin"]').send_keys('Vergilio')
        driver.find_element_by_xpath('//*[@id="txtSenha"]').send_keys('NOVA0001')
        driver.find_element_by_xpath('//*[@id="acessar"]').click()


        # Dashboard
        self.assertIn("ComprasNet", driver.title)

        # Fechar popup
        atual = driver.current_window_handle
        for handle in driver.window_handles:
            driver.switch_to_window(handle)

        driver.close()
        driver.switch_to_window(atual)

        return driver


    def getColeta(self):
        db = self.db
        cursor = db.cursor()
        sql = "SELECT id_coleta,COALESCE(qtd_registro,0), COALESCE(qtd_coletado,0), DATE_FORMAT(data,'%d/%m/%Y') " \
              "  FROM coleta " \
              " WHERE data <= '2015-01-02' " \
              "   AND finalizado = 0"
              #" WHERE finalizado = 0"

        cursor.execute(sql)
        results = cursor.fetchall()
        
        lista = []
        for row in results:
            # Now print fetched result
            print "Carregando dia %s ..." % (row[3])
            item = [row[0],row[1],row[2],row[3]]
            lista.append(item)

        # disconnect from server
        db.close()

        return lista


if __name__ == "__main__":
    unittest.main()
