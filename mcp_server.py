import sys, json
from client import MultimodalAspectRatioSmartCropperClient
sys.stdout.reconfigure(encoding='utf-8')

def handle_mcp():
    cropper = MultimodalAspectRatioSmartCropperClient()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps({"status": "ready", "skill": "genpark-multimodal-aspect-ratio-smart-cropper-skill"}))
        return
    req = json.loads(sys.stdin.read() or "{}")
    w = int(req.get("width", 1920))
    h = int(req.get("height", 1080))
    fx = req.get("focal_x")
    fy = req.get("focal_y")
    res = cropper.generate_all_crops(w, h, fx, fy)
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    handle_mcp()
