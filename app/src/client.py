from atproto import Client
import os
from time import time

HANDLE = 'asinvader.bsky.social' if not os.getenv('BSKY_HANDLE') else os.getenv('BSKY_HANDLE') # Push base handle to dockerfile environment variable
KEY = os.getenv('BSKEY') # Push dev key to environment variable


def get_client()->Client:
    client = Client()
    client.login(HANDLE, KEY)
    return client



if __name__=="__main__":

    start = time()
    client = get_client()
    print(f'Client init time: {time()-start:.3f} seconds')

    profile = client.get_profile(HANDLE)
    follower_count = profile.followers_count
    print(f'You have {follower_count} followers.')