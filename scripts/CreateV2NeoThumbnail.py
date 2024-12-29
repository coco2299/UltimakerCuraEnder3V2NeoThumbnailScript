# Cura V2Neo Thumbnail creator
# Ken Huffman (huffmancoding@gmail.com)
#
# Modified and fixed by (Reduce Picture Error)
# Corentin Heinix (corentin.heinix@gmail.com)
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
    "/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAAQDAwMDAgQDAwMEBAQFBgoGBgUFBgwICQcKDgwPDg4MDQ0PERYTDxAVEQ0NExoTFRcYGRkZDxIbHRsYHRYYGRj/2wBDAQQEBAYFBgsGBgsYEA0QGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBj/wAARCADIAMgDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD7+ooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigBKPejpXiX7R3xbvfht4Ht9O8OTxx+JNWZktpGUP9liXHmTbTwSMqq5BG5gSCARUzmoK7MqtVUouctke17hnGRTq/K6XXPHFxqja9N4q8SyXe/ebw6lcbg31DAD6DA9q+0f2ZvjFqfj3Qbvwv4su1uNf0xVkjuWAVry3PAdgABvU/K2OuVOBnFYU8TGb5Tiw2ZQrz5LWPoGiiiuk9IKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAK13dW9hYTXt3MsMEMZkkkc4CKBkk+wAr88viZ4pufiJ8TdR8TzFxbyMIbKJsjyrdMhBjsTkufdiO1fTn7SXjb7F4Yi8D2EuLnUh5l4VP3LcH7p/wB8jH+6rV8nakBa2mTwznaPevAzHGc1RUYdDx80rpRa6IgTy1tBb4GzbtxV7wTrt/4G8f6Z4p0wM0tlLl4l48+I8SR/8CXOPcKe1RxeGPFk3hF/FMPh3Un0RM7tRWH90oHBOeu0Y5YDaOcmodL23UDj+NDyPb/INcU3Oiuc+ay6co1bS66o/R7R9Wsdd0Cz1nS51ns7uJZ4ZV6MrDIq/ivnL9mjxqVt7jwBqEx+TddaeWP8JOZI/wACdw9mPpX0d2r6LCYhYikpo+5pT54phRRRXUaBRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFZ+r6rZaHoN3q2oSiK1tYmlkb0UCtDtXgnx98Wl2g8GWMuFG24vtp6944//Zj9FrhzDFrC0HUe/T1InLlVzw3xPrF94r8W33iDUBia6k3CPOfKQcKg+gwPrmuNtNBvvHPxY0zwXpRIknlWBpFGfKX70sn/AAFAT9QB3rqL2SKw06e9nOI4UMjfh/kV6j+yN4ElNlqnxP1aH9/fu9pYbh0jD5lcf7zgKPaP3r5fJqcsTVdSR8/iaTxFWFHvq/RH0fY+H9K0/wAIweGraziXTYbUWiW+Pl8oLt249McV8AeKPC0/w3+Nt/4Ruc/ZhJi1kb+O3fmFvwwUPurV+ivU184fta+AG1fwFa+PtMi/07Qji5ZRybViMt/wBwr+y76+ox2GVWk0deaYW9NVILWH5HjOjXl7oPiCz1rTXCXdnKJoieASOx9iMg+xNfb3hjX7LxP4VstcsD+5uog+09Uboyn3BBB+lfDek3CapolrfoMebGCy/wB1uhH4HNe4/Abxc2m63L4RvZcW14TNakn7koHzL/wIDP1U+tfLZNj3QxDoVNnp8zowlRfJn0XRRRX256AUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAGP4m1208NeF7zWbw/u4IyQvd26Ko9ySBXx/qV5datq9zqd/J5l1cyGWRvUn09hwB7CvVfjX4r/tPXo/DVpJm2sTvnKnhpiOB/wEH829q8p2+1fnfEOZe3r+yh8MfzOOvO7scv4g0u/8TaxongLRm26hrt4sAYDPlRr8zyH2UAn324r7s8O6Dp/hjwpp3h7SoRDZWFultCg7KowPx4r5+/Zz8IDVfGuufE69TdDAW0TSMjjah/0iUfWQeX/2zb1r6UJCAliABX1WR4b2GFi5bvUjCUtXVfXb0FqrqFhaappVzpt/Ak9tcxNDLE4yrowwQfqDVM+JvDi3P2Vte00TZx5ZuUB/LNaiOjxhkYMD0IOQa9aNWE9Iu53aSVj4HtPDt14C+IXiL4cXzOx06cT2Tv1mtZOUYevGAf8AaDVvW8k9neRXdpKYZ4XWSOReqMDkH+VerftLeEBC2i/FKxixJpT/AGDVNo+9ZTMAHP8A1zkKt6BWc15bs9RX55xBQeGxXNHZ6nlU6fsm6fbb0PrfwX4lh8WeDbPV48LKy7J4x/yzlHDL+fT2Iroq+bvg74q/sHxf/ZF1JtstTIQZPCTD7p/H7p/4DX0jX2OTY9Y3DqT+JaM9OnLmjcKKKK9YsKKKKACiiigAooooAKKKKACiiigAooooAO1c5428Sw+FPB91qjYaYDy7dD/HI33R9O59ga6Imvm/4t+K/wC3vGB021l3WOnExjaeHl6O34fdH/Aq8fOswWDw7kvieiInLlRwE0ktxcSXFw5llkYvI7dWYnJP4nNVL5pI9NneF1jkCfLIRuEfbeR3C9SPY1ZpGdY0LuyooGSScYr8tjN86k9Thaue7xePvh/8NvA2l+FvDN0mtPZWkccFvYyiX5ccSSy8qu7ljk5OTgGvGfiH8ZdWvYXXV70xxsP3elaecA+m49SPdsD2rjNQ1aYRtb6TGsCdTKFA6/3R/WuXfSGllaSTc7sclmOSa+sq5jVxllU9yC6LqZ1K07csSg3xH8R/atyaNpi22f8AUEOTj/e/+xr174d/GLVbILHpF60BHMmlXp3xn12e3uuPcV5f/Yh/55cfShdHKurKCGHII7VEvYRtKh7kls0c1KVWm73ufY+n/E7wP440C68M+LEh0qS+t3tp7S/cCC4RlIYRynCtxng4b2r56soUgs/ssd59uit3eCK8/wCfmNHKJL/wNVVvTnjisPTtVuEh+y6on2mLpvZcn/gQ/irpI5EliDxMrKR1FcObZlVxNOMK0VePVdTt5/aasUZDBlypHIKnBH0r6k+HXioeK/BcNzM4+3QfuLpR/fA+99GGD+NfLldn8MvFX/CL+NYvPk22F5i3uMnhcn5X/A9fYn0qcgzH6piUpfDLRm1KXK7H0/RSA5GaWv1Hc6wooooAKKKKACiiigAooooAKKKKACiiigDjfiR4qHhbwXNLbuFvrn9xaj0Yjlv+AjJ/KvmDGSSSSeuT3ruvizrV1qnxJu7SYMkGn4t4Y/qoZm/EkfgBXE29rd312tpZW01xM3SKFC7H8BX5fn2NljMW4R2jojkqyu7FeSQIOBubsBWdcJJP80x+UdugFeteHvgn4j1TbNrEsekwHna37yY/8BHC/ifwr1fw78LvCPh0pNFp4vLtf+Xm7/eMD7Dov4CtcBkGKre848q7v/ISoylufOHh34Y+KvExV9O0mSO2b/l6uf3UY+meW/AGvXPD37PWg2kay+JL+fUZephgJhiH5fMfzH0r2cKAMAUdK+uwmQ4ejrP3n57GsaEEcQPhB8NhD5f/AAidjj1O4t+ec1yniD9nzw1extL4eu7jS5+ojcmeE/gTuH4GvY6Su+pluGqR5XBfLQ0dOL6HyH4i+FHi3w0XkutLa6tV5+1Wf71QPcAbl/EY965aCJ4G3wnHbA5Br7lIz15rkfEXw38JeJS0t5piQXTf8vVr+6k/EjhvxBr53G8NNq+Hl8mYPDL7J8sRyhxhhtb09alKggg8jGCK9L8QfA/XdP3TaHcx6pCP+WT4imH/ALK35ivO7yxvtMu/smo2k9rOP+WUyFG/DPX8K+OxeX18K/3kGvy+8zcJR3Por4UeKj4h8GrZ3Uu+/sMQyljy6/wP+I4PuDXoFfLXw31m60f4jaa1tlkupVtJox/ErnH6HB/A19SD1r9C4exzxWFSlvHQ6qcuZC0UUV75oFFFFABRRRQAUUVBd3dpYWUt5fXEVtbxLukmmcIiKO5J4AoAnoryW4/ae/Z+tbgwy/FnwyWXvFc+Yv8A30oIqL/hqb9nr/orHh7/AL+t/hQB6/RXA698bPhT4W8O6Jr3iHxxpenabrkJuNMup3IS7jAU7k46Ydfzrnf+Gpv2ev8AorHh7/v63/xNAHa+Ifh54W8Tamuo6nYubkABpIZWjLgdA2OuK2NI0DRtBsxbaRp1vaR9xEmC31PU/jXm0H7T/wCz7cTpDH8WfDQZjgGS58tR9WYAD8a9Wt7iC7tY7m1njmhkUOkkbBldT0II4IrmjhKMZuooJSfWwrLcmorn/Ffjjwf4G0ldT8Y+JtK0O0Ztiy6hcrCGb0XJ5PsK4A/tTfs9A4/4Wx4e/CVv8K6Rnr9FeY+Hv2hfgr4q8TWXh3w58RtG1LVL2Tyre0t3YvK2CcDj0Br06gAorN1TXtG0SbT4dW1K1spNRulsrNZ5ApuJyrMI0z1YhGOPRTWlQAUVz/jDxt4U8AeGzr/jHW7bR9MEqwG6uSQgdvujIB64NXPD3iDRvFXhmz8Q+Hr+LUNLvY/Nt7qL7kq5xkZ7cUAalUNT0bS9Zsza6rp9vdwn+GZA35elX64jxP8AF34beDPGNl4T8T+MNN0zW75Y3trCdiJJhI5jQgAHqwIH0NROnGa5ZK6AsaL8NvCOga3/AGpp+nN9pXJjMsrSCLP90E8fWuu7V5lr/wC0L8FvCnia88O+I/iLo2m6rZP5VzaXDsrxNgHBGPQis3/hqb9nr/orHh7/AL+t/wDE1FHD06EeWlFJeQkrHsFFeP8A/DU37PX/AEVjw9/39b/4mu58FfELwT8RdHn1XwP4lsNcs4JvIlls5NwjkwDtYdQcEH8a2GdPRRXnWt/HX4ReHfG8ng7WfHuk22vRypA2mh2eYSPjYm1QfmO5cDryKAPRaKQHK5ooAWvzx+Nnibxz+07+1XL8DfBd8lt4b0q6e3l3EmB2gK/aLqYDG8I58tE9QMYLbk/Q49K/Or4Ba3pvws/4KM+MdC8aPBp02p3N/pdtdXZC4mkuhcQgNnAEqMuPU7B1IoGj2LTf2APhPBpsUeqeJvF9/dBQHnS7SBScfwoqYUe3P1q5/wAMDfBcHI1bxiP+4mP/AIivqfPFFArn59/t3eGLDwV8LfhL4R0eW5+w6PbXlnbPM+6TZFbxqm4gDJwBnivRdJ/Yh+Bl34fsLq58ReJ0nmto5JFGroMMVBPG3jk1yn/BR3/kFeAP97Uv/RKVvftF/sp23xI+H1l8RfAWnQL4wi02Br2zVFxqqLEvIzwJwOB2cfKedpAMofEf9jX4IeGvhTr/AIgsPHeuaXc6fZS3MVzealHNCGVSQrptBYE4GAQeeOaZ+x38Vb3wx+yJ481rxPLcXOj+EZDcWkTfeRWt1lMCdOPM6DoN+BgYFfKPwO+D+j/FT4lSeCte8aWnhLVC4W2hudM8xrplJ3xISybJRtOFYc4PGVYV96/E74F6N4G/4J/eMvh58P7W4Z0sWv5pgoa4v5o2WSRn2gZZlj2hQMAAKBgAUAz5g+Fvwu8Y/tcfEzWviL8S/F82m6RbXHkGeJkMhcgt9ls1clYo41ZcsVOc9C24j6EH7C3wHCgHxL4pPHU6unP/AI5XyJ8Av2b7b462OrCx8faRpeq6fMN2nXlg80jwMAVmQiRcoSWB44IOeor2j/h3Jrv/AEUfw/8A+CaX/wCPUDPdfAn7Ivwf8B/EfRvF+ga94gl1LTLj7RbxXGpJLGzbGTDLtyeHPTB6V9H9BXxf8Jv2HtZ+Gvxp8O+OZ/HWj3sek3RuGtrfS5InlHlum0OZSB9/PTsK9c/ap+MP/Co/gVcvpd0sPiTWt2naVgjdEzL+8nAPH7tMsM8Ftg70Enx1+2D8a9T8c/HuPRfCN1cHSfBUpaG4tlZgLyNgZbrjjEbBEVjwCsmThxX3T8AfizZ/GT4I6Z4sTZFqaf6JqlqpH7m6QDfwOisCrr/suK8F/Y1+AGlRfBHVvGPjPS47qbxpZPaQwTqCU0x/fGczH94T3AjzyK8w+DGvav8Assftman8LfFlzIfDmsTx2ZuZS21g7EWd50x82fLc9iT2SgZ9Cft0Ej9lBiD/AMxuw/8ARldz+y5/yZ38Pf8AsER/zNcN+3T/AMmnt/2G7D/0ZXc/suf8mdfD3/sER/zNAHrtfn9+2AT/AMN3/Ddcnb9n03j/ALiYr9Aa/P39sD/k/H4bf9e2m/8ApzFAI968cfsbfC34gfEXV/Geuan4nTUNVuPtEyWt6sUatsVMKoTphB1Jr4z+NfwO8JeAP2wPCfwz0O/1ptG1Q6WJ2uLrfMPtN28Mm1sDHyqMccGv1Ur8+P2o/wDlJJ8Pf97QP/TlLQCPX/8AhgX4LZ/5CvjH6f2mP/iK+erzT/G/7D/7S6anbyXmteDNW+RSx5v7QHJifoouYssVPAOc/dZtn6W1xHxW+F/hn4vfDO98G+J4CYJh5lvcx/620nX7k0Z/vA9uhBIOQaAueNfHj9rLwt4N+CGl6t4B1OHVNc8UWZn0hlGRawkfNcTKcbSpOAjYJfIOArEcR+xt+zvf6cV+NHxGjmuNXvS1xo9rfFpJYg+S95KW5Msm5tuRkKSTy+F8M/ZP+Bvh7x1+0prGn+K3S9sPCrNcvaKmEvpY7hokD9/LDRlypznhScbt36iKoRQqgADgADGKAY6iiigQV83ftJ/spaR8bZV8T6HqEWjeLYYBB5s6F7a9ReUWZRyCuThxyAcEMMAfSNFAHwHpfwc/bq8P6culaV47mSzhJWJT4hWYAezSws+PQE8dMCrv/Ctf2/M/8j7J/wCDu3/+R6+76KAufGv7QfwE+NHxY+Dfww0yGOx1LxJo2nyprlxd36x77h4I0LK2MNlg54x09+PrnQ7aWz8MadZXChZoLWKJwDnDKgB/UVo0UAfJn7S/7JsvxA1yP4g/C/7Pp/i3zVa7tzN9mjvCMYmDgfu5lwvzD7wUdGVSPZPgu3xcX4erovxm0mxGsWiiJdStLtLhL+PoDIoA2yAYDcbW6jHQen0UBc+Hfil+xT4p0v4ht43/AGf9fi0dncyrpZu3sZLNjnd9nnQEeWeMRsAAOMlQFFEfDT9vsDA8eyYH/Ubt/wD4xX3hRQFz49+F/gP9srTPjD4ev/iB4we88MQ3W7Ubf+1YZd8exhjasSk/Nt79qp/FT9nb4sfHH9q+z1zxnbWdj8PbSRbOKKPUd0wsk+Z8RLwJJn4LA5ClO6V9nUUDufMXxz8M/tQ6342srH4LXVt4c8LabaLBH5OoRW73MnclWR8IoCqo46Me4r538a/ssftZfETVLXUPG13p2uXFtEYI5LvWItyxscsmViXgn8u1fpLRQI+W/HXwr+M/xL/YbsfAHiS201fHWn3Nqzu16pivkgcYfzAPlcoecj7ynsa8h8PfBX9uTwt4YsvD3h/xathpllH5Ntaw63BsiQdFGYCcfjX6BUUDufBz/DX9v3yn2ePZNxU7f+J1B17f8sB/Suw+OPwB+KXxA/aM8BeNtGsbCfT9HstOjv5ri/VJPMiuvOlwuPm4Awc8k+3P2DRQIK+R/jj8APiR47/bM8JfEfw9Y6fLoOmHSjcyzXixyL9nvHmk2pj5vlYY5HNfXFFABQelFFAHyr+zN8DPiH8MPjl468UeLrGxg0/WVkFm1vdrKxzdSSjcoHy/K49elfVVFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRQAAFFFAH//Z"
)

