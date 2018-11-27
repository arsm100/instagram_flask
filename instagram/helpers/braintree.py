import os
import braintree
import config

TRANSACTION_SUCCESS_STATUSES = [
    braintree.Transaction.Status.Authorized,
    braintree.Transaction.Status.Authorizing,
    braintree.Transaction.Status.Settled,
    braintree.Transaction.Status.SettlementConfirmed,
    braintree.Transaction.Status.SettlementPending,
    braintree.Transaction.Status.Settling,
    braintree.Transaction.Status.SubmittedForSettlement
]

config = eval(os.environ['APP_SETTINGS'])

if os.environ['FLASK_ENV'] == 'development':
    gateway = braintree.BraintreeGateway(
        braintree.Configuration(
            environment=braintree.Environment.Sandbox,
            merchant_id=config.MERCHANT_ID,
            public_key=config.PUBLIC_KEY,
            private_key=config.PRIVATE_KEY
        )
    )
elif os.environ['FLASK_ENV'] == 'development':
    gateway = braintree.BraintreeGateway(
        braintree.Configuration(
            environment=braintree.Environment.Sandbox,
            merchant_id=config.MERCHANT_ID,
            public_key=config.PUBLIC_KEY,
            private_key=config.PRIVATE_KEY
        )
    )
