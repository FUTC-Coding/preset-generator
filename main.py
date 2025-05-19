from openai import OpenAI
import os
import time
import random
import json
import uuid
import xml.etree.ElementTree as ET
import ratelimiter
from few_shot_examples_fetcher import few_shot_examples

OpenAI.api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI()


#@ratelimiter.RateLimiter(max_calls_per_minute=60)
def generate_preset(theme, model, print_input = False):
    few_shot_themes, few_shot_configs = few_shot_examples(theme)
    few_shot_blocks = []
    for example_theme, config in zip(few_shot_themes, few_shot_configs):
        config_str = config.replace("\n", "").replace(" ", "")
        block = f"Theme: {example_theme} Settings: {config_str}"
        few_shot_blocks.append(block)
    few_shot_text = " ".join(few_shot_blocks)
    print(f"generating preset for theme: {theme} using mode: {model} and few shot settings: {few_shot_themes}", flush=True)

    # Start timer
    start_time = time.time()

    # Simulate API call with random wait time
    wait_time = random.uniform(7.0, 10.0)
    print(f"Waiting {wait_time:.2f} seconds to simulate API call...", flush=True)
    time.sleep(wait_time)

    # response = client.responses.create(
    #     model=model,
    #     input=[
    #         {"role": "system",
    #          "content": "You are an award winning photographer, specializing in image editing and manipulation, especially in Adobe Lightroom."
    #                     "Create settings for a Lightroom preset that matches the named theme."},
    #         {"role": "user", "content": "Please make a lightroom preset that matches the theme of " + theme + " Here are examples of similar themes and their outputs: " + few_shot_text},
    #     ],
    #     text={
    #         "format": {
    #             "type": "json_schema",
    #             "name": "camera_raw_settings",
    #             "schema": {
    #                 "type": "object",
    #                 "properties": {
    #                     "Contrast2012": {
    #                         "type": "integer"
    #                     },
    #                     "Highlights2012": {
    #                         "type": "integer"
    #                     },
    #                     "Shadows2012": {
    #                         "type": "integer"
    #                     },
    #                     "Whites2012": {
    #                         "type": "integer"
    #                     },
    #                     "Blacks2012": {
    #                         "type": "integer"
    #                     },
    #                     "Texture": {
    #                         "type": "integer"
    #                     },
    #                     "Clarity2012": {
    #                         "type": "integer"
    #                     },
    #                     "Dehaze": {
    #                         "type": "integer"
    #                     },
    #                     "Vibrance": {
    #                         "type": "integer"
    #                     },
    #                     "Saturation": {
    #                         "type": "integer"
    #                     },
    #                     "ParametricShadows": {
    #                         "type": "integer"
    #                     },
    #                     "ParametricDarks": {
    #                         "type": "integer"
    #                     },
    #                     "ParametricLights": {
    #                         "type": "integer"
    #                     },
    #                     "ParametricHighlights": {
    #                         "type": "integer"
    #                     },
    #                     "ParametricShadowSplit": {
    #                         "type": "integer"
    #                     },
    #                     "ParametricMidtoneSplit": {
    #                         "type": "integer"
    #                     },
    #                     "ParametricHighlightSplit": {
    #                         "type": "integer"
    #                     },
    #                     "Sharpness": {
    #                         "type": "integer"
    #                     },
    #                     "SharpenRadius": {
    #                         "type": "number"
    #                     },
    #                     "SharpenDetail": {
    #                         "type": "integer"
    #                     },
    #                     "SharpenEdgeMasking": {
    #                         "type": "integer"
    #                     },
    #                     "LuminanceSmoothing": {
    #                         "type": "integer"
    #                     },
    #                     "ColorNoiseReduction": {
    #                         "type": "integer"
    #                     },
    #                     "ColorNoiseReductionDetail": {
    #                         "type": "integer"
    #                     },
    #                     "ColorNoiseReductionSmoothness": {
    #                         "type": "integer"
    #                     },
    #                     "HueAdjustmentRed": {
    #                         "type": "integer"
    #                     },
    #                     "HueAdjustmentOrange": {
    #                         "type": "integer"
    #                     },
    #                     "HueAdjustmentYellow": {
    #                         "type": "integer"
    #                     },
    #                     "HueAdjustmentGreen": {
    #                         "type": "integer"
    #                     },
    #                     "HueAdjustmentAqua": {
    #                         "type": "integer"
    #                     },
    #                     "HueAdjustmentBlue": {
    #                         "type": "integer"
    #                     },
    #                     "HueAdjustmentPurple": {
    #                         "type": "integer"
    #                     },
    #                     "HueAdjustmentMagenta": {
    #                         "type": "integer"
    #                     },
    #                     "SaturationAdjustmentRed": {
    #                         "type": "integer"
    #                     },
    #                     "SaturationAdjustmentOrange": {
    #                         "type": "integer"
    #                     },
    #                     "SaturationAdjustmentYellow": {
    #                         "type": "integer"
    #                     },
    #                     "SaturationAdjustmentGreen": {
    #                         "type": "integer"
    #                     },
    #                     "SaturationAdjustmentAqua": {
    #                         "type": "integer"
    #                     },
    #                     "SaturationAdjustmentBlue": {
    #                         "type": "integer"
    #                     },
    #                     "SaturationAdjustmentPurple": {
    #                         "type": "integer"
    #                     },
    #                     "SaturationAdjustmentMagenta": {
    #                         "type": "integer"
    #                     },
    #                     "LuminanceAdjustmentRed": {
    #                         "type": "integer"
    #                     },
    #                     "LuminanceAdjustmentOrange": {
    #                         "type": "integer"
    #                     },
    #                     "LuminanceAdjustmentYellow": {
    #                         "type": "integer"
    #                     },
    #                     "LuminanceAdjustmentGreen": {
    #                         "type": "integer"
    #                     },
    #                     "LuminanceAdjustmentAqua": {
    #                         "type": "integer"
    #                     },
    #                     "LuminanceAdjustmentBlue": {
    #                         "type": "integer"
    #                     },
    #                     "LuminanceAdjustmentPurple": {
    #                         "type": "integer"
    #                     },
    #                     "LuminanceAdjustmentMagenta": {
    #                         "type": "integer"
    #                     },
    #                     "SplitToningShadowHue": {
    #                         "type": "integer"
    #                     },
    #                     "SplitToningShadowSaturation": {
    #                         "type": "integer"
    #                     },
    #                     "SplitToningHighlightHue": {
    #                         "type": "integer"
    #                     },
    #                     "SplitToningHighlightSaturation": {
    #                         "type": "integer"
    #                     },
    #                     "SplitToningBalance": {
    #                         "type": "integer"
    #                     },
    #                     "ColorGradeMidtoneHue": {
    #                         "type": "integer"
    #                     },
    #                     "ColorGradeMidtoneSat": {
    #                         "type": "integer"
    #                     },
    #                     "ColorGradeShadowLum": {
    #                         "type": "integer"
    #                     },
    #                     "ColorGradeMidtoneLum": {
    #                         "type": "integer"
    #                     },
    #                     "ColorGradeHighlightLum": {
    #                         "type": "integer"
    #                     },
    #                     "ColorGradeBlending": {
    #                         "type": "integer"
    #                     },
    #                     "ColorGradeGlobalHue": {
    #                         "type": "integer"
    #                     },
    #                     "ColorGradeGlobalSat": {
    #                         "type": "integer"
    #                     },
    #                     "ColorGradeGlobalLum": {
    #                         "type": "integer"
    #                     },
    #                     "GrainAmount": {
    #                         "type": "integer"
    #                     },
    #                     "GrainSize": {
    #                         "type": "integer"
    #                     },
    #                     "GrainFrequency": {
    #                         "type": "integer"
    #                     },
    #                     "PostCropVignetteAmount": {
    #                         "type": "integer"
    #                     },
    #                     "ShadowTint": {
    #                         "type": "integer"
    #                     },
    #                     "RedHue": {
    #                         "type": "integer"
    #                     },
    #                     "RedSaturation": {
    #                         "type": "integer"
    #                     },
    #                     "GreenHue": {
    #                         "type": "integer"
    #                     },
    #                     "GreenSaturation": {
    #                         "type": "integer"
    #                     },
    #                     "BlueHue": {
    #                         "type": "integer"
    #                     },
    #                     "BlueSaturation": {
    #                         "type": "integer"
    #                     },
    #                     "CurveRefineSaturation": {
    #                         "type": "integer"
    #                     },
    #                     "OverrideLookVignette": {
    #                         "type": "boolean"
    #                     },
    #                     "ToneCurveName2012": {
    #                         "type": "string"
    #                     },
    #                     "HasSettings": {
    #                         "type": "boolean"
    #                     },
    #                     "Name": {
    #                         "type": "string"
    #                     },
    #                     "ToneCurvePV2012": {
    #                         "type": "array",
    #                         "items": {
    #                             "type": "string"
    #                         }
    #                     },
    #                     "ToneCurvePV2012Red": {
    #                         "type": "array",
    #                         "items": {
    #                             "type": "string"
    #                         }
    #                     },
    #                     "ToneCurvePV2012Green": {
    #                         "type": "array",
    #                         "items": {
    #                             "type": "string"
    #                         }
    #                     },
    #                     "ToneCurvePV2012Blue": {
    #                         "type": "array",
    #                         "items": {
    #                             "type": "string"
    #                         }
    #                     },
    #                     "PointColors": {
    #                         "type": "array",
    #                         "items": {
    #                             "type": "string"
    #                         }
    #                     }
    #                 },
    #                 "required": ["Contrast2012", "Highlights2012", "Shadows2012", "Whites2012", "Blacks2012", "Texture", "Clarity2012", "Dehaze", "Vibrance", "Saturation", "ParametricShadows", "ParametricDarks", "ParametricLights", "ParametricHighlights", "ParametricShadowSplit", "ParametricMidtoneSplit", "ParametricHighlightSplit", "Sharpness", "SharpenRadius", "SharpenDetail", "SharpenEdgeMasking", "LuminanceSmoothing", "ColorNoiseReduction", "ColorNoiseReductionDetail", "ColorNoiseReductionSmoothness", "HueAdjustmentRed", "HueAdjustmentOrange", "HueAdjustmentYellow", "HueAdjustmentGreen", "HueAdjustmentAqua", "HueAdjustmentBlue", "HueAdjustmentPurple", "HueAdjustmentMagenta", "SaturationAdjustmentRed", "SaturationAdjustmentOrange", "SaturationAdjustmentYellow", "SaturationAdjustmentGreen", "SaturationAdjustmentAqua", "SaturationAdjustmentBlue", "SaturationAdjustmentPurple", "SaturationAdjustmentMagenta", "LuminanceAdjustmentRed", "LuminanceAdjustmentOrange", "LuminanceAdjustmentYellow", "LuminanceAdjustmentGreen", "LuminanceAdjustmentAqua", "LuminanceAdjustmentBlue", "LuminanceAdjustmentPurple", "LuminanceAdjustmentMagenta", "SplitToningShadowHue", "SplitToningShadowSaturation", "SplitToningHighlightHue", "SplitToningHighlightSaturation", "SplitToningBalance", "ColorGradeMidtoneHue", "ColorGradeMidtoneSat", "ColorGradeShadowLum", "ColorGradeMidtoneLum", "ColorGradeHighlightLum", "ColorGradeBlending", "ColorGradeGlobalHue", "ColorGradeGlobalSat", "ColorGradeGlobalLum", "GrainAmount", "GrainSize", "GrainFrequency", "PostCropVignetteAmount", "ShadowTint", "RedHue", "RedSaturation", "GreenHue", "GreenSaturation", "BlueHue", "BlueSaturation", "CurveRefineSaturation", "OverrideLookVignette", "ToneCurveName2012", "HasSettings", "Name", "ToneCurvePV2012", "ToneCurvePV2012Red", "ToneCurvePV2012Green", "ToneCurvePV2012Blue", "PointColors"],
    #                 "additionalProperties": False
    #             },
    #             "strict": True
    #         }
    #     }
    # )

    # log time and tokens
    # Log time and tokens used
    elapsed_time = time.time() - start_time
    # print(f"API response time: {elapsed_time:.2f} seconds", flush=True)
    # print(f"Total tokens: {response.usage.total_tokens}", flush=True)

    # simulated response
    simulated_response = """
        {"Contrast2012":20,"Highlights2012":-10,"Shadows2012":10,"Whites2012":-5,"Blacks2012":5,"Texture":5,"Clarity2012":15,"Dehaze":2,"Vibrance":20,"Saturation":10,"ParametricShadows":-10,"ParametricDarks":-5,"ParametricLights":5,"ParametricHighlights":0,"ParametricShadowSplit":25,"ParametricMidtoneSplit":50,"ParametricHighlightSplit":75,"Sharpness":35,"SharpenRadius":1.0,"SharpenDetail":25,"SharpenEdgeMasking":10,"LuminanceSmoothing":10,"ColorNoiseReduction":20,"ColorNoiseReductionDetail":50,"ColorNoiseReductionSmoothness":50,"HueAdjustmentRed":0,"HueAdjustmentOrange":10,"HueAdjustmentYellow":15,"HueAdjustmentGreen":-10,"HueAdjustmentAqua":-10,"HueAdjustmentBlue":-15,"HueAdjustmentPurple":0,"HueAdjustmentMagenta":5,"SaturationAdjustmentRed":5,"SaturationAdjustmentOrange":10,"SaturationAdjustmentYellow":10,"SaturationAdjustmentGreen":-10,"SaturationAdjustmentAqua":-15,"SaturationAdjustmentBlue":-20,"SaturationAdjustmentPurple":0,"SaturationAdjustmentMagenta":5,"LuminanceAdjustmentRed":0,"LuminanceAdjustmentOrange":10,"LuminanceAdjustmentYellow":0,"LuminanceAdjustmentGreen":-5,"LuminanceAdjustmentAqua":0,"LuminanceAdjustmentBlue":-10,"LuminanceAdjustmentPurple":0,"LuminanceAdjustmentMagenta":0,"SplitToningShadowHue":50,"SplitToningShadowSaturation":25,"SplitToningHighlightHue":40,"SplitToningHighlightSaturation":20,"SplitToningBalance":0,"ColorGradeMidtoneHue":30,"ColorGradeMidtoneSat":15,"ColorGradeShadowLum":-10,"ColorGradeMidtoneLum":0,"ColorGradeHighlightLum":10,"ColorGradeBlending":65,"ColorGradeGlobalHue":0,"ColorGradeGlobalSat":0,"ColorGradeGlobalLum":0,"GrainAmount":15,"GrainSize":40,"GrainFrequency":30,"PostCropVignetteAmount":-20,"ShadowTint":0,"RedHue":0,"RedSaturation":0,"GreenHue":0,"GreenSaturation":0,"BlueHue":0,"BlueSaturation":0,"CurveRefineSaturation":0,"OverrideLookVignette":false,"ToneCurveName2012":"MediumContrast","HasSettings":true,"Name":"VintageSummerPastel","ToneCurvePV2012":["0,0","64,50","192,205","255,255"],"ToneCurvePV2012Red":["0,0","64,55","192,210","255,255"],"ToneCurvePV2012Green":["0,0","70,60","200,198","255,255"],"ToneCurvePV2012Blue":["0,0","64,58","180,160","255,255"],"PointColors":["#D8C1A3","#B7A693","#9B8A7A","#786B5E","#5A4A3C"]}
    """
    event = json.loads(simulated_response)

    # event = json.loads(response.output_text)

    return event


