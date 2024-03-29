import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Downloader:
  def __init__(self, session_id, token, domain) -> None:
    self.session_id = session_id
    self.token = token
    self.domain = domain
    self.driver = webdriver.Firefox()
  

  def download_subjects(self, career: str = None,
                        career_plan: str = None,
                        plan_period: str = None):

      self.driver.get(f'https://{self.domain}/')

      cookies = [
          {'name': '.ASPXFORMSAUTH', 'value': self.token, 'domain': self.domain},
          {'name': 'ASP.NET_SessionId', 'value': self.session_id, 'domain': self.domain},
          {'name': 'AspxAutoDetectCookieSupport', 'value': '1', 'domain': self.domain},
      ]

      for cookie in cookies:
        self.driver.add_cookie(cookie)
        
      self.driver.refresh()
      time.sleep(2)
      element_academica = self.driver.find_element(By.XPATH, '//a[@href="/Academica/default.aspx"]')
      element_academica.click()
      time.sleep(4)

      element_mapa_curricular = self.driver.find_element(By.XPATH, '//a[@href="/Academica/mapa_curricular.aspx"]')
      element_mapa_curricular.click()
      time.sleep(4)
    
      carreras_disponibles = [option.get_attribute("value") for option in Select(self.driver.find_element(By.ID, 'ctl00_mainCopy_Filtro_cboCarrera')).options]

      if career:
        assert career in carreras_disponibles
        carreras_disponibles = [career]
      
      for carrera in carreras_disponibles:
        carrera_dropdown = Select(self.driver.find_element(By.ID, 'ctl00_mainCopy_Filtro_cboCarrera'))
        carrera_dropdown.select_by_value(carrera)
        
        planes_disponibles = [option.get_attribute("value") for option in Select(self.driver.find_element(By.ID, 'ctl00_mainCopy_Filtro_cboPlanEstud')).options]

        if career_plan:
          assert career_plan in planes_disponibles
          planes_disponibles = [career_plan]

        for plan in planes_disponibles:
          plan_dropdown = Select(self.driver.find_element(By.ID, 'ctl00_mainCopy_Filtro_cboPlanEstud'))
          plan_dropdown.select_by_value(plan)
          
          
          periodos_disponibles = [option.get_attribute("value") for option in Select(self.driver.find_element(By.ID, 'ctl00_mainCopy_Filtro_lsNoPeriodos')).options]

          if plan_period:
            assert plan_period in periodos_disponibles
            periodos_disponibles = [plan_period]

          for periodo in periodos_disponibles:
            periodo_dropdown = Select(self.driver.find_element(By.ID, 'ctl00_mainCopy_Filtro_lsNoPeriodos'))
            periodo_dropdown.select_by_value(periodo)
            
            pagina_html = self.driver.page_source
            
            try:
              path = f'downloads/subjects/{carrera}/{plan}/'
              os.makedirs(path)
            except FileExistsError:
              pass  
              
            try:
              with open(f'{path}/{periodo}.html', 'w', encoding='utf-8') as archivo:
                archivo.write(pagina_html)
            except FileExistsError:
              pass
                
            time.sleep(4)
        self.driver.close()
        


  def download_schedules(self, career: str = None,
                        career_plan: str = None,
                        plan_period: str = None,
                        shift: str = None,
                        sequence: str = None) -> None:
      self.driver.get(f'https://{self.domain}/')

      cookies = [
          {'name': '.ASPXFORMSAUTH', 'value': self.token, 'domain': self.domain},
          {'name': 'ASP.NET_SessionId', 'value': self.session_id, 'domain': self.domain},
          {'name': 'AspxAutoDetectCookieSupport', 'value': '1', 'domain': self.domain},
      ]

      for cookie in cookies:
        self.driver.add_cookie(cookie)
        
      self.driver.refresh()
      time.sleep(2)
      element_academica = self.driver.find_element(By.XPATH, '//a[@href="/Academica/default.aspx"]')
      element_academica.click()
      time.sleep(4)
      
      horarios_link = self.driver.find_element(By.XPATH, "//a[contains(text(), 'Horarios de Clases')]")
      horarios_link.click()
      time.sleep(4)
      
      
      carreras_disponibles = [option.get_attribute("value") for option in Select(self.driver.find_element(By.ID, 'ctl00_mainCopy_Filtro_cboCarrera')).options]

      if career:
        assert career in carreras_disponibles
        carreras_disponibles = [career]
      
      for carrera in carreras_disponibles:
        time.sleep(4)
        
        carrera_select = Select(self.driver.find_element(By.ID, 'ctl00_mainCopy_Filtro_cboCarrera'))
        carrera_select.select_by_value(carrera)

        planes_disponibles = [option.get_attribute("value") for option in Select(self.driver.find_element(By.ID, 'ctl00_mainCopy_Filtro_cboPlanEstud')).options]

        if career_plan:
          assert career_plan in planes_disponibles
          planes_disponibles = [career_plan]
        
        for plan in planes_disponibles:
          time.sleep(4)
          plan_estudio_select = Select(self.driver.find_element(By.ID, 'ctl00_mainCopy_Filtro_cboPlanEstud'))
          plan_estudio_select.select_by_value(plan)
          
          periodos_disponibles = [option.get_attribute("value") for option in Select(self.driver.find_element(By.ID, 'ctl00_mainCopy_Filtro_lsNoPeriodos')).options]

          if plan_period:
            assert plan_period in periodos_disponibles
            periodos_disponibles = [plan_period]
            
          for periodo in periodos_disponibles:
            time.sleep(4)
            periodo_select = Select(self.driver.find_element(By.ID, 'ctl00_mainCopy_Filtro_lsNoPeriodos'))
            periodo_select.select_by_value(periodo)
            
            turnos_disponibles = [option.get_attribute("value") for option in Select(self.driver.find_element(By.ID, 'ctl00_mainCopy_Filtro_cboTurno')).options]

            if shift:
              assert shift in turnos_disponibles
              turnos_disponibles = [shift]
              
            for turno in turnos_disponibles:
              time.sleep(4)
              turno_select = Select(self.driver.find_element(By.ID, 'ctl00_mainCopy_Filtro_cboTurno'))
              turno_select.select_by_value(turno)
              
              secuencias_disponibles = [option.get_attribute("value") for option in Select(self.driver.find_element(By.ID, 'ctl00_mainCopy_lsSecuencias')).options]
              if sequence:
                assert sequence in secuencias_disponibles
                secuencias_disponibles = [sequence]
                
              for secuencia in secuencias_disponibles:
                time.sleep(4)
                if secuencia == 'Todo':
                  continue
                
                secuencia_select = Select(self.driver.find_element(By.ID, 'ctl00_mainCopy_lsSecuencias'))
                secuencia_select.select_by_value(secuencia)
                
                pagina_html = self.driver.page_source
          
                try:
                  path = f'downloads/schedules/{carrera}/{plan}/{periodo}/{turno}'
                  os.makedirs(path)
                except FileExistsError:
                  pass  
                  
                try:
                  with open(f'{path}/{secuencia}.html', 'w', encoding='utf-8') as archivo:
                    archivo.write(pagina_html)
                except FileExistsError:
                  pass
      
      self.driver.close()

  def download_availability(self, career: str = None, career_plan: str = None):
      self.driver.get(f'https://{self.domain}/')

      cookies = [
          {'name': '.ASPXFORMSAUTH', 'value': self.token, 'domain': self.domain},
          {'name': 'ASP.NET_SessionId', 'value': self.session_id, 'domain': self.domain},
          {'name': 'AspxAutoDetectCookieSupport', 'value': '1', 'domain': self.domain},
      ]

      for cookie in cookies:
        self.driver.add_cookie(cookie)
        
      self.driver.refresh()
      time.sleep(2)

      element_academica = self.driver.find_element(By.XPATH, '//a[@href="/Academica/default.aspx"]')
      element_academica.click()
      time.sleep(4)

      ocupabilidad_link = self.driver.find_element(By.XPATH, '//a[@href="/Academica/Ocupabilidad_grupos.aspx"]')
      ocupabilidad_link.click()
      time.sleep(4)
      
      radio_button = WebDriverWait(self.driver, 10).until(
          EC.presence_of_element_located((By.ID, 'ctl00_mainCopy_rblEsquema_0'))
      )

      radio_button.click()
      
      carreras_disponibles = [option.get_attribute("value") for option in Select(self.driver.find_element(By.ID, 'ctl00_mainCopy_dpdcarrera')).options]

      if career:
        assert career in carreras_disponibles
        carreras_disponibles = [career]
        
      for carrera in carreras_disponibles:
        time.sleep(4)
        carrera_dropdown = Select(self.driver.find_element(By.ID, 'ctl00_mainCopy_dpdcarrera'))
        carrera_dropdown.select_by_value(carrera)
        
        planes_disponibles = [option.get_attribute("value") for option in Select(self.driver.find_element(By.ID, 'ctl00_mainCopy_dpdplan')).options]

        if career_plan:
          assert career_plan in planes_disponibles
          planes_disponibles = [career_plan]
          
        for plan in planes_disponibles:
          time.sleep(4)
          plan_dropdown = Select(self.driver.find_element(By.ID, "ctl00_mainCopy_dpdplan"))
          plan_dropdown.select_by_value(plan)
          
          pagina_html = self.driver.page_source
          
          try:
            path = f'downloads/availability/{carrera}/{plan}'
            os.makedirs(path)
          except FileExistsError:
            pass  
            
          try:
            with open(f'{path}/{datetime.now()}.html', 'w', encoding='utf-8') as archivo:
              archivo.write(pagina_html)
          except FileExistsError:
            pass
          
      self.driver.close()
        

      

      
      
 
                
            
          