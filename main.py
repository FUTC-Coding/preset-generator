from openai import OpenAI
import os
import json
import uuid
import xml.etree.ElementTree as ET
import ratelimiter
from few_shot_examples_fetcher import few_shot_examples

OpenAI.api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI()


@ratelimiter.RateLimiter(max_calls_per_minute=20)
def generate_preset(theme, print_input = False):
    print("generating preset for theme: ", theme)
    few_shot_themes, few_shot_configs = few_shot_examples(theme)
    few_shot_blocks = []
    for example_theme, config in zip(few_shot_themes, few_shot_configs):
        config_str = config.replace("\n", "").replace(" ", "")  
        block = f"Theme: {example_theme}\nSettings: {config_str}"
        few_shot_blocks.append(block)
    few_shot_text = "\n\n".join(few_shot_blocks)
    response = client.responses.create(
        model="gpt-4.1-nano",
        input=[
            {"role": "system",
             "content": "You are an award winning photographer, specializing in image editing and manipulation, especially in Adobe Lightroom."
                        "Create settings for a Lightroom preset that matches the named theme."},
            {"role": "user", "content": "Please make a lightroom preset that matches the theme of " + theme + "Here are examples of similar themes and their outputs: " + few_shot_text},
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "camera_raw_settings",
                "schema": {
                    "type": "object",
                    "properties": {
                        "Contrast2012": {
                            "type": "integer"
                        },
                        "Highlights2012": {
                            "type": "integer"
                        },
                        "Shadows2012": {
                            "type": "integer"
                        },
                        "Whites2012": {
                            "type": "integer"
                        },
                        "Blacks2012": {
                            "type": "integer"
                        },
                        "Texture": {
                            "type": "integer"
                        },
                        "Clarity2012": {
                            "type": "integer"
                        },
                        "Dehaze": {
                            "type": "integer"
                        },
                        "Vibrance": {
                            "type": "integer"
                        },
                        "Saturation": {
                            "type": "integer"
                        },
                        "ParametricShadows": {
                            "type": "integer"
                        },
                        "ParametricDarks": {
                            "type": "integer"
                        },
                        "ParametricLights": {
                            "type": "integer"
                        },
                        "ParametricHighlights": {
                            "type": "integer"
                        },
                        "ParametricShadowSplit": {
                            "type": "integer"
                        },
                        "ParametricMidtoneSplit": {
                            "type": "integer"
                        },
                        "ParametricHighlightSplit": {
                            "type": "integer"
                        },
                        "Sharpness": {
                            "type": "integer"
                        },
                        "SharpenRadius": {
                            "type": "number"
                        },
                        "SharpenDetail": {
                            "type": "integer"
                        },
                        "SharpenEdgeMasking": {
                            "type": "integer"
                        },
                        "LuminanceSmoothing": {
                            "type": "integer"
                        },
                        "ColorNoiseReduction": {
                            "type": "integer"
                        },
                        "ColorNoiseReductionDetail": {
                            "type": "integer"
                        },
                        "ColorNoiseReductionSmoothness": {
                            "type": "integer"
                        },
                        "HueAdjustmentRed": {
                            "type": "integer"
                        },
                        "HueAdjustmentOrange": {
                            "type": "integer"
                        },
                        "HueAdjustmentYellow": {
                            "type": "integer"
                        },
                        "HueAdjustmentGreen": {
                            "type": "integer"
                        },
                        "HueAdjustmentAqua": {
                            "type": "integer"
                        },
                        "HueAdjustmentBlue": {
                            "type": "integer"
                        },
                        "HueAdjustmentPurple": {
                            "type": "integer"
                        },
                        "HueAdjustmentMagenta": {
                            "type": "integer"
                        },
                        "SaturationAdjustmentRed": {
                            "type": "integer"
                        },
                        "SaturationAdjustmentOrange": {
                            "type": "integer"
                        },
                        "SaturationAdjustmentYellow": {
                            "type": "integer"
                        },
                        "SaturationAdjustmentGreen": {
                            "type": "integer"
                        },
                        "SaturationAdjustmentAqua": {
                            "type": "integer"
                        },
                        "SaturationAdjustmentBlue": {
                            "type": "integer"
                        },
                        "SaturationAdjustmentPurple": {
                            "type": "integer"
                        },
                        "SaturationAdjustmentMagenta": {
                            "type": "integer"
                        },
                        "LuminanceAdjustmentRed": {
                            "type": "integer"
                        },
                        "LuminanceAdjustmentOrange": {
                            "type": "integer"
                        },
                        "LuminanceAdjustmentYellow": {
                            "type": "integer"
                        },
                        "LuminanceAdjustmentGreen": {
                            "type": "integer"
                        },
                        "LuminanceAdjustmentAqua": {
                            "type": "integer"
                        },
                        "LuminanceAdjustmentBlue": {
                            "type": "integer"
                        },
                        "LuminanceAdjustmentPurple": {
                            "type": "integer"
                        },
                        "LuminanceAdjustmentMagenta": {
                            "type": "integer"
                        },
                        "SplitToningShadowHue": {
                            "type": "integer"
                        },
                        "SplitToningShadowSaturation": {
                            "type": "integer"
                        },
                        "SplitToningHighlightHue": {
                            "type": "integer"
                        },
                        "SplitToningHighlightSaturation": {
                            "type": "integer"
                        },
                        "SplitToningBalance": {
                            "type": "integer"
                        },
                        "ColorGradeMidtoneHue": {
                            "type": "integer"
                        },
                        "ColorGradeMidtoneSat": {
                            "type": "integer"
                        },
                        "ColorGradeShadowLum": {
                            "type": "integer"
                        },
                        "ColorGradeMidtoneLum": {
                            "type": "integer"
                        },
                        "ColorGradeHighlightLum": {
                            "type": "integer"
                        },
                        "ColorGradeBlending": {
                            "type": "integer"
                        },
                        "ColorGradeGlobalHue": {
                            "type": "integer"
                        },
                        "ColorGradeGlobalSat": {
                            "type": "integer"
                        },
                        "ColorGradeGlobalLum": {
                            "type": "integer"
                        },
                        "GrainAmount": {
                            "type": "integer"
                        },
                        "GrainSize": {
                            "type": "integer"
                        },
                        "GrainFrequency": {
                            "type": "integer"
                        },
                        "PostCropVignetteAmount": {
                            "type": "integer"
                        },
                        "ShadowTint": {
                            "type": "integer"
                        },
                        "RedHue": {
                            "type": "integer"
                        },
                        "RedSaturation": {
                            "type": "integer"
                        },
                        "GreenHue": {
                            "type": "integer"
                        },
                        "GreenSaturation": {
                            "type": "integer"
                        },
                        "BlueHue": {
                            "type": "integer"
                        },
                        "BlueSaturation": {
                            "type": "integer"
                        },
                        "CurveRefineSaturation": {
                            "type": "integer"
                        },
                        "OverrideLookVignette": {
                            "type": "boolean"
                        },
                        "ToneCurveName2012": {
                            "type": "string"
                        },
                        "HasSettings": {
                            "type": "boolean"
                        },
                        "Name": {
                            "type": "string"
                        },
                        "ToneCurvePV2012": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        },
                        "ToneCurvePV2012Red": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        },
                        "ToneCurvePV2012Green": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        },
                        "ToneCurvePV2012Blue": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        },
                        "PointColors": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        }
                    },
                    "required": ["Contrast2012", "Highlights2012", "Shadows2012", "Whites2012", "Blacks2012", "Texture", "Clarity2012", "Dehaze", "Vibrance", "Saturation", "ParametricShadows", "ParametricDarks", "ParametricLights", "ParametricHighlights", "ParametricShadowSplit", "ParametricMidtoneSplit", "ParametricHighlightSplit", "Sharpness", "SharpenRadius", "SharpenDetail", "SharpenEdgeMasking", "LuminanceSmoothing", "ColorNoiseReduction", "ColorNoiseReductionDetail", "ColorNoiseReductionSmoothness", "HueAdjustmentRed", "HueAdjustmentOrange", "HueAdjustmentYellow", "HueAdjustmentGreen", "HueAdjustmentAqua", "HueAdjustmentBlue", "HueAdjustmentPurple", "HueAdjustmentMagenta", "SaturationAdjustmentRed", "SaturationAdjustmentOrange", "SaturationAdjustmentYellow", "SaturationAdjustmentGreen", "SaturationAdjustmentAqua", "SaturationAdjustmentBlue", "SaturationAdjustmentPurple", "SaturationAdjustmentMagenta", "LuminanceAdjustmentRed", "LuminanceAdjustmentOrange", "LuminanceAdjustmentYellow", "LuminanceAdjustmentGreen", "LuminanceAdjustmentAqua", "LuminanceAdjustmentBlue", "LuminanceAdjustmentPurple", "LuminanceAdjustmentMagenta", "SplitToningShadowHue", "SplitToningShadowSaturation", "SplitToningHighlightHue", "SplitToningHighlightSaturation", "SplitToningBalance", "ColorGradeMidtoneHue", "ColorGradeMidtoneSat", "ColorGradeShadowLum", "ColorGradeMidtoneLum", "ColorGradeHighlightLum", "ColorGradeBlending", "ColorGradeGlobalHue", "ColorGradeGlobalSat", "ColorGradeGlobalLum", "GrainAmount", "GrainSize", "GrainFrequency", "PostCropVignetteAmount", "ShadowTint", "RedHue", "RedSaturation", "GreenHue", "GreenSaturation", "BlueHue", "BlueSaturation", "CurveRefineSaturation", "OverrideLookVignette", "ToneCurveName2012", "HasSettings", "Name", "ToneCurvePV2012", "ToneCurvePV2012Red", "ToneCurvePV2012Green", "ToneCurvePV2012Blue", "PointColors"],
                    "additionalProperties": False
                },
                "strict": True
            }
        }
    )

    print([
    {
        "role": "system",
        "content": "You are an award winning photographer, specializing in image editing and manipulation, especially in Adobe Lightroom. "
                   "Create settings for a Lightroom preset that matches the named theme."
    },
    {
        "role": "user",
        "content": "Please make a lightroom preset that matches the theme of " + theme + 
                   ". Here are examples of similar themes and their outputs:\n\n" + few_shot_text
    }
    ])
    event = json.loads(response.output_text)
    print(event)
    print(response.usage.total_tokens)

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