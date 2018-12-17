import datetime

def debug_print(msg, indent=False, end='\n'):
	print("\t"*indent +"[", datetime.datetime.now().time(), "]:", msg, end=end)