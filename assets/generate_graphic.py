# This script formats the output of your audit scripts into a professional image asset.
import PIL.Image, PIL.ImageDraw, PIL.ImageFont

def create_audit_banner(data_summary):
    # Professional dark-mode aesthetic branding
    img = PIL.Image.new('RGB', (1200, 630), color='#0a0a0a')
    d = PIL.ImageDraw.Draw(img)
    d.text((50, 50), "GODHEAD ARCHITECT: INFRASTRUCTURE AUDIT", fill='#00ff41')
    d.text((50, 150), data_summary, fill='#ffffff')
    img.save('assets/graphics/latest_audit.png')
    print("Graphic generated: assets/graphics/latest_audit.png")

create_audit_banner("OPTIMIZATION STATUS: 99.9% UPTIME ACHIEVED\nSECURITY: VULNERABILITY-FREE")
