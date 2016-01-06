import zlib, struct

class Receiver:
	def __init__(self, s):
		self.s = s
		self.buf = bytes()
	def read_next(self):
		self.buf += self.s.recv(MAX_LENGTH)
	def try_to_read_json(self):
		read_next()
		if len(self.buf) >= 4:
			n = struct.unpack('I', self.buf[:4])[0]
			if len(self.buf) >= 4 + n:
				compressed_json = buf[4: 4+n]
				return json.loads(str(zlib.decompress(buf[4: 4+n]), 'utf-8'))
		return None
	def wait_for_json(self):
		while True:
			res = self.try_to_read_json()
			if res != None:
				return res

		
def send_query(s, json_data):
	data = zlib.compress(json.dumps(json_data))
	s.send(struct.pack('I', len(data)) + data)
