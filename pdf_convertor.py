import pdfkit
import os

# --- Configuration ---
html_file_path = 'index.html' # Make sure this file exists in the same folder
pdf_file_path = 'nikolay_dimitrov_cv_styled.pdf' # New name to avoid overwriting

path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

try:
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    print(f"Using wkhtmltopdf configuration: {path_wkhtmltopdf}")
except OSError:
    print(f"Error: Could not find wkhtmltopdf executable at the specified path: {path_wkhtmltopdf}")
    config = None

# --- Conversion ---
if config:
    print(f"Converting '{html_file_path}' to '{pdf_file_path}'...")

    # --- Adjusted Options ---
    options = {
        'page-size': 'A4',
        'margin-top': '20mm',
        'margin-right': '20mm',
        'margin-bottom': '20mm',
        'margin-left': '20mm',
        'encoding': "UTF-8",

        # --- Key Options for Styling/Images ---
        'enable-local-file-access': None, # CRUCIAL: Allows access to nikidimitrow.png
        # 'load-error-handling': 'ignore', # Try uncommenting this if you suspect minor loading errors break things
        # 'load-media-error-handling': 'ignore', # Specific for media errors
        '--enable-javascript': None,       # Enable JS if any dynamic styling depends on it (unlikely here)
        '--javascript-delay': '1000',      # Give JS time to run (if enabled, milliseconds) - adjust if needed
        '--no-stop-slow-scripts': None,    # Don't stop scripts that take time (if JS enabled)
        '--enable-plugins': None,          # May be needed for some complex elements (rarely)
        '--images': None,                  # Explicitly enable images (usually default)
        '--enable-external-links': None,   # Allow linking to external resources (like Google Fonts)

        # --- Try EITHER print OR screen styles ---
        # Option 1: Use Print Styles (as defined in your @media print CSS)
        '--print-media-type': None,

        # Option 2: Force Screen Styles (Comment out --print-media-type above if using this)
        # This is NOT a standard wkhtmltopdf option, but sometimes omitting --print-media-type defaults to screen.
        # If Option 1 fails, try REMOVING the '--print-media-type': None line completely.

        #'--debug-javascript': None,       # Uncomment to see JS console output (if JS enabled)
        #'--disable-smart-shrinking': None # Can sometimes help with layout accuracy
    }

    try:
        if not os.path.exists(html_file_path):
             print(f"Error: HTML file not found at '{os.path.abspath(html_file_path)}'")
        elif not os.path.exists(os.path.join(os.path.dirname(html_file_path), 'nikidimitrow.png')):
            # Explicitly check if the image file exists where expected
            print(f"Warning: Image file 'nikidimitrow.png' not found in the same directory as the HTML.")
            print(f"Expected location: {os.path.abspath(os.path.join(os.path.dirname(html_file_path), 'nikidimitrow.png'))}")
            # Proceed anyway, but PDF might lack the image
            success = pdfkit.from_file(
                 html_file_path,
                 pdf_file_path,
                 options=options,
                 configuration=config
            )
        else:
            print("HTML and Image files seem accessible.")
            success = pdfkit.from_file(
                 html_file_path,
                 pdf_file_path,
                 options=options,
                 configuration=config
            )

        if success:
            print(f"Conversion successful! PDF saved as '{os.path.abspath(pdf_file_path)}'")
        else:
            print("Conversion failed (pdfkit returned False). Check console for errors.")

    except Exception as e:
        print(f"An error occurred during conversion: {e}")
        if 'ContentNotFoundError' in str(e) or 'Exit with code 1' in str(e):
             print("This often indicates wkhtmltopdf had trouble loading resources (images, CSS, fonts) or executing.")
             print("Verify paths and permissions. Try running wkhtmltopdf directly:")
             print(f'"{path_wkhtmltopdf}" --enable-local-file-access "{os.path.abspath(html_file_path)}" test_manual.pdf')
else:
    print("Cannot proceed with conversion due to invalid wkhtmltopdf configuration.")