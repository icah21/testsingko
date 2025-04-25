import cv2
import torch
import random

def load_model(model_path='yolov5/runs/train/cacao_varieties8/weights/best.pt', conf_thresh=0.4):
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload=True)
    model.conf = conf_thresh
    return model

def assign_colors(names):
    return {name: [random.randint(0, 255) for _ in range(3)] for name in names.values()}

def get_detections(model, frame):
    results = model(frame)
    detections = results.xyxy[0]
    return detections
