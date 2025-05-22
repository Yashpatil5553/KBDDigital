import os
import sys
import django

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "KBDDigitalPRO.settings")
django.setup()

from homeapp.models import User
import qrcode

output_dir = os.path.join("static", "qrcodes")
os.makedirs(output_dir, exist_ok=True)

for user in User.objects.all():
    folio = user.Folio_Number
    data = f"{folio}"
    img = qrcode.make(data)

    file_path = os.path.join(output_dir, f"{folio}.png")
    img.save(file_path)
    print(f"✅ QR code saved for {folio}")
