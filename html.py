import csv

def generate_html_page(csv_file):

    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]


    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Web static page</title>
    </head>
    <body>
        <h1>List of devices failing</h1>
        <ul>
    """
    
    for row in data:
        if row["device_id"] == "no_id_for_this_device":
            continue
        url = row["URL"]
        device_id = row["device_id"]
        html_code += f"<li><a href={url}> {device_id}</a></li>"
    
    html_code += """
        </ul>
    </body>
    </html>
    """
        
    with open("result.html", 'w', encoding='utf-8') as htmlfile:
        htmlfile.write(html_code)

    print("html printed with success")