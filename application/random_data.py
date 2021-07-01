import secrets
import random


def create_data():
	types = ['emeter', 'zigbee', 'lora', 'gsm']
	data = [{
		'dev_id': f'{secrets.token_hex(6)}',
		'dev_type': f'{types[random.randint(0, 3)]}'
	} for _ in range(10)]

	return data
