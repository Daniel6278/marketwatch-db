from faker import Faker
import pandas as pd
from hashlib import sha256
import base64

N_INSTANCES = 10

# Create a Faker instance (default locale is en_US)
fake = Faker()

df = pd.DataFrame(columns=["email", "password_hash", "first_name", "last_name"])

for i in range(N_INSTANCES):
    df.loc[i] = [
        fake.email(),
        base64.b64encode(sha256(fake.password().encode("utf-8")).digest()).decode(
            "utf-8"
        ),
        fake.first_name(),
        fake.last_name(),
    ]

df.to_csv("data/tables/User.csv", index=False)
