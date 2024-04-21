"""
An TinyML detection technique using Efficientdet model.
"""
from typing import Any

import cv2
import numpy
from tflite_runtime.interpreter import Interpreter

from .base_detector_strategy import BaseDetectorStrategy, DetectorResult


class EfficientdetStrategy(BaseDetectorStrategy):
    """
    The Efficientdet strategy for detection of objects.
    """
    MODEL_PATH: str = "models/efficientdet_1.tflite"
    LABEL_PATH: str = "models/efficientdet_1_labelmap.txt"
    DETECTION_THRES: float = 0.65

    @classmethod
    def detect_humans(cls, frame: numpy.ndarray) -> DetectorResult:
        """This method detects if there are any humans in the frame."""
        # Create an model interpreter.
        interpreter: Interpreter = Interpreter(model_path=cls.MODEL_PATH)
        interpreter.allocate_tensors()

        # Get model input and output details.
        input_details: list[dict[str, Any]] = interpreter.get_input_details()
        output_details: list[dict[str, Any]] = interpreter.get_output_details()
        _, input_height, input_width, _ = input_details[0]['shape']

        # Prepare image for input-tensor.
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (input_width, input_height), interpolation=cv2.INTER_AREA)
        image_height, image_width = image.shape[:2]

        # Apply the frame into first tensor of the model.
        input_data = numpy.expand_dims(image, axis=0)
        interpreter.set_tensor(input_details[0]['index'], input_data)

        # Calculate the output tensor.
        interpreter.invoke()

        # Recieve the output.
        boxes = interpreter.get_tensor(output_details[0]['index'])[0]
        classes = interpreter.get_tensor(output_details[1]['index'])[0]
        scores = interpreter.get_tensor(output_details[2]['index'])[0]

        # Read label-map.
        with open(cls.LABEL_PATH, 'r', encoding="utf-8") as labelmap:
            labels = [line.strip() for line in labelmap.readlines()]

        # Convert RGB to BGR again.
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Travers through detections.
        detection_regions: list[tuple[int, int, int, int]] = []
        for score, box, pred_class in zip(scores, boxes, classes):
            if score < cls.DETECTION_THRES:
                continue

            if (labels[int(pred_class)]) == 'person':
                frame_height, frame_width = frame.shape[:2]
                min_y = round(box[0] * frame_height)
                min_x = round(box[1] * frame_width)
                max_y = round(box[2] * frame_height)
                max_x = round(box[3] * frame_width)
                detection_regions.append((min_x, max_x, min_y, max_y))
                cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (0, 255, 0), 5)

        result = DetectorResult(
            image=frame,
            human_found=len(detection_regions) > 0,
            regions=detection_regions,
            num_detections=len(detection_regions),
        )
        return result