class ImageResizer:
    def __init__(self):
        pass

    def _resize_image_to_target_size(self, image_path, target_size=8192, max_width=200, max_height=200):
        Major = 0
        try:
            Major = int(CuraVersion.split(".")[0])
        except Exception:
            pass

        if Major < 5:
            from PyQt5.QtGui import QImage
            from PyQt5.QtCore import Qt, QBuffer, QIODevice
        else:
            from PyQt6.QtGui import QImage
            from PyQt6.QtCore import Qt, QBuffer, QIODevice

        try:
            # Load image
            image = QImage(image_path)
            if image.isNull():
                raise ValueError(f"Invalid image at path: {image_path}")

            # Resize with aspect ratio
            resized_image = image.scaled(max_width, max_height, Qt.AspectRatioMode.IgnoreAspectRatio)

            # Initialize quality and buffer
            quality = 100
            thumbnail_data = None
            thumbnail_size = 0

            while quality >= 10:
                buffer = QBuffer()
                buffer.open(QIODevice.OpenModeFlag.WriteOnly)

                # Save image to buffer with current quality
                resized_image.save(buffer, "JPEG", quality)

                # Get buffer size and data
                thumbnail_size = buffer.size()  # Accurate raw binary size
                thumbnail_data = buffer.data()

                # Ensure the image size is strictly below the target size
                if thumbnail_size < target_size:
                    Logger.log("d", f"Found suitable quality: {quality}, Thumbnail size: {thumbnail_size} bytes")
                    break
                elif thumbnail_size < target_size:
                    quality += 1
                else:
                    quality -= 1
                
                buffer.close()  # Ensure the buffer is fully reset

            if not thumbnail_data:
                raise ValueError("Failed to generate thumbnail.")
            

            validator = JPEGValidator()
            base64_message = base64.b64encode(thumbnail_data).decode('ascii')
            if validator._validateBase64Image(base64_message):
                return thumbnail_data, thumbnail_size
            return self._resize_to_quality_or_try_lower(image_path, max_width, max_height, quality)

        except Exception as e:
            Logger.log("w", f"Error in ImageResizer: {e}")
            return None, 0
        
    def _resize_to_quality_or_try_lower(self, image_path, max_width=200, max_height=200, quality=100):
        Major = 0
        try:
            Major = int(CuraVersion.split(".")[0])
        except Exception:
            pass

        if Major < 5:
            from PyQt5.QtGui import QImage
            from PyQt5.QtCore import Qt, QBuffer, QIODevice
        else:
            from PyQt6.QtGui import QImage
            from PyQt6.QtCore import Qt, QBuffer, QIODevice

        try:
            # Load image
            image = QImage(image_path)
            if image.isNull():
                raise ValueError(f"Invalid image at path: {image_path}")

            # Resize with aspect ratio
            resized_image = image.scaled(max_width, max_height, Qt.AspectRatioMode.IgnoreAspectRatio)

            thumbnail_data = None
            thumbnail_size = 0

            validator = JPEGValidator()

            for attempt in range(10):
                buffer = QBuffer()
                buffer.open(QIODevice.OpenModeFlag.WriteOnly)

                # Save image to buffer with current quality
                resized_image.save(buffer, "JPEG", quality)

                # Get buffer size and data
                thumbnail_size = buffer.size()  # Accurate raw binary size
                thumbnail_data = buffer.data()
                
                buffer.close()  # Ensure the buffer is fully reset

                base64_message = base64.b64encode(thumbnail_data).decode('ascii')
                if validator._validateBase64Image(base64_message):
                    Logger.log("d", f"Image succesfully scaled at attempt {attempt+1}, quality = {quality}")
                    return thumbnail_data, thumbnail_size
                
                quality -= 1

            raise ValueError("Failed to generate scaled thumbnail.")

        except Exception as e:
            Logger.log("w", f"Error in ImageResizer: {e}")
            return None, 0
        

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
                Logger.log("w", "Base64 validation failed: decoded data is not a valid JPG image.")
                return False

            # Check for corruption flag set by the message handler
            if self.corrupt_jpg_detected:
                Logger.log("w", "Corrupt JPEG data detected during validation.")
                return False

            Logger.log("d", "Base64 validation succeeded: the data is a valid JPG image.")
            return True
        except base64.binascii.Error as e:
            Logger.log("w", f"Base64 decoding error: {e}")
            return False
        except Exception as e:
            Logger.log("w", f"Unexpected validation error: {e}")
            return False
        finally:
            qInstallMessageHandler(original_handler)  # Restore the original handler

    def _validateJPGPath(self, file_path):
        if not os.path.isfile(file_path):
            Logger.log("w", f"File does not exist at the specified path.")
            return "File does not exist at the specified path."
        if not file_path.endswith(('.jpg', '.jpeg')):
            Logger.log("w", f"File must be a JPG image.")
            return "File must be a JPG image."
        if not self._isValidJPEG(file_path):
            Logger.log("w", f"Invalid JPEG file. Please provide a valid file.")
            return "Invalid JPEG file. Please provide a valid file."
        Logger.log("d", f"File type valid.")
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
            
    def _encodeImageFile(self, file_path, width=200, height=200, max_thumbnail_length=8192):
        try:
            validator = JPEGValidator()

            file_path = file_path.strip("\"'")
            if validator._validateJPGPath(file_path):
                raise FileNotFoundError("The specified file isn't valid.")

            with open(file_path, "rb") as image_file:
                image_data = image_file.read()
                base64_message = base64.b64encode(image_data).decode('ascii')

                is_valid = validator._validateBase64Image(base64_message)
                if not is_valid:
                    raise FileNotFoundError("The specified file isn't valid or corrupted.")
                
                imageResizer = ImageResizer()
                Logger.log("d", f"Image size before resizing: {len(image_data)} bytes")
                # Resize the image to target width and height
                resized_image_data, image_size = imageResizer._resize_image_to_target_size(file_path, target_size=max_thumbnail_length, max_width=width, max_height=height)
                if image_size == 0:
                    raise FileNotFoundError("Failed to resize the image.")
                image_data = resized_image_data
                base64_message = base64.b64encode(image_data).decode('ascii')
                Logger.log("d", f"Resized image size: {image_size} bytes")
                is_valid = validator._validateBase64Image(base64_message)
                if not is_valid:
                    raise FileNotFoundError("Failed to scaled the image successfully")

                return base64_message, len(image_data)
        except Exception as e:
            Logger.log("w", f"Failed to process image file: {e}")
            return None, 0

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
            "key": "ModCreateV2NeoThumbnail",
            "metadata": {},
            "version": 2,
            "settings":
            {
                "width":
                {
                    "label": "Width",
                    "description": "Width of the generated thumbnail. I made a few tries and only 200px work but you're free to try something else. (recommended 200px)",
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
                    "description": "Height of the generated thumbnail. I made a few tries and only 200px work but you're free to try something else. (recommended 200px)",
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
                    "description": "Path to a file to use if render fails. The image will be resize to the size you set but the printer mostly work with 200x200px. The quality can be affected and the image can loose ratio. (leave blank for auto)",
                    "type": "str",
                    "default_value": "",
                    "required": true
                },
                "max_attempts_count":
                {
                    "label": "Max Attempts Count",
                    "description": "Specifies how many times the snapshot will be recreated in case of a JPEG error before the process aborts. A higher value increases the likelihood of success but also extends the time needed for G-code generation. (recommended 10)",
                    "type": "int",
                    "default_value": 10,
                    "minimum_value": 1,
                    "maximum_value": 50,
                    "minimum_value_warning": "Value cannot be lower than 1.",
                    "maximum_value_warning": "Value cannot exceed 50. That will take too much time"
                },
                "max_thumbnail_length":
                {
                    "label": "Max Thumbnail length",
                    "description": "A larger thumbnail length can cause the printer to take a long time to load the image. (recommended max 8000)",
                    "type": "int",
                    "default_value": 8000,
                    "minimum_value": 2000,
                    "maximum_value": 8192,
                    "minimum_value_warning": "Value cannot be lower than 2000. The quality will be very low.",
                    "maximum_value_warning": "Value cannot exceed 8192. It will cause issue all the time."
                }
            }
        }"""

    def execute(self, data):
        width = self.getSettingValueByKey("width")
        height = self.getSettingValueByKey("height")
        jpg_path = self.getSettingValueByKey("jpg_path")
        max_attempts_count = self.getSettingValueByKey("max_attempts_count")
        max_thumbnail_length = self.getSettingValueByKey("max_thumbnail_length")
        Logger.log("d", f"ModCreateV2NeoThumbnail Plugin start with width={width}, height={height}, jpg_path={jpg_path}...")

        validator = JPEGValidator()
        
        valid_encoded_snapshot = None

        for attempt in range(max_attempts_count):
            snapshot = self._createSnapshot(width, height)
            
            if attempt+1 > 1 and attempt+1 <= max_attempts_count and not snapshot and valid_encoded_snapshot == None:
                Logger.logException("w", f"Cancel snapshot creation : Failed {attempt+1} times in a row")
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
            encoded_snapshot, thumbnail_length = self._encodeImageFile(jpg_path, width, height, max_thumbnail_length)

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
