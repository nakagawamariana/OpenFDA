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

class OpenFDAClient():

    OPENFDA_API_URL = "api.fda.gov"
    OPENFDA_API_EVENT = "/drug/event.json"

    def get_event(self, limit):
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET", self.OPENFDA_API_EVENT + "?limit=" + limit)
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

class OpenFDAParser():

    def get_drugs(self,limit):
        client = OpenFDAClient()
        data2 = client.get_event(limit)
        med_list = []
        events = json.loads(data2)
        results =events["results"]
        for i in results:
            patient = i["patient"]
            drug = patient["drug"]
            med_prod = drug[0]["medicinalproduct"]
            med_list.append(med_prod)
        return med_list

    def get_COMPANIES(self,drug):
        client = OpenFDAClient()
        event = client.get_SEARCH_drug(drug)
        companies_list = []
        info = json.loads(event)
        results = info["results"]
        for event in results:
            companies_list += [event ['companynumb']]
        return companies_list

    def get_COMPANIES_list(self,limit):
        client = OpenFDAClient()
        event = client.get_event(limit)
        companies_list = []
        info = json.loads(event)
        results = info["results"]
        for event in results:
            companies_list += [event ['companynumb']]
        return companies_list

    def get_company_search(self,drug):
        client = OpenFDAClient()
        event = client.get_SEARCH_company(drug)
        drugs_list = []
        info = json.loads(event)
        results = info["results"]
        for event in results:
            drugs_list += [event["patient"]["drug"][0]["medicinalproduct"]]
        return drugs_list

    def get_genders(self,limit):
        client = OpenFDAClient()
        event = client.get_event(limit)
        number_list = []
        gender_list = []
        info = json.loads(event)
        results = info['results']
        for number in results:
            number_list += [number['patient']['patientsex']]
        for number in number_list:
            if number =="1":
                gender_list.append("Male")
            elif number == "2":
                gender_list.append("Female")
            elif number == "0":
                gender_list.append("Unknown")
        return gender_list
	
class OpenFDAHTML():

    def get_main_page(self):
        html = '''
        <html>
            <head>
                <link rel="shortcut icon" href="https://pbs.twimg.com/profile_images/701113332183371776/57JHEzt7.jpg">
                <title>OpenFDA Cool App</title>
                </form>
            </head>
            <body>
                <h1>OpenFDA Client</h1>
                <form method="get" action="listDrugs">
                    <input type="submit" value = "Drug list: Send to OpenFDA">
                    </input>
                    Limit: <input type="text" name = "limit" size="5">
                    </input>
                </form>
                <form method="get" action="listCompanies">
                    <input type="submit" value= "Companies list: Send to OpenFDA">
                    </input>
                    Limit: <input type="text" name = "limit" size="5">
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
                   
				</form>
				<form method="get" action="GenderList">
					<input type = "submit" value= "Gender List: Send to OpenFDA">
					</input>
					Limit: <input type= "text" name = "limit" size ="5">
					</input>
				</form>
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

    def get_error_page(self):
        html3 = """
            <html>
                <head>
                    <body>
                        <h1>Error 404</h1>
                    <body>
                </head>
                    <body>
                        Page not found
                    </body>
            </html>
        """
        return html3

class testHTTPRequestHandler (http.server.BaseHTTPRequestHandler):
    def execute(self,html):
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(bytes(html, "utf8"))

    def do_GET (self): #self - peticion del cliente

        if self.path == '/':
            self.send_response(200)
            HTML = OpenFDAHTML()
            html = HTML.get_main_page()
            self.execute(html) #wfile es un fichero enganchado con el cliente

        elif '/listDrugs' in self.path:
            self.send_response(200)
            HTML = OpenFDAHTML()
            parser = OpenFDAParser()
            limit = self.path.split("=")[-1]
            items=parser.get_drugs(limit)
            html = HTML.get_second_page(items)
            self.execute(html)

        elif "searchDrug?drug=" in self.path:
            self.send_response(200)
            HTML = OpenFDAHTML()
            parser = OpenFDAParser()
            drug = self.path.split("=")[-1]
            items= parser.get_COMPANIES(drug)
            html = HTML.get_second_page(items)
            self.execute(html)

        elif '/listCompanies' in self.path:
            self.send_response(200)
            HTML = OpenFDAHTML()
            parser = OpenFDAParser()
            limit = self.path.split("=")[-1]
            items = parser.get_COMPANIES_list(limit)
            html = HTML.get_second_page(items)
            self.execute(html)

        elif "searchCompany?company=" in self.path:
            self.send_response(200)
            HTML = OpenFDAHTML()
            parser = OpenFDAParser()
            drug = self.path.split("=")[-1]
            items = parser.get_company_search(drug)
            html = HTML.get_second_page(items)
            self.execute(html)

        elif "/GenderList" in self.path:
            self.send_response(200)
            HTML = OpenFDAHTML()
            parser = OpenFDAParser()
            limit = self.path.split("=")[-1]
            items = parser.get_genders(limit)
            html = HTML.get_second_page(items)
            self.execute(html)

        elif "/secret" in self.path:
            self.send_response(401)
            self.send_header('WWW-Authenticate','Basic realm="User Visible Realm"')
            self.end_headers()

        elif "/redirect" in self.path:
            self.send_response(302)
            self.send_header('Location', 'http://localhost:8001/')
            self.end_headers()

        else:
            HTML = OpenFDAHTML()
            self.send_response(404)
            html= HTML.get_error_page()
            self.wfile.write(bytes(html, "utf8"))

        return
