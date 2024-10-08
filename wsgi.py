from flask import Flask, render_template, request, redirect, url_for
from requests.exceptions import HTTPError, Timeout, ConnectionError, RequestException
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import json
import webbrowser
import os
import subprocess
import signal
import sys
import time

app = Flask(__name__)
print("IVAC Auto Appointment Script is written by Partho Biswas")
print("Version: beta 02/10/2024")
def otp_slot_time(web_id, name, phone, email, otp):  
    # Start Example otp usage
    XSRFTOKEN = "eyJpdiI6IlwvcmRLS3c3a2liRDVST3cxVVpmcFJRPT0iLCJ2YWx1ZSI6ImU5MWJHZWxMaWphYlFZMW1EMHhHOSswZ3dDOFZBajlOWXZZbmZabVNOWXM1WmRLNVdIXC83d1RCRlFlSGFIemJCIiwibWFjIjoiZjNjMDU3MDU1OWI4MGQzOTY0N2Y2NGE2MzgxZjg2NGY3NTg5ZDE4Yzc5OGM5NzdkODM2ZjEwZTlmMzc1NGQ0YiJ9"
    ivac_session = "eyJpdiI6IkRhTEhWZFJ6V2tuRmlXTHg1Z09kdlE9PSIsInZhbHVlIjoiYTVNMWMwVlwvaUUwR1paWFlWMWlsS2U3bW9NNFYrcW5UVFFKZng5T1pFK0VEZzkxSFFlTTJTNVhkVlwvd0ZGVFgrIiwibWFjIjoiMjcxNWMzNGUyMWUzNWM0ZjE0ZThhZGNjNGM4MjlmNmZhNzY3N2YzMDU1MDQ3OTQ0OTY3NzJiMjNlYjNiN2MxMiJ9"
    cookies = {
        "_ga": "GA1.2.459466864.1727920228",
        "_gid": "GA1.2.2134581214.1728314495",
        "_gat_gtag_UA_32646854_3": "1",
        "_ga_9CCL5E3W1W": "GS1.1.1728322331.9.0.1728322331.60.0.0",
        "XSRF-TOKEN": XSRFTOKEN,
        "ivac_session": ivac_session
    }
    token = "gQvftpzJA3mUq3XUxZ8hUtrCmc2q3ZYcPCStieAA"  # Replace with actual token
    web_id = web_id  # Replace with actual web ID
    name = name  # Replace with actual name
    phone = phone  # Replace with actual phone number
    email = email  # Replace with actual email address
    otp = otp
    specific_date = "2024-10-09"
    best_time_slotid = ""
    best_time_slothour = ""
    best_time_slotdate = specific_date
    best_time_slotavslot = ""
    best_time_slottdisplay = ""
    response_data = ""
    print(web_id+" "+name+" "+phone+" "+email+" "+otp)
    url = "https://payment.ivacbd.com/api/v1/queue-manage"
    print("Expeted Appointment :"+specific_date)
    def input_otp_and_run_again():
        # You can add logic here to re-run the OTP input if needed
        otpe = input("Re-enter the OTP sent to your phone: ")
        check_otp(otpe)
        otp=otpe
        return otp
    def check_otp(otpe):
        # Check if OTP is blank, shorter than 6, or greater than 7 digits
        if otpe == "" or len(otpe) < 6 or len(otpe) > 6:
            print("OTP cannot be blank, less than 6 digits, or greater than 7 digits. Please enter a valid OTP.")
            input_otp_and_run_again()
        else:
            otp = otpe
            print("OTP entered successfully:", otp)
            with open('otp.txt', 'w') as file:
                file.write(otp)
            print(f"OTP {otp} entered and saved. Restarting process...")
                 # Set cookies
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S")
    print(formatted_time)  # Outputs the current date and time in the given format
    # Data to be sent in the POST request
    data = {
        "_token": token,
        "apiKey": token,
        "action": "sendOtp",
        "info": [{
            "web_id": web_id,
            "web_id_repeat": web_id,
            "passport": "",
            "name": name,
            "phone": phone,
            "email": email,
            "amount": "800.00",
            "captcha": "",
            "center": {
                "id": "1",
                "c_name": "Dhaka",
                "prefix": "D",
                "is_delete": "0"
            },
            "is_open": True,
            "ivac": {
                "id": "17",
                "center_info_id": "1",
                "ivac_name": "IVAC, Dhaka (JFP)",
                "address": "Jamuna Future Park",
                "prefix": "D"
            },
            "visa_type": {
                "id": "13",
                "type_name": "MEDICAL/MEDICAL ATTENDANT VISA",
                "is_active": "1"
            },
            "confirm_tos": True
        }],
        "resend": "0"
    }

    #print(data)
    def make_otppost_request_until_success(url, data, cookies, backoff_factor=2):
        """Makes a POST request with form data or JSON and retries indefinitely with a fixed backoff."""
        attempt = 0

        while True:
            attempt += 1
            try:
                headers = {
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
                    "Accept-Encoding": "gzip, deflate, br, zstd",
                    "Content-Type": "application/json",
                    "X-Xsrf-Token": XSRFTOKEN,
                    "Accept-Language": "en-US,en;q=0.5",
                    "Connection": "keep-alive",
                    "Host": "payment.ivacbd.com",
                    "Origin": "null",
                    "Priority": "u=0, i",
                    "Sec-Fetch-Dest": "document",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-Site": "none",
                    "Sec-Fetch-User": "?1",
                    "TE": "trailers",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"
                }
                # Send the POST request with JSON data
                #print(cookies)
                response = requests.post(url, json=data, headers=headers, cookies=cookies, timeout=90)  # Using JSON for this request
                response.raise_for_status()  # Raise HTTPError for bad responses (4xx, 5xx)
                print(f"Request successful on attempt {attempt}")
                return response  # Return the successful response

            except ConnectionError:
                print(f"Connection error on attempt {attempt}. Retrying...")

            except Timeout:
                print(f"Request timed out on attempt {attempt}. Retrying...")

            except HTTPError as http_err:
                if response.status_code == 504:
                    print(f"504 error: Gateway timeout on attempt {attempt}. Retrying...")
                else:
                    print(f"HTTP error occurred: {http_err}. Status Code: {response.status_code}")
                    break

            except RequestException as req_err:
                print(f"Request error occurred: {req_err}. Aborting.")
                break

            # Backoff with a fixed delay of 5 seconds
            print(f"Waiting for {backoff_factor} seconds before retrying...")
            time.sleep(backoff_factor)

        print("Failed to retrieve the URL. Aborting.")
        return None



    # Make the request with retries
    #response = make_otppost_request_until_success(url, data=data, cookies=cookies, backoff_factor=5)
    try:
        1
        loop = False # Defult false
        while loop:
            if os.path.exists('otp.txt'):
                with open('otp.txt', 'r') as file:
                    stored_otp = file.read().strip()
                    otp = stored_otp
                    print(f"The stored OTP is: {stored_otp}")
                    loop = False
            else:
                print("---------------otp----------------")
                print("otp.txt does not exist.")
                #response = make_otppost_request_until_success(url, data=data, cookies=cookies, backoff_factor=2)
                if response:
                    #print("Response Content:", response.json())  # If the response is JSON formatted
                    response_data = response.json()

                    # Extract and print the status code
                    status_code = response_data.get("code")
                    message = response_data.get("message")
                    print(status_code)
                    #print(message)
                    #print(otp)
                    if status_code == 200:                   
                        print(message)
                        loop = False
                        otpenter = True
                        while otpenter:
                            if os.path.exists('otp.txt'):
                                print("\nOtp found local file Ctrl+C")
                                otpenter = False
                            else:
                                print("\nEnter otp by Ctrl+C")
                                otp = input("Enter the OTP sent to your phone: ")
                                with open('otp.txt', 'w') as file:
                                    file.write(otp)
                                otpenter = False
                                #time.sleep(2)
                    elif status_code == 422:
                        loop = True #True refrash send otp
                        print(message)
                        time.sleep(2)
                        
                    else:
                        print("Request did not succeed, retrying...")
                        # You could retry here or handle the failure differently
                        
                else:
                    print("Request failed.")
    except KeyboardInterrupt:
        print("\nProcess interrupted by Ctrl+C")
        otp = input_otp_and_run_again()
    # End Example otp usage
    # Start verifyOtp & get date
    # Data to be sent as multipart form data

    data = {
        "_token": token,
        "apiKey": token,
        "action": "verifyOtp",
        "info": [
            {
                "web_id": web_id,
                "web_id_repeat": web_id,
                "passport": "",
                "name": name,
                "phone": phone,
                "email": email,
                "amount": "800.00",
                "captcha": "",
                "center": {
                    "id": "1",
                    "c_name": "Dhaka",
                    "prefix": "D",
                    "is_delete": "0"
                },
                "is_open": "true",
                "ivac": {
                    "id": "17",
                    "center_info_id": "1",
                    "ivac_name": "IVAC, Dhaka (JFP)",
                    "address": "Jamuna Future Park",
                    "prefix": "D",
                    "visa_fee": "800.00",
                    "is_delete": "0"
                },
                "visa_type": {
                    "id": "13",
                    "type_name": "MEDICAL/MEDICAL ATTENDANT VISA"
                },
                "confirm_tos": "true",
                "otp": otp
            }
        ],
        "otp": otp
    }
    #print(data)
    def make_otpveify_request_until_success(url, data, cookies, backoff_factor=2):
        """Makes a POST request with form data or JSON and retries indefinitely with a fixed backoff."""
        attempt = 0

        while True:
            attempt += 1
            try:
                # Send the POST request with multipart form data
                headers = {
                    "Host": "payment.ivacbd.com",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
                    "Accept": "application/json, text/plain, */*",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Accept-Encoding": "gzip, deflate, br",
                    "X-Xsrf-Token": XSRFTOKEN,  # Replace with the actual XSRF token
                    "Origin": "https://payment.ivacbd.com",
                    "Referer": "https://payment.ivacbd.com/",
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-origin",
                    "Priority": "u=0",
                    "Te": "trailers"
                }
                #print(cookies)
                response = requests.post(url, json=data,  headers=headers, cookies=cookies, timeout=90)  # Using files for multipart form-data
                response.raise_for_status()  # Raise HTTPError for bad responses (4xx, 5xx)
                print(f"Request successful on attempt {attempt}")
                return response  # Return the successful response

            except ConnectionError:
                print(f"Connection error on attempt {attempt}. Retrying...")

            except Timeout:
                print(f"Request timed out on attempt {attempt}. Retrying...")

            except HTTPError as http_err:
                if response.status_code == 504:
                    print(f"504 error: Gateway timeout on attempt {attempt}. Retrying...")
                else:
                    print(f"HTTP error occurred: {http_err}. Status Code: {response.status_code}")
                    break

            except RequestException as req_err:
                print(f"Request error occurred: {req_err}. Aborting.")
                break

            # Backoff with a fixed delay of 5 seconds
            print(f"Waiting for {backoff_factor} seconds before retrying...")
            time.sleep(backoff_factor)

        print("Failed to retrieve the URL. Aborting.")
        return None


    try:
        otploop = False # defulf False
        while otploop:
            print("---------------otp veify----------------")
            if os.path.exists('otp.txt') or len(otp) == 6:
                with open('otp.txt', 'r') as file:
                    stored_otp = file.read().strip()
                    otp = stored_otp
                    print(f"The stored OTP is: {stored_otp}")
                # Make the request with retries
            else:
                print("otp.txt does not exist otp veify.")
            

            otpveifyresponse = make_otpveify_request_until_success(url, data=data, cookies=cookies, backoff_factor=1)
            if otpveifyresponse:
                #print("Request otpveify was successful.")
                print("Otp Verify Response Content:", otpveifyresponse.json())  # If the response is JSON formatted
                responseotp_data = otpveifyresponse.json()
                #response_text = '{"status":"SUCCESS","code":200,"data":{"slot_times":[],"slot_dates":["2024-10-02"],"status":true,"error_reason":""},"message":[""]}'
                #responseotp_data = json.loads(response_text)
                # Extract and print the status code
                otpstatus_code = responseotp_data.get("code")
                otpstatus_status = responseotp_data.get("status")
                otpmessage = responseotp_data.get("message")
                print(f"status code {otpstatus_code}")
                #print(otpmessage)
                print(f"Otp {otp}")
                try:
                    if responseotp_data['status'] == "SUCCESS":               
                        otploop = False
                        print("Operation successful!")
                        print("Slot Dates:", responseotp_data['data']['slot_dates'])
                        print("Slot Times:", responseotp_data['data']['slot_times'])
                        slot_dates = responseotp_data['data']['slot_dates']
                        # Get the first date if it exists
                        if slot_dates:
                            specific_date = slot_dates[0]

                        else:
                            specific_date = None  # Handle the case where slot_dates is empty
                        print(f"First Slot Date: {specific_date}")
                        print("otp verify success")
                    elif responseotp_data['status'] == "FAILED":               
                        print("Operation failed:", responseotp_data['message'][0])
                        otploop = True
                        time.sleep(2)
                    else:
                        print("else Operation failed:", responseotp_data['message'])

                except json.JSONDecodeError:
                    print("Error decoding JSON response.")

            else:
                print("Request failed.")
    except KeyboardInterrupt:
        print("\nProcess interrupted by Ctrl+C")
        #otp = input_otp_and_run_again()
        
            
    # END verifyOtp & get date
    # User data
    data = {
        "apiKey": token,
        "action": "generateSlotTime",
        "amount": "10.00",
        "ivac_id": "17",
        "visa_type": "13",
        "specific_date": specific_date,
        "info": [
            {
                "web_id": web_id,
                "web_id_repeat": web_id,
                "passport": "",
                "name": name,
                "phone": phone,
                "email": email,
                "amount": "800.00",
                "captcha": "",
                "center": {
                    "id": "1",
                    "c_name": "Dhaka",
                    "prefix": "D",
                    "is_delete": "0",
                    "created_by": "",
                    "created_at": "",
                    "updated_at": ""
                },
                "is_open": "true",
                "ivac": {
                    "id": "17",
                    "center_info_id": "1",
                    "ivac_name": "IVAC, Dhaka (JFP)",
                    "address": "Jamuna Future Park",
                    "prefix": "D",
                    "created_on": "2018-07-12 11:58:00",
                    "visa_fee": "800.00",
                    "is_delete": "0",
                    "created_at": "2018-07-12 00:00:00",
                    "updated_at": "",
                    "app_key": "IVACJFP",
                    "contact_number": "",
                    "charge": "3",
                    "new_visa_fee": "800.00",
                    "old_visa_fee": "800.00",
                    "new_fees_applied_from": "2018-08-05 00:00:00",
                    "notify_fees_from": "2018-07-29 04:54:32",
                    "max_notification_count": "2",
                    "allow_old_amount_until_new_date": "2",
                    "notification_text_beside_amount": "(From <from> this IVAC fees will be <new_amount> BDT)",
                    "notification_text_popup": ""
                },
                "visa_type": {
                    "id": "13",
                    "type_name": "MEDICAL/MEDICAL ATTENDANT VISA",
                    "order": "2",
                    "is_active": "1",
                    "$$hashKey": "object:50"
                },
                "confirm_tos": "true",
                "otp": otp,
                "appointment_time": specific_date
            }
        ]
    }
    headers = {
                    "Host": "payment.ivacbd.com",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
                    "Accept": "application/json, text/plain, */*",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Accept-Encoding": "gzip, deflate, br",
                    "X-Xsrf-Token": XSRFTOKEN,  # Replace with the actual XSRF token
                    "Origin": "https://payment.ivacbd.com",
                    "Referer": "https://payment.ivacbd.com/",
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-origin",
                    "Priority": "u=0",
                    "Te": "trailers"
                }
    url = "https://payment.ivacbd.com/api/get_payment_options_v2"       
    def generate_slot_time(url, data, cookies, headers, backoff_factor=2):
        # Prepare the form data

        print(data)
        print(specific_date)
        #print(otp)
        attempt = 0

        while True:
            attempt += 1
            try:
                # Send the POST request with form data
                response = requests.post(url, json=data,  headers=headers, cookies=cookies, timeout=90)
                response.raise_for_status()  # Raise HTTPError for bad responses (4xx, 5xx)
                print(f"Request successful on attempt {attempt}")
                return response.json()  # Assuming the response is JSON

            except ConnectionError:
                print(f"Connection error on attempt {attempt}. Retrying...")

            except Timeout:
                print(f"Request timed out on attempt {attempt}. Retrying...")

            except HTTPError as http_err:
                if response.status_code == 504:
                    print(f"504 error: Gateway timeout on attempt {attempt}. Retrying...")
                else:
                    print(f"HTTP error occurred: {http_err}. Status Code: {response.status_code}")
                    break  # Exit on non-retryable errors

            except RequestException as req_err:
                print(f"Request error occurred: {req_err}. Aborting.")
                break

            # Backoff with a fixed delay
            print(f"Waiting for {backoff_factor} seconds before retrying...")
            time.sleep(backoff_factor)

        print("Failed to retrieve the URL. Aborting.")
        return None

    # Call the function
    try:
        generateslot = True # defult true
        while generateslot:
            print("---------------generate_slot_time----------------")
            response_data = generate_slot_time(url, data, cookies, headers, backoff_factor=2)
            if response_data:
                print("Response Data:", response_data)
                # Sample response object
                response = response_data
                '''response = {
                    "status": "OK",
                    "data": [""],
                    "slot_dates": ["2024-10-03"],
                    "slot_times": [
                        {
                            "id": 128762,
                            "ivac_id": 17,
                            "visa_type": 13,
                            "hour": 9,
                            "date": "2024-10-02",
                            "availableSlot": 117,
                            "time_display": "09:00 - 09:59"
                        },
                        {
                            "id": 149209,
                            "ivac_id": 17,
                            "visa_type": 13,
                            "hour": 10,
                            "date": "2024-10-02",
                            "availableSlot": 150,
                            "time_display": "10:00 - 10:59"
                        },
                        {
                            "id": 128764,
                            "ivac_id": 17,
                            "visa_type": 13,
                            "hour": 11,
                            "date": "2024-10-02",
                            "availableSlot": 87,
                            "time_display": "11:00 - 11:59"
                        },
                        {
                            "id": 128765,
                            "ivac_id": 17,
                            "visa_type": 13,
                            "hour": 12,
                            "date": "2024-10-02",
                            "availableSlot": 99,
                            "time_display": "12:00 - 12:59"
                        },
                        {
                            "id": 128766,
                            "ivac_id": 17,
                            "visa_type": 13,
                            "hour": 13,
                            "date": "2024-10-02",
                            "availableSlot": 110,
                            "time_display": "13:00 - 13:59"
                        },
                        {
                            "id": 128767,
                            "ivac_id": 17,
                            "visa_type": 13,
                            "hour": 14,
                            "date": "2024-10-02",
                            "availableSlot": 136,
                            "time_display": "14:00 - 14:59"
                        },
                        {
                            "id": 128768,
                            "ivac_id": 17,
                            "visa_type": 13,
                            "hour": 15,
                            "date": "2024-10-02",
                            "availableSlot": 117,
                            "time_display": "15:00 - 15:59"
                        },
                        {
                            "id": 128769,
                            "ivac_id": 17,
                            "visa_type": 13,
                            "hour": 16,
                            "date": "2024-10-02",
                            "availableSlot": 145,
                            "time_display": "16:00 - 16:59"
                        }
                    ]
                }
'''
                slot_times_count = len(response["slot_times"])
                if slot_times_count > 0:
                    generateslot = False
                    # Extract available slots
                    available_slots = [slot['availableSlot'] for slot in response['slot_times']]

                    # Find the maximum available slot
                    max_slot = max(available_slots)

                    # Find the index of the maximum available slot
                    max_index = available_slots.index(max_slot)

                    # Get the best time slot details
                    best_time_slot = response['slot_times'][max_index]
                    best_time_slotid = response['slot_times'][max_index]["id"]
                    best_time_slotivacid = response['slot_times'][max_index]["ivac_id"]
                    best_time_slotvtype = response['slot_times'][max_index]["visa_type"]
                    best_time_slothour = response['slot_times'][max_index]["hour"]
                    best_time_slotdate = response['slot_times'][max_index]["date"]
                    best_time_slotavslot = response['slot_times'][max_index]["availableSlot"]
                    best_time_slottdisplay = response['slot_times'][max_index]["time_display"]
                    # Print the results
                    print('Available Slots:', available_slots)
                    print('Highest Available Slot:', max_slot)
                    print('Index of Highest Available Slot:', max_index)
                    print('Best Time Slot:', best_time_slot)
                    print('Best Time Slot id:', best_time_slotid)
                    print('Best Time Slot ivac_id:', best_time_slotivacid)
                    print('Best Time Slot visa_type:', best_time_slotvtype)
                    print('Best Time Slot hour:', best_time_slothour)
                    print('Best Time Slot date:', best_time_slotdate)
                    print('Best Time Slotid availableSlot:', best_time_slotavslot)
                    print('Best Time Slot time_display:', best_time_slottdisplay)
                else:
                     print('Available slot_times:', slot_times_count)
                     print('status:', response['status'])
                     time.sleep(2)
                     
    except KeyboardInterrupt:
        print("\nProcess interrupted by Ctrl+C")
        #otp = input_otp_and_run_again()
        best_time_slotid = "149209"
        best_time_slothour = "10"
        best_time_slotdate = specific_date
        best_time_slotavslot = "126"
        best_time_slottdisplay = "10:00 - 10:59"

    # API endpoint
    data = {
        "apiKey": token,
        "action": "payInvoice",
        "info": [
            {
                "web_id": web_id,
                "web_id_repeat": web_id,
                "passport": "",
                "name": name,
                "phone": phone,
                "email": email,
                "amount": "800.00",
                "captcha": "",
                "center": {
                    "id": "1",
                    "c_name": "Dhaka",
                    "prefix": "D",
                    "is_delete": "0"
                },
                "is_open": "true",
                "ivac": {
                    "id": "17",
                    "center_info_id": "1",
                    "ivac_name": "IVAC, Dhaka (JFP)",
                    "address": "Jamuna Future Park",
                    "prefix": "D",
                    "ceated_on": "2018-07-12 11:58:00",
                    "visa_fee": "800.00",
                    "is_delete": "0",
                    "created_at": "2018-07-12 00:00:00",
                    "app_key": "IVACJFP",
                    "charge": "3",
                    "new_visa_fee": "800.00",
                    "old_visa_fee": "800.00",
                    "new_fees_applied_from": "2018-08-05 00:00:00",
                    "notify_fees_from": "2018-07-29 04:54:32",
                    "max_notification_count": "2",
                    "allow_old_amount_until_new_date": "2",
                    "notification_text_beside_amount": "(From <from> this IVAC fees will be <new_amount> BDT)"
                },
                "amountChangeData": {
                    "allow_old_amount_until_new_date": "2",
                    "max_notification_count": "0",
                    "old_visa_fees": "800.00",
                    "new_fees_applied_from": "2018-08-05 00:00:00",
                    "notice": "false",
                    "new_visa_fee": "800.00"
                },
                "visa_type": {
                    "id": "13",
                    "type_name": "MEDICAL/MEDICAL ATTENDANT VISA",
                    "order": "2",
                    "is_active": "1"
                },
                "confirm_tos": "true",
                "otp": otp
            }
        ],
        "selected_payment": {
            "name": "Bkash",
            "slug": "bkash",
            "grand_total": "824",
            "link": "https://securepay.sslcommerz.com/gwprocess/v4/image/gw1/bkash.png"
        },
        "selected_slot": {
            "id": best_time_slotid,
            "ivac_id": "17",
            "visa_type": "13",
            "hour": best_time_slothour,
            "date": best_time_slotdate,
            "availableSlot": best_time_slotavslot,
            "time_display": best_time_slottdisplay
        }
    }

    url = "https://payment.ivacbd.com/slot_pay_now"
    def pay_invoice(url, data, headers, cookies, backoff_factor=2):
        
        # Prepare the form data
        attempt = 0

        while True:
            attempt += 1
            try:
                # Send the POST request with form data
                headers = {
                    "Host": "payment.ivacbd.com",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
                    "Accept": "application/json, text/plain, */*",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Accept-Encoding": "gzip, deflate, br",
                    "X-Xsrf-Token": XSRFTOKEN,  # Replace with the actual XSRF token
                    "Origin": "https://payment.ivacbd.com",
                    "Referer": "https://payment.ivacbd.com/",
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-origin",
                    "Priority": "u=0",
                    "Te": "trailers"
                }
                response = requests.post(url, json=data,  headers=headers, cookies=cookies, timeout=90)
                response.raise_for_status()  # Raise HTTPError for bad responses (4xx, 5xx)
                print(f"Request successful on attempt {attempt}")
                return response.json()  # Assuming the response is JSON

            except ConnectionError:
                print(f"Connection error on attempt {attempt}. Retrying...")

            except Timeout:
                print(f"Request timed out on attempt {attempt}. Retrying...")

            except HTTPError as http_err:
                if response.status_code == 504:
                    print(f"504 error: Gateway timeout on attempt {attempt}. Retrying...")
                else:
                    print(f"HTTP error occurred: {http_err}. Status Code: {response.status_code}")
                    break  # Exit on non-retryable errors

            except RequestException as req_err:
                print(f"Request error occurred: {req_err}. Aborting.")
                break

            # Backoff with a fixed delay
            print(f"Waiting for {backoff_factor} seconds before retrying...")
            time.sleep(backoff_factor)

        print("Failed to retrieve the URL. Aborting.")
        return None

    # Call the function
    #response_data = pay_invoice(web_id, phone, name, email, specific_date, otp, token)
    payloop = True
    while payloop:
        print("---------------pay_invoice----------------")
        response_data = pay_invoice(url, data, headers, cookies, backoff_factor=2)
        if response_data:
            print("Response Data:", response_data)
            #response_text = '{"status":"OK","url":"https:\\/\\/securepay.sslcommerz.com\\/gwprocess\\/v4\\/gw.php?Q=REDIRECT&SESSIONKEY=C700B051753F933A9CFD3EF67997810F&cardname=","order_id":"SBIMU1725764857254","token_no":"T17U66DD14FC1DF9076405"}'
            #response_data = json.loads(response_text)
            # Check the status of the response
            if response_data['status'] == 'OK':
                payloop = False
                print("Status:", response_data['status'])
                print(response_data['url']+"bkash")
                print("Order ID:", response_data['order_id'])
                print("Token No:", response_data['token_no'])
                url = response_data['url']+"bkash"
                # Open the URL in the web browser
                if os.name == 'posix':
                    print("Operating System: Linux/Unix/Mac")
                    #subprocess.run(["termux-open", url])
                elif os.name == 'nt':
                    print("Operating System: Windows")
                    print(formatted_time)  # Outputs the start date and time in the given format
                    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S")
                    print(formatted_time)  # Outputs the current date and time in the given format
                    #webbrowser.open(url)
                else:
                    print("Unknown Operating System")
                    #webbrowser.open(url)
            else:
                payloop = False
                print("Status:", response_data['status'])
                url = response_data['status']
            return url
        else:
            print("Request failed.")


@app.route('/', methods=['GET', 'POST'])
def index():
        if request.method == 'POST':
            token = "Ud56W1sfSxPoYQE6mKm21BTwgHHB5iGcWOAuJmlI" 
            web_id = request.form['webfile']
            name = request.form['name']
            phone = request.form['mobile']
            email = request.form['email']
            otp = request.form['otp']
            specific_date = "2024-10-09"
            best_time_slotid = ""
            best_time_slothour = ""
            best_time_slotdate = specific_date
            best_time_slotavslot = ""
            best_time_slottdisplay = ""
            print(name+" "+web_id+" "+phone)
            response_data = otp_slot_time(web_id, name, phone, email, otp)

            #response_data = "https://www.abc.com?id=6555"

            #basic_items = response_data.url
            print(response_data)
            return render_template('result.html', items=response_data)
    
        return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT",4000))
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=port)
