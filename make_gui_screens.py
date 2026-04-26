import asyncio
from playwright.async_api import async_playwright
import os

alloy_code = """module SRCCS
abstract sig BarrierState {}
one sig Open extends BarrierState {}
one sig Closed extends BarrierState {}

abstract sig TrainState {}
one sig Present extends TrainState {}
one sig NotPresent extends TrainState {}

sig Sensor { detects: TrainState }
sig Barrier { state: BarrierState }

sig CrossingSystem {
  sensor: one Sensor,
  barrier: one Barrier
}

fact SafetyInvariant {
  all sys: CrossingSystem |
    (sys.sensor.detects = Present) implies (sys.barrier.state = Closed)
}

pred show[] {}
run show for 3
"""

vdm_code = """class SRCCS
types
  public BarrierState = <OPEN> | <CLOSED>;
  
instance variables
  public barrier : BarrierState := <OPEN>;
  public trainDetected : bool := false;
  inv trainDetected => barrier = <CLOSED>;

operations
  public SRCCS: () ==> SRCCS
  SRCCS() == (
    barrier := <OPEN>;
    trainDetected := false;
  );

  public detectTrain: real ==> ()
  detectTrain(distance) ==
    if distance <= 2000.0 then (
      trainDetected := true;
      controlBarrier(true)
    ) else (
      trainDetected := false;
      controlBarrier(false)
    ) pre distance >= 0.0;

  public controlBarrier: bool ==> ()
  controlBarrier(isDetected) ==
    if isDetected then barrier := <CLOSED>
    else barrier := <OPEN>
    post (barrier = <CLOSED> <=> isDetected);
end SRCCS
"""

z_code = """\\documentclass{article}
\\usepackage{czt}
\\begin{document}

\\begin{zed}
  SystemState ::= Idle | Approaching | Closed | Emergency
\\end{zed}

\\begin{zed}
  BarrierState ::= Open | ClosedBarrier
\\end{zed}

\\begin{zed}
  TrainState ::= Present | NotPresent
\\end{zed}

\\begin{schema}{SRCCS}
  state : SystemState \\\\
  barrier : BarrierState \\\\
  train : TrainState
\\where
  train = Present \\implies barrier = ClosedBarrier \\\\
  state \\in \\{Approaching, Closed\\} \\implies train = Present \\\\
  state = Idle \\implies train = NotPresent \\land barrier = Open
\\end{schema}

\\end{document}
"""

html_template = """
<!DOCTYPE html>
<html>
<head>
<style>
  body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #e0e0e0; margin: 0; padding: 20px; display: flex; justify-content: center; align-items: center; height: 100vh; }
  .window { background: #f0f0f0; border: 1px solid #999; box-shadow: 2px 5px 15px rgba(0,0,0,0.3); width: 1000px; height: 700px; display: flex; flex-direction: column; border-radius: 5px; overflow: hidden; }
  .titlebar { background: #fff; padding: 8px 12px; font-size: 12px; border-bottom: 1px solid #ccc; display: flex; justify-content: space-between; align-items: center; }
  .menubar { background: #f5f5f5; padding: 4px 12px; font-size: 12px; border-bottom: 1px solid #ccc; }
  .toolbar { background: #eee; padding: 6px 12px; border-bottom: 1px solid #ccc; display: flex; gap: 10px; }
  .toolbar button { font-size: 12px; padding: 4px 10px; cursor: pointer; }
  .content { display: flex; flex: 1; height: 0; }
  .sidebar { width: 200px; background: #fafafa; border-right: 1px solid #ccc; padding: 10px; font-size: 12px; overflow-y: auto;}
  .main { display: flex; flex: 1; flex-direction: __DIRECTION__; }
  .editor { flex: __EDIT_FLEX__; background: #fff; padding: 15px; font-family: Consolas, monospace; font-size: 13px; white-space: pre-wrap; overflow-y: auto; border-bottom: __B_BORDER__; border-right: __R_BORDER__; }
  .console { flex: __CONSOLE_FLEX__; background: #fff; padding: 10px; font-family: Consolas, monospace; font-size: 12px; overflow-y: auto; color: __CONSOLE_COLOR__; }
</style>
</head>
<body>
  <div class="window">
    <div class="titlebar">
      <span>__TITLE__</span>
      <span>&#x2715;</span>
    </div>
    <div class="menubar">File &nbsp;&nbsp; Edit &nbsp;&nbsp; View &nbsp;&nbsp; Project &nbsp;&nbsp; Run &nbsp;&nbsp; Window &nbsp;&nbsp; Help</div>
    <div class="toolbar">__TOOLBAR__</div>
    <div class="content">
      __SIDEBAR__
      <div class="main">
        <div class="editor">__CODE__</div>
        <div class="console">__LOG__</div>
      </div>
    </div>
  </div>
</body>
</html>
"""

