from __future__ import annotations
import cv2
import json
import paho.mqtt.client as mqtt
import numpy as np
from tcolorpy import tcolor
import time

BROKER = "localhost"
TOPIC = "paso"
PORT = 1883
INBOX = None

# COLOR
class Color:
	def __init__(self, r: float, g: float, b: float, normalize=False) -> None:
		self.r = r / 255.0 if normalize else r
		self.g = g / 255.0 if normalize else g
		self.b = b / 255.0 if normalize else b

	def __str__(self) -> str:
		r_hex: str = f"{int(self.r * 255):02X}"
		g_hex: str = f"{int(self.g * 255):02X}"
		b_hex: str = f"{int(self.b * 255):02X}"
		return f"#{r_hex}{g_hex}{b_hex}"

	def reverse(self, normalize: bool = False) -> Color:
		return Color(1.0 - self.r, 1.0 - self.g, 1.0 - self.b, normalize)

	@staticmethod
	def from_frame(frame: np.ndarray, normalize: bool = True) -> Color:
		avg_b = np.mean(frame[:, :, 0])
		avg_g = np.mean(frame[:, :, 1])
		avg_r = np.mean(frame[:, :, 2])
		return Color(avg_r, avg_g, avg_b, normalize)

	@staticmethod
	def mix_colors(color1: Color, color2: Color, normalize: bool = False) -> Color:
		mixed_r = min(1.0, color1.r + color2.r)
		mixed_g = min(1.0, color1.g + color2.g)
		mixed_b = min(1.0, color1.b + color2.b)
		return Color(mixed_r, mixed_g, mixed_b, normalize)


	@staticmethod
	def decide_lamp_color(settings: dict, room_color: Color) -> Color:
		mode = settings.get("mode", "manual")
		temperature = settings.get("temperature", 127.5)
		brightness = settings.get("brightness", 255)

		red = temperature / 255.0
		blue = 1.0 - red
		green = 0.3 + (temperature / 255.0) * 0.4

		red *= brightness / 255.0
		green *= brightness / 255.0
		blue *= brightness / 255.0

		target_color = Color(red, green, blue, normalize=False)
		print(tcolor(f"\nTARGET:\t{target_color}------------------------------------------------", color=str(target_color)))

		if mode == "manual":
			return target_color

		elif mode == "automatic":
			lamp_r = max(0.0, target_color.r - room_color.r)
			lamp_g = max(0.0, target_color.g - room_color.g)
			lamp_b = max(0.0, target_color.b - room_color.b)
			lamp_color = Color(lamp_r, lamp_g, lamp_b, normalize=False)
			return lamp_color
		else:
			raise ValueError(f"Unknown mode: {mode}")


# CAMERA
class Camera:
	def __init__(self, cap: cv2.VideoCapture, auto_processing: bool = False) -> None:
		self.cap = cap
		if not auto_processing:
			self.disable_auto_processing()

	def disable_auto_processing(self) -> None:
		self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
		self.cap.set(cv2.CAP_PROP_AUTO_WB, 0)
		self.cap.set(cv2.CAP_PROP_EXPOSURE, -4)
		self.cap.set(cv2.CAP_PROP_GAIN, 0)

	def get_frame(self) -> np.ndarray:
		ret, frame = self.cap.read()
		if not ret:
			raise RuntimeError("Failed to capture frame from the webcam.")
		return frame


def on_connect(client, userdata, flags, rc, *args) -> None:
	client.subscribe(TOPIC)

def on_message(client, userdata, msg, *args) -> None:
	global INBOX
	try:
		INBOX = json.loads(msg.payload.decode('utf-8').replace("'", '"'))
		print(f"\n\nREQUEST: {INBOX}")
	except json.JSONDecodeError:
		print("Error decoding MQTT message payload.")

if __name__ == "__main__":

	try:
		# CLIENT - setup
		mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
		# mqttc = mqtt.Client()
		mqttc.on_connect = on_connect
		mqttc.on_message = on_message
		mqttc.connect(BROKER, PORT, 60)
		mqttc.loop_start()

		# CAMERA - setup
		camera: Camera = Camera(cv2.VideoCapture(0))
		if not camera.cap.isOpened():
			raise RuntimeError("Webcam not found.")

		# MAIN LOOP
		while True:
			frame: np.ndarray = camera.get_frame()
			frame_color: Color = Color.from_frame(frame)

			if INBOX:
				lamp_color: Color = Color.decide_lamp_color(INBOX, frame_color)
				mixed_color: Color = Color.mix_colors(lamp_color, frame_color)
				print(tcolor(f"LAMP:\t{lamp_color}", color=str(lamp_color)), tcolor(f"\tROOM:\t{frame_color}", color=str(frame_color)), tcolor(f"\tMIX:\t{mixed_color}", color=str(mixed_color)))

				# PLACEHOLDER: setting color of real lamp, depends on the specific lamp.
				# This one (Philips) accepts brightness and saturation instead of color, for example

				# import phue
				# bridge = phue.Bridge("Your IP address")
				# light = bridge.lights[0]
				# light.hue = 65535
				# light.saturation = 254
				# light.brightness = 254

				# while this one (blender) does not
				# import bpy
				# bpy.ops.object.light_add(type='AREA')
				# light_obj = bpy.data.objects['Area']
				# light_obj.data.energy = 500
				# light_obj.color = [1.0, 0.0, 0.0, 1.0]

				time.sleep(1)

	except RuntimeError as init_error:
		print(f"INIT ERROR: {init_error}")

	finally:
		if 'camera' in locals():
			camera.cap.release()
		if 'mqttc' in locals():
			mqttc.loop_stop()
			mqttc.disconnect()
