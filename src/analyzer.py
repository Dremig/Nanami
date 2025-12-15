import os
import random
import subprocess


def file(path):
    '''
    file command wrapper
    '''
    if os.path.exists(path):
        result = subprocess.run(['file','-b', path], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip(), True
        else:
            return result.stderr.strip(), False
    return "File not found.", False

def pngcheck(path):
    '''
    pngcheck command wrapper
    '''
    if os.path.exists(path):
        result = subprocess.run(['pngcheck','-7cpqstvx' , path], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return result.stderr.strip()
    return "File not found."

def exiftool(path):
    '''
    exiftool
    '''
    if os.path.exists(path):
        result = subprocess.run(['exiftool', path], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return result.stderr.strip()
    return "File not found."

def strings(path):
    '''
    strings command wrapper
    '''
    if os.path.exists(path):
        result = subprocess.run(['strings', path], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return result.stderr.strip()
    return "File not found."


def stego_analysis(image_path):
    print(f"processing: {image_path} ...")
    analysis_results = {}
    file_result, file_success = file(image_path)
    # print(f"file result: {file_result}")
    analysis_results['file'] = file_result
    if file_success and "image" in file_result.lower():
        # ensure it's an image
        exiftool_result = exiftool(image_path)
        analysis_results['exiftool'] = exiftool_result
        if "PNG image data" in file_result:
            pngcheck_result = pngcheck(image_path)
            print(f"pngcheck result: {pngcheck_result}")
            analysis_results['pngcheck'] = pngcheck_result
        



    