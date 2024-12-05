# Form Export Demonstration, powered by SIGNiX
![SIGNiX (4c) (Custom)](https://github.com/user-attachments/assets/af5bbf18-ee52-41b3-9637-cd28c5537ac4)

[SIGNiX](https://www.signix.com/) digital signature platform has a Form Export feature for exporting
a tagged PDF for data and signature collection, plus XML describing the form configuration, for use
with an API call.

## Description
This project contains files and source code for a simple web application as a showcase and tutorial for
the SIGNiX Form Export feature.

## About Form Export
Form Export is a feature introduced with Release 177 of the SIGNiX platform, in January 2025.

The feature enables tagged PDFs and a form configuration to be exported from SIGNiX MyDoX. This means
PDFs can be uploaded to MyDoX and tagged with data fields and signature fields using the portal's UI. Then
the document can be exported as a tagged PDF, complete with fields in PDF format. Also included in the 
export is an XML description of document fields and a Base64 encoded version of the document. The XML is in
the same format as the **Form** element in the **SubmitDocument** API call, allowing the file to be used as a 
template when submitting transactions to SIGNiX via the Flex API.

The Form Export feature is therefore a great boost to developers integrating with the SIGNiX API.

![001-exported-pdf-and-xml](https://github.com/user-attachments/assets/c9d82766-2d55-46dc-a317-b517d9bccee1)


## Works Great For Forms With Static Layout

Many forms have the same layout from transaction to transaction. This means the locations of data and signature
fields are the same on every document. The Form Export feature enables those tags to be simply and 
quickly placed using the MyDoX UI. No additional third-party software (e.g. Adobe Acrobat) is needed to tag
the documents.

Data fields on a PDF can be prepopulated using values provided when the transaction is submitted via the API. 
This provides a simple way to generate documents and share documents with personalized content, as shown in 
this sample application.

![002-populated-and-signed-form](https://github.com/user-attachments/assets/dccbb084-b09a-451f-be50-77bca11c6faa)


Some documents have dynamic content, where the layout reflows accordingly. For those documents, use SIGNiX 
Text Tagging. See the demo and sample code for Text Tagging in this GitHub repository: 
[zoom-jet-packs](https://github.com/kmsignix/zoom-jet-packs).

## Table of Contents
- Installation
- Usage
- Code Structure and Explanation
- Contributing
- License
- Contact

## Installation
Steps to install the project.

1. Clone the repository:
   ```bash
   git clone https://github.com/kmsignix/zoom-transaction-export
2. Navigate to the project directory:
   ```bash
   cd zoom-transaction-export
3. Create a Python virtual environment and activate it. For example:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
4. Install the dependencies:
   ```bash
   pip install -r requirements.txt
5. Set up environmental variables. This project uses environment variables to contain credentials and signer-specific data (so they don't appear in code). In VSC, these can be put in the `launch.json` file. For example:
   ```json
   "env": {
                "FLASK_APP": "app.py",
                "FLASK_DEBUG": "1",
                "signix_service_url": "{{SERVICE_URL}}",
                "sponsor": "{{YOUR_SPONSOR_NAME}}", 
                "client": "{{YOUR_CLIENT_NAME}}", 
                "user_id": "{{USERNAME}}", 
                "pswd": "{{PASSWORD}}", 
                "workgroup": "SDD", 
                "demo": "yes",
                "del_docs_after": "60", 
                "email_content": "Your documents for the Sample Application are available online for viewing and signing.",
                "submitter_first_name": "{{YOUR_FIRST_NAME}}",
                "submitter_last_name": "{{YOUR_LAST_NAME}}",
                "submitter_email": "{{YOUR_EMAIL}}",
                "signer1_email": "{{YOUR_OTHER_EMAIL}}",
                "signer1_mobile_number": "{{YOUR_MOBILE_NUMBER}}"
            },

## Usage
Running the application can be done in the VSC debug module, or otherwise. Port 5000 will be opened 
(typically on localhost), and will serve pages to a web browser. As soon as the page is opened, the
form is populated with data and a transaction is sent to the SIGNiX platform via the API. The SIGNiX
platform responds with a link to the signing experience, where the user can view the document and
sign it.

![003-signix-signing-experience](https://github.com/user-attachments/assets/5ead2d12-baeb-4b61-a9f0-2bc29015c37c)

The scenario for this demonstration relates to a fictional company named Zoom Jet Packs. Specifically,
a form was created in Microsoft Word to summarize fees due at the end of a lease. Zoom Jet Packs calculates
the fees and requires the lessee to sign to acknowledge the details.

### How It Works

Once the document was exported to PDF using the built-in Microsoft Word feature, it was uploaded to SIGNiX MyDoX.

Using MyDoX, the form was tagged with data fields and signature fields. The fields were given values enclosed with
{{ and }}, which is a standard notation for data point placeholders for template engines (e.g. for Jinja, as used here).

The transaction was then exported from MyDoX in a zip file, and the XML file was put in the **templates** folder of
the project repository. The use of {{ and }} notation enables the XML file to be used unmodified as a template. The
XML file also includes a rendition of the tagged PDF in Base64 format, which is required by the SIGNiX Flex API
when creating transactions and uploading documents.

The web application is written in **Python** using **Flask**, and **Jinja** (which is included in the Flash module) 
is used to populate the template with document data. Given the exported XML is in the correct format for 
describing form elements of a transaction creation API call, the result can then be incorporated into another
template that adds transaction metadata and signer information.

```python
# Populate the form template with form data
form_template = env.get_template("lease-termination-form_assignedFields.xml")
rendered_form = form_template.render(data=form_data)

# Combine the transaction data with signer data and the rendered form
tx_data = tx_data_create(signer_data, rendered_form)

# Generate transaction request using combined transaction data, signerdata  and rendered form
tx_template = env.get_template("tx-and-signers.xml")
rendered_tx = tx_template.render(data=tx_data)
```

The entire body of the **SubmitDocument** Flex API call is therefore created / poplulated with templates using
Jinja, before being sent to SIGNiX using the Python **requests** module. The response from the API includes a link
to the signing experience, which is extracted using a regular expression and passed to the browser via a redirect.
```python
# Submit transaction to SIGNiX
url = os.getenv('signix_service_url')
response = requests.post(url, data=transaction_request)

signer_escaped_url = re.search('<PickupLink>(.*?)</PickupLink>', response.text).group(1)
signer_url = html.unescape(signer_escaped_url)

return redirect(signer_url)
```

## Code Structure and Explanation

**Documents** folder contains the Microsft Word file used to create the form. The folder also includes the PDF
that was generated by exporting the document to PDF using the feature in Microsoft Word.

**Templates** folder contains the XML exported from the **Form Export** feature of MyDoX 
("lease-termination-form_assignedFields.xml"). This is the unmodified file included in the zip file from the export.
The folder includes another template ("tx-and-signers.xml") that is used to hold the form created from the first 
template and into which transaction metadata and signer information is added.

**app.py** is the source for the Flask app. It has a single route defined ("/"), which, when opened, creates a
SIGNiX transaction and redirects to the signing experience.

**initialize.py** files contain data that populates the templates. This includes the form_data_initialize.py file,
as below.
```python
# This function is used to create an object that is used to populate 
# the lease termination form

def form_data_create():
    form_data = {
        "name": "Max Fun",
        "phone": "555-123-4567",
        "email": "signer1@example.com",
        "address1": "123 Main St",
        "address2": "Unit 3202",
        "cityStateZip": "Houston, TX 77001",
        "leaseStartDate": "12/02/2021",
        "leaseEndDate": "12/01/2024",
        "model": "Skyward P-2021",
        "jpin": "4CH8P4K7E3X6Z9R2V",
        "wearAndTear": "Dent on left fuel tank",
        "wearAndTearCost": "$1,867",
        "hoursAllowed": "3,000",
        "hoursFlown": "3,102",
        "hoursOverage": "102",
        "hourlyOverageRate": "$29",
        "overageCost": "$2,958",
        "chargesOther": "Collection from customer home",
        "chargesOtherAmount": "$250",
        "totalAmountDue": "$5,075"
    }

    return form_data
```

## Contributing
Guidelines for contributing coming soon.

## License
This project is distributed under the MIT license. See the LICENSE.txt file for details.

## Contact
Contact information coming soon.
