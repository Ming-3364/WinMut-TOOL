from .config import WEB_DEMO_SRC_DIR
import os

def getDemoSrc():
    demo_src_dict = []
    items = os.listdir(WEB_DEMO_SRC_DIR)
    for item in items:
        demo_src = {}
        item_path = os.path.join(WEB_DEMO_SRC_DIR, item)
        demo_src['label'] = item
        demo_src['path'] = item_path
        demo_src_dict.append(demo_src)
    return demo_src_dict