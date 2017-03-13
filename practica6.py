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


#HTTPRequestHandler class
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
        #print (data1)
        #event = json.loads(data1)
        event = data1
        return event

    def get_drugs(self):
        #with open("event.json") as f:
            #event = json.load(f)
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
            #print (results.keys())
            #print (results[0])

    def get_main_page(self):
        html = '''
        <html>
            <head>
                <title>OpenFDA Cool App</title>
                </form>
            </head>
            <body>
                <h1>OpenFDA Client</h1>
                <form method="get" action="receive_drugs">
                    <input type="submit" value = "Drug list: Send to OpenFDA">
                    </input>
                </form>
                <form method="get" action="receive_companies">
                    <input type="submit" value= "Companies list: Send to OpenFDA">
                    </input>
                </form>
                <form method="get" action = "search_drugs">
                    <input type="text" name = "drug">
                    </input>
                    <input type="submit" value = "Send drug to OpenFDA">
                    </input>
                </form>
                <form method="get" action="search_company">
                    <input type="text" name= "company">
                    </input>
                    <input type="submit" value = "Send company to OpenFDA">
                    </input>
            </body>

        </html>
        '''
        return html
 #en la prectica 3 sera action search
    def get_second_page(self):
        med_list = self.get_drugs()
        html2 = """
		<html>
        	<head>
				<title>OpenFDA Cool App</title>
			</head>
        	<body>
				<ul>
		"""
        for drug in med_list:
            html2 += "<li>"+drug+"</li>\n"
        html2 += """
				</ul>
            </body>
		</html>
		"""
        return html2

    def get_third_page(self, drug):
        companies_list = self.get_COMPANIES(drug)
        html3 = """
		<html>
        	<head>
				<title>OpenFDA Cool App</title>
			</head>
        	<body>
				<ul>
		"""
        for comp in companies_list:
            html3 += "<li>"+comp+"</li>\n"
        html3 += """
				</ul>
            </body>
		</html>
		"""
        return html3

    def get_fourth_page(self):
        comp_list = self.get_COMPANIES_list()
        html4 = """
		<html>
        	<head>
				<title>OpenFDA Cool App</title>
			</head>
        	<body>
				<ul>
		"""
        for comp in comp_list:
            html4 += "<li>"+comp+"</li>\n"
        html4 += """
				</ul>
            </body>
		</html>
		"""
        return html4

    def get_fifth_page(self,drug):
        drugs_list = self.get_company_search(drug)
        html5 = """
		<html>
        	<head>
				<title>OpenFDA Cool App</title>
			</head>
        	<body>
				<ul>
		"""
        for drug in drugs_list:
            html5 += "<li>"+drug+"</li>\n"
        html5 += """
				</ul>
            </body>
		</html>
		"""
        return html5


    def get_SEARCH_drug(self, drug):
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET", self.OPENFDA_API_EVENT + '?search=patient.drug.medicinalproduct='+ drug +'&limit=10')
        r1 = conn.getresponse()
        print (r1.status, r1.reason)

        data1 = r1.read()
        data1 = data1.decode("utf8")
        #print (data1)
        #event = json.loads(data1)
        event = data1
        return event

    def get_SEARCH_company(self, comp):
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET", self.OPENFDA_API_EVENT + '?search=companynumb:'+ comp +'&limit=10')
        r1 = conn.getresponse()
        print (r1.status, r1.reason)

        data1 = r1.read()
        data1 = data1.decode("utf8")
        #print (data1)
        #event = json.loads(data1)
        event = data1
        return event

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

        '''main_page = False
        is_event = False
        if self.path == '/' :
            main_page = True
        elif self.path == "/receive?":
            is_event = True'''
        # Send response status code: el 200 significa todo bien
        self.send_response(200)

        #Send Headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        #html = self.get_main_page()

        # Send message back to client
        #message = "hello world!" + self.path

        #write content as utf-8 data
        #event = "EVENTO"
        if self.path == '/':
            html = self.get_main_page()
            self.wfile.write(bytes(html, "utf8")) #wfile es un fichero enganchado con el cliente

        elif self.path == '/receive_drugs?':
            html2 = self.get_second_page()
            print (html2)
            self.wfile.write(bytes(html2, "utf8"))

        elif "/search_drugs?" in self.path:
            url = self.path
            drug= url.split("=")[-1]
            html3 = self.get_third_page(drug)
            self.wfile.write(bytes(html3, "utf8"))

        elif self.path == '/receive_companies?':
            html4 = self.get_fourth_page()
            print (html4)
            self.wfile.write(bytes(html4, "utf8"))

        elif "/search_company?" in self.path:
            url = self.path
            drug= url.split("=")[-1]
            html5 = self.get_fifth_page(drug)
            self.wfile.write(bytes(html5, "utf8"))

        return
