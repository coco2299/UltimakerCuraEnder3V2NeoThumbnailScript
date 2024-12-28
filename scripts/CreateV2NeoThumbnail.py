# Cura V2Neo Thumbnail creator
# Ken Huffman (huffmancoding@gmail.com)
#
# Modified and fixed by (Reduce Picture Error)
# Coco2299 (corentin.heinix@gmail.com)
#
# This only works with Cura 5.0 or later
# Based on:
# https://github.com/Ultimaker/Cura/blob/master/plugins/PostProcessingPlugin/scripts/CreateThumbnail.py

import os
import base64

from UM.Logger import Logger
from cura.Snapshot import Snapshot
from cura.CuraVersion import CuraVersion

from ..Script import Script

# Hardcoded Base64-encoded default JPG (ensure this is valid for your case)
DEFAULT_BASE64_JPG = (
    "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"
)

class JPEGValidator:
    def __init__(self):
        self.corrupt_jpg_detected = False  # Global flag for corruption detection

    def _message_handler(self, msg_type, context, message):
        """Custom message handler to detect corrupt JPEG errors."""
        if "Corrupt JPEG data" in message:
            self.corrupt_jpg_detected = True  # Set flag if corruption is detected

    def _validateBase64Image(self, base64_data):
        Major=0
        try:
          Major = int(CuraVersion.split(".")[0])
        except:
          pass

        if Major < 5 :
          from PyQt5.QtGui import QImage
          from PyQt5.QtCore import Qt, qInstallMessageHandler
        else :
          from PyQt6.QtGui import QImage
          from PyQt6.QtCore import Qt, qInstallMessageHandler

        """Validate the integrity of a Base64-encoded image."""
        self.corrupt_jpg_detected = False  # Reset the flag before validation
        original_handler = qInstallMessageHandler(self._message_handler)  # Install custom handler

        try:
            # Decode the Base64 string
            binary_data = base64.b64decode(base64_data)

            # Use QImage to load and validate the image
            image = QImage()
            if not image.loadFromData(binary_data, "JPG"):
                print("Base64 validation failed: decoded data is not a valid JPG image.")
                return False

            # Check for corruption flag set by the message handler
            if self.corrupt_jpg_detected:
                print("Corrupt JPEG data detected during validation.")
                return False

            print("Base64 validation succeeded: the data is a valid JPG image.")
            return True
        except base64.binascii.Error as e:
            print(f"Base64 decoding error: {e}")
            return False
        except Exception as e:
            print(f"Unexpected validation error: {e}")
            return False
        finally:
            qInstallMessageHandler(original_handler)  # Restore the original handler

