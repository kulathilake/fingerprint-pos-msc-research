import evaluate

if __name__ == "__main__":
    cent_lat = evaluate.test_centralised_latency("http://localhost:3000", "user_0", "./fvc2002/102_1.tif")
    