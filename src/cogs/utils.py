import random
import time

def generate_random_seed():
    current_millis = int(round(time.time() * 1000))
    random.seed(current_millis)
