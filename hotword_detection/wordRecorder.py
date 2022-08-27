"""This module is used for recording speech utterances both for training as well as testing purposes. SoundDevice is required for this module."""
import sounddevice as sd
from array import array
import wave,sys
from struct import pack

class wordRecorder:
	"""

	This class contains methods for recording audio from a microphone, segmenting audio to remove noise by using an amplitude based VAD and for storing segmented utterances in an appropriate folder.

	:param blockSize: int
	:type samplingFrequency: int
	:param threshold: Threshold used for amplitude based VAD (scaled in the range 0-16384)
	:type threshold: int

	Documentation related to all member functions is listed below.

	"""
	def __init__(self, blocksize = 8000, threshold = 14000):
		self.threshold = threshold
		self.device_info = sd.query_devices(None, "input")
		self.samplerate = int(self.device_info["default_samplerate"])
		self.blocksize = blocksize
	
	def isSilent(self, data):
		"""

		This function is used to check if the whole recorded audio is silence or not. If it is silence, then this utterance is discarded.

		:param data: Recorded audio 
		:type data: array
		:returns: 1 if entire audio is silence and 0 otherwise
		:rtype: boolean

		"""
		return max(data) < self.threshold

	def normalize(self, data):
		"""

		This function is used to normalize the sampled audio stream such that all values lie in the range -16383 to 16384. This is because we use a 16-bit representation to store audio. Out of these 16 bits 1 bit is reserved as a sign bit.

		:param data: Recorded audio
		:type data: array
		:returns: Normalized audio
		:rtype: array

		"""
		maxShort = 16384
		scale = float(maxShort)/max(abs(i-127) for i in data)

		r = []
		for i in data:
			r.append(int((i-127)*scale))
		return r

	def trimWord(self, data):
		"""
		
		This function implements the amplitude based Voice Activity detector. It segments out audio based on whether the amplitude of the audio is greater than the specified threshold or not.

		:param data: Normalized audio
		:type data: array
		:returns: Trimmed audio containing only speech segments
		:rtype: array
		
		"""
	def trimStart(data):
		snd_started = False
		r = array('h')

		for i in data:
			if not snd_started and abs(i)>self.threshold:
				snd_started = True
				r.append(i)

			elif snd_started:
				r.append(i)
		return r

		data = trimStart(data)
		data.reverse()
		data = trimStart(data)
		data.reverse()
		return data

	def record(self):
		"""

		This function implements the recording routine used for getting audio from a microphone using SoundDevice. It also calls the ``normalize()`` and ``trimWord()`` methods to return the normalized and trimmed audio containing speech only.

		:returns: Trimmed and normalized recorded audio
		:rtype: array

		"""
		with sd.RawInputStream(self.samplerate, self.blocksize, 9, 1, dtype="int16") as stream:
			data = bytearray()
			try:
				print("The program is recording... (Press Ctrl+C to stop)")
				while True:
					buff = stream.read(1)[0]
					data += buff
			except KeyboardInterrupt:
				print("Interrupted by the user")
				# self.normalize(data)
				return stream.samplesize, data

	def record2File(self, path):
		"""

		This function is used to store the recorded audio after it has been normalized and trimmed into a specified directory as a .wav file.

		:param path: Path to directory where audio is to be stored
				:type data: str
				
		"""
		sample_width, data = self.record()
		with wave.open(path, "wb") as wf:
			wf.setnchannels(1)
			wf.setsampwidth(sample_width)
			wf.setframerate(self.samplerate)
			wf.writeframes(data)

