import africastalking


# Initialize SDK
username = "sandbox"    # use 'sandbox' for development in the test environment
api_key = "023b2739b4c9e880b6d2f2dc0b6acc55e66415b82bc6fcb55c359873e1374606"      # use your sandbox app API key for development in the test environment
africastalking.initialize(username, api_key)


# Initialize a service e.g. SMS
sms = africastalking.SMS


# Use the service synchronously
response = sms.send(message="Starting with the word NAME", recipients=["+254721649416"], sender_id= "20635", enqueue = False)

# response = sms.send_premium( message ="Starting with the word NAME, please enter your full names, using the format below: \n NAME FIRSTNAME LASTNAME i.e ( NAME JOHN DOE) ", 
#                             short_code= "20635",
#                             recipients= ["+254721649416"],
                            

#    )
print(response)



