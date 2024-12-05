from flask import Flask, render_template, make_response, redirect, request
from jinja2 import Environment, FileSystemLoader # used for direct template use
from datetime import datetime
import requests # used to send request over HTTPS
import os       # used to get environment variables and read files
import re       # used to extract the url from the SIGNiX submit document request
import html     # used to unescape the url returned by SIGNiX
from signer_data_initialize import signer_data_create
from form_data_initialize import form_data_create
from tx_data_initialize import tx_data_create

# Set up environment for Flask and the Jinja templating system
app = Flask(__name__)
env = Environment(loader=FileSystemLoader('templates'))

# Initialize signer and form data
signer_data = signer_data_create()
form_data = form_data_create()

# Populate the form template with form data
form_template = env.get_template("lease-termination-form_assignedFields.xml")
rendered_form = form_template.render(data=form_data)

# Combine the transaction data with signer data and the rendered form
tx_data = tx_data_create(signer_data, rendered_form)

@app.route("/")
def home():
    # Update transactionId with current time, to make it unique
    now = datetime.now()
    formatted_now = now.strftime('%Y-%m-%d %H:%M:%S:%f')[:-3]
    tx_data['transaction_data']['transactionId'] = "ZoomJPakLTerm" + formatted_now
    
    # Generate transaction request using combined transaction data, signer data and rendered form
    tx_template = env.get_template("tx-and-signers.xml")
    rendered_tx = tx_template.render(data=tx_data)
    transaction_request = {'method': 'SubmitDocument', 'request': rendered_tx}

    # Submit transaction to SIGNiX
    url = os.getenv('signix_service_url')
    response = requests.post(url, data=transaction_request)

    # print(response.text)

    signer_escaped_url = re.search('<PickupLink>(.*?)</PickupLink>', response.text).group(1)
    signer_url = html.unescape(signer_escaped_url)

    return redirect(signer_url)

if __name__ == "__main__":
        app.run(debug=True)