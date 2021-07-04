import datetime
from speech_recognition import Microphone, Recognizer, AudioFile, UnknownValueError,RequestError
import pyttsx3

recog = Recognizer()
mic = Microphone()
talker = pyttsx3.init()
talker.setProperty("rate",110)

print()
print("..........................................")
print("...~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~...")
print("...   WELLCOME to SPEECH_RECOGNITION!  ...")
print("...~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~...")
print("..........................................")
print()


while True:

	try:
		with mic:

			recog.adjust_for_ambient_noise(mic, duration = 2)

			t = str(datetime.datetime.now())
			print(t[0:19] + " Computer: Say something")

			#sound = recog.listen(mic, timeout = 3)
			sound = recog.listen(mic)

		# recognizer some where between 50 - 4000
		print(t[0:19] + " Computer: threshold {} processing....".format(round(recog.energy_threshold,2)))

		text = recog.recognize_google(sound)

		t = str(datetime.datetime.now())
		print(t[0:19] + " You said: " + text )

		#talker.say(text)
		#talker.runAndWait()

	except UnknownValueError:
		t = str(datetime.datetime.now())
		print(t[0:19] + " Error   : Unable to recognize")

	except RequestError as exc:
		t = str(datetime.datetime.now())
		print(t[0:19] + " Error   : " + exc)

