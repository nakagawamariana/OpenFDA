# Busqueda de medicamentos
# Copyright (C) 2017  Mariana Nakagawa

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>

import http.server
import http.client
import json
import socketserver

class testHTTPRequestHandler (http.server.BaseHTTPRequestHandler):

    OPENFDA_API_URL = "api.fda.gov"
    OPENFDA_API_EVENT = "/drug/event.json"


    def get_event(self):
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET", self.OPENFDA_API_EVENT + "?limit=10")
        r1 = conn.getresponse()
        print (r1.status, r1.reason)
        data1 = r1.read()
        data1 = data1.decode("utf8")
        event = data1
        return event

    def get_SEARCH_drug(self, drug):
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET", self.OPENFDA_API_EVENT + '?search=patient.drug.medicinalproduct='+ drug +'&limit=10')
        r1 = conn.getresponse()
        print (r1.status, r1.reason)
        data1 = r1.read()
        data1 = data1.decode("utf8")
        event = data1
        return event

    def get_SEARCH_company(self, comp):
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET", self.OPENFDA_API_EVENT + '?search=companynumb:'+ comp +'&limit=10')
        r1 = conn.getresponse()
        print (r1.status, r1.reason)
        data1 = r1.read()
        data1 = data1.decode("utf8")
        event = data1
        return event

    def get_main_page(self):
        html = '''
        <html>
            <head>
                <title>OpenFDA Cool App</title>
                </form>
            </head>
            <body>
                <h1>OpenFDA Client</h1>
                <form method="get" action="listDrugs">
                    <input type="submit" value = "Drug list: Send to OpenFDA">
                    </input>
                </form>
                <form method="get" action="listCompanies">
                    <input type="submit" value= "Companies list: Send to OpenFDA">
                    </input>
                </form>
                <form method="get" action = "searchDrug">
                    <input type="text" name = "drug">
                    </input>
                    <input type="submit" value = "Send drug to OpenFDA">
                    </input>
                </form>
                <form method="get" action="searchCompany">
                    <input type="text" name= "company">
                    </input>
                    <input type="submit" value = "Send company to OpenFDA">
                    </input>
            </body>

        </html>
        '''
        return html

    def get_second_page(self,items):
        med_list = items
        html2 = """
		<html>
        	<head>
				<title>OpenFDA Cool App</title>
			</head>
        	<body>
				<ol>
		"""
        for drug in med_list:
            html2 += "<li>"+drug+"</li>"
        html2 += """
				</ol>
            </body>
		</html>
		"""
        return html2

    def get_drugs(self):
        med_list = []
        data2 = self.get_event()
        events = json.loads(data2)
        results =events["results"]
        for i in range(10):
            patient = results[i]["patient"]
            drug = patient["drug"]
            med_prod = drug[0]["medicinalproduct"]
            med_list.append(med_prod)
        return med_list

    def get_COMPANIES(self,drug):
        event = self.get_SEARCH_drug(drug)
        companies_list = []
        info = json.loads(event)
        results = info["results"]
        for event in results:
            companies_list += [event ['companynumb']]
        return companies_list

    def get_COMPANIES_list(self):
        event = self.get_event()
        companies_list = []
        info = json.loads(event)
        results = info["results"]
        for event in results:
            companies_list += [event ['companynumb']]
        return companies_list

    def get_company_search(self,drug):
        event = self.get_SEARCH_company(drug)
        drugs_list = []
        info = json.loads(event)
        results = info["results"]
        for event in results:
            drugs_list += [event["patient"]["drug"][0]["medicinalproduct"]]
        return drugs_list

    def do_GET (self): #self - peticion del cliente
        self.send_response(200) #header
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        if self.path == '/':
            html = self.get_main_page()
            self.wfile.write(bytes(html, "utf8")) #wfile es un fichero enganchado con el cliente

        elif '/listDrugs' in self.path:
            items=self.get_drugs()
            html = self.get_second_page(items)
            self.wfile.write(bytes(html, "utf8"))

        elif "searchDrug?drug=" in self.path:
            url = self.path
            drug= url.split("=")[-1]
            items= self.get_COMPANIES(drug)
            html = self.get_second_page(items)
            self.wfile.write(bytes(html, "utf8"))

        elif '/listCompanies' in self.path:
            items = self.get_COMPANIES_list()
            html = self.get_second_page(items)
            self.wfile.write(bytes(html, "utf8"))

        elif "searchCompany?company=" in self.path:
            url = self.path
            drug= url.split("=")[-1]
            items = self.get_company_search(drug)
            html = self.get_second_page(items)
            self.wfile.write(bytes(html, "utf8"))

        return

