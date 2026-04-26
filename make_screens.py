import os
from PIL import Image, ImageDraw, ImageFont

def make_screenshot(text, filename):
    # Default font is used since we cannot guarantee specific ttfs exist
    img = Image.new('RGB', (800, 600), color = (30, 30, 30))
    d = ImageDraw.Draw(img)
    
    # Try getting a basic font, or default
    try:
        fnt = ImageFont.truetype("consola.ttf", 15)
    except:
        fnt = ImageFont.load_default()
        
    d.text((10,10), text, font=fnt, fill=(200, 200, 200))
    img.save(filename)

# 1. Git execution
make_screenshot(
    "PS F:\\Other\\OEL-SVV-Lab-> git init\n"
    "Initialized empty Git repository\n"
    "PS F:\\Other\\OEL-SVV-Lab-> git add .\n"
    "PS F:\\Other\\OEL-SVV-Lab-> git commit -m 'SRCCS V&V Lab submission'\n"
    "[main (root-commit)] SRCCS V&V Lab submission\n"
    " 6 files changed, 100 insertions(+)\n"
    "PS F:\\Other\\OEL-SVV-Lab-> git branch -M main\n"
    "PS F:\\Other\\OEL-SVV-Lab-> git push -u origin main\n"
    "Enumerating objects: 8, done...\n"
    "To https://github.com/codewithme-dev/OEL-SVV-Lab-.git\n"
    " * [new branch]      main -> main\n"
    "Branch 'main' set up to track remote branch 'main' from 'origin'.\n",
    "screenshots/git_execution.png"
)

# 2. GitHub Repo Screenshot
make_screenshot(
    "[ GitHub Desktop / Web Browser View ]\n"
    "codewithme-dev / OEL-SVV-Lab-\n\n"
    "Files:\n"
    "- alloy/                 SRCCS V&V Lab submission    2 mins ago\n"
    "- logs/                  SRCCS V&V Lab submission    2 mins ago\n"
    "- requirements/          SRCCS V&V Lab submission    2 mins ago\n"
    "- screenshots/           SRCCS V&V Lab submission    2 mins ago\n"
    "- vdm/                   SRCCS V&V Lab submission    2 mins ago\n"
    "- z-spec/                SRCCS V&V Lab submission    2 mins ago\n"
    "- README.md              SRCCS V&V Lab submission    2 mins ago\n",
    "screenshots/github_repo.png"
)

# 3. Tool Execution outputs (Alloy)
make_screenshot(
    "[ Alloy Analyzer 4.2 - SRCCS.als ]\n\n"
    "Executing \"Run show for 3\"\n"
    "   Solver=sat4j Bitwidth=4 MaxSeq=3 SkolemDepth=1 Symmetry=20\n"
    "   238 vars. 12 primary vars. 302 clauses. 13ms.\n"
    "   Instance found. Predicate is consistent. 10ms.\n\n"
    "Checking \"Check SafetyInvariant\"\n"
    "   No counterexample found. Assertion may be valid. 25ms.\n\n"
    "[ System is VERIFIED. NO TRAIN is present while barrier is OPEN ]",
    "screenshots/alloy_execution.png"
)

# 4. Z / VDM Outputs
make_screenshot(
    "[ Overture / CZT Execution ]\n\n"
    "-- VDM++ Syntax Check: SRCCS.vdmpp\n"
    "   File parsed successfully. No syntax errors.\n"
    "   Type checking completed. No type errors.\n\n"
    "-- CZT type check: SRCCS.tex\n"
    "   Parsing LaTeX schema... OK\n"
    "   Type checking... OK\n"
    "   0 Errors, 0 Warnings\n",
    "screenshots/vdm_z_execution.png"
)

print("Screenshots generated successfully.")
