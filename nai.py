import base64
import io
import json
import random
import zipfile
import requests


class NovelAIAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://image.novelai.net/ai"
        self.headers = {
            "accept": "*/*",
            "content-type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

    def generate_image(self, input_text, model, width, height, scale, sampler, steps, n_samples=1, ucPreset=0,
                       qualityToggle=True, sm=False, sm_dyn=False, dynamic_thresholding=False, controlnet_strength=1, legacy=False, add_original_image=True,
                       cfg_rescale=0, noise_schedule="native", legacy_v3_extend=False,input_image=None, seed=0, negative_prompt="",
                       reference_image_multiple=[], reference_information_extracted_multiple=[], reference_strength_multiple=[]):
        # Use parameters passed dynamically, no config from JSON
        print("Start generating image")
        data = {
            "input": input_text + ", best quality, amazing quality, very aesthetic, absurdres",
            "model": model,
            "action": "generate",  # Default action is text-to-image generation
            "parameters": {
                "params_version": 1,
                "width": width,  # Image width
                "height": height,  # Image height
                "scale": scale,  # CFG scale
                "sampler": sampler,  # Sampler choice
                "steps": steps,  # Steps count
                "n_samples": n_samples,  # Number of samples
                "ucPreset": ucPreset,  # UcPreset
                "qualityToggle": qualityToggle,  # Quality toggle
                "sm": sm,  # SMEA option
                "sm_dyn": sm_dyn,  # Dynamic SMEA option
                "dynamic_thresholding": dynamic_thresholding,  # Dynamic thresholding
                "controlnet_strength": controlnet_strength,  # ControlNet strength
                "legacy": legacy,  # Legacy setting
                "add_original_image": add_original_image,  # Include original image
                "cfg_rescale": cfg_rescale,  # CFG rescale
                "noise_schedule": noise_schedule,  # Noise schedule
                "legacy_v3_extend": legacy_v3_extend,  # Legacy extension
                "seed": seed if seed else random.randint(0, 0xffffffffffffffff),  # Random seed if not provided
                "negative_prompt": negative_prompt,  # Negative prompt
                "reference_image_multiple": reference_image_multiple,
                "reference_information_extracted_multiple": reference_information_extracted_multiple,
                "reference_strength_multiple": reference_strength_multiple,
            }
        }
        if input_image is not None:
            buffer = io.BytesIO()
            input_image.save(buffer, format="PNG")
            image_payload = base64.b64encode(buffer.getvalue()).decode("utf-8")
            data["action"]="img2img"
            data["parameters"]["image"] = image_payload

        # Send the request to NovelAI API
        data_json = json.dumps(data)
        response = requests.post(self.base_url + "/generate-image", headers=self.headers, data=data_json)

        if response.status_code == 200:
            # Handle successful response
            with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
                with zip_ref.open("image_0.png") as image_file:
                    image_data = image_file.read()
                    print("Generated image")
                    return image_data
        else:
            raise Exception(f"Image generation failed: {response.status_code}, {response.text}")