def create_xmp_file(preset_data):
    # Create the root element
    xmpmeta = ET.Element('x:xmpmeta', {
        'xmlns:x': 'adobe:ns:meta/',
        'x:xmptk': 'Adobe XMP Core 7.0-c000 1.000000, 0000/00/00-00:00:00'
    })

    rdf = ET.SubElement(xmpmeta, 'rdf:RDF', {
        'xmlns:rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
    })

    description = ET.SubElement(rdf, 'rdf:Description', {
        'rdf:about': '',
        'xmlns:crs': 'http://ns.adobe.com/camera-raw-settings/1.0/',
        'crs:PresetType': 'Normal',
        'crs:Cluster': '',
        'crs:UUID': str(uuid.uuid4()).upper().replace('-', ''),
        'crs:SupportsAmount2': 'True',
        'crs:SupportsAmount': 'True',
        'crs:SupportsColor': 'True',
        'crs:SupportsMonochrome': 'True',
        'crs:SupportsHighDynamicRange': 'True',
        'crs:SupportsNormalDynamicRange': 'True',
        'crs:SupportsSceneReferred': 'True',
        'crs:SupportsOutputReferred': 'True',
        'crs:RequiresRGBTables': 'False',
        'crs:CameraModelRestriction': '',
        'crs:Copyright': '',
        'crs:ContactInfo': '',
        'crs:Version': '17.2',
        'crs:ProcessVersion': '15.4',
        'crs:ToneCurveName2012': 'Custom',
        'crs:HasSettings': 'True',
    })

    # Update description with values from API response
    for key, value in preset_data.items():
        if isinstance(value, list):
            parent_element = ET.SubElement(description, f'crs:{key}')
            seq = ET.SubElement(parent_element, 'rdf:Seq')
            for item in value:
                li = ET.SubElement(seq, 'rdf:li')
                li.text = str(item)
        else:
            description.set(f'crs:{key}', str(value))

    # Convert to string
    from io import BytesIO
    xml_bytes = BytesIO()
    tree = ET.ElementTree(xmpmeta)
    tree.write(xml_bytes, encoding='utf-8', xml_declaration=True)

    return xml_bytes.getvalue().decode('utf-8')