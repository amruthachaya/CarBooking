import razorpay

client = razorpay.Client(auth=("rzp_test_pcJUI2h54atKS2", "zcn5CaE2muoStTh5Q6QBmqM0"))

a = client.payment_link.create({
    "amount": 1000,
    "currency": "INR",
    "accept_partial": "true",
    "first_min_partial_amount": 200,
    "description": "For Testing",
    "customer":
        {
            "name": "Amrutha",
            "email": "amruthachaya4381@gmail.com",
            "contact": "9148169281"
        },
    "notify":
        {
            "sms": True,
            "email": True
        }
})

print(a)