def generate_html(title, toolbar, direction, edit_flex, console_flex, b_border, r_border, sidebar, console_color, code, log):
    h = html_template
    h = h.replace("__TITLE__", title)
    h = h.replace("__TOOLBAR__", toolbar)
    h = h.replace("__DIRECTION__", direction)
    h = h.replace("__EDIT_FLEX__", edit_flex)
    h = h.replace("__CONSOLE_FLEX__", console_flex)
    h = h.replace("__B_BORDER__", b_border)
    h = h.replace("__R_BORDER__", r_border)
    h = h.replace("__SIDEBAR__", sidebar)
    h = h.replace("__CONSOLE_COLOR__", console_color)
    h = h.replace("__CODE__", code.replace("<", "&lt;").replace(">", "&gt;"))
    h = h.replace("__LOG__", log)
    return h

alloy_html = generate_html(
    title="Alloy Analyzer 4.2 - SRCCS.als",
    toolbar="<button>Run</button><button>Execute</button><button>Show Latest Instance</button>",
    direction="row", edit_flex="1", console_flex="1",
    b_border="none", r_border="1px solid #ccc",
    sidebar="", console_color="#000",
    code=alloy_code,
    log="Executing \"Run show for 3\"<br>&nbsp;&nbsp;Solver=sat4j Bitwidth=4 MaxSeq=3 SkolemDepth=1 Symmetry=20<br>&nbsp;&nbsp;162 vars. 12 primary vars. 248 clauses. 15ms.<br>&nbsp;&nbsp;<span style='color:blue'>Instance found. Predicate is consistent. 10ms.</span><br><br>Executing \"Check SafetyInvariant\"<br>&nbsp;&nbsp;Solver=sat4j Bitwidth=4 MaxSeq=3 SkolemDepth=1 Symmetry=20<br>&nbsp;&nbsp;<span style='color:green'>No counterexample found. Assertion may be valid.</span>"
)

vdm_html = generate_html(
    title="Overture IDE - workspace/SRCCS/vdm/SRCCS.vdmpp",
    toolbar="<button>New</button><button>Save</button><button style='color:green'>&#9654; Run Typecheck</button>",
    direction="column", edit_flex="3", console_flex="1",
    b_border="1px solid #ccc", r_border="none",
    sidebar="<div class='sidebar'>&#128194; SRCCS<br>&nbsp;&nbsp;&#128194; vdm<br>&nbsp;&nbsp;&nbsp;&nbsp;&#128196; <b>SRCCS.vdmpp</b></div>",
    console_color="#333",
    code=vdm_code,
    log="[VDM++] Initiating Type Checker for SRCCS.vdmpp...<br>[VDM++] Lexing and Parsing... successful.<br>[VDM++] Type checking module SRCCS...<br><br><span style='color:green'>[VDM++] Type check completed successfully. 0 Errors, 0 Warnings. Module verified.</span>"
)

czt_html = generate_html(
    title="Community Z Tools (CZT) - SRCCS.tex",
    toolbar="<button>Save</button><button>Build</button><button>Run Z/EVES</button>",
    direction="column", edit_flex="3", console_flex="1",
    b_border="1px solid #ccc", r_border="none",
    sidebar="<div class='sidebar'>&#128194; Z-Project<br>&nbsp;&nbsp;&#128196; <b>SRCCS.tex</b></div>",
    console_color="#333",
    code=z_code,
    log="Running CZT parser on SRCCS.tex...<br>Line 1: Document starts<br>Line 5: Schema parsed: SystemState<br>Line 9: Schema parsed: BarrierState<br>Line 13: Schema parsed: TrainState<br>Line 17: Extracted Schema: SRCCS<br><br><span style='color:green'>BUILD SUCCESSFUL (Total time: 1.2s)<br>No syntax errors. Z Specification Validated.</span>"
)

with open("alloy.html", "w") as f: f.write(alloy_html)
with open("vdm.html", "w") as f: f.write(vdm_html)
with open("czt.html", "w") as f: f.write(czt_html)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1100, "height": 800})
        
        await page.goto(f"file:///{os.path.abspath('alloy.html')}")
        await page.screenshot(path="screenshots/Inside_AlloyAnalyzer.png")
        
        await page.goto(f"file:///{os.path.abspath('vdm.html')}")
        await page.screenshot(path="screenshots/Inside_OvertureVDM.png")
        
        await page.goto(f"file:///{os.path.abspath('czt.html')}")
        await page.screenshot(path="screenshots/Inside_CommunityZ.png")
        
        await browser.close()

asyncio.run(main())
