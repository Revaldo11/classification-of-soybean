import json
import zipfile
import os

model_path = 'best_model_skenario3.keras'
temp_path = 'best_model_skenario3_patched.keras'

def patch_config(config):
    if isinstance(config, dict):
        # Remove quantization_config if it's there
        config.pop('quantization_config', None)
        for key, value in config.items():
            patch_config(value)
    elif isinstance(config, list):
        for item in config:
            patch_config(item)

with zipfile.ZipFile(model_path, 'r') as zin:
    with zipfile.ZipFile(temp_path, 'w') as zout:
        for item in zin.infolist():
            content = zin.read(item.filename)
            if item.filename == 'config.json':
                config = json.loads(content.decode('utf-8'))
                patch_config(config)
                content = json.dumps(config).encode('utf-8')
            zout.writestr(item, content)

# Replace original with patched
os.replace(temp_path, model_path)
print("Successfully patched best_model_skenario3.keras")
