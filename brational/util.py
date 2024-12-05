DEBUG = False

def my_print(on:bool, string:str, level:int=0):
    from datetime import datetime
    if on:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{now}]" + "\t"*level + f" {string}")