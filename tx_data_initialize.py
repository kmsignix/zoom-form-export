# This function is used to create a transaction
import os    # used to get environment variables

def tx_data_create(signer_data, rendered_form):

    tx_data = {
        "cust_info": {
            "sponsor": os.getenv('sponsor'),
            "client": os.getenv('client'),
            "userId": os.getenv('user_id'),
            "password": os.getenv('pswd'),
            "workgroup": os.getenv('workgroup'),
            "demo": os.getenv('demo'),
            "del_docs_after": os.getenv('del_docs_after'),
            "email_content": os.getenv('email_content')
        },
        "transaction_data": {
            "transactionId": "ZoomJPakLTerm",
            "doc_set_description": "Zoom Jet Pack Lease Termination Acknowledgement",
            "filename": "leaseterm.zip",
            "contact_info": "If you have a question, please contact " + 
                signer_data['submitter']['name'] + " at " + 
                signer_data['submitter']['phone'],
            "delivery_type": "SDDDC",
            "suspend_on_start": "no"
        },
        "submitter": {
            "email": signer_data['submitter']['email'],
            "name": signer_data['submitter']['name']
        },
        "signers": signer_data['signers'],
        "form": rendered_form
    }

    return tx_data