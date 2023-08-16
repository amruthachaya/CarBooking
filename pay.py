import razorpay

client = razorpay.Client(auth=("rzp_test_pcJUI2h54atKS2", "zcn5CaE2muoStTh5Q6QBmqM0"))
order = client.order.create({
    "amount": 50000,
    "currency": "INR",
    "receipt": "receipt#1",
    "notes": {
        "key1": "value3",
        "key2": "value2"
    }
})

print(order)


