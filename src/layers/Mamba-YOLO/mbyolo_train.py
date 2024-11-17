from ultralytics import YOLO
import argparse
import os

os.environ['CUDA_VISIBLE_DEVICES'] = '0'  

ROOT = os.path.abspath('.') + "/"


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, default=ROOT + '/ultralytics/cfg/datasets/coco.yaml', help='dataset.yaml path')
    parser.add_argument('--config', type=str, default=ROOT + '/ultralytics/cfg/models/mamba-yolo/Mamba-YOLO-T.yaml', help='model path(s)')
    parser.add_argument('--batch_size', type=int, default=16, help='batch size')
    parser.add_argument('--imgsz', '--img', '--img-size', type=int, default=1024, help='inference size (pixels)')
    parser.add_argument('--task', default='train', help='train, val, test, speed or study')
    parser.add_argument('--device', default='0', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--workers', type=int, default=4, help='max dataloader workers (per RANK in DDP mode)')
    parser.add_argument('--epochs', type=int, default=30)
    parser.add_argument('--optimizer', default='auto', help='SGD, Adam, AdamW')# SGD
    parser.add_argument('--amp', action='store_true', help='open amp')
    parser.add_argument('--project', default='/output_dir/', help='save to project/name')
    parser.add_argument('--name', default='mambayolo', help='save to project/name')
    parser.add_argument('--half', action='store_true', help='use FP16 half-precision inference')
    parser.add_argument('--dnn', action='store_true', help='use OpenCV DNN for ONNX inference')
    opt = parser.parse_args()
    return opt


if __name__ == '__main__':
    opt = parse_opt()
    task = opt.task
    args = {
        "data": ROOT + opt.data,
        "epochs": 300,
        "workers": opt.workers,
        "batch": 8,
        "optimizer": opt.optimizer,
        "device": opt.device,
        "amp": opt.amp,
        "project": ROOT + opt.project,
        "name": opt.name,
        "imgsz": 1024,
        "flipud": 0.5,
        "fliplr":0.5,
        "pretrained":False,
        "lr0":0.005,
        "lrf":0.001,
        "degrees":170,
        "augment":True,
        
    }
    model_conf = ROOT + opt.config # this is for .yml file
    task_type = {
        "train": YOLO(model_conf).train(**args),
        "val": YOLO(model_conf).val(**args),
        "test": YOLO(model_conf).test(**args),
    }
    task_type.get(task)
