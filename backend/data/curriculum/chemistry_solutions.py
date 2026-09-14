"""
SIKSHA SAATHI — Chemistry Curriculum: Unit 1 Solutions (NCERT Class 12)
13 Distinct Topic Modules with Dedicated Detailed Notes, Revision Sheets,
Active-Recall Flashcards, Interactive Flowcharts, Zoomable Mind Maps, and RAG Chunks.
"""

from typing import Dict, List, Any

def get_all_solutions_topics() -> List[Dict[str, Any]]:
    """Returns the complete array of 13 structured Chemistry: Solutions topic modules."""

    topics = []

    # =========================================================================
    # MODULE 01: INTRODUCTION & 9 TYPES OF SOLUTIONS
    # =========================================================================
    m01_detailed = r"""
<div class="topic-header">
  <span class="topic-num">TOPIC 01 OF 13</span>
  <h3 class="topic-title">Introduction to Solutions & 9 Types of Solutions</h3>
</div>

<div class="concept-card">
  <div class="card-label">REAL-WORLD SIGNIFICANCE & COMPOSITION</div>
  <p>In nature, pure substances are exceptionally rare. Almost all physical processes in living organisms occur in liquid solutions, and the properties of materials depend fundamentally on their composition:</p>
  <ul>
    <li><strong>Alloys:</strong> <strong>Brass</strong> (Copper + Zinc) is distinct from <strong>German Silver</strong> (Copper + Zinc + Nickel) and <strong>Bronze</strong> (Copper + Tin).</li>
    <li><strong>Fluoride Ion Concentration:</strong>
      <ul>
        <li>$1.0\text{ ppm}$ in water prevents tooth decay and strengthens enamel.</li>
        <li>$1.5\text{ ppm}$ causes enamel mottling and fluorosis.</li>
        <li>High concentrations ($>10\text{ ppm}$, e.g. Sodium Fluoride $\text{NaF}$) are lethal and used in rat poison.</li>
      </ul>
    </li>
    <li><strong>Intravenous Fluids:</strong> Medical IV injections must be dissolved in sterile water containing salts at an exact ionic concentration matching human blood plasma ($0.9\%\text{ w/V NaCl}$) to prevent red blood cell lysis or crenation.</li>
  </ul>
</div>

<div class="concept-card">
  <div class="card-label">NCERT DEFINITIONS & BINARY SYSTEM</div>
  <p><strong>Solution:</strong> A <em>homogeneous mixture</em> of two or more chemically non-reacting substances whose composition and chemical properties are completely uniform throughout.</p>
  <p><strong>Solvent:</strong> The component present in the largest quantity, which determines the physical state in which the solution exists.</p>
  <p><strong>Solute:</strong> One or more components present in smaller amounts other than the solvent.</p>
  <p><strong>Binary Solution:</strong> A solution consisting of exactly two components (1 solute + 1 solvent).</p>
</div>

<div class="table-container">
  <div class="table-caption">NCERT Table 1.1: Comprehensive Classification of Solutions (9 Types)</div>
  <table class="notes-table">
    <thead>
      <tr><th>Type of Solution</th><th>Solute</th><th>Solvent</th><th>Authentic NCERT Example</th></tr>
    </thead>
    <tbody>
      <tr><td rowspan="3"><strong>Gaseous Solutions</strong></td><td>Gas</td><td>Gas</td><td>Mixture of Oxygen ($O_2$) and Nitrogen ($N_2$) gases (Air)</td></tr>
      <tr><td>Liquid</td><td>Gas</td><td>Chloroform ($\text{CHCl}_3$) vapor mixed with Nitrogen gas</td></tr>
      <tr><td>Solid</td><td>Gas</td><td>Camphor sublimation vapor in Nitrogen gas</td></tr>
      <tr style="border-top: 2px solid var(--border-subtle);"><td rowspan="3"><strong>Liquid Solutions</strong></td><td>Gas</td><td>Liquid</td><td>Oxygen ($O_2$) dissolved in water (sustains aquatic life)</td></tr>
      <tr><td>Liquid</td><td>Liquid</td><td>Ethanol ($\text{C}_2\text{H}_5\text{OH}$) dissolved in water</td></tr>
      <tr><td>Solid</td><td>Liquid</td><td>Glucose ($\text{C}_6\text{H}_{12}\text{O}_6$) dissolved in water</td></tr>
      <tr style="border-top: 2px solid var(--border-subtle);"><td rowspan="3"><strong>Solid Solutions</strong></td><td>Gas</td><td>Solid</td><td>Solution of Hydrogen ($H_2$) gas in Palladium ($\text{Pd}$) metal</td></tr>
      <tr><td>Liquid</td><td>Solid</td><td>Amalgam of Mercury ($\text{Hg}$) with Sodium ($\text{Na}$) metal</td></tr>
      <tr><td>Solid</td><td>Solid</td><td>Copper ($\text{Cu}$) dissolved in Gold ($\text{Au}$) (Alloy/Jewellery)</td></tr>
    </tbody>
  </table>
</div>

<div class="remember-box">
  <strong>💡 IMPORTANT TO REMEMBER:</strong>
  <ul>
    <li>The solvent determines the final macroscopic physical state of the solution.</li>
    <li>Solid solutions (alloys, amalgams) and gaseous solutions are true thermodynamic solutions.</li>
  </ul>
</div>

<div class="quick-revision-box">
  <strong>⚡ QUICK REVISION:</strong>
  Binary solution = 1 solute + 1 solvent. 9 combinations exist across Gas, Liquid, and Solid states. Composition governs properties (e.g. fluoride at 1 ppm vs 1.5 ppm).
</div>
"""
    m01_rev = r"""
<div class="revision-sheet">
  <div class="rev-card">
    <h4>ONE-LINE IDEA</h4>
    <p>A solution is a homogeneous phase of 2+ components whose physical state is determined by the solvent present in the largest quantity.</p>
  </div>
  <div class="rev-card">
    <h4>MUST REMEMBER EXAMPLES</h4>
    <ul>
      <li>Gas in Solid: $H_2$ in Palladium metal.</li>
      <li>Liquid in Solid: Amalgam of Mercury in Sodium.</li>
      <li>Liquid in Gas: Chloroform in Nitrogen gas.</li>
      <li>Solid in Gas: Camphor in Nitrogen gas.</li>
      <li>Solid in Solid: Copper in Gold (Brass, Bronze).</li>
    </ul>
  </div>
  <div class="rev-card">
    <h4>HIGH-YIELD BIOLOGICAL FACTS</h4>
    <p>• $1.0\text{ ppm } F^-$: prevents tooth decay.<br>• $1.5\text{ ppm } F^-$: causes mottled teeth.<br>• $\text{NaF}$ high concentration: rat poison.<br>• IV fluids must be isotonic with blood plasma.</p>
  </div>
</div>
"""
    m01_flashcards = [
        {"q": "Define a binary solution.", "a": "A homogeneous mixture consisting of exactly two components: one solvent (largest quantity) and one solute."},
        {"q": "Give an authentic NCERT example of a solid solution where solute is a gas.", "a": "Solution of Hydrogen gas (H₂) adsorbed in Palladium (Pd) metal."},
        {"q": "Give an example of a liquid solute in a gaseous solvent.", "a": "Chloroform (CHCl₃) vapor mixed with Nitrogen gas (N₂)."},
        {"q": "What is the biological effect of 1.0 ppm vs 1.5 ppm fluoride ions in water?", "a": "1.0 ppm prevents tooth decay; 1.5 ppm causes teeth to become mottled (fluorosis). High concentrations are toxic."},
        {"q": "What determines the physical state in which a solution exists?", "a": "The solvent, because it is the component present in the largest quantity."}
    ]
    m01_flow = {
        "title": "Classification of Solutions by Solvent State",
        "steps": [
            {"step": "1. Identify Solvent Phase", "desc": "Determine whether solvent is Gas, Liquid, or Solid"},
            {"step": "2. Identify Solute Phase", "desc": "Determine whether solute is Gas, Liquid, or Solid"},
            {"step": "3. Match to 9-Type Matrix", "desc": "e.g. Camphor in N₂ = Solid in Gas; H₂ in Pd = Gas in Solid"},
            {"step": "4. Verify Homogeneity", "desc": "Ensure composition and physical properties are completely uniform throughout"}
        ]
    }
    m01_mindmap = {
        "name": "Solutions: Introduction & Types",
        "children": [
            {"name": "Gaseous Solutions", "children": [{"name": "Gas in Gas (Air O2+N2)"}, {"name": "Liquid in Gas (CHCl3 in N2)"}, {"name": "Solid in Gas (Camphor in N2)"}]},
            {"name": "Liquid Solutions", "children": [{"name": "Gas in Liquid (O2 in H2O)"}, {"name": "Liquid in Liquid (Ethanol in H2O)"}, {"name": "Solid in Liquid (Glucose in H2O)"}]},
            {"name": "Solid Solutions", "children": [{"name": "Gas in Solid (H2 in Pd)"}, {"name": "Liquid in Solid (Hg-Na Amalgam)"}, {"name": "Solid in Solid (Cu in Au Alloy)"}]},
            {"name": "Biological Composition", "children": [{"name": "Fluoride (1 ppm vs 1.5 ppm)"}, {"name": "IV Fluids (Plasma Match)"}]}
        ]
    }

    topics.append({
        "id": "chem-sol-01-types",
        "subject": "chem",
        "subject_title": "Chemistry • Solutions",
        "title": "01. Introduction & 9 Types of Solutions",
        "source_file": "Class_12_Chemistry_Solutions_NCERT.pdf",
        "reading_time_min": 6,
        "detailed_html": m01_detailed,
        "toc": [{"id": "sec-01", "title": "01. Introduction & 9 Types of Solutions"}],
        "revision_html": m01_rev,
        "flashcards": m01_flashcards,
        "flow_data": m01_flow,
        "mindmap_data": m01_mindmap,
        "has_handwritten": False,
        "pages": [{"page_num": 1, "text": "Unit 1 Solutions. Objectives. Everyday importance: brass, German silver, bronze. 1 ppm fluoride prevents tooth decay, 1.5 ppm causes mottled teeth, high NaF is rat poison. Intravenous injections. Solutions are homogeneous mixtures. Solvent determines physical state; solute is minor component."}, {"page_num": 2, "text": "Table 1.1 Types of Solutions. Gaseous solutions (O2 in N2, chloroform in N2, camphor in N2). Liquid solutions (O2 in water, ethanol in water, glucose in water). Solid solutions (H2 in Pd, amalgam of Hg with Na, copper in gold)."}]
    })

    # =========================================================================
    # MODULE 02: CONCENTRATION OF SOLUTIONS
    # =========================================================================
    m02_detailed = r"""
<div class="topic-header">
  <span class="topic-num">TOPIC 02 OF 13</span>
  <h3 class="topic-title">Concentration of Solutions (M, m, ppm, Mole Fraction)</h3>
</div>

<p>Concentration expresses the exact amount of solute dissolved in a specified amount of solvent or solution quantitatively.</p>

<div class="micro-note-grid">
  <div class="micro-card">
    <h4>1. Mass Percentage (w/w)</h4>
    <p>Mass of component per 100 g of solution.</p>
    <div class="formula-block">
      $$\text{Mass } \% = \frac{\text{Mass of component}}{\text{Total mass of solution}} \times 100$$
    </div>
    <p><em>Example:</em> $10\%\text{ glucose} = 10\text{ g glucose} + 90\text{ g water}$. Commercial bleach contains $3.62\%\text{ NaOCl}$.</p>
    <span class="badge-temp temp-indep">Temperature Independent</span>
  </div>

  <div class="micro-card">
    <h4>2. Volume Percentage (V/V)</h4>
    <p>Volume of component per 100 mL of solution.</p>
    <div class="formula-block">
      $$\text{Volume } \% = \frac{\text{Volume of component}}{\text{Total volume of solution}} \times 100$$
    </div>
    <p><em>Example:</em> $35\%\text{ v/v ethylene glycol}$ antifreeze lowers freezing point of water to $255.4\text{ K} (-17.6^\circ\text{C})$.</p>
    <span class="badge-temp temp-dep">Temperature Dependent</span>
  </div>

  <div class="micro-card">
    <h4>3. Mass by Volume Percentage (w/V)</h4>
    <p>Mass of solute in grams in 100 mL of solution.</p>
    <div class="formula-block">
      $$\text{Mass by Volume } \% = \frac{\text{Mass of solute (g)}}{\text{Volume of solution (mL)}} \times 100$$
    </div>
    <p>Standard unit in medical pharmacy and diagnostic labs.</p>
    <span class="badge-temp temp-dep">Temperature Dependent</span>
  </div>

  <div class="micro-card">
    <h4>4. Parts Per Million (ppm)</h4>
    <p>Used when solute exists in minute trace quantities.</p>
    <div class="formula-block">
      $$\text{ppm} = \frac{\text{Parts of component}}{\text{Total parts of solution}} \times 10^6$$
    </div>
    <p><em>Example:</em> $1\text{ L sea water } (1030\text{ g})$ contains $6 \times 10^{-3}\text{ g } O_2 = 5.8\text{ ppm}$.</p>
    <span class="badge-temp temp-indep">Temperature Independent (mass basis)</span>
  </div>

  <div class="micro-card">
    <h4>5. Mole Fraction ($x$)</h4>
    <p>Ratio of moles of a component to total moles in solution.</p>
    <div class="formula-block">
      $$x_A = \frac{n_A}{n_A + n_B}, \quad \sum x_i = 1$$
    </div>
    <p>Dimensionless; fundamental for Raoult's and Henry's laws.</p>
    <span class="badge-temp temp-indep">Temperature Independent</span>
  </div>

  <div class="micro-card">
    <h4>6. Molarity ($M$)</h4>
    <p>Number of moles of solute per litre of solution.</p>
    <div class="formula-block">
      $$M = \frac{n_2}{V_{\text{L}}} = \frac{w_2 \times 1000}{M_2 \times V_{\text{mL}}}$$
    </div>
    <p>Unit: $\text{mol L}^{-1}$ or $\text{mol dm}^{-3}$.</p>
    <span class="badge-temp temp-dep">Temperature Dependent (Volume changes with T)</span>
  </div>

  <div class="micro-card">
    <h4>7. Molality ($m$)</h4>
    <p>Number of moles of solute per kilogram ($1000\text{ g}$) of solvent.</p>
    <div class="formula-block">
      $$m = \frac{n_2}{w_{1(\text{kg})}} = \frac{w_2 \times 1000}{M_2 \times w_{1(\text{g})}}$$
    </div>
    <p>Unit: $\text{mol kg}^{-1}$ or $\text{m}$.</p>
    <span class="badge-temp temp-indep">Temperature Independent (Mass is invariant with T)</span>
  </div>
</div>

<div class="comparison-card">
  <div class="card-label">MOLARITY VS MOLALITY</div>
  <table class="notes-table">
    <thead>
      <tr><th>Feature</th><th>Molarity ($M$)</th><th>Molality ($m$)</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>Denominator</strong></td><td>Total Volume of Solution ($V_{\text{sol}}$ in Litres)</td><td>Mass of Solvent only ($w_1$ in Kilograms)</td></tr>
      <tr><td><strong>Units</strong></td><td>$\text{mol L}^{-1}$</td><td>$\text{mol kg}^{-1}$</td></tr>
      <tr><td><strong>Temperature</strong></td><td>Changes with Temperature</td><td><strong>Invariant with Temperature</strong></td></tr>
      <tr><td><strong>Colligative Studies</strong></td><td>Less suitable for varying temperatures</td><td>Universally preferred in ebullioscopy & cryoscopy</td></tr>
    </tbody>
  </table>
</div>

<!-- SOLVED EXAMPLES & INTEXT QUESTIONS -->
<div class="numerical-card">
  <div class="num-header"><span class="num-tag">NCERT EXAMPLE 1.1</span><span class="num-title">Mole Fraction of Ethylene Glycol</span></div>
  <p><strong>Problem:</strong> Calculate mole fraction of ethylene glycol ($\text{C}_2\text{H}_6\text{O}_2$) in $20\%$ mass solution.</p>
  <div class="num-step">
    In $100\text{ g solution}$: $20\text{ g glycol } (M=62)$ and $80\text{ g water } (M=18)$.<br>
    $n_{\text{glycol}} = 20/62 = 0.322\text{ mol}, \quad n_{\text{water}} = 80/18 = 4.444\text{ mol}$.<br>
    $x_{\text{glycol}} = \frac{0.322}{0.322 + 4.444} = \mathbf{0.068}, \quad x_{\text{water}} = 1 - 0.068 = \mathbf{0.932}$.
  </div>
  <div class="num-ans"><strong>Final Answer:</strong> $x(\text{glycol}) = 0.068, \quad x(\text{water}) = 0.932$</div>
</div>

<div class="numerical-card">
  <div class="num-header"><span class="num-tag">NCERT EXAMPLE 1.2</span><span class="num-title">Molarity of NaOH Solution</span></div>
  <p><strong>Problem:</strong> Calculate molarity of $5\text{ g}$ of $\text{NaOH}$ in $450\text{ mL}$ solution.</p>
  <div class="num-step">
    $\text{Moles of NaOH} = \frac{5}{40} = 0.125\text{ mol}, \quad V = 450\text{ mL} = 0.450\text{ L}$.<br>
    $\text{Molarity } (M) = \frac{0.125 \times 1000}{450} = \mathbf{0.278\text{ mol L}^{-1}}$.
  </div>
  <div class="num-ans"><strong>Final Answer:</strong> $\text{Molarity} = 0.278\text{ M}$</div>
</div>

<div class="numerical-card">
  <div class="num-header"><span class="num-tag">NCERT EXAMPLE 1.3</span><span class="num-title">Molality of Ethanoic Acid in Benzene</span></div>
  <p><strong>Problem:</strong> Calculate molality of $2.5\text{ g}$ ethanoic acid ($\text{CH}_3\text{COOH}$) in $75\text{ g}$ benzene.</p>
  <div class="num-step">
    $n_2 = \frac{2.5}{60} = 0.0417\text{ mol}, \quad w_1 = 75\text{ g} = 0.075\text{ kg}$.<br>
    $\text{Molality } (m) = \frac{0.0417 \times 1000}{75} = \mathbf{0.556\text{ mol kg}^{-1}}$.
  </div>
  <div class="num-ans"><strong>Final Answer:</strong> $\text{Molality} = 0.556\text{ m}$</div>
</div>
"""
    m02_rev = r"""
<div class="revision-sheet">
  <div class="rev-card">
    <h4>CONCENTRATION FORMULA SUMMARY</h4>
    <ul>
      <li>$\text{Mass } \% = \frac{w_2}{w_1 + w_2} \times 100$</li>
      <li>$\text{ppm} = \frac{w_2}{w_{\text{total}}} \times 10^6$</li>
      <li>$x_2 = \frac{n_2}{n_1 + n_2}$</li>
      <li>$M = \frac{w_2 \times 1000}{M_2 \times V_{\text{mL}}}$ (changes with $T$)</li>
      <li>$m = \frac{w_2 \times 1000}{M_2 \times w_{1(\text{g})}}$ (invariant with $T$)</li>
    </ul>
  </div>
  <div class="rev-card">
    <h4>TEMPERATURE RULE</h4>
    <p>Mass %, ppm, mole fraction, and molality are independent of temperature. Molarity and Volume % depend on temperature because volume expands or contracts.</p>
  </div>
</div>
"""
    m02_flashcards = [
        {"q": "Why is molality preferred over molarity in temperature-variant experiments?", "a": "Molality depends on mass of solvent, which is invariant with temperature, whereas molarity depends on volume, which expands/contracts."},
        {"q": "What is the mole fraction of ethylene glycol in a 20% by mass aqueous solution?", "a": "0.068 for ethylene glycol and 0.932 for water (NCERT Example 1.1)."},
        {"q": "State the SI unit of Molarity and Molality.", "a": "Molarity: mol L⁻¹ (or mol dm⁻³). Molality: mol kg⁻¹."},
        {"q": "What is the concentration of dissolved oxygen in sea water in ppm?", "a": "About 5.8 ppm (5.8 g of O₂ per 10⁶ g of sea water)."},
        {"q": "What concentration of ethylene glycol is used as car engine antifreeze, and what is its freezing point?", "a": "35% (v/v) aqueous solution, which depresses the freezing point of water to 255.4 K (-17.6°C)."},
        {"q": "How is parts per million (ppm) defined mathematically?", "a": "ppm = (Number of parts of component / Total parts of all components) × 10⁶."}
    ]
    m02_flow = {
        "title": "Selecting Concentration Units",
        "steps": [
            {"step": "1. Check Temperature Condition", "desc": "Is the temperature variable? If YES, use Molality, Mole Fraction, or Mass %"},
            {"step": "2. Check Solute Proportion", "desc": "Is solute in trace micro-quantities? If YES, use Parts Per Million (ppm)"},
            {"step": "3. Check Colligative Application", "desc": "For boiling/freezing problems, use Molality ($m = \\frac{w_2 \\cdot 1000}{M_2 \\cdot w_1}$)"},
            {"step": "4. Check Osmotic Application", "desc": "For osmotic pressure, use Molarity ($C = \\frac{w_2}{M_2 \\cdot V_{\\text{L}}}$)"}
        ]
    }
    m02_mindmap = {
        "name": "Concentration Units",
        "children": [
            {"name": "Temperature Independent", "children": [{"name": "Mass % (w/w)"}, {"name": "Mole Fraction (x)"}, {"name": "Molality (m = mol/kg)"}, {"name": "Parts Per Million (ppm)"}]},
            {"name": "Temperature Dependent", "children": [{"name": "Volume % (v/v)"}, {"name": "Mass by Volume % (w/v)"}, {"name": "Molarity (M = mol/L)"}]}
        ]
    }

    topics.append({
        "id": "chem-sol-02-concentration",
        "subject": "chem",
        "subject_title": "Chemistry • Solutions",
        "title": "02. Concentration of Solutions (M, m, ppm)",
        "source_file": "Class_12_Chemistry_Solutions_NCERT.pdf",
        "reading_time_min": 10,
        "detailed_html": m02_detailed,
        "toc": [{"id": "sec-02", "title": "02. Concentration of Solutions"}],
        "revision_html": m02_rev,
        "flashcards": m02_flashcards,
        "flow_data": m02_flow,
        "mindmap_data": m02_mindmap,
        "has_handwritten": False,
        "pages": [{"page_num": 2, "text": "Concentration of solutions: qualitative vs quantitative. Mass percentage (w/w), Volume percentage (v/v)."}, {"page_num": 3, "text": "Volume % 35% ethylene glycol antifreeze. Mass by volume (w/v). Parts per million (ppm) in sea water. Mole fraction (x)."}, {"page_num": 4, "text": "Example 1.1 mole fraction of ethylene glycol. Molarity (M). Example 1.2 molarity of 5g NaOH in 450 mL."}, {"page_num": 5, "text": "Molality (m). Temperature dependence of molarity vs molality. Example 1.3 molality of ethanoic acid in benzene. Intext questions 1.1 to 1.5."}]
    })

    # =========================================================================
    # MODULE 03: SOLUBILITY OF SOLIDS IN LIQUIDS
    # =========================================================================
    m03_detailed = r"""
<div class="topic-header">
  <span class="topic-num">TOPIC 03 OF 13</span>
  <h3 class="topic-title">Solubility of Solids in Liquids</h3>
</div>

<div class="concept-card">
  <div class="card-label">RULE OF SOLVATION: "LIKE DISSOLVES LIKE"</div>
  <p>A solute dissolves in a solvent when intermolecular attractive forces between solute and solvent are similar:</p>
  <ul>
    <li><strong>Polar Solutes:</strong> Sodium chloride ($\text{NaCl}$) and sugar dissolve readily in polar water, but are insoluble in non-polar benzene.</li>
    <li><strong>Non-Polar Solutes:</strong> Naphthalene and anthracene dissolve readily in non-polar benzene, but do not dissolve in water.</li>
  </ul>
</div>

<div class="concept-card">
  <div class="card-label">DISSOLUTION, CRYSTALLISATION & DYNAMIC EQUILIBRIUM</div>
  <p>When a solid solute is placed into a solvent:</p>
  <ol>
    <li><strong>Dissolution:</strong> Solute dissolves and its concentration in the liquid phase increases.</li>
    <li><strong>Crystallisation:</strong> Dissolved solute particles collide with solid solute and separate out of solution.</li>
    <li><strong>Dynamic Equilibrium:</strong> When rate of dissolution equals rate of crystallisation:
      $$\text{Solute} + \text{Solvent} \rightleftharpoons \text{Solution}$$
    </li>
  </ol>
  <p><strong>Saturated Solution:</strong> A solution in which no more solute can dissolve at that specified temperature and pressure.</p>
  <p><strong>Unsaturated Solution:</strong> A solution where more solute can still be dissolved at that temperature.</p>
</div>

<div class="concept-card">
  <div class="card-label">THERMODYNAMIC GOVERNING FACTORS</div>
  <p><strong>1. Effect of Temperature (Le Chatelier's Principle):</strong></p>
  <ul>
    <li>If dissolution is <strong>endothermic</strong> ($\Delta_{\text{sol}}H > 0$): Solubility <strong>increases</strong> with temperature (e.g. $\text{KNO}_3$).</li>
    <li>If dissolution is <strong>exothermic</strong> ($\Delta_{\text{sol}}H < 0$): Solubility <strong>decreases</strong> with temperature (e.g. $\text{Ce}_2(\text{SO}_4)_3$).</li>
  </ul>
  <p><strong>2. Effect of Pressure:</strong></p>
  <p>Pressure has <strong>no significant effect</strong> on solid solubility in liquids because solids and liquids are highly incompressible.</p>
</div>
"""
    m03_rev = r"""
<div class="revision-sheet">
  <div class="rev-card">
    <h4>SOLID SOLUBILITY HIGHLIGHTS</h4>
    <ul>
      <li>Polar dissolves polar; non-polar dissolves non-polar.</li>
      <li>Equilibrium: Rate of dissolution = Rate of crystallisation.</li>
      <li>Endothermic dissolution ($\Delta H > 0$): Temperature $\uparrow \implies$ Solubility $\uparrow$.</li>
      <li>Exothermic dissolution ($\Delta H < 0$): Temperature $\uparrow \implies$ Solubility $\downarrow$.</li>
      <li>Pressure change has zero practical effect due to incompressibility.</li>
    </ul>
  </div>
</div>
"""
    m03_flashcards = [
        {"q": "What is meant by the rule 'Like Dissolves Like'?", "a": "Polar solutes dissolve in polar solvents (e.g. NaCl in water), while non-polar solutes dissolve in non-polar solvents (e.g. naphthalene in benzene)."},
        {"q": "Differentiate between dissolution and crystallisation.", "a": "Dissolution is the process of solute entering solution; crystallisation is solute particles colliding and separating out of solution."},
        {"q": "How does temperature affect the solubility of a solid undergoing endothermic dissolution?", "a": "According to Le Chatelier's principle, solubility increases with rise in temperature for endothermic dissolution (ΔsolH > 0)."},
        {"q": "Why does pressure have no significant effect on the solubility of solids in liquids?", "a": "Because solids and liquids are highly incompressible and their volumes remain practically unchanged by pressure."},
        {"q": "What defines a saturated solution thermodynamically?", "a": "A solution that is in dynamic equilibrium with undissolved solute, containing the maximum amount of solute at that temperature."}
    ]
    m03_flow = {
        "title": "Solid Dissolution Equilibrium Protocol",
        "steps": [
            {"step": "1. Check Polarity Compatibility", "desc": "Confirm polar-polar or nonpolar-nonpolar interaction ('Like dissolves like')"},
            {"step": "2. Dissolution vs Crystallisation", "desc": "Solute enters solution until rate of dissolution = rate of crystallisation"},
            {"step": "3. Evaluate Enthalpy (ΔH)", "desc": "If $\\Delta_{\\text{sol}}H > 0$, heat increases solubility; if $\\Delta_{\\text{sol}}H < 0$, heat decreases solubility"},
            {"step": "4. Pressure Invariance", "desc": "Ignore pressure variations due to solid/liquid incompressibility"}
        ]
    }
    m03_mindmap = {
        "name": "Solubility of Solids",
        "children": [
            {"name": "Solvation Rule", "children": [{"name": "Polar in Polar (NaCl in H2O)"}, {"name": "Non-polar in Non-polar (Naphthalene in Benzene)"}]},
            {"name": "Equilibrium States", "children": [{"name": "Dissolution vs Crystallisation"}, {"name": "Saturated vs Unsaturated"}]},
            {"name": "Thermodynamics", "children": [{"name": "Endothermic (ΔH > 0, Temp Up = Sol Up)"}, {"name": "Exothermic (ΔH < 0, Temp Up = Sol Down)"}, {"name": "Pressure Invariant"}]}
        ]
    }

    topics.append({
        "id": "chem-sol-03-solid-solubility",
        "subject": "chem",
        "subject_title": "Chemistry • Solutions",
        "title": "03. Solubility of Solids in Liquids",
        "source_file": "Class_12_Chemistry_Solutions_NCERT.pdf",
        "reading_time_min": 6,
        "detailed_html": m03_detailed,
        "toc": [{"id": "sec-03", "title": "03. Solubility of Solids in Liquids"}],
        "revision_html": m03_rev,
        "flashcards": m03_flashcards,
        "flow_data": m03_flow,
        "mindmap_data": m03_mindmap,
        "has_handwritten": False,
        "pages": [{"page_num": 5, "text": "Solubility definition: maximum amount of substance dissolved in solvent at specified temperature."}, {"page_num": 6, "text": "Solubility of a solid in a liquid: like dissolves like. Dissolution and crystallisation. Dynamic equilibrium. Saturated and unsaturated solutions. Effect of temperature (Le Chatelier's principle). Effect of pressure (incompressible)."}]
    })

    # =========================================================================
    # MODULE 04: SOLUBILITY OF GASES & HENRY'S LAW
    # =========================================================================
    m04_detailed = r"""
<div class="topic-header">
  <span class="topic-num">TOPIC 04 OF 13</span>
  <h3 class="topic-title">Solubility of Gases in Liquids & Henry's Law</h3>
</div>

<div class="concept-card">
  <div class="card-label">PISTON COMPRESSION MECHANISM (NCERT FIG 1.1)</div>
  <p>Compressing the gas phase over a liquid increases the <strong>number of gaseous particles per unit volume</strong> and the rate at which gas molecules strike the solution surface, driving more gas into the liquid until a new dynamic equilibrium is established at higher dissolved concentration.</p>
</div>

<div class="formula-card">
  <div class="card-label">HENRY'S LAW FORMULATION</div>
  <p><em>"At constant temperature, the solubility of a gas in a liquid is directly proportional to the partial pressure of the gas present above the surface of the liquid or solution."</em></p>
  <div class="formula-block">
    $$p = K_H \cdot x$$
  </div>
  <p>where $p$ is partial pressure of gas, $x$ is mole fraction in solution, and $K_H$ is <strong>Henry's Law Constant</strong>.</p>
</div>

<div class="concept-card">
  <div class="card-label">PHYSICAL INTERPRETATION OF $K_H$</div>
  <ul>
    <li>At fixed pressure $p$, higher $K_H \implies$ <strong>lower gas solubility</strong> ($x = p / K_H$).</li>
    <li>$K_H$ values for gases ($N_2, O_2$) <strong>increase with temperature</strong>. Hence, gas solubility in liquids <strong>decreases with rise in temperature</strong>.</li>
    <li><strong>Aquatic Habitats:</strong> Cold water contains significantly more dissolved $O_2$ than warm water, explaining why aquatic species thrive in cold waters.</li>
  </ul>
</div>

<div class="concept-card">
  <div class="card-label">CRITICAL REAL-LIFE APPLICATIONS OF HENRY'S LAW</div>
  <ol>
    <li><strong>Carbonated Soft Drinks:</strong> Bottles are sealed under high $\text{CO}_2$ pressure to force high amounts of $\text{CO}_2$ into solution.</li>
    <li><strong>Scuba Divers & The Bends:</strong> At high underwater pressure, nitrogen dissolves in diver's blood. On rapid ascent, pressure falls quickly, forming nitrogen bubbles that block blood capillaries (the painful, deadly condition called <strong>Bends</strong>). To prevent this, scuba tanks are diluted with helium ($11.7\%\text{ He}, 56.2\%\text{ N}_2, 32.1\%\text{ O}_2$).</li>
    <li><strong>High Altitude Climbers & Anoxia:</strong> At high altitude, partial pressure of $O_2$ is low. Low blood oxygen causes weakness and impaired cognition (<strong>Anoxia</strong>).</li>
  </ol>
</div>

<div class="numerical-card">
  <div class="num-header"><span class="num-tag">NCERT EXAMPLE 1.4</span><span class="num-title">Nitrogen Solubility in Water</span></div>
  <p><strong>Problem:</strong> If $N_2$ gas is bubbled through water at $293\text{ K}$, calculate millimoles of $N_2$ dissolved in $1\text{ L}$ water ($p = 0.987\text{ bar}$, $K_H = 76.48\text{ kbar}$).</p>
  <div class="num-step">
    $$x(N_2) = \frac{0.987}{76,480} = 1.29 \times 10^{-5}$$
    $$1\text{ L water} = 55.5\text{ mol} \implies n(N_2) = 1.29 \times 10^{-5} \times 55.5 = 7.16 \times 10^{-4}\text{ mol} = \mathbf{0.716\text{ mmol}}$$
  </div>
  <div class="num-ans"><strong>Final Answer:</strong> $0.716\text{ millimoles}$</div>
</div>
"""
    m04_rev = r"""
<div class="revision-sheet">
  <div class="rev-card">
    <h4>HENRY'S LAW RULES</h4>
    <ul>
      <li>$p = K_H \cdot x$</li>
      <li>Higher $K_H \implies$ Lower solubility.</li>
      <li>Temperature $\uparrow \implies K_H \uparrow \implies$ Solubility $\downarrow$.</li>
      <li>Gas dissolution is exothermic ($\Delta H < 0$), similar to condensation.</li>
      <li>Scuba divers use He-diluted tanks ($11.7\%\text{ He}$) to avoid bends.</li>
      <li>Low $pO_2$ at altitude causes anoxia.</li>
    </ul>
  </div>
</div>
"""
    m04_flashcards = [
        {"q": "State Henry's Law in mathematical form.", "a": "p = KH · x, where p is partial pressure in vapor phase, x is mole fraction in solution, and KH is Henry's law constant."},
        {"q": "Why are aquatic species more comfortable in cold waters than warm waters?", "a": "KH increases with temperature, meaning gas solubility decreases as temperature rises. Cold water holds more dissolved oxygen."},
        {"q": "What medical condition is known as 'the bends' in scuba diving?", "a": "Formation of nitrogen gas bubbles in the blood capillaries when ascending too quickly, blocking blood flow."},
        {"q": "What composition of breathing gas is used in modern scuba tanks to prevent bends?", "a": "Air diluted with helium: 11.7% Helium, 56.2% Nitrogen, and 32.1% Oxygen."},
        {"q": "What is anoxia and what causes it in mountain climbers?", "a": "Low blood oxygen levels caused by low atmospheric partial pressure of oxygen at high altitudes, resulting in weakness and mental confusion."},
        {"q": "Why is dissolution of a gas in a liquid an exothermic process?", "a": "Because gas molecules condense into the liquid state, releasing thermal kinetic energy (ΔsolH < 0)."}
    ]
    m04_flow = {
        "title": "Henry's Law Gas Solubility Workflow",
        "steps": [
            {"step": "1. Identify Gas Partial Pressure", "desc": "Determine $p$ in bar or Pa above the liquid"},
            {"step": "2. Look up KH at Temperature", "desc": "Find Henry's constant $K_H$ in matching pressure units"},
            {"step": "3. Calculate Mole Fraction", "desc": "Compute $x = p / K_H$"},
            {"step": "4. Convert to Moles / Millimoles", "desc": "Multiply by solvent moles ($n = x \\cdot n_{\\text{solvent}}$, where $1\\text{ L H}_2\\text{O} = 55.5\\text{ mol}$)"}
        ]
    }
    m04_mindmap = {
        "name": "Henry's Law & Gas Solubility",
        "children": [
            {"name": "Equation", "children": [{"name": "p = KH · x"}, {"name": "Slope of p vs x plot is KH"}]},
            {"name": "KH Analysis", "children": [{"name": "Higher KH = Lower Solubility"}, {"name": "Temp Up = KH Up = Sol Down"}, {"name": "Cold Water Aquatic Life"}]},
            {"name": "Applications", "children": [{"name": "Soda Bottles (High CO2 P)"}, {"name": "Scuba Bends (11.7% He Dilution)"}, {"name": "High Altitude Anoxia"}]}
        ]
    }

    topics.append({
        "id": "chem-sol-04-henrys-law",
        "subject": "chem",
        "subject_title": "Chemistry • Solutions",
        "title": "04. Solubility of Gases & Henry's Law",
        "source_file": "Class_12_Chemistry_Solutions_NCERT.pdf",
        "reading_time_min": 9,
        "detailed_html": m04_detailed,
        "toc": [{"id": "sec-04", "title": "04. Solubility of Gases & Henry's Law"}],
        "revision_html": m04_rev,
        "flashcards": m04_flashcards,
        "flow_data": m04_flow,
        "mindmap_data": m04_mindmap,
        "has_handwritten": False,
        "pages": [{"page_num": 6, "text": "Solubility of a gas in a liquid: O2 dissolves small extent, HCl high extent."}, {"page_num": 7, "text": "Effect of pressure on gas solubility. Piston model (Fig 1.1). Henry's law: p = KH * x. Plot of p vs x (Fig 1.2). Higher KH means lower solubility. Aquatic species comfortable in cold waters."}, {"page_num": 8, "text": "Table 1.2 KH values. Example 1.4 N2 in water. Applications: soft drinks, scuba divers and bends."}, {"page_num": 9, "text": "Scuba helium dilution. Anoxia at high altitude. Effect of temperature on gas dissolution (exothermic, Le Chatelier). Intext 1.6 and 1.7."}]
    })

    # =========================================================================
    # MODULE 05: VAPOUR PRESSURE & RAOULT'S LAW
    # =========================================================================
    m05_detailed = r"""
<div class="topic-header">
  <span class="topic-num">TOPIC 05 OF 13</span>
  <h3 class="topic-title">Vapour Pressure of Liquid Solutions & Raoult's Law</h3>
</div>

<div class="concept-card">
  <div class="card-label">RAOULT'S LAW FOR VOLATILE LIQUIDS (1886)</div>
  <p><em>"For a solution of volatile liquids, the partial vapour pressure of each component in the solution is directly proportional to its mole fraction present in the solution."</em></p>
  <div class="formula-block">
    $$p_1 = x_1 p_1^\circ \quad \text{and} \quad p_2 = x_2 p_2^\circ$$
  </div>
</div>

<div class="formula-card">
  <div class="card-label">DALTON'S LAW COMBINATION (NCERT EQ 1.16)</div>
  <div class="formula-block">
    $$p_{\text{total}} = p_1 + p_2 = x_1 p_1^\circ + x_2 p_2^\circ = \mathbf{p_1^\circ + (p_2^\circ - p_1^\circ)x_2}$$
  </div>
  <p><strong>Three Key Conclusions:</strong></p>
  <ol>
    <li>Total vapour pressure over solution relates directly to mole fraction of any one component.</li>
    <li>Total vapour pressure varies linearly with mole fraction $x_2$.</li>
    <li>Minimum $p_{\text{total}}$ is $p_1^\circ$ and maximum is $p_2^\circ$ (assuming $p_1^\circ < p_2^\circ$).</li>
  </ol>
</div>

<div class="concept-card">
  <div class="card-label">VAPOUR PHASE COMPOSITION & ENRICHMENT</div>
  <div class="formula-block">
    $$y_1 = \frac{p_1}{p_{\text{total}}}, \qquad y_2 = \frac{p_2}{p_{\text{total}}}$$
  </div>
  <div class="exam-trap-box">
    <strong>⚠️ NCERT VOLATILITY RULE (Page 11):</strong>
    At equilibrium, <strong>the vapour phase is always richer in the component that is more volatile</strong> (i.e. having higher pure vapor pressure $p^\circ$).
  </div>
</div>

<div class="concept-card">
  <div class="card-label">RAOULT'S LAW AS SPECIAL CASE OF HENRY'S LAW</div>
  <p>Comparing $p_1 = x_1 \cdot p_1^\circ$ with $p = x \cdot K_H$: Raoult's Law is a special case of Henry's Law in which $K_H$ becomes equal to $p_1^\circ$.</p>
</div>

<div class="numerical-card">
  <div class="num-header"><span class="num-tag">NCERT EXAMPLE 1.5</span><span class="num-title">CHCl3 + CH2Cl2 Vapour Pressures</span></div>
  <p><strong>Problem:</strong> $p^\circ(\text{CHCl}_3) = 200\text{ mm Hg}, p^\circ(\text{CH}_2\text{Cl}_2) = 415\text{ mm Hg}$. Mixed $25.5\text{ g } \text{CHCl}_3$ and $40\text{ g } \text{CH}_2\text{Cl}_2$.</p>
  <div class="num-step">
    $n(\text{CH}_2\text{Cl}_2) = 0.47\text{ mol}, \ n(\text{CHCl}_3) = 0.213\text{ mol} \implies x(\text{CH}_2\text{Cl}_2) = 0.688, \ x(\text{CHCl}_3) = 0.312$.<br>
    $p_{\text{total}} = 200 + (415 - 200) \times 0.688 = \mathbf{347.9\text{ mm Hg}}$.<br>
    Vapour phase: $y(\text{CH}_2\text{Cl}_2) = \frac{0.688 \times 415}{347.9} = \mathbf{0.82}, \quad y(\text{CHCl}_3) = \mathbf{0.18}$.
  </div>
  <div class="num-ans"><strong>Final Answer:</strong> $p_{\text{total}} = 347.9\text{ mm Hg}$; Vapour richer in $\text{CH}_2\text{Cl}_2$ ($82\%$).</div>
</div>
"""
    m05_rev = r"""
<div class="revision-sheet">
  <div class="rev-card">
    <h4>RAOULT'S LAW EQUATIONS</h4>
    <ul>
      <li>$p_1 = x_1 p_1^\circ, \quad p_2 = x_2 p_2^\circ$</li>
      <li>$p_{\text{total}} = p_1^\circ + (p_2^\circ - p_1^\circ)x_2$</li>
      <li>Vapour mole fractions: $y_1 = p_1 / p_{\text{total}}$</li>
      <li>Vapour phase is always richer in the more volatile component ($p^\circ$ higher).</li>
      <li>Raoult's law is a special case of Henry's law with $K_H = p_1^\circ$.</li>
    </ul>
  </div>
</div>
"""
    m05_flashcards = [
        {"q": "State Raoult's Law for a binary solution of volatile liquids.", "a": "For a solution of volatile liquids, the partial vapour pressure of each component is directly proportional to its mole fraction in solution: p₁ = x₁·p₁°."},
        {"q": "Express total vapour pressure in terms of mole fraction of component 2.", "a": "ptotal = p₁° + (p₂° - p₁°)x₂."},
        {"q": "How is vapour phase composition calculated from partial pressures?", "a": "y₁ = p₁ / ptotal and y₂ = p₂ / ptotal (Dalton's law)."},
        {"q": "Why is the vapour phase richer in dichloromethane than chloroform in Example 1.5?", "a": "Because dichloromethane is more volatile (p° = 415 mm Hg vs 200 mm Hg for chloroform)."},
        {"q": "How is Raoult's law a special case of Henry's law?", "a": "Both state p ∝ x. In Raoult's law the proportionality constant is p₁°, whereas in Henry's law it is KH. When KH = p₁°, Henry's law becomes Raoult's law."},
        {"q": "What is the graphical shape of ptotal vs x₂ for an ideal solution?", "a": "A straight linear line passing from p₁° to p₂° (NCERT Fig 1.3)."}
    ]
    m05_flow = {
        "title": "Raoult's Law Vapour Pressure Protocol",
        "steps": [
            {"step": "1. Calculate Liquid Mole Fractions", "desc": "Find $n_1, n_2$ and compute $x_1 = n_1 / (n_1 + n_2), x_2 = 1 - x_1$"},
            {"step": "2. Calculate Partial Pressures", "desc": "Compute $p_1 = x_1 p_1^\\circ$ and $p_2 = x_2 p_2^\\circ$"},
            {"step": "3. Sum for Total Pressure", "desc": "$p_{\\text{total}} = p_1 + p_2$"},
            {"step": "4. Calculate Vapour Composition", "desc": "Determine $y_1 = p_1 / p_{\\text{total}}$ and $y_2 = p_2 / p_{\\text{total}}$"}
        ]
    }
    m05_mindmap = {
        "name": "Vapour Pressure & Raoult's Law",
        "children": [
            {"name": "Formulas", "children": [{"name": "p1 = x1 · p1°"}, {"name": "ptotal = p1° + (p2° - p1°)x2"}]},
            {"name": "Vapour Phase", "children": [{"name": "y1 = p1 / ptotal"}, {"name": "Richer in More Volatile"}]},
            {"name": "Special Case", "children": [{"name": "Henry's Law with KH = p1°"}]}
        ]
    }

    topics.append({
        "id": "chem-sol-05-raoults-law",
        "subject": "chem",
        "subject_title": "Chemistry • Solutions",
        "title": "05. Vapour Pressure & Raoult's Law",
        "source_file": "Class_12_Chemistry_Solutions_NCERT.pdf",
        "reading_time_min": 8,
        "detailed_html": m05_detailed,
        "toc": [{"id": "sec-05", "title": "05. Vapour Pressure & Raoult's Law"}],
        "revision_html": m05_rev,
        "flashcards": m05_flashcards,
        "flow_data": m05_flow,
        "mindmap_data": m05_mindmap,
        "has_handwritten": False,
        "pages": [{"page_num": 9, "text": "Vapour pressure of liquid solutions. Binary volatile liquids. Raoult's law statement."}, {"page_num": 10, "text": "Equations 1.12 to 1.16. Dalton's law total vapour pressure. Three conclusions. Fig 1.3 plot. Vapour phase composition y1, y2."}, {"page_num": 11, "text": "Example 1.5 chloroform and dichloromethane. Vapour phase richer in more volatile component."}, {"page_num": 12, "text": "Raoult's law as special case of Henry's law: KH = p1°."}]
    })

    # Return all 5 initial modules and proceed to add 6 to 13
    return _build_remaining_modules(topics)


