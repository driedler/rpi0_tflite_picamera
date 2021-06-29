import io
import os
import time 

# Import the necessary 3d-party Python packages
# NOTE: These packages reside on the RPI0
#       Assuming you followed the README,
#       you should be able to ctrl+click the packages as if they 
#       were installed locally
import picamera
from cv2 import cv2
import numpy as np
from tflite_micro_runtime.interpreter import Interpreter
from tflite_micro_runtime.image_transform import ImageTransformer


curdir = os.path.dirname(os.path.abspath(__file__))



def main():
  model_path = f'{curdir}/trained_model.tflite'

  # Local the model into the interpreter
  interpreter = Interpreter(model_path)
  interpreter.allocate_tensors()
  input_details = interpreter.get_input_details()[0]
  output_details = interpreter.get_output_details()[0]
  _, height, width, _ = input_details['shape']
  input_index = input_details['index']
  output_index = output_details['index']

  roi_w, roi_h = 128,128

  # This will perform a perspective transform
  # then standardize the image
  # NOTE: In practice, the src_points should points to a
  #       polygon within the image
  img_xfrm = ImageTransformer(
	src_points=[[0, 0], [roi_w, 0], [roi_w-1, roi_h-1], [0, roi_h-1]],
	dst_size=(width,height),
	standardize=True
  )

  with picamera.PiCamera(resolution=(640, 480), framerate=30) as camera:
    camera.zoom = 0., 0., roi_w/640, roi_h/480
    camera.start_preview()
    try:
      stream = io.BytesIO()
      for _ in camera.capture_continuous(
          stream, format='jpeg', use_video_port=True):
        stream.seek(0)

        # Read the image into a buffer
        im_buf = np.frombuffer(stream.read(), np.uint8)
        # Convert the image from JPG to numpy
        im = cv2.imdecode(im_buf, cv2.IMREAD_COLOR)
        # Perform a perspective transform on the image
        # then standardize the image
        x = img_xfrm.invoke(im)
        x = np.expand_dims(x, 0)
       
        input_tensor = interpreter.tensor(input_index)()[0]
        np.copyto(input_tensor, x)
        input_tensor = None
   
        start_time = time.time()
        interpreter.invoke()

        output = np.squeeze(interpreter.get_tensor(output_index))
        elapsed_ms = (time.time() - start_time) * 1000
        print(f'({elapsed_ms:.4f}) {output}')
   
        stream.seek(0)
        stream.truncate()

    finally:
      camera.stop_preview()


if __name__ == '__main__':
  main()