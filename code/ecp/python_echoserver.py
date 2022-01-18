# -*- coding: utf-8 -*-
"""
Target a server running as a PACs in the local host
"""
import os
import pandas as pd
import json
import time


def main():
    for index in range(4):
        try:
            query='echoscu -v localhost 4242'
            print(query)
            os.system(query)
        except Exception as e:
            print(e)
    


if __name__ == "__main__":
    main()

