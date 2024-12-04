from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
from dotenv import load_dotenv
import requests
import uuid
from datetime import datetime
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Pesapal Configuration
PESAPAL_CONSUMER_KEY = os.getenv('PESAPAL_CONSUMER_KEY')
PESAPAL_CONSUMER_SECRET = os.getenv('PESAPAL_CONSUMER_SECRET')
PESAPAL_ENVIRONMENT = os.getenv('PESAPAL_ENVIRONMENT', 'sandbox')

# Pesapal API URLs
PESAPAL_BASE_URL = 'https://pay.pesapal.com/v3'

def get_access_token():
    auth_response = requests.post(
        f'{PESAPAL_BASE_URL}/api/Auth/RequestToken',
        json={
            'consumer_key': PESAPAL_CONSUMER_KEY,
            'consumer_secret': PESAPAL_CONSUMER_SECRET
        }
    )
    
    if auth_response.status_code != 200:
        raise Exception(f'Failed to authenticate with Pesapal: {auth_response.text}')
    
    return auth_response.json().get('token')

def register_ipn():
    try:
        token = get_access_token()
        
        # Register IPN URL
        callback_url = url_for('payment_callback', _external=True)
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        # First, list existing IPNs
        list_ipn_response = requests.get(
            f'{PESAPAL_BASE_URL}/api/URLSetup/GetIpnList',
            headers=headers
        )
        
        print(f"IPN list response: {list_ipn_response.text}")
        
        if list_ipn_response.status_code == 200:
            ipn_list = list_ipn_response.json()
            # Check if we already have an IPN registered
            for ipn in ipn_list:
                if ipn.get('url') == callback_url:
                    print(f"Found existing IPN: {ipn}")
                    return ipn.get('ipn_id')
        
        # If no existing IPN found, register new one
        ipn_request = {
            "url": callback_url,
            "ipn_notification_type": "GET"
        }
        
        print(f"Registering new IPN with request: {ipn_request}")
        
        ipn_response = requests.post(
            f'{PESAPAL_BASE_URL}/api/URLSetup/RegisterIPN',
            json=ipn_request,
            headers=headers
        )
        
        print(f"IPN registration response: {ipn_response.text}")
        
        if ipn_response.status_code == 200:
            ipn_data = ipn_response.json()
            if ipn_data.get('status') == '200':
                return ipn_data.get('ipn_id')
        
        raise Exception(f'Failed to register IPN: {ipn_response.text}')
    except Exception as e:
        print(f"Error registering IPN: {str(e)}")
        raise

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/initiate-payment', methods=['POST'])
def initiate_payment():
    try:
        # Get form data
        amount = request.form.get('amount')
        email = request.form.get('email')
        first_name = request.form.get('firstName', '')
        last_name = request.form.get('lastName', '')
        phone = request.form.get('phone', '')
        description = request.form.get('description', 'Payment for services')
        
        # Get recurring payment data
        enable_recurring = request.form.get('enableRecurring')
        account_number = request.form.get('accountNumber')
        frequency = request.form.get('frequency')
        start_date = request.form.get('startDate')
        end_date = request.form.get('endDate')
        
        # Validate required fields
        if not all([amount, email, first_name, last_name, phone]):
            return jsonify({'error': 'All fields are required'}), 400

        # Validate recurring payment fields if enabled
        if enable_recurring:
            if not all([account_number, frequency, start_date, end_date]):
                return jsonify({'error': 'All recurring payment fields are required'}), 400
            
            # Validate frequency
            valid_frequencies = ['DAILY', 'WEEKLY', 'MONTHLY', 'YEARLY']
            if frequency not in valid_frequencies:
                return jsonify({'error': 'Invalid payment frequency'}), 400

        print(f"Initiating {'recurring' if enable_recurring else 'one-time'} payment for amount: {amount}, email: {email}")

        # First register or get existing IPN
        ipn_id = register_ipn()
        if not ipn_id:
            return jsonify({'error': 'Failed to register IPN URL'}), 500

        # Get fresh token for order submission
        token = get_access_token()
        
        # Create order with IPN
        order_id = str(uuid.uuid4())
        callback_url = url_for('payment_callback', _external=True)
        
        # Base order request
        order_request = {
            "id": order_id,
            "currency": "KES",
            "amount": float(amount),
            "description": description,
            "callback_url": callback_url,
            "notification_id": ipn_id,
            "cancellation_url": url_for('index', _external=True),
            "billing_address": {
                "email_address": email,
                "phone_number": phone,
                "country_code": "KE",
                "first_name": first_name,
                "last_name": last_name
            }
        }

        # Add recurring payment details if enabled
        if enable_recurring:
            order_request["account_number"] = account_number
            order_request["subscription_details"] = {
                "start_date": start_date,
                "end_date": end_date,
                "frequency": frequency,
                "payment_method": "CARD",
                "currency_code": "KES"
            }
            # Force card payment for recurring payments
            order_request["payment_method"] = "CARD"

        print(f"Submitting order request: {json.dumps(order_request, indent=2)}")

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        submit_order_response = requests.post(
            f'{PESAPAL_BASE_URL}/api/Transactions/SubmitOrderRequest',
            json=order_request,
            headers=headers
        )

        print(f"Submit order response status: {submit_order_response.status_code}")
        print(f"Submit order response content: {submit_order_response.text}")

        if submit_order_response.status_code != 200:
            return jsonify({'error': f'Failed to create order: {submit_order_response.text}'}), 500

        response_data = submit_order_response.json()
        if response_data.get('error'):
            error_message = response_data['error'].get('message', 'Unknown error occurred')
            return jsonify({'error': error_message}), 500
        
        redirect_url = response_data.get('redirect_url')
        if not redirect_url:
            return jsonify({'error': 'No redirect URL in response'}), 500

        # Pass payment type to template
        return render_template('payment.html', 
                            iframe_url=redirect_url,
                            amount=float(amount),
                            callback_url=callback_url,
                            is_recurring=bool(enable_recurring))

    except Exception as e:
        print(f"Error in initiate_payment: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/payment-callback')
def payment_callback():
    try:
        order_tracking_id = request.args.get('OrderTrackingId')
        merchant_reference = request.args.get('OrderMerchantReference')
        
        if not order_tracking_id or not merchant_reference:
            return render_template('payment_status.html', 
                                status='error',
                                message='Missing payment tracking information')

        # Get fresh token
        token = get_access_token()
        if not token:
            return render_template('payment_status.html', 
                                status='error',
                                message='Failed to authenticate with payment gateway')

        # Get transaction status
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        status_response = requests.get(
            f'{PESAPAL_BASE_URL}/api/Transactions/GetTransactionStatus?orderTrackingId={order_tracking_id}',
            headers=headers
        )
        
        if status_response.status_code != 200:
            return render_template('payment_status.html', 
                                status='error',
                                message='Failed to fetch payment status')

        transaction_data = status_response.json()
        
        # Get subscription details if this was a recurring payment
        subscription_data = None
        if transaction_data.get('payment_method') == 'card':
            subscription_response = requests.get(
                f'{PESAPAL_BASE_URL}/api/Transactions/GetSubscriptionStatus?orderTrackingId={order_tracking_id}',
                headers=headers
            )
            if subscription_response.status_code == 200:
                subscription_data = subscription_response.json()

        return render_template('payment_status.html',
                            status=transaction_data.get('payment_status_description', 'Unknown'),
                            message=transaction_data.get('status_message', ''),
                            transaction_data=transaction_data,
                            subscription_data=subscription_data,
                            merchant_reference=merchant_reference)

    except Exception as e:
        print(f"Error in payment_callback: {str(e)}")
        return render_template('payment_status.html', 
                            status='error',
                            message=f'An error occurred: {str(e)}')

if __name__ == '__main__':
    app.run(debug=True)
