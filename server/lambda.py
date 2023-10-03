import http.server
import json
import base64
from PyPDF2 import PdfMerger
from io import BytesIO


class RequestHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)

    def do_POST(self):
        if self.path == '/mergefiles':
            # Read the post data
            try: 
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
            
                data = json.loads(post_data)

                print(data.keys())

                # Check if "files" is a key in data
                if "files" not in data:
                    response = {'status': 'Bad Request', 'message': 'files key not found.'}
                    self.send_response(400)
                # Check if all the files in data["files"] are PDF files presented as dataURL
                elif not isinstance(data["files"], list) or not len(data["files"]) <= 5 or len(data["files"]) <= 1:
                    response = {'status': 'Bad Request', 'message': 'At least 2 and up to 5 files are required'}
                    self.send_response(400)
                # Check if all the files in data["files"] are PDF files presented as dataURL
                elif not all([file['document'].startswith("data:application/pdf;base64,") for file in data["files"]]):
                    response = {'status': 'Bad Request', 'message': 'All files must be pdf files.'}
                    self.send_response(400)
                else:
                    # Create a merger object
                    pdf_merger = PdfMerger()

                    for file_data in data['files']:
                        # Extract the base64 encoded PDF content from the dataURL
                        pdf_content = base64.b64decode(file_data['document'].split(",")[1])
                        pdf_merger.append(BytesIO(pdf_content))

                    # Merge the PDF files into a single PDF document
                    merged_pdf_bytes = BytesIO()
                    pdf_merger.write(merged_pdf_bytes)
                    merged_pdf_bytes.seek(0)

                    # Prepare the response
                    response = {
                        'status': 'Success',
                        'message': 'PDF files merged successfully.',
                        'merged_file': base64.b64encode(merged_pdf_bytes.read()).decode()
                    }
                    self.send_response(200)

                self.send_header('Access-Control-Allow-Origin', 'http://localhost:3000')
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
            except Exception as e:
                response = {'status': 'Bad Request', 'message': str(e)}
                self.send_response(400)
                self.send_header('Access-Control-Allow-Origin', 'http://localhost:3000')
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', 'http://localhost:3000')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, RequestHandler)
    print(f'Starting server on {server_address[0]}:{server_address[1]}')
    httpd.serve_forever()