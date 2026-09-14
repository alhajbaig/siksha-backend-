"""
SIKHSAATHI — Primary Curriculum & Resource Service
Extracts and structures authentic study material from the resources/ folder:
Physics, Chemistry, Mathematics, and Computer Science.
Provides Detailed Notes, Revision Sheets, Flashcards, Flowcharts, Mind Maps, and RAG Chunks.
"""

import os
import re
import html
import json
try:
    import pymupdf as fitz
except ImportError:
    try:
        import fitz  # PyMuPDF
    except ImportError:
        fitz = None
if fitz and not hasattr(fitz, "open"):
    try:
        import pymupdf as fitz
    except ImportError:
        fitz = None
from typing import Dict, List, Any, Optional

RESOURCES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "resources"))

class ResourceService:
    def __init__(self):
        self.chapters_db: Dict[str, Dict[str, Any]] = {}
        self.all_chunks: List[Dict[str, Any]] = []
        self._load_and_build_curriculum()

    def _load_and_build_curriculum(self):
        """Loads and structures all 8 resource chapters."""

        # -------------------------------------------------------------
        # 1. PHYSICS: Units and Dimensions
        # -------------------------------------------------------------
        self._add_units_and_dimensions()

        # -------------------------------------------------------------
        # 2. PHYSICS: Newton's Laws of Motion
        # -------------------------------------------------------------
        self._add_newtons_laws()

        # -------------------------------------------------------------
        # 2b. PHYSICS: Class 12 (NCERT Chapters 1 to 14)
        # -------------------------------------------------------------
        self._add_physics_curriculum()

        # -------------------------------------------------------------
        # 3. CHEMISTRY: Acids, Bases and Salts
        # -------------------------------------------------------------
        self._add_acids_bases_salts()

        # -------------------------------------------------------------
        # 3b. CHEMISTRY: Solutions (NCERT Class 12 Unit 1)
        # -------------------------------------------------------------
        self._add_chemistry_solutions()

        # -------------------------------------------------------------
        # 3c. BIOLOGY: Class 12 (NCERT Units VI - X, 13 Chapters)
        # -------------------------------------------------------------
        self._add_biology_curriculum()

        # -------------------------------------------------------------
        # 4. MATHEMATICS: Differentiation & Differential Calculus
        # -------------------------------------------------------------
        self._add_differentiation()

        # -------------------------------------------------------------
        # 4b. MATHEMATICS: Class 12 (NCERT Chapters 1 to 13)
        # -------------------------------------------------------------
        self._add_maths_curriculum()

        # -------------------------------------------------------------
        # 5. COMPUTER SCIENCE: Database Management Systems (DBMS)
        # -------------------------------------------------------------
        self._add_dbms()

        # -------------------------------------------------------------
        # 6. COMPUTER SCIENCE: SQL & Relational Queries
        # -------------------------------------------------------------
        self._add_sql()

        # -------------------------------------------------------------
        # 7. COMPUTER SCIENCE: Computer Networks (CN)
        # -------------------------------------------------------------
        self._add_computer_networks()

        # -------------------------------------------------------------
        # 8. COMPUTER SCIENCE: Operating Systems (OS)
        # -------------------------------------------------------------
        self._add_operating_systems()

    def _extract_pdf_pages(self, filename: str) -> List[Dict[str, Any]]:
        fpath = os.path.join(RESOURCES_DIR, filename)
        pages = []
        if os.path.exists(fpath) and fitz is not None:
            try:
                doc = fitz.open(fpath)
                for idx, page in enumerate(doc):
                    txt = page.get_text().strip()
                    pages.append({"page_num": idx + 1, "text": txt})
                doc.close()
            except Exception as e:
                print(f"Error reading {filename}: {e}")
        return pages

    def _add_units_and_dimensions(self):
        cid = "phys-units-dimensions"
        source_file = "Units_and_Dimensions_in_Physics_Detailed_Notes.pdf"
        pages = self._extract_pdf_pages(source_file)

        detailed_html = r"""
<div id="sec-1" class="study-section">
  <h3>1. Physical Quantities & Measurement</h3>
  <p>A <strong>physical quantity</strong> is any characteristic of a physical body or phenomenon that can be quantified and measured using standard physical instruments (e.g., mass, length, time, velocity, force).</p>
  <div class="formula-block">
    <strong>Fundamental Relation:</strong> $Q = n \cdot u$<br>
    where $Q$ is the physical quantity, $n$ is the numerical value, and $u$ is the unit of measurement. $n_1 u_1 = n_2 u_2 = \text{constant}$.
  </div>
</div>

<div id="sec-2" class="study-section">
  <h3>2. Fundamental & Derived Quantities (SI System)</h3>
  <p>The International System of Units (SI) defines <strong>7 fundamental base quantities</strong> and 2 supplementary quantities:</p>
  <ul>
    <li><strong>Length:</strong> Meter ($m$) — $[L]$</li>
    <li><strong>Mass:</strong> Kilogram ($kg$) — $[M]$</li>
    <li><strong>Time:</strong> Second ($s$) — $[T]$</li>
    <li><strong>Electric Current:</strong> Ampere ($A$) — $[I]$ or $[A]$</li>
    <li><strong>Thermodynamic Temperature:</strong> Kelvin ($K$) — $[\Theta]$ or $[K]$</li>
    <li><strong>Amount of Substance:</strong> Mole ($mol$) — $[N]$</li>
    <li><strong>Luminous Intensity:</strong> Candela ($cd$) — $[J]$</li>
  </ul>
  <p><strong>Supplementary Quantities:</strong> Plane Angle (Radian, $rad$) and Solid Angle (Steradian, $sr$) are dimensionless.</p>
</div>

<div id="sec-3" class="study-section">
  <h3>3. Dimensional Formulae of Key Mechanics Quantities</h3>
  <p>Dimensional formula expresses a physical quantity in terms of fundamental dimensions $[M^a L^b T^c I^d \Theta^e N^f J^g]$.</p>
  <div class="formula-block">
    <strong>Velocity:</strong> $v = \frac{dx}{dt} \implies [M^0 L T^{-1}]$<br>
    <strong>Acceleration:</strong> $a = \frac{dv}{dt} \implies [M^0 L T^{-2}]$<br>
    <strong>Force:</strong> $F = m \cdot a \implies [M L T^{-2}]$<br>
    <strong>Work & Energy:</strong> $W = F \cdot d \implies [M L^2 T^{-2}]$<br>
    <strong>Power:</strong> $P = \frac{dW}{dt} \implies [M L^2 T^{-3}]$<br>
    <strong>Pressure / Stress:</strong> $P = \frac{F}{A} \implies [M L^{-1} T^{-2}]$<br>
    <strong>Universal Gravitational Constant ($G$):</strong> $F = \frac{G m_1 m_2}{r^2} \implies [G] = [M^{-1} L^3 T^{-2}]$<br>
    <strong>Planck's Constant ($h$):</strong> $E = h\nu \implies [h] = [M L^2 T^{-1}]$
  </div>
</div>

<div id="sec-4" class="study-section">
  <h3>4. Principle of Homogeneity & Dimensional Analysis</h3>
  <p>The <strong>Principle of Homogeneity</strong> states that in any physically valid equation, the dimensions of every additive or subtractive term on both sides must be identical.</p>
  <p>If $A + B = C$, then $[A] = [B] = [C]$. Transcendental functions ($\sin, \cos, \ln, e^x$) and their arguments must be strictly dimensionless.</p>
  <div class="exam-trap-box">
    <strong>⚠️ Common Exam Trap:</strong> A dimensionally correct equation may not be physically correct (e.g. missing dimensionless constant $1/2$ in $s = ut + at^2$). However, a dimensionally incorrect equation is ALWAYS physically incorrect!
  </div>
</div>
"""
        toc = [
            {"id": "sec-1", "title": "1. Physical Quantities & Measurement"},
            {"id": "sec-2", "title": "2. Fundamental & Derived Quantities (SI System)"},
            {"id": "sec-3", "title": "3. Dimensional Formulae of Key Quantities"},
            {"id": "sec-4", "title": "4. Principle of Homogeneity & Limitations"}
        ]

        revision_html = r"""
<div class="revision-sheet">
  <div class="rev-card">
    <h4>ONE-LINE IDEA</h4>
    <p>Units provide measurement standards, while dimensions characterize the fundamental physical nature of quantities independently of unit magnitude.</p>
  </div>
  <div class="rev-card">
    <h4>MUST REMEMBER</h4>
    <ul>
      <li>7 SI Base units: $kg, m, s, A, K, mol, cd$.</li>
      <li>Plane angle ($rad$) and solid angle ($sr$) have units but are strictly DIMENSIONLESS.</li>
      <li>Argument of trigonometric, logarithmic, and exponential functions must be dimensionless ($[\theta] = [M^0 L^0 T^0]$).</li>
    </ul>
  </div>
  <div class="rev-card">
    <h4>CORE FORMULAS</h4>
    <ul>
      <li>$[G] = [M^{-1} L^3 T^{-2}]$ (Gravitational constant)</li>
      <li>$[h] = [M L^2 T^{-1}]$ (Planck's constant)</li>
      <li>$[W] = [E] = [\tau] = [M L^2 T^{-2}]$ (Work, Energy, Torque have identical dimensions)</li>
      <li>$[\eta] = [M L^{-1} T^{-1}]$ (Coefficient of viscosity)</li>
    </ul>
  </div>
  <div class="rev-card">
    <h4>EXAM TRAPS</h4>
    <p>• Quantities can be dimensionless yet have units (Angle in radians).<br>• Dimensionless physical constants ($G, h, k_B$) have units and dimensions, while numerical constants ($\pi, 2$) have neither.</p>
  </div>
</div>
"""

        flashcards = [
            {"q": "What is the Principle of Homogeneity of dimensions?", "a": "Every additive or subtractive term on both sides of a physically valid equation must have identical dimensions."},
            {"q": "What is the dimensional formula for the Universal Gravitational Constant (G)?", "a": "[M⁻¹ L³ T⁻²], derived from F = G(m₁m₂)/r²."},
            {"q": "Can a quantity have units but no dimensions? Give an example.", "a": "Yes! Plane angle (Radian) and Solid angle (Steradian) have units but are dimensionless [M⁰ L⁰ T⁰]."},
            {"q": "What is the dimensional formula of Planck's Constant (h)?", "a": "[M L² T⁻¹], derived from E = h·ν."},
            {"q": "Name three quantities with the dimensional formula [M L² T⁻²].", "a": "Work, Kinetic Energy, Potential Energy, Torque, and Heat Energy."},
            {"q": "What are the limitations of dimensional analysis?", "a": "1. Cannot determine dimensionless constants (like 1/2, π). 2. Fails for equations with trigonometric/exponential functions. 3. Cannot determine whether a quantity is scalar or vector."}
        ]

        flow_data = {
            "title": "Dimensional Analysis & Formula Derivation Workflow",
            "steps": [
                {"step": "1. Identify Variables", "desc": "Express target quantity $Q$ as power product of governing factors $A^x B^y C^z$"},
                {"step": "2. Write Dimensions", "desc": "Substitute $[M, L, T]$ dimensional formula for each variable on LHS and RHS"},
                {"step": "3. Equate Exponents", "desc": "Form linear system by equating powers of $M$, $L$, and $T$ separately"},
                {"step": "4. Solve System", "desc": "Solve for exponents $x, y, z$ to obtain dimensionless proportionality constant $k$"}
            ]
        }

        mindmap_data = {
            "name": "Units & Dimensions",
            "children": [
                {"name": "SI Base System", "children": [{"name": "7 Base Units (kg, m, s, A, K, mol, cd)"}, {"name": "2 Supplementary (rad, sr)"}]},
                {"name": "Dimensional Formulas", "children": [{"name": "Mechanics: [M, L, T]"}, {"name": "Constants: G, h, k_B"}, {"name": "Viscosity & Surface Tension"}]},
                {"name": "Applications", "children": [{"name": "Check Equation Validity"}, {"name": "Unit Conversion (n₁u₁ = n₂u₂)"}, {"name": "Derive Relationships"}]},
                {"name": "Limitations", "children": [{"name": "Cannot find constants (π, 1/2)"}, {"name": "Max 3 variables for [M,L,T]"}, {"name": "No scalar/vector distinction"}]}
            ]
        }

        self._store_chapter(
            cid=cid,
            subject="phys",
            subject_title="Physics",
            title="Units and Dimensions",
            source_file=source_file,
            reading_time_min=8,
            detailed_html=detailed_html,
            toc=toc,
            revision_html=revision_html,
            flashcards=flashcards,
            flow_data=flow_data,
            mindmap_data=mindmap_data,
            has_handwritten=True,
            pages=pages
        )

    def _add_newtons_laws(self):
        cid = "phys-newtons-laws"
        source_file = "Newtons_Laws_of_Motion_Detailed_Notes.pdf"
        pages = self._extract_pdf_pages(source_file)

        detailed_html = r"""
<div id="sec-1" class="study-section">
  <h3>1. Newton's First Law & Inertia</h3>
  <p><strong>First Law (Law of Inertia):</strong> An object continues in its state of rest or uniform motion in a straight line unless acted upon by a non-zero net external force.</p>
  <p><strong>Inertia</strong> is the inherent property of a body to resist change in its state of motion. Quantitative measure of inertia is <em>mass</em>.</p>
  <ul>
    <li><strong>Inertia of Rest:</strong> Tendency to stay stationary (e.g. passengers jerk backwards when a bus accelerates).</li>
    <li><strong>Inertia of Motion:</strong> Tendency to stay in motion (e.g. passengers lurch forward on sudden braking).</li>
    <li><strong>Inertia of Direction:</strong> Tendency to maintain linear path (e.g. sparks flying tangentially from a grinder).</li>
  </ul>
</div>

<div id="sec-2" class="study-section">
  <h3>2. Newton's Second Law & Momentum</h3>
  <p><strong>Linear Momentum ($\vec{p}$):</strong> Measure of quantity of motion, $\vec{p} = m \cdot \vec{v}$.</p>
  <div class="formula-block">
    <strong>Second Law of Motion:</strong> $\vec{F}_{\text{net}} = \frac{d\vec{p}}{dt} = m \frac{d\vec{v}}{dt} + \vec{v}\frac{dm}{dt}$<br>
    For constant mass: $\vec{F}_{\text{net}} = m \cdot \vec{a}$<br>
    <strong>Impulse ($\vec{J}$):</strong> $\vec{J} = \int \vec{F} dt = \Delta \vec{p} = m\vec{v}_f - m\vec{v}_i$
  </div>
</div>

<div id="sec-3" class="study-section">
  <h3>3. Newton's Third Law & Action-Reaction Pairs</h3>
  <p><strong>Third Law:</strong> To every action, there is an equal and opposite reaction ($\vec{F}_{AB} = -\vec{F}_{BA}$).</p>
  <p><strong>Critical Rules:</strong> Action and reaction forces act on <em>different bodies</em> simultaneously; therefore, they <strong>never cancel each other</strong>.</p>
</div>

<div id="sec-4" class="study-section">
  <h3>4. Free Body Diagrams (FBD) & Friction</h3>
  <p>A <strong>Free Body Diagram (FBD)</strong> isolates a system and represents all external forces acting directly ON it.</p>
  <div class="formula-block">
    <strong>Static Friction:</strong> $f_s \le \mu_s N$ &nbsp;(Self-adjusting up to limiting friction $f_{s,\max} = \mu_s N$)<br>
    <strong>Kinetic Friction:</strong> $f_k = \mu_k N$ &nbsp;($\mu_k < \mu_s$, constant during relative motion)<br>
    <strong>Apparent Weight in Elevator:</strong> Accelerating up: $N = m(g + a)$, Accelerating down: $N = m(g - a)$, Free fall ($a=g$): $N = 0$.
  </div>
</div>
"""
        toc = [
            {"id": "sec-1", "title": "1. Newton's First Law & Inertia"},
            {"id": "sec-2", "title": "2. Newton's Second Law & Momentum"},
            {"id": "sec-3", "title": "3. Newton's Third Law & Pairs"},
            {"id": "sec-4", "title": "4. Free Body Diagrams & Friction"}
        ]

        revision_html = r"""
<div class="revision-sheet">
  <div class="rev-card">
    <h4>ONE-LINE IDEA</h4>
    <p>Forces cause changes in momentum; internal forces always cancel in pairs while net external force dictates acceleration.</p>
  </div>
  <div class="rev-card">
    <h4>MUST REMEMBER</h4>
    <ul>
      <li>Newton's 2nd law in true differential form is $\vec{F} = d\vec{p}/dt$, not just $m\vec{a}$ (rocket propulsion has variable mass).</li>
      <li>Action-reaction pairs act on different objects and never produce equilibrium on a single object.</li>
      <li>Static friction is self-adjusting ($0 \le f_s \le \mu_s N$).</li>
    </ul>
  </div>
  <div class="rev-card">
    <h4>KEY EQUATIONS</h4>
    <ul>
      <li>$\vec{F}_{\text{net}} = m\vec{a}$</li>
      <li>$\vec{J} = \Delta \vec{p} = \vec{F}_{\text{avg}} \Delta t$</li>
      <li>$f_{s,\max} = \mu_s N, \quad f_k = \mu_k N$</li>
      <li>Elevator: $N = m(g \pm a)$</li>
    </ul>
  </div>
</div>
"""

        flashcards = [
            {"q": "State Newton's Second Law of Motion in fundamental differential form.", "a": "F_net = dp/dt. The rate of change of linear momentum is directly proportional to net applied force."},
            {"q": "Why do action and reaction forces not cancel each other out?", "a": "Because action and reaction act on two completely different bodies, not on the same body."},
            {"q": "What is Impulse and how is it related to momentum?", "a": "Impulse J = ∫ F dt = Δp (change in linear momentum). It is represented by the area under a Force-Time graph."},
            {"q": "What is the apparent weight of a person in an elevator accelerating downwards with acceleration 'a'?", "a": "N = m(g - a). In free fall (a = g), apparent weight N = 0 (weightlessness)."},
            {"q": "Why is the coefficient of kinetic friction (μk) less than static friction (μs)?", "a": "Once motion starts, microscopic surface irregularities do not have sufficient time to interlock as deeply as when stationary."}
        ]

        flow_data = {
            "title": "Newton's 2nd Law Mechanics Problem-Solving Workflow",
            "steps": [
                {"step": "1. Isolate System", "desc": "Identify each mass in the system separately"},
                {"step": "2. Draw FBD", "desc": "Draw all external forces: Gravity ($mg$), Normal ($N$), Tension ($T$), Friction ($f$)"},
                {"step": "3. Choose Coordinate Axes", "desc": "Align one axis along expected acceleration direction and resolve components"},
                {"step": "4. Apply Equations", "desc": "Write $\Sigma F_x = m a_x$ and $\Sigma F_y = 0$, then solve system simultaneously"}
            ]
        }

        mindmap_data = {
            "name": "Newton's Laws of Motion",
            "children": [
                {"name": "1st Law (Inertia)", "children": [{"name": "Inertia of Rest"}, {"name": "Inertia of Motion"}, {"name": "Inertia of Direction"}]},
                {"name": "2nd Law (Dynamics)", "children": [{"name": "F = dp/dt = ma"}, {"name": "Impulse (J = Δp)"}, {"name": "Conservation of Momentum"}]},
                {"name": "3rd Law (Interactions)", "children": [{"name": "Action-Reaction Pairs"}, {"name": "Different Bodies"}, {"name": "Simultaneous Occurrence"}]},
                {"name": "Friction & Applications", "children": [{"name": "Static (0 ≤ fs ≤ μsN)"}, {"name": "Kinetic (fk = μkN)"}, {"name": "Pulleys & Elevators"}]}
            ]
        }

        self._store_chapter(
            cid=cid,
            subject="phys",
            subject_title="Physics",
            title="Newton’s Laws of Motion",
            source_file=source_file,
            reading_time_min=10,
            detailed_html=detailed_html,
            toc=toc,
            revision_html=revision_html,
            flashcards=flashcards,
            flow_data=flow_data,
            mindmap_data=mindmap_data,
            has_handwritten=True,
            pages=pages
        )

    def _add_acids_bases_salts(self):
        cid = "chem-acids-bases-salts"
        source_file = "Acids_Bases_and_Salts_Detailed_Notes.pdf"
        pages = self._extract_pdf_pages(source_file)

        detailed_html = r"""
<div id="sec-1" class="study-section">
  <h3>1. Theories of Acids and Bases</h3>
  <p>Three classical theories define acidic and basic character in chemistry:</p>
  <ul>
    <li><strong>Arrhenius Theory:</strong> Acids release $H^+$ (or $H_3O^+$) ions in aqueous solution ($HCl \rightarrow H^+ + Cl^-$). Bases release $OH^-$ ions ($NaOH \rightarrow Na^+ + OH^-$).</li>
    <li><strong>Brønsted–Lowry Theory:</strong> Acid is a <strong>proton ($H^+$) donor</strong>; Base is a <strong>proton ($H^+$) acceptor</strong>. Every acid has a conjugate base, and every base has a conjugate acid ($NH_3 + H_2O \rightleftharpoons NH_4^+ + OH^-$).</li>
    <li><strong>Lewis Theory:</strong> Acid is an <strong>electron-pair acceptor</strong> (electrophile, e.g., $BF_3, AlCl_3$); Base is an <strong>electron-pair donor</strong> (nucleophile, e.g., $:NH_3, H_2\ddot{O}$).</li>
  </ul>
</div>

<div id="sec-2" class="study-section">
  <h3>2. Strength, pH & Ionic Product of Water</h3>
  <p>The autoionization of pure water: $2H_2O \rightleftharpoons H_3O^+ + OH^-$ with equilibrium constant $K_w = [H^+][OH^-] = 1.0 \times 10^{-14} \text{ at } 25^\circ\text{C}$.</p>
  <div class="formula-block">
    <strong>pH Definition:</strong> $pH = -\log_{10}[H^+], \quad pOH = -\log_{10}[OH^-]$<br>
    <strong>Fundamental Relation:</strong> $pH + pOH = 14 \text{ (at } 25^\circ\text{C})$<br>
    • Acidic: $pH < 7 \iff [H^+] > 10^{-7}\text{ M}$<br>
    • Neutral: $pH = 7 \iff [H^+] = 10^{-7}\text{ M}$<br>
    • Basic / Alkaline: $pH > 7 \iff [H^+] < 10^{-7}\text{ M}$
  </div>
</div>

<div id="sec-3" class="study-section">
  <h3>3. Indicators & Color Transitions</h3>
  <table style="width: 100%; border-collapse: collapse; margin: 0.8rem 0; font-size: 0.85rem;">
    <thead>
      <tr style="border-bottom: 2px solid var(--border-card); text-align: left;">
        <th style="padding: 6px;">Indicator</th>
        <th style="padding: 6px;">Acidic Medium</th>
        <th style="padding: 6px;">Neutral</th>
        <th style="padding: 6px;">Basic Medium</th>
      </tr>
    </thead>
    <tbody>
      <tr style="border-bottom: 1px solid var(--border-subtle);"><td style="padding: 6px;">Litmus Paper</td><td style="padding: 6px; color: #EF4444;">Red</td><td style="padding: 6px;">Purple</td><td style="padding: 6px; color: #3B82F6;">Blue</td></tr>
      <tr style="border-bottom: 1px solid var(--border-subtle);"><td style="padding: 6px;">Phenolphthalein</td><td style="padding: 6px;">Colorless</td><td style="padding: 6px;">Colorless</td><td style="padding: 6px; color: #EC4899;">Pink / Magenta</td></tr>
      <tr><td style="padding: 6px;">Methyl Orange</td><td style="padding: 6px; color: #EF4444;">Red</td><td style="padding: 6px; color: #F59E0B;">Orange</td><td style="padding: 6px; color: #EAB308;">Yellow</td></tr>
    </tbody>
  </table>
</div>

<div id="sec-4" class="study-section">
  <h3>4. Important Industrial Salts & Reactions</h3>
  <ul>
    <li><strong>Baking Soda (Sodium Hydrogen Carbonate, $NaHCO_3$):</strong> Prepared by Solvay process. Mild non-corrosive base used in antacids and fire extinguishers. $2NaHCO_3 \xrightarrow{\Delta} Na_2CO_3 + H_2O + CO_2\uparrow$.</li>
    <li><strong>Washing Soda (Sodium Carbonate Decahydrate, $Na_2CO_3 \cdot 10H_2O$):</strong> Recrystallization of sodium carbonate. Used for removing permanent hardness of water.</li>
    <li><strong>Bleaching Powder (Calcium Oxychloride, $CaOCl_2$):</strong> Action of chlorine on dry slaked lime: $Ca(OH)_2 + Cl_2 \rightarrow CaOCl_2 + H_2O$.</li>
    <li><strong>Plaster of Paris ($CaSO_4 \cdot \frac{1}{2}H_2O$):</strong> Heating gypsum ($CaSO_4 \cdot 2H_2O$) at $373\text{ K}$. On mixing with water, it re-solidifies into hard gypsum.</li>
  </ul>
</div>
"""
        toc = [
            {"id": "sec-1", "title": "1. Theories of Acids and Bases"},
            {"id": "sec-2", "title": "2. Strength, pH & Ionic Product (Kw)"},
            {"id": "sec-3", "title": "3. Indicators & Color Transitions"},
            {"id": "sec-4", "title": "4. Important Industrial Salts & Formulas"}
        ]

        revision_html = r"""
<div class="revision-sheet">
  <div class="rev-card">
    <h4>ONE-LINE IDEA</h4>
    <p>Acids and bases are defined by proton transfer (Brønsted) or electron pair donation (Lewis), neutralizing to yield ionic salts and water.</p>
  </div>
  <div class="rev-card">
    <h4>MUST REMEMBER FORMULAS</h4>
    <ul>
      <li>$pH = -\log[H^+]$, $pOH = -\log[OH^-]$</li>
      <li>$pH + pOH = 14$ at $25^\circ\text{C}$</li>
      <li>Plaster of Paris: $CaSO_4 \cdot \frac{1}{2}H_2O$</li>
      <li>Gypsum: $CaSO_4 \cdot 2H_2O$</li>
      <li>Bleaching Powder: $CaOCl_2$</li>
      <li>Baking Soda: $NaHCO_3$, Washing Soda: $Na_2CO_3 \cdot 10H_2O$</li>
    </ul>
  </div>
  <div class="rev-card">
    <h4>EXAM TRAPS</h4>
    <p>• Acid + Metal $\rightarrow$ Salt + $H_2\uparrow$ (except with concentrated $HNO_3$ which oxidizes $H_2$ to $H_2O$).<br>• Diluting acid: Always add ACID TO WATER slowly with stirring, NEVER water to concentrated acid!</p>
  </div>
</div>
"""

        flashcards = [
            {"q": "What is the difference between Arrhenius, Brønsted-Lowry, and Lewis acid definitions?", "a": "Arrhenius: releases H⁺ in water. Brønsted-Lowry: H⁺ (proton) donor. Lewis: Electron-pair acceptor."},
            {"q": "What is the chemical formula of Plaster of Paris and how is it prepared?", "a": "CaSO₄·½H₂O. Prepared by heating Gypsum (CaSO₄·2H₂O) at 373 K (100°C)."},
            {"q": "Why is water never added directly to concentrated sulfuric acid?", "a": "Dissolution is highly exothermic; adding water generates localized boiling that splatters concentrated acid violently."},
            {"q": "What color does Phenolphthalein turn in basic medium?", "a": "Pink / Magenta. It remains colorless in acidic and neutral media."},
            {"q": "What is a conjugate acid-base pair?", "a": "Two species that differ by exactly one proton (H⁺), such as NH₄⁺ (acid) and NH₃ (base)."}
        ]

        flow_data = {
            "title": "Acid-Base Classification & Neutralization Mechanism",
            "steps": [
                {"step": "1. Proton / Electron Evaluation", "desc": "Classify compound: Proton donor (Acid) vs Proton/Electron donor (Base)"},
                {"step": "2. Dissociation in Water", "desc": "Strong electrolytes ionize 100% ($\alpha = 1$); Weak electrolytes establish $K_a / K_b$ equilibrium"},
                {"step": "3. Neutralization Reaction", "desc": "Reaction: $H^+_{(aq)} + OH^-_{(aq)} \rightarrow H_2O_{(l)}$ ($\Delta H = -57.1\text{ kJ/mol}$)"},
                {"step": "4. Salt Hydrolysis", "desc": "Strong Acid + Weak Base $\rightarrow$ Acidic salt ($pH < 7$); Weak Acid + Strong Base $\rightarrow$ Basic salt ($pH > 7$)"}
            ]
        }

        mindmap_data = {
            "name": "Acids, Bases & Salts",
            "children": [
                {"name": "Theories", "children": [{"name": "Arrhenius (H+/OH- in H2O)"}, {"name": "Brønsted-Lowry (Proton Donor/Acceptor)"}, {"name": "Lewis (Electron Pair Acceptor/Donor)"}]},
                {"name": "pH & Equilibria", "children": [{"name": "pH = -log[H+]"}, {"name": "Kw = [H+][OH-] = 10^-14"}, {"name": "Buffer Solutions"}]},
                {"name": "Indicators", "children": [{"name": "Litmus (Red/Blue)"}, {"name": "Phenolphthalein (Colorless/Pink)"}, {"name": "Methyl Orange (Red/Yellow)"}]},
                {"name": "Important Salts", "children": [{"name": "Baking Soda (NaHCO3)"}, {"name": "Washing Soda (Na2CO3·10H2O)"}, {"name": "Plaster of Paris (CaSO4·½H2O)"}, {"name": "Bleaching Powder (CaOCl2)"}]}
            ]
        }

        self._store_chapter(
            cid=cid,
            subject="chem",
            subject_title="Chemistry",
            title="Acids, Bases and Salts",
            source_file=source_file,
            reading_time_min=12,
            detailed_html=detailed_html,
            toc=toc,
            revision_html=revision_html,
            flashcards=flashcards,
            flow_data=flow_data,
            mindmap_data=mindmap_data,
            has_handwritten=True,
            pages=pages
        )

    def _add_chemistry_solutions(self):
        from backend.data.curriculum.chemistry_solutions import get_all_solutions_topics
        for data in get_all_solutions_topics():
            self._store_chapter(
                cid=data["id"],
                subject=data["subject"],
                subject_title=data["subject_title"],
                title=data["title"],
                source_file=data["source_file"],
                reading_time_min=data["reading_time_min"],
                detailed_html=data["detailed_html"],
                toc=data["toc"],
                revision_html=data["revision_html"],
                flashcards=data["flashcards"],
                flow_data=data["flow_data"],
                mindmap_data=data["mindmap_data"],
                has_handwritten=data["has_handwritten"],
                pages=data["pages"]
            )

    def _add_biology_curriculum(self):
        from backend.data.curriculum.biology_class12 import get_all_biology_topics
        for data in get_all_biology_topics():
            self._store_chapter(
                cid=data["id"],
                subject=data["subject"],
                subject_title=data["subject_title"],
                title=data["title"],
                source_file=data.get("source_file", "Class_12_Biology_NCERT.pdf"),
                reading_time_min=data.get("reading_time_min", 14),
                detailed_html=data["detailed_html"],
                toc=data.get("toc", [{"id": "sec-01", "title": data["title"]}]),
                revision_html=data["revision_html"],
                flashcards=data["flashcards"],
                flow_data=data["flow_data"],
                mindmap_data=data["mindmap_data"],
                has_handwritten=data.get("has_handwritten", False),
                pages=data.get("pages", [])
            )

    def _add_physics_curriculum(self):
        from backend.data.curriculum.physics_class12 import get_all_physics_topics
        for data in get_all_physics_topics():
            self._store_chapter(
                cid=data["id"],
                subject=data["subject"],
                subject_title=data["subject_title"],
                title=data["title"],
                source_file=data.get("source_file", "Physics_NCERT.pdf"),
                reading_time_min=data.get("reading_time_min", 15),
                detailed_html=data["detailed_html"],
                toc=data.get("toc", []),
                revision_html=data["revision_html"],
                flashcards=data["flashcards"],
                flow_data=data["flow_data"],
                mindmap_data=data["mindmap_data"],
                has_handwritten=data.get("has_handwritten", True),
                pages=data.get("pages", [])
            )

    def _add_maths_curriculum(self):
        from backend.data.curriculum.maths_class12 import get_all_maths_topics
        for data in get_all_maths_topics():
            self._store_chapter(
                cid=data["id"],
                subject=data["subject"],
                subject_title=data["subject_title"],
                title=data["title"],
                source_file=data.get("source_file", "Maths_NCERT.pdf"),
                reading_time_min=data.get("reading_time_min", 16),
                detailed_html=data["detailed_html"],
                toc=data.get("toc", []),
                revision_html=data["revision_html"],
                flashcards=data["flashcards"],
                flow_data=data["flow_data"],
                mindmap_data=data["mindmap_data"],
                has_handwritten=data.get("has_handwritten", True),
                pages=data.get("pages", [])
            )

    def _add_differentiation(self):
        cid = "math-differentiation"
        source_file = "Differentiation_Detailed_Notes.pdf"
        pages = self._extract_pdf_pages(source_file)

        detailed_html = r"""
<div id="sec-1" class="study-section">
  <h3>1. Definition & First Principles</h3>
  <p>The <strong>derivative</strong> represents the instantaneous rate of change of a function $f(x)$ with respect to $x$, geometrically representing the slope of the tangent line at $(x, f(x))$.</p>
  <div class="formula-block">
    <strong>First Principle of Differentiation:</strong><br>
    $f'(x) = \frac{dy}{dx} = \lim_{h \to 0} \frac{f(x + h) - f(x)}{h}$
  </div>
</div>

<div id="sec-2" class="study-section">
  <h3>2. Fundamental Differentiation Rules</h3>
  <div class="formula-block">
    <strong>Power Rule:</strong> $\frac{d}{dx}[x^n] = n x^{n-1}$<br>
    <strong>Constant Multiple:</strong> $\frac{d}{dx}[c f(x)] = c f'(x)$<br>
    <strong>Sum & Difference:</strong> $\frac{d}{dx}[f(x) \pm g(x)] = f'(x) \pm g'(x)$<br>
    <strong>Product Rule (Leibniz):</strong> $\frac{d}{dx}[u \cdot v] = u \frac{dv}{dx} + v \frac{du}{dx}$<br>
    <strong>Quotient Rule:</strong> $\frac{d}{dx}\left[\frac{u}{v}\right] = \frac{v \frac{du}{dx} - u \frac{dv}{dx}}{v^2}$<br>
    <strong>Chain Rule (Composite):</strong> $\frac{d}{dx}[f(g(x))] = f'(g(x)) \cdot g'(x)$
  </div>
</div>

<div id="sec-3" class="study-section">
  <h3>3. Derivatives of Standard Functions</h3>
  <div class="formula-block">
    <strong>Trigonometric:</strong><br>
    $\frac{d}{dx}[\sin x] = \cos x, \quad \frac{d}{dx}[\cos x] = -\sin x, \quad \frac{d}{dx}[\tan x] = \sec^2 x$<br>
    $\frac{d}{dx}[\sec x] = \sec x \tan x, \quad \frac{d}{dx}[\csc x] = -\csc x \cot x, \quad \frac{d}{dx}[\cot x] = -\csc^2 x$<br><br>
    <strong>Exponential & Logarithmic:</strong><br>
    $\frac{d}{dx}[e^x] = e^x, \quad \frac{d}{dx}[a^x] = a^x \ln a, \quad \frac{d}{dx}[\ln x] = \frac{1}{x} \quad (x > 0)$<br><br>
    <strong>Inverse Trigonometric:</strong><br>
    $\frac{d}{dx}[\arcsin x] = \frac{1}{\sqrt{1 - x^2}}, \quad \frac{d}{dx}[\arccos x] = -\frac{1}{\sqrt{1 - x^2}}, \quad \frac{d}{dx}[\arctan x] = \frac{1}{1 + x^2}$
  </div>
</div>

<div id="sec-4" class="study-section">
  <h3>4. Advanced Techniques: Implicit & Logarithmic Differentiation</h3>
  <p><strong>Implicit Differentiation:</strong> Differentiate both sides with respect to $x$, applying the chain rule to terms with $y$ (e.g., $\frac{d}{dx}[y^2] = 2y \frac{dy}{dx}$), then collect $\frac{dy}{dx}$ terms.</p>
  <p><strong>Logarithmic Differentiation:</strong> For functions of the form $y = [f(x)]^{g(x)}$, take natural logarithm on both sides ($\ln y = g(x) \ln f(x)$) before differentiating.</p>
</div>
"""
        toc = [
            {"id": "sec-1", "title": "1. Definition & First Principles"},
            {"id": "sec-2", "title": "2. Fundamental Rules (Product, Quotient, Chain)"},
            {"id": "sec-3", "title": "3. Derivatives of Standard & Inverse Trig Functions"},
            {"id": "sec-4", "title": "4. Implicit & Logarithmic Differentiation"}
        ]

        revision_html = r"""
<div class="revision-sheet">
  <div class="rev-card">
    <h4>ONE-LINE IDEA</h4>
    <p>Differentiation measures instantaneous rate of change and geometric tangent slope using algebraic power, product, quotient, and chain rules.</p>
  </div>
  <div class="rev-card">
    <h4>MUST REMEMBER RULES</h4>
    <ul>
      <li>Product: $(uv)' = u'v + uv'$</li>
      <li>Quotient: $(u/v)' = \frac{u'v - uv'}{v^2}$ (Low d-High minus High d-Low over Low-squared)</li>
      <li>Chain: $\frac{dy}{dx} = \frac{dy}{du} \cdot \frac{du}{dx}$</li>
      <li>All trigonometric functions starting with 'co' ($\cos, \cot, \csc$) have a NEGATIVE derivative!</li>
    </ul>
  </div>
  <div class="rev-card">
    <h4>EXAM TRAPS</h4>
    <p>• Forgetting the chain rule multiplier: $\frac{d}{dx}[(3x+2)^5] = 5(3x+2)^4 \cdot 3 = 15(3x+2)^4$, not just $5(3x+2)^4$.<br>• Using $(uv)' = u'v'$ is invalid!</p>
  </div>
</div>
"""

        flashcards = [
            {"q": "State the definition of derivative using first principles.", "a": "f'(x) = lim(h->0) [f(x+h) - f(x)] / h."},
            {"q": "What is the derivative of a^x with respect to x?", "a": "d/dx [a^x] = a^x · ln(a)."},
            {"q": "What is the derivative of arctan(x)?", "a": "d/dx [arctan(x)] = 1 / (1 + x²)."},
            {"q": "What rule is used to differentiate y = x^x?", "a": "Logarithmic differentiation: ln(y) = x·ln(x) => (1/y)·y' = ln(x) + 1 => y' = x^x(ln x + 1)."},
            {"q": "What is the Quotient Rule formula?", "a": "d/dx [u/v] = (v·u' - u·v') / v²."}
        ]

        flow_data = {
            "title": "Chain Rule Differentiation Workflow",
            "steps": [
                {"step": "1. Identify Layers", "desc": "Decompose function $y = f(g(h(x)))$ into outer and inner components"},
                {"step": "2. Differentiate Outer Layer", "desc": "Compute derivative of outer function $f'$ evaluated at internal argument $g(h(x))$"},
                {"step": "3. Multiply Inner Derivatives", "desc": "Multiply step-by-step by $g'(h(x))$ and finally $h'(x)$"},
                {"step": "4. Algebraic Simplification", "desc": "Factor common terms and simplify rational/trigonometric expressions"}
            ]
        }

        mindmap_data = {
            "name": "Differentiation",
            "children": [
                {"name": "Foundations", "children": [{"name": "First Principles Limit"}, {"name": "Geometric Slope"}, {"name": "Differentiability ⇒ Continuity"}]},
                {"name": "Core Rules", "children": [{"name": "Power: d(x^n)/dx = n·x^(n-1)"}, {"name": "Product: (uv)' = u'v + uv'"}, {"name": "Quotient: (u/v)' = (u'v-uv')/v²"}, {"name": "Chain Rule: dy/dx = (dy/du)(du/dx)"}]},
                {"name": "Function Families", "children": [{"name": "Trig: sin, cos, tan, sec, csc, cot"}, {"name": "Inverse Trig: arcsin, arctan"}, {"name": "Exponential: e^x, a^x"}, {"name": "Logarithmic: ln x, log_a x"}]},
                {"name": "Advanced Methods", "children": [{"name": "Implicit Differentiation"}, {"name": "Logarithmic (f(x)^g(x))"}, {"name": "Parametric Form"}, {"name": "Higher Order (d²y/dx²)"}]}
            ]
        }

        self._store_chapter(
            cid=cid,
            subject="math",
            subject_title="Maths",
            title="Differentiation & Calculus",
            source_file=source_file,
            reading_time_min=10,
            detailed_html=detailed_html,
            toc=toc,
            revision_html=revision_html,
            flashcards=flashcards,
            flow_data=flow_data,
            mindmap_data=mindmap_data,
            has_handwritten=True,
            pages=pages
        )

    def _add_dbms(self):
        cid = "cs-dbms"
        source_file = "dbms.pdf"
        pages = self._extract_pdf_pages(source_file)

        detailed_html = r"""
<div id="sec-1" class="study-section">
  <h3>1. Database Architecture & 3-Schema Model</h3>
  <p>A <strong>Database Management System (DBMS)</strong> is software designed to store, retrieve, define, and manage structured data efficiently.</p>
  <ul>
    <li><strong>Internal / Physical Level:</strong> Describes physical storage structures, index organization, and data layout on disk.</li>
    <li><strong>Conceptual / Logical Level:</strong> Defines all database entities, relationships, attributes, and integrity constraints without storage details.</li>
    <li><strong>External / View Level:</strong> User-customized views of the data hiding irrelevant details and security restrictions.</li>
  </ul>
  <p><strong>Data Independence:</strong> <em>Logical Data Independence</em> (immunity of external schemas to conceptual changes) and <em>Physical Data Independence</em> (immunity of conceptual schema to physical storage changes).</p>
</div>

<div id="sec-2" class="study-section">
  <h3>2. Relational Model & Key Concepts</h3>
  <ul>
    <li><strong>Super Key:</strong> Set of one or more attributes that uniquely identifies a tuple.</li>
    <li><strong>Candidate Key:</strong> Minimal Super Key with no extraneous attributes.</li>
    <li><strong>Primary Key:</strong> The chosen candidate key (must be unique and non-NULL).</li>
    <li><strong>Foreign Key:</strong> Attribute that references the Primary Key of another relation to enforce <em>referential integrity</em>.</li>
  </ul>
</div>

<div id="sec-3" class="study-section">
  <h3>3. Relational Normalization (1NF to BCNF)</h3>
  <p>Normalization decomposes tables to eliminate redundancy and update/insert/delete anomalies:</p>
  <ul>
    <li><strong>1NF (First Normal Form):</strong> All attribute values must be atomic (no multi-valued or composite attributes).</li>
    <li><strong>2NF (Second Normal Form):</strong> In 1NF and no non-prime attribute is partially dependent on any candidate key (elimination of partial dependency).</li>
    <li><strong>3NF (Third Normal Form):</strong> In 2NF and for every functional dependency $X \to Y$, either $X$ is a super key or $Y$ is a prime attribute (elimination of transitive dependency).</li>
    <li><strong>BCNF (Boyce-Codd Normal Form):</strong> For every non-trivial functional dependency $X \to Y$, $X$ must be a strict super key.</li>
  </ul>
</div>

<div id="sec-4" class="study-section">
  <h3>4. Transactions & ACID Properties</h3>
  <div class="formula-block">
    <strong>Atomicity:</strong> All operations execute completely or none at all (Rollback / Commit).<br>
    <strong>Consistency:</strong> Database transitions from one valid state to another satisfying all integrity constraints.<br>
    <strong>Isolation:</strong> Concurrent transactions execute independently without interference.<br>
    <strong>Durability:</strong> Once committed, updates persist permanently even through system crashes.
  </div>
</div>
"""
        toc = [
            {"id": "sec-1", "title": "1. Database Architecture & 3-Schema Model"},
            {"id": "sec-2", "title": "2. Relational Keys & Integrity Constraints"},
            {"id": "sec-3", "title": "3. Normalization (1NF, 2NF, 3NF, BCNF)"},
            {"id": "sec-4", "title": "4. Transactions & ACID Properties"}
        ]

        revision_html = r"""
<div class="revision-sheet">
  <div class="rev-card">
    <h4>ONE-LINE IDEA</h4>
    <p>DBMS organizes data through 3-tier abstraction, enforces integrity constraints, eliminates anomalies via normalization, and guarantees transactional ACID safety.</p>
  </div>
  <div class="rev-card">
    <h4>NORMALIZATION CHEAT SHEET</h4>
    <ul>
      <li>1NF: Atomic values only.</li>
      <li>2NF: 1NF + No Partial Dependency (Proper subset of Candidate Key $\to$ Non-prime).</li>
      <li>3NF: 2NF + No Transitive Dependency ($X \to Y \implies X$ is Super Key OR $Y$ is Prime).</li>
      <li>BCNF: Every LHS of $X \to Y$ must be a Super Key.</li>
    </ul>
  </div>
  <div class="rev-card">
    <h4>ACID & SERIALIZABILITY</h4>
    <p>• Conflict Serializability verified using Precedence (Serialization) Graph (cycle $\implies$ non-serializable).<br>• Two-Phase Locking (2PL) guarantees conflict serializability.</p>
  </div>
</div>
"""

        flashcards = [
            {"q": "What are the ACID properties in DBMS?", "a": "Atomicity (all or nothing), Consistency (preserves invariants), Isolation (concurrency control), Durability (persists after commit)."},
            {"q": "What is the difference between 3NF and BCNF?", "a": "In 3NF, for X -> Y, X must be a super key OR Y must be a prime attribute. In BCNF, X must ALWAYS be a super key."},
            {"q": "What is the difference between Candidate Key and Primary Key?", "a": "Candidate key is any minimal super key. Primary key is the specific candidate key selected by database designer to identify tuples uniquely."},
            {"q": "What is Two-Phase Locking (2PL)?", "a": "A concurrency control protocol with a Growing Phase (locks acquired, none released) and a Shrinking Phase (locks released, none acquired)."},
            {"q": "What anomaly is caused by partial dependency?", "a": "Redundant data storage and update anomalies, resolved by decomposing table into 2NF."}
        ]

        flow_data = {
            "title": "Relational Table Normalization Procedure",
            "steps": [
                {"step": "1. Test 1NF", "desc": "Ensure all table attributes contain atomic values (remove repeating groups)"},
                {"step": "2. Test 2NF", "desc": "Identify Candidate Keys; remove Partial Dependencies (subset of CK determining non-prime)"},
                {"step": "3. Test 3NF", "desc": "Check Functional Dependencies $X \to Y$: Ensure $X$ is Super Key or $Y$ is Prime"},
                {"step": "4. Test BCNF", "desc": "Decompose if any non-trivial FD has a non-super-key on LHS"}
            ]
        }

        mindmap_data = {
            "name": "Database Management Systems",
            "children": [
                {"name": "Architecture", "children": [{"name": "3-Tier Schema (Internal, Conceptual, External)"}, {"name": "Data Independence (Logical & Physical)"}]},
                {"name": "Relational Model", "children": [{"name": "Keys: Super, Candidate, Primary, Foreign"}, {"name": "Integrity: Entity, Referential, Domain"}]},
                {"name": "Normalization", "children": [{"name": "1NF (Atomic)"}, {"name": "2NF (No Partial Dep)"}, {"name": "3NF (No Transitive Dep)"}, {"name": "BCNF (Strict Super Key)"}]},
                {"name": "Transactions", "children": [{"name": "ACID Properties"}, {"name": "Concurrency: 2PL, Timestamp"}, {"name": "Serializability & Deadlocks"}]}
            ]
        }

        self._store_chapter(
            cid=cid,
            subject="cs",
            subject_title="CS",
            title="Database Management Systems (DBMS)",
            source_file=source_file,
            reading_time_min=15,
            detailed_html=detailed_html,
            toc=toc,
            revision_html=revision_html,
            flashcards=flashcards,
            flow_data=flow_data,
            mindmap_data=mindmap_data,
            has_handwritten=True,
            pages=pages
        )

    def _add_sql(self):
        cid = "cs-sql"
        source_file = "SQL Notes📌.pdf"
        pages = self._extract_pdf_pages(source_file)

        detailed_html = r"""
<div id="sec-1" class="study-section">
  <h3>1. SQL Command Categories</h3>
  <ul>
    <li><strong>DDL (Data Definition Language):</strong> Defines schema structure: <code>CREATE</code>, <code>ALTER</code>, <code>DROP</code>, <code>TRUNCATE</code>, <code>RENAME</code>.</li>
    <li><strong>DML (Data Manipulation Language):</strong> Modifies table records: <code>INSERT</code>, <code>UPDATE</code>, <code>DELETE</code>.</li>
    <li><strong>DQL (Data Query Language):</strong> Retrieves data: <code>SELECT</code>.</li>
    <li><strong>DCL (Data Control Language):</strong> Manages permissions: <code>GRANT</code>, <code>REVOKE</code>.</li>
    <li><strong>TCL (Transaction Control Language):</strong> Controls transactional state: <code>COMMIT</code>, <code>ROLLBACK</code>, <code>SAVEPOINT</code>.</li>
  </ul>
</div>

<div id="sec-2" class="study-section">
  <h3>2. SQL Query Execution Order</h3>
  <p>SQL queries are executed logically in a specific order distinct from written syntax:</p>
  <div class="formula-block">
    <strong>Execution Sequence:</strong><br>
    1. <code>FROM</code> / <code>JOIN</code> &nbsp;(Identifies target tables & cross-products)<br>
    2. <code>WHERE</code> &nbsp;(Filters row-level records before grouping)<br>
    3. <code>GROUP BY</code> &nbsp;(Aggregates rows into groups)<br>
    4. <code>HAVING</code> &nbsp;(Filters groups based on aggregate conditions)<br>
    5. <code>SELECT</code> &nbsp;(Evaluates projected expressions & column aliases)<br>
    6. <code>DISTINCT</code> &nbsp;(Removes duplicate result rows)<br>
    7. <code>ORDER BY</code> &nbsp;(Sorts final result set)<br>
    8. <code>LIMIT / OFFSET</code> &nbsp;(Restricts returned row count)
  </div>
</div>

<div id="sec-3" class="study-section">
  <h3>3. Relational JOINs</h3>
  <ul>
    <li><strong>INNER JOIN:</strong> Returns rows when there is matching key in both tables.</li>
    <li><strong>LEFT OUTER JOIN:</strong> Returns all rows from left table and matched rows from right table (fills NULLs if no match).</li>
    <li><strong>RIGHT OUTER JOIN:</strong> Returns all rows from right table and matched rows from left table.</li>
    <li><strong>FULL OUTER JOIN:</strong> Returns all rows when there is a match in either table.</li>
    <li><strong>CROSS JOIN:</strong> Cartesian product of both tables ($N \times M$ rows).</li>
  </ul>
</div>

<div id="sec-4" class="study-section">
  <h3>4. Subqueries & Window Functions</h3>
  <p><strong>Correlated Subquery:</strong> Subquery that references columns from the outer query, executing once per candidate outer row.</p>
  <p><strong>Window Functions:</strong> Calculate aggregate/ranking values across row sets without collapsing rows: <code>ROW_NUMBER()</code>, <code>RANK()</code>, <code>DENSE_RANK()</code>, <code>LEAD()</code>, <code>LAG() OVER (PARTITION BY ... ORDER BY ...)</code>.</p>
</div>
"""
        toc = [
            {"id": "sec-1", "title": "1. SQL Command Categories (DDL, DML, DQL, TCL)"},
            {"id": "sec-2", "title": "2. SQL Query Execution Order"},
            {"id": "sec-3", "title": "3. Relational JOINs (Inner, Left, Right, Full)"},
            {"id": "sec-4", "title": "4. Subqueries & Window Functions"}
        ]

        revision_html = r"""
<div class="revision-sheet">
  <div class="rev-card">
    <h4>ONE-LINE IDEA</h4>
    <p>SQL is the declarative query standard for relational databases, executing logically via FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY.</p>
  </div>
  <div class="rev-card">
    <h4>MUST REMEMBER CLAUSE RULES</h4>
    <ul>
      <li>WHERE filters individual rows before grouping; HAVING filters aggregated groups.</li>
      <li>Aggregate functions (COUNT, SUM, AVG, MIN, MAX) ignore NULL values (except COUNT(*)).</li>
      <li>DELETE is DML (can be rolled back, fires triggers); TRUNCATE is DDL (resets high-water mark, faster, cannot be rolled back in standard SQL).</li>
    </ul>
  </div>
</div>
"""

        flashcards = [
            {"q": "What is the logical order of execution for a SQL SELECT query?", "a": "FROM / JOIN -> WHERE -> GROUP BY -> HAVING -> SELECT -> DISTINCT -> ORDER BY -> LIMIT."},
            {"q": "What is the difference between WHERE and HAVING clauses?", "a": "WHERE filters rows before aggregation. HAVING filters groups after GROUP BY aggregation."},
            {"q": "What is the difference between DELETE and TRUNCATE?", "a": "DELETE is DML (row-by-row, logs transactions, rollable). TRUNCATE is DDL (deallocates pages, faster, resets identity)."},
            {"q": "What is the difference between RANK() and DENSE_RANK() window functions?", "a": "RANK() leaves gaps in sequence for tied values (1, 2, 2, 4). DENSE_RANK() leaves no gaps (1, 2, 2, 3)."},
            {"q": "What is a Foreign Key constraint?", "a": "Enforces referential integrity by ensuring column values match a Primary Key value in another relation."}
        ]

        flow_data = {
            "title": "SQL Query Logical Execution Order",
            "steps": [
                {"step": "1. FROM & JOINs", "desc": "Load source tables and perform join conditions"},
                {"step": "2. WHERE Filter", "desc": "Filter rows matching predicate condition"},
                {"step": "3. GROUP BY & HAVING", "desc": "Aggregate rows into groups and filter groups via HAVING"},
                {"step": "4. SELECT & ORDER BY", "desc": "Project columns, evaluate window functions, and sort results"}
            ]
        }

        mindmap_data = {
            "name": "SQL & Relational Queries",
            "children": [
                {"name": "Language Categories", "children": [{"name": "DDL: CREATE, ALTER, DROP, TRUNCATE"}, {"name": "DML: INSERT, UPDATE, DELETE"}, {"name": "DQL: SELECT"}, {"name": "TCL: COMMIT, ROLLBACK"}]},
                {"name": "Execution Pipeline", "children": [{"name": "FROM -> WHERE"}, {"name": "GROUP BY -> HAVING"}, {"name": "SELECT -> DISTINCT -> ORDER BY"}]},
                {"name": "JOINs & Subqueries", "children": [{"name": "INNER, LEFT, RIGHT, FULL OUTER"}, {"name": "Correlated vs Non-Correlated"}, {"name": "EXISTS / IN / ALL / ANY"}]},
                {"name": "Advanced Features", "children": [{"name": "Window Functions (ROW_NUMBER, DENSE_RANK)"}, {"name": "Views & Common Table Expressions (CTEs)"}, {"name": "Indexes (B-Tree, Hash)"}]}
            ]
        }

        self._store_chapter(
            cid=cid,
            subject="cs",
            subject_title="CS",
            title="SQL & Relational Queries",
            source_file=source_file,
            reading_time_min=14,
            detailed_html=detailed_html,
            toc=toc,
            revision_html=revision_html,
            flashcards=flashcards,
            flow_data=flow_data,
            mindmap_data=mindmap_data,
            has_handwritten=True,
            pages=pages
        )

    def _add_computer_networks(self):
        cid = "cs-cn"
        source_file = "cn.pdf"
        pages = self._extract_pdf_pages(source_file)

        detailed_html = r"""
<div id="sec-1" class="study-section">
  <h3>1. OSI 7-Layer Architecture vs TCP/IP</h3>
  <ul>
    <li><strong>7. Application Layer:</strong> Network processes to applications (HTTP, DNS, FTP, SMTP).</li>
    <li><strong>6. Presentation Layer:</strong> Data representation, encryption, and compression (SSL/TLS, ASCII, JPEG).</li>
    <li><strong>5. Session Layer:</strong> Interhost communication and session management (RPC, NetBIOS).</li>
    <li><strong>4. Transport Layer:</strong> End-to-end connections, reliability, flow/congestion control (TCP, UDP). Data Unit: <em>Segment</em>.</li>
    <li><strong>3. Network Layer:</strong> Logical addressing, routing, path determination (IP, ICMP, OSPF, BGP). Data Unit: <em>Packet</em>.</li>
    <li><strong>2. Data Link Layer:</strong> Physical addressing, framing, error/flow control (Ethernet, MAC, ARP, CSMA/CD). Data Unit: <em>Frame</em>.</li>
    <li><strong>1. Physical Layer:</strong> Binary transmission over physical medium (Cables, Fiber, Signals). Data Unit: <em>Bit</em>.</li>
  </ul>
</div>

<div id="sec-2" class="study-section">
  <h3>2. Transport Layer: TCP vs UDP & 3-Way Handshake</h3>
  <table style="width: 100%; border-collapse: collapse; margin: 0.8rem 0; font-size: 0.85rem;">
    <thead>
      <tr style="border-bottom: 2px solid var(--border-card); text-align: left;">
        <th style="padding: 6px;">Feature</th>
        <th style="padding: 6px;">TCP (Transmission Control Protocol)</th>
        <th style="padding: 6px;">UDP (User Datagram Protocol)</th>
      </tr>
    </thead>
    <tbody>
      <tr style="border-bottom: 1px solid var(--border-subtle);"><td style="padding: 6px;">Connection</td><td style="padding: 6px;">Connection-oriented (3-Way Handshake)</td><td style="padding: 6px;">Connectionless</td></tr>
      <tr style="border-bottom: 1px solid var(--border-subtle);"><td style="padding: 6px;">Reliability</td><td style="padding: 6px;">Guaranteed (ACK, Retransmission)</td><td style="padding: 6px;">Best-effort (No ACK)</td></tr>
      <tr style="border-bottom: 1px solid var(--border-subtle);"><td style="padding: 6px;">Ordering</td><td style="padding: 6px;">Guaranteed in-order delivery</td><td style="padding: 6px;">No ordering guarantees</td></tr>
      <tr><td style="padding: 6px;">Header Size</td><td style="padding: 6px;">20–60 Bytes</td><td style="padding: 6px;">8 Bytes (Low overhead)</td></tr>
    </tbody>
  </table>
  <div class="formula-block">
    <strong>TCP 3-Way Handshake:</strong><br>
    1. Client $\xrightarrow{\text{SYN, seq}=x}$ Server<br>
    2. Server $\xrightarrow{\text{SYN-ACK, seq}=y, \text{ack}=x+1}$ Client<br>
    3. Client $\xrightarrow{\text{ACK, seq}=x+1, \text{ack}=y+1}$ Server
  </div>
</div>

<div id="sec-3" class="study-section">
  <h3>3. IP Addressing & Subnetting</h3>
  <p>IPv4 uses 32-bit addresses formatted as 4 octets. CIDR (Classless Inter-Domain Routing) notation: <code>192.168.1.0/24</code>.</p>
  <div class="formula-block">
    <strong>Number of Total IP Addresses:</strong> $2^{(32 - \text{prefix})}$<br>
    <strong>Number of Usable Host IPs:</strong> $2^{(32 - \text{prefix})} - 2$ &nbsp;(Subtract Network ID & Broadcast ID)
  </div>
</div>
"""
        toc = [
            {"id": "sec-1", "title": "1. OSI 7-Layer Architecture vs TCP/IP"},
            {"id": "sec-2", "title": "2. Transport Layer: TCP vs UDP & 3-Way Handshake"},
            {"id": "sec-3", "title": "3. IP Addressing, Subnetting & Routing"}
        ]

        revision_html = r"""
<div class="revision-sheet">
  <div class="rev-card">
    <h4>ONE-LINE IDEA</h4>
    <p>Computer Networks transmit data via layered encapsulation, routing IP packets across networks, and ensuring end-to-end transport reliability with TCP.</p>
  </div>
  <div class="rev-card">
    <h4>LAYER DATA UNITS</h4>
    <ul>
      <li>Application / Presentation / Session: Data / Message</li>
      <li>Transport: Segment</li>
      <li>Network: Packet / Datagram</li>
      <li>Data Link: Frame (MAC address)</li>
      <li>Physical: Bits</li>
    </ul>
  </div>
</div>
"""

        flashcards = [
            {"q": "What is the sequence of the OSI 7-layer model from bottom to top?", "a": "Physical -> Data Link -> Network -> Transport -> Session -> Presentation -> Application (Please Do Not Throw Sausage Pizza Away)."},
            {"q": "How does TCP 3-Way Handshake establish connection?", "a": "1. Client sends SYN. 2. Server replies with SYN-ACK. 3. Client responds with ACK."},
            {"q": "What is the difference between TCP and UDP?", "a": "TCP is connection-oriented, reliable with ACKs and flow control. UDP is connectionless, lightweight, and prioritized for streaming/gaming."},
            {"q": "How many usable host addresses are in a /26 IPv4 subnet?", "a": "2^(32-26) - 2 = 2^6 - 2 = 64 - 2 = 62 usable host addresses."},
            {"q": "What is the purpose of the ARP (Address Resolution Protocol)?", "a": "Maps a known logical IP address (Network Layer) to a physical MAC address (Data Link Layer)."}
        ]

        flow_data = {
            "title": "Data Encapsulation & Packet Transmission Flow",
            "steps": [
                {"step": "1. Application Data", "desc": "Application generates payload (HTTP message)"},
                {"step": "2. Transport Segment", "desc": "TCP/UDP adds Port Numbers and Sequence Numbers"},
                {"step": "3. Network Packet", "desc": "IP layer adds Source/Destination IP and TTL"},
                {"step": "4. Data Link Frame", "desc": "Ethernet adds MAC header and CRC checksum trailer"}
            ]
        }

        mindmap_data = {
            "name": "Computer Networks",
            "children": [
                {"name": "OSI 7 Layers", "children": [{"name": "Application & Presentation"}, {"name": "Transport (Segment)"}, {"name": "Network (Packet)"}, {"name": "Data Link & Physical (Frame/Bits)"}]},
                {"name": "Protocols", "children": [{"name": "Transport: TCP (3-Way Handshake) vs UDP"}, {"name": "Network: IP, ICMP, ARP, OSPF, BGP"}, {"name": "Application: HTTP/HTTPS, DNS, DHCP"}]},
                {"name": "Addressing & Routing", "children": [{"name": "IPv4 / IPv6"}, {"name": "Subnetting (CIDR)"}, {"name": "Routing Algorithms (Dijkstra, Bellman-Ford)"}]},
                {"name": "Flow & Congestion", "children": [{"name": "Sliding Window Protocol"}, {"name": "TCP Slow Start & Congestion Avoidance"}]}
            ]
        }

        self._store_chapter(
            cid=cid,
            subject="cs",
            subject_title="CS",
            title="Computer Networks (CN)",
            source_file=source_file,
            reading_time_min=16,
            detailed_html=detailed_html,
            toc=toc,
            revision_html=revision_html,
            flashcards=flashcards,
            flow_data=flow_data,
            mindmap_data=mindmap_data,
            has_handwritten=True,
            pages=pages
        )

    def _add_operating_systems(self):
        cid = "cs-os"
        source_file = "os_copy.pdf"
        pages = self._extract_pdf_pages(source_file)

        detailed_html = r"""
<div id="sec-1" class="study-section">
  <h3>1. Process Management & PCB</h3>
  <p>A <strong>Process</strong> is a program in execution. Its state is captured in the <strong>Process Control Block (PCB)</strong>, containing Process ID (PID), Program Counter (PC), CPU registers, memory limits, and open file lists.</p>
  <ul>
    <li><strong>Process States:</strong> New $\to$ Ready $\to$ Running $\to$ Waiting / Blocked $\to$ Terminated.</li>
    <li><strong>Context Switch:</strong> Storing state of current process in its PCB and loading saved state of another process from its PCB.</li>
  </ul>
</div>

<div id="sec-2" class="study-section">
  <h3>2. CPU Scheduling Algorithms</h3>
  <ul>
    <li><strong>FCFS (First-Come, First-Served):</strong> Non-preemptive, simple, suffers from <em>Convoy Effect</em>.</li>
    <li><strong>SJF (Shortest Job First):</strong> Optimal average waiting time; preemptive version is SRTF (Shortest Remaining Time First).</li>
    <li><strong>Round Robin (RR):</strong> Preemptive with time quantum $q$; prevents starvation.</li>
    <li><strong>Priority Scheduling:</strong> Can cause starvation (solved by <em>Aging</em>).</li>
  </ul>
</div>

<div id="sec-3" class="study-section">
  <h3>3. Deadlocks & 4 Coffman Conditions</h3>
  <p>A <strong>Deadlock</strong> occurs when a set of processes are blocked because each is holding a resource and waiting for another resource held by another process.</p>
  <div class="formula-block">
    <strong>4 Necessary Conditions for Deadlock:</strong><br>
    1. <strong>Mutual Exclusion:</strong> At least one resource must be held in non-shareable mode.<br>
    2. <strong>Hold and Wait:</strong> Process holds resource while requesting additional ones.<br>
    3. <strong>No Preemption:</strong> Resources cannot be forcibly seized from a process.<br>
    4. <strong>Circular Wait:</strong> Closed chain of processes exists where each waits for resource held by next ($P_0 \to P_1 \to \dots \to P_n \to P_0$).
  </div>
  <p><strong>Banker's Algorithm:</strong> Avoids deadlocks by verifying system remains in a <em>Safe State</em> before granting resource requests ($Need = Max - Allocation \le Available$).</p>
</div>

<div id="sec-4" class="study-section">
  <h3>4. Memory Management & Paging</h3>
  <p><strong>Paging:</strong> Non-contiguous memory allocation dividing logical address space into fixed-size <strong>Pages</strong> and physical memory into <strong>Frames</strong>.</p>
  <div class="formula-block">
    <strong>Logical Address:</strong> Page Number ($p$) and Page Offset ($d$).<br>
    <strong>TLB (Translation Lookaside Buffer):</strong> High-speed hardware cache for page table mappings.<br>
    <strong>Effective Access Time (EAT):</strong> $EAT = h(t_{\text{TLB}} + t_{\text{mem}}) + (1-h)(t_{\text{TLB}} + 2 t_{\text{mem}})$.
  </div>
</div>
"""
        toc = [
            {"id": "sec-1", "title": "1. Process Management & PCB States"},
            {"id": "sec-2", "title": "2. CPU Scheduling (FCFS, SJF, Round Robin)"},
            {"id": "sec-3", "title": "3. Deadlocks & 4 Coffman Conditions"},
            {"id": "sec-4", "title": "4. Memory Management, Paging & TLB"}
        ]

        revision_html = r"""
<div class="revision-sheet">
  <div class="rev-card">
    <h4>ONE-LINE IDEA</h4>
    <p>Operating Systems manage CPU scheduling, synchronization, memory virtualization via paging, and deadlock prevention.</p>
  </div>
  <div class="rev-card">
    <h4>DEADLOCK 4 CONDITIONS</h4>
    <ul>
      <li>Mutual Exclusion</li>
      <li>Hold and Wait</li>
      <li>No Preemption</li>
      <li>Circular Wait</li>
    </ul>
  </div>
  <div class="rev-card">
    <h4>KEY EQUATIONS</h4>
    <ul>
      <li>Turnaround Time = Completion Time - Arrival Time</li>
      <li>Waiting Time = Turnaround Time - Burst Time</li>
      <li>EAT = $h(t_{\text{TLB}} + t_m) + (1-h)(t_{\text{TLB}} + 2 t_m)$</li>
    </ul>
  </div>
</div>
"""

        flashcards = [
            {"q": "What are the 4 necessary conditions for Deadlock?", "a": "1. Mutual Exclusion, 2. Hold and Wait, 3. No Preemption, 4. Circular Wait."},
            {"q": "What is the difference between Preemptive and Non-Preemptive scheduling?", "a": "Preemptive allows OS to interrupt a running process (e.g. Round Robin, SRTF). Non-preemptive allows process to run until it finishes or yields (e.g. FCFS)."},
            {"q": "What is the Convoy Effect?", "a": "When small CPU-bound or I/O-bound processes wait behind a massive CPU-heavy process in FCFS scheduling, degrading throughput."},
            {"q": "What is Paging and what problem does it solve?", "a": "Paging is non-contiguous memory management dividing logical memory into Pages and physical memory into Frames, eliminating external fragmentation."},
            {"q": "What is the Critical Section Problem and what are its requirements?", "a": "A code segment accessing shared resources. Requirements: 1. Mutual Exclusion, 2. Progress, 3. Bounded Waiting."}
        ]

        flow_data = {
            "title": "Process State Transition Lifecycle",
            "steps": [
                {"step": "1. New State", "desc": "Process created and admitted to Ready queue by Long-Term Scheduler"},
                {"step": "2. Ready -> Running", "desc": "Short-Term Scheduler (Dispatcher) allocates CPU to process"},
                {"step": "3. Running -> Waiting", "desc": "Process initiates I/O or awaits event/mutex"},
                {"step": "4. Terminated", "desc": "Process finishes execution and OS reclaims allocated resources and PCB"}
            ]
        }

        mindmap_data = {
            "name": "Operating Systems",
            "children": [
                {"name": "Process Management", "children": [{"name": "PCB & Context Switch"}, {"name": "Process States (New, Ready, Running, Wait, Term)"}, {"name": "Threads & Fork"}]},
                {"name": "CPU Scheduling", "children": [{"name": "FCFS (Convoy Effect)"}, {"name": "SJF / SRTF (Optimal)"}, {"name": "Round Robin (Quantum)"}, {"name": "Priority & Multilevel"}]},
                {"name": "Synchronization & Deadlock", "children": [{"name": "Critical Section & Mutex/Semaphores"}, {"name": "4 Coffman Conditions"}, {"name": "Banker's Algorithm"}]},
                {"name": "Memory Management", "children": [{"name": "Paging & Frames"}, {"name": "TLB & Page Tables"}, {"name": "Virtual Memory & Page Faults (FIFO, LRU)"}]}
            ]
        }

        self._store_chapter(
            cid=cid,
            subject="cs",
            subject_title="CS",
            title="Operating Systems (OS)",
            source_file=source_file,
            reading_time_min=16,
            detailed_html=detailed_html,
            toc=toc,
            revision_html=revision_html,
            flashcards=flashcards,
            flow_data=flow_data,
            mindmap_data=mindmap_data,
            has_handwritten=True,
            pages=pages
        )

    def _store_chapter(
        self,
        cid: str,
        subject: str,
        subject_title: str,
        title: str,
        source_file: str,
        reading_time_min: int,
        detailed_html: str,
        toc: List[Dict[str, str]],
        revision_html: str,
        flashcards: List[Dict[str, str]],
        flow_data: Dict[str, Any],
        mindmap_data: Dict[str, Any],
        has_handwritten: bool,
        pages: List[Dict[str, Any]]
    ):
        # Calculate clean text word count
        clean_text = re.sub(r"<[^>]+>", " ", detailed_html)
        words = len(clean_text.split())

        # Generate semantic chunks for RAG & vector search
        chunks = []
        chunk_idx = 1
        for p in pages:
            ptxt = p.get("text", "").strip()
            pnum = p.get("page_num", 1)
            if not ptxt:
                continue
            paras = [pr.strip() for pr in ptxt.split("\n\n") if len(pr.strip()) > 30]
            for para in paras:
                chunks.append({
                    "chapter_id": cid,
                    "chapter_title": title,
                    "subject": subject,
                    "chunk_index": chunk_idx,
                    "page_number": pnum,
                    "text": para
                })
                chunk_idx += 1

        if not chunks:
            # Fallback chunk
            chunks.append({
                "chapter_id": cid,
                "chapter_title": title,
                "subject": subject,
                "chunk_index": 1,
                "page_number": 1,
                "text": clean_text[:400]
            })

        self.all_chunks.extend(chunks)

        self.chapters_db[cid] = {
            "id": cid,
            "subject": subject,
            "subject_title": subject_title,
            "title": title,
            "source_file": source_file,
            "reading_time_min": reading_time_min,
            "word_count": words,
            "detailed_html": detailed_html,
            "toc": toc,
            "revision_html": revision_html,
            "flashcards": flashcards,
            "flow_data": flow_data,
            "mindmap_data": mindmap_data,
            "has_handwritten": has_handwritten,
            "chunks_count": len(chunks)
        }

    def get_library(self, subject_filter: Optional[str] = None, search_query: Optional[str] = None) -> Dict[str, Any]:
        """Returns subject counts and chapters list."""
        counts = {"all": 0, "phys": 0, "chem": 0, "bio": 0, "math": 0, "cs": 0}

        all_chapters = list(self.chapters_db.values())
        for ch in all_chapters:
            s = ch["subject"]
            if s in counts:
                counts[s] += 1
            counts["all"] += 1

        filtered = all_chapters
        if subject_filter and subject_filter != "all":
            filtered = [c for c in filtered if c["subject"] == subject_filter]

        if search_query and search_query.strip():
            sq = search_query.strip().lower()
            filtered = [
                c for c in filtered
                if sq in c["title"].lower() or sq in c["subject_title"].lower() or sq in c["detailed_html"].lower()
            ]

        # Order logically by subject then title
        def sort_key(c):
            order = {"phys": 1, "chem": 2, "bio": 3, "math": 4, "cs": 5}
            return (order.get(c["subject"], 6), c["title"])

        filtered.sort(key=sort_key)

        return {
            "status": "success",
            "counts": counts,
            "chapters": [
                {
                    "id": c["id"],
                    "title": c["title"],
                    "subject": c["subject"],
                    "subject_title": c["subject_title"],
                    "reading_time_min": c["reading_time_min"],
                    "has_handwritten": c["has_handwritten"]
                }
                for c in filtered
            ]
        }

    def get_chapter(self, chapter_id: str) -> Optional[Dict[str, Any]]:
        return self.chapters_db.get(chapter_id)

    def search_excerpts(self, query: str) -> List[Dict[str, Any]]:
        """Searches across all notes and chunks returning subject, chapter, and excerpt."""
        q_lower = query.strip().lower()
        if not q_lower:
            return []

        results = []
        for ch in self.chapters_db.values():
            # Check title
            if q_lower in ch["title"].lower():
                results.append({
                    "chapter_id": ch["id"],
                    "title": ch["title"],
                    "subject": ch["subject_title"],
                    "section": "Overview",
                    "excerpt": f"Matched chapter: {ch['title']} in {ch['subject_title']}."
                })
                continue

            # Check chunks
            for chunk in self.all_chunks:
                if chunk["chapter_id"] == ch["id"] and q_lower in chunk["text"].lower():
                    # Extract snippet
                    txt = chunk["text"]
                    idx = txt.lower().find(q_lower)
                    start = max(0, idx - 40)
                    end = min(len(txt), idx + len(q_lower) + 80)
                    snippet = "..." + txt[start:end].replace("\n", " ") + "..."
                    results.append({
                        "chapter_id": ch["id"],
                        "title": ch["title"],
                        "subject": ch["subject_title"],
                        "section": f"Page {chunk['page_number']}",
                        "excerpt": snippet
                    })
                    break

        return results[:8]

resource_service = ResourceService()