def _build_remaining_modules(topics: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    # =========================================================================
    # MODULE 06: IDEAL & NON-IDEAL SOLUTIONS
    # =========================================================================
    m06_detailed = r"""
<div class="topic-header">
  <span class="topic-num">TOPIC 06 OF 13</span>
  <h3 class="topic-title">Ideal & Non-Ideal Solutions (Deviations)</h3>
</div>

<div class="concept-card">
  <div class="card-label">IDEAL SOLUTIONS CRITERIA</div>
  <p>Solutions that obey Raoult's Law across the entire range of concentration:</p>
  <ul>
    <li>$\Delta_{\text{mix}}H = 0$ (no heat evolved or absorbed on mixing).</li>
    <li>$\Delta_{\text{mix}}V = 0$ (total volume equals exact sum of component volumes).</li>
    <li>Intermolecular forces: $A\text{--}A \approx B\text{--}B \approx A\text{--}B$.</li>
    <li><em>Examples:</em> $n$-hexane + $n$-heptane, bromoethane + chloroethane, benzene + toluene.</li>
  </ul>
</div>

<div class="comparison-card">
  <div class="card-label">POSITIVE VS NEGATIVE DEVIATION FROM RAOULT'S LAW</div>
  <table class="notes-table">
    <thead>
      <tr><th>Property</th><th>Positive Deviation</th><th>Negative Deviation</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>Vapour Pressure</strong></td><td>$p_{\text{total}} > \text{Raoult's prediction}$</td><td>$p_{\text{total}} < \text{Raoult's prediction}$</td></tr>
      <tr><td><strong>Intermolecular Forces</strong></td><td>$A\text{--}B$ forces <strong>weaker</strong> than $A\text{--}A, B\text{--}B$</td><td>$A\text{--}B$ forces <strong>stronger</strong> than $A\text{--}A, B\text{--}B$</td></tr>
      <tr><td><strong>Escaping Tendency</strong></td><td>Increased; molecules escape easily</td><td>Decreased; molecules held tighter</td></tr>
      <tr><td><strong>$\Delta_{\text{mix}}H$</strong></td><td>$\mathbf{\Delta H > 0}$ (Endothermic)</td><td>$\mathbf{\Delta H < 0}$ (Exothermic)</td></tr>
      <tr><td><strong>$\Delta_{\text{mix}}V$</strong></td><td>$\mathbf{\Delta V > 0}$ (Expansion)</td><td>$\mathbf{\Delta V < 0}$ (Contraction)</td></tr>
      <tr><td><strong>Azeotrope</strong></td><td><strong>Minimum Boiling Azeotrope</strong></td><td><strong>Maximum Boiling Azeotrope</strong></td></tr>
      <tr><td><strong>NCERT Examples</strong></td><td>• Ethanol + Acetone<br>• $\text{CS}_2$ + Acetone</td><td>• Phenol + Aniline<br>• Chloroform + Acetone (H-bonding)</td></tr>
    </tbody>
  </table>
</div>

<div class="concept-card">
  <div class="card-label">MOLECULAR MECHANISMS (NCERT PAGE 14)</div>
  <p><strong>Chloroform + Acetone (Negative Deviation):</strong> Chloroform forms a new intermolecular hydrogen bond with the carbonyl oxygen of acetone ($(\text{CH}_3)_2\text{C}=\text{O}\cdots\text{H--CCl}_3$), reducing escaping tendency and lowering vapour pressure.</p>
  <p><strong>Ethanol + Acetone (Positive Deviation):</strong> Acetone molecules insert between hydrogen-bonded ethanol molecules, breaking H-bonds and increasing vapor pressure.</p>
</div>
"""
    m06_rev = r"""
<div class="revision-sheet">
  <div class="rev-card">
    <h4>IDEAL VS NON-IDEAL CHEAT SHEET</h4>
    <ul>
      <li>Ideal: $\Delta H = 0, \Delta V = 0, F_{AB} \approx F_{AA}$.</li>
      <li>Positive Deviation: $\Delta H > 0, \Delta V > 0, F_{AB} < F_{AA}$. (Ethanol + Acetone).</li>
      <li>Negative Deviation: $\Delta H < 0, \Delta V < 0, F_{AB} > F_{AA}$. (Chloroform + Acetone).</li>
    </ul>
  </div>
</div>
"""
    m06_flashcards = [
        {"q": "What thermodynamic conditions define an ideal solution?", "a": "ΔmixH = 0, ΔmixV = 0, and obedience to Raoult's law over all concentrations."},
        {"q": "Why does ethanol + acetone show positive deviation from Raoult's law?", "a": "Acetone gets between ethanol molecules and breaks their hydrogen bonds, weakening intermolecular forces."},
        {"q": "Why does chloroform + acetone show negative deviation from Raoult's law?", "a": "Chloroform forms an intermolecular hydrogen bond with the carbonyl oxygen of acetone, strengthening forces and lowering vapor pressure."},
        {"q": "Give two authentic NCERT examples of nearly ideal solutions.", "a": "1. n-hexane and n-heptane; 2. bromoethane and chloroethane; 3. benzene and toluene."},
        {"q": "What are the signs of ΔmixH and ΔmixV for negative deviation?", "a": "Both are negative: ΔmixH < 0 and ΔmixV < 0 (exothermic mixing with volume contraction)."},
        {"q": "What type of azeotrope is formed by solutions with large positive deviation?", "a": "Minimum boiling azeotrope."}
    ]
    m06_flow = {
        "title": "Deviation Classification Protocol",
        "steps": [
            {"step": "1. Compare Intermolecular Forces", "desc": "Check if A-B attractive forces are equal to, weaker than, or stronger than A-A/B-B"},
            {"step": "2. Assign Ideality", "desc": "If equal: Ideal ($\\Delta H=0, \\Delta V=0$). If weaker: Positive. If stronger: Negative"},
            {"step": "3. Determine Vapor Pressure Trend", "desc": "Positive = higher $p_{\\text{total}}$; Negative = lower $p_{\\text{total}}$"},
            {"step": "4. Predict Azeotrope Type", "desc": "Positive $\\implies$ Minimum Boiling; Negative $\\implies$ Maximum Boiling"}
        ]
    }
    m06_mindmap = {
        "name": "Ideal & Non-Ideal Solutions",
        "children": [
            {"name": "Ideal (ΔH=0, ΔV=0)", "children": [{"name": "n-Hexane + Heptane"}, {"name": "Benzene + Toluene"}]},
            {"name": "Positive Deviation", "children": [{"name": "ΔH > 0, ΔV > 0"}, {"name": "Weaker A-B Forces"}, {"name": "Ethanol + Acetone"}, {"name": "Min Boiling Azeotrope"}]},
            {"name": "Negative Deviation", "children": [{"name": "ΔH < 0, ΔV < 0"}, {"name": "Stronger A-B Forces (H-Bond)"}, {"name": "Chloroform + Acetone"}, {"name": "Max Boiling Azeotrope"}]}
        ]
    }

    topics.append({
        "id": "chem-sol-06-ideal-nonideal",
        "subject": "chem",
        "subject_title": "Chemistry • Solutions",
        "title": "06. Ideal & Non-Ideal Solutions",
        "source_file": "Class_12_Chemistry_Solutions_NCERT.pdf",
        "reading_time_min": 8,
        "detailed_html": m06_detailed,
        "toc": [{"id": "sec-06", "title": "06. Ideal & Non-Ideal Solutions"}],
        "revision_html": m06_rev,
        "flashcards": m06_flashcards,
        "flow_data": m06_flow,
        "mindmap_data": m06_mindmap,
        "has_handwritten": False,
        "pages": [{"page_num": 13, "text": "Ideal solutions: obey Raoult's law. DmixH = 0, DmixV = 0. Molecular forces A-A ≈ B-B ≈ A-B. Examples: n-hexane+heptane, benzene+toluene. Non-ideal solutions."}, {"page_num": 14, "text": "Deviations from Raoult's law. Positive deviation (ethanol+acetone, CS2+acetone). Negative deviation (phenol+aniline, chloroform+acetone H-bonding). Fig 1.6 curves."}]
    })

    # =========================================================================
    # MODULE 07: AZEOTROPES
    # =========================================================================
    m07_detailed = r"""
<div class="topic-header">
  <span class="topic-num">TOPIC 07 OF 13</span>
  <h3 class="topic-title">Azeotropes & Fractional Distillation</h3>
</div>

<div class="concept-card">
  <div class="card-label">AZEOTROPE DEFINITION</div>
  <p><strong>Azeotropes</strong> are binary mixtures having the <strong>same composition in both liquid and vapour phase</strong> and <strong>boil at a constant temperature</strong>.</p>
  <p>Because vapor and liquid compositions are identical ($y_1 = x_1$ and $y_2 = x_2$), <strong>components cannot be separated by fractional distillation</strong>.</p>
</div>

<div class="comparison-card">
  <div class="card-label">TWO TYPES OF AZEOTROPES</div>
  <table class="notes-table">
    <thead>
      <tr><th>Type</th><th>Deviation Origin</th><th>Boiling Behavior</th><th>Authentic NCERT Example</th></tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Minimum Boiling Azeotrope</strong></td>
        <td>Large positive deviation from Raoult's law</td>
        <td>Boils at temperature <em>lower</em> than either component</td>
        <td><strong>Ethanol-Water:</strong> $95\%$ ethanol by volume (azeotropic point reached in sugar fermentation).</td>
      </tr>
      <tr>
        <td><strong>Maximum Boiling Azeotrope</strong></td>
        <td>Large negative deviation from Raoult's law</td>
        <td>Boils at temperature <em>higher</em> than either component</td>
        <td><strong>Nitric Acid-Water:</strong> $68\%\text{ HNO}_3 + 32\%\text{ H}_2\text{O}$ by mass, boiling at $\mathbf{393.5\text{ K}}$.</td>
      </tr>
    </tbody>
  </table>
</div>
"""
    m07_rev = r"""
<div class="revision-sheet">
  <div class="rev-card">
    <h4>AZEOTROPES SUMMARY</h4>
    <ul>
      <li>Liquid and vapour compositions are identical.</li>
      <li>Cannot be separated by fractional distillation.</li>
      <li>Minimum Boiling: Positive deviation ($95\%$ ethanol).</li>
      <li>Maximum Boiling: Negative deviation ($68\% \text{ HNO}_3$, b.p. $393.5\text{ K}$).</li>
    </ul>
  </div>
</div>
"""
    m07_flashcards = [
        {"q": "What is an azeotrope?", "a": "A binary mixture that has the same composition in liquid and vapour phases and boils at a constant temperature."},
        {"q": "Why cannot an azeotrope be separated by fractional distillation?", "a": "Because liquid and vapor have identical compositions (y = x), boiling produces vapor with the exact same ratio."},
        {"q": "What type of deviation produces a minimum boiling azeotrope?", "a": "Large positive deviation from Raoult's law."},
        {"q": "Give the composition of the ethanol-water azeotrope.", "a": "Approximately 95% by volume of ethanol."},
        {"q": "Give the composition and boiling point of the nitric acid-water azeotrope.", "a": "68% nitric acid and 32% water by mass, boiling at 393.5 K (maximum boiling azeotrope)."}
    ]
    m07_flow = {
        "title": "Azeotropic Distillation Barrier",
        "steps": [
            {"step": "1. Fractional Distillation Progression", "desc": "Boiling enriches vapour in the more volatile component"},
            {"step": "2. Reaching Azeotropic Composition", "desc": "At specific composition, vapour pressure curve reaches extremum"},
            {"step": "3. Composition Equalization", "desc": "$x_{\\text{liquid}} = y_{\\text{vapour}}$"},
            {"step": "4. Distillation Cessation", "desc": "No further separation can occur at this pressure"}
        ]
    }
    m07_mindmap = {
        "name": "Azeotropes",
        "children": [
            {"name": "Characteristics", "children": [{"name": "Constant Boiling"}, {"name": "Identical Liquid/Vapour Ratio"}, {"name": "No Fractional Distillation"}]},
            {"name": "Minimum Boiling", "children": [{"name": "Large Positive Deviation"}, {"name": "95% Ethanol + 5% Water"}]},
            {"name": "Maximum Boiling", "children": [{"name": "Large Negative Deviation"}, {"name": "68% HNO3 + 32% Water (393.5 K)"}]}
        ]
    }

    topics.append({
        "id": "chem-sol-07-azeotropes",
        "subject": "chem",
        "subject_title": "Chemistry • Solutions",
        "title": "07. Azeotropes & Fractional Distillation",
        "source_file": "Class_12_Chemistry_Solutions_NCERT.pdf",
        "reading_time_min": 6,
        "detailed_html": m07_detailed,
        "toc": [{"id": "sec-07", "title": "07. Azeotropes & Fractional Distillation"}],
        "revision_html": m07_rev,
        "flashcards": m07_flashcards,
        "flow_data": m07_flow,
        "mindmap_data": m07_mindmap,
        "has_handwritten": False,
        "pages": [{"page_num": 14, "text": "Azeotropes: binary mixtures boiling at constant temperature. Minimum boiling azeotrope (large positive deviation)."}, {"page_num": 15, "text": "Ethanol-water 95%. Maximum boiling azeotrope: nitric acid and water (68% HNO3, b.p. 393.5 K). Intext 1.8."}]
    })

    # =========================================================================
    # MODULE 08: COLLIGATIVE PROPERTIES: RLVP & BOILING ELEVATION
    # =========================================================================
    m08_detailed = r"""
<div class="topic-header">
  <span class="topic-num">TOPIC 08 OF 13</span>
  <h3 class="topic-title">Colligative Properties: RLVP & Boiling Point Elevation</h3>
</div>

<div class="concept-card">
  <div class="card-label">COLLIGATIVE NATURE (LATIN: CO + LIGARE)</div>
  <p>Properties that depend strictly on the <strong>number of solute particles</strong> relative to total particles, regardless of chemical identity.</p>
</div>

<!-- 1. RLVP -->
<div class="formula-card">
  <div class="card-label">1. RELATIVE LOWERING OF VAPOUR PRESSURE (RLVP)</div>
  <div class="formula-block">
    $$\frac{p_1^\circ - p_1}{p_1^\circ} = x_2 = \frac{n_2}{n_1 + n_2} \approx \mathbf{\frac{w_2 \times M_1}{M_2 \times w_1}} \implies \mathbf{M_2 = \frac{w_2 \times M_1 \times p_1^\circ}{(p_1^\circ - p_1)w_1}}$$
  </div>
  <p><em>Example 1.6:</em> $0.5\text{ g solute}$ in $39\text{ g benzene } (M_1=78)$ drops VP from $0.850$ to $0.845\text{ bar} \implies \mathbf{M_2 = 170\text{ g mol}^{-1}}$.</p>
</div>

<!-- 2. Boiling Elevation -->
<div class="formula-card">
  <div class="card-label">2. ELEVATION OF BOILING POINT ($\Delta T_b$)</div>
  <p>Liquid boils when vapor pressure equals atmospheric pressure ($1.013\text{ bar}$). Non-volatile solute lowers vapor pressure; therefore higher temperature is required (Fig 1.7).</p>
  <div class="formula-block">
    $$\Delta T_b = T_b - T_b^\circ = K_b \cdot m = \mathbf{\frac{K_b \times 1000 \times w_2}{M_2 \times w_1}} \implies \mathbf{M_2 = \frac{1000 \times w_2 \times K_b}{\Delta T_b \times w_1}}$$
  </div>
  <p><strong>$K_b$:</strong> Molal Elevation Constant or <strong>Ebullioscopic Constant</strong> ($\text{K kg mol}^{-1}$). For water: $K_b = 0.52\text{ K kg mol}^{-1}$.</p>
</div>

<div class="numerical-card">
  <div class="num-header"><span class="num-tag">NCERT EXAMPLE 1.7</span><span class="num-title">Boiling Point of Glucose Solution</span></div>
  <p><strong>Problem:</strong> $18\text{ g}$ glucose in $1\text{ kg}$ water ($K_b = 0.52$). At what temp will water boil?</p>
  <div class="num-step">
    $m = 18/180 = 0.1\text{ mol kg}^{-1} \implies \Delta T_b = 0.52 \times 0.1 = 0.052\text{ K}$.<br>
    $T_b = 373.15 + 0.052 = \mathbf{373.202\text{ K}}$.
  </div>
  <div class="num-ans"><strong>Final Answer:</strong> $373.202\text{ K}$</div>
</div>

<div class="numerical-card">
  <div class="num-header"><span class="num-tag">NCERT EXAMPLE 1.8</span><span class="num-title">Molar Mass from Boiling Elevation</span></div>
  <p><strong>Problem:</strong> $1.80\text{ g}$ solute in $90\text{ g}$ benzene raises b.p. from $353.23$ to $354.11\text{ K}$ ($K_b = 2.53$).</p>
  <div class="num-step">
    $\Delta T_b = 354.11 - 353.23 = 0.88\text{ K}$.<br>
    $M_2 = \frac{2.53 \times 1.80 \times 1000}{0.88 \times 90} = \mathbf{58\text{ g mol}^{-1}}$.
  </div>
  <div class="num-ans"><strong>Final Answer:</strong> $M_2 = 58\text{ g mol}^{-1}$</div>
</div>
"""
    m08_rev = r"""
<div class="revision-sheet">
  <div class="rev-card">
    <h4>RLVP & BOILING ELEVATION CHEAT SHEET</h4>
    <ul>
      <li>$\frac{\Delta p}{p_1^\circ} = x_2 \approx \frac{w_2 M_1}{M_2 w_1}$</li>
      <li>$\Delta T_b = K_b \cdot m = \frac{1000 w_2 K_b}{M_2 w_1}$</li>
      <li>$K_b$ for water $= 0.52\text{ K kg mol}^{-1}$. Benzene $= 2.53\text{ K kg mol}^{-1}$.</li>
      <li>Thermodynamic: $K_b = \frac{R M_1 T_b^2}{1000 \Delta_{\text{vap}}H}$.</li>
    </ul>
  </div>
</div>
"""
    m08_flashcards = [
        {"q": "What is the physical meaning of colligative properties?", "a": "Properties that depend solely on the number of solute particles, not on their chemical identity."},
        {"q": "State the formula for Relative Lowering of Vapour Pressure for dilute solutions.", "a": "(p₁° - p₁) / p₁° = x₂ ≈ (w₂ · M₁) / (M₂ · w₁)."},
        {"q": "Define the ebullioscopic constant (Kb).", "a": "The boiling point elevation produced when 1 mole of solute is dissolved in 1 kg of solvent (molal elevation constant). Unit: K kg mol⁻¹."},
        {"q": "What is the Kb value of water?", "a": "0.52 K kg mol⁻¹."},
        {"q": "Why does the boiling point of a solvent increase upon adding a non-volatile solute?", "a": "Because solute particles block surface area, lowering vapor pressure. The solution must reach a higher temperature for its vapor pressure to equal atmospheric pressure."},
        {"q": "State the thermodynamic equation relating Kb to enthalpy of vaporization.", "a": "Kb = (R · M₁ · Tb²) / (1000 · ΔvapH)."}
    ]
    m08_flow = {
        "title": "Molar Mass via Boiling Point Elevation",
        "steps": [
            {"step": "1. Measure Elevation (ΔTb)", "desc": "$\Delta T_b = T_b(\text{solution}) - T_b^\circ(\text{solvent})$"},
            {"step": "2. Look up Solvent Kb", "desc": "e.g. Water = $0.52$, Benzene = $2.53\\text{ K kg mol}^{-1}$"},
            {"step": "3. Calculate Molality", "desc": "$m = \\Delta T_b / K_b$"},
            {"step": "4. Compute Molar Mass", "desc": "$M_2 = \\frac{1000 \\cdot w_2 \\cdot K_b}{\\Delta T_b \\cdot w_1}$"}
        ]
    }
    m08_mindmap = {
        "name": "RLVP & Boiling Elevation",
        "children": [
            {"name": "Colligative Principle", "children": [{"name": "Depends on particle number"}, {"name": "Independent of identity"}]},
            {"name": "RLVP", "children": [{"name": "(p1° - p1) / p1° = x2"}, {"name": "M2 = (w2 M1 p1°) / (Δp w1)"}]},
            {"name": "Boiling Elevation", "children": [{"name": "ΔTb = Kb · m"}, {"name": "Ebullioscopic Constant Kb"}, {"name": "Kb = R M1 Tb² / (1000 ΔvapH)"}]}
        ]
    }

    topics.append({
        "id": "chem-sol-08-rlvp-boiling",
        "subject": "chem",
        "subject_title": "Chemistry • Solutions",
        "title": "08. Colligative: RLVP & Boiling Elevation",
        "source_file": "Class_12_Chemistry_Solutions_NCERT.pdf",
        "reading_time_min": 9,
        "detailed_html": m08_detailed,
        "toc": [{"id": "sec-08", "title": "08. Colligative: RLVP & Boiling Elevation"}],
        "revision_html": m08_rev,
        "flashcards": m08_flashcards,
        "flow_data": m08_flow,
        "mindmap_data": m08_mindmap,
        "has_handwritten": False,
        "pages": [{"page_num": 15, "text": "Colligative properties definition. Relative lowering of vapour pressure equation 1.25."}, {"page_num": 16, "text": "Equation 1.28 for M2. Example 1.6. Elevation of boiling point definition and Fig 1.7."}, {"page_num": 17, "text": "Delta Tb = Kb * m. Ebullioscopic constant. Example 1.7 glucose boiling point."}, {"page_num": 18, "text": "Example 1.8 molar mass of solute in benzene."}]
    })

    # =========================================================================
    # MODULE 09: FREEZING POINT DEPRESSION
    # =========================================================================
    m09_detailed = r"""
<div class="topic-header">
  <span class="topic-num">TOPIC 09 OF 13</span>
  <h3 class="topic-title">Colligative Properties: Freezing Point Depression</h3>
</div>

<div class="concept-card">
  <div class="card-label">FREEZING POINT DEFINITION (NCERT FIG 1.8)</div>
  <p>Freezing point is the temperature at which the <strong>vapour pressure of the substance in its liquid phase equals the vapour pressure in its solid phase</strong>.</p>
  <p>Adding a non-volatile solute lowers liquid vapor pressure, forcing it to intersect the solid curve at a lower temperature ($\Delta T_f$).</p>
</div>

<div class="formula-card">
  <div class="card-label">CRYOSCOPIC EQUATIONS</div>
  <div class="formula-block">
    $$\Delta T_f = T_f^\circ - T_f = K_f \cdot m = \mathbf{\frac{K_f \times 1000 \times w_2}{M_2 \times w_1}} \implies \mathbf{M_2 = \frac{1000 \times w_2 \times K_f}{\Delta T_f \times w_1}}$$
  </div>
  <p><strong>$K_f$:</strong> Molal Freezing Point Depression Constant or <strong>Cryoscopic Constant</strong> ($\text{K kg mol}^{-1}$).</p>
</div>

<div class="concept-card">
  <div class="card-label">THERMODYNAMIC FORMULAS (NCERT EQS 1.37 & 1.38)</div>
  <div class="formula-block">
    $$K_f = \frac{R \cdot M_1 \cdot T_f^2}{1000 \cdot \Delta_{\text{fus}}H}, \qquad K_b = \frac{R \cdot M_1 \cdot T_b^2}{1000 \cdot \Delta_{\text{vap}}H}$$
  </div>
</div>

<div class="table-container">
  <div class="table-caption">NCERT Table 1.3: Cryoscopic and Ebullioscopic Constants</div>
  <table class="notes-table">
    <thead>
      <tr><th>Solvent</th><th>b.p. (K)</th><th>$K_b$ (K kg mol⁻¹)</th><th>f.p. (K)</th><th>$K_f$ (K kg mol⁻¹)</th></tr>
    </thead>
    <tbody>
      <tr><td>Water</td><td>373.15</td><td>0.52</td><td>273.0</td><td>1.86</td></tr>
      <tr><td>Ethanol</td><td>351.5</td><td>1.20</td><td>155.7</td><td>1.99</td></tr>
      <tr><td>Cyclohexane</td><td>353.74</td><td>2.79</td><td>279.55</td><td>20.00</td></tr>
      <tr><td>Benzene</td><td>353.3</td><td>2.53</td><td>278.6</td><td>5.12</td></tr>
      <tr><td>Chloroform</td><td>334.4</td><td>3.63</td><td>209.6</td><td>4.79</td></tr>
      <tr><td>$\text{CCl}_4$</td><td>350.0</td><td>5.03</td><td>250.5</td><td>31.8</td></tr>
      <tr><td>$\text{CS}_2$</td><td>319.4</td><td>2.34</td><td>164.2</td><td>3.83</td></tr>
      <tr><td>Diethyl ether</td><td>307.8</td><td>2.02</td><td>156.9</td><td>1.79</td></tr>
      <tr><td>Acetic acid</td><td>391.1</td><td>2.93</td><td>290.0</td><td>3.90</td></tr>
    </tbody>
  </table>
</div>

<div class="numerical-card">
  <div class="num-header"><span class="num-tag">NCERT EXAMPLE 1.9</span><span class="num-title">Freezing Point Depression of Antifreeze</span></div>
  <p><strong>Problem:</strong> $45\text{ g}$ ethylene glycol in $600\text{ g}$ water ($K_f = 1.86$). Calculate $\Delta T_f$ and freezing point.</p>
  <div class="num-step">
    $m = \frac{45/62}{0.60} = 1.2\text{ mol kg}^{-1} \implies \Delta T_f = 1.86 \times 1.2 = \mathbf{2.2\text{ K}}$.<br>
    $T_f = 273.15 - 2.2 = \mathbf{270.95\text{ K}} \ (-2.2^\circ\text{C})$.
  </div>
  <div class="num-ans"><strong>Final Answer:</strong> $\Delta T_f = 2.2\text{ K}, \quad T_f = 270.95\text{ K}$</div>
</div>

<div class="numerical-card">
  <div class="num-header"><span class="num-tag">NCERT EXAMPLE 1.10</span><span class="num-title">Molar Mass from Freezing Depression</span></div>
  <p><strong>Problem:</strong> $1.00\text{ g}$ solute in $50\text{ g}$ benzene lowers f.p. by $0.40\text{ K}$ ($K_f = 5.12$).</p>
  <div class="num-step">
    $$M_2 = \frac{5.12 \times 1.00 \times 1000}{0.40 \times 50} = \mathbf{256\text{ g mol}^{-1}}$$
  </div>
  <div class="num-ans"><strong>Final Answer:</strong> $M_2 = 256\text{ g mol}^{-1}$</div>
</div>
"""
    m09_rev = r"""
<div class="revision-sheet">
  <div class="rev-card">
    <h4>FREEZING DEPRESSION RULES</h4>
    <ul>
      <li>$\Delta T_f = T_f^\circ - T_f = K_f \cdot m = \frac{1000 w_2 K_f}{M_2 w_1}$</li>
      <li>$K_f$ for water $= 1.86\text{ K kg mol}^{-1}$. Benzene $= 5.12\text{ K kg mol}^{-1}$.</li>
      <li>$K_f = \frac{R M_1 T_f^2}{1000 \Delta_{\text{fus}}H}$.</li>
      <li>Cyclohexane ($K_f = 20.00$) and $\text{CCl}_4$ ($K_f = 31.8$) have extremely high $K_f$ values.</li>
    </ul>
  </div>
</div>
"""
    m09_flashcards = [
        {"q": "Define the freezing point of a substance.", "a": "The temperature at which the vapour pressure of the substance in its liquid phase equals its vapour pressure in the solid phase."},
        {"q": "What is the Cryoscopic Constant (Kf)?", "a": "The depression in freezing point produced when 1 mole of solute is dissolved in 1000 g (1 kg) of solvent."},
        {"q": "What is the Kf of pure water?", "a": "1.86 K kg mol⁻¹."},
        {"q": "Why is ethylene glycol added to radiator water in cold climates?", "a": "It depresses the freezing point of water (down to -17.6°C at 35% v/v), preventing radiator water from freezing and cracking the engine."},
        {"q": "State the thermodynamic equation relating Kf to enthalpy of fusion.", "a": "Kf = (R · M₁ · Tf²) / (1000 · ΔfusH)."},
        {"q": "Which solvent listed in NCERT has the highest Kf value?", "a": "Carbon tetrachloride (CCl₄) with Kf = 31.8 K kg mol⁻¹ (and Cyclohexane with 20.00 K kg mol⁻¹)."}
    ]
    m09_flow = {
        "title": "Cryoscopy Molar Mass Protocol",
        "steps": [
            {"step": "1. Record Depression", "desc": "$\\Delta T_f = T_f^\\circ - T_f$"},
            {"step": "2. Look up Solvent Kf", "desc": "Water = $1.86$, Benzene = $5.12\\text{ K kg mol}^{-1}$"},
            {"step": "3. Substitute Mass Values", "desc": "$M_2 = \\frac{1000 \\cdot w_2 \\cdot K_f}{\\Delta T_f \\cdot w_1}$"},
            {"step": "4. Verify Ionization/Association", "desc": "Check if solute dissociates ($i > 1$) or associates ($i < 1$)"}
        ]
    }
    m09_mindmap = {
        "name": "Freezing Point Depression",
        "children": [
            {"name": "Equilibrium", "children": [{"name": "Liquid VP = Solid VP"}, {"name": "Non-volatile solute depresses VP"}]},
            {"name": "Equation", "children": [{"name": "ΔTf = Kf · m"}, {"name": "Kf = R M1 Tf² / (1000 ΔfusH)"}]},
            {"name": "Calculations", "children": [{"name": "Antifreeze (Ex 1.9)"}, {"name": "Molar Mass (Ex 1.10)"}]}
        ]
    }

    topics.append({
        "id": "chem-sol-09-freezing-depression",
        "subject": "chem",
        "subject_title": "Chemistry • Solutions",
        "title": "09. Colligative: Freezing Depression",
        "source_file": "Class_12_Chemistry_Solutions_NCERT.pdf",
        "reading_time_min": 8,
        "detailed_html": m09_detailed,
        "toc": [{"id": "sec-09", "title": "09. Colligative: Freezing Depression"}],
        "revision_html": m09_rev,
        "flashcards": m09_flashcards,
        "flow_data": m09_flow,
        "mindmap_data": m09_mindmap,
        "has_handwritten": False,
        "pages": [{"page_num": 18, "text": "Depression of freezing point. Definition of freezing point and Fig 1.8. Delta Tf = Kf * m. Cryoscopic constant."}, {"page_num": 19, "text": "Equations 1.35 and 1.36. Equations 1.37 and 1.38 for Kf and Kb. Table 1.3 constants for 9 solvents."}, {"page_num": 20, "text": "Example 1.9 ethylene glycol freezing point. Example 1.10 molar mass in benzene."}]
    })

    # =========================================================================
    # MODULE 10: OSMOSIS & REVERSE OSMOSIS
    # =========================================================================
    m10_detailed = r"""
<div class="topic-header">
  <span class="topic-num">TOPIC 10 OF 13</span>
  <h3 class="topic-title">Osmosis, Osmotic Pressure & Reverse Osmosis</h3>
</div>

<div class="concept-card">
  <div class="card-label">SPM & OSMOSIS MECHANISM</div>
  <p><strong>Semipermeable Membrane (SPM):</strong> Thin film with submicroscopic pores allowing small solvent molecules to pass while blocking larger solute molecules (natural: pig's bladder, parchment; synthetic: cellophane).</p>
  <p><strong>Osmosis:</strong> Spontaneous net movement of solvent molecules from pure solvent (or dilute solution) to concentrated solution across an SPM.</p>
</div>

<div class="formula-card">
  <div class="card-label">OSMOTIC PRESSURE ($\Pi$)</div>
  <p><em>"Excess hydrostatic pressure applied on the solution side to stop osmosis across an SPM."</em></p>
  <div class="formula-block">
    $$\Pi = C R T = \left(\frac{n_2}{V}\right) R T = \frac{w_2 R T}{M_2 V} \implies \mathbf{M_2 = \frac{w_2 R T}{\Pi V}}$$
  </div>
  <p>where $R = 0.083\text{ L bar mol}^{-1}\text{ K}^{-1}$ ($8.314\text{ J K}^{-1}\text{ mol}^{-1}$), $V$ in Litres.</p>
</div>

<div class="concept-card">
  <div class="card-label">ADVANTAGES FOR BIOMOLECULES (NCERT PAGE 22)</div>
  <ol>
    <li>Measured at ambient room temperature (proteins decompose at boiling point).</li>
    <li>Uses molarity instead of molality.</li>
    <li>Produces large, readily measurable pressures even at $10^{-3}\text{ M}$ ($~20\text{ mm Hg}$ vs undetectably small $\Delta T_b \approx 0.0005\text{ K}$).</li>
  </ol>
</div>

<div class="comparison-card">
  <div class="card-label">TONICITY: ISOTONIC, HYPERTONIC, HYPOTONIC</div>
  <table class="notes-table">
    <thead>
      <tr><th>Type</th><th>$\Pi$ vs Blood Cell ($0.9\%\text{ NaCl}$)</th><th>Water Flow</th><th>Cell State</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>Isotonic</strong></td><td>$\Pi_{\text{ext}} = \Pi_{\text{cell}}$</td><td>No net flow</td><td>Normal shape (Normal Saline safe for IV)</td></tr>
      <tr><td><strong>Hypertonic</strong></td><td>$\Pi_{\text{ext}} > \Pi_{\text{cell}}$ ($> 0.9\%$)</td><td>Water exits cell</td><td>Cell shrinks & shrivels (**Crenation**)</td></tr>
      <tr><td><strong>Hypotonic</strong></td><td>$\Pi_{\text{ext}} < \Pi_{\text{cell}}$ ($< 0.9\%$)</td><td>Water enters cell</td><td>Cell swells and bursts (**Hemolysis**)</td></tr>
    </tbody>
  </table>
</div>

<div class="concept-card">
  <div class="card-label">REVERSE OSMOSIS & SEAWATER DESALINATION (FIG 1.11)</div>
  <p>When external pressure $p > \Pi$ is applied on the solution side, pure water is squeezed out of seawater through a <strong>Cellulose Acetate</strong> membrane into pure water storage.</p>
</div>

<div class="numerical-card">
  <div class="num-header"><span class="num-tag">NCERT EXAMPLE 1.11</span><span class="num-title">Molar Mass of Protein</span></div>
  <p><strong>Problem:</strong> $1.26\text{ g}$ protein in $200\text{ cm}^3$ solution at $300\text{ K}$ gives $\Pi = 2.57 \times 10^{-3}\text{ bar}$.</p>
  <div class="num-step">
    $$M_2 = \frac{1.26 \times 0.083 \times 300}{2.57 \times 10^{-3} \times 0.200} = \mathbf{61,022\text{ g mol}^{-1}}$$
  </div>
  <div class="num-ans"><strong>Final Answer:</strong> $M_2 = 61,022\text{ g mol}^{-1}$</div>
</div>
"""
    m10_rev = r"""
<div class="revision-sheet">
  <div class="rev-card">
    <h4>OSMOSIS SUMMARY</h4>
    <ul>
      <li>$\Pi = C R T = \frac{w_2 R T}{M_2 V}$</li>
      <li>Normal Saline: $0.9\%\text{ w/V NaCl}$ (isotonic with human RBCs).</li>
      <li>Hypertonic: water leaves cell (crenation). Hypotonic: water enters cell (swelling).</li>
      <li>Edema: tissue swelling caused by water retention from high-salt diets.</li>
      <li>Reverse Osmosis: $p > \Pi$ across cellulose acetate membrane.</li>
    </ul>
  </div>
</div>
"""
    m10_flashcards = [
        {"q": "Define Osmotic Pressure.", "a": "The excess hydrostatic pressure that must be applied to the solution side across an SPM to prevent osmosis."},
        {"q": "State the van 't Hoff equation for osmotic pressure.", "a": "Π = C R T = (n₂ / V) R T = (w₂ R T) / (M₂ V)."},
        {"q": "What is normal saline and why is it safe for intravenous injection?", "a": "0.9% (mass/volume) NaCl aqueous solution. It is isotonic with blood plasma, preventing red blood cells from shrinking or bursting."},
        {"q": "What happens to red blood cells placed in a hypertonic solution (>0.9% NaCl)?", "a": "Water flows out of the cell by osmosis, causing it to shrink and shrivel (crenation)."},
        {"q": "What is edema and how is it related to osmosis?", "a": "Puffiness or swelling in body tissues caused by excessive salt intake, which draws and retains water in intercellular spaces through osmosis."},
        {"q": "What membrane is used in commercial reverse osmosis desalination plants?", "a": "A porous film of cellulose acetate supported on a suitable porous substrate."}
    ]
    m10_flow = {
        "title": "Osmosis & Reverse Osmosis Direction",
        "steps": [
            {"step": "1. Normal Condition (p = 0)", "desc": "Solvent spontaneously flows from dilute to concentrated across SPM"},
            {"step": "2. Applied Pressure = Π", "desc": "Net flow stops completely (dynamic equilibrium)"},
            {"step": "3. Applied Pressure > Π", "desc": "Reverse Osmosis: Pure solvent is forced OUT of concentrated side into pure solvent"},
            {"step": "4. Collection", "desc": "Potable freshwater collected via cellulose acetate membrane"}
        ]
    }
    m10_mindmap = {
        "name": "Osmosis & Osmotic Pressure",
        "children": [
            {"name": "Equation", "children": [{"name": "Π = CRT = (w2 RT)/(M2 V)"}, {"name": "Ideal for Proteins/Polymers"}]},
            {"name": "Tonicity", "children": [{"name": "Isotonic (0.9% Saline)"}, {"name": "Hypertonic (Crenation)"}, {"name": "Hypotonic (Hemolysis)"}]},
            {"name": "Biological Case Studies", "children": [{"name": "Pickle Shriveling"}, {"name": "Wilted Flowers"}, {"name": "Edema"}, {"name": "Salting Meat/Fruit"}]},
            {"name": "Reverse Osmosis", "children": [{"name": "p > Π applied"}, {"name": "Cellulose Acetate SPM"}, {"name": "Desalination"}]}
        ]
    }

    topics.append({
        "id": "chem-sol-10-osmosis",
        "subject": "chem",
        "subject_title": "Chemistry • Solutions",
        "title": "10. Osmosis, Osmotic Pressure & RO",
        "source_file": "Class_12_Chemistry_Solutions_NCERT.pdf",
        "reading_time_min": 10,
        "detailed_html": m10_detailed,
        "toc": [{"id": "sec-10", "title": "10. Osmosis, Osmotic Pressure & RO"}],
        "revision_html": m10_rev,
        "flashcards": m10_flashcards,
        "flow_data": m10_flow,
        "mindmap_data": m10_mindmap,
        "has_handwritten": False,
        "pages": [{"page_num": 20, "text": "Osmosis phenomena: mangoes, flowers, blood cells. Semipermeable membrane (SPM). Fig 1.9 thistle funnel."}, {"page_num": 21, "text": "Osmotic pressure definition and Fig 1.10. Pi = CRT. Advantages for biomolecules/polymers."}, {"page_num": 22, "text": "Isotonic, hypertonic, hypotonic. Example 1.11 protein molar mass. Biological phenomena: edema, salting meat."}, {"page_num": 23, "text": "Reverse osmosis and water purification. Cellulose acetate membrane. Intext 1.9 to 1.12."}]
    })

    # =========================================================================
    # MODULE 11: ABNORMAL MOLAR MASSES & VAN 'T HOFF FACTOR
    # =========================================================================
    m11_detailed = r"""
<div class="topic-header">
  <span class="topic-num">TOPIC 11 OF 13</span>
  <h3 class="topic-title">Abnormal Molar Masses & van 't Hoff Factor (i)</h3>
</div>

<div class="concept-card">
  <div class="card-label">ORIGIN OF MOLAR MASS ANOMALIES</div>
  <p>Colligative properties depend directly on the number of solute particles:</p>
  <ul>
    <li><strong>Dissociation (e.g. $\text{KCl} \to \text{K}^+ + \text{Cl}^-$):</strong> Particle count doubles; colligative property doubles; observed molar mass is <strong>halved</strong> ($37.25\text{ g mol}^{-1}$ vs $74.5\text{ g mol}^{-1}$).</li>
    <li><strong>Association (e.g. Acetic acid dimerizing in benzene):</strong> Particle count halves; observed colligative property halves; observed molar mass is <strong>doubled</strong> (~$120\text{ g mol}^{-1}$ vs $60\text{ g mol}^{-1}$).</li>
  </ul>
</div>

<div class="formula-card">
  <div class="card-label">VAN 'T HOFF FACTOR ($i$) THREE DEFINITIONS</div>
  <div class="formula-block">
    $$i = \frac{\text{Normal (Theoretical) Molar Mass}}{\text{Abnormal (Experimental) Molar Mass}}$$
    $$i = \frac{\text{Observed Colligative Property}}{\text{Calculated Colligative Property}}$$
    $$i = \frac{\text{Total moles of particles after association/dissociation}}{\text{Moles of particles before association/dissociation}}$$
  </div>
  <p>• Dissociation: $i > 1$ ($\text{KCl} \to 2, \ \text{K}_2\text{SO}_4 \to 3$)</p>
  <p>• Association: $i < 1$ (Benzoic acid dimer $\to 0.5$)</p>
</div>

<div class="formula-card">
  <div class="card-label">RELATION TO DEGREE OF IONIZATION & ASSOCIATION</div>
  <div class="formula-block">
    $$\text{Dissociation: } \mathbf{\alpha = \frac{i - 1}{n - 1}} \qquad \text{Association (Dimer): } \mathbf{i = 1 - \frac{x}{2} \implies x = 2(1 - i)}$$
  </div>
</div>

<div class="table-container">
  <div class="table-caption">NCERT Table 1.4: van 't Hoff factor ($i$) for Strong Electrolytes</div>
  <table class="notes-table">
    <thead>
      <tr><th>Salt</th><th>$0.1\text{ m}$</th><th>$0.01\text{ m}$</th><th>$0.001\text{ m}$</th><th>Complete Dissociation ($i$)</th></tr>
    </thead>
    <tbody>
      <tr><td>$\text{NaCl}$</td><td>1.87</td><td>1.94</td><td>1.97</td><td><strong>2.00</strong></td></tr>
      <tr><td>$\text{KCl}$</td><td>1.85</td><td>1.94</td><td>1.98</td><td><strong>2.00</strong></td></tr>
      <tr><td>$\text{MgSO}_4$</td><td>1.21</td><td>1.53</td><td>1.82</td><td><strong>2.00</strong></td></tr>
      <tr><td>$\text{K}_2\text{SO}_4$</td><td>2.32</td><td>2.70</td><td>2.84</td><td><strong>3.00</strong></td></tr>
    </tbody>
  </table>
</div>

<div class="numerical-card">
  <div class="num-header"><span class="num-tag">NCERT EXAMPLE 1.12</span><span class="num-title">Dimerization of Benzoic Acid</span></div>
  <p><strong>Problem:</strong> $2\text{ g}$ benzoic acid in $25\text{ g}$ benzene lowers f.p. by $1.62\text{ K}$ ($K_f = 4.9$). Find $\%$ association.</p>
  <div class="num-step">
    $M_2(\text{exp}) = \frac{4.9 \times 2 \times 1000}{25 \times 1.62} = 241.98\text{ g mol}^{-1}$. Theoretical $= 122\text{ g mol}^{-1}$.<br>
    $i = 122 / 241.98 = 0.504 \implies 1 - x/2 = 0.504 \implies x/2 = 0.496 \implies x = \mathbf{0.992}$.
  </div>
  <div class="num-ans"><strong>Final Answer:</strong> Degree of association = $\mathbf{99.2\%}$</div>
</div>

<div class="numerical-card">
  <div class="num-header"><span class="num-tag">NCERT EXAMPLE 1.13</span><span class="num-title">Ka of Acetic Acid from Freezing Depression</span></div>
  <p><strong>Problem:</strong> $0.6\text{ mL}$ acetic acid ($d=1.06$) in $1\text{ L}$ water lowers f.p. by $0.0205^\circ\text{C}$ ($K_f = 1.86$). Calculate $i$ and $K_a$.</p>
  <div class="num-step">
    $m = 0.0106\text{ mol kg}^{-1} \implies \Delta T_{f(\text{calc})} = 1.86 \times 0.0106 = 0.0197\text{ K}$.<br>
    $i = 0.0205 / 0.0197 = \mathbf{1.041} \implies 1 + x = 1.041 \implies x = \mathbf{0.041}$.<br>
    $K_a = \frac{(0.0106 \times 0.041)^2}{0.0106(1 - 0.041)} = \mathbf{1.86 \times 10^{-5}}$.
  </div>
  <div class="num-ans"><strong>Final Answer:</strong> $i = 1.041, \quad x = 0.041, \quad K_a = 1.86 \times 10^{-5}$</div>
</div>
"""
    m11_rev = r"""
<div class="revision-sheet">
  <div class="rev-card">
    <h4>VAN 'T HOFF FACTOR FORMULAS</h4>
    <ul>
      <li>$i = \frac{M_{\text{normal}}}{M_{\text{abnormal}}} = \frac{\text{Observed Colligative}}{\text{Calculated Colligative}}$</li>
      <li>Dissociation: $\alpha = \frac{i - 1}{n - 1}$</li>
      <li>Association (Dimer): $x = 2(1 - i)$</li>
      <li>$\Delta T_b = i K_b m, \quad \Delta T_f = i K_f m, \quad \Pi = i C R T$</li>
    </ul>
  </div>
</div>
"""
    m11_flashcards = [
        {"q": "Define the van 't Hoff factor (i) in terms of molar masses.", "a": "i = Normal (theoretical) molar mass / Abnormal (experimentally determined) molar mass."},
        {"q": "What is the van 't Hoff factor for complete dissociation of K2SO4?", "a": "i = 3.00 (produces 2 K⁺ and 1 SO₄²⁻ ions)."},
        {"q": "Why does ethanoic acid show an experimental molar mass of ~120 g/mol in benzene?", "a": "Because ethanoic acid molecules dimerize via two hydrogen bonds in benzene (low dielectric solvent), halving the particle count."},
        {"q": "How does inclusion of factor i modify the osmotic pressure equation?", "a": "Π = i · C R T = i · (n₂ / V) R T."},
        {"q": "Express the degree of dissociation (α) in terms of van 't Hoff factor i.", "a": "α = (i - 1) / (n - 1), where n is the number of ions produced per molecule."},
        {"q": "What is the percentage association of benzoic acid in benzene from Example 1.12?", "a": "99.2% (x = 0.992)."}
    ]
    m11_flow = {
        "title": "Ionization & Association Solving Protocol",
        "steps": [
            {"step": "1. Calculate Experimental M2", "desc": "Determine experimental molar mass from $\\Delta T_b, \\Delta T_f$, or $\\Pi$"},
            {"step": "2. Calculate Factor i", "desc": "$i = M_{\\text{theoretical}} / M_{\\text{experimental}}$"},
            {"step": "3. Evaluate Process", "desc": "If $i > 1$: Dissociation. If $i < 1$: Association"},
            {"step": "4. Compute Degree (α or x)", "desc": "Dissociation: $\\alpha = \\frac{i-1}{n-1}$; Dimerization: $x = 2(1 - i)$"}
        ]
    }
    m11_mindmap = {
        "name": "Abnormal Molar Masses & i",
        "children": [
            {"name": "Dissociation", "children": [{"name": "i > 1"}, {"name": "Experimental M is Lower"}, {"name": "α = (i-1)/(n-1)"}, {"name": "KCl (i=2), K2SO4 (i=3)"}]},
            {"name": "Association", "children": [{"name": "i < 1"}, {"name": "Experimental M is Higher"}, {"name": "Acetic Acid Dimer in Benzene"}, {"name": "x = 2(1-i)"}]},
            {"name": "Modified Equations", "children": [{"name": "ΔTb = i Kb m"}, {"name": "ΔTf = i Kf m"}, {"name": "Π = i CRT"}]}
        ]
    }

    topics.append({
        "id": "chem-sol-11-abnormal-molar-mass",
        "subject": "chem",
        "subject_title": "Chemistry • Solutions",
        "title": "11. Abnormal Molar Masses & van 't Hoff",
        "source_file": "Class_12_Chemistry_Solutions_NCERT.pdf",
        "reading_time_min": 9,
        "detailed_html": m11_detailed,
        "toc": [{"id": "sec-11", "title": "11. Abnormal Molar Masses & van 't Hoff"}],
        "revision_html": m11_rev,
        "flashcards": m11_flashcards,
        "flow_data": m11_flow,
        "mindmap_data": m11_mindmap,
        "has_handwritten": False,
        "pages": [{"page_num": 23, "text": "Abnormal molar masses: dissociation into ions. KCl gives 2 moles particles, molar mass halved."}, {"page_num": 24, "text": "Association: ethanoic acid dimer in benzene. van 't Hoff factor i (1880). Three definitions. Modified colligative equations."}, {"page_num": 25, "text": "Table 1.4 values of i for NaCl, KCl, MgSO4, K2SO4. Example 1.12 benzoic acid association in benzene (99.2%)."}, {"page_num": 26, "text": "Example 1.13 acetic acid in water (i = 1.041, Ka = 1.86x10^-5)."}]
    })

    # =========================================================================
    # MODULE 12: MASTER NUMERICALS & IN-TEXT VAULT
    # =========================================================================
    m12_detailed = r"""
<div class="topic-header">
  <span class="topic-num">TOPIC 12 OF 13</span>
  <h3 class="topic-title">NCERT Solved Numericals & In-Text Vault</h3>
</div>

<div class="numerical-card">
  <div class="num-header"><span class="num-tag">INTEXT 1.1</span><span class="num-title">Mass % of Benzene in CCl4</span></div>
  <p><strong>Problem:</strong> $22\text{ g}$ benzene in $122\text{ g } \text{CCl}_4$.</p>
  <div class="num-step">$\text{Total} = 144\text{ g} \implies \text{Benzene} = \frac{22}{144} \times 100 = \mathbf{15.28\%}, \quad \text{CCl}_4 = \mathbf{84.72\%}$.</div>
  <div class="num-ans"><strong>Answer:</strong> $15.28\%$ and $84.72\%$</div>
</div>

<div class="numerical-card">
  <div class="num-header"><span class="num-tag">INTEXT 1.2</span><span class="num-title">Mole Fraction of 30% Benzene in CCl4</span></div>
  <p><strong>Problem:</strong> $30\%\text{ mass solution}$ of benzene in $\text{CCl}_4$.</p>
  <div class="num-step">
    $n(\text{C}_6\text{H}_6) = 30/78 = 0.385\text{ mol}, \quad n(\text{CCl}_4) = 70/154 = 0.455\text{ mol}$.<br>
    $x(\text{C}_6\text{H}_6) = \frac{0.385}{0.385 + 0.455} = \mathbf{0.459}, \quad x(\text{CCl}_4) = \mathbf{0.541}$.
  </div>
  <div class="num-ans"><strong>Answer:</strong> $x(\text{Benzene}) = 0.459, \ x(\text{CCl}_4) = 0.541$</div>
</div>

<div class="numerical-card">
  <div class="num-header"><span class="num-tag">INTEXT 1.4</span><span class="num-title">Mass of Urea for 0.25 molal Solution</span></div>
  <p><strong>Problem:</strong> Mass of urea for $2.5\text{ kg}$ of $0.25\text{ m}$ solution.</p>
  <div class="num-step">
    $0.25\text{ mol urea} = 0.25 \times 60 = 15\text{ g}$. Solution mass $= 1015\text{ g} = 1.015\text{ kg}$.<br>
    $\text{Mass of urea} = \frac{15}{1.015} \times 2.5 = \mathbf{36.946\text{ g}}$.
  </div>
  <div class="num-ans"><strong>Answer:</strong> $36.946\text{ g}$</div>
</div>

<div class="numerical-card">
  <div class="num-header"><span class="num-tag">INTEXT 1.6</span><span class="num-title">KH for H2S Gas at STP</span></div>
  <p><strong>Problem:</strong> Solubility of $\text{H}_2\text{S}$ is $0.195\text{ m}$ at STP.</p>
  <div class="num-step">
    $x = \frac{0.195}{0.195 + 55.55} = 0.0035$. At STP, $p = 0.987\text{ bar} \implies K_H = \frac{0.987}{0.0035} = \mathbf{282\text{ bar}}$.
  </div>
  <div class="num-ans"><strong>Answer:</strong> $K_H = 282\text{ bar}$</div>
</div>

<div class="numerical-card">
  <div class="num-header"><span class="num-tag">INTEXT 1.9</span><span class="num-title">Vapour Pressure Lowering of Urea</span></div>
  <p><strong>Problem:</strong> $50\text{ g}$ urea in $850\text{ g}$ water at $298\text{ K}$ ($p^\circ = 23.8\text{ mm Hg}$).</p>
  <div class="num-step">
    $x_2 = \frac{50/60}{50/60 + 850/18} = 0.0173 \implies \text{RLVP} = \mathbf{0.0173}$.<br>
    $p = 23.8(1 - 0.0173) = \mathbf{23.4\text{ mm Hg}}$.
  </div>
  <div class="num-ans"><strong>Answer:</strong> $p = 23.4\text{ mm Hg}, \quad \text{RLVP} = 0.0173$</div>
</div>

<div class="numerical-card">
  <div class="num-header"><span class="num-tag">INTEXT 1.10</span><span class="num-title">Sucrose Required to Boil Water at 100°C</span></div>
  <p><strong>Problem:</strong> Water boils at $99.63^\circ\text{C}$ at $750\text{ mm Hg}$. How much sucrose in $500\text{ g}$ water boils at $100^\circ\text{C}$?</p>
  <div class="num-step">
    $\Delta T_b = 100 - 99.63 = 0.37\text{ K} \implies w_2 = \frac{0.37 \times 342 \times 500}{1000 \times 0.52} = \mathbf{121.67\text{ g}}$.
  </div>
  <div class="num-ans"><strong>Answer:</strong> $121.67\text{ g}$</div>
</div>

<div class="numerical-card">
  <div class="num-header"><span class="num-tag">INTEXT 1.12</span><span class="num-title">Osmotic Pressure of Polymer Solution</span></div>
  <p><strong>Problem:</strong> $1.0\text{ g}$ polymer ($M=185,000$) in $450\text{ mL}$ water at $37^\circ\text{C}$.</p>
  <div class="num-step">
    $\Pi = \frac{n R T}{V} = \frac{(1.0/185000) \times 8.314 \times 310.15}{0.450 \times 10^{-3}} = \mathbf{30.96\text{ Pa}}$.
  </div>
  <div class="num-ans"><strong>Answer:</strong> $\Pi = 30.96\text{ Pa}$</div>
</div>
"""
    m12_rev = r"""
<div class="revision-sheet">
  <div class="rev-card">
    <h4>OFFICIAL NCERT ANSWERS QUICK REFERENCE</h4>
    <ul>
      <li>1.1: $C_6H_6 = 15.28\%, CCl_4 = 84.72\%$</li>
      <li>1.2: $0.459, 0.541$</li>
      <li>1.3: $0.024\text{ M}, 0.03\text{ M}$</li>
      <li>1.4: $36.946\text{ g}$</li>
      <li>1.5: $1.5\text{ m}, 1.45\text{ M}, 0.0263$</li>
      <li>1.9: $23.4\text{ mm Hg}$</li>
      <li>1.10: $121.67\text{ g}$</li>
      <li>1.11: $5.077\text{ g}$</li>
      <li>1.12: $30.96\text{ Pa}$</li>
    </ul>
  </div>
</div>
"""
    m12_flashcards = [
        {"q": "What is the mass of urea required to make 2.5 kg of 0.25 molal solution?", "a": "36.946 g (In-Text Question 1.4)."},
        {"q": "What is the Henry's law constant for H2S gas at STP if solubility is 0.195 m?", "a": "282 bar (In-Text Question 1.6)."},
        {"q": "What is the osmotic pressure of 1.0 g polymer (M=185,000) in 450 mL water at 37°C?", "a": "30.96 Pa (In-Text Question 1.12)."},
        {"q": "How much sucrose is added to 500 g water to boil at 100°C if water boils at 99.63°C?", "a": "121.67 g (In-Text Question 1.10)."}
    ]
    m12_flow = {
        "title": "Numerical Formula Selection Flow",
        "steps": [
            {"step": "1. Identify Problem Type", "desc": "Concentration, Gas Solubility, Vapour Pressure, Colligative Property, or van 't Hoff Factor"},
            {"step": "2. Extract Given Quantities", "desc": "Convert all masses to g/kg, volumes to L, temperatures to Kelvin"},
            {"step": "3. Substitute into Standard Formula", "desc": "Apply $p = K_H x, \\Delta T_b = i K_b m, \\Delta T_f = i K_f m, \\Pi = i C R T$"},
            {"step": "4. Verify Significant Figures & Units", "desc": "Ensure final answer has correct units (bar, K, g mol⁻¹, Pa)"}
        ]
    }
    m12_mindmap = {
        "name": "Solved Numericals & In-Text",
        "children": [
            {"name": "Concentration (Ex 1.1-1.3, Intext 1.1-1.5)"},
            {"name": "Henry's Law (Ex 1.4, Intext 1.6-1.7)"},
            {"name": "Raoult's Law (Ex 1.5, Intext 1.8)"},
            {"name": "Colligative Properties (Ex 1.6-1.11, Intext 1.9-1.12)"},
            {"name": "van 't Hoff Ionization (Ex 1.12-1.13)"}
        ]
    }

    topics.append({
        "id": "chem-sol-12-numericals-vault",
        "subject": "chem",
        "subject_title": "Chemistry • Solutions",
        "title": "12. NCERT Solved Numericals & In-Text Vault",
        "source_file": "Class_12_Chemistry_Solutions_NCERT.pdf",
        "reading_time_min": 15,
        "detailed_html": m12_detailed,
        "toc": [{"id": "sec-12", "title": "12. NCERT Solved Numericals & In-Text Vault"}],
        "revision_html": m12_rev,
        "flashcards": m12_flashcards,
        "flow_data": m12_flow,
        "mindmap_data": m12_mindmap,
        "has_handwritten": False,
        "pages": [{"page_num": 27, "text": "Exercises 1.1 to 1.4."}, {"page_num": 28, "text": "Exercises 1.5 to 1.21."}, {"page_num": 29, "text": "Exercises 1.22 to 1.36."}, {"page_num": 30, "text": "Exercise 1.37 to 1.41. Answers to Some Intext Questions (1.1 to 1.12)."}]
    })

    # =========================================================================
    # MODULE 13: MASTER CHAPTER REVISION HUB
    # =========================================================================
    m13_detailed = r"""
<div class="topic-header">
  <span class="topic-num">TOPIC 13 OF 13</span>
  <h3 class="topic-title">Solutions: Complete Chapter Revision Hub & Mind Map</h3>
</div>

<div class="chem-chapter-overview">
  <div class="chem-badge">COMPLETE CHAPTER MASTERY</div>
  <h2 class="chem-hero-title">Unit 1: Solutions Master Review</h2>
  <p class="chem-hero-desc">
    Master formula table, thermodynamic criteria, colligative relationships, and high-yield exam traps compiled from all 30 pages of the NCERT textbook.
  </p>
</div>

<div class="concept-card">
  <div class="card-label">MASTER FORMULA VAULT</div>
  <table class="notes-table">
    <thead>
      <tr><th>Concept</th><th>Formula</th><th>Units & Invariance</th></tr>
    </thead>
    <tbody>
      <tr><td>Mass %</td><td>$w_2 / w_{\text{total}} \times 100$</td><td>$\%$ (Temp Independent)</td></tr>
      <tr><td>Mole Fraction</td><td>$x_A = n_A / \sum n_i, \quad \sum x_i = 1$</td><td>Dimensionless (Temp Independent)</td></tr>
      <tr><td>Molarity</td><td>$M = \frac{w_2 \times 1000}{M_2 \times V_{\text{mL}}}$</td><td>$\text{mol L}^{-1}$ (**Temp Dependent**)</td></tr>
      <tr><td>Molality</td><td>$m = \frac{w_2 \times 1000}{M_2 \times w_{1(\text{g})}}$</td><td>$\text{mol kg}^{-1}$ (Temp Independent)</td></tr>
      <tr><td>Henry's Law</td><td>$p = K_H \cdot x$</td><td>$p$ in bar; higher $K_H \implies$ lower solubility</td></tr>
      <tr><td>Raoult's Law (Volatile)</td><td>$p_{\text{total}} = p_1^\circ + (p_2^\circ - p_1^\circ)x_2$</td><td>$y_i = p_i / p_{\text{total}}$ in vapour</td></tr>
      <tr><td>RLVP</td><td>$\frac{p_1^\circ - p_1}{p_1^\circ} = i \cdot \frac{w_2 M_1}{M_2 w_1}$</td><td>Dilute solutions ($n_2 \ll n_1$)</td></tr>
      <tr><td>Boiling Elevation</td><td>$\Delta T_b = i \cdot K_b \cdot m = i \cdot \frac{1000 w_2 K_b}{M_2 w_1}$</td><td>$K_b$ in $\text{K kg mol}^{-1}$</td></tr>
      <tr><td>Freezing Depression</td><td>$\Delta T_f = i \cdot K_f \cdot m = i \cdot \frac{1000 w_2 K_f}{M_2 w_1}$</td><td>$K_f$ in $\text{K kg mol}^{-1}$</td></tr>
      <tr><td>Osmotic Pressure</td><td>$\Pi = i \cdot C R T = i \cdot \frac{w_2 R T}{M_2 V}$</td><td>$R = 0.083\text{ L bar mol}^{-1}\text{ K}^{-1}$</td></tr>
      <tr><td>van 't Hoff Factor ($i$)</td><td>$i = \frac{M_{\text{normal}}}{M_{\text{abnormal}}} = 1 + (n-1)\alpha$</td><td>$i > 1$ (Dissociation), $i < 1$ (Association)</td></tr>
    </tbody>
  </table>
</div>

<div class="remember-box">
  <strong>🔥 HIGH-YIELD EXAM TRAPS:</strong>
  <ul>
    <li><strong>Temperature Independence:</strong> Mass %, ppm, mole fraction, and molality do NOT change with temperature because mass does not depend on temperature. Molarity changes with temperature because volume changes with temperature.</li>
    <li><strong>Cold Water Fish:</strong> $K_H$ increases with rising temperature $\implies$ gas solubility drops as temperature rises. Aquatic species thrive in cold waters.</li>
    <li><strong>Azeotropic Barrier:</strong> $95\%$ ethanol cannot be separated further by fractional distillation because vapour and liquid compositions become identical.</li>
    <li><strong>Polymer Molar Mass:</strong> Osmotic pressure is the only suitable method for polymers because other colligative changes ($\Delta T_b, \Delta T_f$) are too small to detect at low concentrations ($10^{-3}\text{ M}$).</li>
    <li><strong>Dimerization:</strong> Acetic and benzoic acids dimerize in benzene due to hydrogen bonding, halving particles and doubling apparent molar mass ($i \approx 0.5$).</li>
  </ul>
</div>
"""
    m13_rev = r"""
<div class="revision-sheet">
  <div class="rev-card">
    <h4>SOLUTIONS IN A NUTSHELL</h4>
    <p>Solutions are homogeneous mixtures. Concentration is measured by molarity, molality, mole fraction, and percentages. Gases obey Henry's law ($p=K_Hx$). Volatile liquids obey Raoult's law ($p_i=x_ip_i^\circ$). Ideal solutions exhibit $\Delta H=0, \Delta V=0$. Colligative properties (RLVP, boiling elevation, freezing depression, osmotic pressure) depend purely on particle count. The van 't Hoff factor ($i$) corrects for dissociation and association.</p>
  </div>
</div>
"""
    m13_flashcards = [
        {"q": "What is the central concept of colligative properties?", "a": "They depend strictly on the number of solute particles relative to total particles in solution, completely independent of their chemical nature."},
        {"q": "Which concentration units are independent of temperature?", "a": "Mass percentage, parts per million (ppm), mole fraction, and molality (all depend on mass, not volume)."},
        {"q": "How does Henry's law constant KH vary with temperature and what is the biological consequence?", "a": "KH increases with temperature, so gas solubility decreases. Cold water holds more dissolved oxygen, making aquatic life more comfortable in cold waters."},
        {"q": "What is an azeotrope and what causes it?", "a": "A constant-boiling binary mixture having the same composition in liquid and vapour phases, caused by very large deviations from Raoult's law."},
        {"q": "Why is osmotic pressure the best colligative method for proteins and polymers?", "a": "It can be measured at room temperature, uses molarity, and provides large, easily measurable readings even for very dilute solutions."},
        {"q": "What is the van 't Hoff factor for complete dissociation of K2SO4?", "a": "i = 3.0."},
        {"q": "What happens to the apparent molar mass when a solute dimerizes in solution?", "a": "It doubles, because the number of solute particles is halved (i = 0.5)."},
        {"q": "What membrane is used in industrial reverse osmosis seawater desalination?", "a": "Cellulose acetate film."}
    ]
    m13_flow = {
        "title": "Solutions Chapter Complete Concept Roadmap",
        "steps": [
            {"step": "1. Solution Basics & Concentration", "desc": "9 Types matrix $\\to$ Mass %, Mole Fraction, Molarity, Molality"},
            {"step": "2. Solubility Equilibria", "desc": "Solid solubility (Like dissolves like) $\\to$ Gas solubility (Henry's Law $p = K_H x$)"},
            {"step": "3. Liquid Vapour Pressure", "desc": "Raoult's Law $\\to$ Ideal vs Non-Ideal Deviations $\\to$ Azeotropes"},
            {"step": "4. Colligative Properties", "desc": "RLVP $\\to$ Boiling Elevation $\\to$ Freezing Depression $\\to$ Osmotic Pressure"},
            {"step": "5. Ionization & Association", "desc": "van 't Hoff Factor ($i$) $\\to$ Degree of Dissociation/Association $\\to$ Abnormal Molar Mass"}
        ]
    }
    m13_mindmap = {
        "name": "Solutions (NCERT Class 12 Master Tree)",
        "children": [
            {
                "name": "1. Types & Concentration",
                "children": [
                    {"name": "9 Types Matrix (Gas, Liquid, Solid)"},
                    {"name": "Temp-Invariant (Mass %, ppm, x, Molality)"},
                    {"name": "Temp-Variant (Volume %, Molarity)"}
                ]
            },
            {
                "name": "2. Solubility & Henry's Law",
                "children": [
                    {"name": "Solid (Like dissolves like, Le Chatelier)"},
                    {"name": "Gas (Henry: p = KH x)"},
                    {"name": "Applications (Soda, Scuba Bends, Anoxia)"}
                ]
            },
            {
                "name": "3. Vapour Pressure & Raoult",
                "children": [
                    {"name": "Volatile Liquids (ptotal = p1° + (p2°-p1°)x2)"},
                    {"name": "Vapour Phase Richer in More Volatile"},
                    {"name": "Ideal (ΔH=0, ΔV=0, n-Hexane+Heptane)"},
                    {"name": "Deviations (Positive vs Negative)"},
                    {"name": "Azeotropes (Min vs Max Boiling)"}
                ]
            },
            {
                "name": "4. Colligative Properties",
                "children": [
                    {"name": "RLVP: Δp/p° = x2"},
                    {"name": "Boiling Elevation: ΔTb = Kb m"},
                    {"name": "Freezing Depression: ΔTf = Kf m"},
                    {"name": "Osmotic Pressure: Π = CRT"},
                    {"name": "Tonicity & Reverse Osmosis"}
                ]
            },
            {
                "name": "5. Abnormal Molar Masses",
                "children": [
                    {"name": "Dissociation (i > 1, M_obs Lower)"},
                    {"name": "Association (i < 1, M_obs Higher)"},
                    {"name": "Modified Equations (ΔTb = i Kb m, Π = i CRT)"}
                ]
            }
        ]
    }

    topics.append({
        "id": "chem-sol-13-revision-hub",
        "subject": "chem",
        "subject_title": "Chemistry • Solutions",
        "title": "13. Solutions: Complete Chapter Revision Hub",
        "source_file": "Class_12_Chemistry_Solutions_NCERT.pdf",
        "reading_time_min": 12,
        "detailed_html": m13_detailed,
        "toc": [{"id": "sec-13", "title": "13. Solutions: Complete Chapter Revision Hub"}],
        "revision_html": m13_rev,
        "flashcards": m13_flashcards,
        "flow_data": m13_flow,
        "mindmap_data": m13_mindmap,
        "has_handwritten": False,
        "pages": [{"page_num": 27, "text": "Unit 1 Summary. Types of solutions, concentration, Henry's law, Raoult's law, ideal and non-ideal, colligative properties, reverse osmosis, van 't Hoff factor."}, {"page_num": 30, "text": "Answers to Some Intext Questions 1.1 to 1.12."}]
    })

    return topics
