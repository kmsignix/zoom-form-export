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