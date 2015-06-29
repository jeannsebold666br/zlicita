#!/usr/bin/python
#  -*- coding: utf8 -*-
import unittest
import pymysql
import re
import codecs
from datetime import datetime, date, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        
        self.db = pymysql.connect(user="root",passwd="tux",db="zlicita", host="localhost")
        #self.db = MySQLdb.Connection(user="root",passwd="tux",db="zlicita", host="localhost")#, charset="utf8",  use_unicode=True)



    def test_main(self):
        lista = self.getColeta()
        
        driver = self.roboLogin()
        #driver = self.driver

        for registro  in lista:
            i = datetime.now()
            dtstart = i.strftime('%Y-%m-%d %H:%M:%S')
            print()
            print("===< Iniciado dia {} em {} >===".format(registro[3], dtstart))
            print()

            driver = self.coletar(driver, registro)

            i = datetime.now()
            dtend = i.strftime('%Y-%m-%d %H:%M:%S')

            self.finalizaColeta(registro[0], dtstart, dtend)

            print()
            print ("===> finalizado dia {} em {} <===".format(registro[3], dtend))
            print()


    def finalizaColeta(self, id_coleta, dtstart, dtend):
        db = self.db
        cursor = db.cursor()
        sql = "UPDATE coleta SET data_ini_coleta = '{}', data_fim_coleta='{}', finalizado = 1 WHERE id_coleta = {};"\
              .format(dtstart, dtend, id_coleta)
        print(sql)
        cursor.execute(sql)
        db.commit()
        #db.close()


    def atualizaColeta(self, id_coleta, total, coletado, dtstart, dtend):
        db = self.db
        cursor = db.cursor()
        sql = "UPDATE coleta SET data_ini_coleta = '{}', data_fim_coleta='{}', qtd_registro = '{}', qtd_coletado='{}' WHERE id_coleta = {};"\
              .format(dtstart, dtend, total, coletado, id_coleta)
        print(sql)
        cursor.execute(sql)
        db.commit()


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
        print("-- URL: {}".format(url))
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
            print("-- Sem registro --")
            return driver


        print("--- Total: {} - Coletado: {} - Dia:{} ---".format(total, coletado, dia))




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

        paginas_start = int(paginas_start)
        paginas = int(paginas)

        for pagina in range(paginas_start,paginas+1):
            print("## Pagina Start {} - Pagina atual {} de {} - form {} ##".format(paginas_start, pagina, paginas, form_start))

            url = "https://www.comprasnet.gov.br/ConsultaLicitacoes/ConsLicitacao_Relacao.asp?numprp=&dt_publ_ini="+dia+"&dt_publ_fim="+dia+"&chkModalidade=1,2,3,20,5,99&chk_concor=&chk_pregao=&chk_rdc=&optTpPesqMat=M&optTpPesqServ=S&chkTodos=-1&chk_concorTodos=&chk_pregaoTodos=&txtlstUf=&txtlstMunicipio=&txtlstUasg=&txtlstGrpMaterial=&txtlstClasMaterial=&txtlstMaterial=&txtlstGrpServico=&txtlstServico=&txtObjeto=&numpag="+str(pagina)


            for form in range(form_start,11):
                driver.get(url)

                time.sleep(2)

                i = datetime.now()
                registro_dtstart = i.strftime('%Y-%m-%d %H:%M:%S')
                numero_registro = (pagina*10)+form
                print
                print("--< Iniciando coleta registro #{} em {} >--".format(numero_registro, registro_dtstart))


                cidade_estado = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr[3]/td[2]/form["+str(form)+"]/table/tbody/tr[1]/td[2]/table/tbody/tr/td[2]").text
                #driver.find_element_by_xpath("/html/body/table[2]/tbody/tr[3]/td[2]/form["+str(form)+"]/table/tbody/tr[2]/td[2]/input[3]").click()
                itens = driver.find_elements_by_name('itens')
                itens[form-1].click()
                url_registro = driver.current_url

                print("-- {} --".format(driver.current_url))
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
                tmp = re.search(r".*Nº(.*)", pregao)
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
                tmp = re.search(r".*Endereço:(.*)", endereco)
                if (tmp):
                    endereco = tmp.group(1)

                telefone = text[4]
                tmp = re.search(r".*Telefone:(.*)", telefone)
                if (tmp):
                    telefone = tmp.group(1)

                fax = text[5]
                tmp = re.search(r".*Fax:(.*)", fax)
                if (tmp):
                    fax = tmp.group(1)

                proposta = text[6]
                tmp = re.search(r".*Entrega da Proposta:(.*)", proposta)
                if (tmp):
                    proposta = tmp.group(1)

                item = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr[2]/td/table[2]/tbody/tr[3]").text
                item_material = ''
                item_servico = ''
                tmp = re.search(r".*Itens de Serviços.*", item.split("\n")[0])
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

                print("id_coleta = {}".format(id_coleta))
                print("total = {}".format(total))
                print("numero_registro = {}".format(numero_registro))
                print("cidade = {}".format(cidade))
                print("estado = {}".format(estado))
                print("orgao_1 = {}".format(orgao_1))
                print("orgao_2 = {}".format(orgao_2))
                print("orgao_3 = {}".format(orgao_3))
                print("uasg = {}".format(uasg))
                print("pregao = {}".format(pregao))
                print("objeto = {}".format(objeto))
                print("edital = {}".format(edital))
                print("endereco = {}".format(endereco))
                print("telefone = {}".format(telefone))
                print("fax = {}".format(fax))
                print("proposta = {}".format(proposta))
                print("item_servico = {}".format(item_servico.split("\n")[0]))
                print("item_material = {}".format(item_material.split("\n")[0]))
                print("link_download = {}".format(link_download))
                print("url_registro = {}".format(url_registro))

                i = datetime.now()
                registro_dtend = i.strftime('%Y-%m-%d %H:%M:%S')
                #page_source = str(driver.page_source)
                #page_source = page_source.encode('utf-8')
                page_source = driver.page_source
                #page_source = page_source.encode('latin-1')
                #page_source = unicode(page_source.strip(codecs.BOM_UTF8), 'latin-1')
                #page_source = ""

                registros = [
                    id_coleta,
                    numero_registro,
                    cidade,
                    estado,
                    uasg,
                    orgao_1,
                    orgao_2,
                    orgao_3,
                    pregao,
                    objeto,
                    edital,
                    endereco,
                    telefone,
                    fax,
                    proposta,
                    item_material,
                    item_servico,
                    page_source,
                    link_download,
                    url_registro,
                    registro_dtstart,
                    registro_dtend
                ]

                self.insertRegistro(registros)
                self.atualizaColeta(id_coleta, total, numero_registro, registro_dtstart, registro_dtend)


                print
                print("--> Finalizado coleta registro #{} em {} <--".format(numero_registro, registro_dtend))


            form_start = 1



        return  driver

    def insertRegistro(self, registros):
        db = self.db
        #db = MySQLdb.connect("localhost","root","tux","zlicita")
        cursor = db.cursor()
        #var_string = ', '.join("'{}'" * len(registros))
        #var_string = "'{}'," * len(registros)
        #print
        #print len(registros)
        #var_string = var_string[0:len(var_string)-1]
        sql = "INSERT INTO registro "\
              "(id_coleta, numero_registro, cidade, estado, uasg, orgao1, orgao2, orgao3, pregao, objeto, edital, endereco, telefone, fax, proposta, item_material, item_servico, html, link_download, url, data_inicio_coleta, data_fim_coleta)" \
              " VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');" \
              .format(
                registros[0],
                registros[1],
                registros[2],
                registros[3],
                db.escape_string(registros[4]),
                db.escape_string(registros[5]),
                db.escape_string(registros[6]),
                db.escape_string(registros[7]),
                db.escape_string(registros[8]),
                db.escape_string(registros[9]),
                db.escape_string(registros[10]),
                db.escape_string(registros[11]),
                db.escape_string(registros[12]),
                db.escape_string(registros[13]),
                db.escape_string(registros[14]),
                db.escape_string(registros[15]), # item_material
                db.escape_string(registros[16]),
                db.escape_string(registros[17]),
                registros[18],
                registros[19],
                registros[20],
                registros[21]
              )



        #sql = unicode(sql,'iso-8859-1')
        #sql = unicode(sql,'utf-8')
        #sql = sql.decode('utf-8').encode('utf-8')
        #sql = sql.encode('iso-8859-1')
        #sql = sql.encode('utf8')
        #sql = db.escape_string(sql)
        #charset = db.character_set_name()
        #sql = sql.encode(charset)
        #sql = sql.decode('ascii', 'ignore')
        #sql = sql.decode('iso8859-15')
        #sql = unicode(sql,'utf-8')
        #sql = db.escape_string(sql)
        #sql = sql.encode('utf-8')
        #sql = sql.encode('iso-8859-1')


        print(sql)

        cursor.execute(sql)
        db.commit()
        #db.close()


    def tearDown(self):
        self.driver.close()


    def roboLogin(self):
        print("### Efetuando login no sistema ###")

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
              " WHERE  finalizado = 0"
              #" WHERE finalizado = 0"

        cursor.execute(sql)
        results = cursor.fetchall()
        
        lista = []
        for row in results:
            # Now print fetched result
            print("Carregando dia {} ...".format(row[3]))
            item = [row[0],row[1],row[2],row[3]]
            lista.append(item)

        # disconnect from server
        #db.close()

        return lista


if __name__ == "__main__":
    unittest.main()