class ModCreateV2NeoThumbnail(Script):
    def __init__(self):
        super().__init__()

    def _createSnapshot(self, width, height):
        Logger.log("d", "Creating thumbnail image...")
        try:
            return Snapshot.snapshot(width, height)
        except Exception:
            Logger.logException("w", "Failed to create snapshot image")

    def _encodeSnapshot(self, snapshot):
        Major=0
        try:
          Major = int(CuraVersion.split(".")[0])
        except:
          pass

        if Major < 5 :
          from PyQt5.QtCore import QByteArray, QIODevice, QBuffer
        else :
          from PyQt6.QtCore import QByteArray, QIODevice, QBuffer

        Logger.log("d", "Encoding thumbnail image...")
        try:
            thumbnail_buffer = QBuffer()
            if Major < 5 :
              thumbnail_buffer.open(QBuffer.ReadWrite)
            else:
              thumbnail_buffer.open(QBuffer.OpenModeFlag.ReadWrite)
            thumbnail_image = snapshot
            thumbnail_image.save(thumbnail_buffer, "JPG")
            thumbnail_data = thumbnail_buffer.data()
            thumbnail_length = thumbnail_data.length()
            base64_bytes = base64.b64encode(thumbnail_data)
            base64_message = base64_bytes.decode('ascii')
            thumbnail_buffer.close()
            Logger.log("d", "Snapshot thumbnail_length={}".format(thumbnail_length))
            return (base64_message, thumbnail_length)
        except Exception:
            Logger.logException("w", "Failed to encode snapshot image")
            
    def _encodeImageFile(self, file_path):
        try:
            if self._validateJPGPath(file_path):
                raise FileNotFoundError("The specified file isn't valid.")

            with open(file_path, "rb") as image_file:
                image_data = image_file.read()
                base64_message = base64.b64encode(image_data).decode('ascii')
                return base64_message, len(image_data)
        except Exception as e:
            Logger.log("w", f"Failed to process image file: {e}")
            return None, 0
    
    def _validateJPGPath(self, value):
        file_path = value.strip("\"'")
        if not os.path.isfile(file_path):
            Logger.log("w", f"File does not exist at the specified path.")
            return "File does not exist at the specified path."
        if not file_path.endswith(('.jpg', '.jpeg')):
            Logger.log("w", f"File must be a JPG image.")
            return "File must be a JPG image."
        if not self._isValidJPEG(file_path):
            Logger.log("w", f"Invalid JPEG file. Please provide a valid file.")
            return "Invalid JPEG file. Please provide a valid file."
        Logger.log("d", f"File valid.")
        return None  # No error means validation passes
    
    def _isValidJPEG(self, file_path):
        """Check if the file has a valid JPEG header."""
        try:
            with open(file_path, "rb") as f:
                header = f.read(2)
                f.seek(-2, os.SEEK_END)
                footer = f.read(2)
                return header == b'\xff\xd8' and footer == b'\xff\xd9'
        except Exception as e:
            Logger.log("w", f"Error checking JPEG file: {e}")
            return False

    def _convertSnapshotToGcode(self, thumbnail_length, encoded_snapshot, width, height, chunk_size=76):
        Logger.log("d", "Converting snapshot into gcode...")
        gcode = []

        # these numbers appear to be related to image size, guessing here
        x1 = (int)(width/80) + 1
        x2 = width - x1
        header = "; jpg begin {}*{} {} {} {} {}".format(
            width, height, thumbnail_length, x1, x2, 500)
        Logger.log("d", "Gcode header={}".format(header))
        gcode.append(header)

        chunks = ["; {}".format(encoded_snapshot[i:i+chunk_size])
                  for i in range(0, len(encoded_snapshot), chunk_size)]
        gcode.extend(chunks)

        gcode.append("; jpg end")
        gcode.append(";")
        gcode.append("")

        return gcode

    def getSettingDataString(self):
        return """{
            "name": "Create V2Neo Thumbnail",
            "key": "CreateV2NeoThumbnail",
            "metadata": {},
            "version": 2,
            "settings":
            {
                "width":
                {
                    "label": "Width",
                    "description": "Width of the generated thumbnail",
                    "unit": "px",
                    "type": "int",
                    "default_value": 200,
                    "minimum_value": 12,
                    "maximum_value": 800,
                    "minimum_value_warning": "The thumbnail width can't be too small",
                    "maximum_value_warning": "The thumbnail width can't be that big"
                },
                "height":
                {
                    "label": "Height",
                    "description": "Height of the generated thumbnail",
                    "unit": "px",
                    "type": "int",
                    "default_value": 200,
                    "minimum_value": 12,
                    "maximum_value": 800,
                    "minimum_value_warning": "The thumbnail height can't be too small",
                    "maximum_value_warning": "The thumbnail height can't be that big"
                },
                "jpg_path":
                {
                    "label": "Default JPG image",
                    "description": "Path to a 200x200 JPG file to use if render fails (leave blank for auto)",
                    "type": "str",
                    "default_value": "",
                    "required": true,
                    "validate": "self._validateJPGPath(value)"
                },
                "max_attempts_count":
                {
                    "label": "Max Attempts Count",
                    "description": "Specifies how many times the snapshot will be recreated in case of a JPEG error before the process aborts. A higher value increases the likelihood of success but also extends the time needed for G-code generation.",
                    "type": "int",
                    "default_value": 10,
                    "minimum_value": 1,
                    "maximum_value": 50,
                    "minimum_value_warning": "Value cannot be lower than 1.",
                    "maximum_value_warning": "Value cannot exceed 50. That will take too much time"
                }
            }
        }"""

    def execute(self, data):
        width = self.getSettingValueByKey("width")
        height = self.getSettingValueByKey("height")
        jpg_path = self.getSettingValueByKey("jpg_path")
        max_attempts_count = self.getSettingValueByKey("max_attempts_count")
        Logger.log("d", f"ModCreateV2NeoThumbnail Plugin start with width={width}, height={height}, jpg_path={jpg_path}...")

        validator = JPEGValidator()
        
        valid_encoded_snapshot = None

        for attempt in range(max_attempts_count):
            snapshot = self._createSnapshot(width, height)
            
            if attempt > 1 and not snapshot and valid_encoded_snapshot == None:
                Logger.logException("w", f"Cancel snapshot creation : Failed {attempt} times in a row")
                break
            
            if snapshot:
                Logger.log("d", f"Snapshot created (attempt {attempt + 1})")
                encoded_snapshot, thumbnail_length = self._encodeSnapshot(snapshot)

                is_valid = validator._validateBase64Image(encoded_snapshot)
                if is_valid:
                    valid_encoded_snapshot = encoded_snapshot
                    Logger.log("d", f"Snapshot valid (attempt {attempt + 1})")
                    break

                if attempt == max_attempts_count-1:
                    Logger.log("d", f"No Valid Snapshot found after {attempt + 1} attempts")

        encoded_snapshot = valid_encoded_snapshot

        # If snapshot fails, try to use the provided JPG file
        if not encoded_snapshot and jpg_path:
            Logger.log("d", "Falling back to the provided JPG file")
            encoded_snapshot, thumbnail_length = self._encodeImageFile(jpg_path)

        # If JPG file fails, use the default hardcoded base64 image
        if not encoded_snapshot:
            Logger.log("d", "Using the default hardcoded base64 image")
            encoded_snapshot = DEFAULT_BASE64_JPG
            thumbnail_length = len(base64.b64decode(DEFAULT_BASE64_JPG))

        # Convert snapshot (or fallback image) to G-code
        if encoded_snapshot:
            snapshot_gcode = self._convertSnapshotToGcode(
                thumbnail_length, encoded_snapshot, width, height)

            # Insert G-code at the top of the file
            if data:
                layer_index = 0
                lines = data[layer_index].split("\n")
                lines[0:0] = snapshot_gcode
                data[layer_index] = "\n".join(lines)

        Logger.log("d", "ModCreateV2NeoThumbnail Plugin end")
        return data
