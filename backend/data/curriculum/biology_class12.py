"""
SIKSHA SAATHI — Biology Curriculum: NCERT Class 12 (Complete 13 Chapters)
13 Distinct Topic Modules with Dedicated Detailed Notes, Revision Sheets,
Active-Recall Flashcards, Interactive Flowcharts, Zoomable Mind Maps, and RAG Chunks.
Fully aligned with NCERT Biology Class XII Textbook (Units VI to X).
"""

import os
import json
from typing import Dict, List, Any

ENHANCED_DATA_PATH = os.path.join(os.path.dirname(__file__), "biology_class12_enhanced.json")

def get_all_biology_topics() -> List[Dict[str, Any]]:
    """Returns the complete array of 13 structured Biology Class 12 topic modules."""
    if os.path.exists(ENHANCED_DATA_PATH):
        try:
            with open(ENHANCED_DATA_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Failed to load enhanced biology JSON: {e}")

    topics = []

    # =========================================================================
    # MODULE 01: SEXUAL REPRODUCTION IN FLOWERING PLANTS
    # =========================================================================
    m01_detailed = r"""
<div class="topic-header">
  <span class="topic-num">UNIT VI • TOPIC 01 OF 13</span>
  <h3 class="topic-title">Sexual Reproduction in Flowering Plants</h3>
</div>

<div class="concept-card">
  <div class="card-label">FLOWER AS A REPRODUCTIVE ORGAN & PRE-FERTILIZATION STRUCTURES</div>
  <p>Flowers are morphological and embryological marvels and the sites of sexual reproduction in Angiosperms. Hormonal and structural changes initiate floral primordia differentiation into an inflorescence bearing floral buds and flowers.</p>
  <ul>
    <li><strong>Stamen, Microsporangium & Pollen Grain:</strong>
      <ul>
        <li>A typical stamen consists of a long slender stalk called <strong>filament</strong> and a terminal bilobed structure called <strong>anther</strong>. Angiosperm anther is <em>bilobed</em> and <em>dithecous</em> (two thecae per lobe separated by a longitudinal groove).</li>
        <li><strong>4 Microsporangia:</strong> Located at the corners, two in each lobe, which develop into pollen sacs.</li>
        <li><strong>Microsporangium Wall Layers:</strong>
          <ol>
            <li><em>Epidermis:</em> Outermost single layer for protection.</li>
            <li><em>Endothecium:</em> Second layer with fibrous alpha-cellulosic thickenings; hygroscopic, aiding dehiscence.</li>
            <li><em>Middle Layers:</em> 1 to 3 transient parenchymatous layers that degenerate at maturity.</li>
            <li><em>Tapetum:</em> Innermost nutritive layer nourishing developing microspores. Cells have dense cytoplasm and are generally <strong>multinucleate</strong> or polyploid.</li>
          </ol>
        </li>
      </ul>
    </li>
    <li><strong>Microsporogenesis:</strong> Process of formation of microspores from Pollen Mother Cell (PMC) / Microspore Mother Cell (MMC) through meiosis. Each PMC produces a <em>microspore tetrad</em>.</li>
    <li><strong>Pollen Grain (Male Gametophyte):</strong> Spherical, $25\text{--}50\,\mu\text{m}$ diameter, with a two-layered wall:
      <ul>
        <li><em>Exine:</em> Hard outer layer made of <strong>sporopollenin</strong> (most resistant organic material known; withstands high temperatures, strong acids and alkalis; no enzyme degrades it). Prominent apertures where sporopollenin is absent are called <strong>germ pores</strong>.</li>
        <li><em>Intine:</em> Inner thin, continuous layer composed of <strong>cellulose and pectin</strong>.</li>
        <li><strong>2-Celled vs 3-Celled Stage:</strong> In $>60\%$ of angiosperms, pollen grains are shed at the 2-celled stage (large <em>vegetative cell</em> with abundant food reserves and irregular nucleus + small spindle-shaped <em>generative cell</em> floating in vegetative cytoplasm). In $<40\%$, generative cell divides mitotically to form two male gametes before shedding (3-celled stage).</li>
        <li><em>Pollen Viability:</em> 30 minutes in rice and wheat; several months in members of Rosaceae, Leguminosae, and Solanaceae. Pollen grains stored for years at $-196^\circ\text{C}$ in liquid nitrogen (pollen banks).</li>
      </ul>
    </li>
  </ul>
</div>

<div class="table-container">
  <div class="table-caption">NCERT Comparison: Microsporogenesis vs Megasporogenesis</div>
  <table class="notes-table">
    <thead>
      <tr><th>Feature</th><th>Microsporogenesis</th><th>Megasporogenesis</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>Site of Occurrence</strong></td><td>Inside microsporangium (pollen sac) of anther</td><td>Inside megasporangium (ovule / nucellus) of ovary</td></tr>
      <tr><td><strong>Mother Cell</strong></td><td>Microspore Mother Cell (PMC) ($2n$)</td><td>Megaspore Mother Cell (MMC) ($2n$)</td></tr>
      <tr><td><strong>Meiotic Division</strong></td><td>Produces 4 functional microspores in a tetrad</td><td>Produces 4 megaspores arranged linearly</td></tr>
      <tr><td><strong>Fate of Spores</strong></td><td>All 4 microspores survive and form pollen grains ($100\%$ survival)</td><td>3 degenerate at micropylar end; only 1 functional at chalazal end ($25\%$ survival)</td></tr>
      <tr><td><strong>Gametes Produced</strong></td><td>Each pollen grain produces 2 male gametes</td><td>Embryo sac produces 1 female gamete (egg cell)</td></tr>
    </tbody>
  </table>
</div>

<div class="concept-card">
  <div class="card-label">PISTIL, MEGASPORANGIUM (OVULE) & EMBRYO SAC</div>
  <p>The gynoecium represents female reproductive organ. Monocarpellary (single pistil) or multicarpellary (syncarpous fused / apocarpous free).</p>
  <ul>
    <li><strong>Anatomy of Anatropous Ovule:</strong>
      <ul>
        <li><strong>Funicle:</strong> Stalk attaching ovule to placenta.</li>
        <li><strong>Hilum:</strong> Junction between ovule body and funicle.</li>
        <li><strong>Integuments:</strong> Protective envelopes encircling nucellus except at a small pore called <strong>micropyle</strong>.</li>
        <li><strong>Chalaza:</strong> Basal part of ovule opposite to micropylar end.</li>
        <li><strong>Nucellus:</strong> Central mass of parenchymatous cells with abundant reserve food.</li>
      </ul>
    </li>
    <li><strong>Female Gametophyte (Embryo Sac):</strong> Develops from single functional megaspore at chalazal end (<strong>monosporic development</strong>). Three sequential free-nuclear mitotic divisions produce 8 nuclei:
      <ul>
        <li><strong>Egg Apparatus (Micropylar end, 3 cells):</strong> 1 central egg cell ($n$) + 2 flanking <strong>synergids</strong> with specialized cellular thickenings called <strong>filiform apparatus</strong> (guides entry of pollen tube into synergid).</li>
        <li><strong>Antipodal Cells (Chalazal end, 3 cells):</strong> Nutritive and vegetative role, degenerate after fertilization.</li>
        <li><strong>Central Cell (1 large cell):</strong> Contains 2 <strong>polar nuclei</strong>.</li>
        <li><strong>Mature Embryo Sac Architecture:</strong> <strong>7-celled, 8-nucleate</strong> structure.</li>
      </ul>
    </li>
  </ul>
</div>

<div class="concept-card">
  <div class="card-label">POLLINATION MECHANISMS & OUTBREEDING DEVICES</div>
  <ul>
    <li><strong>Kinds of Pollination:</strong>
      <ol>
        <li><em>Autogamy:</em> Transfer of pollen from anther to stigma of <em>same flower</em>. Requires synchrony in pollen release and stigma receptivity. Cleistogamous flowers (e.g. <em>Viola</em> common pansy, <em>Oxalis</em>, <em>Commelina</em>) never open, ensuring seed set even without pollinators. Chasmogamous flowers have exposed anthers and stigmas.</li>
        <li><em>Geitonogamy:</em> Transfer of pollen from anther to stigma of <em>another flower of the same plant</em>. Functionally cross-pollination (requires agent), genetically self-pollination (zygote from same plant).</li>
        <li><em>Xenogamy:</em> Transfer of pollen to stigma of a <em>flower on a different plant</em>. Brings genetically different pollen grains to stigma.</li>
      </ol>
    </li>
    <li><strong>Agents of Pollination:</strong>
      <ul>
        <li><strong>Wind (Anemophily):</strong> Pollen light, dry, non-sticky; well-exposed stamens; feathery stigma to trap airborne pollen; single ovule per ovary; packed into inflorescence (e.g., corn cob tassels, grasses).</li>
        <li><strong>Water (Hydrophily):</strong> Rare (30 genera, mostly monocots). <em>Vallisneria</em> (epihydrophily: female flower reaches surface by long stalk; pollen released onto water surface), <em>Zostera</em> (sea grasses: hypohydrophily; long ribbon-like pollen released inside water without exine). Note: <em>Water hyacinth</em> and <em>water lily</em> are aquatic plants pollinated by <strong>insects or wind</strong>!</li>
        <li><strong>Animals (Zoophily):</strong> Large, colorful, fragrant, nectar-rich flowers. Bees are dominant pollinators. <em>Amorphophallus</em> (6 ft flower) and <em>Yucca</em> have obligate mutualism with Pronuba moth (safe egg-laying site in locule).</li>
      </ul>
    </li>
    <li><strong>Outbreeding Devices (Preventing Inbreeding Depression):</strong>
      <ol>
        <li>Pollen release and stigma receptivity not synchronized (<em>Dichogamy</em>: Protandry / Protogyny).</li>
        <li>Anther and stigma placed at different positions (<em>Heterostyly</em>).</li>
        <li><strong>Self-incompatibility:</strong> Genetic mechanism preventing self-pollen from fertilizing ovules by inhibiting pollen germination or pollen tube growth.</li>
        <li>Production of unisexual flowers (<em>Dicliny</em>): Monoecious plants (castor, maize) prevent autogamy but not geitonogamy; Dioecious plants (papaya) prevent both autogamy and geitonogamy.</li>
      </ol>
    </li>
  </ul>
</div>

<div class="remember-box">
  <strong>DOUBLE FERTILIZATION & POST-FERTILIZATION DESTINY:</strong>
  <ul>
    <li><strong>Syngamy:</strong> One male gamete ($n$) + Egg nucleus ($n$) $\to$ <strong>Zygote ($2n$)</strong>, which develops into Embryo.</li>
    <li><strong>Triple Fusion:</strong> Second male gamete ($n$) + 2 Polar nuclei ($2n$) in central cell $\to$ <strong>Primary Endosperm Nucleus (PEN, $3n$)</strong>, which forms Endosperm.</li>
    <li>Unique hallmark event restricted exclusively to Angiosperms!</li>
    <li><strong>Endosperm Precedes Embryo:</strong> PEN divides repeatedly to form triploid endosperm tissue filled with reserve food to nourish developing embryo. Free-nuclear endosperm: e.g. tender coconut water (thousands of free nuclei) + surrounding cellular endosperm (white coconut meat).</li>
    <li><strong>Seed Anatomy:</strong> Non-albuminous/Exalbuminous (endosperm completely consumed e.g. pea, groundnut, beans) vs Albuminous/Endospermic (endosperm retained e.g. wheat, maize, barley, castor, sunflower). Persistent nucellus in seed = <strong>Perisperm</strong> (e.g. black pepper, beet).</li>
    <li><strong>Apomixis:</strong> Form of asexual reproduction mimicking sexual reproduction producing seeds without fertilization (e.g. Asteraceae and grasses). Diploid egg formed without reduction division or nucellar cells protrude into embryo sac (<strong>Polyembryony</strong> in <em>Citrus</em> and <em>Mango</em>).</li>
  </ul>
</div>
"""

    m01_revision = r"""
<div class="quick-revision-box">
  <h4>High-Yield Revision — Sexual Reproduction in Flowering Plants</h4>
  <ul>
    <li><strong>Anther:</strong> Bilobed, dithecous, 4 microsporangia. Wall = Epidermis $\to$ Endothecium (dehiscence) $\to$ Middle layers $\to$ Tapetum (nourishing, multinucleate).</li>
    <li><strong>Sporopollenin:</strong> Forms exine; synthesized from carotenoids; resistant to physical, chemical, enzymatic breakdown; preserved in fossils.</li>
    <li><strong>Embryo Sac:</strong> 7-celled, 8-nucleate monosporic structure: 3 antipodals (chalazal) + 2 polar nuclei in central cell + egg apparatus (2 synergids with filiform apparatus + 1 egg cell at micropyle).</li>
    <li><strong>Cleistogamous Flowers:</strong> Invariable autogamy, no pollinators required (<em>Viola, Oxalis, Commelina</em>).</li>
    <li><strong>Double Fertilization:</strong> Syngamy ($n + n \to 2n$ zygote) + Triple Fusion ($n + 2n \to 3n$ PEN). Discovered by Nawaschin.</li>
    <li><strong>False Fruits:</strong> Thalamus contributes to fruit formation (Apple, Pear, Strawberry, Cashew). Parthenocarpic fruit develops without fertilization (Banana, induced by auxins).</li>
    <li><strong>Perisperm:</strong> Residual persistent nucellus in mature seed (Black pepper, Beetroot).</li>
  </ul>
</div>
"""

    m01_flashcards = [
      {"q": "What makes sporopollenin the most resistant organic material known?", "a": "It withstands high temperatures, strong acids, and alkalis. No enzyme is known that degrades sporopollenin, which allows pollen grains to be preserved as fossils."},
      {"q": "What is the ploidy and cellular composition of a mature angiosperm embryo sac?", "a": "It is 7-celled and 8-nucleate: 3 antipodal cells (chalazal, n), 1 central cell with 2 polar nuclei (n+n), and an egg apparatus of 2 synergids (n) and 1 egg cell (n)."},
      {"q": "Why is tender coconut water considered free-nuclear endosperm?", "a": "The primary endosperm nucleus (PEN) undergoes repeated free-nuclear divisions without cytokinesis, producing thousands of free triploid nuclei suspended in liquid."},
      {"q": "What is the functional difference between Geitonogamy and Xenogamy?", "a": "Geitonogamy is functionally cross-pollination via pollinating agents but genetically self-pollination (same plant). Xenogamy brings genetically distinct pollen from a different plant."},
      {"q": "What is apomixis and why is it commercially important in hybrid seed production?", "a": "Apomixis is seed formation without fertilization. If hybrid crops are made apomictic, farmers can reuse harvested seeds year after year without segregation of desirable hybrid traits."},
      {"q": "What is the function of the filiform apparatus in synergids?", "a": "It consists of special finger-like cellular thickenings at the micropylar tip that guide the entry of the pollen tube into the synergid."}
    ]

    m01_flow = [
      {"id": "s1", "title": "Microsporogenesis", "badge": "Step 1", "desc": "Diploid Pollen Mother Cell (PMC) undergoes meiosis to produce 4 haploid microspores in a tetrad."},
      {"id": "s2", "title": "Pollen Maturation", "badge": "Step 2", "desc": "Microspores separate and develop sporopollenin exine and cellulose intine. Mitosis produces vegetative and generative cells (60% shed at 2-celled stage)."},
      {"id": "s3", "title": "Megasporogenesis", "badge": "Step 3", "desc": "Single MMC in nucellus undergoes meiosis forming 4 megaspores; 3 micropylar degenerate, chalazal megaspore survives."},
      {"id": "s4", "title": "Embryo Sac Genesis", "badge": "Step 4", "desc": "Functional megaspore undergoes 3 rounds of free-nuclear mitosis forming 8 nuclei organized into 7 cells."},
      {"id": "s5", "title": "Pollination & Syngamy", "badge": "Step 5", "desc": "Pollen lands on stigma, germinates pollen tube guided by filiform apparatus. Syngamy forms 2n zygote; triple fusion forms 3n PEN."},
      {"id": "s6", "title": "Seed & Fruit Development", "badge": "Step 6", "desc": "PEN develops into endosperm, zygote forms embryo, ovule matures into seed with testa/tegmen, ovary ripens into pericarp fruit."}
    ]

    m01_mindmap = {
      "id": "root", "title": "Sexual Reprod. in Plants", "icon": "🌸", "children": [
        {"id": "male", "title": "Male Organs (Stamen)", "icon": "♂️", "children": [
          {"id": "m1", "title": "Anther Wall: Epidermis, Endothecium, Middle, Tapetum"},
          {"id": "m2", "title": "Pollen: Exine (Sporopollenin) + Intine (Pectin/Cellulose)"},
          {"id": "m3", "title": "Shedding: 2-celled (60%) vs 3-celled (40%)"}
        ]},
        {"id": "female", "title": "Female Organs (Carpel)", "icon": "♀️", "children": [
          {"id": "f1", "title": "Ovule Anatomy: Funicle, Hilum, Integuments, Nucellus, Chalaza"},
          {"id": "f2", "title": "Embryo Sac: 7-celled, 8-nucleate monosporic structure"},
          {"id": "f3", "title": "Egg apparatus: 2 Synergids + Filiform apparatus + 1 Egg"}
        ]},
        {"id": "pollination", "title": "Pollination Types", "icon": "🐝", "children": [
          {"id": "p1", "title": "Autogamy (Cleistogamy e.g. Viola, Oxalis)"},
          {"id": "p2", "title": "Geitonogamy (Functionally cross, genetically self)"},
          {"id": "p3", "title": "Xenogamy (True cross-pollination)"},
          {"id": "p4", "title": "Agents: Anemophily, Hydrophily (Zostera), Zoophily (Bees)"}
        ]},
        {"id": "fertilization", "title": "Double Fertilization", "icon": "⚡", "children": [
          {"id": "d1", "title": "Syngamy: Male gamete + Egg cell -> 2n Zygote"},
          {"id": "d2", "title": "Triple Fusion: Male gamete + 2 Polar nuclei -> 3n PEN"},
          {"id": "d3", "title": "Endosperm: Free-nuclear (Coconut water) -> Cellular (Meat)"},
          {"id": "d4", "title": "Special: Apomixis, Polyembryony (Citrus), Perisperm (Black pepper)"}
        ]}
      ]
    }

    m01_pages = [
      {"page_num": 1, "text": "Sexual reproduction in flowering plants NCERT summary: Anther structure with 4 layers: Epidermis, Endothecium, Middle layers, and Tapetum. Microsporogenesis from pollen mother cells to microspores. Pollen wall exine composed of sporopollenin, intine of cellulose and pectin. Shedding at 2-celled stage in 60% angiosperms."},
      {"page_num": 2, "text": "Megasporogenesis: Anatropous ovule with funicle, hilum, integuments, micropyle, nucellus, chalaza. Monosporic development from single functional megaspore at chalazal end producing 7-celled 8-nucleate female gametophyte with egg apparatus, antipodals, and polar nuclei."},
      {"page_num": 3, "text": "Pollination strategies: Autogamy, geitonogamy, xenogamy. Outbreeding devices include dichogamy, self-incompatibility, and dioecy. Double fertilization involves syngamy (2n zygote) and triple fusion (3n primary endosperm nucleus). Endosperm development precedes embryo. Apomixis and polyembryony in citrus."}
    ]

    topics.append({
      "id": "bio-ch01-flowering-plants",
      "title": "01. Sexual Reproduction in Flowering Plants",
      "subject": "bio",
      "subject_title": "Biology • Class 12",
      "reading_time_min": 14,
      "has_handwritten": False,
      "detailed_html": m01_detailed,
      "revision_html": m01_revision,
      "flashcards": m01_flashcards,
      "flow_data": m01_flow,
      "mindmap_data": m01_mindmap,
      "pages": m01_pages
    })

    # =========================================================================
    # MODULE 02: HUMAN REPRODUCTION
    # =========================================================================
    m02_detailed = r"""
<div class="topic-header">
  <span class="topic-num">UNIT VI • TOPIC 02 OF 13</span>
  <h3 class="topic-title">Human Reproduction</h3>
</div>

<div class="concept-card">
  <div class="card-label">MALE REPRODUCTIVE SYSTEM</div>
  <p>Located in the pelvic region. Humans are sexually reproducing and viviparous.</p>
  <ul>
    <li><strong>Testes:</strong> Suspended in <strong>scrotum</strong> outside the abdominal cavity; keeps testicular temperature $2\text{--}2.5^\circ\text{C}$ lower than internal core body temperature, strictly essential for spermatogenesis. Oval, length 4-5 cm, width 2-3 cm.</li>
    <li><strong>Internal Architecture:</strong> ~250 <em>testicular lobules</em> per testis. Each lobule contains 1 to 3 highly coiled <strong>seminiferous tubules</strong>.
      <ul>
        <li><strong>Inside tubules:</strong> <em>Male germ cells (Spermatogonia, $2n$)</em> that undergo meiosis to form sperms, and <em>Sertoli cells (Nurse cells)</em> that provide nutrition to germ cells.</li>
        <li><strong>Interstitial spaces:</strong> Contain small blood vessels and <strong>Leydig cells (Interstitial cells)</strong> that synthesize and secrete testicular hormones called <strong>androgens (Testosterone)</strong>.</li>
      </ul>
    </li>
    <li><strong>Accessory Ducts:</strong> Rete testis $\to$ Vasa efferentia (10-12) $\to$ Epididymis (stores and matures sperms) $\to$ Vas deferens (ascends into abdomen, loops over urinary bladder) $\to$ Ejaculatory duct $\to$ Urethra (urethral meatus).</li>
    <li><strong>Accessory Glands:</strong>
      <ul>
        <li><em>Seminal Vesicles (Paired):</em> Secrete alkaline seminal fluid rich in <strong>fructose</strong>, prostaglandins, and clotting proteins ($60\%\text{ of semen}$).</li>
        <li><em>Prostate Gland (Single):</em> Surrounds urethra, secretes milky, slightly acidic fluid containing citrate and calcium.</li>
        <li><em>Bulbourethral / Cowper's Glands (Paired):</em> Secrete clear mucus for lubrication of penis during copulation.</li>
        <li><strong>Semen = Spermatozoa ($10\%$) + Seminal Plasma ($90\%$).</strong> Normal ejaculate volume: 2-3.5 mL containing <strong>200 to 300 million sperms</strong> ($60\%$ normal morphology, $40\%$ vigorous motility).</li>
      </ul>
    </li>
  </ul>
</div>

<div class="concept-card">
  <div class="card-label">FEMALE REPRODUCTIVE SYSTEM</div>
  <ul>
    <li><strong>Ovaries:</strong> Primary female sex organs producing ovum and steroid hormones (estrogen, progesterone). Peripheral cortex contains ovarian follicles, central medulla contains blood vessels and nerves.</li>
    <li><strong>Oviducts / Fallopian Tubes ($10\text{--}12\text{ cm}$):</strong>
      <ol>
        <li><em>Infundibulum:</em> Funnel-shaped part closest to ovary with finger-like projections called <strong>fimbriae</strong> that collect ovum after ovulation.</li>
        <li><em>Ampulla:</em> Wider, curved middle portion; <strong>site of fertilization</strong>.</li>
        <li><em>Isthmus:</em> Narrow terminal lumen joining uterus.</li>
      </ol>
    </li>
    <li><strong>Uterus (Womb):</strong> Inverted pear-shaped organ supported by pelvic ligaments. Wall has 3 layers:
      <ol>
        <li><em>Perimetrium:</em> External thin membranous serosa.</li>
        <li><em>Myometrium:</em> Middle thick layer of smooth muscle; exhibits strong rhythmic contractions during parturition.</li>
        <li><em>Endometrium:</em> Inner glandular vascular lining; undergoes cyclical breakdown during menstrual cycles and hosts embryo implantation.</li>
      </ol>
    </li>
    <li><strong>Cervix & Vagina:</strong> Cervical canal + vagina constitute <strong>birth canal</strong>.</li>
    <li><strong>Mammary Glands:</strong> Paired secondary sexual structures with 15-20 mammary lobes containing alveoli $\to$ mammary tubules $\to$ mammary duct $\to$ ampulla $\to$ lactiferous duct.</li>
  </ul>
</div>

<div class="table-container">
  <div class="table-caption">NCERT Comparison: Spermatogenesis vs Oogenesis</div>
  <table class="notes-table">
    <thead>
      <tr><th>Feature</th><th>Spermatogenesis</th><th>Oogenesis</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>Initiation</strong></td><td>Begins at <em>puberty</em> due to surge in GnRH</td><td>Initiated during <em>embryonic development</em> stage (millions of oogonia formed before birth; none added after)</td></tr>
      <tr><td><strong>Meiotic Continuity</strong></td><td>Continuous division without pause</td><td>Arrests twice: Prophase I (diplotene) until puberty; Metaphase II until sperm entry</td></tr>
      <tr><td><strong>Yield per Mother Cell</strong></td><td>1 Primary Spermatocyte $\to$ <strong>4 equal functional sperms</strong></td><td>1 Primary Oocyte $\to$ <strong>1 functional ovum + 2 to 3 non-functional polar bodies</strong></td></tr>
      <tr><td><strong>Cytokinesis</strong></td><td>Equal cytoplasmic division</td><td>Highly unequal cytoplasmic division (ovum retains cytoplasm)</td></tr>
      <tr><td><strong>Cessation</strong></td><td>Continues into old age</td><td>Terminates at menopause (~45-50 years of age)</td></tr>
    </tbody>
  </table>
</div>

<div class="concept-card">
  <div class="card-label">MENSTRUAL CYCLE PHASES & HORMONAL ORCHESTRATION</div>
  <p>Reproductive cycle in female primates (monkeys, apes, humans) with a standard periodicity of $28\text{--}29\text{ days}$.</p>
  <ol>
    <li><strong>Menstrual Phase (Days 1–5):</strong> Breakdown of endometrial lining and rupture of blood vessels due to sudden drop in progesterone and estrogen when fertilization fails. Blood discharge: 50-80 mL.</li>
    <li><strong>Follicular / Proliferative Phase (Days 6–13):</strong> Pituitary gonadotropins (FSH & LH) increase gradually. FSH stimulates primary follicles to mature into Graafian follicles; growing follicles secrete <strong>Estrogen</strong>, which stimulates endometrial proliferation.</li>
    <li><strong>Ovulatory Phase (Day 14):</strong> Rapid secretion of LH reaches maximum mid-cycle peak called <strong>LH Surge</strong>. Induces rupture of Graafian follicle and release of secondary oocyte (<strong>Ovulation</strong>).</li>
    <li><strong>Luteal / Secretory Phase (Days 15–28):</strong> Ruptured Graafian follicle transforms into yellow endocrine body called <strong>Corpus Luteum</strong>, which secretes massive amounts of <strong>Progesterone</strong> (maintains endometrium for pregnancy). In absence of fertilization, corpus luteum degenerates into <em>Corpus Albicans</em>, progesterone plummets, triggering next menstruation.</li>
  </ol>
</div>

<div class="remember-box">
  <strong>FERTILIZATION, CLEAVAGE, IMPLANTATION & PARTURITION:</strong>
  <ul>
    <li><strong>Capacitation & Acrosome Reaction:</strong> Sperms undergo functional maturation in female genital tract. Acrosome releases hyaluronidase and acrosin (corona penetrating enzyme).</li>
    <li><strong>Block to Polyspermy:</strong> Sperm contact with <em>zona pellucida</em> induces membrane depolarization (fast block) followed by cortical granule exocytosis hardening zona pellucida (slow block), ensuring only one sperm fertilizes ovum.</li>
    <li><strong>Cleavage & Blastocyst:</strong> Zygote divides mitotically ($2 \to 4 \to 8 \to 16$ cells). 8-16 celled solid embryo = <strong>Morula</strong>. Fluid cavity forms <strong>Blastocyst</strong> with outer <em>Trophoblast</em> (attaches to endometrium for placenta formation) and <em>Inner Cell Mass (ICM)</em> (embryonic stem cells differentiating into 3 germ layers: Ectoderm, Mesoderm, Endoderm).</li>
    <li><strong>Placenta Endocrine Hormones:</strong> Secretes <strong>hCG</strong> (human chorionic gonadotropin), <strong>hPL</strong> (human placental lactogen), estrogens, progesterone. <em>Relaxin</em> is secreted by the ovary. (hCG, hPL, relaxin produced only during pregnancy).</li>
    <li><strong>Parturition Reflex:</strong> Initiated by fully developed fetus and placenta inducing mild uterine contractions called <strong>Foetal Ejection Reflex</strong>. Triggers release of <strong>Oxytocin</strong> from maternal posterior pituitary, which stimulates stronger contractions in a positive feedback loop.</li>
    <li><strong>Colostrum:</strong> Yellowish milk secreted in initial days containing abundant <strong>IgA antibodies</strong> providing passive natural immunity to the newborn.</li>
  </ul>
</div>
"""

    m02_revision = r"""
<div class="quick-revision-box">
  <h4>High-Yield Revision — Human Reproduction</h4>
  <ul>
    <li><strong>Testes:</strong> Temperature $2-2.5^\circ\text{C}$ lower in scrotum. Leydig cells secrete testosterone; Sertoli cells nourish germ cells and secrete Inhibin & ABP.</li>
    <li><strong>Sperm Anatomy:</strong> Acrosome (modified Golgi complex with lytic enzymes), Neck (proximal & distal centriole), Middle piece (spiral mitochondria / Nebenkern), Tail (axial filament).</li>
    <li><strong>Oogenesis Arrest:</strong> Primary oocytes arrested at Diplotene of Prophase I; Secondary oocytes arrested at Metaphase II, completed only upon sperm entry.</li>
    <li><strong>LH Surge:</strong> Mid-cycle (Day 14) peak of LH triggers ovulation of secondary oocyte.</li>
    <li><strong>Corpus Luteum:</strong> Secretes progesterone to sustain secretory endometrium. Degenerates if hCG signal absent.</li>
    <li><strong>Placental Hormones:</strong> hCG, hPL, Estrogen, Progesterone; Relaxin from ovary. hCG is the marker detected in pregnancy test kits.</li>
    <li><strong>Parturition:</strong> Positive feedback: Foetal ejection reflex $\to$ Maternal pituitary Oxytocin $\to$ Stronger myometrial contractions.</li>
  </ul>
</div>
"""

    m02_flashcards = [
      {"q": "Why are testes situated outside the abdominal cavity in the scrotum?", "a": "Scrotum maintains a temperature 2 to 2.5°C lower than internal body temperature, which is essential for normal spermatogenesis and sperm survival."},
      {"q": "What exact event triggers the completion of the second meiotic division in the human female?", "a": "The entry of a sperm into the secondary oocyte induces the completion of meiosis II, forming a haploid ovum (ootid) and a second polar body."},
      {"q": "Which specific hormone is responsible for triggering ovulation mid-cycle?", "a": "Luteinizing Hormone (LH); the rapid rise known as the LH surge around day 14 causes rupture of the Graafian follicle and release of the secondary oocyte."},
      {"q": "What is the structural difference between trophoblast and inner cell mass in a blastocyst?", "a": "The trophoblast is the outer epithelial layer that attaches to the endometrium and forms the embryonic part of the placenta. The inner cell mass contains pluripotent stem cells that give rise to all embryonic tissues."},
      {"q": "Name the hormones produced in women only during pregnancy.", "a": "Human Chorionic Gonadotropin (hCG), Human Placental Lactogen (hPL), and Relaxin (secreted by the ovary)."},
      {"q": "Why is colostrum considered indispensable for a newborn baby?", "a": "Colostrum is rich in secretory IgA antibodies, providing immediate passive immunity that protects the infant against gastrointestinal and respiratory pathogens."}
    ]

    m02_flow = [
      {"id": "h1", "title": "Gametogenesis", "badge": "Step 1", "desc": "Spermatogenesis in seminiferous tubules forms flagellated sperms; Oogenesis produces secondary oocyte arrested at Metaphase II."},
      {"id": "h2", "title": "Insemination & Capacitation", "badge": "Step 2", "desc": "Millions of sperms deposited in vagina; undergo capacitation and travel through cervix and uterus to the ampulla of fallopian tube."},
      {"id": "h3", "title": "Acrosome Reaction & Fertilization", "badge": "Step 3", "desc": "Sperm penetrates corona radiata and zona pellucida; blocks polyspermy; meiosis II finishes; pronuclear fusion forms 2n zygote."},
      {"id": "h4", "title": "Cleavage to Blastocyst", "badge": "Step 4", "desc": "Zygote cleaves into morula (8-16 cells), then hollow blastocyst with outer trophoblast and inner cell mass."},
      {"id": "h5", "title": "Implantation & Placentation", "badge": "Step 5", "desc": "Blastocyst embeds into endometrium on day 7; trophoblast chorionic villi interdigitate with uterine tissue to form placenta."},
      {"id": "h6", "title": "Gestation & Parturition", "badge": "Step 6", "desc": "9-month fetal development; foetal ejection reflex stimulates oxytocin release causing vigorous myometrial contractions and delivery."}
    ]

    m02_mindmap = {
      "id": "root", "title": "Human Reproduction", "icon": "👶", "children": [
        {"id": "male", "title": "Male System", "icon": "♂️", "children": [
          {"id": "m1", "title": "Testes & Scrotum (2-2.5°C cooler for spermatogenesis)"},
          {"id": "m2", "title": "Seminiferous tubules: Sertoli cells + Leydig cells (Androgens)"},
          {"id": "m3", "title": "Glands: Seminal vesicles (Fructose), Prostate, Bulbourethral"}
        ]},
        {"id": "female", "title": "Female System", "icon": "♀️", "children": [
          {"id": "f1", "title": "Ovaries, Oviducts (Infundibulum, Ampulla - fertilization site)"},
          {"id": "f2", "title": "Uterine wall: Perimetrium, Myometrium (Oxytocin target), Endometrium"},
          {"id": "f3", "title": "Menstrual cycle: Menstrual -> Follicular -> Ovulatory (LH surge) -> Luteal"}
        ]},
        {"id": "embryo", "title": "Fertilization & Development", "icon": "🔬", "children": [
          {"id": "e1", "title": "Acrosome reaction & Polyspermy block at Zona pellucida"},
          {"id": "e2", "title": "Morula (8-16 cells) -> Blastocyst (Trophoblast + ICM)"},
          {"id": "e3", "title": "Placental Hormones: hCG, hPL, Progesterone, Estrogen, Relaxin"},
          {"id": "e4", "title": "Parturition (Oxytocin positive feedback) & Lactation (Colostrum IgA)"}
        ]}
      ]
    }

    m02_pages = [
      {"page_num": 1, "text": "Human male reproduction: Testes situated in scrotum keeping temperature 2 to 2.5 degrees lower for spermatogenesis. 250 testicular lobules with seminiferous tubules. Leydig cells secrete androgens. Sertoli cells nourish germ cells. Seminal vesicles secrete fructose and prostaglandins."},
      {"page_num": 2, "text": "Female reproduction: Ovaries produce ova and estrogen/progesterone. Fallopian tube ampulla is the site of fertilization. Menstrual cycle phases: menstrual, follicular (estrogen rise), ovulatory (day 14 LH surge), and luteal (corpus luteum secretes progesterone)."},
      {"page_num": 3, "text": "Fertilization and embryonic development: Acrosomal reaction and cortical reaction block polyspermy. Zygote undergoes cleavage to morula and blastocyst. Trophoblast attaches for implantation. Placenta produces hCG, hPL, relaxin. Parturition driven by foetal ejection reflex and oxytocin."}
    ]

    topics.append({
      "id": "bio-ch02-human-reproduction",
      "title": "02. Human Reproduction",
      "subject": "bio",
      "subject_title": "Biology • Class 12",
      "reading_time_min": 15,
      "has_handwritten": False,
      "detailed_html": m02_detailed,
      "revision_html": m02_revision,
      "flashcards": m02_flashcards,
      "flow_data": m02_flow,
      "mindmap_data": m02_mindmap,
      "pages": m02_pages
    })

    # =========================================================================
    # MODULE 03: REPRODUCTIVE HEALTH
    # =========================================================================
    m03_detailed = r"""
<div class="topic-header">
  <span class="topic-num">UNIT VI • TOPIC 03 OF 13</span>
  <h3 class="topic-title">Reproductive Health</h3>
</div>

<div class="concept-card">
  <div class="card-label">REPRODUCTIVE HEALTH CONCEPTS & POPULATION EXPLOSION</div>
  <p>According to the World Health Organization (WHO), reproductive health means a total well-being in all aspects of reproduction: <strong>physical, emotional, behavioral, and social</strong>.</p>
  <ul>
    <li><strong>India's Pioneering Role:</strong> India was among the first countries in the world to initiate action plans and programs at a national level to attain total reproductive health: <strong>Family Planning</strong> initiated in <strong>1951</strong>, popularized as <strong>Reproductive and Child Health Care (RCH)</strong> programs.</li>
    <li><strong>Amniocentesis:</strong> Fetal sex determination and chromosomal defect diagnostic test based on chromosomal pattern in amniotic fluid cells. Statutory ban imposed on amniocentesis for sex determination to curb female foeticide.</li>
    <li><strong>Population Explosion Drivers:</strong> Rapid decline in death rate, Maternal Mortality Rate (MMR), Infant Mortality Rate (IMR), accompanied by an increase in the number of people in reproducible age.</li>
  </ul>
</div>

<div class="table-container">
  <div class="table-caption">NCERT Classification of Contraceptive Methods</div>
  <table class="notes-table">
    <thead>
      <tr><th>Category</th><th>Examples & Mode of Action</th><th>Key Features & Efficacy</th></tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Natural / Traditional</strong></td>
        <td>
          • <em>Periodic Abstinence:</em> Avoid coitus from day 10 to 17 of menstrual cycle (fertile period).<br>
          • <em>Coitus Interruptus:</em> Withdrawal of penis before ejaculation.<br>
          • <em>Lactational Amenorrhea:</em> Intense breastfeeding prevents ovulation for up to 6 months postpartum.
        </td>
        <td>Zero side effects, but high failure rate. No protection against STIs.</td>
      </tr>
      <tr>
        <td><strong>Barrier Methods</strong></td>
        <td>
          • <em>Condoms (e.g. Nirodh):</em> Thin rubber/latex sheath covering penis or vagina/cervix.<br>
          • <em>Diaphragms, Cervical Caps, Vaults:</em> Rubber barriers inserted into female tract to cover cervix.
        </td>
        <td>Condoms protect against <strong>both unwanted pregnancy and STIs/AIDS</strong>. Diaphragms are reusable; spermicidal creams/jellies boost efficiency.</td>
      </tr>
      <tr>
        <td><strong>Intrauterine Devices (IUDs)</strong></td>
        <td>
          1. <em>Non-medicated:</em> Lippes loop (promotes phagocytosis of sperms).<br>
          2. <em>Copper-releasing:</em> CuT, Cu7, Multiload 375 ($Cu^{2+}$ ions suppress sperm motility and fertilizing capacity).<br>
          3. <em>Hormone-releasing:</em> Progestasert, LNG-20 (makes uterus unsuitable for implantation and cervix hostile to sperms).
        </td>
        <td><strong>Most widely accepted contraceptive method</strong> in India for spacing children. Must be inserted by doctors/trained nurses.</td>
      </tr>
      <tr>
        <td><strong>Oral Contraceptive Pills</strong></td>
        <td>
          • Combined estrogen-progestogen or progestogen-only pills taken daily for 21 days starting within first 5 days of cycle.<br>
          • <strong>Saheli:</strong> Once-a-week non-steroidal pill (Centchroman) developed by CDRI Lucknow.
        </td>
        <td>Inhibit ovulation and implantation; alter quality of cervical mucus to retard sperm entry. Saheli has high contraceptive value with very few side effects.</td>
      </tr>
      <tr>
        <td><strong>Surgical / Sterilization</strong></td>
        <td>
          • <strong>Vasectomy:</strong> Small part of vas deferens removed or tied through small scrotal incision.<br>
          • <strong>Tubectomy:</strong> Small part of fallopian tube removed or tied through small abdominal/vaginal incision.
        </td>
        <td>Terminal, permanent methods blocking gamete transport. Highly effective, but <strong>reversibility is extremely poor</strong>.</td>
      </tr>
    </tbody>
  </table>
</div>

<div class="concept-card">
  <div class="card-label">MTP & SEXUALLY TRANSMITTED INFECTIONS (STIs)</div>
  <ul>
    <li><strong>Medical Termination of Pregnancy (MTP / Induced Abortion):</strong> Voluntary termination before full term. ~45 to 50 million MTPs performed globally each year (20% of conceived pregnancies).
      <ul>
        <li>Legalized in India in <strong>1971</strong> with strict conditions to avoid misuse. MTP Amendment Act 2017: Up to 12 weeks requires 1 registered medical practitioner opinion; 12 to 24 weeks requires 2 practitioners' opinion. Safest during <strong>first trimester (up to 12 weeks)</strong>.</li>
      </ul>
    </li>
    <li><strong>Sexually Transmitted Infections (STIs / VD / RTI):</strong>
      <ul>
        <li><em>Bacterial:</em> Gonorrhea (<em>Neisseria gonorrhoeae</em>), Syphilis (<em>Treponema pallidum</em>), Chlamydiasis.</li>
        <li><em>Viral:</em> <strong>Hepatitis B, Genital Herpes, HIV/AIDS</strong> (these three are <strong>not curable</strong>; others are completely curable if detected early).</li>
        <li><em>Protozoan:</em> Trichomoniasis (<em>Trichomonas vaginalis</em>).</li>
        <li>Hepatitis B and HIV can also transmit via infected blood transfusions, shared needles, and from mother to fetus. STIs can lead to Pelvic Inflammatory Diseases (PID), ectopic pregnancies, and infertility.</li>
      </ul>
    </li>
  </ul>
</div>

<div class="remember-box">
  <strong>INFERTILITY & ASSISTED REPRODUCTIVE TECHNOLOGIES (ART):</strong>
  <p>Inability to conceive even after 2 years of unprotected sexual cohabitation. Specialized techniques include:</p>
  <ul>
    <li><strong>IVF-ET (In Vitro Fertilization & Embryo Transfer — "Test Tube Baby"):</strong> Fertilization outside body in conditions similar to the body, followed by embryo transfer:
      <ul>
        <li><strong>ZIFT (Zygote Intra-Fallopian Transfer):</strong> Zygote or early embryo up to <strong>8 blastomeres</strong> transferred into Fallopian tube.</li>
        <li><strong>IUT (Intra-Uterine Transfer):</strong> Embryos with <strong>more than 8 blastomeres</strong> transferred directly into the uterus.</li>
      </ul>
    </li>
    <li><strong>GIFT (Gamete Intra-Fallopian Transfer):</strong> Transfer of an unfertilized ovum collected from donor into fallopian tube of female who cannot produce one but can provide suitable environment for fertilization and development.</li>
    <li><strong>ICSI (Intra-Cytoplasmic Sperm Injection):</strong> Specialized lab procedure in which a single sperm is directly micro-injected into the ovum to form an embryo.</li>
    <li><strong>AI / IUI (Artificial Insemination / Intra-Uterine Insemination):</strong> Semen collected from husband or donor is artificially introduced into vagina or uterus (IUI) when male partner has low sperm count (oligospermia) or inability to inseminate.</li>
  </ul>
</div>
"""

    m03_revision = r"""
<div class="quick-revision-box">
  <h4>High-Yield Revision — Reproductive Health</h4>
  <ul>
    <li><strong>RCH Programme:</strong> Launched in India (family planning 1951). Amniocentesis banned for sex determination.</li>
    <li><strong>IUDs:</strong> Non-medicated (Lippes loop); Cu-releasing (CuT, Cu7, Multiload 375 - suppress sperm motility); Hormone-releasing (Progestasert, LNG-20 - make uterus hostile).</li>
    <li><strong>Saheli:</strong> Once-a-week non-steroidal oral contraceptive developed by CDRI, Lucknow.</li>
    <li><strong>MTP:</strong> Legalized in 1971; safest in first trimester (up to 12 weeks).</li>
    <li><strong>Incurable STIs:</strong> Hepatitis-B, Genital Herpes, HIV/AIDS.</li>
    <li><strong>ART Thresholds:</strong> ZIFT = embryo $\le 8$ blastomeres into fallopian tube; IUT = embryo $> 8$ blastomeres into uterus; GIFT = transfer of gamete (ovum); ICSI = direct sperm microinjection into ovum cytoplasm.</li>
  </ul>
</div>
"""

    m03_flashcards = [
      {"q": "How do copper-releasing IUDs (like CuT and Multiload 375) prevent contraception?", "a": "Released copper ions suppress sperm motility and inhibit the fertilizing capacity of spermatozoa, while promoting phagocytosis of sperms within the uterus."},
      {"q": "What makes the oral contraceptive 'Saheli' unique compared to traditional pills?", "a": "Saheli is a non-steroidal formulation (Centchroman) taken once a week, developed by CDRI Lucknow. It has high contraceptive efficacy with very few hormonal side effects."},
      {"q": "What is the critical distinction between ZIFT and IUT in assisted reproduction?", "a": "In ZIFT, a zygote or early embryo with up to 8 blastomeres is transferred into the fallopian tube. In IUT, an embryo with more than 8 blastomeres is transferred directly into the uterus."},
      {"q": "Which three Sexually Transmitted Infections are considered non-curable?", "a": "Hepatitis-B, Genital Herpes, and HIV/AIDS."},
      {"q": "Under what condition is Gamete Intra-Fallopian Transfer (GIFT) recommended?", "a": "For females who cannot produce viable ova due to ovarian dysfunction, but possess a healthy fallopian tube and uterus suitable for fertilization and embryonic gestation."},
      {"q": "Why is amniocentesis legally banned for sex determination in India?", "a": "To stop the alarming increase in female foeticide and maintain a balanced sex ratio in the population."}
    ]

    m03_flow = [
      {"id": "r1", "title": "Awareness & Education", "badge": "Step 1", "desc": "RCH programs educate youth on reproductive anatomy, puberty changes, safe sexual practices, and STI prevention."},
      {"id": "r2", "title": "Contraceptive Selection", "badge": "Step 2", "desc": "Couple chooses ideal method: spacing (IUDs, Pills like Saheli, Barriers) or permanent terminal sterilization (Vasectomy/Tubectomy)."},
      {"id": "r3", "title": "STI Screening & MTP", "badge": "Step 3", "desc": "Early diagnosis and treatment of curable STIs; safe legal MTP within 12 weeks in case of contraceptive failure or maternal risk."},
      {"id": "r4", "title": "Infertility Diagnosis", "badge": "Step 4", "desc": "Clinical evaluation of both partners to diagnose ovulatory failure, tubal blockage, or oligospermia."},
      {"id": "r5", "title": "ART Implementation", "badge": "Step 5", "desc": "Application of specific technology: ZIFT (<=8 blastomeres), IUT (>8 blastomeres), GIFT (ovum transfer), ICSI (direct microinjection), or IUI."}
    ]

    m03_mindmap = {
      "id": "root", "title": "Reproductive Health", "icon": "🛡️", "children": [
        {"id": "birth", "title": "Birth Control", "icon": "💊", "children": [
          {"id": "b1", "title": "Natural: Periodic abstinence, Coitus interruptus, Lactational amenorrhea"},
          {"id": "b2", "title": "Barriers: Condoms (Nirodh - protects from STIs), Diaphragms"},
          {"id": "b3", "title": "IUDs: Non-medicated (Lippes), Cu-releasing (CuT), Hormone (LNG-20)"},
          {"id": "b4", "title": "Pills: Saheli (non-steroidal, CDRI), Sterilization: Vasectomy & Tubectomy"}
        ]},
        {"id": "sti", "title": "STIs & MTP", "icon": "⚠️", "children": [
          {"id": "s1", "title": "Incurable STIs: HIV, Hepatitis-B, Genital Herpes"},
          {"id": "s2", "title": "Curable STIs: Syphilis, Gonorrhea, Chlamydiasis, Trichomoniasis"},
          {"id": "s3", "title": "MTP Act 1971 (2017 amendment): Safest up to 12 weeks"}
        ]},
        {"id": "art", "title": "Infertility & ART", "icon": "🧪", "children": [
          {"id": "a1", "title": "IVF-ET: ZIFT (<=8 blastomeres in tube) vs IUT (>8 in uterus)"},
          {"id": "a2", "title": "GIFT: Gamete transfer into fallopian tube"},
          {"id": "a3", "title": "ICSI: Direct sperm injection into ovum"},
          {"id": "a4", "title": "IUI / AI: Artificial insemination for male oligospermia"}
        ]}
      ]
    }

    m03_pages = [
      {"page_num": 1, "text": "Reproductive Health and contraception: RCH programs in India. Amniocentesis banned for sex determination. Natural methods include periodic abstinence and lactational amenorrhea. Barrier methods like condoms protect against STIs."},
      {"page_num": 2, "text": "IUD types: Non-medicated Lippes loop, copper-releasing CuT and Multiload 375 that suppress sperm motility, hormone-releasing LNG-20 that makes uterus hostile. Saheli non-steroidal pill from CDRI Lucknow. Permanent vasectomy and tubectomy."},
      {"page_num": 3, "text": "MTP legal aspects: safe up to 12 weeks. Non-curable STIs: Hepatitis-B, Genital Herpes, HIV. Infertility treatments: IVF with ZIFT (up to 8 blastomeres in fallopian tube) and IUT (over 8 blastomeres in uterus), GIFT, ICSI microinjection, and IUI artificial insemination."}
    ]

    topics.append({
      "id": "bio-ch03-reproductive-health",
      "title": "03. Reproductive Health",
      "subject": "bio",
      "subject_title": "Biology • Class 12",
      "reading_time_min": 12,
      "has_handwritten": False,
      "detailed_html": m03_detailed,
      "revision_html": m03_revision,
      "flashcards": m03_flashcards,
      "flow_data": m03_flow,
      "mindmap_data": m03_mindmap,
      "pages": m03_pages
    })

    # =========================================================================
    # MODULE 04: PRINCIPLES OF INHERITANCE AND VARIATION
    # =========================================================================
    m04_detailed = r"""
<div class="topic-header">
  <span class="topic-num">UNIT VII • TOPIC 04 OF 13</span>
  <h3 class="topic-title">Principles of Inheritance and Variation</h3>
</div>

<div class="concept-card">
  <div class="card-label">MENDELIAN GENETICS & LAWS OF INHERITANCE</div>
  <p>Gregor Johann Mendel conducted hybridization experiments on garden peas (<em>Pisum sativum</em>) for 7 years (1856–1863) and proposed laws of inheritance.</p>
  <ul>
    <li><strong>7 Contrasting Traits in Garden Pea:</strong> Stem height (Tall/Dwarf), Flower color (Violet/White), Flower position (Axial/Terminal), Pod shape (Inflated/Constricted), Pod color (Green/Yellow), Seed shape (Round/Wrinkled), Seed color (Yellow/Green).</li>
    <li><strong>Monohybrid Cross:</strong> Cross between true-breeding tall ($TT$) and dwarf ($tt$) plants:
      <ul>
        <li>$F_1$ generation: All Tall ($Tt$).</li>
        <li>$F_2$ generation: Phenotypic ratio $3\text{ Tall} : 1\text{ Dwarf}$ ($3:1$); Genotypic ratio $1\,TT : 2\,Tt : 1\,tt$ ($1:2:1$).</li>
        <li><strong>Test Cross:</strong> Crossing an organism showing dominant phenotype (genotype unknown: $TT$ or $Tt$) with homozygous recessive parent ($tt$). If progeny are $100\%$ dominant, unknown is homozygous $TT$; if $1:1$ dominant to recessive, unknown is heterozygous $Tt$.</li>
      </ul>
    </li>
    <li><strong>Mendel's First Law (Law of Dominance):</strong> Characters are controlled by discrete units called factors (genes). Factors occur in pairs. In a dissimilar pair, one factor dominates (dominant) the other (recessive).</li>
    <li><strong>Mendel's Second Law (Law of Segregation):</strong> Alleles do not show blending; both characters are recovered in $F_2$. During gamete formation, paired factors segregate so that a gamete receives only one allele with equal probability ("Purity of Gametes"). Universal law with <em>no exceptions</em>.</li>
  </ul>
</div>

<div class="concept-card">
  <div class="card-label">DEVIATIONS FROM MENDELIAN RATIOS</div>
  <ul>
    <li><strong>Incomplete Dominance:</strong> $F_1$ phenotype is intermediate between the two homozygous parents.
      <ul>
        <li>Classic Example: Dog flower / Snapdragon (<em>Antirrhinum majus</em>) and 4 o'clock plant (<em>Mirabilis jalapa</em>). Red ($RR$) $\times$ White ($rr$) $\to$ $F_1$ Pink ($Rr$).</li>
        <li>$F_2$ Ratio: <strong>Phenotypic ratio = Genotypic ratio = $1\text{ Red} : 2\text{ Pink} : 1\text{ White}$ ($1:2:1$)</strong>.</li>
      </ul>
    </li>
    <li><strong>Co-dominance:</strong> Both alleles express simultaneously in heterozygote.
      <ul>
        <li>Classic Example: <strong>ABO Blood Grouping in Humans</strong>, controlled by gene $I$ on chromosome 9 with 3 alleles: $I^A, I^B, i$. $I^A$ and $I^B$ produce different surface sugar polymers; $i$ produces none.</li>
        <li>$I^A$ and $I^B$ are completely dominant over $i$, but when $I^A$ and $I^B$ are present together ($I^A I^B$), both express producing <strong>AB blood type</strong>.</li>
        <li>Population exhibits <strong>6 genotypes</strong> and <strong>4 phenotypes</strong> (A, B, AB, O). (Also illustrates <em>Multiple Allelism</em>).</li>
      </ul>
    </li>
    <li><strong>Dihybrid Cross & Law of Independent Assortment:</strong> Cross involving two pairs of contrasting traits (Round-Yellow $RRYY$ $\times$ Wrinkled-Green $rryy$).
      <ul>
        <li>$F_2$ Phenotypic ratio: <strong>$9\text{ Round-Yellow} : 3\text{ Round-Green} : 3\text{ Wrinkled-Yellow} : 1\text{ Wrinkled-Green}$ ($9:3:3:1$)</strong>.</li>
        <li><em>Law:</em> When two pairs of traits are combined in a hybrid, segregation of one pair of characters is independent of the other pair. (Applies only to genes located on different chromosomes or far apart).</li>
      </ul>
    </li>
  </ul>
</div>

<div class="concept-card">
  <div class="card-label">CHROMOSOMAL THEORY, LINKAGE & SEX DETERMINATION</div>
  <ul>
    <li><strong>Chromosomal Theory of Inheritance (Sutton & Boveri, 1902):</strong> Chromosomes occur in pairs, segregate at meiosis, and assort independently just like Mendelian factors. Chromosome movement during anaphase explains Mendel's laws.</li>
    <li><strong>Thomas Hunt Morgan's Drosophila Experiments:</strong> Verified chromosomal theory using fruit fly <em>Drosophila melanogaster</em> (short 2-week life cycle, easy synthetic culture, clear dimorphism, high progeny).
      <ul>
        <li><strong>Linkage:</strong> Physical association of genes on the same chromosome. Linked genes do not assort independently and deviate from $9:3:3:1$.</li>
        <li>Tight linkage: Genes for yellow body ($y$) and white eyes ($w$) showed only <strong>$1.3\%$ recombination</strong>.</li>
        <li>Loose linkage: White eyes ($w$) and miniature wings ($m$) showed <strong>$37.2\%$ recombination</strong>.</li>
        <li><strong>Genetic Mapping:</strong> Alfred Sturtevant used recombination frequency between gene pairs as a measure of distance on chromosomes ($1\%\text{ recombination} = 1\text{ map unit / centimorgan}$).</li>
      </ul>
    </li>
    <li><strong>Sex Determination Systems:</strong>
      <ul>
        <li><em>XX-XY Type (Male heterogamety):</em> Humans and <em>Drosophila</em>. Male produces 50% X and 50% Y sperms.</li>
        <li><em>XX-XO Type (Male heterogamety):</em> Grasshoppers and insects. Male has only one X chromosome ($XO$).</li>
        <li><em>ZZ-ZW Type (Female heterogamety):</em> Birds. Female is $ZW$ (heterogametic); male is $ZZ$ (homogametic).</li>
        <li><em>Haplodiploidy:</em> Honeybees. Female (Queen/Worker) develops from fertilized diploid egg ($2n=32$); Male (Drone) develops parthenogenetically from unfertilized haploid egg ($n=16$). Drones produce sperms by mitosis; they have no father and cannot have sons, but have a grandfather and can have grandsons!</li>
      </ul>
    </li>
  </ul>
</div>

<div class="remember-box">
  <strong>GENETIC DISORDERS IN HUMANS:</strong>
  <p><strong>1. Mendelian Disorders (Altered single gene):</strong></p>
  <ul>
    <li><strong>Hemophilia (Sex-linked Recessive):</strong> Royal disease (Queen Victoria pedigree). Defect in blood clotting cascade; simple cut causes non-stop bleeding. Heterozygous female is carrier; rarely manifests in females because mother must be carrier and father hemophilic.</li>
    <li><strong>Sickle-Cell Anemia (Autosomal Recessive):</strong> Point mutation in $\beta$-globin gene on chromosome 11. Single base substitution: <strong>$\text{GAG} \to \text{GUG}$</strong> at 6th codon, substituting <strong>Glutamic acid (polar) with Valine (hydrophobic)</strong>. Mutant Hb undergoes polymerization under low oxygen tension causing RBCs to become sickle-shaped. Heterozygotes ($Hb^A Hb^S$) show resistance to malaria!</li>
    <li><strong>Phenylketonuria (PKU, Autosomal Recessive):</strong> Inborn error of metabolism; lack of enzyme <em>phenylalanine hydroxylase</em> leads to accumulation of phenylalanine converted into phenylpyruvic acid. Causes severe mental retardation and hypopigmentation.</li>
    <li><strong>Thalassemia (Autosomal Recessive):</strong> Quantitative defect in globin chain synthesis. $\alpha$-Thalassemia (controlled by $HBA1$ and $HBA2$ on chromosome 16); $\beta$-Thalassemia (controlled by $HBB$ on chromosome 11).</li>
  </ul>
  <p><strong>2. Chromosomal Disorders (Aneuploidy / Non-disjunction):</strong></p>
  <ul>
    <li><strong>Down's Syndrome (Trisomy 21, $2n+1 = 47$):</strong> Described by Langdon Down (1866). Short stature, small round head, furrowed tongue, partially open mouth, broad palm with characteristic palm crease (simian crease), delayed mental development.</li>
    <li><strong>Klinefelter's Syndrome ($47, XXY$):</strong> Extra X chromosome in male. Overall masculine development with feminine traits: enlarged breasts (<strong>Gynecomastia</strong>), tall stature, sterile.</li>
    <li><strong>Turner's Syndrome ($45, XO$):</strong> Monosomy of X chromosome in female. Sterile female with rudimentary ovaries, lack of secondary sexual characteristics, short stature, webbed neck.</li>
  </ul>
</div>
"""

    m04_revision = r"""
<div class="quick-revision-box">
  <h4>High-Yield Revision — Principles of Inheritance</h4>
  <ul>
    <li><strong>Mendel's Pea Crosses:</strong> Monohybrid $F_2 = 3:1$ (pheno), $1:2:1$ (geno). Dihybrid $F_2 = 9:3:3:1$.</li>
    <li><strong>Incomplete Dominance:</strong> Snapdragon (<em>Antirrhinum</em>) $F_2$ pheno = geno = $1:2:1$ (Pink heterozygote).</li>
    <li><strong>ABO Blood Group:</strong> Co-dominance of $I^A$ and $I^B$; 3 alleles, 6 genotypes, 4 phenotypes.</li>
    <li><strong>Linkage:</strong> Discovered by Morgan in Drosophila. Inversely proportional to recombination frequency. Map units = % recombination (Sturtevant).</li>
    <li><strong>Haplodiploidy:</strong> Honeybees ($2n=32$ female, $n=16$ drone male formed by parthenogenesis).</li>
    <li><strong>Sickle-Cell Mutation:</strong> GAG $\to$ GUG at codon 6 of $\beta$-globin chain (Glutamic acid $\to$ Valine).</li>
    <li><strong>Chromosomal Aneuploidies:</strong> Down's ($47, +21$); Klinefelter's ($47, XXY$ - sterile male with gynecomastia); Turner's ($45, XO$ - sterile female with rudimentary ovaries).</li>
  </ul>
</div>
"""

    m04_flashcards = [
      {"q": "What is the exact molecular point mutation that causes Sickle-Cell Anemia?", "a": "A single nucleotide transversion from GAG to GUG at the 6th codon of the beta-globin gene, which substitutes glutamic acid with valine in the polypeptide chain."},
      {"q": "Why is the Law of Segregation considered universal while Independent Assortment is not?", "a": "Alleles always separate cleanly during meiosis in gamete formation without blending. Independent assortment fails when two genes are physically linked on the same chromosome."},
      {"q": "In snapdragons (Antirrhinum majus), what are the phenotypic and genotypic ratios in the F2 generation?", "a": "Both phenotypic and genotypic ratios are identical: 1 Red (RR) : 2 Pink (Rr) : 1 White (rr) due to incomplete dominance."},
      {"q": "How does sex determination in honeybees (haplodiploidy) lead to males having no fathers?", "a": "Drones are haploid (n=16) and develop parthenogenetically from unfertilized eggs laid by the queen. Thus, a drone has only a mother and grandfather, but no father or sons."},
      {"q": "What is the chromosomal karyotype and clinical presentation of Klinefelter's syndrome?", "a": "Karyotype is 47, XXY. Affected individuals are males with overall masculine development but exhibit feminine characteristics such as gynecomastia (breast development) and are sterile."},
      {"q": "How did Alfred Sturtevant utilize Morgan's linkage findings to construct genetic maps?", "a": "He established that the frequency of genetic recombination between gene pairs is directly proportional to the physical distance separating them on the chromosome (1% recombination = 1 centimorgan)."}
    ]

    m04_flow = [
      {"id": "g1", "title": "Mendelian Hybridization", "badge": "Step 1", "desc": "Pure breeding lines crossed; F1 shows dominant trait; F2 segregates 3:1 phenotypic and 1:2:1 genotypic."},
      {"id": "g2", "title": "Non-Mendelian Ratios", "badge": "Step 2", "desc": "Identification of incomplete dominance (1:2:1), codominance (ABO blood groups), and multiple allelism."},
      {"id": "g3", "title": "Chromosomal Theory", "badge": "Step 3", "desc": "Sutton & Boveri link gene segregation to meiotic chromosome behavior; Morgan discovers sex-linkage in Drosophila."},
      {"id": "g4", "title": "Linkage & Recombination", "badge": "Step 4", "desc": "Proximity of genes on chromosomes limits crossing over; Sturtevant builds first chromosome maps using recombinant frequencies."},
      {"id": "g5", "title": "Pedigree Analysis", "badge": "Step 5", "desc": "Tracing inheritance of Mendelian traits (autosomal dominant/recessive, X-linked) across human family generations."},
      {"id": "g6", "title": "Genetic Pathology", "badge": "Step 6", "desc": "Point mutations (Sickle-cell GAG->GUG, Thalassemia) and chromosomal non-disjunction (Down 47,+21, Klinefelter 47,XXY, Turner 45,XO)."}
    ]

    m04_mindmap = {
      "id": "root", "title": "Principles of Inheritance", "icon": "🧬", "children": [
        {"id": "mendel", "title": "Mendel's Principles", "icon": "🌱", "children": [
          {"id": "me1", "title": "Monohybrid: Law of Dominance & Law of Segregation (Universal)"},
          {"id": "me2", "title": "Dihybrid: Law of Independent Assortment (9:3:3:1)"},
          {"id": "me3", "title": "Test cross (Dominant x Homozygous recessive -> 1:1 or 100%)"}
        ]},
        {"id": "extensions", "title": "Deviations & Linkage", "icon": "🔀", "children": [
          {"id": "ex1", "title": "Incomplete dominance (Snapdragon pink 1:2:1)"},
          {"id": "ex2", "title": "Codominance & Multiple alleles (ABO blood group)"},
          {"id": "ex3", "title": "Morgan's Drosophila: Linkage vs Recombination, Gene mapping"}
        ]},
        {"id": "sex", "title": "Sex Determination", "icon": "🚻", "children": [
          {"id": "sx1", "title": "XX-XY (Human, Drosophila) & XX-XO (Grasshopper)"},
          {"id": "sx2", "title": "ZZ-ZW (Birds female heterogamety)"},
          {"id": "sx3", "title": "Haplodiploidy in Honeybees (Female 2n=32, Male n=16)"}
        ]},
        {"id": "disorders", "title": "Genetic Disorders", "icon": "🏥", "children": [
          {"id": "d1", "title": "Mendelian: Sickle-cell (GAG->GUG), Hemophilia (X-linked), PKU"},
          {"id": "d2", "title": "Aneuploidy: Down (Trisomy 21), Klinefelter (XXY), Turner (XO)"}
        ]}
      ]
    }

    m04_pages = [
      {"page_num": 1, "text": "Mendel's experiments with Pisum sativum 7 traits. Monohybrid cross 3:1 phenotypic and 1:2:1 genotypic ratio. Test cross confirms zygosity. Law of Segregation is universal. Incomplete dominance in snapdragon produces 1:2:1 pink flowers. Codominance in ABO blood grouping with alleles IA, IB, and i."},
      {"page_num": 2, "text": "Chromosomal theory of inheritance by Sutton and Boveri. Thomas Hunt Morgan's experiments on Drosophila melanogaster proving sex linkage. Tight linkage in yellow-white 1.3% recombination vs loose linkage white-miniature 37.2%. Sturtevant's chromosome mapping. Sex determination in humans, birds ZZ-ZW, and honeybee haplodiploidy."},
      {"page_num": 3, "text": "Genetic disorders: Sickle-cell anemia point mutation GAG to GUG at 6th codon of beta-globin replacing glutamic acid with valine. Hemophilia sex-linked recessive. Down syndrome trisomy 21 with 47 chromosomes. Klinefelter syndrome 47 XXY with gynecomastia. Turner syndrome 45 XO with sterile rudimentary ovaries."}
    ]

    topics.append({
      "id": "bio-ch04-principles-inheritance",
      "title": "04. Principles of Inheritance and Variation",
      "subject": "bio",
      "subject_title": "Biology • Class 12",
      "reading_time_min": 16,
      "has_handwritten": False,
      "detailed_html": m04_detailed,
      "revision_html": m04_revision,
      "flashcards": m04_flashcards,
      "flow_data": m04_flow,
      "mindmap_data": m04_mindmap,
      "pages": m04_pages
    })

    # =========================================================================
    # MODULE 05: MOLECULAR BASIS OF INHERITANCE
    # =========================================================================
    m05_detailed = r"""
<div class="topic-header">
  <span class="topic-num">UNIT VII • TOPIC 05 OF 13</span>
  <h3 class="topic-title">Molecular Basis of Inheritance</h3>
</div>

<div class="concept-card">
  <div class="card-label">DNA STRUCTURE & HISTONE PACKAGING</div>
  <p>Deoxyribonucleic acid (DNA) is the genetic material in most organisms. A polynucleotide chain is built from nucleotide monomers: <strong>Nitrogenous base + Pentose sugar + Phosphate group</strong>.</p>
  <ul>
    <li><strong>Chemical Anatomy:</strong>
      <ul>
        <li>Purines: Adenine (A), Guanine (G); Pyrimidines: Cytosine (C), Thymine (T) in DNA / Uracil (U) in RNA.</li>
        <li>Base linked to sugar at $C_1'$ via <strong>N-glycosidic bond</strong> forming nucleoside. Phosphate linked to $C_5'$ OH via <strong>phosphoester bond</strong> forming nucleotide.</li>
        <li>Successive nucleotides linked by <strong>$3'\text{--}5'$ phosphodiester bonds</strong>. Backbone is composed of sugar and phosphate.</li>
      </ul>
    </li>
    <li><strong>Watson-Crick Double Helix Model (1953):</strong> Based on Rosalind Franklin & Maurice Wilkins' X-ray diffraction data:
      <ol>
        <li>Two polynucleotide chains running in <strong>antiparallel polarity</strong> ($5'\to 3'$ and $3'\to 5'$).</li>
        <li>Bases pair via hydrogen bonds: <strong>$A = T$ (2 H-bonds)</strong> and <strong>$G \equiv C$ (3 H-bonds)</strong>.</li>
        <li>Right-handed helix pitch = <strong>$3.4\text{ nm}$</strong>; ~10 base pairs per turn; distance between adjacent bp = <strong>$0.34\text{ nm}$</strong>.</li>
        <li><strong>Erwin Chargaff's Rules:</strong> For double-stranded DNA, $[A] = [T]$ and $[G] = [C]$; ratio $\frac{[A+G]}{[T+C]} = 1$. Base ratio $\frac{A+T}{G+C}$ is species-specific.</li>
      </ol>
    </li>
    <li><strong>DNA Packaging in Eukaryotes:</strong> Human diploid genome length = $2 \times 3.3 \times 10^9\text{ bp} \times 0.34 \times 10^{-9}\text{ m} \approx \mathbf{2.2\text{ meters}}$, packaged inside a $10^{-6}\text{ m}$ nucleus:
      <ul>
        <li><strong>Histone Octamer:</strong> Positively charged basic proteins rich in <strong>Lysine and Arginine</strong> residues ($H_2A, H_2B, H_3, H_4 \times 2$).</li>
        <li><strong>Nucleosome:</strong> Negatively charged DNA ($200\text{ bp}$) wraps around histone octamer. $H_1$ histone seals the exit.</li>
        <li>Beads-on-string structure $\to$ Solenoid chromatin fiber ($30\text{ nm}$) $\to$ Metaphase chromosomes with Non-Histone Chromosomal (NHC) proteins.</li>
        <li><em>Euchromatin:</em> Loosely packed, lightly staining, transcriptionally active. <em>Heterochromatin:</em> Densely packed, darkly staining, transcriptionally inactive.</li>
      </ul>
    </li>
  </ul>
</div>

<div class="concept-card">
  <div class="card-label">SEARCH FOR GENETIC MATERIAL & MESELSON-STAHL REPLICATION</div>
  <ul>
    <li><strong>Griffith's Transformation Experiment (1928):</strong> <em>Streptococcus pneumoniae</em> smooth virulent S-strain (mucopolysaccharide coat) and rough non-virulent R-strain. Mice injected with Heat-killed S + Live R contracted pneumonia and died; live S bacteria recovered. Proved a "Transforming Principle" transferred from heat-killed S to R.</li>
    <li><strong>Avery, MacLeod & McCarty (1944):</strong> Purified biochemicals (proteins, RNA, DNA). Proteases and RNases did not affect transformation; only <strong>DNase</strong> inhibited transformation, proving DNA is the transforming genetic material.</li>
    <li><strong>Hershey-Chase Bacteriophage Experiment (1952):</strong> Conclusive proof using $T_2$ bacteriophage and <em>E. coli</em>:
      <ul>
        <li>Grew phages in radioactive $^{35}\text{S}$ (labels protein coat) and $^{32}\text{P}$ (labels DNA core).</li>
        <li>Infection $\to$ Blending (detached viral coats) $\to$ Centrifugation.</li>
        <li>Pellet (bacterial cells) showed radioactivity only with $^{32}\text{P}$; supernatant showed $^{35}\text{S}$. Proved viral DNA entered cells.</li>
      </ul>
    </li>
    <li><strong>Semiconservative DNA Replication (Meselson & Stahl, 1958):</strong>
      <ul>
        <li>Grew <em>E. coli</em> in $^{15}\text{NH}_4\text{Cl}$ (heavy isotope) $\to$ all DNA heavy ($^{15}\text{N}/^{15}\text{N}$).</li>
        <li>Transferred to normal $^{14}\text{N}$ medium: After 1 generation ($20\text{ min}$), all DNA was hybrid intermediate ($^{15}\text{N}/^{14}\text{N}$). After 2 generations ($40\text{ min}$), $50\%$ hybrid and $50\%$ light ($^{14}\text{N}/^{14}\text{N}$). Analyzed by $\text{CsCl}$ density gradient centrifugation.</li>
        <li>Taylor (1958) demonstrated semiconservative replication in chromosomes of <em>Vicia faba</em> using radioactive tritiated thymidine.</li>
      </ul>
    </li>
    <li><strong>Replication Machinery:</strong> DNA-dependent DNA Polymerase synthesizes strictly in $5'\to 3'$ direction at high speed ($2000\text{ bp/sec}$). Leading strand synthesized continuously; Lagging strand synthesized discontinuously as <strong>Okazaki fragments</strong>, joined by <strong>DNA Ligase</strong>. Initiated at specific site called <strong>Origin of Replication (ori)</strong>.</li>
  </ul>
</div>

<div class="concept-card">
  <div class="card-label">TRANSCRIPTION, GENETIC CODE & TRANSLATION</div>
  <ul>
    <li><strong>Transcription Unit:</strong> Promoter (binding site for RNA polymerase) $\to$ Structural gene $\to$ Terminator.
      <ul>
        <li>Template strand has $3'\to 5'$ polarity; Coding strand has $5'\to 3'$ polarity (same sequence as mRNA, with T instead of U).</li>
        <li><em>Prokaryotes:</em> Single RNA polymerase binds promoter with <strong>sigma ($\sigma$) initiation factor</strong>; terminates with <strong>rho ($\rho$) factor</strong>. Polycistronic mRNA.</li>
        <li><em>Eukaryotes (Monocistronic):</em> 3 RNA polymerases: RNA Pol I (rRNAs: 28S, 18S, 5.8S), <strong>RNA Pol II (hnRNA / precursor of mRNA)</strong>, RNA Pol III (tRNA, 5S rRNA, snRNA).</li>
        <li><strong>Post-Transcriptional Modifications of hnRNA:</strong>
          <ol>
            <li><em>Splicing:</em> Non-coding intervening sequences (<strong>Introns</strong>) removed; coding sequences (<strong>Exons</strong>) joined in specific order by spliceosomes.</li>
            <li><em>Capping:</em> Unusual nucleotide methyl guanosine triphosphate ($\text{m}^7\text{Gppp}$) added to $5'$ end.</li>
            <li><em>Tailing:</em> Polyadenylation; 200–300 adenylate residues added to $3'$ end.</li>
          </ol>
        </li>
      </ul>
    </li>
    <li><strong>The Genetic Code (Gamow, Nirenberg, Khorana):</strong>
      <ul>
        <li><strong>Triplet:</strong> 64 codons total; 61 code for amino acids; 3 stop codons (UAA, UAG, UGA - ochre, amber, opal).</li>
        <li><strong>Degenerate:</strong> Most amino acids coded by more than one codon (except Met and Trp).</li>
        <li><strong>Unambiguous:</strong> One codon codes for only one specific amino acid.</li>
        <li><strong>Universal:</strong> Same codon codes for same amino acid from bacteria to human (UUU = Phenylalanine).</li>
        <li><strong>AUG Dual Function:</strong> Codes for <strong>Methionine</strong> and acts as <strong>Initiator codon</strong>.</li>
        <li><strong>tRNA (Adapter Molecule):</strong> Cloverleaf 2D model (inverted-L 3D structure); contains anticodon loop complementary to codon and amino acid acceptor end at $3'$ ($\text{CCA}-3'$).</li>
      </ul>
    </li>
    <li><strong>Translation Steps:</strong> Aminoacylation of tRNA (charging with ATP) $\to$ Initiation (ribosome binds mRNA at AUG) $\to$ Elongation (peptide bond formation catalyzed by <strong>23S rRNA</strong> ribozyme in bacteria) $\to$ Termination (release factor binds stop codon).</li>
  </ul>
</div>

<div class="remember-box">
  <strong>LAC OPERON & HUMAN GENOME PROJECT (HGP):</strong>
  <ul>
    <li><strong>Lac Operon (Francois Jacob & Jacques Monod):</strong> Polycistronic structural genes regulated by a common promoter and regulatory gene in <em>E. coli</em>:
      <ul>
        <li><strong>$i$ gene:</strong> Synthesizes constitutive Repressor protein.</li>
        <li><strong>$z$ gene:</strong> Codes for <strong>$\beta$-galactosidase</strong> (hydrolyzes lactose into galactose + glucose).</li>
        <li><strong>$y$ gene:</strong> Codes for <strong>Permease</strong> (increases cell membrane permeability to $\beta$-galactosides).</li>
        <li><strong>$a$ gene:</strong> Codes for <strong>Transacetylase</strong>.</li>
        <li><strong>Regulation:</strong> In absence of lactose, repressor binds operator ($o$), blocking RNA polymerase. In presence of inducer (<strong>Lactose / Allolactose</strong>), inducer binds repressor, inactivating it; RNA polymerase transcribes the operon. Example of <em>negative inducible control</em>.</li>
      </ul>
    </li>
    <li><strong>Human Genome Project (HGP, 1990–2003):</strong> Coordinated by US Dept of Energy & Wellcome Trust:
      <ul>
        <li>Human genome contains <strong>$3164.7\text{ million}$ base pairs</strong>. Average gene size: 3000 bases (largest gene: <em>Dystrophin</em> at $2.4\text{ million bp}$).</li>
        <li>Total estimated genes = <strong>~30,000</strong>. Functions unknown for $>50\%$ discovered genes. Less than <strong>$2\%$</strong> genome codes for proteins. Chromosome 1 has most genes (2968); Y chromosome has fewest (231). 1.4 million locations of Single Nucleotide Polymorphisms (SNPs).</li>
      </ul>
    </li>
    <li><strong>DNA Fingerprinting (Alec Jeffreys):</strong> Exploits <strong>Variable Number of Tandem Repeats (VNTRs)</strong> satellite DNA showing high degree of polymorphism. Restriction enzyme digestion $\to$ Gel electrophoresis $\to$ Southern blot to nylon membrane $\to$ Hybridization with radiolabeled VNTR probe $\to$ Autoradiography. Used in forensics and paternity disputes.</li>
  </ul>
</div>
"""

    m05_revision = r"""
<div class="quick-revision-box">
  <h4>High-Yield Revision — Molecular Basis of Inheritance</h4>
  <ul>
    <li><strong>Watson-Crick DNA:</strong> Antiparallel, pitch 3.4 nm, 10 bp/turn, distance 0.34 nm. Chargaff: A=T, G=C, (A+G)/(T+C) = 1.</li>
    <li><strong>Nucleosome:</strong> 200 bp DNA + Octamer of basic histones (H2A, H2B, H3, H4 x2) rich in Lysine & Arginine.</li>
    <li><strong>Hershey-Chase (1952):</strong> 32P entered bacterial pellet (DNA is genetic material); 35S remained in supernatant (protein coat).</li>
    <li><strong>Meselson & Stahl:</strong> Semiconservative replication in 15N E. coli; 1st gen = 100% hybrid 15N/14N; 2nd gen = 50% hybrid, 50% light.</li>
    <li><strong>Eukaryotic Splicing:</strong> Introns removed, exons spliced; 5' capping with m7Gppp; 3' tailing with poly-A tail (hnRNA -> mRNA).</li>
    <li><strong>Genetic Code:</strong> 64 codons, 61 sense, 3 stop (UAA, UAG, UGA). AUG = Methionine & Initiator.</li>
    <li><strong>Lac Operon:</strong> z = beta-galactosidase; y = permease; a = transacetylase. Inducer = allolactose. Negative inducible control.</li>
    <li><strong>VNTRs:</strong> Minisatellites (0.1 to 20 kb) used in Alec Jeffreys' DNA fingerprinting.</li>
  </ul>
</div>
"""

    m05_flashcards = [
      {"q": "What experimental evidence proved conclusively that DNA, not protein, is the genetic material?", "a": "The Hershey-Chase experiment (1952) using T2 bacteriophage labeled with 35S (protein) and 32P (DNA). Only 32P radioactivity was detected inside the bacterial pellet following infection and blending."},
      {"q": "How did Meselson and Stahl differentiate between parental and daughter DNA strands?", "a": "By equilibrium density gradient centrifugation using Cesium Chloride (CsCl) to separate heavy 15N-labeled DNA from intermediate 15N/14N hybrid DNA and light 14N DNA."},
      {"q": "What post-transcriptional processing events must eukaryotic hnRNA undergo to become mature mRNA?", "a": "1. Splicing (removal of non-coding introns and joining of exons), 2. Capping (addition of methyl guanosine triphosphate to 5' end), and 3. Tailing (polyadenylation of 200-300 adenylate residues at 3' end)."},
      {"q": "What are the structural genes of the Lac Operon and what enzymes do they encode?", "a": "LacZ encodes beta-galactosidase (hydrolyzes lactose to glucose and galactose), LacY encodes permease (membrane transporter for lactose), and LacA encodes transacetylase."},
      {"q": "Why is the genetic code described as degenerate and unambiguous?", "a": "Degenerate means a single amino acid can be specified by more than one codon. Unambiguous means each specific codon always codes for only one particular amino acid."},
      {"q": "What molecular feature allows VNTRs to serve as reliable markers in DNA fingerprinting?", "a": "VNTRs (Variable Number of Tandem Repeats) are short repetitive minisatellite DNA sequences whose repeat copy number varies extensively between individuals due to high mutation frequency."}
    ]

    m05_flow = [
      {"id": "m1", "title": "Double Helix & Nucleosome", "badge": "Step 1", "desc": "Antiparallel DNA double helix wrapped around histone octamer forming nucleosomes; compacted into chromatin fibers."},
      {"id": "m2", "title": "Semiconservative Replication", "badge": "Step 2", "desc": "Helicase unwinds ori; DNA polymerase synthesizes leading strand continuously and lagging strand as Okazaki fragments."},
      {"id": "m3", "title": "Transcription & Processing", "badge": "Step 3", "desc": "RNA Pol II copies template strand into hnRNA; introns spliced, 5' cap and 3' poly-A tail added forming mature mRNA."},
      {"id": "m4", "title": "Translation & Synthesis", "badge": "Step 4", "desc": "Ribosome reads triplet codons; aminoacylated tRNAs bind; 23S rRNA ribozyme catalyzes peptide bonds until stop codon."},
      {"id": "m5", "title": "Gene Regulation (Lac Operon)", "badge": "Step 5", "desc": "Absence of lactose keeps repressor on operator; lactose inducer binds repressor turning transcription of Z, Y, A genes ON."},
      {"id": "m6", "title": "DNA Fingerprinting", "badge": "Step 6", "desc": "Restriction digestion of genomic DNA, agarose separation, Southern blotting, VNTR probe hybridization, and autoradiography."}
    ]

    m05_mindmap = {
      "id": "root", "title": "Molecular Genetics", "icon": "🧬", "children": [
        {"id": "dna", "title": "DNA Architecture", "icon": "🔬", "children": [
          {"id": "dn1", "title": "Double Helix (Watson-Crick, pitch 3.4nm, A=T, G=C)"},
          {"id": "dn2", "title": "Packaging: Nucleosome (Octamer of H2A, H2B, H3, H4 + 200bp DNA)"},
          {"id": "dn3", "title": "Experiments: Griffith, Avery-MacLeod, Hershey-Chase (32P proof)"}
        ]},
        {"id": "central", "title": "Central Dogma", "icon": "🔄", "children": [
          {"id": "cd1", "title": "Replication: Meselson-Stahl (15N), Semiconservative, Okazaki fragments"},
          {"id": "cd2", "title": "Transcription: RNA Pol II, Splicing (Intron removal), Capping, Tailing"},
          {"id": "cd3", "title": "Genetic Code: 64 codons, Triplet, Degenerate, AUG dual function"},
          {"id": "cd4", "title": "Translation: Ribosome, charged tRNA, 23S rRNA ribozyme"}
        ]},
        {"id": "regulation", "title": "Operon & Genomics", "icon": "💻", "children": [
          {"id": "rg1", "title": "Lac Operon: z (beta-gal), y (permease), a (transacetylase), Allolactose"},
          {"id": "rg2", "title": "HGP: 3164.7 million bp, ~30,000 genes, <2% protein coding"},
          {"id": "rg3", "title": "DNA Fingerprinting: Alec Jeffreys, VNTR minisatellites, Southern blot"}
        ]}
      ]
    }

    m05_pages = [
      {"page_num": 1, "text": "DNA double helix structure: antiparallel strands, right-handed helix with 3.4 nm pitch and 10 bp per turn. Chargaff rule A=T and G=C. Histone octamer wraps 200 bp of DNA to form nucleosome. Hershey-Chase experiment with 35S and 32P bacteriophages proved DNA is genetic material."},
      {"page_num": 2, "text": "Replication is semiconservative proved by Meselson and Stahl using 15N isotope. Transcription in eukaryotes produces hnRNA modified by splicing out introns, 5' capping with methyl guanosine triphosphate, and 3' poly-A tailing. Genetic code has 64 triplet codons, 61 coding, 3 stop codons."},
      {"page_num": 3, "text": "Lac operon negative inducible regulation: i gene repressor inactivated by lactose inducer allowing transcription of lacZ beta-galactosidase, lacY permease, lacA transacetylase. Human Genome Project discovered 30,000 genes with chromosome 1 having most genes. DNA fingerprinting uses VNTR minisatellites."}
    ]

    topics.append({
      "id": "bio-ch05-molecular-basis",
      "title": "05. Molecular Basis of Inheritance",
      "subject": "bio",
      "subject_title": "Biology • Class 12",
      "reading_time_min": 17,
      "has_handwritten": False,
      "detailed_html": m05_detailed,
      "revision_html": m05_revision,
      "flashcards": m05_flashcards,
      "flow_data": m05_flow,
      "mindmap_data": m05_mindmap,
      "pages": m05_pages
    })

    # Append remaining 8 chapters (06 to 13)
    _add_remaining_biology_chapters(topics)

    return topics

def _add_remaining_biology_chapters(topics: List[Dict[str, Any]]):
    """Helper to append chapters 06 to 13."""

    # =========================================================================
    # MODULE 06: EVOLUTION
    # =========================================================================
    m06_detailed = r"""
<div class="topic-header">
  <span class="topic-num">UNIT VII • TOPIC 06 OF 13</span>
  <h3 class="topic-title">Evolution</h3>
</div>

<div class="concept-card">
  <div class="card-label">ORIGIN OF LIFE & MILLER-UREY EXPERIMENT</div>
  <ul>
    <li><strong>Big Bang Theory:</strong> Universe originated ~20 billion years ago in a singular huge explosion. Earth formed ~4.5 billion years ago; primitive reducing atmosphere composed of water vapor, methane ($CH_4$), ammonia ($NH_3$), and hydrogen ($H_2$) with <strong>no free $O_2$</strong>.</li>
    <li><strong>Oparin-Haldane Hypothesis:</strong> Life originated abiogenetically from non-living organic molecules ("chemical evolution" preceding biological evolution).</li>
    <li><strong>Miller-Urey Experiment (1953):</strong> Simulated primitive Earth conditions:
      <ul>
        <li>Electric discharge ($75,000\text{ V}$) created in closed flask containing $CH_4, NH_3, H_2$ ($2:1:2$) and water vapor at <strong>$800^\circ\text{C}$</strong>.</li>
        <li>Result: Synthesis of <strong>amino acids</strong> (Glycine, Alanine, Aspartic acid). Similar experiments produced sugars, nitrogen bases, pigments, and fats.</li>
        <li>First non-cellular life forms: 3 billion years ago (giant macromolecules: RNA, proteins, polysaccharides). First cellular life: 2 billion years ago (single-celled aquatic heterotrophs).</li>
      </ul>
    </li>
  </ul>
</div>

<div class="table-container">
  <div class="table-caption">NCERT Comparison: Homologous vs Analogous Organs</div>
  <table class="notes-table">
    <thead>
      <tr><th>Criterion</th><th>Homologous Organs (Divergent Evolution)</th><th>Analogous Organs (Convergent Evolution)</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>Anatomical Origin</strong></td><td>Same fundamental structure and embryonic origin</td><td>Different structural anatomy and embryonic origin</td></tr>
      <tr><td><strong>Function</strong></td><td>Adapted to perform different functions</td><td>Adapted to perform identical/similar functions</td></tr>
      <tr><td><strong>Evolutionary Process</strong></td><td><strong>Divergent Evolution</strong> (adaptation to different ecological niches)</td><td><strong>Convergent Evolution</strong> (independent adaptation to same habitat)</td></tr>
      <tr><td><strong>Animal Examples</strong></td><td>Forelimbs of Whale, Bat, Cheetah, and Human</td><td>Wings of Butterfly (invertebrate) and Bird (vertebrate); Eye of Octopus and Mammal</td></tr>
      <tr><td><strong>Plant Examples</strong></td><td>Thorns of <em>Bougainvillea</em> and Tendrils of <em>Cucurbita</em> (both modified axillary buds)</td><td>Sweet potato (root modification) and Potato (stem tuber modification) for starch storage</td></tr>
    </tbody>
  </table>
</div>

<div class="concept-card">
  <div class="card-label">NATURAL SELECTION, ADAPTIVE RADIATION & HARDY-WEINBERG PRINCIPLE</div>
  <ul>
    <li><strong>Industrial Melanism (England):</strong> Peppered moth (<em>Biston betularia</em>):
      <ul>
        <li><em>Before Industrialization (1850s):</em> White-winged moths predominated because tree trunks were covered with light-colored lichens (polluted-sensitive bioindicators); melanic dark moths were preyed upon by birds.</li>
        <li><em>After Industrialization (1920s):</em> Coal soot blackened trunks and killed lichens. Dark melanic moths (<em>Biston carbonaria</em>) survived camouflage; white moths were heavily predated. Proof of natural selection acting on pre-existing genetic variations.</li>
      </ul>
    </li>
    <li><strong>Adaptive Radiation:</strong> Process of evolution of different species in a given geographical area starting from a common point and radiating to other geographical areas (habitats):
      <ul>
        <li><em>Darwin's Finches:</em> Galapagos Islands finches radiated from original seed-eating ancestor to insectivorous, vegetarian, and cactus-feeding beaks.</li>
        <li><em>Australian Marsupials:</em> Radiated from common ancestor within Australia: Kangaroo, Wombat, Bandicoot, Tasmanian wolf.</li>
        <li><em>Convergent Evolution of Placental Mammals & Marsupials:</em> Placental wolf $\leftrightarrow$ Tasmanian wolf; Anteater $\leftrightarrow$ Numbat; Flying squirrel $\leftrightarrow$ Flying phalanger.</li>
      </ul>
    </li>
    <li><strong>Hardy-Weinberg Principle:</strong> In a large, randomly mating population without evolutionary forces, <strong>allele frequencies remain constant</strong> from generation to generation (Genetic Equilibrium):
      <div class="formula-block">
        $p + q = 1 \implies p^2 + 2pq + q^2 = 1$<br>
        where $p$ = frequency of dominant allele $A$, $q$ = frequency of recessive allele $a$, $p^2$ = homozygous dominant $AA$, $2pq$ = heterozygous $Aa$, $q^2$ = homozygous recessive $aa$.
      </div>
      <ul>
        <li><strong>5 Factors Disrupting Equilibrium:</strong> 1. Gene migration / gene flow, 2. Genetic drift (random chance changes in small populations; <em>Founder effect</em> and <em>Bottleneck effect</em>), 3. Mutation, 4. Genetic recombination, 5. Natural selection.</li>
        <li><strong>3 Types of Natural Selection:</strong>
          <ol>
            <li><em>Stabilizing:</em> Favors average phenotype (peak gets higher and narrower, e.g. human birth weight).</li>
            <li><em>Directional:</em> Favors one extreme phenotype (peak shifts in one direction, e.g. industrial melanism).</li>
            <li><em>Disruptive:</em> Favors both extremes over intermediate (two peaks form).</li>
          </ol>
        </li>
      </ul>
    </li>
  </ul>
</div>

<div class="remember-box">
  <strong>HUMAN EVOLUTION CHRONOLOGY:</strong>
  <ul>
    <li><strong>Dryopithecus & Ramapithecus (15 mya):</strong> Hairy, walked like gorillas/chimps. Dryopithecus was more ape-like; Ramapithecus was more man-like.</li>
    <li><strong>Australopithecus (2 mya):</strong> Lived in East African grasslands; walked upright; hunted with stone weapons; essentially fruit-eaters.</li>
    <li><strong>Homo habilis (First human-like hominid):</strong> Brain capacity <strong>650–800 cc</strong>; made tools; did not eat meat.</li>
    <li><strong>Homo erectus (1.5 mya):</strong> Fossils found in Java (1891); brain capacity <strong>900 cc</strong>; walked fully erect; <strong>ate meat</strong>.</li>
    <li><strong>Neanderthal Man (100,000–40,000 ya):</strong> Brain capacity <strong>1400 cc</strong>; lived in near East and Central Asia; used hides to protect body; <strong>buried their dead</strong>.</li>
    <li><strong>Homo sapiens (Modern Man):</strong> Arose in Africa 75,000–10,000 years ago; prehistoric cave art developed ~18,000 ya; agriculture began ~10,000 ya.</li>
  </ul>
</div>
"""

    m06_revision = r"""
<div class="quick-revision-box">
  <h4>High-Yield Revision — Evolution</h4>
  <ul>
    <li><strong>Miller's Setup:</strong> 800°C, CH4 : NH3 : H2 (2:1:2) + H2O vapor + electric discharge -> amino acids (alanine, glycine, aspartic acid).</li>
    <li><strong>Homologous:</strong> Divergent evolution (same origin, different function) -> Thorn of Bougainvillea & Tendril of Cucurbita; Whale flipper & Human hand.</li>
    <li><strong>Analogous:</strong> Convergent evolution (different origin, same function) -> Potato & Sweet potato; Eye of Octopus & Mammal.</li>
    <li><strong>Hardy-Weinberg:</strong> $p^2 + 2pq + q^2 = 1$. Disrupted by gene flow, genetic drift (founder effect), mutation, recombination, natural selection.</li>
    <li><strong>Cranial Capacities:</strong> Homo habilis (650-800 cc) $\to$ Homo erectus (900 cc, meat eater) $\to$ Neanderthal (1400 cc, buried dead) $\to$ Homo sapiens.</li>
  </ul>
</div>
"""

    m06_flashcards = [
      {"q": "What gases were used in the Miller-Urey experiment and what was synthesized?", "a": "Methane (CH4), Ammonia (NH3), Hydrogen (H2), and water vapor at 800°C with electric discharge. The experiment successfully synthesized amino acids (glycine, alanine, aspartic acid)."},
      {"q": "Why are the thorns of Bougainvillea and tendrils of Cucurbita considered homologous?", "a": "Both are structural modifications of axillary buds sharing the same embryonic origin, but have diverged to perform different functions (defense vs climbing support)."},
      {"q": "State the Hardy-Weinberg algebraic equation and define its components.", "a": "p^2 + 2pq + q^2 = 1, where p is the frequency of dominant allele A, q is the frequency of recessive allele a, p^2 is homozygous dominant AA, 2pq is heterozygous Aa, and q^2 is homozygous recessive aa."},
      {"q": "What is the Founder Effect in population genetics?", "a": "When a small group of individuals migrates and colonizes a new habitat, their allele frequencies by chance differ from the original population, founding a genetically distinct new population."},
      {"q": "Arrange human ancestors in chronological evolutionary sequence with cranial capacities.", "a": "Australopithecus -> Homo habilis (650-800 cc) -> Homo erectus (900 cc) -> Neanderthal man (1400 cc) -> Homo sapiens (~1400-1450 cc)."},
      {"q": "What is the difference between Lamarck's and de Vries' theories of evolutionary variation?", "a": "Lamarck proposed slow inheritance of acquired characters through use and disuse. Hugo de Vries proposed that evolution occurs through sudden, random, directionless mutations called saltation."}
    ]

    m06_flow = [
      {"id": "ev1", "title": "Chemical Evolution", "badge": "Step 1", "desc": "Prebiotic synthesis of amino acids in reducing atmosphere (Oparin-Haldane & Miller-Urey experiment)."},
      {"id": "ev2", "title": "Cellular Emergence", "badge": "Step 2", "desc": "First cellular forms ~2 billion years ago; aquatic prokaryotic heterotrophs evolving photosynthetic ability."},
      {"id": "ev3", "title": "Anatomical Divergence", "badge": "Step 3", "desc": "Homology (divergent evolution) and Analogy (convergent evolution); adaptive radiation in isolated islands."},
      {"id": "ev4", "title": "Natural Selection", "badge": "Step 4", "desc": "Industrial melanism in peppered moths; stabilization, directional shift, or disruption of phenotypes."},
      {"id": "ev5", "title": "Genetic Equilibrium", "badge": "Step 5", "desc": "Hardy-Weinberg equilibrium maintained unless disturbed by drift, mutation, gene flow, or selection."},
      {"id": "ev6", "title": "Hominid Evolution", "badge": "Step 6", "desc": "Dryopithecus -> Australopithecus -> H. habilis (tools) -> H. erectus (fire/meat) -> Neanderthal (burials) -> H. sapiens."}
    ]

    m06_mindmap = {
      "id": "root", "title": "Evolution", "icon": "🦴", "children": [
        {"id": "origin", "title": "Origin of Life", "icon": "⚡", "children": [
          {"id": "o1", "title": "Oparin-Haldane: Chemical evolution (reducing atmosphere)"},
          {"id": "o2", "title": "Miller-Urey: CH4, NH3, H2, H2O at 800°C -> Amino acids"}
        ]},
        {"id": "evidence", "title": "Evidences & Radiation", "icon": "🦕", "children": [
          {"id": "e1", "title": "Homology (Divergent): Whale flipper & Human arm; Thorn & Tendril"},
          {"id": "e2", "title": "Analogy (Convergent): Bird & Butterfly wings; Potato & Sweet potato"},
          {"id": "e3", "title": "Adaptive Radiation: Darwin's Finches & Australian Marsupials"}
        ]},
        {"id": "mechanisms", "title": "Mechanisms & Hardy-Weinberg", "icon": "📊", "children": [
          {"id": "m1", "title": "Natural Selection: Industrial melanism (Biston betularia)"},
          {"id": "m2", "title": "Hardy-Weinberg: p^2 + 2pq + q^2 = 1; 5 disturbing forces"},
          {"id": "m3", "title": "De Vries Saltation (Single-step large mutations)"}
        ]},
        {"id": "hominids", "title": "Human Evolution", "icon": "🚶", "children": [
          {"id": "h1", "title": "Homo habilis: 650-800 cc, first toolmaker, vegetarian"},
          {"id": "h2", "title": "Homo erectus: 900 cc, upright walk, ate meat"},
          {"id": "h3", "title": "Neanderthal: 1400 cc, buried dead; Homo sapiens modern"}
        ]}
      ]
    }

    m06_pages = [
      {"page_num": 1, "text": "Origin of life Miller-Urey experiment with electric discharge, 800 degrees, methane, ammonia, hydrogen, water vapor producing amino acids. Homologous organs show divergent evolution sharing common ancestor like whale flipper and cheetah leg. Analogous organs show convergent evolution like eye of octopus and mammal."},
      {"page_num": 2, "text": "Adaptive radiation in Darwin's finches and Australian marsupials. Hardy-Weinberg equilibrium principle states p squared plus 2pq plus q squared equals 1. Genetic drift and founder effect alter equilibrium. Three types of selection: stabilizing, directional, disruptive."},
      {"page_num": 3, "text": "Human evolution timeline: Dryopithecus ape-like, Ramapithecus man-like, Australopithecus walked upright, Homo habilis brain 650-800 cc, Homo erectus brain 900 cc and ate meat, Neanderthal man brain 1400 cc and buried dead, modern Homo sapiens emerged in Africa."}
    ]

    topics.append({
      "id": "bio-ch06-evolution",
      "title": "06. Evolution",
      "subject": "bio",
      "subject_title": "Biology • Class 12",
      "reading_time_min": 15,
      "has_handwritten": False,
      "detailed_html": m06_detailed,
      "revision_html": m06_revision,
      "flashcards": m06_flashcards,
      "flow_data": m06_flow,
      "mindmap_data": m06_mindmap,
      "pages": m06_pages
    })

    # =========================================================================
    # MODULE 07: HUMAN HEALTH AND DISEASE
    # =========================================================================
    m07_detailed = r"""
<div class="topic-header">
  <span class="topic-num">UNIT VIII • TOPIC 07 OF 13</span>
  <h3 class="topic-title">Human Health and Disease</h3>
</div>

<div class="concept-card">
  <div class="card-label">COMMON INFECTIOUS DISEASES IN HUMANS</div>
  <p>Health is defined by WHO as a state of complete <strong>physical, mental, and social well-being</strong>, not merely the absence of disease. Disease-causing organisms are called <strong>pathogens</strong>.</p>
  <ul>
    <li><strong>Typhoid:</strong> Caused by bacterium <em>Salmonella typhi</em>. Transmitted through contaminated food and water; enters small intestine. Symptoms: sustained high fever ($39\text{--}40^\circ\text{C}$), stomach pain, constipation, headache, intestinal perforation in severe cases. Confirmatory test: <strong>Widal Test</strong>. Classic carrier: Mary Mallon ("Typhoid Mary").</li>
    <li><strong>Pneumonia:</strong> Caused by <em>Streptococcus pneumoniae</em> and <em>Haemophilus influenzae</em>. Infects <strong>alveoli</strong> of lungs (alveoli fill with fluid leading to respiratory distress). Lips and fingernails turn gray to bluish in severe cases. Transmitted by droplets/aerosols.</li>
    <li><strong>Common Cold:</strong> Caused by <strong>Rhino viruses</strong>. Infects nose and respiratory passage, but <strong>NOT the lungs</strong>! Symptoms: nasal congestion, sore throat, cough for 3–7 days.</li>
    <li><strong>Malaria:</strong> Caused by protozoan <em>Plasmodium</em> (<em>P. vivax, P. malariae, P. falciparum</em>). <em>P. falciparum</em> causes malignant, fatal malaria.
      <ul>
        <li><strong>Life Cycle:</strong> Requires two hosts: Female <em>Anopheles</em> mosquito (vector) and human:
          <ol>
            <li>Infected mosquito injects <strong>sporozoites</strong> (infectious stage) into human bloodstream during bite.</li>
            <li>Sporozoites reach liver cells and multiply asexually, then burst liver cells.</li>
            <li>Invade Red Blood Cells (RBCs) and multiply. RBC rupture releases toxic substance called <strong>Hemozoin</strong>, which causes recurring chills and high fever every 3 to 4 days.</li>
            <li>Gametocytes (sexual stages) develop in human RBCs.</li>
            <li>Female mosquito bites human and ingests gametocytes. Fertilization and development occur in <strong>mosquito gut</strong>.</li>
            <li>Mature sporozoites escape gut and migrate to <strong>mosquito salivary glands</strong>.</li>
          </ol>
        </li>
      </ul>
    </li>
    <li><strong>Amoebiasis (Amoebic Dysentery):</strong> Caused by <em>Entamoeba histolytica</em> in large intestine. Mechanical carrier: houseflies. Symptoms: stool with excess mucus and blood clots.</li>
    <li><strong>Ascariasis & Filariasis:</strong> <em>Ascaris lumbricoides</em> (roundworm causing intestinal blockage); <em>Wuchereria bancrofti & W. malayi</em> (filarial worm causing elephantiasis/chronic inflammation of lower limbs, transmitted by female <em>Culex</em> mosquito).</li>
    <li><strong>Ringworm:</strong> Fungal infection of skin, nails, and scalp caused by genera <em>Microsporum, Trichophyton, Epidermophyton</em>. Dry scaly itchy lesions.</li>
  </ul>
</div>

<div class="concept-card">
  <div class="card-label">IMMUNITY: INNATE & ACQUIRED DEFENSE SYSTEMS</div>
  <ul>
    <li><strong>Innate Immunity (Non-specific, present from birth):</strong>
      <ol>
        <li><em>Physical Barriers:</em> Skin (prevents entry); Mucus coating of respiratory, gastrointestinal, and urogenital tracts trapping microbes.</li>
        <li><em>Physiological Barriers:</em> Stomach acid ($\text{HCl}$), saliva, tears containing lysozyme.</li>
        <li><em>Cellular Barriers:</em> Polymorphonuclear leukocytes (PMNL-neutrophils), monocytes, Natural Killer (NK) cells, tissue macrophages.</li>
        <li><em>Cytokine Barriers:</em> Virus-infected cells secrete proteins called <strong>Interferons</strong> which protect non-infected cells from viral replication.</li>
      </ol>
    </li>
    <li><strong>Acquired Immunity (Pathogen-specific with Memory):</strong>
      <ul>
        <li><strong>Humoral Immune Response:</strong> Mediated by <strong>B-lymphocytes</strong> producing an army of protein antibodies into blood/lymph ($H_2L_2$ monomer: 2 heavy + 2 light chains linked by disulfide bonds). Types: <strong>IgG, IgA, IgM, IgE, IgD</strong>.</li>
        <li><strong>Cell-Mediated Immunity (CMI):</strong> Mediated by <strong>T-lymphocytes</strong> (Helper T, Cytotoxic T). Responsible for <strong>graft rejection</strong> in kidney/heart transplants (tissue matching and immunosuppressants like Cyclosporin A required). Differentiates between 'self' and 'non-self'.</li>
        <li><em>Active Immunity:</em> Body's own cells produce antibodies upon antigen exposure (natural infection or vaccination); slow but long-lasting.</li>
        <li><em>Passive Immunity:</em> Pre-formed antibodies directly administered; fast protection. E.g., <strong>Colostrum</strong> containing abundant <strong>IgA</strong> antibodies; anti-tetanus serum; anti-venom.</li>
      </ul>
    </li>
    <li><strong>Allergy & Autoimmunity:</strong>
      <ul>
        <li><em>Allergy:</em> Exaggerated immune response to environmental allergens mediated by <strong>IgE antibodies</strong>. Mast cells release <strong>Histamine and Serotonin</strong>. Treated with antihistamines, adrenaline, and corticosteroids.</li>
        <li><em>Autoimmunity:</em> Immune system attacks self-cells due to genetic and environmental factors, e.g., <strong>Rheumatoid Arthritis</strong>.</li>
        <li><em>Lymphoid Organs:</em> Primary (Bone marrow, Thymus - maturation sites) and Secondary (Spleen, Lymph nodes, Tonsils, Peyer's patches, <strong>MALT</strong> - Mucosa-Associated Lymphoid Tissue constitutes $50\%$ of lymphoid tissue in humans).</li>
      </ul>
    </li>
  </ul>
</div>

<div class="remember-box">
  <strong>AIDS, CANCER & DRUG ABUSE:</strong>
  <ul>
    <li><strong>AIDS (Acquired Immuno Deficiency Syndrome):</strong> Caused by Human Immunodeficiency Virus (<strong>HIV</strong>), a retrovirus with an RNA genome enclosed in an envelope:
      <ul>
        <li>HIV enters <strong>macrophages</strong> (acting as "HIV factory"), where <strong>reverse transcriptase</strong> converts viral RNA into viral DNA, incorporating into host genome.</li>
        <li>HIV simultaneously attacks <strong>Helper T-lymphocytes ($T_H$)</strong>, replicates, and destroys them. $T_H$ cell count drops precipitously ($<200/\mu\text{L}$), leaving patient defenseless against opportunistic infections (<em>Mycobacterium</em>, fungi, <em>Toxoplasma</em>).</li>
        <li>Diagnostic test: <strong>ELISA</strong> (Enzyme-Linked Immunosorbent Assay); confirmed by Western Blot.</li>
      </ul>
    </li>
    <li><strong>Cancer:</strong> Uncontrolled mitotic cell division due to breakdown of <strong>contact inhibition</strong>:
      <ul>
        <li><em>Benign tumors:</em> Remain confined to original location. <em>Malignant tumors:</em> Mass of proliferating neoplastic cells that invade surrounding tissues; enter bloodstream and lodge at distant sites forming secondary tumors (<strong>Metastasis</strong> - most feared property).</li>
        <li>Causes: Carcinogens (ionizing radiation X-rays, UV rays; chemicals in tobacco smoke); Proto-oncogenes activated into <strong>oncogenes</strong>. Treatment: Surgery, Radiotherapy, Chemotherapy, and Immunotherapy ($\alpha$-interferon).</li>
      </ul>
    </li>
    <li><strong>Drugs and Alcohol Abuse:</strong>
      <ul>
        <li><strong>Opioids:</strong> Bind opioid receptors in CNS and GI tract. <em>Morphine</em> (painkiller from poppy <em>Papaver somniferum</em> latex); <em>Heroin / Smack</em> (diacetylmorphine, white odorless bitter crystalline, depressant).</li>
        <li><strong>Cannabinoids:</strong> Bind cannabinoid receptors in brain. Obtained from <em>Cannabis sativa</em> inflorescence (Marijuana, hashish, charas, ganja). Affects cardiovascular system.</li>
        <li><strong>Cocaine / Coke / Crack:</strong> Extracted from South American coca plant <em>Erythroxylum coca</em>. Interferes with dopamine neurotransmitter transport; CNS stimulant causing euphoria and hallucinations in high doses.</li>
      </ul>
    </li>
  </ul>
</div>
"""

    m07_revision = r"""
<div class="quick-revision-box">
  <h4>High-Yield Revision — Human Health and Disease</h4>
  <ul>
    <li><strong>Typhoid:</strong> Salmonella typhi, Widal test. Pneumonia: Alveolar fluid accumulation. Common cold: Rhino virus (lungs unaffected).</li>
    <li><strong>Malaria:</strong> Sporozoite injected $\to$ Liver $\to$ RBC rupture releasing Hemozoin (chills). Gametocytes formed in human; fertilization in mosquito gut.</li>
    <li><strong>Innate Barriers:</strong> Physical (skin, mucus), Physiological (HCl, tears), Cellular (PMNL, macrophages), Cytokine (Interferons).</li>
    <li><strong>Antibodies ($H_2L_2$):</strong> IgA (colostrum, secretions), IgE (allergy, mast cells histamine), IgG (crosses placenta), IgM (pentamer, first response).</li>
    <li><strong>Graft Rejection:</strong> Mediated by Cell-Mediated Immunity (CMI / T-cells).</li>
    <li><strong>AIDS:</strong> HIV attacks Helper T-cells ($CD_4^+$) and macrophages. Diagnosed by ELISA.</li>
    <li><strong>Cancer:</strong> Loss of contact inhibition; metastasis (malignant spreading); treated with $\alpha$-interferon.</li>
    <li><strong>Drugs:</strong> Heroin (diacetylmorphine, depressant); Cocaine (dopamine interference, Erythroxylum coca); Cannabinoids (cardiovascular effects).</li>
  </ul>
</div>
"""

    m07_flashcards = [
      {"q": "What toxic substance is released during the rupture of RBCs in malaria that causes recurring chills and fever?", "a": "Hemozoin, a toxic crystalline pigment formed by the breakdown of hemoglobin by Plasmodium parasites."},
      {"q": "Which type of immune response is responsible for graft rejection in organ transplantation?", "a": "Cell-Mediated Immunity (CMI), driven by T-lymphocytes that differentiate between self and non-self cells."},
      {"q": "What is the specific role of interferons in innate immunity?", "a": "Interferons are cytokine proteins secreted by virus-infected host cells that stimulate neighboring uninfected cells to produce antiviral proteins, inhibiting viral spread."},
      {"q": "Why is HIV classified as a retrovirus, and how does it deplete the immune system?", "a": "HIV possesses an RNA genome and uses reverse transcriptase to synthesize viral DNA in host cells. It progressively attacks and destroys Helper T-lymphocytes (CD4+ cells), causing severe immunodeficiency."},
      {"q": "What is metastasis and why is it considered the most feared property of malignant tumors?", "a": "Metastasis is the sloughing off of cancerous cells from a primary malignant tumor into blood and lymph vessels, which travel to distant anatomical sites and initiate secondary tumors."},
      {"q": "From which plant is heroin synthesized and what is its primary physiological effect?", "a": "Heroin (diacetylmorphine) is synthesized by acetylation of morphine extracted from the latex of the opium poppy (Papaver somniferum). It acts as a central nervous system depressant and slows down bodily functions."}
    ]

    m07_flow = [
      {"id": "d1", "title": "Pathogen Invasion", "badge": "Step 1", "desc": "Entry of pathogen through food/water (Typhoid, Amoebiasis), droplet inhalation (Pneumonia, Cold), or insect vector (Malaria, Filariasis)."},
      {"id": "d2", "title": "Innate Defense Engagement", "badge": "Step 2", "desc": "Physical skin/mucus barriers, stomach acid, PMNL neutrophils, and interferons act immediately to contain the infection."},
      {"id": "d3", "title": "Acquired Immune Activation", "badge": "Step 3", "desc": "Antigen presentation stimulates B-cells to secrete H2L2 antibodies (humoral) and T-cells to mediate cellular cytotoxicity (CMI)."},
      {"id": "d4", "title": "Immunological Memory", "badge": "Step 4", "desc": "Memory B and T cells generated; subsequent exposure triggers rapid, massive secondary anamnestic response."},
      {"id": "d5", "title": "Pathological Derangements", "badge": "Step 5", "desc": "Allergies (IgE / mast cell histamine release), Autoimmunity (Rheumatoid arthritis), or Immunodeficiency (HIV depleting Helper T-cells)."},
      {"id": "d6", "title": "Neoplasia & Therapeutics", "badge": "Step 6", "desc": "Loss of contact inhibition leads to malignant tumors; managed with surgery, chemo, radiotherapy, and alpha-interferon biological response modifiers."}
    ]

    m07_mindmap = {
      "id": "root", "title": "Human Health & Disease", "icon": "🩺", "children": [
        {"id": "infections", "title": "Infectious Pathogens", "icon": "🦠", "children": [
          {"id": "i1", "title": "Bacterial: Typhoid (Widal test) & Pneumonia (Alveolar fluid)"},
          {"id": "i2", "title": "Viral: Common cold (Rhino virus) & Dengue / Chikungunya"},
          {"id": "i3", "title": "Protozoan: Malaria (Plasmodium vivax/falciparum, Hemozoin chills)"},
          {"id": "i4", "title": "Helminths & Fungi: Ascariasis, Filariasis (Wuchereria), Ringworm"}
        ]},
        {"id": "immunity", "title": "Immune Architecture", "icon": "🛡️", "children": [
          {"id": "im1", "title": "Innate: Physical, Physiological (HCl), Cellular (PMNL), Cytokines (Interferon)"},
          {"id": "im2", "title": "Acquired: Humoral (B-cell antibodies IgG/A/M/E) & CMI (T-cell graft rejection)"},
          {"id": "im3", "title": "Passive Immunity: Colostrum IgA & Antivenom"},
          {"id": "im4", "title": "Allergies (IgE, Histamine) & Autoimmunity (Rheumatoid arthritis)"}
        ]},
        {"id": "severe", "title": "AIDS, Cancer & Drugs", "icon": "🏥", "children": [
          {"id": "s1", "title": "AIDS: HIV retrovirus destroys Helper T-cells; ELISA test"},
          {"id": "s2", "title": "Cancer: Loss of contact inhibition; Metastasis; Oncogenes"},
          {"id": "s3", "title": "Drugs: Opioids (Heroin), Cannabinoids, Cocaine (Dopamine blocker)"}
        ]}
      ]
    }

    m07_pages = [
      {"page_num": 1, "text": "Common diseases in humans: Typhoid caused by Salmonella typhi diagnosed by Widal test. Pneumonia caused by Streptococcus pneumoniae filling alveoli with fluid. Malaria caused by Plasmodium vivax and falciparum with life cycle in human and Anopheles mosquito releasing hemozoin causing chills."},
      {"page_num": 2, "text": "Innate immunity barriers: physical skin, physiological stomach acid, cellular PMNL neutrophils, cytokine interferons. Acquired immunity: B-cells produce antibodies H2L2 while T-cells mediate cell-mediated immunity responsible for graft rejection. Colostrum contains IgA providing passive immunity."},
      {"page_num": 3, "text": "AIDS caused by retrovirus HIV destroying Helper T-cells diagnosed by ELISA. Cancer results from loss of contact inhibition leading to malignant tumors that spread via metastasis. Drug abuse includes opioids like heroin from poppy, cannabinoids from cannabis, and cocaine from Erythroxylum coca."}
    ]

    topics.append({
      "id": "bio-ch07-human-health",
      "title": "07. Human Health and Disease",
      "subject": "bio",
      "subject_title": "Biology • Class 12",
      "reading_time_min": 16,
      "has_handwritten": False,
      "detailed_html": m07_detailed,
      "revision_html": m07_revision,
      "flashcards": m07_flashcards,
      "flow_data": m07_flow,
      "mindmap_data": m07_mindmap,
      "pages": m07_pages
    })

    # =========================================================================
    # MODULE 08: MICROBES IN HUMAN WELFARE
    # =========================================================================
    m08_detailed = r"""
<div class="topic-header">
  <span class="topic-num">UNIT VIII • TOPIC 08 OF 13</span>
  <h3 class="topic-title">Microbes in Human Welfare</h3>
</div>

<div class="concept-card">
  <div class="card-label">HOUSEHOLD & INDUSTRIAL MICROBIAL APPLICATIONS</div>
  <ul>
    <li><strong>Household Products:</strong>
      <ul>
        <li><strong>Curd:</strong> Lactic Acid Bacteria (<strong>LAB</strong>, e.g. <em>Lactobacillus</em>) added as inoculum/starter to milk. LAB produce acids that coagulate and partially digest milk proteins (casein). LAB dramatically increases nutritional quality by enriching with <strong>Vitamin $B_{12}$</strong> and checks disease-causing microbes in gut.</li>
        <li><strong>Fermented Dough:</strong> Dough for idli and dosa is fermented by bacteria; puffed-up appearance is due to production of <strong>$CO_2$ gas</strong>. Dough for bread is leavened using <strong>Baker's Yeast (<em>Saccharomyces cerevisiae</em>)</strong>.</li>
        <li><strong>Toddy:</strong> Traditional drink of Southern India made by fermenting palm sap.</li>
        <li><strong>Cheese:</strong> <em>Swiss Cheese</em> has large characteristic holes due to huge $CO_2$ production by bacterium <strong><em>Propionibacterium sharmanii</em></strong>. <em>Roquefort Cheese</em> is ripened by specific fungi <strong><em>Penicillium roqueforti</em></strong> giving it unique flavor.</li>
      </ul>
    </li>
    <li><strong>Industrial Products (Fermentors):</strong>
      <ul>
        <li><strong>Fermented Beverages:</strong> <em>Brewer's Yeast</em> (<em>Saccharomyces cerevisiae</em>) ferments malted cereals and fruit juices into ethanol. <em>Undistilled:</em> Wine and Beer (lower alcohol). <em>Distilled:</em> Whisky, Brandy, Rum (higher alcohol).</li>
        <li><strong>Antibiotics:</strong> Alexander Fleming (1928) discovered <strong>Penicillin</strong> from mold <em>Penicillium notatum</em> while working on <em>Staphylococcus</em>. Ernst Chain and Howard Florey established its full therapeutic potential to treat wounded soldiers in WWII (Nobel Prize 1945).</li>
      </ul>
    </li>
  </ul>
</div>

<div class="table-container">
  <div class="table-caption">NCERT Master Table: Bioactive Molecules, Organic Acids & Enzymes</div>
  <table class="notes-table">
    <thead>
      <tr><th>Product / Molecule</th><th>Microbial Source</th><th>Type of Microbe</th><th>Industrial / Medical Application</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>Citric Acid</strong></td><td><em>Aspergillus niger</em></td><td>Fungus</td><td>Food preservation, flavoring agent</td></tr>
      <tr><td><strong>Acetic Acid</strong></td><td><em>Acetobacter aceti</em></td><td>Bacterium</td><td>Vinegar production</td></tr>
      <tr><td><strong>Butyric Acid</strong></td><td><em>Clostridium butyricum</em></td><td>Bacterium</td><td>Chemical synthesis, butter rancidity testing</td></tr>
      <tr><td><strong>Lactic Acid</strong></td><td><em>Lactobacillus</em></td><td>Bacterium</td><td>Dairy processing, food preservative</td></tr>
      <tr><td><strong>Lipases</strong></td><td><em>Candida / Pseudomonas</em></td><td>Microbes</td><td>Detergent formulations (removes oily stains from laundry)</td></tr>
      <tr><td><strong>Pectinases & Proteases</strong></td><td>Various fungi & bacteria</td><td>Microbes</td><td>Clarifying commercial bottled fruit juices (crystal clear)</td></tr>
      <tr><td><strong>Streptokinase</strong></td><td><em>Streptococcus</em> (genetically modified)</td><td>Bacterium</td><td><strong>"Clot Buster"</strong> removing clots from blood vessels of heart attack patients</td></tr>
      <tr><td><strong>Cyclosporin A</strong></td><td><em>Trichoderma polysporum</em></td><td>Fungus</td><td><strong>Immunosuppressive agent</strong> in organ transplant patients</td></tr>
      <tr><td><strong>Statins</strong></td><td><em>Monascus purpureus</em></td><td>Yeast (Fungus)</td><td><strong>Blood cholesterol lowering agent</strong> (competitively inhibits HMG-CoA reductase)</td></tr>
    </tbody>
  </table>
</div>

<div class="concept-card">
  <div class="card-label">SEWAGE TREATMENT PLANTS (STPs) & BIOGAS GENERATION</div>
  <ul>
    <li><strong>Sewage Treatment Process:</strong>
      <ol>
        <li><strong>Primary Treatment (Physical):</strong> Sequential filtration removes floating debris; sedimentation removes grit (soil and small pebbles). Solid settling down = <strong>Primary Sludge</strong>; liquid supernatant = <strong>Primary Effluent</strong>.</li>
        <li><strong>Secondary Treatment (Biological):</strong> Primary effluent transferred to large aeration tanks with mechanical agitation and air pumping:
          <ul>
            <li>Vigorous growth of aerobic microbes into <strong>Flocs</strong> (masses of bacteria associated with fungal filaments to form mesh-like structures).</li>
            <li>Microbes consume major organic matter, dramatically reducing <strong>Biochemical Oxygen Demand (BOD)</strong>. <em>BOD is the amount of oxygen required to oxidize all organic matter in 1 liter of water. Higher BOD = higher pollution load.</em></li>
            <li>When BOD is reduced, effluent passes to settling tank where flocs settle down as <strong>Activated Sludge</strong>.</li>
            <li>Small part of activated sludge pumped back as <em>inoculum</em>; remaining pumped into <strong>Anaerobic Sludge Digesters</strong>. Anaerobic bacteria digest bacteria and fungi, producing <strong>Biogas</strong> (mixture of $CH_4, H_2S, CO_2$).</li>
          </ul>
        </li>
      </ol>
    </li>
    <li><strong>Biogas Plant (Gobar Gas):</strong> Methanogens (e.g. <strong><em>Methanobacterium</em></strong>) are anaerobic bacteria present in anaerobic sludge and cattle rumen (converting cellulose into methane). Technology developed in India by <strong>IARI</strong> and <strong>KVIC</strong>.</li>
  </ul>
</div>

<div class="remember-box">
  <strong>BIOCONTROL AGENTS & BIOFERTILIZERS:</strong>
  <ul>
    <li><strong>Biocontrol of Pests & Diseases:</strong>
      <ul>
        <li><strong>Ladybird beetle:</strong> Controls aphids. <strong>Dragonflies:</strong> Control mosquitoes.</li>
        <li><strong><em>Bacillus thuringiensis</em> (Bt):</strong> Dried spores mixed with water sprayed on plants. Caterpillars ingest crystal protoxin; alkaline gut pH dissolves toxin, creating gut pores and killing larvae.</li>
        <li><strong><em>Trichoderma</em>:</strong> Free-living fungus common in root ecosystems; effective against several soil-borne plant pathogens.</li>
        <li><strong>Baculoviruses (Genus <em>Nucleopolyhedrovirus</em>):</strong> Narrow spectrum, species-specific insecticidal applications. Cause no harm to non-target plants, mammals, birds, or beneficial insects; cornerstone of <strong>Integrated Pest Management (IPM)</strong>.</li>
      </ul>
    </li>
    <li><strong>Biofertilizers:</strong>
      <ul>
        <li><strong>Bacteria:</strong> Symbiotic <em>Rhizobium</em> in legume root nodules; Free-living nitrogen fixers in soil: <em>Azotobacter</em> and <em>Azospirillum</em>.</li>
        <li><strong>Fungi (Mycorrhiza):</strong> Genus <strong><em>Glomus</em></strong> forms symbiotic associations with roots. Absorbs <strong>phosphorus</strong> from soil, confers resistance to root-borne pathogens, salinity, and drought tolerance.</li>
        <li><strong>Cyanobacteria (Blue-green algae):</strong> Autotrophic nitrogen fixers in paddy fields: <em>Anabaena, Nostoc, Oscillatoria</em>. Add organic matter and improve fertility.</li>
      </ul>
    </li>
  </ul>
</div>
"""

    m08_revision = r"""
<div class="quick-revision-box">
  <h4>High-Yield Revision — Microbes in Human Welfare</h4>
  <ul>
    <li><strong>Curd & LAB:</strong> Enriches Vitamin B12, checks gut pathogens. Swiss cheese: Propionibacterium sharmanii (CO2 holes).</li>
    <li><strong>Industrial Key Molecules:</strong>
      <ul>
        <li>Streptokinase (<em>Streptococcus</em>) $\to$ Clot buster for myocardial infarction.</li>
        <li>Cyclosporin A (<em>Trichoderma polysporum</em>) $\to$ Immunosuppressant for organ transplants.</li>
        <li>Statins (<em>Monascus purpureus</em>) $\to$ Blood cholesterol lowering (HMG-CoA reductase competitive inhibitor).</li>
      </ul>
    </li>
    <li><strong>STP Principle:</strong> Aeration tank (aerobic flocs reduce BOD) $\to$ Settling tank $\to$ Anaerobic sludge digester (methanogens produce biogas).</li>
    <li><strong>Biocontrol:</strong> Ladybird (aphids), Dragonfly (mosquitoes), Baculoviruses / Nucleopolyhedrovirus (narrow-spectrum IPM).</li>
    <li><strong>Biofertilizers:</strong> Glomus (mycorrhiza absorbs Phosphorus), Rhizobium, Azotobacter, Azospirillum, Cyanobacteria (Anabaena, Nostoc in paddy).</li>
  </ul>
</div>
"""

    m08_flashcards = [
      {"q": "What is the source and medical function of Cyclosporin A?", "a": "Cyclosporin A is produced by the fungus Trichoderma polysporum and is used as an immunosuppressive agent in patients undergoing organ transplantation."},
      {"q": "How do statins lower blood cholesterol levels and what organism produces them?", "a": "Statins are produced by the yeast Monascus purpureus. They lower blood cholesterol by acting as competitive inhibitors of the enzyme responsible for cholesterol synthesis (HMG-CoA reductase)."},
      {"q": "What are flocs and what role do they play in biological sewage treatment?", "a": "Flocs are masses of aerobic bacteria associated with fungal filaments forming mesh-like networks. In aeration tanks, they consume organic matter, dramatically lowering the Biochemical Oxygen Demand (BOD)."},
      {"q": "What bacterium produces the 'clot buster' enzyme streptokinase?", "a": "Streptococcus; modified strains produce streptokinase, used clinically to dissolve blood clots in patients suffering from myocardial infarction."},
      {"q": "Why are Baculoviruses (Nucleopolyhedrovirus) considered ideal for Integrated Pest Management (IPM)?", "a": "They are narrow-spectrum, species-specific insecticidal pathogens that kill target pests without harming beneficial non-target insects, mammals, birds, or fish."},
      {"q": "What specific nutrient benefit does the fungal genus Glomus provide to plants through mycorrhizae?", "a": "Glomus absorbs phosphorus from soil and transfers it to the plant, while providing enhanced resistance to root pathogens and tolerance to drought and salinity."}
    ]

    m08_flow = [
      {"id": "mb1", "title": "Household Fermentation", "badge": "Step 1", "desc": "Lactobacillus coagulates casein forming curd rich in Vitamin B12; yeast leavens bread and ferments beverages."},
      {"id": "mb2", "title": "Industrial Biomolecules", "badge": "Step 2", "desc": "Large-scale fermentors produce penicillin, organic acids, streptokinase clot buster, cyclosporin A, and statins."},
      {"id": "mb3", "title": "Primary Sewage Treatment", "badge": "Step 3", "desc": "Physical removal of floating debris by sequential filtration and grit by gravity sedimentation into primary sludge."},
      {"id": "mb4", "title": "Secondary Biological STP", "badge": "Step 4", "desc": "Aerobic flocs in aeration tanks oxidize organic matter, crashing BOD; settled activated sludge pumped to digesters."},
      {"id": "mb5", "title": "Biogas Methanogenesis", "badge": "Step 5", "desc": "Methanobacterium in anaerobic sludge digesters and cattle rumen converts organic waste into inflammable biogas (CH4, CO2)."},
      {"id": "mb6", "title": "Eco-Friendly Agriculture", "badge": "Step 6", "desc": "Bt crystals and Nucleopolyhedrovirus control pests; Rhizobium, Glomus (phosphorus), and cyanobacteria enrich soil naturally."}
    ]

    m08_mindmap = {
      "id": "root", "title": "Microbes in Welfare", "icon": "🧫", "children": [
        {"id": "household", "title": "Household & Industrial", "icon": "🧀", "children": [
          {"id": "h1", "title": "Curd: LAB (Vitamin B12); Swiss cheese: Propionibacterium (CO2)"},
          {"id": "h2", "title": "Clot Buster: Streptokinase from Streptococcus"},
          {"id": "h3", "title": "Immunosuppressant: Cyclosporin A from Trichoderma polysporum"},
          {"id": "h4", "title": "Cholesterol: Statins from Monascus purpureus (yeast)"}
        ]},
        {"id": "sewage", "title": "Sewage & Biogas", "icon": "♻️", "children": [
          {"id": "s1", "title": "Primary (Physical filtration/sedimentation) -> Effluent"},
          {"id": "s2", "title": "Secondary (Aerobic Flocs consume organic waste, reducing BOD)"},
          {"id": "s3", "title": "Anaerobic Digesters: Methanogens produce Biogas (CH4 + CO2)"}
        ]},
        {"id": "agriculture", "title": "Biocontrol & Biofertilizer", "icon": "🌾", "children": [
          {"id": "a1", "title": "Biocontrol: Ladybird (aphids), Bt (caterpillars), Baculoviruses (IPM)"},
          {"id": "a2", "title": "Biofertilizers: Rhizobium, Azotobacter, Glomus (Phosphorus absorption)"},
          {"id": "a3", "title": "Cyanobacteria: Anabaena, Nostoc, Oscillatoria in paddy fields"}
        ]}
      ]
    }

    m08_pages = [
      {"page_num": 1, "text": "Microbes in food production: Lactic Acid Bacteria LAB converts milk to curd increasing Vitamin B12. Saccharomyces cerevisiae baker's yeast leavens bread. Swiss cheese holes caused by Propionibacterium sharmanii releasing CO2. Penicillin discovered by Alexander Fleming from Penicillium notatum."},
      {"page_num": 2, "text": "Bioactive molecules: Streptokinase from Streptococcus dissolves clots. Cyclosporin A from Trichoderma polysporum is an immunosuppressant. Statins from Monascus purpureus inhibit cholesterol synthesis. Sewage treatment uses aerobic flocs to reduce BOD followed by anaerobic digestion producing biogas."},
      {"page_num": 3, "text": "Biocontrol and biofertilizers: Bacillus thuringiensis Bt crystal toxins kill caterpillars. Nucleopolyhedrovirus baculoviruses provide narrow-spectrum pest control. Glomus mycorrhizae absorb phosphorus. Nitrogen fixing cyanobacteria Anabaena and Nostoc fertilize paddy fields."}
    ]

    topics.append({
      "id": "bio-ch08-microbes-welfare",
      "title": "08. Microbes in Human Welfare",
      "subject": "bio",
      "subject_title": "Biology • Class 12",
      "reading_time_min": 13,
      "has_handwritten": False,
      "detailed_html": m08_detailed,
      "revision_html": m08_revision,
      "flashcards": m08_flashcards,
      "flow_data": m08_flow,
      "mindmap_data": m08_mindmap,
      "pages": m08_pages
    })

    # =========================================================================
    # MODULE 09: BIOTECHNOLOGY: PRINCIPLES AND PROCESSES
    # =========================================================================
    m09_detailed = r"""
<div class="topic-header">
  <span class="topic-num">UNIT IX • TOPIC 09 OF 13</span>
  <h3 class="topic-title">Biotechnology: Principles and Processes</h3>
</div>

<div class="concept-card">
  <div class="card-label">CORE PRINCIPLES & TOOLS OF RECOMBINANT DNA TECHNOLOGY</div>
  <p>Biotechnology deals with techniques of using live organisms or enzymes from organisms to produce products and processes useful to humans. European Federation of Biotechnology (EFB) defines it as <em>"The integration of natural science and organisms, cells, parts thereof, and molecular analogues for products and services."</em></p>
  <ul>
    <li><strong>Core Techniques:</strong>
      <ol>
        <li><em>Genetic Engineering:</em> Techniques to alter chemistry of genetic material (DNA/RNA) to introduce into host organisms and change phenotype. Stanley Cohen and Herbert Boyer constructed first recombinant DNA in <strong>1972</strong> by combining antibiotic resistance gene with native plasmid of <em>Salmonella typhimurium</em>.</li>
        <li><em>Bioprocess Engineering:</em> Maintenance of sterile ambience in chemical engineering processes to enable growth of only desired microbe/cell in large quantities.</li>
      </ol>
    </li>
    <li><strong>Tools of Recombinant DNA Technology:</strong>
      <ul>
        <li><strong>Restriction Endonucleases ("Molecular Scissors"):</strong> Discovered in 1963 in <em>E. coli</em>. Cut DNA at specific <strong>palindromic nucleotide sequences</strong> (reads same $5'\to 3'$ on both complementary strands).
          <ul>
            <li>Nomenclature: <em>EcoRI</em> $\to$ <strong>E</strong> = <em>Escherichia</em>, <strong>co</strong> = <em>coli</em>, <strong>R</strong> = strain RY13, <strong>I</strong> = first endonuclease isolated.</li>
            <li>EcoRI recognition site:
              <div class="formula-block">
                $5'\text{--G} \downarrow \text{A-A-T-T-C--}3'$<br>
                $3'\text{--C-T-T-A-A} \uparrow \text{G--}5'$
              </div>
            </li>
            <li>Produces overhanging single-stranded sticky ends. <strong>DNA Ligase</strong> joins complementary sticky ends via phosphodiester bonds.</li>
          </ul>
        </li>
        <li><strong>Agarose Gel Electrophoresis:</strong> Separates cut DNA fragments by size/charge. Negatively charged DNA migrates toward positive electrode (anode) through agarose matrix (from sea weeds). Smaller fragments move farther. Stained with <strong>Ethidium Bromide (EtBr)</strong> and exposed to UV light: visible as <strong>bright orange bands</strong>. Cutting out and extracting DNA from gel = <strong>Elution</strong>.</li>
      </ul>
    </li>
  </ul>
</div>

<div class="concept-card">
  <div class="card-label">CLONING VECTORS & COMPETENT HOST TRANSFORMATION</div>
  <ul>
    <li><strong>Essential Features of a Cloning Vector (e.g. pBR322):</strong>
      <ol>
        <li><strong>Origin of Replication (ori):</strong> Specific sequence where replication starts. Controls the <strong>copy number</strong> of linked foreign DNA.</li>
        <li><strong>Selectable Markers:</strong> Help identify and eliminate non-transformants while permitting selective growth of transformants. Normal <em>E. coli</em> lacks antibiotic resistance; plasmid genes for resistance to <strong>ampicillin ($amp^R$)</strong> and <strong>tetracycline ($tet^R$)</strong> serve as selectable markers.</li>
        <li><strong>Cloning / Recognition Sites:</strong> Must have single/unique recognition sites for restriction enzymes (multiple sites generate fragments, complicating cloning).
          <ul>
            <li><em>Insertional Inactivation:</em> Insertion of foreign DNA at <em>BamHI</em> site within $tet^R$ gene of pBR322 inactivates tetracycline resistance. Transformants grow on ampicillin but die on tetracycline, identifying recombinants!</li>
            <li><em>Blue-White Screening:</em> Recombinant DNA inserted into coding sequence of <strong>$\beta$-galactosidase ($lacZ$)</strong> gene. Non-recombinants produce active enzyme giving <strong>blue colonies</strong> with chromogenic substrate; recombinants with inactivated gene produce <strong>white colonies</strong>.</li>
          </ul>
        </li>
      </ol>
    </li>
    <li><strong>Vectors for Plants and Animals:</strong>
      <ul>
        <li><em>Agrobacterium tumefaciens</em>: Soil bacterium delivering <strong>T-DNA</strong> via <strong>Ti-plasmid</strong> (Tumor-inducing) into dicot plants; disarmed Ti-plasmid is used to deliver desired genes without inducing crown gall tumors.</li>
        <li><em>Retroviruses:</em> Disarmed retroviruses used to deliver foreign genes into mammalian host cells.</li>
      </ul>
    </li>
    <li><strong>Making Host Competent for Transformation:</strong> DNA is hydrophilic and cannot pass through cell membranes:
      <ul>
        <li><em>Chemical Treatment:</em> Incubate with divalent cation ($\text{Ca}^{2+}$) to increase pore permeability $\to$ <strong>Heat Shock</strong> ($42^\circ\text{C}$ for brief pulse, then placed back on ice).</li>
        <li><em>Micro-injection:</em> Recombinant DNA injected directly into nucleus of animal cell using micropipette.</li>
        <li><em>Biolistics / Gene Gun:</em> Plant cells bombarded with high-velocity micro-projectiles of <strong>gold or tungsten</strong> coated with DNA.</li>
      </ul>
    </li>
  </ul>
</div>

<div class="remember-box">
  <strong>PROCESSES OF rDNA TECHNOLOGY & BIOREACTORS:</strong>
  <ol>
    <li><strong>Isolation of DNA:</strong> Cell wall degraded using <strong>Lysozyme</strong> (bacteria), <strong>Cellulase</strong> (plant cells), or <strong>Chitinase</strong> (fungi). RNA removed by RNase, proteins by Protease. Pure DNA precipitated by adding <strong>chilled ethanol</strong>, spooled out as fine threads (<strong>Spooling</strong>).</li>
    <li><strong>PCR (Polymerase Chain Reaction - Kary Mullis 1983):</strong> In vitro gene amplification billion-fold through 3 cyclic steps:
      <ul>
        <li><em>1. Denaturation ($94\text{--}96^\circ\text{C}$):</em> Target double-stranded DNA separated into single strands.</li>
        <li><em>2. Annealing ($50\text{--}56^\circ\text{C}$):</em> Two sets of synthetic oligonucleotide primers bind to complementary ends.</li>
        <li><em>3. Extension ($72^\circ\text{C}$):</em> Thermostable <strong>Taq Polymerase</strong> (isolated from thermophilic bacterium <em>Thermus aquaticus</em>) synthesizes new DNA using dNTPs and $\text{Mg}^{2+}$.</li>
      </ul>
    </li>
    <li><strong>Bioreactors (100–1000 Liters):</strong> Large stainless steel vessels providing optimal temperature, pH, substrate, oxygen, and agitator for mass microbial cell culture:
      <ul>
        <li><em>Simple Stirred-Tank Bioreactor:</em> Curved base to facilitate mixing; agitator ensures homogeneous oxygen and nutrient distribution.</li>
        <li><em>Sparged Stirred-Tank Bioreactor:</em> Sterile air bubbles sparged through liquid to dramatically increase surface area for oxygen transfer.</li>
      </ul>
    </li>
    <li><strong>Downstream Processing:</strong> Series of processes including <strong>separation and purification</strong> of biosynthetic product, formulation with suitable preservatives, clinical trials, and stringent quality control testing before commercial release.</li>
  </ol>
</div>
"""

    m09_revision = r"""
<div class="quick-revision-box">
  <h4>High-Yield Revision — Biotechnology: Principles & Processes</h4>
  <ul>
    <li><strong>Cohen & Boyer (1972):</strong> First rDNA constructed using Salmonella typhimurium plasmid.</li>
    <li><strong>Restriction Enzymes:</strong> Molecular scissors; EcoRI cuts $5'\text{-GAATTC-}3'$ creating sticky ends.</li>
    <li><strong>Gel Electrophoresis:</strong> DNA moves to anode; stained with Ethidium Bromide, fluoresces bright orange under UV; extracted by Elution.</li>
    <li><strong>Vector Essentials:</strong> Origin of replication (ori, copy number), Selectable markers (ampR, tetR), Cloning sites.</li>
    <li><strong>Blue-White Selection:</strong> Insertional inactivation of beta-galactosidase (lacZ) -> Recombinant colonies are white; non-recombinant colonies are blue.</li>
    <li><strong>Competence:</strong> Ca2+ treatment + Heat shock (42°C); Micro-injection (animals); Gene gun / Biolistics (Gold/Tungsten in plants).</li>
    <li><strong>PCR Steps:</strong> Denaturation (94°C) $\to$ Annealing (54°C) $\to$ Extension (72°C via Taq Polymerase from <em>Thermus aquaticus</em>).</li>
    <li><strong>Downstream Processing:</strong> Separation, purification, quality testing of finished product.</li>
  </ul>
</div>
"""

    m09_flashcards = [
      {"q": "What is a palindromic sequence in DNA and give the EcoRI recognition palindrome?", "a": "A sequence that reads identical on both strands when reading in the 5' to 3' direction. EcoRI recognizes 5'-GAATTC-3' and cuts between G and A."},
      {"q": "Why is Taq polymerase exclusively used in PCR rather than normal DNA polymerase?", "a": "Taq polymerase (from thermophilic bacterium Thermus aquaticus) is thermostable and remains active through repeated high-temperature denaturation cycles at 94°C."},
      {"q": "How does insertional inactivation of the lacZ gene differentiate recombinants from non-recombinants?", "a": "Insertional inactivation disrupts the beta-galactosidase enzyme. On chromogenic substrate, recombinants form white colonies, while non-recombinants form blue colonies."},
      {"q": "What is the function of the 'ori' (origin of replication) sequence in a cloning vector?", "a": "It is the specific DNA sequence that initiates DNA replication and dictates the copy number of the cloned target DNA inside the host cell."},
      {"q": "What is the difference between micro-injection and biolistics (gene gun)?", "a": "Micro-injection injects foreign rDNA directly into the nucleus of an animal cell using a micropipette. Biolistics bombards plant cells with gold or tungsten microparticles coated with DNA."},
      {"q": "What is 'downstream processing' in biotechnology manufacturing?", "a": "The post-bioreactor stages involving product isolation, separation, purification, preservation, and clinical quality control testing before market distribution."}
    ]

    m09_flow = [
      {"id": "bp1", "title": "DNA Cleavage & Isolation", "badge": "Step 1", "desc": "Cell lysis via lysozyme/cellulase/chitinase; DNA cut with restriction endonuclease at palindromic site."},
      {"id": "bp2", "title": "Gel Separation & Elution", "badge": "Step 2", "desc": "Fragments resolved on agarose gel, visualized by EtBr under UV as orange bands, cut out and eluted."},
      {"id": "bp3", "title": "Gene Amplification (PCR)", "badge": "Step 3", "desc": "Denaturation at 94°C -> Primer Annealing at 54°C -> Extension at 72°C via Taq polymerase across 30 cycles."},
      {"id": "bp4", "title": "Vector Ligation", "badge": "Step 4", "desc": "DNA ligase joins sticky ends of gene of interest into linearized plasmid vector (e.g. pBR322)."},
      {"id": "bp5", "title": "Host Transformation", "badge": "Step 5", "desc": "Ca2+ heat shock, microinjection, or gene gun introduces rDNA into competent host; screened by blue-white selection."},
      {"id": "bp6", "title": "Bioreactor & Downstream", "badge": "Step 6", "desc": "Large-scale stirred-tank fermentation for product synthesis, followed by downstream separation and purification."}
    ]

    m09_mindmap = {
      "id": "root", "title": "Biotech: Principles", "icon": "🧬", "children": [
        {"id": "tools", "title": "Core Tools", "icon": "✂️", "children": [
          {"id": "t1", "title": "Restriction Endonucleases: Palindromic EcoRI (5'-GAATTC-3')"},
          {"id": "t2", "title": "Agarose Gel: EtBr orange bands under UV, Elution"},
          {"id": "t3", "title": "Ligase (joins sticky ends) & Lysozyme/Cellulase/Chitinase"}
        ]},
        {"id": "vectors", "title": "Cloning Vectors", "icon": "🚢", "children": [
          {"id": "v1", "title": "pBR322: ori, ampR, tetR selectable markers"},
          {"id": "v2", "title": "Blue-White selection: lacZ insertional inactivation"},
          {"id": "v3", "title": "Ti-plasmid (Agrobacterium for plants) & Disarmed retrovirus"}
        ]},
        {"id": "transformation", "title": "Competent Hosts", "icon": "🧫", "children": [
          {"id": "h1", "title": "Bacteria: Ca2+ + Heat shock at 42°C"},
          {"id": "h2", "title": "Animals: Micro-injection directly into nucleus"},
          {"id": "h3", "title": "Plants: Gene gun / Biolistics (Gold or Tungsten microparticles)"}
        ]},
        {"id": "processes", "title": "Processes & Scaling", "icon": "🏭", "children": [
          {"id": "p1", "title": "PCR: Denaturation (94°C) -> Annealing (54°C) -> Extension (72°C, Taq)"},
          {"id": "p2", "title": "Bioreactors: Simple stirred vs Sparged stirred-tank"},
          {"id": "p3", "title": "Downstream processing: Separation, purification, quality testing"}
        ]}
      ]
    }

    m09_pages = [
      {"page_num": 1, "text": "Principles of biotechnology: Cohen and Boyer in 1972 created first recombinant DNA. Restriction endonucleases cut at palindromic sequences like EcoRI 5'-GAATTC-3' generating sticky ends. Agarose gel electrophoresis separates DNA stained with Ethidium Bromide showing orange bands under UV."},
      {"page_num": 2, "text": "Cloning vectors require origin of replication ori, selectable markers like ampicillin and tetracycline resistance, and single cloning sites. Insertional inactivation of lacZ gene produces white recombinant colonies. Competent cells made using calcium chloride and heat shock, or microinjection and gene gun."},
      {"page_num": 3, "text": "Polymerase Chain Reaction PCR involves denaturation at 94°C, annealing with primers at 54°C, and extension using Taq polymerase from Thermus aquaticus at 72°C. Large scale production in stirred-tank bioreactors followed by downstream processing purification."}
    ]

    topics.append({
      "id": "bio-ch09-biotech-principles",
      "title": "09. Biotechnology: Principles and Processes",
      "subject": "bio",
      "subject_title": "Biology • Class 12",
      "reading_time_min": 15,
      "has_handwritten": False,
      "detailed_html": m09_detailed,
      "revision_html": m09_revision,
      "flashcards": m09_flashcards,
      "flow_data": m09_flow,
      "mindmap_data": m09_mindmap,
      "pages": m09_pages
    })

    # =========================================================================
    # MODULE 10: BIOTECHNOLOGY AND ITS APPLICATIONS
    # =========================================================================
    m10_detailed = r"""
<div class="topic-header">
  <span class="topic-num">UNIT IX • TOPIC 10 OF 13</span>
  <h3 class="topic-title">Biotechnology and its Applications</h3>
</div>

<div class="concept-card">
  <div class="card-label">APPLICATIONS IN AGRICULTURE: BT COTTON & RNAi</div>
  <ul>
    <li><strong>Genetically Modified Organisms (GMOs):</strong> Plants, bacteria, fungi, and animals whose genes have been altered by manipulation:
      <ul>
        <li>Increases tolerance to abiotic stresses (cold, drought, salt, heat).</li>
        <li>Reduces reliance on chemical pesticides (pest-resistant crops).</li>
        <li>Helps reduce post-harvest losses and increases efficiency of mineral usage.</li>
        <li>Enhances nutritional value: e.g. <strong>Golden Rice</strong> (enriched with <strong>Vitamin A / $\beta$-carotene</strong>).</li>
      </ul>
    </li>
    <li><strong>Bt Cotton (Insect Pest Resistance):</strong>
      <ul>
        <li>Soil bacterium <em>Bacillus thuringiensis</em> produces insecticidal crystalline proteins (<strong>Cry proteins</strong>).</li>
        <li>Toxin exists as inactive <strong>protoxin</strong> in bacterium. Once ingested by insect, the <strong>alkaline pH of insect midgut</strong> solubilizes the crystal, activating the toxin.</li>
        <li>Activated toxin binds to surface of midgut epithelial cells, creates pores that cause cell swelling and lysis, killing the insect.</li>
        <li><em>Gene Specificity:</em> <strong>CryIAc</strong> and <strong>CryIIAb</strong> control <strong>cotton bollworms</strong>; <strong>CryIAb</strong> controls <strong>corn borer</strong>.</li>
      </ul>
    </li>
    <li><strong>RNA Interference (RNAi) in Tobacco Roots:</strong>
      <ul>
        <li>Nematode <em>Meloidogyne incognita</em> infects tobacco roots, causing severe yield reduction.</li>
        <li><strong>RNAi Mechanism:</strong> Natural cellular defense in all eukaryotes involving sequence-specific silencing of target mRNA by complementary double-stranded RNA (<strong>dsRNA</strong>).</li>
        <li>Using <em>Agrobacterium</em> vectors, nematode-specific genes introduced into host plant in both <strong>sense and antisense</strong> orientations.</li>
        <li>Both RNAs hybridize to form dsRNA, triggering RNAi that cleaves the nematode mRNA. Nematode cannot survive in transgenic tobacco host!</li>
      </ul>
    </li>
  </ul>
</div>

<div class="concept-card">
  <div class="card-label">APPLICATIONS IN MEDICINE: HUMULIN & GENE THERAPY</div>
  <ul>
    <li><strong>Genetically Engineered Insulin (Humulin):</strong>
      <ul>
        <li>Human insulin synthesized as a pro-hormone containing: <strong>Chain A (21 aa) + Chain B (30 aa) + C-peptide (33 aa)</strong>. In mature functional insulin, <strong>C-peptide is removed</strong>, and Chains A and B are linked by two <strong>disulfide bridges</strong>.</li>
        <li>Earlier, insulin was extracted from pancreas of slaughtered cattle and pigs, causing severe allergic reactions.</li>
        <li>In <strong>1983, Eli Lilly</strong> (American company) synthesized two separate DNA sequences corresponding to A and B chains, inserted them into plasmids of <em>E. coli</em>, produced chains separately, extracted them, and joined them by creating <strong>disulfide bonds</strong> to form mature human insulin!</li>
      </ul>
    </li>
    <li><strong>Gene Therapy (ADA Deficiency):</strong>
      <ul>
        <li>Collection of methods that allows correction of a gene defect diagnosed in a child or embryo.</li>
        <li>First clinical gene therapy performed in <strong>1990</strong> on a <strong>4-year-old girl</strong> with <strong>Adenosine Deaminase (ADA) deficiency</strong> (crucial enzyme for immune system function, leading to Severe Combined Immunodeficiency SCID).</li>
        <li><em>Method:</em> Lymphocytes extracted from patient's blood $\to$ cultured in vitro $\to$ functional human ADA cDNA introduced using <strong>retroviral vector</strong> $\to$ returned to patient. Because lymphocytes have limited lifespan, periodic infusions required. Permanent cure: introduce ADA gene into cells at <strong>early embryonic stages</strong> (bone marrow stem cells).</li>
      </ul>
    </li>
    <li><strong>Molecular Diagnosis:</strong> Recombinant DNA, PCR, and ELISA enable detection of pathogen when concentration is extremely low:
      <ul>
        <li>PCR detects minute traces of HIV in suspected AIDS patients and point mutations in cancer genes.</li>
        <li>ELISA detects presence of antigens (proteins, glycoproteins) or antibodies synthesized against pathogen.</li>
      </ul>
    </li>
  </ul>
</div>

<div class="remember-box">
  <strong>TRANSGENIC ANIMALS & BIOETHICAL ISSUES:</strong>
  <ul>
    <li><strong>Transgenic Animals:</strong> Animals that have had their DNA manipulated to possess and express an extra foreign gene. $>95\%$ of all existing transgenic animals are <strong>mice</strong>.
      <ul>
        <li><em>Study of Normal Physiology & Development:</em> Study of gene regulation and growth factors (e.g. Insulin-like Growth Factor).</li>
        <li><em>Study of Human Diseases:</em> Transgenic animal models for cancer, cystic fibrosis, rheumatoid arthritis, Alzheimer's disease.</li>
        <li><em>Biological Products:</em> Human protein <strong>$\alpha$-1-antitrypsin</strong> produced to treat <strong>emphysema</strong>. <strong>Rosie (1997):</strong> First transgenic cow produced human protein-enriched milk (<strong>$2.4\text{ g/liter}$</strong>) containing human <strong>$\alpha$-lactalbumin</strong>, nutritionally far superior for human babies.</li>
        <li><em>Vaccine & Chemical Safety Testing:</em> Transgenic mice replace monkeys to test safety of polio vaccines before human trials.</li>
      </ul>
    </li>
    <li><strong>Ethical Issues & Biopiracy:</strong>
      <ul>
        <li><strong>GEAC (Genetic Engineering Appraisal Committee):</strong> Indian government body that evaluates validity of GM research and safety of introducing GMOs for public use.</li>
        <li><strong>Biopiracy:</strong> Use of bio-resources by multinational corporations and other organizations without proper authorization from the countries and people concerned without compensatory payment.</li>
        <li><em>Case Study:</em> In 1997, a US company got patent rights on <strong>Basmati Rice</strong> through the US Patent and Trademark Office by crossing with semi-dwarf varieties and claiming it as an invention. India has 200,000 varieties of rice (27 documented Basmati varieties). Indian Patent Bill amended to counter such piracy.</li>
      </ul>
    </li>
  </ul>
</div>
"""

    m10_revision = r"""
<div class="quick-revision-box">
  <h4>High-Yield Revision — Biotech Applications</h4>
  <ul>
    <li><strong>Bt Cotton:</strong> Bacillus thuringiensis Cry protoxin activated by alkaline pH in insect gut $\to$ midgut epithelial lysis. CryIAc & CryIIAb (bollworm); CryIAb (corn borer).</li>
    <li><strong>RNAi:</strong> Cellular defense in eukaryotes; dsRNA silences target mRNA of <em>Meloidogyne incognita</em> in tobacco.</li>
    <li><strong>Humulin (Eli Lilly 1983):</strong> Separate synthesis of Chain A (21 aa) and Chain B (30 aa) in E. coli linked by disulfide bonds. Mature insulin lacks C-peptide.</li>
    <li><strong>ADA Gene Therapy (1990):</strong> 4-year-old girl with SCID treated using retroviral vector delivering ADA cDNA into lymphocytes.</li>
    <li><strong>Rosie the Cow (1997):</strong> Transgenic cow producing human alpha-lactalbumin enriched milk (2.4 g/L).</li>
    <li><strong>Emphysema:</strong> Treated using human protein $\alpha$-1-antitrypsin.</li>
    <li><strong>GEAC:</strong> Regulates GMO approvals in India. Biopiracy: Unethical exploitation of indigenous bioresources (Basmati patent controversy).</li>
  </ul>
</div>
"""

    m10_flashcards = [
      {"q": "Why does the Bt toxin not kill the bacterium Bacillus thuringiensis itself?", "a": "The toxin exists as an inactive crystalline protoxin inside the bacterium. It is only converted into its active lethal form in the alkaline pH of the insect midgut."},
      {"q": "What specific Cry genes are used to protect cotton against bollworms versus corn against borers?", "a": "CryIAc and CryIIAb control cotton bollworms, while CryIAb controls the corn borer."},
      {"q": "How was genetically engineered human insulin (Humulin) created by Eli Lilly in 1983?", "a": "They synthesized two DNA sequences for insulin chains A and B separately, inserted them into E. coli plasmids, produced and isolated chains A and B, and joined them with disulfide bonds (omitting the C-peptide)."},
      {"q": "What was the first clinical gene therapy disease and how was it delivered?", "a": "Adenosine Deaminase (ADA) deficiency in a 4-year-old girl in 1990. Functional ADA cDNA was inserted into the patient's cultured lymphocytes using a retroviral vector and re-infused."},
      {"q": "What is the commercial and nutritional significance of the transgenic cow 'Rosie'?", "a": "Produced in 1997, Rosie produced human protein-enriched milk (2.4 g/L) containing human alpha-lactalbumin, making it nutritionally more balanced for human babies than natural cow milk."},
      {"q": "What is biopiracy? Cite the landmark Indian agricultural example.", "a": "Biopiracy is the commercial exploitation of biological resources and traditional knowledge by foreign entities without proper authorization or fair compensation, such as the 1997 US patent on Indian Basmati rice."}
    ]

    m10_flow = [
      {"id": "ba1", "title": "Agricultural Pest Defense", "badge": "Step 1", "desc": "Bt Cry genes cloned into cotton; alkaline midgut pH activates protoxin, creating pores and killing bollworms."},
      {"id": "ba2", "title": "RNA Interference", "badge": "Step 2", "desc": "Agrobacterium introduces sense/antisense genes into tobacco; dsRNA silences Meloidogyne nematode mRNA."},
      {"id": "ba3", "title": "Humulin Synthesis", "badge": "Step 3", "desc": "Eli Lilly synthesizes Chain A and Chain B in E. coli; chains purified and joined by disulfide bridges without C-peptide."},
      {"id": "ba4", "title": "Clinical Gene Therapy", "badge": "Step 4", "desc": "ADA deficiency treated by retroviral cDNA delivery into patient lymphocytes; permanent cure requires embryonic stem cell integration."},
      {"id": "ba5", "title": "Transgenic Animal Models", "badge": "Step 5", "desc": "Mice models for human diseases; Rosie the cow producing human alpha-lactalbumin milk (2.4 g/L); alpha-1-antitrypsin for emphysema."},
      {"id": "ba6", "title": "Bioethics & Patenting", "badge": "Step 6", "desc": "GEAC regulates GMO release; patent enforcement against biopiracy of Basmati rice, Neem, and Turmeric."}
    ]

    m10_mindmap = {
      "id": "root", "title": "Biotech: Applications", "icon": "🌽", "children": [
        {"id": "agriculture", "title": "Agriculture", "icon": "🌱", "children": [
          {"id": "ag1", "title": "Bt Cotton: CryIAc & CryIIAb (bollworm); CryIAb (corn borer)"},
          {"id": "ag2", "title": "Alkaline gut pH converts protoxin -> active pore-forming toxin"},
          {"id": "ag3", "title": "RNAi: dsRNA silences Meloidogyne incognita in tobacco"},
          {"id": "ag4", "title": "Golden Rice: Vitamin A / beta-carotene enriched"}
        ]},
        {"id": "medicine", "title": "Medicine", "icon": "💉", "children": [
          {"id": "md1", "title": "Humulin (Eli Lilly 1983): Chain A + B via disulfide bonds (no C-peptide)"},
          {"id": "md2", "title": "Gene Therapy (1990): ADA deficiency via retroviral vector in lymphocytes"},
          {"id": "md3", "title": "Molecular Diagnostics: PCR (early HIV/cancer) & ELISA"}
        ]},
        {"id": "animals", "title": "Transgenic Animals & Ethics", "icon": "🐄", "children": [
          {"id": "an1", "title": "Rosie Cow: Human alpha-lactalbumin milk (2.4 g/L)"},
          {"id": "an2", "title": "alpha-1-antitrypsin treats emphysema; Polio vaccine testing in mice"},
          {"id": "an3", "title": "GEAC regulation & Biopiracy of Basmati rice"}
        ]}
      ]
    }

    m10_pages = [
      {"page_num": 1, "text": "Biotechnology in agriculture: Bt cotton uses Cry proteins from Bacillus thuringiensis. Inactive protoxin dissolved by alkaline pH in insect gut creating pores. CryIAc and CryIIAb control bollworms, CryIAb controls corn borer. RNA interference uses dsRNA to silence Meloidogyne incognita in tobacco."},
      {"page_num": 2, "text": "Biotechnology in medicine: Genetically engineered insulin Humulin created by Eli Lilly in 1983 by synthesizing chains A and B in E. coli linked by disulfide bonds without C-peptide. Gene therapy for ADA deficiency in 1990 used retroviral vectors. Molecular diagnosis using PCR and ELISA."},
      {"page_num": 3, "text": "Transgenic animals and ethics: Over 95% transgenic animals are mice. Rosie cow in 1997 produced milk with 2.4 g/L human alpha-lactalbumin. Alpha-1-antitrypsin treats emphysema. GEAC regulates GMO safety in India. Biopiracy controversies over Basmati rice patenting."}
    ]

    topics.append({
      "id": "bio-ch10-biotech-applications",
      "title": "10. Biotechnology and its Applications",
      "subject": "bio",
      "subject_title": "Biology • Class 12",
      "reading_time_min": 14,
      "has_handwritten": False,
      "detailed_html": m10_detailed,
      "revision_html": m10_revision,
      "flashcards": m10_flashcards,
      "flow_data": m10_flow,
      "mindmap_data": m10_mindmap,
      "pages": m10_pages
    })

    # =========================================================================
    # MODULE 11: ORGANISMS AND POPULATIONS
    # =========================================================================
    m11_detailed = r"""
<div class="topic-header">
  <span class="topic-num">UNIT X • TOPIC 11 OF 13</span>
  <h3 class="topic-title">Organisms and Populations</h3>
</div>

<div class="concept-card">
  <div class="card-label">ABIOTIC FACTORS & ADAPTIVE RESPONSES</div>
  <p>Ecology is fundamentally concerned with four levels of biological organization: <strong>Organisms, Populations, Communities, and Biomes</strong>.</p>
  <ul>
    <li><strong>Major Abiotic Factors:</strong>
      <ul>
        <li><strong>Temperature:</strong> Most ecologically relevant environmental factor. Dictates enzyme kinetics and basal metabolism. <em>Eurythermal:</em> tolerate wide temperature range; <em>Stenothermal:</em> restricted to narrow temperature range.</li>
        <li><strong>Water:</strong> Next in importance. Salinity (parts per thousand, ppt): $<5\text{ ppt}$ (inland water), $30\text{--}35\text{ ppt}$ (sea), $>100\text{ ppt}$ (hypersaline lagoons). <em>Euryhaline</em> (wide salinity tolerance) vs <em>Stenohaline</em> (narrow salinity tolerance).</li>
        <li><strong>Light:</strong> Photosynthesis, photoperiodic flowering, diurnal circadian rhythms.</li>
        <li><strong>Soil:</strong> Composition, grain size, percolation, and water-holding capacity dictate vegetation.</li>
      </ul>
    </li>
    <li><strong>Responses to Abiotic Factors:</strong>
      <ol>
        <li><em>Regulate:</em> Maintain constant internal homeostasis by physiological means (thermoregulation and osmoregulation). All birds, mammals, and very few lower vertebrates (e.g. human core $37^\circ\text{C}$).</li>
        <li><em>Conform:</em> $99\%$ of all animals and nearly all plants cannot maintain constant internal environment; body temperature fluctuates with ambient temperature.</li>
        <li><em>Migrate:</em> Move away temporarily from stressful habitat to more hospitable area and return when stressful period is over (e.g. Siberian cranes migrate to <strong>Keoladeo National Park in Bharatpur, Rajasthan</strong>).</li>
        <li><em>Suspend:</em> Escape in time. Bacterial/fungal thick-walled spores; seed dormancy; <strong>Hibernation</strong> (winter sleep in bears); <strong>Aestivation</strong> (summer sleep in snails and fish); <strong>Diapause</strong> (stage of suspended development in zooplankton).</li>
      </ol>
    </li>
    <li><strong>Morphological & Physiological Adaptations:</strong>
      <ul>
        <li><em>Kangaroo Rat (North American Desert):</em> Capable of meeting entire water requirement through <strong>internal fat oxidation</strong> (water as by-product); highly concentrated urine.</li>
        <li><em>Desert Plants:</em> Thick cuticle, sunken stomata arranged in pits, <strong>CAM photosynthetic pathway</strong> (stomata open at night), leaves reduced to spines (e.g. <em>Opuntia</em> with photosynthetic flattened stems called phylloclades).</li>
        <li><strong>Allen's Rule:</strong> Mammals from colder climates have <strong>shorter ears and limbs</strong> to minimize heat loss.</li>
        <li><em>Blubber in Polar Seals:</em> Thick subcutaneous fat layer acting as thermal insulator.</li>
        <li><em>Altitude Sickness:</em> Low atmospheric pressure at $>3,500\text{ m}$ (e.g. Rohtang Pass) causes hypoxia (nausea, fatigue, palpitations). Body acclimatizes by <strong>increasing RBC production, decreasing binding affinity of hemoglobin, and increasing breathing rate</strong>.</li>
      </ul>
    </li>
  </ul>
</div>

<div class="concept-card">
  <div class="card-label">POPULATION ATTRIBUTES & MATHEMATICAL GROWTH MODELS</div>
  <ul>
    <li><strong>Population Attributes:</strong> Birth rate (natality per capita), Death rate (mortality per capita), Sex ratio, Age Pyramids (Triangular = Expanding; Bell-shaped = Stable; Urn-shaped = Declining).</li>
    <li><strong>Population Density Equation:</strong>
      <div class="formula-block">
        $N_{t+1} = N_t + [(B + I) - (D + E)]$<br>
        where $B$ = Natality, $I$ = Immigration, $D$ = Mortality, $E$ = Emigration.
      </div>
    </li>
    <li><strong>Growth Models:</strong>
      <ul>
        <li><strong>1. Exponential / Geometric Growth (J-shaped curve):</strong> Occurs when resources are unlimited:
          <div class="formula-block">
            $\frac{dN}{dt} = rN \implies N_t = N_0 e^{rt}$<br>
            where $r$ is the <strong>intrinsic rate of natural increase</strong> (measure of biotic potential). E.g., for Norway rat $r = 0.015$, flour beetle $r = 0.12$, human population in 1981 $r = 0.0205$.
          </div>
        </li>
        <li><strong>2. Logistic Growth (S-shaped / Sigmoid curve):</strong> Resources are finite and limiting. Population growth reaches an upper asymptote called <strong>Carrying Capacity ($K$)</strong>:
          <div class="formula-block">
            <strong>Verhulst-Pearl Logistic Growth:</strong> $\frac{dN}{dt} = rN \left(\frac{K - N}{K}\right)$<br>
            Phases: Lag phase $\to$ Acceleration / Deceleration phase $\to$ Asymptote (when $N \to K$). Considered more realistic model in nature.
          </div>
        </li>
      </ul>
    </li>
  </ul>
</div>

<div class="table-container">
  <div class="table-caption">NCERT Master Table: Population Interactions</div>
  <table class="notes-table">
    <thead>
      <tr><th>Type of Interaction</th><th>Species A</th><th>Species B</th><th>Authentic NCERT Ecological Example</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>Mutualism</strong></td><td>$+$ (Benefits)</td><td>$+$ (Benefits)</td><td>Lichens (fungus + alga); Mycorrhizae (fungus + plant); Fig tree & Wasp; <em>Ophrys</em> orchid pseudo-copulation with Colpa bee</td></tr>
      <tr><td><strong>Competition</strong></td><td>$-$ (Harmed)</td><td>$-$ (Harmed)</td><td>Abingdon tortoise in Galapagos extinct after goats introduced; MacArthur's warblers resource partitioning</td></tr>
      <tr><td><strong>Predation</strong></td><td>$+$ (Benefits)</td><td>$-$ (Harmed)</td><td>Tiger & Deer; Prickly pear cactus controlled by moth; Monarch butterfly chemical defense</td></tr>
      <tr><td><strong>Parasitism</strong></td><td>$+$ (Benefits)</td><td>$-$ (Harmed)</td><td>Ticks on dogs; <em>Cuscuta</em> on hedge plants; Human liver fluke; Brood parasitism (Cuckoo/Koel lays eggs in Crow's nest)</td></tr>
      <tr><td><strong>Commensalism</strong></td><td>$+$ (Benefits)</td><td>$0$ (Neutral)</td><td>Orchid epiphytic on mango branch; Barnacles on whale back; Cattle egret & grazing cattle; Sea anemone & Clownfish</td></tr>
      <tr><td><strong>Amensalism</strong></td><td>$-$ (Harmed)</td><td>$0$ (Neutral)</td><td><em>Penicillium</em> secreting penicillin antibiotic inhibiting bacterial growth without benefit/harm to fungus</td></tr>
    </tbody>
  </table>
</div>

<div class="remember-box">
  <strong>GAUSE'S PRINCIPLE & COMPETITIVE COEXISTENCE:</strong>
  <ul>
    <li><strong>Gause's Competitive Exclusion Principle:</strong> Two closely related species competing for the exact same limiting resources cannot coexist indefinitely; the competitively inferior species will eventually be eliminated.</li>
    <li><strong>Resource Partitioning (MacArthur, 1958):</strong> Avoidance of competition by choosing different foraging times or behavioral patterns. Five closely related species of warblers coexisting peacefully on the same spruce tree!</li>
  </ul>
</div>
"""

    m11_revision = r"""
<div class="quick-revision-box">
  <h4>High-Yield Revision — Organisms and Populations</h4>
  <ul>
    <li><strong>Homeostasis:</strong> Regulate (mammals/birds core 37°C), Conform (99% animals), Migrate (Siberian cranes at Keoladeo), Suspend (diapause in zooplankton, hibernation in bears, aestivation in snails).</li>
    <li><strong>Adaptations:</strong> Allen's rule (shorter extremities in cold); Kangaroo rat (metabolic water oxidation); Altitude sickness (hypoxia counteracted by increased RBCs, decreased Hb affinity, hyperventilation).</li>
    <li><strong>Growth Models:</strong>
      <ul>
        <li>Exponential: $dN/dt = rN$ (J-shaped, unlimited resources).</li>
        <li>Logistic (Verhulst-Pearl): $dN/dt = rN((K-N)/K)$ (S-shaped sigmoid, carrying capacity K).</li>
      </ul>
    </li>
    <li><strong>Interactions:</strong>
      <ul>
        <li>Mutualism ($+/+$): Fig & Wasp, Ophrys orchid pseudo-copulation.</li>
        <li>Competition ($-/-$): Gause's exclusion vs MacArthur's warbler resource partitioning.</li>
        <li>Commensalism ($+/0$): Orchid on mango, Barnacles on whale, Egret & Cattle.</li>
        <li>Amensalism ($-/0$): Penicillium inhibiting bacteria. Brood parasitism: Cuckoo & Crow.</li>
      </ul>
    </li>
  </ul>
</div>
"""

    m11_flashcards = [
      {"q": "State Allen's Rule and explain its physiological significance.", "a": "Mammals living in colder climates possess shorter ears and limbs (extremities) compared to temperate relatives, which minimizes surface area-to-volume ratio and reduces heat loss."},
      {"q": "How does the human body physiologically adapt to high-altitude hypoxia (>3500 m)?", "a": "The body compensates for low atmospheric pO2 by: 1. Increasing red blood cell (RBC) production, 2. Decreasing the binding affinity of hemoglobin to facilitate oxygen release to tissues, and 3. Increasing breathing rate."},
      {"q": "Write the Verhulst-Pearl Logistic Growth equation and define each variable.", "a": "dN/dt = rN((K - N)/K), where N is population density, r is the intrinsic rate of natural increase, and K is the carrying capacity of the environment."},
      {"q": "What is Gause's Competitive Exclusion Principle and when does it apply?", "a": "Two closely related species competing for the exact same limiting resource cannot coexist indefinitely; the competitively superior species eliminates the inferior one. It applies when resources are limiting."},
      {"q": "How do MacArthur's warblers overcome competitive exclusion to coexist on the same tree?", "a": "Through Resource Partitioning: five distinct warbler species adapted to forage in different zones of the spruce tree at different times of day, avoiding direct competition."},
      {"q": "Give two classic examples of Commensalism (+/0) described in NCERT.", "a": "1. An epiphyte orchid growing on a mango branch (orchid gets support and sunlight; tree is unaffected), 2. Cattle egrets foraging near grazing livestock to feed on flushed insects."}
    ]

    m11_flow = [
      {"id": "op1", "title": "Abiotic Stress Response", "badge": "Step 1", "desc": "Organisms encounter temperature, water, or light stress; respond by regulating, conforming, migrating, or suspending."},
      {"id": "op2", "title": "Adaptive Plasticity", "badge": "Step 2", "desc": "Morphological (CAM in cactus, blubber in seals) and physiological adaptations (altitude RBC compensation)."},
      {"id": "op3", "title": "Population Metrics", "badge": "Step 3", "desc": "Quantifying birth rate, death rate, and sex ratio; constructing expanding, stable, or declining age pyramids."},
      {"id": "op4", "title": "Growth Dynamics", "badge": "Step 4", "desc": "Exponential J-curve (dN/dt = rN) shifts to Verhulst-Pearl Logistic Sigmoid curve (dN/dt = rN(K-N)/K) as resources limit."},
      {"id": "op5", "title": "Species Interactions", "badge": "Step 5", "desc": "Mutualism (+/+), Competition (-/-), Predation (+/-), Parasitism (+/-), Commensalism (+/0), and Amensalism (-/0)."},
      {"id": "op6", "title": "Coexistence Equilibrium", "badge": "Step 6", "desc": "Resource partitioning (MacArthur warblers) and co-evolution maintain long-term biodiversity balance in ecological communities."}
    ]

    m11_mindmap = {
      "id": "root", "title": "Organisms & Pop.", "icon": "🦊", "children": [
        {"id": "abiotic", "title": "Abiotic & Responses", "icon": "🌡️", "children": [
          {"id": "ab1", "title": "Factors: Temperature (Eury/Stenothermal), Water, Light, Soil"},
          {"id": "ab2", "title": "Responses: Regulate, Conform (99%), Migrate (Keoladeo), Suspend (Diapause)"},
          {"id": "ab3", "title": "Adaptations: Allen's rule, Kangaroo rat, Altitude hypoxia compensation"}
        ]},
        {"id": "growth", "title": "Growth Models", "icon": "📈", "children": [
          {"id": "gm1", "title": "Exponential: dN/dt = rN (J-shaped, unlimited resources)"},
          {"id": "gm2", "title": "Logistic: dN/dt = rN((K-N)/K) (Sigmoid, Carrying capacity K)"},
          {"id": "gm3", "title": "Population density: Nt+1 = Nt + [(B+I) - (D+E)]"}
        ]},
        {"id": "interactions", "title": "Population Interactions", "icon": "🤝", "children": [
          {"id": "in1", "title": "Mutualism (+/+): Lichens, Mycorrhizae, Fig & Wasp, Ophrys orchid"},
          {"id": "in2", "title": "Competition (-/-): Gause exclusion vs MacArthur resource partitioning"},
          {"id": "in3", "title": "Parasitism & Predation (+/-): Brood parasitism (Cuckoo), Monarch defense"},
          {"id": "in4", "title": "Commensalism (+/0): Orchid on mango; Amensalism (-/0): Penicillium"}
        ]}
      ]
    }

    m11_pages = [
      {"page_num": 1, "text": "Organisms and environment: Temperature is the most relevant abiotic factor. Responses include regulation in mammals and birds, conforming in 99% animals, migration like Siberian cranes to Keoladeo Ghana sanctuary, and suspension like diapause in zooplankton. Allen's rule states colder climate mammals have shorter ears and limbs."},
      {"page_num": 2, "text": "Population growth models: Exponential growth dN/dt = rN produces a J-shaped curve when resources are unlimited. Verhulst-Pearl Logistic growth dN/dt = rN((K-N)/K) produces a sigmoid curve where K is carrying capacity. Age pyramids can be expanding, stable, or declining."},
      {"page_num": 3, "text": "Population interactions: Mutualism benefits both species like fig and wasp or Ophrys orchid sexual deceit. Gause competitive exclusion principle states two species competing for identical limited resource cannot coexist, but MacArthur showed warblers coexist through resource partitioning. Commensalism benefits one like orchid on mango branch."}
    ]

    topics.append({
      "id": "bio-ch11-organisms-populations",
      "title": "11. Organisms and Populations",
      "subject": "bio",
      "subject_title": "Biology • Class 12",
      "reading_time_min": 15,
      "has_handwritten": False,
      "detailed_html": m11_detailed,
      "revision_html": m11_revision,
      "flashcards": m11_flashcards,
      "flow_data": m11_flow,
      "mindmap_data": m11_mindmap,
      "pages": m11_pages
    })

    # =========================================================================
    # MODULE 12: ECOSYSTEM
    # =========================================================================
    m12_detailed = r"""
<div class="topic-header">
  <span class="topic-num">UNIT X • TOPIC 12 OF 13</span>
  <h3 class="topic-title">Ecosystem</h3>
</div>

<div class="concept-card">
  <div class="card-label">ECOSYSTEM STRUCTURE & PRIMARY PRODUCTIVITY</div>
  <p>An ecosystem is a functional unit of nature where living organisms interact among themselves and with the physical environment. Four basic structural and functional aspects: <strong>Productivity, Decomposition, Energy Flow, and Nutrient Cycling</strong>.</p>
  <ul>
    <li><strong>Stratification:</strong> Vertical distribution of different species occupying different levels (e.g. in a forest: trees occupy top vertical strata, shrubs middle, herbs and grasses the forest floor).</li>
    <li><strong>Productivity:</strong> Rate of biomass production per unit area over a time period ($\text{g/m}^2/\text{yr}$ or $\text{kcal/m}^2/\text{yr}$):
      <ul>
        <li><strong>Gross Primary Productivity (GPP):</strong> Total rate of synthesis of organic matter by producers during photosynthesis.</li>
        <li><strong>Net Primary Productivity (NPP):</strong> Biomass remaining available for heterotrophs (herbivores and decomposers) after respiratory loss:
          <div class="formula-block">
            $NPP = GPP - R$<br>
            where $R$ = Respiration loss by plants.
          </div>
        </li>
        <li><em>Global Biosphere NPP:</em> Annual net primary productivity of whole biosphere is ~<strong>$170\text{ billion tons}$</strong> (dry weight). Oceans occupy $70\%$ of Earth's surface but contribute only <strong>$55\text{ billion tons}$</strong> due to light limitation and nutrient deficiency!</li>
      </ul>
    </li>
  </ul>
</div>

<div class="concept-card">
  <div class="card-label">DECOMPOSITION DYNAMICS (5 STEPS)</div>
  <p>Breakdown of complex organic matter from <strong>detritus</strong> (dead plant remains: leaves, bark, flowers; dead animal remains and fecal matter) into inorganic substances ($CO_2, H_2O$, nutrients):</p>
  <ol>
    <li><strong>Fragmentation:</strong> Detritivores (e.g. <strong>Earthworms</strong>) break down detritus into smaller particles, increasing surface area.</li>
    <li><strong>Leaching:</strong> Water-soluble inorganic nutrients percolate into soil horizon and precipitate as unavailable salts.</li>
    <li><strong>Catabolism:</strong> Bacterial and fungal enzymes degrade detrital fragments into simpler inorganic substances.</li>
    <li><strong>Humification:</strong> Leads to accumulation of a dark-colored, amorphous colloidal substance called <strong>Humus</strong> (highly resistant to microbial action, extremely slow decomposition, nutrient reservoir).</li>
    <li><strong>Mineralization:</strong> Degradation of humus by specialized microbes releasing inorganic nutrients back into soil.</li>
  </ol>
  <div class="remember-box">
    <strong>Decomposition Kinetics:</strong> Slower if detritus is rich in <em>lignin and chitin</em>; faster if rich in <em>nitrogen and water-soluble sugars</em>. Warm, moist environments dramatically accelerate decomposition; low temperatures and anaerobiosis inhibit it.
  </div>
</div>

<div class="concept-card">
  <div class="card-label">ENERGY FLOW & FOOD CHAINS</div>
  <ul>
    <li>Sun is the sole source of energy for all ecosystems (except deep sea hydrothermal vents).</li>
    <li><strong>Photosynthetically Active Radiation (PAR):</strong> Accounts for <strong>$<50\%$</strong> of incident solar radiation. Plants capture only <strong>$2\text{--}10\%$ of PAR</strong> ($1\text{--}5\%$ of total solar radiation) to sustain the entire living world!</li>
    <li><strong>Food Chain Architectures:</strong>
      <ul>
        <li><strong>Grazing Food Chain (GFC):</strong> Starts with living photosynthetic autotrophs (Producers $\to$ Herbivore $\to$ Carnivore). In <strong>aquatic ecosystems</strong>, GFC is the major conduit for energy flow.</li>
        <li><strong>Detritus Food Chain (DFC):</strong> Starts with dead organic matter / detritus $\to$ Decomposers (Fungi and Bacteria - Saprotrophs). In <strong>terrestrial ecosystems</strong>, a much larger fraction of energy flows through DFC than GFC.</li>
      </ul>
    </li>
    <li><strong>Lindeman's 10% Law:</strong> Only <strong>$10\%$</strong> of the energy available at a trophic level is transferred to the next higher trophic level; $90\%$ is lost as metabolic heat during respiration.</li>
  </ul>
</div>

<div class="table-container">
  <div class="table-caption">NCERT Comparison: Ecological Pyramids</div>
  <table class="notes-table">
    <thead>
      <tr><th>Pyramid Type</th><th>Typical Shape</th><th>Exception / Inverted Condition</th></tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Pyramid of Numbers</strong></td>
        <td><strong>Upright</strong> in Grassland and Pond ecosystems (millions of producers support fewer carnivores)</td>
        <td><strong>Inverted / Spindle-shaped</strong> in Tree Ecosystem: Single large tree ($1$) supports thousands of herbivorous birds ($100$), which support millions of hyperparasites ($10,000$).</td>
      </tr>
      <tr>
        <td><strong>Pyramid of Biomass</strong></td>
        <td><strong>Upright</strong> in Terrestrial ecosystems (forest, grassland)</td>
        <td><strong>Inverted in Aquatic / Marine Ecosystem:</strong> Biomass of phytoplankton producers is far less than biomass of predatory fishes (phytoplanktons have high turnover rate and short lifespan).</td>
      </tr>
      <tr>
        <td><strong>Pyramid of Energy</strong></td>
        <td><strong>ALWAYS UPRIGHT without exception</strong></td>
        <td><strong>NO EXCEPTIONS!</strong> Energy decreases progressively at each successive trophic level according to second law of thermodynamics.</td>
      </tr>
    </tbody>
  </table>
</div>

<div class="concept-card">
  <div class="card-label">ECOLOGICAL SUCCESSION: HYDRARCH & XERARCH</div>
  <p>Predictable, orderly, directional process of change in species composition of a given area over ecological time: <strong>Pioneer species $\to$ Seral communities $\to$ Climax community</strong> (in equilibrium with environment).</p>
  <ul>
    <li><em>Primary Succession:</em> Occurs on newly formed bare substrate where no life ever existed (bare rock, newly cooled lava, newly submerged sand dune). Extremely slow (hundreds to thousands of years to build soil).</li>
    <li><em>Secondary Succession:</em> Occurs in areas where previous biological communities were destroyed (burned forests, flooded lands, abandoned farmlands). Much faster because soil is already present.</li>
    <li><strong>Succession Pathways converge on Mesic (Moderate Water) Conditions:</strong>
      <ul>
        <li><strong>Hydrarch Succession (in water bodies):</strong> Phytoplankton (pioneers) $\to$ Submerged plants (<em>Hydrilla</em>) $\to$ Submerged free-floating plants (<em>Pistia</em>) $\to$ Reed-swamp stage (<em>Typha</em>) $\to$ Marsh-meadow $\to$ Scrub $\to$ <strong>Forest (Climax mesic)</strong>.</li>
        <li><strong>Xerarch Succession (on dry bare rocks):</strong> Crustose Lichens (pioneers secreting acids to weather rock) $\to$ Foliose Lichens $\to$ Mosses $\to$ Annual grasses $\to$ Perennial herbs $\to$ Shrubs $\to$ <strong>Forest (Climax mesic)</strong>.</li>
      </ul>
    </li>
  </ul>
</div>
"""

    m12_revision = r"""
<div class="quick-revision-box">
  <h4>High-Yield Revision — Ecosystem</h4>
  <ul>
    <li><strong>Productivity:</strong> $NPP = GPP - R$. Biosphere annual NPP = 170 billion tons (oceans contribute only 55 billion tons despite 70% area).</li>
    <li><strong>Decomposition Steps:</strong> Fragmentation (earthworm) $\to$ Leaching $\to$ Catabolism (enzymes) $\to$ Humification (humus) $\to$ Mineralization.</li>
    <li><strong>Energy Flow:</strong> PAR < 50% solar radiation; plants capture 2-10% PAR. Lindeman's 10% law.</li>
    <li><strong>Aquatic vs Terrestrial Conduit:</strong> Aquatic = GFC major conduit; Terrestrial = DFC major conduit.</li>
    <li><strong>Pyramids:</strong> Energy is ALWAYS upright. Biomass is INVERTED in sea/ocean (phytoplankton < zooplankton/fish). Numbers inverted on single tree.</li>
    <li><strong>Succession:</strong> Both Hydrarch (wet) and Xerarch (dry) converge to stable Mesic Forest climax. Pioneer on rock = Lichens; Pioneer in water = Phytoplankton.</li>
  </ul>
</div>
"""

    m12_flashcards = [
      {"q": "Why is the annual net primary productivity of oceans only 55 billion tons despite covering 70% of Earth?", "a": "Due to limited light penetration in deep waters and severe scarcity of essential mineral nutrients (like nitrogen and iron) across vast open pelagic zones."},
      {"q": "What are the 5 sequential steps of the decomposition process?", "a": "1. Fragmentation (detritivores), 2. Leaching (water-soluble salts wash down), 3. Catabolism (microbial enzymes), 4. Humification (dark amorphous humus formation), and 5. Mineralization (inorganic nutrient release)."},
      {"q": "Why is the Pyramid of Energy always strictly upright without any exceptions?", "a": "According to the Second Law of Thermodynamics, energy is irreversibly dissipated as respiratory metabolic heat at each trophic transfer; thus, higher trophic levels invariably receive less energy."},
      {"q": "Under what condition is the Pyramid of Biomass inverted?", "a": "In aquatic/marine ecosystems, where the standing crop biomass of phytoplankton producers is smaller than that of zooplanktons and fishes due to the phytoplanktons' microscopic size, rapid life cycle, and high turnover rate."},
      {"q": "What are the pioneer species in Xerarch succession versus Hydrarch succession?", "a": "In Xerarch succession on bare rock, pioneer species are lichens (secreting weathering acids). In Hydrarch succession in water, pioneer species are microscopic phytoplanktons."},
      {"q": "What is the ultimate climatic endpoint of both Hydrarch and Xerarch succession?", "a": "Both successional pathways converge on a medium moisture (Mesic) climax community, typically a stable mature forest."}
    ]

    m12_flow = [
      {"id": "ec1", "title": "Solar Energy Capture", "badge": "Step 1", "desc": "Producers capture 2-10% PAR via photosynthesis; Gross Primary Productivity (GPP) minus respiration leaves Net Primary Productivity (NPP)."},
      {"id": "ec2", "title": "Trophic Energy Transfer", "badge": "Step 2", "desc": "Energy transfers through GFC (aquatic) and DFC (terrestrial); only 10% passes to next level (Lindeman's law)."},
      {"id": "ec3", "title": "Decomposition Cascade", "badge": "Step 3", "desc": "Earthworms fragment detritus -> Leaching -> Bacterial catabolism -> Humus accumulation -> Mineralization."},
      {"id": "ec4", "title": "Pyramidal Thermodynamics", "badge": "Step 4", "desc": "Energy pyramid stays strictly upright; biomass pyramid inverts in oceans; numbers pyramid inverts on a single tree."},
      {"id": "ec5", "title": "Primary & Secondary Succession", "badge": "Step 5", "desc": "Pioneer lichens/phytoplankton colonize bare terrain; serial communities replace one another over decades."},
      {"id": "ec6", "title": "Climax Equilibrium", "badge": "Step 6", "desc": "Convergence of hydric and xeric series to stable mesic forest community in balance with regional climate."}
    ]

    m12_mindmap = {
      "id": "root", "title": "Ecosystem", "icon": "🌲", "children": [
        {"id": "productivity", "title": "Productivity & Decomp.", "icon": "🍂", "children": [
          {"id": "pr1", "title": "Productivity: NPP = GPP - R; Biosphere = 170 billion tons (Oceans: 55)"},
          {"id": "pr2", "title": "Decomposition: Fragmentation -> Leaching -> Catabolism -> Humus -> Minerals"}
        ]},
        {"id": "energy", "title": "Energy Flow & Chains", "icon": "⚡", "children": [
          {"id": "en1", "title": "PAR < 50% solar; Plants capture 2-10% PAR; Lindeman 10% law"},
          {"id": "en2", "title": "Grazing (GFC - major in aquatic) vs Detritus (DFC - major in terrestrial)"}
        ]},
        {"id": "pyramids", "title": "Ecological Pyramids", "icon": "🔺", "children": [
          {"id": "py1", "title": "Energy: ALWAYS upright (no exceptions)"},
          {"id": "py2", "title": "Biomass: Inverted in aquatic/sea (phytoplankton < fish)"},
          {"id": "py3", "title": "Numbers: Inverted on single tree ecosystem"}
        ]},
        {"id": "succession", "title": "Ecological Succession", "icon": "🌱", "children": [
          {"id": "sc1", "title": "Primary (bare rock/lava) vs Secondary (burnt forest, soil present)"},
          {"id": "sc2", "title": "Hydrarch (Phytoplankton pioneer) & Xerarch (Lichen pioneer)"},
          {"id": "sc3", "title": "Both converge to Mesic Forest climax"}
        ]}
      ]
    }

    m12_pages = [
      {"page_num": 1, "text": "Ecosystem productivity and decomposition: Gross primary productivity GPP minus respiration equals net primary productivity NPP. Global biosphere produces 170 billion tons dry weight with oceans producing only 55 billion tons. Decomposition has 5 steps: fragmentation by earthworms, leaching, catabolism, humification forming humus, and mineralization."},
      {"page_num": 2, "text": "Energy flow follows 10% law of Lindeman. Photosynthetically active radiation PAR is under 50% of sunlight. Grazing food chain GFC is dominant in aquatic environments while detritus food chain DFC dominates terrestrial environments. Pyramid of energy is always upright without exception."},
      {"page_num": 3, "text": "Ecological pyramids and succession: Pyramid of biomass is inverted in aquatic ocean ecosystems because phytoplankton biomass is less than fish. Pyramid of numbers is inverted in tree ecosystem. Succession proceeds from pioneer species (lichens on rock, phytoplankton in water) through seral stages to climax mesic forest."}
    ]

    topics.append({
      "id": "bio-ch12-ecosystem",
      "title": "12. Ecosystem",
      "subject": "bio",
      "subject_title": "Biology • Class 12",
      "reading_time_min": 14,
      "has_handwritten": False,
      "detailed_html": m12_detailed,
      "revision_html": m12_revision,
      "flashcards": m12_flashcards,
      "flow_data": m12_flow,
      "mindmap_data": m12_mindmap,
      "pages": m12_pages
    })

    # =========================================================================
    # MODULE 13: BIODIVERSITY AND CONSERVATION
    # =========================================================================
    m13_detailed = r"""
<div class="topic-header">
  <span class="topic-num">UNIT X • TOPIC 13 OF 13</span>
  <h3 class="topic-title">Biodiversity and Conservation</h3>
</div>

<div class="concept-card">
  <div class="card-label">BIODIVERSITY LEVELS & GLOBAL ESTIMATES</div>
  <p>Biodiversity is the totality of genes, species, and ecosystems of a region, popularized by sociobiologist <strong>Edward Wilson</strong>.</p>
  <ul>
    <li><strong>Three Hierarchical Levels of Biodiversity:</strong>
      <ol>
        <li><em>Genetic Diversity:</em> Genetic variation within a single species. E.g., medicinal plant <em>Rauwolfia vomitoria</em> in Himalayan ranges shows genetic variation in potency and concentration of active chemical <strong>Reserpine</strong>. India possesses $>50,000$ genetically distinct strains of <strong>Rice</strong> and $>1,000$ varieties of <strong>Mango</strong>.</li>
        <li><em>Species Diversity:</em> Diversity at the species level. E.g., <strong>Western Ghats have greater amphibian species diversity</strong> than Eastern Ghats.</li>
        <li><em>Ecological Diversity:</em> Diversity of ecosystems. India (with deserts, rainforests, mangroves, coral reefs, alpine meadows) has far greater ecological diversity than Scandinavian countries like Norway.</li>
      </ol>
    </li>
    <li><strong>Global Species Counts (Robert May's Estimate):</strong>
      <ul>
        <li>IUCN (2004): Slightly over $1.5\text{ million}$ species described.</li>
        <li>Robert May's scientifically sound global estimate = <strong>~7 million species</strong>.</li>
        <li>Animals constitute <strong>$>70\%$</strong> of all recorded species; plants (including algae, fungi, bryophytes, pteridophytes, gymnosperms, angiosperms) comprise ~<strong>$22\%$</strong>.</li>
        <li>Among animals, <strong>Insects constitute $>70\%$</strong> (out of every 10 animals on Earth, 7 are insects!). Fungi species outnumber the combined total of fishes, amphibians, reptiles, and mammals!</li>
        <li><em>India's Megadiversity:</em> India has only <strong>$2.4\%$</strong> of world's land area, but shares an impressive <strong>$8.1\%$</strong> of global species diversity! One of the <strong>12 mega-diversity countries</strong> of the world.</li>
      </ul>
    </li>
  </ul>
</div>

<div class="concept-card">
  <div class="card-label">PATTERNS OF BIODIVERSITY & SPECIES-AREA RELATIONSHIP</div>
  <ul>
    <li><strong>Latitudinal Gradients:</strong> Species diversity decreases as we move away from equator toward poles.
      <ul>
        <li>Tropics ($23.5^\circ\text{N}$ to $23.5^\circ\text{S}$) harbor far more species than temperate or polar zones. E.g., Colombia near equator has 1,400 bird species; New York ($41^\circ\text{N}$) has 105; Greenland ($71^\circ\text{N}$) has only 56.</li>
        <li><strong>Amazonian Rainforest (South America):</strong> Greatest biodiversity on Earth: $>40,000$ plant species, $3,000$ fishes, $1,300$ birds, $427$ mammals, $427$ amphibians, $378$ reptiles, $>125,000$ invertebrates!</li>
        <li><em>Why Tropics Have Higher Diversity:</em> 1. Tropical latitudes have remained unglaciated and undisturbed for millions of years (more speciation time), 2. Tropical environments are more constant and predictable, promoting niche specialization, 3. Greater solar energy input drives higher productivity.</li>
      </ul>
    </li>
    <li><strong>Species-Area Relationship (Alexander von Humboldt):</strong>
      <p>German naturalist observed that within a region, species richness increases with increasing explored area, but only up to a limit. On a rectangular graph it forms a <strong>rectangular hyperbola</strong>; on a logarithmic scale, it is a straight line:</p>
      <div class="formula-block">
        $\log S = \log C + Z \log A$<br>
        where $S$ = Species richness, $A$ = Area, $Z$ = Slope of line (regression coefficient), $C$ = $Y$-intercept.
      </div>
      <ul>
        <li>For small regions (plants in Britain, birds in California): $Z$ value is remarkably constant at <strong>$0.1\text{ to }0.2$</strong>.</li>
        <li>For entire continents (frugivorous birds and mammals in tropical forests): slope is much steeper, $Z = \mathbf{0.6\text{ to }1.2}$ ($Z = 1.15$).</li>
      </ul>
    </li>
  </ul>
</div>

<div class="concept-card">
  <div class="card-label">LOSS OF BIODIVERSITY: THE "EVIL QUARTET"</div>
  <p>Current human-induced extinction rates are estimated to be <strong>100 to 1,000 times faster</strong> than pre-human background extinction rates. The four major causes ("The Evil Quartet") are:</p>
  <ol>
    <li><strong>Habitat Loss & Fragmentation (Most Important Cause):</strong> Amazon rainforest ("Lungs of our planet") is being cut and cleared for cultivating <strong>soybeans</strong> and converting to beef cattle pasture. Large habitats broken into small fragments affect mammals and birds requiring large territories.</li>
    <li><strong>Over-Exploitation:</strong> Excessive human greed led to extinction of <strong>Steller's Sea Cow</strong> and <strong>Passenger Pigeon</strong> in the last 500 years. Marine fish populations over-harvested.</li>
    <li><strong>Alien Species Invasions:</strong> Non-native species become invasive, wiping out indigenous species:
      <ul>
        <li><strong>Nile Perch</strong> introduced into Lake Victoria in East Africa caused extinction of $>200$ species of native cichlid fish.</li>
        <li>Invasive weeds: <em>Parthenium</em> (carrot grass), <em>Lantana</em>, and <strong><em>Eichhornia</em> (water hyacinth - "Terror of Bengal")</strong>.</li>
        <li>African catfish <strong><em>Clarias gariepinus</em></strong> illegally introduced for aquaculture threatens indigenous catfishes in Indian rivers.</li>
      </ul>
    </li>
    <li><strong>Co-extinctions:</strong> When a species becomes extinct, any plant or animal obligately associated with it also becomes extinct (e.g. host fish and its specific parasite; coevolved plant-pollinator mutualism).</li>
  </ol>
</div>

<div class="remember-box">
  <strong>BIODIVERSITY CONSERVATION STRATEGIES:</strong>
  <ul>
    <li><strong>Why Conserve?</strong>
      <ul>
        <li><em>Narrowly Utilitarian:</em> Direct economic benefits: food (cereals, pulses), firewood, fiber, construction, industrial tannins/dyes, $>25\%$ of prescription drugs derived from plants (<strong>Bioprospecting</strong>).</li>
        <li><em>Broadly Utilitarian:</em> Ecosystem services: Amazon produces $20\%$ of Earth's $O_2$; pollination by bees; flood/erosion control; aesthetic joy.</li>
        <li><em>Ethical:</em> Moral responsibility to preserve all living species for future generations.</li>
      </ul>
    </li>
    <li><strong>In-Situ (On-Site) Conservation:</strong> Protecting endangered species in their natural habitat:
      <ul>
        <li><strong>Biodiversity Hotspots:</strong> Regions with exceptionally high species richness and high degree of <strong>endemism</strong> (species confined to that region and found nowhere else). 34 hotspots worldwide covering $<2\%$ of Earth's land, but strict protection reduces extinction by $30\%$. <strong>3 Hotspots cover India:</strong> 1. Western Ghats and Sri Lanka, 2. Indo-Burma, 3. Himalaya.</li>
        <li><strong>Protected Areas in India:</strong> 14 Biosphere Reserves, 90 National Parks, 448 Wildlife Sanctuaries.</li>
        <li><strong>Sacred Groves:</strong> Undisturbed forest patches protected by tribal religious traditions: <em>Khasi and Jaintia Hills in Meghalaya</em> (last refuges for rare plants), <em>Aravalli Hills in Rajasthan</em>, <em>Western Ghats of Karnataka and Maharashtra</em>, <em>Sarguja, Chanda, Bastar in MP</em>.</li>
      </ul>
    </li>
    <li><strong>Ex-Situ (Off-Site) Conservation:</strong> Threatened animals and plants taken out of natural habitat and placed in special care settings:
      <ul>
        <li>Zoological Parks, Botanical Gardens, Wildlife Safari Parks.</li>
        <li>Advanced biotechnological methods: <strong>Cryopreservation</strong> of gametes in liquid nitrogen at $-196^\circ\text{C}$ in viable form; In vitro fertilization; Tissue culture propagation; <strong>Seed Banks</strong>.</li>
      </ul>
    </li>
    <li><strong>International Conventions:</strong>
      <ul>
        <li><strong>The Earth Summit (Rio de Janeiro, 1992):</strong> Convention on Biological Diversity calling all nations to conserve biodiversity.</li>
        <li><strong>World Summit on Sustainable Development (Johannesburg, South Africa, 2002):</strong> 190 countries pledged commitment to significantly reduce biodiversity loss rate.</li>
      </ul>
    </li>
  </ul>
</div>
"""

    m13_revision = r"""
<div class="quick-revision-box">
  <h4>High-Yield Revision — Biodiversity & Conservation</h4>
  <ul>
    <li><strong>Robert May's Estimate:</strong> ~7 million species worldwide. India = 2.4% land area, 8.1% global species diversity (12 megadiverse nations).</li>
    <li><strong>Species-Area Relationship:</strong> $\log S = \log C + Z \log A$ (Humboldt). Z = 0.1-0.2 (regional), Z = 0.6-1.2 (continental, 1.15 for tropical frugivores).</li>
    <li><strong>Evil Quartet:</strong> 1. Habitat loss/fragmentation (Amazon for soy), 2. Over-exploitation (Steller's sea cow, Passenger pigeon), 3. Alien invasion (Nile perch, Water hyacinth, Clarias gariepinus), 4. Co-extinction.</li>
    <li><strong>Biodiversity Hotspots:</strong> 34 globally; high endemism. 3 in India: Western Ghats-Sri Lanka, Indo-Burma, Himalaya.</li>
    <li><strong>Sacred Groves:</strong> Khasi & Jaintia hills (Meghalaya), Aravalli (Rajasthan), Western Ghats.</li>
    <li><strong>Ex-Situ:</strong> Cryopreservation ($-196^\circ\text{C}$ liquid $N_2$), Seed banks, Botanical gardens, Zoos.</li>
    <li><strong>Conventions:</strong> Earth Summit (Rio 1992); World Summit on Sustainable Development (Johannesburg 2002).</li>
  </ul>
</div>
"""

    m13_flashcards = [
      {"q": "What is the mathematical equation for Alexander von Humboldt's Species-Area Relationship?", "a": "log S = log C + Z log A, where S is species richness, A is area, C is the y-intercept, and Z is the regression coefficient (slope of the line)."},
      {"q": "What are the four major causes of biodiversity loss collectively known as 'The Evil Quartet'?", "a": "1. Habitat loss and fragmentation, 2. Over-exploitation, 3. Alien species invasions, and 4. Co-extinctions."},
      {"q": "Name the three biodiversity hotspots that extend into India's geographical territory.", "a": "1. Western Ghats and Sri Lanka, 2. Indo-Burma, and 3. Himalaya."},
      {"q": "What is an ecological endemic species?", "a": "A species that is confined exclusively to a particular geographic region and is not found anywhere else in the world."},
      {"q": "Give two prominent examples of animal species driven to extinction by over-exploitation.", "a": "Steller's Sea Cow and the Passenger Pigeon."},
      {"q": "What is the difference between In-Situ and Ex-Situ conservation? Give two examples of each.", "a": "In-situ protects species within their natural ecosystem (National Parks, Biosphere Reserves). Ex-situ protects endangered species outside their natural habitat (Cryopreservation, Zoological Parks)."}
    ]

    m13_flow = [
      {"id": "bd1", "title": "Biodiversity Distribution", "badge": "Step 1", "desc": "Genetic (Rauwolfia), species (Western Ghats amphibians), and ecological diversity; Amazon rainforest maximum."},
      {"id": "bd2", "title": "Humboldt's Curve", "badge": "Step 2", "desc": "log S = log C + Z log A; Z=0.1-0.2 for regions, scaling to Z=0.6-1.2 across entire continents."},
      {"id": "bd3", "title": "Ecosystem Rivet Popping", "badge": "Step 3", "desc": "Tilman plots show higher diversity enhances stability; Paul Ehrlich's rivet popper hypothesis warns against keystone loss."},
      {"id": "bd4", "title": "The Evil Quartet", "badge": "Step 4", "desc": "Anthropogenic extinction through habitat fragmentation, over-harvesting, invasive aliens (Nile perch), and co-extinctions."},
      {"id": "bd5", "title": "In-Situ Hotspots & Reserves", "badge": "Step 5", "desc": "Protection of 34 global hotspots (Western Ghats, Indo-Burma, Himalaya), 14 biosphere reserves, and sacred groves."},
      {"id": "bd6", "title": "Ex-Situ Cryopreservation", "badge": "Step 6", "desc": "Preserving gametes in liquid nitrogen at -196°C, operating seed banks, and adhering to Earth Summit mandates."}
    ]

    m13_mindmap = {
      "id": "root", "title": "Biodiversity & Conserv.", "icon": "🌍", "children": [
        {"id": "diversity", "title": "Diversity Patterns", "icon": "🌴", "children": [
          {"id": "dv1", "title": "Levels: Genetic (Rauwolfia reserpine), Species (Amphibians), Ecological"},
          {"id": "dv2", "title": "Robert May: ~7 million species (Animals >70%, Insects >70% animals)"},
          {"id": "dv3", "title": "Species-Area: log S = log C + Z log A (Humboldt, Z=0.1-0.2 vs 0.6-1.2)"}
        ]},
        {"id": "loss", "title": "The Evil Quartet", "icon": "⚠️", "children": [
          {"id": "ls1", "title": "Habitat Loss & Fragmentation: Amazon cleared for soy/cattle"},
          {"id": "ls2", "title": "Over-exploitation: Steller's sea cow, Passenger pigeon"},
          {"id": "ls3", "title": "Alien Invasions: Nile perch (Lake Victoria), Water hyacinth (Eichhornia)"},
          {"id": "ls4", "title": "Co-extinctions: Obligate plant-pollinator mutualisms"}
        ]},
        {"id": "conservation", "title": "Conservation Methods", "icon": "🛡️", "children": [
          {"id": "cs1", "title": "In-situ: 34 Hotspots (Western Ghats, Indo-Burma, Himalaya), Sacred groves"},
          {"id": "cs2", "title": "Ex-situ: Cryopreservation (-196°C liquid N2), Seed banks, Zoos"},
          {"id": "cs3", "title": "Conventions: Earth Summit (Rio 1992), World Summit (Johannesburg 2002)"}
        ]}
      ]
    }

    m13_pages = [
      {"page_num": 1, "text": "Biodiversity levels: Genetic diversity in Rauwolfia vomitoria producing reserpine, species diversity in Western Ghats amphibians, ecological diversity in Indian rainforests and deserts. Robert May estimated 7 million species with animals over 70% and insects making up 70% of animals. India has 8.1% of global biodiversity."},
      {"page_num": 2, "text": "Patterns of biodiversity: Tropics harbor more species than temperate zones with Amazon rainforest highest. Humboldt species-area relationship log S equals log C plus Z log A with Z between 0.1 and 0.2 for regions and 0.6 to 1.2 for continents. Tilman proved diversity increases ecosystem stability."},
      {"page_num": 3, "text": "The Evil Quartet causing biodiversity loss: habitat loss in Amazon forest, over-exploitation causing extinction of Steller's sea cow and passenger pigeon, alien species invasions like Nile perch and water hyacinth, and co-extinctions. Conservation in-situ includes 34 hotspots and sacred groves; ex-situ includes cryopreservation at -196°C and seed banks."}
    ]

    topics.append({
      "id": "bio-ch13-biodiversity-conservation",
      "title": "13. Biodiversity and Conservation",
      "subject": "bio",
      "subject_title": "Biology • Class 12",
      "reading_time_min": 14,
      "has_handwritten": False,
      "detailed_html": m13_detailed,
      "revision_html": m13_revision,
      "flashcards": m13_flashcards,
      "flow_data": m13_flow,
      "mindmap_data": m13_mindmap,
      "pages": m13_pages
    })
