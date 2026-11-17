import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    mosaic_dir = os.path.join(app.static_folder, 'images', 'mosaic')
    try:
        mosaic_images = [f for f in os.listdir(mosaic_dir) if f.lower().endswith(('png', 'jpg', 'jpeg', 'webp'))]
    except Exception:
        mosaic_images = []
    return render_template('index.html', mosaic_images=mosaic_images)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
