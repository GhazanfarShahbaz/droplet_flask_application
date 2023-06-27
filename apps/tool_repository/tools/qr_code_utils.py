import qrcode

from io import BytesIO


def get_qr_settings() -> qrcode.main.QRCode:
    """
    Returns QR code settings.

    This function returns a QR code object with the following settings:
    - version: 1
    - error_correction: qrcode.constants.ERROR_CORRECT_L
    - box_size: 10
    - border: 4

    Returns:
        A QR code object.
    """
    qr: qrcode.main.QRCode = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    return qr


def qr_code_to_io(qr_code) -> BytesIO:
    """
    Converts a QR code object to a BytesIO object.

    This function takes a QR code object `qr_code` and saves it to a new BytesIO object `img_io`.
    The function then returns the BytesIO object.

    Args:
        qr_code: A QR code object.

    Returns:
        A BytesIO object containing the QR code image data.
    """
    img_io = BytesIO()
    qr_code.save(img_io, "PNG", quality=70)
    img_io.seek(0)

    return img_io


def generate_qrcode_for_url(url: str) -> BytesIO:
    """
    Generates a QR code for the given URL.

    This function takes a string `url` representing a URL and generates a QR code image for it.
    The function returns a BytesIO object containing the QR code image.

    Args:
        url: A string representing the URL to generate a QR code for.

    Returns:
        A BytesIO object containing the QR code image data.
    """
    qr: qrcode.main.QRCode = get_qr_settings()

    qr.make(fit=True)
    qr.add_data(data=url)

    img = qr.make_image(back_color=(0, 0, 0), fill_color=(226, 220, 110))

    return qr_code_to_io(img)
