# Quantum Pay Pesapal Integration

A modern, secure payment integration system for processing payments through Pesapal's payment gateway. This implementation provides a seamless payment experience with support for multiple payment methods including M-Pesa and Card Payments, featuring a sleek and responsive user interface.

<div align="center">
    <img src="https://www.pesapal.com/media/117786/pesapal_logo_and_slogan_outlined-01.png?anchor=center&mode=crop&width=770&height=375&rnd=133316248260000000" alt="Pesapal Logo" width="200"/>
</div>

## ✨ Features

- 🔒 Secure payment processing through Pesapal
- 💳 Multiple payment methods support (M-Pesa, Card Payments)
- 🎨 Modern, responsive UI with intuitive design
- ⚡ Real-time payment status updates
- 🔔 IPN (Instant Payment Notification) support
- 🛡️ Comprehensive error handling
- 📝 Detailed transaction logging
- 🔄 Support for recurring payments
- 📱 Mobile-friendly interface
- 🌐 Cross-browser compatibility

## 🚀 Prerequisites

- Python 3.7+
- Pesapal merchant account
- Pesapal API credentials (Consumer Key and Secret)

## 💻 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ShalomObongo/quantum-pay-pesapal-python.git
   cd quantum-pay-pesapal-2
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` with your Pesapal credentials and configuration.

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `PESAPAL_CONSUMER_KEY` | Your Pesapal consumer key | Yes |
| `PESAPAL_CONSUMER_SECRET` | Your Pesapal consumer secret | Yes |
| `PESAPAL_ENVIRONMENT` | 'sandbox' for testing or 'live' for production | Yes |
| `FLASK_ENV` | Application environment (development/production) | Yes |
| `FLASK_DEBUG` | Enable/disable debug mode | No |
| `SECRET_KEY` | Flask secret key for session management | Yes |
| `PORT` | Server port (default: 5000) | No |
| `HOST` | Server host (default: 0.0.0.0) | No |

## 🎯 Usage

1. Start the application:
   ```bash
   python app.py
   ```

2. Access the payment form at:
   ```
   http://localhost:5000
   ```

3. Fill in the payment details:
   - Amount
   - Email
   - Phone Number
   - First Name
   - Last Name
   - Payment Description
   - Recurring Payment Options (if needed)

4. Complete the payment through the embedded Pesapal interface

## 🔄 Payment Flow

1. **Initial Form**: 
   - User fills payment details
   - Validates input fields
   - Supports recurring payment setup

2. **Payment Processing**: 
   - Custom payment page loads
   - Pesapal interface embedded
   - Real-time status updates
   - Progress indicators

3. **Confirmation**: 
   - Payment status displayed
   - Transaction details shown
   - Email notification sent (if configured)
   - Receipt generation (optional)

## 🔔 IPN (Instant Payment Notification)

The system automatically handles IPN registration and updates. For production:

1. Configure your domain in Pesapal dashboard
2. Ensure your callback URL is accessible
3. SSL certificate is required for production

## 🎨 UI Customization

The payment interface features a modern, responsive design with:

- Clean and intuitive form layout
- Smooth animations and transitions
- Clear error messages and validation
- Loading indicators
- Mobile-optimized interface
- Customizable color schemes
- Responsive grid system

## 🔒 Security Features

- Input validation and sanitization
- CSRF protection
- Secure session management
- XSS prevention
- Rate limiting
- Error logging
- Secure credential storage

## 📱 Mobile Responsiveness

The interface is fully responsive and tested on:
- iOS devices
- Android devices
- Tablets
- Desktop browsers

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Development

### Project Structure
```
quantum-pay-pesapal-2/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── .env               # Configuration file
├── .gitignore         # Git ignore rules
├── README.md          # Documentation
└── templates/         # HTML templates
    ├── index.html     # Payment form
    ├── payment.html   # Custom payment page
    └── payment_status.html  # Status page
```

### Adding New Features

1. Create feature branch
2. Implement changes
3. Test thoroughly
4. Submit pull request

## Testing

1. Use sandbox environment
2. Test all payment methods
3. Verify IPN handling
4. Check error scenarios

## Troubleshooting

Common issues and solutions:

1. **IPN not working**:
   - Check URL accessibility
   - Verify SSL certificate
   - Confirm IPN registration

2. **Payment failing**:
   - Verify API credentials
   - Check environment setting
   - Confirm amount format

## Acknowledgments

- Pesapal API team
- Contributors
- Open source community

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and queries, please create an issue or contact the development team.

---

<div align="center">
Made with ⚡ by Shalom Obongo
</div>

